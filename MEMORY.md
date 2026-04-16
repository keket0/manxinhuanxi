# MEMORY.md

更新时间：2026-04-15

这是主会话的长期记忆总表，只保留稳定、会反复用到、值得长期保留的信息。

---

## 用户偏好
- 用户要求以后一直用中文回复。
- 用户进一步强调：除非必须原样引用报错、字段名、命令名，否则回复说明不要夹英文。
- 用户偏好回复风格：结论优先，简洁，失败透明。
- 高风险操作需要先确认，尤其是删除、卸载、改配置、暴露端口、重启等。
- 涉及配置或核心技能变更，要遵循既定安全流程，不绕过。
- 搜索与外部信息优先走已验证路线，拿不准要明确说不确定。
- 用户要求以后称呼其为“主人”。

## 工作方式
- 回答涉及过去工作、决定、偏好、待办时，先做记忆检索，不凭印象回答。
- 主人现在要求所有 agent 都要具备长期记忆，并在回答相关历史信息前先做记忆检索。
- 每天做的任务需要定期整理总结和日记，这条要求适用于现有和未来新建的所有 agent。
- 如需补能力，优先免费来源：
  1. 官方 ClawHub
  2. GitHub 高 star 免费项目或技能
- 安装技能不能只看“装上”，还要做最小可用性验证和学习结论。
- 缺能力时，可以去官方技能站安装，或去 GitHub 自行找 star 较高且免费的技能，但不要默认装付费或来源可疑的东西。
- 持续项目与长期待办统一维护在 `PROJECTS.md`，避免只记过去，不追踪未来。
- `PROJECTS.md` 里的项目线默认包含：优先级、最近更新时间、阻塞状态、下一次触发条件，方便 heartbeat 推进。
- OmniBox 写源时，优先深度理解文档和目标网站本身，目标是让用户直接给网站后就能写成可用的 JS 源；现有 4 个影视 JSON 主要用于代号定位和最终挂载，不作为主要写法模板。
- 收到 OmniBox 示例 JS 时，默认先学习写法、提炼可复用模式、沉淀笔记，再反哺后续实战写源，不机械照抄。
- 主人以后还会继续投喂 JS 示例，并会明确说明这是不夜源写法还是 OmniBox 写法；我必须按标注分类学习，不能混淆。
- 主人让我学习的 JS 只是学习材料，不能再牵扯到“不夜自用 / 不夜分享 / pg自用 / pg分享”这 4 个 JSON 本身。
- 不夜源与 OmniBox 不是一套写法体系，后续必须严格分开理解：OmniBox 按开发框架与 handler 学，不夜源按挂载体系、`type/api/ext/header/proxy/timeout` 这类配置结构学，不能混用。
- 真正开始写源前，如果主人没明确说类型，我要先确认是“不夜源”还是“OmniBox/monibox 源”再动手。
- 四个影视接口代号路径必须长期记住，后续用户只报代号就直接定位，不再反复询问路径：`pg分享=/www/manmanai/PG/jsm🧿.json`，`pg自用=/www/manmanai/pg_zy/jsm🧿.json`，`不夜自用=/www/manmanai/pg_zy/buyezy🧿.json`，`不夜分享=/www/manmanai/pg_zy/buyegg🧿.json`。
- `/www/manmanai/buye/vod/routes` 是主人存放大量不夜 JS 源的主学习目录，后续学习不夜源应优先从这里按类型拆解：影视源、网盘源、聚合配置、功能目录、后台 API 控制器。
- 以后主人要求修改 `不夜自用`、`不夜分享`、`pg自用`、`pg共享/pg分享` 这四个配置时，可能只会给“源关键字”而不是完整条目名。此时我应先按代号文件搜索匹配关键字，列举出命中的候选源给主人确认，再根据主人指定的具体条目执行替换，不能擅自猜测目标条目。
- 主人的 OpenWrt 在 `192.168.50.2`，已确认可通过 SSH 访问，并且 LuCI Web 后台正常可打开和登录，当前不需要为基础网页管理额外补装核心组件。
- 主人的 OpenClaw Web 已改为局域网可访问，当前地址是 `http://192.168.50.100:18789/`；Gateway 已从 loopback 改为 `bind=lan`，并改为密码登录模式。
- 2026-04-16 已确认通过 Lucky 反代 `http://192.168.50.100:18789/` 到 `https://claw.keket.cn:7788/` 后可正常使用密码登录。该场景要点是 `gateway.controlUi.allowedOrigins` 需长期包含 `https://claw.keket.cn:7788`，否则会被 `origin not allowed` 拒绝。
## 环境与基础结论
- OpenClaw 主工作区在 `/root/.openclaw/workspace`。
- 大文件目录使用 `/www/manmanai/openclaw`，适合 downloads、artifacts、browser-data、tts-output、logs 等大体积产物。
- 当前策略是：主目录 `/root/.openclaw` 与 `/root/.openclaw/workspace` 保持原位，大文件优先落到 `/www/manmanai/openclaw`。
- 2026-04-16 主人进一步明确新的统一落盘规则，且适用于后续各个 agent，包括未来新建的 agent：小配置、小代码、小文本继续放各自原 workspace；音频、下载、浏览器数据、临时产物、大文件优先放 `/www/manmanai/openclaw`。
- 这条“文件分流落盘规则”已视为长期记忆，后续默认执行，新建 agent 时也要继承这条规则，不再反复确认常规落盘位置。
- 已准备大盘备份目录 `/www/manmanai/openclaw/backup`，用于后续快照与恢复。
- 主人的 Docker 项目统一放在 `/www/manmanai/docker/<项目名>/` 下，每个项目目录内固定放 `docker-compose.yml`，方便整洁管理与手动维护。
- 以后如需新建 Docker 项目，应按“创建项目目录 -> 在目录内写好 `docker-compose.yml` -> 进入该目录执行 `docker-compose up -d`”的流程进行。
- 以后如主人要求升级某个 Docker 项目，应进入对应项目目录，按固定升级命令执行：`docker-compose pull && docker-compose up -d --remove-orphans`。

