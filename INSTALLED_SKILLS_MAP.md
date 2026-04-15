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

## 四、Telegram 相关

### 8. telegram-bot-manager
- 状态：可用
- 价值：Telegram bot 配置与管理
- 优先场景：bot 设置、网络检查、配置排查

### 9. openclaw-telegram-acp-troubleshooter
- 状态：可用
- 价值：排查 OpenClaw Telegram / ACP 相关问题
- 优先场景：Telegram 集成异常、命令菜单、连接链路排查

## 五、半可用

### 10. openai-tts
- 状态：半可用
- 已打通：脚本权限、`jq`、`curl`、网络链路、代理
- 当前阻塞：OpenAI key 无效，返回 `401 invalid_api_key`
- 优先场景：文本转语音、音频输出
- 备注：一旦换成有效官方 key，可直接转正

## 六、当前仍未拿下的主线

### 第一优先
1. `agent-browser-core`
2. `find-skills-for-clawhub`

### 第二优先
3. `openclaw-find-skills`
4. `agent-browser-stagehand`

### 次级
5. `message-routing`
6. `liang-tavily-extract`
7. `reflect`

## 七、原始“必须学习技能”映射

- `weather` → 已可用
- `Agent Browser` → 未装上，主追 `agent-browser-core`
- `claw-ds-generator` → 高概率不存在 / 下架 / 名字不对
- `cn-ecommerce-search` → 已可用
- `duckduckgo-search` → 已可用
- `find-skills` → 未装上，主追 `find-skills-for-clawhub`
- `openai-tts` → 已装，半可用
- `proactive-agent` → 已有替代 `proactive-agent-lite`
- `self-improvement` → 已可用
- `tavily-search` → 已可用

## 八、当前最实用的技能组合

### 资料检索组合
- `tavily-search`
- `duckduckgo-search`
- `weather`

### 行为增强组合
- `proactive-agent-lite`
- `self-improvement`
- `self-improving-proactive-agent`

### 中文电商组合
- `cn-ecommerce-search`

### Telegram 运维组合
- `telegram-bot-manager`
- `openclaw-telegram-acp-troubleshooter`

## 九、一句话总结

现在最缺的已经不是搜索、主动性、自我改进、电商，而是：
- 浏览器自动化
- 技能发现导航
