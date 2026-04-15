# 必学技能深入学习手册

更新时间：2026-04-15

本文聚焦主人指定的 10 个“必须学习技能”：

- weather
- Agent Browser
- claw-ds-generator
- cn-ecommerce-search
- duckduckgo-search
- find-skills
- openai-tts
- proactive-agent
- self-improvement
- tavily-search

目标不是重复 SKILL.md，而是给出当前环境下的真实可用性、推荐用法、风险点与替代关系。

---

## 1. weather

### 当前状态
- 已安装
- 当前主用：`skills/weather`
- 重复项：`skills/weather-1-0-0`

### 核心能力
- 当前天气
- 短期预报
- 不需要 API key
- 主服务：`wttr.in`
- 备选：`Open-Meteo`

### 当前环境可用性
- 可战斗
- 零额外配置
- 成本最低

### 推荐调用方式
- 简单天气：`wttr.in/城市?format=3`
- 更详细时再用完整 forecast
- 作为日常查询和 heartbeat 辅助能力很合适

### 风险点
- 免费服务偶发不稳定
- 复杂城市名要注意 URL 编码

### 结论
- 保留
- 主用 `weather`
- `weather-1-0-0` 作为重复包存在即可，不必主用

---

## 2. Agent Browser

### 当前状态
已装多条相关技能：
- `agent-browser-core`
- `agent-browser-clawdbot`
- `agent-browser-stagehand`

### 核心能力
- 浏览器自动化
- 基于快照和 refs 的稳定交互
- 多步网页流程控制
- 适合复杂 SPA、详情页提取、定向导航

### 当前环境可用性
- `agent-browser-core`：可战斗
- `agent-browser-clawdbot`：可战斗，偏操作手册
- `agent-browser-stagehand`：当前包不完整，不建议投入

### 推荐调用方式
优先顺序：
1. `agent-browser-core`
2. `agent-browser-clawdbot`
3. 不优先用 `agent-browser-stagehand`

最佳实践：
- 先 `open`
- 再 `snapshot -i --json`
- 用 ref 做 `click/fill/get`
- 页面变化后重新 snapshot

### 风险点
- 不是所有网站都能稳定自动化
- 登录态、风控、动态渲染仍可能阻塞
- 不要把 `stagehand` 当成熟主力

### 结论
- 这是当前浏览器线主力
- 对主人当前环境，优先级非常高

---

## 3. claw-ds-generator

### 当前状态
- 仍未安装成功
- `clawhub install claw-ds-generator` 返回：`Skill not found`

### 核心判断
- 当前没有找到对应真实 slug
- 多轮搜索没有找到明确对应条目

### 当前环境可用性
- 不可用

### 风险点
- 继续盲装只会重复报错
- 容易浪费限额和时间

### 结论
- 当前不继续盲重试
- 若主人后续提供原链接、作者名、截图，再反查真实 slug

---

## 4. cn-ecommerce-search

### 当前状态
已存在：
- `cn-ecommerce-search`
- `cn-ecommerce-search-v2`

### 核心能力
- 中国电商搜索
- 商品链接解析
- 比价与详情获取
- 面向淘宝、京东、拼多多、1688 等平台

### 当前环境可用性
- 旧版 `cn-ecommerce-search`：不可战斗
- `cn-ecommerce-search-v2`：当前主线，半可用但最值得继续用

### 真实原因
旧版阻塞不是本地环境，而是上游依赖：
- `@shopmeagent/cn-ecommerce-search-mcp`
- 当前公开 npm registry 直接 `404`

### 推荐调用方式
- 不再围绕旧版继续投入
- 以 `cn-ecommerce-search-v2` 为主
- 配合：
  - `agent-browser`
  - 外部搜索
  - 定向详情页路线

### 风险点
- 各平台风控差异大
- 搜索页和详情页可用性差异很大
- 不能承诺“一键全平台稳定对比”

### 结论
- 旧版保留作参考
- 实战主力切到 `cn-ecommerce-search-v2`

---

## 5. duckduckgo-search

### 当前状态
- 已安装
- 已验证可作为外部搜索主力之一

### 核心能力
- 文本搜索
- 新闻搜索
- 图片搜索
- 视频搜索
- Suggestions / Maps / Instant Answers
- 不需要 API key

### 当前环境可用性
- 可战斗

### 推荐调用方式
适用于：
- 找官网
- 找入口
- 找文章
- 搜商品详情页入口
- 当站内搜索被风控时做外部绕行

### 风险点
- 搜索质量不总是最优
- 更适合找入口，不一定适合深研究

### 结论
- 这是当前低成本外部搜索主力
- 与 Tavily 形成互补

---

## 6. find-skills

