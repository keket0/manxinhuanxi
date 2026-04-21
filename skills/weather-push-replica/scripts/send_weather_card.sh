#!/usr/bin/env bash
set -euo pipefail

WORKSPACE="${WEATHER_WORKSPACE:-$(cd "$(dirname "$0")/.." && pwd)}"
OUTPUT_DIR="${WEATHER_OUTPUT_DIR:-/www/manmanai/openclaw/任务推送/天气}"
CHANNEL="${WEATHER_CHANNEL:-telegram}"
ACCOUNT="${WEATHER_ACCOUNT_ID:-agner}"
SENDER_MODE="${WEATHER_SENDER_MODE:-openclaw}"
TARGET="${WEATHER_TARGET:-}"
if [ "$SENDER_MODE" = "openclaw" ] && [ -z "$TARGET" ]; then
  echo "WEATHER_TARGET is required when WEATHER_SENDER_MODE=openclaw" >&2
  exit 1
fi

mkdir -p "$OUTPUT_DIR"
cd "$WORKSPACE"
PYTHON_BIN="${WEATHER_PYTHON_BIN:-$WORKSPACE/.venv/bin/python}"
if [ ! -x "$PYTHON_BIN" ]; then
  PYTHON_BIN="python3"
fi
WEATHER_OUTPUT_DIR="$OUTPUT_DIR" "$PYTHON_BIN" scripts/weather_card.py >/tmp/weather_card_paths.txt
WEATHER_OUTPUT_DIR="$OUTPUT_DIR" "$PYTHON_BIN" scripts/render_weather_card.py >/tmp/weather_render.log 2>&1
WEATHER_OUTPUT_DIR="$OUTPUT_DIR" node scripts/weather_card_playwright_screenshot.js >/tmp/weather_pw.log 2>&1
"$PYTHON_BIN" - <<'PY'
import json, os
from pathlib import Path
output_dir = Path(os.environ.get('WEATHER_OUTPUT_DIR', '/www/manmanai/openclaw/任务推送/天气'))
meta = json.loads((output_dir / 'weather_card_meta.json').read_text(encoding='utf-8'))
caption = (meta.get('one_liner') or '').strip()
if not caption:
    raise SystemExit('missing weather caption')
Path('/tmp/weather_caption.txt').write_text(caption, encoding='utf-8')
PY
CAPTION=$(cat /tmp/weather_caption.txt)
if [ "$SENDER_MODE" = "openclaw" ]; then
  openclaw message send --channel "$CHANNEL" --account "$ACCOUNT" --target "$TARGET" --media "$OUTPUT_DIR/weather_card_pw.png" --message "$CAPTION" --json
else
  echo "WEATHER_SENDER_MODE=$SENDER_MODE, skip built-in send"
  echo "$CAPTION"
fi

# 推送成功后清理非必要中间产物，保留截图与图标目录
find "$OUTPUT_DIR" -maxdepth 1 -type f \( -name 'weather_card.html' -o -name 'weather_card_meta.json' -o -name 'weather_card_caption.txt' -o -name 'weather_raw.json' -o -name 'weather_card.png' \) -delete
