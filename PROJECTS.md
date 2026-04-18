# PROJECTS.md

更新时间：2026-04-18

这个文件用于维护持续项目、长期待办、当前状态和下一步。它不是流水账，而是项目索引。

使用规则：
- 每条项目线都要有优先级、最近更新时间、阻塞状态、下一次触发条件。
- 有重大进展时，先更新这里，再决定是否同步到 `MEMORY.md`。
- heartbeat 看到没有明确当前任务时，应优先参考这里推进长期工作。

---

## 1. Telegram 稳定性线
- 优先级：中
- 最近更新时间：2026-04-15
- 阻塞状态：部分待查，非当前主阻塞
- 下一次触发条件：主人再次关注 Telegram 稳定性，或日志持续出现明显 Telegram API 失败

### 当前状态
- Telegram 在线可用。
- 菜单功能已恢复正常。
- 图片接收问题已结案，最终根因是 Telegram 机器人隐私模式设置，用户已手动修复。
- 现网仍偶发出现部分 Telegram API 请求失败日志，不应与图片问题混为一谈。

### 已确认事实
- `channels.telegram.proxy` 需要保留。
- 全局代理当前为 `http://192.168.50.2:5898`。
- 图片问题的最终根因不是 transport / TLS / 代理代码层。

### 下一步
- 若主人继续关注 Telegram 稳定性，再单独排查 `sendChatAction` / `deleteWebhook` / `deleteMyCommands` 等偶发失败。

---

## 2. 技能体系建设线
- 优先级：高
- 最近更新时间：2026-04-18
- 阻塞状态：部分阻塞
- 下一次触发条件：主人提出新能力需求，或现有技能不足以完成任务

### 当前状态
- 长期目标是构建一套免费、稳定、可验证的技能体系。
- 已完成一批核心技能安装、验证、分层与学习。
- 已建立：
  - `INSTALLED_SKILLS_MAP.md`
  - `SKILLS_DEEP_DIVE_2026-04-15.md`
- 2026-04-16 已新增从 GitHub 仓库 `JimLiu/baoyu-skills` 项目级全量安装的一组 baoyu 技能，当前 `.agents/skills/` 下已可见 22 个相关技能。
- 2026-04-18 新增并核读了一批技能：`vetter`、`self-evolving`、`summarize-1-0-0`、`liang-tavily-search`、`find-skills-for-clawhub`、`agent-browser-clawdbot`。
- 其中已完成最小可用验证的有：
  - `liang-tavily-search`
  - `summarize-1-0-0`
  - `agent-browser-clawdbot`
- 主人已明确把网页自动化默认主链路切到 `agent-browser`，内置 `browser` 工具降为备用链路。

### 已确认主力技能
- `agent-browser-core`
- `agent-browser-clawdbot`
- `duckduckgo-search`
- `liang-tavily-search`
- `liang-tavily-extract`
- `telegram-bot-manager`
- `weather`

### 当前阻塞
- `claw-ds-generator` 当前更像不存在 / 下架 / 名字不对。
- `openai-tts` 卡在无效 OpenAI key。
- `self-evolving` 更适合作为谨慎参考型技能，不适合默认放开长期驱动。
- `find-skills-for-clawhub` 与 `vetter` 更偏工作流/审查辅助，不是直接执行型主力技能。

### 下一步
- 需要补能力时，优先官方 ClawHub 和 GitHub 高 star 免费来源。
- 对新装技能保持“先装，再最小验证，再学习结论”的流程。
- 后续如主人要实际使用 baoyu 技能，先按具体任务筛选最合适的 skill，再补充针对性学习和实战验证，避免一次性启用高风险发布类能力。
- 后续遇到网页自动化任务，默认先走 `agent-browser`，只有在需要内置可视分析、截图/PDF 或特定集成时才回退到内置 `browser`。

---

## 3. 中文电商搜索线
- 优先级：中
- 最近更新时间：2026-04-15
- 阻塞状态：部分阻塞
- 下一次触发条件：主人继续要求商品表、比价表或指定机型详情

### 当前状态
- 旧版 `cn-ecommerce-search` 不再是主线。
- 主线已切到 `cn-ecommerce-search-v2` + 外部搜索 + `agent-browser`。
- 当前最有效突破口是京东定向详情页路线。

### 已确认事实
- 京东站内搜索页容易风控。
- 京东定向详情页可打开并验证真实商品信息。
- 苏宁、当当能抽，但 `iPhone 15` 结果噪音高。

### 下一步
- 若继续做 `iPhone 15 / Pro / Pro Max`，优先沿京东定向详情页路线整理商品表。
- 不再把时间浪费在旧版失效 npm 包上。

---

## 4. 长期记忆与日记线
- 优先级：高
- 最近更新时间：2026-04-17
- 阻塞状态：无阻塞，重点在持续执行
- 下一次触发条件：每天结束前、上下文明显变长时、出现重要决定、用户纠正，或新建 agent 时

### 当前状态
- 已建立长期记忆体系：
  - `MEMORY.md`
  - `SESSION-STATE.md`
  - `memory/YYYY-MM-DD.md`
  - `memory/DAILY_TEMPLATE.md`
  - `HEARTBEAT.md`
- 2026-04-17 已进一步明确为全局规则：所有现有和未来新建的 agent 都必须具备长期记忆，并在回答过去工作、偏好、决定、待办前先做记忆检索。
- 2026-04-17 已进一步明确：每天做过的任务都要定期总结并写入日记，不允许只做不记。

