# 通过 `cli.js.map` 还原源码指南

## 目的

本文档说明如何从 `cli.js.map` 中恢复源码文件，并验证还原结果的完整性与可用性。

适用前提：

- `cli.js.map` 存在且可读取
- Source Map 包含 `sources` 与 `sourcesContent`
- `sources.length === sourcesContent.length`

## 还原原理

Source Map 的关键字段：

- `sources`：原始源文件路径列表
- `sourcesContent`：对应路径的源码文本

按索引一一对应：

- `sources[i]` 是路径
- `sourcesContent[i]` 是该路径文件内容

因此可通过遍历索引，将每对数据写回磁盘完成“源码恢复”。

## 目录策略建议

建议不要直接写回项目根目录，避免覆盖现有文件。推荐输出到独立目录，例如：

- `recovered-src/`：仅恢复业务源码（`../src/**`）
- `recovered-all/`：恢复全部（包含 `node_modules` 来源）

## 最小可用还原脚本（Python 3）

将以下脚本保存为 `scripts/recover_from_sourcemap.py`，然后执行。

```python
#!/usr/bin/env python3
import json
import os
from pathlib import Path

MAP_PATH = Path("cli.js.map")
OUT_DIR = Path("recovered-src")

# 是否只恢复 src 源码
ONLY_SRC = True

def normalize_source_path(source: str) -> str:
    # 常见路径形态: ../src/xxx.ts
    # 统一去掉 ../ 前缀，避免路径逃逸
    while source.startswith("../"):
        source = source[3:]
    # 去掉开头斜杠
    source = source.lstrip("/\\")
    return source

def is_safe_relative_path(path: str) -> bool:
    p = Path(path)
    return not any(part == ".." for part in p.parts)

def main() -> None:
    if not MAP_PATH.exists():
        raise FileNotFoundError(f"Source map not found: {MAP_PATH}")

    with MAP_PATH.open("r", encoding="utf-8") as f:
        data = json.load(f)

    sources = data.get("sources", [])
    sources_content = data.get("sourcesContent", [])

    if len(sources) != len(sources_content):
        raise ValueError(
            f"Length mismatch: sources={len(sources)} vs sourcesContent={len(sources_content)}"
        )

    OUT_DIR.mkdir(parents=True, exist_ok=True)

    written = 0
    skipped = 0

    for src, content in zip(sources, sources_content):
        if content is None:
            skipped += 1
            continue

        if ONLY_SRC and not src.startswith("../src/"):
            skipped += 1
            continue

        rel = normalize_source_path(src)
        if not is_safe_relative_path(rel):
            skipped += 1
            continue

        target = OUT_DIR / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content, encoding="utf-8")
        written += 1

    print(f"Done. written={written}, skipped={skipped}, out_dir={OUT_DIR}")

if __name__ == "__main__":
    main()
```

## 执行步骤

1. 在项目根目录创建脚本：
   - `scripts/recover_from_sourcemap.py`
2. 执行：
   - `python3 scripts/recover_from_sourcemap.py`
3. 查看输出目录：
   - `recovered-src/src/...`

## 完整还原（可选）

如果你希望恢复所有来源（包括依赖源码），将脚本中的：

- `ONLY_SRC = True` 改为 `ONLY_SRC = False`

然后重跑脚本，输出目录会显著增大。

## 结果验证

建议至少做三层验证：

1. **数量校验**  
   对比脚本输出的 `written` 数量与预期 `src` 文件数。

2. **关键入口校验**  
   检查关键文件是否存在，例如：
   - `recovered-src/src/entrypoints/cli.tsx`

3. **语法校验（可选）**  
   在恢复目录执行 TypeScript/ESLint 检查，确认文本内容无截断和编码问题。

## 常见问题

### 1) 为什么恢复后不能直接运行？

恢复的是源码文件，不等于完整工程。通常缺少：

- `package.json`
- 构建配置
- 锁文件
- 资源文件
- 脚本/CI 配置

### 2) 为什么有些文件被跳过？

可能原因：

- `sourcesContent[i]` 为 `null`
- 路径不在过滤范围（例如非 `../src/`）
- 安全路径检查未通过

### 3) 恢复代码和原仓库完全一致吗？

多数情况下逻辑非常接近，但不保证 100% 一致。原因包括：

- 构建时宏替换或条件编译
- 构建产物中路径标准化差异
- 某些虚拟模块并非真实文件

## 合规与安全说明

还原源码涉及知识产权和合规边界。请确保你对目标代码拥有合法授权，并遵循所在组织的安全规范。

对外共享还原结果前，建议先做敏感信息扫描与脱敏处理。
