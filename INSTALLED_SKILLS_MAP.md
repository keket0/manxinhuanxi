# 已装技能作战图

更新时间：2026-04-15

## 一、搜索型

### 1. tavily-search
- 状态：可用
- 价值：高质量网页搜索，适合文档、新闻、资料检索
- 优先场景：需要更结构化、更适合模型消费的搜索结果
- 依赖：`TAVILY_API_KEY`（已配置）
- 备注：已实测跑通

### 2. duckduckgo-search
- 状态：可用
- 价值：轻量通用搜索，不需要 API key
- 优先场景：普通网页、新闻、图片、视频搜索
- 依赖：无额外 key
- 备注：适合做兜底和低成本搜索

### 3. weather
- 状态：可用（内置）
- 价值：天气查询
- 优先场景：当前天气、预报、出行前天气判断
- 依赖：无额外 key

## 二、干活型

### 4. cn-ecommerce-search
- 状态：可用
- 价值：搜索中国 8 大电商平台商品信息
- 优先场景：找商品、看商品链接、比价、找供应商
- 支持平台：淘宝、天猫、京东、拼多多、1688、AliExpress、抖音、小红书
- 依赖：无 API key
- 备注：是真正可直接干活的技能

## 三、行为增强型

### 5. proactive-agent-lite
- 状态：可用
- 价值：让 agent 更主动，增强连续性、恢复力、对主人价值导向
- 优先场景：长任务、多轮协作、主动发现下一步
- 依赖：无额外 key / 无额外二进制
- 备注：可作为 `proactive-agent` 的当前正式替代

### 6. self-improvement
- 状态：可用
- 价值：沉淀错误、纠正、知识缺口、最佳实践
- 优先场景：失败复盘、用户纠正、发现更好流程、记录能力缺口
- 关键文件：
  - `.learnings/ERRORS.md`
  - `.learnings/LEARNINGS.md`
  - `.learnings/FEATURE_REQUESTS.md`
- 备注：偏学习日志与长期沉淀

### 7. self-improving-proactive-agent
- 状态：可用
- 价值：把“自我改进 + 主动推进”合成一套统一运行模型
- 优先场景：复杂任务、长任务、需要 heartbeat 跟进、需要上下文恢复
- 核心规则：
  - 先恢复上下文，再问用户
  - 做完后留 next move
  - 只在有真实变化时 heartbeat
  - 从明确纠正和重复成功中学习，不从沉默里脑补
- 备注：这是当前最像“长期运行规范”的技能之一

## 四、浏览器自动化

### 8. agent-browser-core
- 状态：可用，且已实测达到“基本可战斗”
- 价值：浏览器自动化核心规范，适合稳定、结构化、多步骤网页操作
- 优先场景：复杂网页流程、需要 snapshot / refs / JSON 的可控自动化
- 依赖：外部 `agent-browser` CLI 与浏览器运行环境（现已安装）
- 实测通过：`open https://example.com --json`、`snapshot`、`get title`、`screenshot`
- 产物落点：`/www/manmanai/openclaw/artifacts/agent-browser/example-com.png`
- 备注：当前浏览器线真正可战斗的主力

### 9. agent-browser-stagehand
- 状态：已安装，但当前 skill 包不完整
- 价值：自然语言驱动的浏览器自动化，支持本地 Chrome 或远程 Browserbase
- 优先场景：快速浏览、自然语言点击/提取、需要远程浏览器时
- 依赖：文档要求执行 `npm install`、`npm link`；本地模式依赖 Chrome，远程模式依赖 Browserbase key
- 当前问题：安装下来的技能目录只有文档和 `setup.json`，缺少 `package.json` 与源码，无法实际完成初始化
- 备注：当前更像文档型 / 参考型技能，不能当作已可直接运行的浏览器工具

