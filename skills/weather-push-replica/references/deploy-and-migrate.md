# 部署与迁移说明

## 1. 作用
这套技能用于生成并发送当前确认版天气卡，包含：
- `wttr.in` 主源 + `Open-Meteo` 校验
- 中文天气卡图片
- Playwright 截图
- 天气文字提醒
- OpenClaw 发送
- 07:00 主推送 + 08:00 兜底补发

## 2. 目录重点
```text
weather-push-replica/
├── SKILL.md
├── scripts/
│   ├── weather_card.py
│   ├── render_weather_card.py
│   ├── weather_card_playwright_screenshot.js
│   ├── send_weather_card.sh
│   └── weather_fallback_guard.py
├── assets/
│   ├── icons-legacy/
│   └── twemoji-weather/
└── references/
    └── deploy-and-migrate.md
```

## 3. 运行依赖
建议目标机器具备：
- Python 3.11+
- Node.js 18+
- Playwright + Chromium
- OpenClaw CLI（如果继续走 OpenClaw 发送）

### Python venv
```bash
python3 -m venv .venv
.venv/bin/pip install lunardate
```

### Playwright
```bash
npm install playwright
npx playwright install chromium
```

## 4. 常用环境变量
### 基础
```bash
export WEATHER_WORKSPACE=/path/to/weather-push-replica
export WEATHER_OUTPUT_DIR=/data/weather-output
export WEATHER_PYTHON_BIN=/path/to/weather-push-replica/.venv/bin/python
```

### 发送
```bash
export WEATHER_SENDER_MODE=openclaw
export WEATHER_CHANNEL=telegram
export WEATHER_ACCOUNT_ID=agner
export WEATHER_TARGET=1747307647
```

### 只生成不发送
```bash
export WEATHER_SENDER_MODE=none
```

### 城市参数
```bash
export WEATHER_WTTR_QUERY=枣庄
export WEATHER_TARGET_CITY=枣庄
export WEATHER_TARGET_LAT=34.81071
export WEATHER_TARGET_LON=117.32373
export WEATHER_TARGET_TZ=Asia/Shanghai
export WEATHER_OPEN_METEO_GEOCODE='https://geocoding-api.open-meteo.com/v1/search?name=%E6%9E%A3%E5%BA%84%E5%B8%82&count=5&language=zh&format=json'
```

## 5. 当前线上行为
- 用户发“天气”即实时推送
- 成功时默认静默
- 发送后会清理 `weather_card.html`、`weather_card_meta.json`、`weather_raw.json` 等中间文件
- 默认保留最终图 `weather_card_pw.png`

## 6. 当前视觉与文案约束
- 城市标题只显示城市名，不显示“地区”
- “每日一句”使用随机句库
- “简短提醒”的天气字位置已单独调好
- 逐时天气与未来天气速览的天气 emoji 大小保持当前确认版
- 其他标题 emoji 可单独调，但不要误伤逐时/速览区

## 7. 最小验证
```bash
WEATHER_SENDER_MODE=none bash scripts/send_weather_card.sh
```
检查：
- 成功生成 `weather_card_pw.png`
- 卡片布局正常
- 城市标题显示为城市名
- “每日一句”不是固定一句
- 逐时天气标题按当前时段动态变化

## 8. 如果要迁移到另一台机器
优先直接复制整个技能目录，不要只拷单个脚本。

至少一起带走：
- `scripts/`
- `assets/icons-legacy/`
- `assets/twemoji-weather/`
- `.venv` 的安装方式（可重建，不强拷）

## 9. 修改建议
- 版式修改优先改 `render_weather_card.py`
- 文案、句库、提醒逻辑优先改 `weather_card.py`
- 若用户只点一个局部，尽量只改该局部，减少回滚成本
