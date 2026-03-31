# `cli.js.map` 说明文档

## 概览

`cli.js.map` 是 JavaScript Source Map 文件，用于将打包后的代码位置映射回原始源码位置，便于调试与错误定位。

该文件是 **Source Map v3**，并且包含了完整的 `sourcesContent`，意味着它不仅能用于行列号映射，还能直接暴露原始源码文本。

## 文件基本信息

[cli.js.map](https://unpkg.com/@anthropic-ai/claude-code@2.1.88/cli.js.map)

- 文件名：`cli.js.map`
- 大小：约 `59.8 MB`（`59766257` bytes）
- 版本：`version: 3`
- 顶层字段：
  - `version`
  - `sources`
  - `sourcesContent`
  - `mappings`
  - `names`

当前观测结果：

- `sources` 数量：`4756`
- `sourcesContent` 数量：`4756`（与 `sources` 一一对应）
- `mappings` 长度：约 `10,951,046` 字符
- `names` 为空数组
- `file`、`sourceRoot` 未设置（常见于独立 map 文件）

## 结构含义

### `sources`

记录原始源文件路径列表。例如：

- `../src/entrypoints/cli.tsx`
- `../src/cli/handlers/...`
- `../node_modules/...`

这说明打包结果不仅包含项目自身源码，也包含大量第三方依赖。

### `sourcesContent`

与 `sources` 对齐的源码文本数组。某个下标对应的 `sources[i]` 和 `sourcesContent[i]` 是同一个源文件。

当该字段存在且完整时，可以在没有源码仓库的情况下查看原始代码内容。

### `mappings`

VLQ 编码后的位置信息，建立“打包后代码位置 -> 原始文件/行/列”的映射关系。调试器和错误平台依赖它实现可读堆栈。

### `names`

可选符号名映射。该文件中为空，不影响主要的行列号映射和源码还原能力。

## 内容特征（本文件）

扩展名分布（按 `sources` 统计）：

- `.js`: 2626
- `.ts`: 1354
- `.tsx`: 552
- `.mjs`: 221
- `.cjs`: 3

可以看到该映射覆盖了大量 TypeScript/TSX 源代码与依赖源码。

## 能做什么

1. **错误定位**  
   将线上压缩堆栈还原到源文件和精确行列。

2. **调试体验提升**  
   在浏览器或 Node 调试器中直接查看原始 TS/TSX 代码。

3. **源码审计/逆向分析**  
   由于包含 `sourcesContent`，可直接分析实现逻辑、入口和依赖结构。

## 安全与发布风险

由于本文件包含完整源码文本，公开发布会带来以下风险：

- 暴露内部实现细节和架构信息
- 便于逆向分析业务逻辑
- 可能间接暴露敏感常量、内部路径、调试开关等信息

## 建议实践

1. **生产环境谨慎暴露 source map**  
   不对外公开下载，或通过鉴权仅对内部错误平台可见。

2. **按环境区分策略**  
   开发/测试环境可保留完整 map；生产环境可考虑不带 `sourcesContent`。

3. **发布前安全扫描**  
   对 map 和产物进行敏感信息扫描（密钥、token、内部地址、凭证片段）。

4. **最小化暴露范围**  
   仅上传到 Sentry 等错误平台，避免静态公开目录直接访问。

## 快速自检清单

- 是否真的需要在生产环境公开 `*.map`？
- 是否包含 `sourcesContent`？
- 是否做过敏感信息扫描？
- 是否限制了 map 文件访问权限？
- 是否有明确的保留/清理策略？

---

如果后续需要，可基于此文件继续补充：

- `cli` 入口执行链路（entrypoint -> handlers -> transports）
- 高风险字符串排查报告模板
- 与错误平台（如 Sentry）的上传和访问控制规范
