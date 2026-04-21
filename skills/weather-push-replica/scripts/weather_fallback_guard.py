#!/usr/bin/env python3
import json
import os
import subprocess
import sys
from datetime import datetime, timedelta
from pathlib import Path
from zoneinfo import ZoneInfo

TZ = ZoneInfo(os.getenv('WEATHER_TIMEZONE', 'Asia/Shanghai'))
WORKSPACE = Path(os.getenv('WEATHER_WORKSPACE', str(Path(__file__).resolve().parent.parent)))
MAIN_JOB_RUNS = Path(os.getenv('WEATHER_MAIN_RUNS_JSONL', '')) if os.getenv('WEATHER_MAIN_RUNS_JSONL') else None
OUTPUT_DIR = Path(os.getenv('WEATHER_OUTPUT_DIR', '/www/manmanai/openclaw/任务推送/天气'))
PNG = OUTPUT_DIR / 'weather_card_pw.png'


def log(msg: str):
    print(f'[weather_fallback_guard] {msg}', flush=True)


def shanghai_day_bounds(now: datetime):
    start = now.replace(hour=0, minute=0, second=0, microsecond=0)
    end = start + timedelta(days=1)
    return start, end


def load_jsonl(path: Path):
    if not path or not str(path) or not path.exists():
        return []
    rows = []
    for line in path.read_text(encoding='utf-8', errors='ignore').splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            rows.append(json.loads(line))
        except Exception:
            continue
    return rows


def find_today_7am_run():
    now = datetime.now(TZ)
    day_start, day_end = shanghai_day_bounds(now)
    rows = load_jsonl(MAIN_JOB_RUNS)
    matches = []
    for row in rows:
        run_at_ms = row.get('runAtMs')
        if not isinstance(run_at_ms, int):
            continue
        dt = datetime.fromtimestamp(run_at_ms / 1000, TZ)
        if not (day_start <= dt < day_end):
            continue
        if dt.hour != 7:
            continue
        if row.get('action') != 'finished':
            continue
        matches.append((dt, row))
    matches.sort(key=lambda x: x[0])
    return matches[-1][1] if matches else None


def is_delivered(row):
    if not row:
        return False
    return row.get('delivered') is True or row.get('deliveryStatus') == 'delivered' or row.get('status') == 'ok'


def run(cmd):
    log('run: ' + ' '.join(cmd))
    subprocess.run(cmd, check=True)


def build_card_and_send():
    env = os.environ.copy()
    env.setdefault('WEATHER_WORKSPACE', str(WORKSPACE))
    env.setdefault('WEATHER_OUTPUT_DIR', str(OUTPUT_DIR))
    env.setdefault('WEATHER_CHANNEL', 'telegram')
    env.setdefault('WEATHER_ACCOUNT_ID', 'agner')
    env.setdefault('WEATHER_TARGET', '1747307647')
    log('run: bash ' + str(WORKSPACE / 'scripts' / 'send_weather_card.sh'))
    subprocess.run(['bash', str(WORKSPACE / 'scripts' / 'send_weather_card.sh')], check=True, env=env)
    if not PNG.exists() or PNG.stat().st_size == 0:
        raise SystemExit('weather card png missing after render')
    log('fallback message delivered')


def main():
    if not MAIN_JOB_RUNS or not str(MAIN_JOB_RUNS):
        log('WEATHER_MAIN_RUNS_JSONL missing -> direct fallback send')
        build_card_and_send()
        return
    row = find_today_7am_run()
    if row is None:
        log('no finished 07:00 run found for today -> will fallback send')
        build_card_and_send()
        return
    log('today 07:00 run: ' + json.dumps({
        'status': row.get('status'),
        'delivered': row.get('delivered'),
        'deliveryStatus': row.get('deliveryStatus'),
        'runAtMs': row.get('runAtMs')
    }, ensure_ascii=False))
    if is_delivered(row):
        print('NO_REPLY')
        return
    build_card_and_send()


if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print(f'weather fallback failed: {e}', file=sys.stderr)
        raise
