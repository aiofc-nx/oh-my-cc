# 使用方法

<img src="./imgs/tudou.jpg" alt="交流群" width="40%" />

## 安装依赖

```bash
bun install
```

## 配置

```json
// ~/.claude/settings.json
{
  "model": "glm-5.1",
  "env": {
    "ANTHROPIC_AUTH_TOKEN": "API KEY",
    "ANTHROPIC_BASE_URL": "https://open.bigmodel.cn/api/anthropic",
    "API_TIMEOUT_MS": "3000000",
    "CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC": "1",
    "ANTHROPIC_DEFAULT_HAIKU_MODEL": "glm-4.5-air",
    "ANTHROPIC_DEFAULT_SONNET_MODEL": "glm-5-turbo",
    "ANTHROPIC_DEFAULT_OPUS_MODEL": "glm-5.1"
  }
}
```

## 启动方式

```bash
IS_DEMO=true bun cli.js
```

## **源码还原的方法**

**关键是获取本次泄露的`cli.js.map`**