### 10. chrome-web-automation
- 状态：已安装，当前更像参考型技能
- 价值：描述如何接管现有 Chrome 会话进行调试、填表、截图、复现问题
- 优先场景：用户当前已打开的浏览器现场、真实登录态问题、当前 tab 排障
- 依赖：需要底层浏览器执行能力；技能包本身未附带独立可执行工程
- 当前判断：目录中只有 `SKILL.md`、参考文件和 `agents/openai.yaml`，没有 `package.json` 或独立脚本，更像从内置能力抽出的说明包装
- 备注：不是通用主力，而是“接管现场”方法说明；真正执行仍应依赖 OpenClaw / 浏览器工具链本身

### 11. openclaw-web-automation
- 状态：可用
- 价值：轻量公共网页查询，适合公开网页摘要、关键词检查、简单统计
- 优先场景：无登录、无复杂交互的公共页面检查
- 依赖：本地 Python 环境
- 备注：快刀型技能，简单网页任务优先级很高

## 五、技能发现 / 抽取 / 路由

### 12. find-skills-for-clawhub
- 状态：可用
- 价值：官方 ClawHub 技能发现导航，负责搜索、推荐、安装流程指导
- 优先场景：找技能、问 OpenClaw 能不能做某事、需要搜索和安装技能时
- 依赖：`clawhub` CLI（现已安装且已登录）
- 备注：当前技能生态导航核心件

### 13. openclaw-find-skills
- 状态：可用
- 价值：补充型找技能技能，适合继续扩展技能发现能力
- 优先场景：继续搜技能、查替代 skill、补充生态导航
- 依赖：按技能文档执行
- 备注：和 `find-skills-for-clawhub` 可形成双保险

### 14. liang-tavily-extract
- 状态：可用
- 价值：按 URL 提取网页正文，适合与 `tavily-search` 组成“先搜后吃”组合
- 优先场景：已知 URL 的内容抽取、文档精读、页面正文抓取
- 依赖：`node`、`TAVILY_API_KEY`
- 备注：当前已具备可用条件，价值很高

### 15. message-routing
- 状态：可用，但应谨慎使用
- 价值：管理 Telegram 消息路由与模型切换
- 优先场景：明确要调整 Telegram 模型路由、fallback、排查处理链路时
- 风险：会修改 `~/.openclaw/openclaw.json` 并可能重启 gateway
- 备注：不是普通查询型技能，属于高影响配置技能

### 16. reflect
- 状态：可用
- 价值：补充反思与复盘能力
- 优先场景：任务复盘、方法回看、总结做法
- 依赖：按技能文档执行
- 备注：更像行为增强和复盘补件

## 六、Telegram 相关

### 17. telegram-bot-manager
- 状态：可用
- 价值：Telegram bot 配置与管理
- 优先场景：bot 设置、网络检查、配置排查

### 18. openclaw-telegram-acp-troubleshooter
- 状态：可用
- 价值：排查 OpenClaw Telegram / ACP 相关问题
- 优先场景：Telegram 集成异常、命令菜单、连接链路排查

### 19. telegram-agent-setup
- 状态：可用
- 价值：Telegram agent 初始配置与接入指导
- 优先场景：新建 Telegram agent、初始接入、基础配置教学
- 备注：偏 setup / onboarding

### 20. telegram
- 状态：可用
- 价值：通用 Telegram 能力参考与模板补充
- 优先场景：Telegram Bot API、命令模板、更新路由参考
- 备注：偏参考资料型

## 七、半可用

### 21. openai-tts
- 状态：半可用
- 已打通：脚本权限、`jq`、`curl`、网络链路、代理
- 当前阻塞：OpenAI key 无效，返回 `401 invalid_api_key`
- 优先场景：文本转语音、音频输出
- 备注：一旦换成有效官方 key，可直接转正

## 八、当前仍未拿下 / 可判定异常的条目

### 官方当前不可安装
1. `phy-openclaw-telegram-bot`
2. `claw-ds-generator`

### 当前判断
- 这两个在已登录官方 `clawhub` CLI 下仍返回 `Skill not found`
- 更像不存在 / 已下架 / 下载源无此条目，而不是 429 限流