### 当前状态
- exact slug `find-skills` 当前装不上
- 但已有替代：
  - `find-skills-for-clawhub`
  - `openclaw-find-skills`

### 核心能力
- 搜技能
- 找替代技能
- 判断 OpenClaw 是否已有现成能力

### 当前环境可用性
- 名字本体不可装
- 目标能力已覆盖

### 推荐调用方式
主用：
- `find-skills-for-clawhub`
补充：
- `openclaw-find-skills`

### 风险点
- 技能站搜索结果可能受索引、限流、slug 不准影响
- 不能把搜索命中直接当“100% 可安装”

### 结论
- 不再执着 exact slug
- 当前能力已经到位

---

## 7. openai-tts

### 当前状态
- 已安装
- 当前半可用

### 核心能力
- 文本转语音
- 多 voice
- 可输出 mp3 / opus / wav 等

### 当前环境可用性
- 脚本链路正常
- 依赖链正常
- 网络正常
- 当前阻塞：**OpenAI key 无效**

### 已确认事实
服务端返回：
- `401`
- `invalid_api_key`

### 推荐调用方式
- 一旦换成有效 OpenAI key，可直接恢复
- 适合故事、摘要、短播报、语音回复

### 风险点
- 依赖官方可用 key
- 有成本

### 结论
- 技能本身没问题
- 当前不是真坏，是 key 问题

---

## 8. proactive-agent

### 当前状态
- 已安装
- 比 `proactive-agent-lite` 更完整

### 核心能力
- WAL Protocol
- Working Buffer
- Compaction Recovery
- Unified Search
- Security Hardening
- Autonomous vs Prompted Crons
- Self-improvement guardrails

### 当前环境可用性
- 可学习，适合长期方法论吸收
- 不建议直接整套覆盖现有 workspace 体系

### 推荐调用方式
重点吸收这些思想：
- 关键细节先写状态，再回复
- 上下文压缩前要有 working buffer
- 恢复上下文要先查文件，不先问用户
- 主动性要建立在真实价值而不是刷存在感上

### 风险点
- 它自带一整套 workspace 文件哲学
- 若机械照搬，容易和现有 AGENTS/SOUL/USER 体系冲突

### 结论
- 值得学
- 应该“吸收原则”，不是“整包照搬”

---

## 9. self-improvement

### 当前状态
- 已安装
- 高价值辅助技能

### 核心能力
- 记录错误
- 记录用户纠正
- 记录知识缺口
- 记录功能需求
- 推动长期改进

### 当前环境可用性
- 可用
- 非即战力型，但长期价值高

### 推荐调用方式
重点记录三类：
- `.learnings/ERRORS.md`
- `.learnings/LEARNINGS.md`
- `.learnings/FEATURE_REQUESTS.md`

适合记录：
- 失败命令
- 用户纠正
- 更优做法
- 外部 API 真实坑点

### 风险点
- 文档里有一些老口径，要以现网实测为准
- 不能为了“学习”而泛滥记流水账

### 结论
- 很适合主人当前长期调环境、装技能、排故障的场景
- 值得持续使用

---

## 10. tavily-search

### 当前状态
- exact slug `tavily-search` 装不上
- 但已有：
  - `liang-tavily-search`
  - `liang-tavily-extract`

### 核心能力
- LLM 友好的网页搜索
- 带 snippets / score / metadata
- 可配 domain include / exclude
- 可配 topic / depth / time range

### 当前环境可用性
- 能力已到位
- 已实测可用

### 推荐调用方式
- 广泛入口搜索时：DuckDuckGo
- 研究型搜索时：Tavily
- 已知 URL 的精读提取：`liang-tavily-extract`

### 风险点
- 依赖 Tavily key
- exact slug 装不上，不必执着名字一致

### 结论
- 当前实战主力用 `liang-tavily-search`
- 目标能力已经具备

---

# 最终总表

## 第一梯队，当前真主力
- `weather`
- `agent-browser-core`
- `agent-browser-clawdbot`
- `duckduckgo-search`
- `liang-tavily-search`
- `liang-tavily-extract`
- `proactive-agent`

## 第二梯队，有条件可用
- `self-improvement`
- `cn-ecommerce-search-v2`
- `openai-tts`（换有效 key 后恢复）

## 第三梯队，名字没装上但能力已被替代覆盖
- `find-skills`
- `tavily-search`
- `Agent Browser`（已由多个已装包覆盖）

## 当前仍未拿下
- `claw-ds-generator`

---

# 最小结论

主人这批“必须学习技能”里，真正没拿下的当前只剩：
- `claw-ds-generator`

其余都已经：
- 装上了，或者
- 已被更合适的替代技能覆盖了，或者
- 已经完成真实可用性验证。