### 已确认规则
- 过去事项先检索记忆再回答。
- 每天要补总结和日记。
- 稳定长期事实沉淀到 `MEMORY.md`。
- 这套记忆与日记规则不只限于主会话，也适用于所有 agent。

### 下一步
- 持续执行，不靠临时记忆。
- 适时把当天关键信息从 daily note 提炼进 `MEMORY.md`。
- 后续每次新建 agent 时，同步检查其 `USER.md` / `AGENTS.md` / `HEARTBEAT.md` 是否已继承记忆检索与日记规则。

---

## 5. 备份与可恢复性线
- 优先级：中
- 最近更新时间：2026-04-18
- 阻塞状态：低阻塞
- 下一次触发条件：主人明确下令“备份龙虾”/“龙虾备份”，或关键配置有大改需要阶段性快照时

### 当前状态
- 大盘目录已整理为：`/www/manmanai/openclaw`
- 本地当前配置型备份固定路径：`/www/manmanai/openclaw/backups/local-config/root/.openclaw`
- 本地历史备份策略已确定：每次只保留最新 3 份
- GitHub 私有仓库只作为远程备份目标，不再在本地常驻保留 clone
- 已把这套流程沉淀为技能：`/root/.openclaw/workspace/skills/backup-openclaw`
- 最近一次 GitHub 远程备份提交：`055c158`
- 最新快照目录：`/www/manmanai/openclaw/backups/snapshots/2026-04-18-100705`

### 已确认事实
- 大文件走 `/www/manmanai/openclaw`。
- 主目录仍在 `/root/.openclaw` 与 `/root/.openclaw/workspace`。
- 只有在主人明确下令“备份龙虾”或“龙虾备份”时，才执行本地备份和 GitHub 远程备份。
- 本地与 GitHub 统一采用“配置型备份 + 学习技能”边界。
- 默认不备份 `downloads`、`artifacts`、`browser-data`、`logs`、`cache`、`tmp` 等运行产物。
- GitHub 推送应使用临时工作区，推送完成后删除，避免与本地备份形成重复占用。

### 下一步
- 持续保持快照与配置型备份可恢复。
- 下次再执行“备份龙虾”时，直接按 `backup-openclaw` 技能固定流程执行。
- 如主人未来真的迁机器，可按 `MIGRATION.md` 逐项执行，并优先补全全局 CLI 清单。

---

## 6. 模型与 TTS 能力线
- 优先级：中
- 最近更新时间：2026-04-15
- 阻塞状态：TTS 有明确阻塞
- 下一次触发条件：主人提供有效 OpenAI key，或需要进一步完善 fallback 模型链

### 当前状态
- NVIDIA provider 已加为备用模型来源。
- `openai-tts` 技能本身和链路已打通。
- 当前 TTS 真正阻塞点是 OpenAI key 无效。

### 下一步
- 如果主人后续提供有效 OpenAI key，可立即恢复 TTS 实战能力。
- 如需进一步自动容灾，可再考虑整理 fallback 模型链。

---

## 7. OpenClaw Web 访问线
- 优先级：高
- 最近更新时间：2026-04-16
- 阻塞状态：当前可用，后续以稳定维护为主
- 下一次触发条件：主人再次反馈 Web 控制台无法访问、密码登录失败、反代异常，或需要从临时方案切到更稳的 HTTPS 正路

### 当前状态
- OpenClaw Gateway 当前已恢复为 `bind=lan`，密码登录可用。
- 局域网地址 `http://192.168.50.100:18789/` 可访问。
- Lucky 反代 `https://claw.keket.cn:7788/` 已确认可正常密码登录。
- 当前反代方案的关键点已确认：`gateway.controlUi.allowedOrigins` 必须包含 `https://claw.keket.cn:7788`。

### 已确认事实
- 之前失败的真实根因不是密码错误，而是 WebSocket 握手阶段的 `origin not allowed`。
- `gateway.controlUi.allowedOrigins` 至少需要包含：
  - `http://192.168.50.100:18789`
  - `http://openclaw.local:18789`
  - `https://claw.keket.cn:7788`
- 当前仍属于临时可用优先方案，`dangerouslyDisableDeviceAuth=true` 还在使用中。

### 下一步
- 若主人继续用当前方案，重点是保持反代域名与 allowedOrigins 一致，不要漏配。
- 若后续要做长期加固，优先考虑更标准的 HTTPS 正路，并评估撤回 break-glass 配置。

---

## 8. 小记者内容线
- 优先级：中
- 最近更新时间：2026-04-18
- 阻塞状态：按需触发
- 下一次触发条件：主人提出小红书文案、配图、内容整理、发布准备或其他内容型任务

### 当前状态
- 已创建长期 agent：`xiaojizhe`
- 主人已明确：以后凡是小红书内容相关工作，默认优先交给 `xiaojizhe` 处理
- 主会话负责总调度、系统操作、跨线协同和必要回传

### 下一步
- 后续遇到小红书内容类任务时，优先调度给 `xiaojizhe`
- 若涉及账号登录、浏览器环境、文件路径、消息发送等系统动作，再由主会话承接或协同

---

## 9. 当前长期待办清单

### 高优先级
- 持续执行每日总结 / 日记
- 保持长期记忆检索习惯
- 新技能一律走“安装 + 验证 + 学习结论”流程

### 中优先级
- 继续完善技能体系
- 继续推进电商详情页路线
- 视需要继续排查 Telegram 其他偶发 API 失败

### 低优先级
- 继续追 `claw-ds-generator` 的替代能力，而不是死磕名字本身