## 常用官方入口与资料源
- OpenClaw 官方网站：`https://openclaw.ai`
- OpenClaw 官方文档：`https://docs.openclaw.ai`
- OpenClaw GitHub 仓库：`https://github.com/openclaw/openclaw`
- ClawHub 技能广场：`https://clawhub.ai`
- Awesome OpenClaw Skills 合集：`https://github.com/VoltAgent/awesome-openclaw-skills`
- 后续如需查官方说明、能力边界、技能来源，优先从这组入口开始。

## 代理与 Telegram 线稳定事实
- OpenClaw gateway 先前曾使用全局代理：`http://192.168.50.2:5898`，但为避免 browser 被 SSRF / policy 拦截，当前默认方案已改为不恢复 gateway 全局代理。
- `channels.telegram.proxy` 需要保留，不能随便移除，否则 Telegram 可能失联。
- 主人已在 2026-04-16 明确要求：Telegram 专用代理要长期保持，不要去触碰，后续排障、改代理、改网络策略时都不得擅自改动这条配置。
- 2026-04-16 已完成 GitHub CLI `gh` 持久登录，当前登录用户为 `keket0`，认证信息由 `gh` 保存在 `/root/.config/gh/hosts.yml`。后续优先直接复用该登录态，不再默认重复走网页设备码授权。
- 2026-04-16 已再次确认 browser 当前可用，包括成功打开并读取 `example.com`、`python.org`、`github.com`。后续判断 browser 问题时，要先区分“整体故障”“单次超时”“站点策略拦截”，不要再混为一谈。
- 主人已在 2026-04-16 明确要求：以后若需要代理，只按单次命令或单个工具单独加代理，不恢复全局代理作为默认方案。
- 当前统一使用的代理地址是：`http://192.168.50.2:5898`。该地址目前用于 Telegram 专用代理，也用于我在需要时按次给单个命令或单个工具临时加代理。
- 主人已在 2026-04-16 明确确认对代理策略的长期理解：全局代理是“很多程序默认都走代理”，省事但影响面大、容易互相打架，也会伤到 OpenClaw browser；单独代理是“谁需要谁临时走代理”，更适合当前这台机器的长期稳定方案。后续默认保持单独代理，不回到全局代理。
- Telegram 图片问题的最终真实根因，不是 transport / TLS / 代理代码层，而是 Telegram 机器人隐私模式设置；用户手动修复后已恢复。
- Telegram 图片问题已结案，但其他 Telegram API 偶发失败日志不能与该问题混为一谈。

## 技能体系长期结论
- 当前值得长期保留的第一梯队技能包括：
  - `agent-browser-core`
  - `agent-browser-clawdbot`
  - `duckduckgo-search`
  - `liang-tavily-search`
  - `liang-tavily-extract`
  - `telegram-bot-manager`
  - `weather`
- `openai-tts` 当前阻塞不是网络，而是 OpenAI key 无效；换有效 key 后可恢复。
- `claw-ds-generator` 当前更像不存在、已下架或名字不对，不应继续盲重试。
- `cn-ecommerce-search` 旧版依赖包当前公开 npm `404`，主线应切到 `cn-ecommerce-search-v2`。

## 电商线长期结论
- 中文电商搜索当前更有效的路线，不是死磕站内搜索，而是“外部搜索 + 定向详情页 + agent-browser 验证”。
- 京东是当前最有效的突破口：站内搜索可能风控，但定向详情页可打开。
- 苏宁与当当技术上能抽取，但 `iPhone 15` 业务结果噪音大，不适合作为主战场。
