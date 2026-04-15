# MEMORY.md

更新时间：2026-04-15

这是主会话的长期记忆总表，只保留稳定、会反复用到、值得长期保留的信息。

---

## 用户偏好
- 用户要求以后一直用中文回复。
- 用户偏好回复风格：结论优先，简洁，失败透明。
- 高风险操作需要先确认，尤其是删除、卸载、改配置、暴露端口、重启等。
- 涉及配置或核心技能变更，要遵循既定安全流程，不绕过。
- 搜索与外部信息优先走已验证路线，拿不准要明确说不确定。
- 用户要求以后称呼其为“主人”。

## 工作方式
- 回答涉及过去工作、决定、偏好、待办时，先做记忆检索，不凭印象回答。
- 每天做的任务需要定期整理总结和日记。
- 如需补能力，优先免费来源：
  1. 官方 ClawHub
  2. GitHub 高 star 免费项目或技能
- 安装技能不能只看“装上”，还要做最小可用性验证和学习结论。
- 持续项目与长期待办统一维护在 `PROJECTS.md`，避免只记过去，不追踪未来。

## 环境与基础结论
- OpenClaw 主工作区在 `/root/.openclaw/workspace`。
- 大文件目录使用 `/www/manmanai/openclaw`，适合 downloads、artifacts、browser-data、tts-output、logs 等大体积产物。
- 当前策略是：主目录 `/root/.openclaw` 与 `/root/.openclaw/workspace` 保持原位，大文件优先落到 `/www/manmanai/openclaw`。
- 已准备大盘备份目录 `/www/manmanai/openclaw/backup`，用于后续快照与恢复。

## 代理与 Telegram 线稳定事实
- OpenClaw gateway 当前使用全局代理：`http://192.168.50.2:5898`。
- `channels.telegram.proxy` 需要保留，不能随便移除，否则 Telegram 可能失联。
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