## 九、原始“必须学习技能”映射

- `weather` → 已可用
- `Agent Browser` → 已可用，主力为 `agent-browser-core`，补充为 `agent-browser-stagehand`
- `claw-ds-generator` → 仍不可安装，且更像不存在 / 下架 / 名字不对
- `cn-ecommerce-search` → 已可用
- `duckduckgo-search` → 已可用
- `find-skills` → 已可用，主力为 `find-skills-for-clawhub`，补充为 `openclaw-find-skills`
- `openai-tts` → 已装，半可用
- `proactive-agent` → 已有替代 `proactive-agent-lite`
- `self-improvement` → 已可用
- `tavily-search` → 已可用

## 十、当前最实用的技能组合

### 资料检索组合
- `tavily-search`
- `duckduckgo-search`
- `weather`

### 搜索后精读组合
- `tavily-search`
- `liang-tavily-extract`

### 行为增强组合
- `proactive-agent-lite`
- `self-improvement`
- `self-improving-proactive-agent`
- `reflect`

### 中文电商组合
- `cn-ecommerce-search-v2`（当前优先）
- `cn-ecommerce-search`（旧条目，依赖包失效）

### 浏览器自动化组合
- `agent-browser-core`（主力，已实测可战斗）
- `agent-browser-stagehand`（当前仅参考，包不完整）
- `chrome-web-automation`（当前偏参考型，适合指导接管现有 Chrome 会话）
- `openclaw-web-automation`（需补外部 Automation Kit Python runtime）

### 技能发现组合
- `find-skills-for-clawhub`
- `openclaw-find-skills`

### Telegram 运维组合
- `telegram-bot-manager`
- `openclaw-telegram-acp-troubleshooter`
- `telegram-agent-setup`
- `telegram`

## 十一、当前分级清单

### A. 已实测可战斗
- `agent-browser-core`
- `find-skills-for-clawhub`
- `tavily-search`
- `duckduckgo-search`
- `telegram-bot-manager`
- `liang-tavily-extract`

### B. 已装且高价值，但当前偏参考 / 指南型
- `telegram`
- `telegram-agent-setup`
- `chrome-web-automation`
- `self-improvement`
- `self-improving-proactive-agent`
- `proactive-agent-lite`
- `reflect`
- `openclaw-telegram-acp-troubleshooter`

### C. 已装但需额外环境 / 外部运行时
- `openai-tts`（缺有效官方 OpenAI key）
- `openclaw-web-automation`（缺外部 Automation Kit Python runtime / repo）
- `cn-ecommerce-search`（旧版依赖 `npx @shopmeagent/cn-ecommerce-search-mcp`，补代理后返回 npm `404 Not Found`，更像上游包名失效/下架/私有不可见，而不只是网络问题）

### C+ 已实测可用，但仍建议保留运行时前提意识
- `liang-tavily-extract`（已实测可抽取 `https://example.com`，依赖 `node` + `TAVILY_API_KEY`）
- `cn-ecommerce-search-v2`（已安装；skill 本体为浏览器/网页搜索工作流说明，不再依赖旧版失效 npm 包；当前至少已验证 JD、闲鱼搜索页可通过代理抓取到页面 HTML）

### D. 已装但当前包/形态不适合直接执行
- `agent-browser-stagehand`（skill 包不完整，缺 `package.json` / 源码）
- `telegram`（更偏 Telegram Bot API 设计参考而非直接执行工具）

### E. 官方当前不可安装 / 明显异常
- `phy-openclaw-telegram-bot`
- `claw-ds-generator`

## 十二、一句话总结

当前技能体系已经基本成型。
真正已被实测打通的主力包括浏览器自动化核心、技能发现、搜索与 Telegram bot 诊断；
当前主要剩余问题集中在外部运行时缺失、无效 key、个别包发布不完整，以及少数官方当前不可安装条目。
