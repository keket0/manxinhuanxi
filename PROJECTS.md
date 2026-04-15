# PROJECTS.md

更新时间：2026-04-15

这个文件用于维护持续项目、长期待办、当前状态和下一步。它不是流水账，而是项目索引。

---

## 1. Telegram 稳定性线

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

### 当前状态
- 长期目标是构建一套免费、稳定、可验证的技能体系。
- 已完成一批核心技能安装、验证、分层与学习。
- 已建立：
  - `INSTALLED_SKILLS_MAP.md`
  - `SKILLS_DEEP_DIVE_2026-04-15.md`

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
- 部分技能是参考型，不适合当主力。

### 下一步
- 需要补能力时，优先官方 ClawHub 和 GitHub 高 star 免费来源。
- 对新装技能保持“先装，再最小验证，再学习结论”的流程。

---

## 3. 中文电商搜索线

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

### 当前状态
- 已建立长期记忆体系：
  - `MEMORY.md`
  - `SESSION-STATE.md`
  - `memory/YYYY-MM-DD.md`
  - `memory/DAILY_TEMPLATE.md`
  - `HEARTBEAT.md`

### 已确认规则
- 过去事项先检索记忆再回答。
- 每天要补总结和日记。
- 稳定长期事实沉淀到 `MEMORY.md`。

### 下一步
- 持续执行，不靠临时记忆。
- 适时把当天关键信息从 daily note 提炼进 `MEMORY.md`。

---

## 5. 备份与可恢复性线

### 当前状态
- 大盘目录已准备好：`/www/manmanai/openclaw`
- 备份目录已准备好：`/www/manmanai/openclaw/backup`
- 已有备份脚本与快照基础。

### 已确认事实
- 大文件走 `/www/manmanai/openclaw`。
- 主目录仍在 `/root/.openclaw` 与 `/root/.openclaw/workspace`。
- 若未来重装系统，只保住 `/www` 盘还不够，核心配置仍需备份。

### 下一步
- 持续保持快照可恢复。
- 后续如有关键配置大改，改后补一份备份。

---

## 6. 模型与 TTS 能力线

### 当前状态
- NVIDIA provider 已加为备用模型来源。
- `openai-tts` 技能本身和链路已打通。
- 当前 TTS 真正阻塞点是 OpenAI key 无效。

### 下一步
- 如果主人后续提供有效 OpenAI key，可立即恢复 TTS 实战能力。
- 如需进一步自动容灾，可再考虑整理 fallback 模型链。

---

## 7. 当前长期待办清单

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
