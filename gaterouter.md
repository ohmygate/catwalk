# GateRouter 文档

统一的 AI 模型路由平台。一个 API 密钥，… 模型，智能自动路由。

---

## 快速开始

### 1. 创建 API 密钥

1. 前往 [gaterouter.ai](https://www.gaterouter.ai/zh)，选择登录模式，授权登录
2. 进入控制台 → 进入设置 → 进入 API 密钥 → [创建密钥](https://www.gaterouter.ai/zh/dashboard/settings/keys)

### 2. 自动路由（可选）

自动路由默认开启，控制方式：

    进入控制台 → 进入设置 → 进入路由 → 自动路由开关

开启后，GateRouter 会自动为每个请求选择最佳模型。如果你更倾向于自行选择模型，可跳过此步，直接指定模型（如 anthropic/claude-sonnet-4.6）。

---

## 标准接入

与 OpenAI API 完全兼容，支持 Python、Node.js、curl 等生态工具。

替换 Base URL (`https://api.gaterouter.ai/openai/v1`) 与 API 密钥即可使用。

**Python:**

```python
from openai import OpenAI

client = OpenAI(
    api_key="GATEROUTER_API_KEY",  # get GATEROUTER_API_KEY from gaterouter.ai (API Key)
    base_url="https://api.gaterouter.ai/openai/v1",
)

completion = client.chat.completions.create(
    model="auto",
    messages=[
        {"role": "system", "content": "system prompt"},
        {"role": "user", "content": "how are you?"}
    ],
)

# get the response from LLM (role=assistant)
print(completion.choices[0].message.content)
```

**响应示例：**

```json
{
    "id": "243c850e-214c-431e-977f-ebaf4aa95f56",
    "choices": [
        {
            "index": 0,
            "message": {
                "role": "assistant",
                "content": "Hello! Nice to meet you. How can I help you?"
            },
            "finish_reason": "stop"
        }
    ],
    "created": 1773408946,
    "model": "deepseek.v3-v1:0",
    "object": "chat.completion",
    "usage": {
        "prompt_tokens": 5,
        "completion_tokens": 15,
        "total_tokens": 20
    }
}
```

---

## OpenClaw 接入

如果您已安装好 OpenClaw，请按照以下步骤接入 GateRouter。

### 接入 GateRouter

#### 方式 1：Web 控制台配置

**1. 启动 Web 控制台**

在终端中运行以下命令：

```
openclaw dashboard
```

浏览器会自动打开控制台页面（通常是 [http://127.0.0.1:18789](http://127.0.0.1:18789)）。如果浏览器没有自动打开，请手动访问该地址。

**2. 进入配置页面**

选择 配置 → Raw 模式。

**3. 添加 GateRouter 配置**

在 JSON 中添加 env，并将 GATEROUTER_API_KEY 替换为您的 GateRouter API 密钥：

```json
env: {
    vars: {
      GATEROUTER_API_KEY: 'sk-or-v1-xxxxxxxxxxxxxxxx',
    },
  },
```

添加 models，将 baseUrl 调整为 https://api.gaterouter.ai/openai/v1：

```json
models: {
  mode: 'merge',
  providers: {
    gaterouter: {
      baseUrl: 'https://api.gaterouter.ai/openai/v1',
      apiKey: '${GATEROUTER_API_KEY}',
      api: 'openai-completions',
      models: [
        {
          id: 'gaterouter/auto',
          name: 'Gaterouter Auto',
          api: 'openai-completions',
          reasoning: false,
          input: ['text'],
          cost: {
            input: 0,
            output: 0,
            cacheRead: 0,
            cacheWrite: 0,
          },
          contextWindow: 200000,
          maxTokens: 8192,
        },
      ],
    },
  },
},
```

替换原 "agents": {...} 部分为：

```json
agents: {
  defaults: {
    model: {
      primary: 'gaterouter/auto',
    },
    models: {
      'gaterouter/auto': {
        alias: 'Gaterouter Auto',
      },
    },
  },
},
```

**4. 保存并应用配置**

Web 控制台：配置完成后，单击右上角 Save 保存配置，再单击 Update。

**5. 验证接入成功**

在 OpenClaw Chat 界面发送测试问题，例如：Hello。如果配置成功，系统会调用 GateRouter API → 自动路由到最优模型 → 返回结果。

#### 方式 2：编辑文件配置

**1. 找到 openclaw.json 文件**

macOS：

打开 Finder，快捷键：Command + Shift + G

输入：`~/.openclaw`

回车，就能看到 `openclaw.json`。

Windows：

路径：`C:\Users\你的用户名\.openclaw\openclaw.json`

**2. 添加 GateRouter 配置**

在 JSON 中添加 env，并将 GATEROUTER_API_KEY 替换为您的 GateRouter API 密钥：

```json
"env": {
  "vars": {
    "GATEROUTER_API_KEY": "sk-or-v1-xxxxxxxxxxxxxxxx"
  }
},
```

添加 models，将 baseUrl 调整为 https://api.gaterouter.ai/openai/v1：

```json
"models": {
  "mode": "merge",
  "providers": {
    "gaterouter": {
      "baseUrl": "https://api.gaterouter.ai/openai/v1",
      "apiKey": "${GATEROUTER_API_KEY}",
      "api": "openai-completions",
      "models": [
        {
          "id": "gaterouter/auto",
          "name": "Gaterouter Auto",
          "api": "openai-completions",
          "reasoning": false,
          "input": ["text"],
          "cost": {
            "input": 0,
            "output": 0,
            "cacheRead": 0,
            "cacheWrite": 0
          },
          "contextWindow": 200000,
          "maxTokens": 8192
        }
      ]
    }
  }
},
```

替换原 "agents": {...}, 部分：

```json
"agents": {
  "defaults": {
    "model": {
      "primary": "gaterouter/minimax/minimax-m2.5"
    },
    "models": {
      "gaterouter/auto": {
        "alias": "Gaterouter Auto"
      }
    }
  }
},
```

**3. 保存及验证配置**

保存配置文件后，在终端中运行以下命令查看内容，确认配置正确：

```
cat ~/.openclaw/openclaw.json
```

**4. 验证接入成功**

在本地终端中运行以下命令，即可通过命令行方式开始对话：

```
openclaw tui
```

也可以在终端中运行以下命令，在 OpenClaw Chat 界面进行对话：

```
openclaw dashboard
```

### 可选配置

**自动模型路由**

GateRouter 推荐将 primary 设置为 gaterouter/auto。

根据价格、延迟、可用性，自动选择最优模型。

**指定模型**

如果需要固定模型，例如：primary 设置为 gaterouter/deepseek/deepseek-v3.2

### 常见问题

1. **当仅 OpenAI 系列模型请求成功，而其他模型均请求失败**

   目前我们提供接入的模型均支持 OpenAI 通用协议。请在 OpenClaw 接入配置中，将 api 设置为 `openai-completions`（参见上文示例）。若 OpenAI 系列模型可用而其他模型均失败，请优先检查 `providers` 配置项中的 `api` 类型。

2. **提示找不到模型或回复为空**

   请确认：模型 ID 拼写是否正确；配置中的 `provider` 名称与引用时是否一致；配置中的 `reasoning` 参数必须设置为 `false`。

---

## Cursor 接入

如果您已安装好 Cursor，请按照以下步骤接入 GateRouter。

### 1. 打开 Cursor 设置

右上角菜单 → Settings。

### 2. 进入 Models 配置

在左侧菜单中：

- 找到并打开 Models。
- 点击 View All Models，滑到最底部，点击 Add Custom Model。
- 填写具体模型 ID，例如：deepseek/deepseek-v3.2。**不能填写 auto**。

### 3. 添加 GateRouter 配置

填写接入信息：

- 展开 API Keys。
- 填写您的 GateRouter API 密钥。
- 填写 GateRouter 的 Base URL：`https://api.gaterouter.ai/openai/v1`

### 4. 保存并关闭 Settings 页面。

### 5. 在 Cursor 中使用 GateRouter

在 Chat、Composer、Agent 等对话界面中，模型选择下拉框选择添加的 GateRouter 模型，即可进行使用。

---

## Claude Code 接入

如果您已安装好 [Claude Code](https://code.claude.com/docs/en/overview)（Anthropic 终端 / IDE 中的 AI 编程助手），请按照以下步骤接入 GateRouter。

### 1. 创建 GateRouter API 密钥

1. 进入**控制台 → 设置 → API 密钥**，[创建密钥](https://www.gaterouter.ai/zh/dashboard/settings/keys)。
2. 复制以 `sk-or-v1-` 开头的密钥，后续替换下文占位符。
3. 若需**自动路由**：**控制台 → 设置 → 路由** → 打开「自动路由」。关闭时需在请求中显式指定模型 ID。

### 2. 配置 Anthropic Base URL 与 API Key

Claude Code 会读取环境变量；推荐与官方 [LLM gateway](https://code.claude.com/docs/en/llm-gateway) 说明一致，设置：

| 变量 | 值 |
|------|-----|
| `ANTHROPIC_BASE_URL` | `https://api.gaterouter.ai/anthropic` |
| `ANTHROPIC_API_KEY` | 您的 GateRouter API 密钥（`sk-or-v1-…`） |

**方式 A：当前终端会话（临时）**

```bash
export ANTHROPIC_BASE_URL="https://api.gaterouter.ai/anthropic"
export ANTHROPIC_API_KEY="sk-or-v1-xxxxxxxxxxxxxxxx"
claude
```

**方式 B：写入 Shell 配置文件**

将以下内容追加到 `~/.zshrc` 或 `~/.bashrc`：

```bash
export ANTHROPIC_BASE_URL="https://api.gaterouter.ai/anthropic"
export ANTHROPIC_API_KEY="sk-or-v1-xxxxxxxxxxxxxxxx"
```

执行 `source ~/.zshrc`（或重新打开终端）后，再运行 `claude`。

**方式 C：Claude Code `settings.json`（推荐）**

在用户级或项目级配置中写入 `env`（路径见 [Claude Code settings](https://platform.claude.com/docs/en/settings)），例如**项目目录下** `.claude/settings.json`：

```json
{
  "env": {
    "ANTHROPIC_BASE_URL": "https://api.gaterouter.ai/anthropic",
    "ANTHROPIC_API_KEY": "sk-or-v1-xxxxxxxxxxxxxxxx"
  }
}
```

**安全提示**：不要将真实密钥提交到公共仓库；可使用各操作系统的密钥管理或 CI 密钥注入，本地仅用环境变量。

**恢复直连 Anthropic 官方**

若需临时绕过网关：

```bash
env -u ANTHROPIC_BASE_URL -u ANTHROPIC_API_KEY claude
```

（需已配置 Anthropic 官方账号或其它默认凭据。）

### 3. 配置模型（GateRouter 模型 ID）

GateRouter 文档中的模型 ID 形如 `provider/model-name`（如 `anthropic/claude-sonnet-4.6`），与 Claude Code 内置别名（如 `sonnet`）**不完全相同**。任选其一：

#### 3.1 使用环境变量指定默认模型

```bash
export ANTHROPIC_MODEL="anthropic/claude-sonnet-4.6"
```

或在 `settings.json` 的 `env` 中增加同名键。

#### 3.2 使用别名映射

将别名映射到 GateRouter 的模型 ID（示例为 Sonnet）：

```bash
export ANTHROPIC_DEFAULT_SONNET_MODEL="anthropic/claude-sonnet-4.6"
export ANTHROPIC_DEFAULT_OPUS_MODEL="anthropic/claude-opus-4.6"
export ANTHROPIC_DEFAULT_HAIKU_MODEL="anthropic/claude-haiku-4.5"
```

具体 ID 以 [GateRouter 文档 - 模型](https://www.gaterouter.ai/zh/models) 列表为准。

#### 3.3 在 `/model` 中选自定义项

若需在界面中选择网关侧模型，可使用 Claude Code 的自定义模型项（见官方 [Model configuration - ANTHROPIC_CUSTOM_MODEL_OPTION](https://code.claude.com/docs/en/model-config)）：

```bash
export ANTHROPIC_CUSTOM_MODEL_OPTION="anthropic/claude-sonnet-4.6"
export ANTHROPIC_CUSTOM_MODEL_OPTION_NAME="Sonnet（GateRouter）"
```

#### 3.4 自动路由模型 `auto`

若在控制台已开启自动路由，可尝试将 `ANTHROPIC_MODEL` 设为 `auto`（与 OpenAI 接入页的 `auto` 语义一致）。若遇报错，请改回显式模型 ID（如 `anthropic/claude-sonnet-4.6`）。

### 4. 验证接入是否成功

1. 在已配置环境的终端执行：

```
claude
```

2. 进入会话后输入简单指令，例如：**请用一句话介绍你自己。**

3. 若返回正常回复且无鉴权/路由错误，即表示请求已到达 GateRouter 并由所选模型响应。

### 5. 常见问题

| 现象 | 可能原因 | 处理建议 |
|------|---------|---------|
| 401 / 鉴权失败 | API Key 错误或未导出 | 检查 `ANTHROPIC_API_KEY`，与控制台密钥一致 |
| 404 on URL | Base URL 误用 OpenAI 路径 | 使用 `https://api.gaterouter.ai/anthropic` |
| 模型不存在 / 路由错误 | 模型 ID 格式错误或控制台未允许该模型 | 对照文档「模型」表；检查控制台路由与允许列表 |
| 仍走官方 Anthropic | 环境变量未生效 | 确认 `settings.json` 位置层级；或在新 shell 中 `echo $ANTHROPIC_BASE_URL` 验证 |

---

## Hermes 接入

### 前置条件

- 已在 [GateRouter 控制台](https://www.gaterouter.ai/zh/dashboard/settings/keys) 创建 API 密钥。
- 若使用自动路由，请在控制台 设置 → 路由 中开启 自动路由。

### 方式一：终端配置

#### 1. 选择模型与自定义端点

在终端执行：

```
hermes model
```

在菜单中选择 Custom endpoint，按提示填写：

| 项 | 值 |
|----|-----|
| API base URL | `https://api.gaterouter.ai/openai/v1` |
| API key | 你的 GateRouter API 密钥 |
| Model | `auto`（推荐自动路由），或控制台列出的完整模型 ID（如 `deepseek/deepseek-v3.2`） |

若询问 context length（上下文长度），直接回车留空即可（由 Hermes 自动探测）。

#### 2.（可选）本地 Web 管理界面

若希望通过浏览器编辑配置，可运行：

```
hermes dashboard
```

#### 3. 验证

```
hermes chat "Hello"
```

成功则说明请求已到达 GateRouter，并由智能路由或你指定的模型返回结果。

也可运行 `hermes doctor` 验证是否连接成功。

### 方式二：直接编辑配置文件

#### 1. 文件位置

**macOS / Linux**

- `~/.hermes/config.yaml`，主配置（模型、provider、base_url、api_key 等）
- `~/.hermes/.env`，密钥与敏感环境变量（推荐）

**Windows**

- `C:\Users\<用户名>\.hermes\config.yaml`
- `C:\Users\<用户名>\.hermes\.env`

#### 2. 在 `.env` 中保存密钥（任选其一）

**写法 A**（与 GateRouter 命名一致）

```
# GateRouter API 密钥
GATEROUTER_API_KEY=sk-or-v1_xxxxxxxxxxxxxxxxxxxxx
```

**写法 B**（与 Hermes 自定义端点常见约定一致）

Hermes 对自定义端点在未单独配置 `model.api_key` 时，会回退使用 `OPENAI_API_KEY`。可将 GateRouter 密钥写入：

```
OPENAI_API_KEY=sk-or-v1_xxxxxxxxxxxxxxxxxxxxx
```

#### 3. 在 `config.yaml` 中配置 `model`

**自动路由（auto）**

```yaml
model:
  default: auto
  provider: custom
  base_url: https://api.gaterouter.ai/openai/v1
  api_key: ${GATEROUTER_API_KEY}
```

若使用写法 B，可将 `api_key` 留空或删除该字段，让 Hermes 使用 `OPENAI_API_KEY`。

Hermes 会在加载配置时展开 `${VAR}`（变量须已在环境中存在，通常由 `~/.hermes/.env` 注入）。

**固定模型示例**

模型 ID 须与 [GateRouter 模型列表](#模型) 一致：

```yaml
model:
  default: deepseek/deepseek-v3.2
  provider: custom
  base_url: https://api.gaterouter.ai/openai/v1
  api_key: ${GATEROUTER_API_KEY}
```

---

## QClaw 接入

如果您已安装好 QClaw，请按照以下步骤接入 GateRouter。

### 对话式完成配置

**1. 在对话中输入以下内容**，请将 apiKey 替换为您的 GateRouter API 密钥：

```
帮我新增一个provider
名称：GateRouter
apiKey: sk-or-v1-xxxxxxxxxxxxxxxx
baseUrl: https://api.gaterouter.ai/openai/v1
模型（可传多个）： 1、auto  2、deepseek/deepseek-v3.2
```

QClaw 会自动添加成功并重启生效。

**2. 验证是否成功**

直接输入：「帮我验证一下 GateRouter 配置有没有生效」。对话会返回「GateRouter provider 已成功添加！」（以实际界面为准。）

**3. 切换到 GateRouter 使用**

直接输入：「切换到 GateRouter 下面的 auto」。对话会返回「已切换成功！」（以实际界面为准。）

---

## AutoClaw 接入

**1. 配置入口**

点击左下角偏好设置，选择模型与 API，点击添加自定义模型。

**2. 添加模型**

- 服务商选择自定义。
- 添加 GateRouter 支持的模型 ID，例如 `deepseek/deepseek-v3.2`。
- 填写显示名称，例如：`GateRouter(deepseek-v3.2)`。
- 填写 API Key，例如：`sk-or-v1-xxxxxxxxxxxxxxxx`。
- 填写 Base URL：`https://api.gaterouter.ai/openai/v1`

**3. 测试配置是否成功**

点击连通测试，显示「测试成功」字样，则表示配置成功。

**4. 模型使用**

- 点击添加按钮，保存成功后，返回应用。
- 在聊天框下方选择切换模型，选择配置的 `GateRouter(deepseek-v3.2)`，即可使用。

---

## API 参考

| 字段 | 值 |
|------|-----|
| Base URL | `https://api.gaterouter.ai/openai/v1` |
| 认证 | `Authorization: Bearer <API_KEY>` |
| 格式 | OpenAI 兼容 |
| 计费 | 按量计费 |

**注意**：API 路径是 `/openai/v1`（不是 `/v1`）。

### 端点

| 方法 | 路径 | 描述 |
|------|------|------|
| POST | `/chat/completions` | 聊天补全（支持流式） |
| GET | `/models` | 获取可用模型列表 |

---

## 模型

| 模型 ID | 描述 | 用途 |
|---------|------|------|
| `openai/gpt-5.2` | OpenAI 最新 | 推理任务 |
| `openai/gpt-5` | OpenAI 通用旗舰 | 通用 |
| `openai/gpt-5-mini` | OpenAI 轻量版 | 通用 / 成本优化 |
| `openai/gpt-5-nano` | OpenAI 极致低成本 | 简单任务 |
| `openai/gpt-4.1` | OpenAI 稳定 | 通用 |
| `openai/gpt-4.1-nano` | OpenAI 轻量稳定版 | 简单任务 |
| `anthropic/claude-opus-4.6` | Anthropic 最强模型 | 复杂推理 |
| `anthropic/claude-sonnet-4.6` | Anthropic 均衡 | 通用 |
| `anthropic/claude-sonnet-4.5` | Anthropic 上一代 | 通用 |
| `anthropic/claude-haiku-4.5` | Anthropic 快速 | 简单任务 |
| `google/gemini-3.1-pro` | Google 最新旗舰 | 长上下文 / 推理 |
| `google/gemini-2.5-pro` | Google 上一代旗舰 | 长上下文 |
| `deepseek/deepseek-v3.2` | DeepSeek 最新 | 高性价比 |
| `deepseek/deepseek-v3.1` | DeepSeek 上一代 | 通用 |
| `x-ai/grok-4` | xAI 最新旗舰 | 推理 / 实时信息 |
| `x-ai/grok-4.1-fast` | xAI 高速版 | 快速响应 |
| `moonshotai/kimi-k2.5` | Moonshot 长文本能力强 | 长上下文 |
| `z-ai/glm-5` | Z.ai 最新 | 通用 |
| `z-ai/glm-5-turbo` | 编程、推理 | 多场景应用 |
| `z-ai/glm-4.7-flash` | Z.ai 快速版 | 简单任务 |
| `minimax/minimax-m2.5` | MiniMax 多模态能力 | 通用 |

模型 ID 格式：`provider/model-name`。版本号使用 `.`（如 4.6），而非 `-`。

更多模型可访问 [模型页面](https://www.gaterouter.ai/zh/models) 查看。

---

## 故障排除

| 错误 | 原因 | 解决方案 |
|------|------|---------|
| `auto routing is not enabled` | 未开启自动路由 | 进入控制台 → 进入设置 → 进入路由 → 打开自动路由开关 |
| `provider routing is not configured` | 模型 ID 格式错误 | 可进入文档页面 → 模型，进行查看 |
| `404 page not found` | API 路径错误 | 请确认 Base URL 为 `https://api.gaterouter.ai/openai/v1` |
| `unsupported parameter: max_tokens` | 部分模型不支持该参数 | 改用 `max_completion_tokens` |
