#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

if ! command -v python3 >/dev/null 2>&1; then
  echo "python3 not found" >&2
  exit 1
fi
if ! command -v node >/dev/null 2>&1; then
  echo "node not found" >&2
  exit 1
fi

python3 -m venv .venv
.venv/bin/pip install --upgrade pip
.venv/bin/pip install lunardate

if [ ! -f package.json ]; then
  cat > package.json <<'JSON'
{
  "name": "weather-push-replica",
  "private": true,
  "version": "1.0.0",
  "description": "Replicable weather push skill",
  "dependencies": {
    "playwright": "^1.52.0"
  }
}
JSON
fi

npm install
npx playwright install chromium

echo "install done"
