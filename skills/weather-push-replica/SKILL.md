---
name: weather-push-replica
description: 生成并发送当前正式版天气卡与天气文字。用于用户说“天气”时即时推送，也用于维护天气卡布局、天气文案、发送链路、定时补发与迁移部署。
---

# Weather Push Replica

当前正式天气技能，负责“生成天气卡 + 文字推送 + 直接发送”。

## 何时使用
- 用户说“天气”，需要立刻实时推送
- 用户要改天气卡布局、文案、标题、天气符号、发送行为
- 用户要维护定时天气推送或兜底补发
- 用户要迁移这套天气能力到别的机器

## 默认行为
- 生成天气卡图片和对应文字
- 默认直接按已配置目标发送
- 成功后静默，不额外回执
- 文字推送中：
  - 有雨雪时段时，写“几点下、几点停”
  - 雨雪已过时，不再报降水概率
  - 没有雨雪时段时，这一段留空

## 当前链路
- 主天气源：`wttr.in`
- 校验与逐小时雨雪时段：`Open-Meteo`
- 输出目录：`/www/manmanai/openclaw/任务推送/天气`
- 默认发送：Telegram `agner -> 1747307647`

## 固定约束
- 用户发“天气”时默认直接实时推送，不先确认
- 成功时默认静默，除非失败或用户明确要求查看结果
- 城市标题只显示城市名，不显示“地区”
- 天气状态语义固定：☀️ 晴、🌧️ 小雨、❄️ 小雪、⛅ 多云、🌫️ 雾、💨 大风
- 保持当前确认版布局与天气符号风格，不随意重做整张卡
- 只在用户点名模块时做局部修改，优先直接出图验证

## 关键文件
- `scripts/weather_card.py`：天气数据、文字推送、雨雪时段逻辑
- `scripts/render_weather_card.py`：版式、字体、标题、天气符号与卡片渲染
- `scripts/weather_card_playwright_screenshot.js`：截图
- `scripts/send_weather_card.sh`：发送与清理
- `scripts/weather_fallback_guard.py`：兜底补发
- `assets/template-config.json`：模板参数入口
- `references/deploy-and-migrate.md`：迁移说明

## 常用执行
### 直接发送当前天气卡
```bash
WEATHER_WORKSPACE="/root/.openclaw/workspace-agner/skills/weather-push-replica" \
WEATHER_OUTPUT_DIR="/www/manmanai/openclaw/任务推送/天气" \
WEATHER_CHANNEL="telegram" \
WEATHER_ACCOUNT_ID="agner" \
WEATHER_TARGET="1747307647" \
WEATHER_PYTHON_BIN="/root/.openclaw/workspace-agner/skills/weather-push-replica/.venv/bin/python" \
bash scripts/send_weather_card.sh
```

### 只生成不发送
```bash
WEATHER_SENDER_MODE=none bash scripts/send_weather_card.sh
```

### 临时切城市
运行前覆盖这些环境变量：
- `WEATHER_WTTR_QUERY`
- `WEATHER_TARGET_CITY`
- `WEATHER_TARGET_LAT`
- `WEATHER_TARGET_LON`
- `WEATHER_TARGET_TZ`
- `WEATHER_OPEN_METEO_GEOCODE`

## 维护原则
- 优先保留当前正式版外观，不轻易换风格
- 调整天气文案时，先改文字逻辑，再做一次实际生成验证
- 用户要求“滚回”时，只回滚最近一层相关改动
- 迁移或导出技能时，不要把 `.venv/`、`__pycache__/`、运行截图与生成产物一起打包
