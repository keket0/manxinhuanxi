#!/usr/bin/env python3
import json, html, os
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
TEMPLATE = json.loads((BASE / 'assets' / 'template-config.json').read_text(encoding='utf-8'))
LAYOUT = TEMPLATE.get('layout', {})
FONT = TEMPLATE.get('font_sizes', {})
ICON_SIZES = TEMPLATE.get('icon_sizes', {})
SYMBOL_SIZES = TEMPLATE.get('weather_symbol_sizes', {})
CITY_DISPLAY = TEMPLATE.get('city_display', {})
OUTPUT_DIR = Path(os.environ.get('WEATHER_OUTPUT_DIR', '/www/manmanai/openclaw/任务推送/天气'))
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
META = OUTPUT_DIR / 'weather_card_meta.json'
HTML = OUTPUT_DIR / 'weather_card.html'

meta = json.loads(META.read_text(encoding='utf-8'))

def icon(src: str, label: str, size: int = 28, valign: int = -5):
    return f'<img src="{src}" alt="{html.escape(label)}" style="width:{size}px;height:{size}px;vertical-align:{valign}px;display:inline-block;" />'


def pick_weather_symbol_name(text: str) -> str:
    t = (text or '').strip()
    if any(k in t for k in ['雷', '暴雨', '大雨', '中雨', '阵雨', '雨']):
        return 'rain.svg'
    if any(k in t for k in ['雪', '冰雹', '冻雨']):
        return 'snow.svg'
    if any(k in t for k in ['雾', '霾', '沙', '尘', '霭']):
        return 'fog.svg'
    if any(k in t for k in ['阴', '多云']):
        return 'cloud-sun.svg'
    if any(k in t for k in ['风', '大风']):
        return 'wind.svg'
    return 'sun.svg'


def weather_symbol(text: str, size: int, cls: str = '') -> str:
    symbol_dir = Path(os.environ.get('WEATHER_SYMBOLS_DIR', str(BASE / 'assets' / 'twemoji-weather')))
    path = symbol_dir / pick_weather_symbol_name(text)
    class_attr = f' class="{cls}"' if cls else ''
    return f'<img src="{path.as_uri()}" alt="{html.escape(text or "天气")}"{class_attr} style="width:{size}px;height:{size}px;display:inline-block;" />'


icon_dir = Path(os.environ.get('WEATHER_ICONS_DIR', str(BASE / 'assets' / 'icons-legacy')))
ICON = {
    'weather': icon((icon_dir / 'weather.svg').as_uri(), '天气', ICON_SIZES.get('weather', 28)),
    'pin': icon((icon_dir / 'pin.svg').as_uri(), '地点', ICON_SIZES.get('pin', 34)),
    'note': icon((icon_dir / 'note.svg').as_uri(), '今日一句', ICON_SIZES.get('note', 34)),
    'bell': icon((icon_dir / 'bell.svg').as_uri(), '简短提醒', ICON_SIZES.get('bell', 34)),
    'coat': icon((icon_dir / 'coat.svg').as_uri(), '穿衣指数', ICON_SIZES.get('coat', 32)),
    'cold': icon((icon_dir / 'cold.svg').as_uri(), '感冒指数', ICON_SIZES.get('cold', 32)),
    'run': icon((icon_dir / 'run.svg').as_uri(), '运动指数', ICON_SIZES.get('run', 32)),
    'sun': icon((icon_dir / 'sun.svg').as_uri(), '紫外线指数', ICON_SIZES.get('sun', 32)),
    'clock': icon((icon_dir / 'clock.svg').as_uri(), '逐时天气', ICON_SIZES.get('clock', 28)),
    'calendar': icon((icon_dir / 'calendar.svg').as_uri(), '未来天气', ICON_SIZES.get('calendar', 28)),
}

future_html = ''.join(
    f'<div class="future-item"><div class="ficon">{weather_symbol(x.get("weather", "天气"), SYMBOL_SIZES.get("future", 54), "ficon-img")}</div><div class="future-content"><div class="fday">{html.escape(x["day"])}</div><div class="fweather"><span>{html.escape(x["weather"])}</span></div><div class="ftemp">{html.escape(x["temp"])}</div></div></div>'
    for x in meta.get('future', [])[:3]
)
weather_text = meta.get('weather', '--')
weather_emoji_html = weather_symbol(weather_text, SYMBOL_SIZES.get('main', 72), 'main-weather-emoji')
weather_display = html.escape(weather_text)

def display_city_name(raw: str) -> str:
    s = (raw or '').strip()
    if not s:
        return CITY_DISPLAY.get('fallback', '枣庄')
    for suffix in CITY_DISPLAY.get('strip_suffixes', ['地区', '市', '区', '县', '州', '盟']):
        if s.endswith(suffix):
            s = s[:-len(suffix)]
            break
    return s.strip() or (raw or '').strip()

city_display = display_city_name(meta.get('city', '枣庄'))

hourly_cards = meta.get('hourly_cards', [])[:4]
if len(hourly_cards) >= 2:
    hourly_title = f"{hourly_cards[0].get('time', '--')}-{hourly_cards[-1].get('time', '--')} 逐时天气"
elif len(hourly_cards) == 1:
    hourly_title = f"{hourly_cards[0].get('time', '--')} 起逐时天气"
else:
    hourly_title = '逐时天气'

hourly_html = ''.join(
    '<div class="hour-item">'
    f'<div class="hicon">{weather_symbol(x.get("weather", "天气"), SYMBOL_SIZES.get("hourly", 50), "hicon-img")}</div>'
    '<div class="hour-content">'
    f'<div class="htime">{html.escape(x.get("time", "--"))}</div>'
    f'<div class="htemp">{html.escape(x.get("temp", "--"))}</div>'
    f'<div class="hweather"><span>{html.escape(x.get("weather", "--"))}</span></div>'
    f'<div class="hrain">降雨 {html.escape(x.get("rain_prob", "--"))}</div>'
    f'<div class="hwind">{html.escape(x.get("wind", "--"))}</div>'
    '</div>'
    '</div>'
    for x in hourly_cards
)

def title_with_icon(icon_html: str, text: str, klass: str) -> str:
    return f'<div class="{klass} center-title-row"><span class="title-wrap"><span class="title-icon">{icon_html}</span><span class="title-text">{html.escape(text)}</span></span></div>'


def box(title_html, item):
    return f'''<div class="index-box center-box">{title_html}<div class="ibox-level center-text">{html.escape(item.get("level","--"))}</div><div class="ibox-desc center-text">{html.escape(item.get("desc","--"))}</div></div>'''

html_doc = f'''<!doctype html>
<html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>天气卡</title>
<style>
*{{box-sizing:border-box}}
body{{-webkit-font-smoothing:antialiased;-moz-osx-font-smoothing:grayscale;text-rendering:optimizeLegibility;margin:0;font-family:'PingFang SC','Noto Sans CJK SC','Microsoft YaHei','Segoe UI',system-ui,-apple-system,BlinkMacSystemFont,sans-serif;background:#071a2b}}
.card{{width:1080px;min-height:1868px;color:#fff;background:radial-gradient(circle at top right,#67e8f944,transparent 25%),radial-gradient(circle at bottom left,#93c5fd44,transparent 25%),linear-gradient(160deg,#0b2d4d,#123b67 50%,#0e7490);padding:60px 58px 48px;display:flex;flex-direction:column;gap:18px;overflow:hidden}}
.top{{display:flex;justify-content:space-between;align-items:center}}
.badge{{font-size:32px;font-weight:900;padding:12px 22px;border-radius:999px;background:#ffffff16;border:1px solid #ffffff26}}
.date{{font-size:32px;font-weight:900;color:#c8f5ff}}
.main{{display:grid;grid-template-columns:1.5fr 0.5fr;gap:18px;align-items:stretch}}
.hero{{background:#ffffff12;border:1px solid #ffffff24;border-radius:30px;padding:48px 44px 44px;display:flex;flex-direction:column;gap:20px;min-height:648px;position:relative}}
.city{{font-size:48px;color:#d6f7ff;font-weight:800}}
.sub{{font-size:24px;color:#b9d8ef}}
.weather{{font-size:108px;line-height:1.04;font-weight:900;margin-top:26px;word-break:break-word;text-align:center}}
.main-weather-emoji{{position:absolute;top:28px;right:24px;width:78px;height:78px;display:block}}
.temp{{font-size:86px;font-weight:900;color:#fde68a;line-height:1.03;text-align:center}}
.wind{{font-size:36px;color:#e0f2fe;font-weight:700;text-align:center}}
.tip{{margin-top:24px;font-size:33px;line-height:1.48;font-weight:650;color:#f8fafc;word-break:break-word;text-align:center}}
.side{{display:grid;grid-template-rows:repeat(2,minmax(0,1fr));gap:14px;min-height:648px}}
.side-card{{background:#ffffff12;border:1px solid #ffffff24;border-radius:28px;padding:22px 20px;display:flex;flex-direction:column;gap:8px;justify-content:flex-start;overflow:hidden;min-height:248px}}
.side-card.centered-body{{justify-content:flex-start}}
.sc-title{{font-size:28px;color:#c8f5ff;font-weight:900;margin-bottom:2px}}
.sc-big{{font-size:42px;font-weight:1000;line-height:1.08;word-break:break-word;margin-top:0}}
.short-label-wrap{{display:flex;align-items:center;justify-content:center;width:100%;min-height:72px}}
.short-label{{position:relative;top:0}}
.short-card-body{{flex:1;display:grid;grid-template-rows:auto 1fr auto;align-items:stretch;text-align:center;width:100%;padding:10px 2px 4px}}
.short-gap{{display:flex;align-items:center;justify-content:center;width:100%;min-height:96px}}
.short-desc-fixed{{margin-top:0}}
.sc-text{{font-size:27px;line-height:1.5;color:#eef8ff;font-weight:650;word-break:break-word;text-align:center}}
.indices{{display:grid;grid-template-columns:1fr 1fr;gap:20px;margin-top:44px}}
.index-box{{background:#ffffff12;border:1px solid #ffffff24;border-radius:26px;padding:26px 26px;min-height:218px;display:flex;flex-direction:column;gap:12px;overflow:hidden}}
.ibox-title{{font-size:28px;color:#c8f5ff;font-weight:900;margin-bottom:2px}}
.ibox-level{{font-size:42px;font-weight:1000;line-height:1.08;word-break:break-word}}
.ibox-desc{{font-size:27px;line-height:1.5;color:#eef8ff;font-weight:650;word-break:break-word}}
.center-title{{text-align:center}}
.center-text{{text-align:center}}
.center-title-row{{width:100%;text-align:center;line-height:1.24}}
.center-title-row .title-wrap{{position:relative;display:inline-block;padding-top:2px;padding-bottom:2px}}
.center-title-row .title-icon{{position:absolute;right:100%;top:50%;transform:translateY(-50%);margin-right:8px;line-height:0}}
.center-title-row .title-text{{display:inline-block}}
.center-column{{display:flex;flex-direction:column;align-items:center;text-align:center}}
.hourly{{background:#ffffff12;border:1px solid #ffffff24;border-radius:30px;padding:28px 30px;display:flex;flex-direction:column;gap:18px}}
.section-title{{font-size:30px;color:#c8f5ff;font-weight:900}}
.hourly-grid{{display:grid;grid-template-columns:repeat(4,1fr);gap:18px}}
.hour-item{{background:#ffffff10;border:1px solid #ffffff1f;border-radius:22px;padding:18px 16px;min-height:224px;display:flex;flex-direction:column;gap:10px;overflow:hidden;position:relative}}
.hicon{{position:absolute;top:10px;right:12px;line-height:1;transform-origin:top right;z-index:2}}
.hicon-img{{width:46px;height:46px;display:block}}
.hour-content{{width:100%;display:flex;flex-direction:column;gap:8px;align-items:center;justify-content:flex-start}}
.htime{{width:100%;font-size:24px;color:#dbeafe;font-weight:900;text-align:left}}
.htemp{{font-size:34px;color:#fde68a;font-weight:1000;line-height:1.08;text-align:center}}
.hweather{{font-size:28px;font-weight:800;line-height:1.12;text-align:center;padding-top:4px}}
.hweather span{{display:inline-block}}
.hrain{{font-size:25px;color:#d1fae5;font-weight:700;text-align:center}}
.hwind{{font-size:25px;color:#e0f2fe;font-weight:700;line-height:1.38;word-break:break-word;text-align:center}}
.future{{background:#ffffff12;border:1px solid #ffffff24;border-radius:30px;padding:28px 30px;display:flex;flex-direction:column;gap:18px}}
.future-grid{{display:grid;grid-template-columns:1fr 1fr 1fr;gap:18px}}
.future-item{{background:#ffffff10;border:1px solid #ffffff1f;border-radius:22px;padding:20px 18px;min-height:176px;display:flex;flex-direction:column;gap:10px;overflow:hidden;position:relative}}
.ficon{{position:absolute;top:10px;right:12px;line-height:1;transform-origin:top right;z-index:2}}
.ficon-img{{width:50px;height:50px;display:block}}
.future-content{{width:100%;display:flex;flex-direction:column;gap:8px;align-items:center;justify-content:flex-start}}
.fday{{width:100%;font-size:24px;color:#dbeafe;font-weight:900;line-height:1.22;text-align:left}}
.fweather{{font-size:30px;font-weight:800;line-height:1.12;word-break:break-word;text-align:center;padding-top:8px}}
.fweather span{{display:inline-block}}
.ftemp{{font-size:27px;color:#fde68a;font-weight:800;line-height:1.08;text-align:center}}
</style></head><body><div class="card">
<div class="top"><div class="badge">{ICON['weather']} 每日天气提醒</div><div class="date">{html.escape(meta.get('date','--'))}</div></div>
<div class="main">
  <div class="hero">{weather_emoji_html}{title_with_icon(ICON['pin'], city_display, 'city')}<div class="weather">{weather_display}</div><div class="temp">{html.escape(meta.get('temp','--'))}</div><div class="wind">风力：{html.escape(meta.get('wind','--'))}</div><div class="tip">{html.escape(meta.get('suggestion','出门记得看路况，注意保暖。'))}</div></div>
  <div class="side"><div class="side-card center-column">{title_with_icon(ICON['note'], '今日一句', 'sc-title')}<div style="flex:1;display:flex;align-items:center;justify-content:center;text-align:center;width:100%;padding:10px 4px 4px;"><div class="sc-text" style="max-width:100%;">{html.escape(meta.get('tagline','天气早知道，出门不慌张。'))}</div></div></div><div class="side-card center-column">{title_with_icon(ICON['bell'], '简短提醒', 'sc-title')}<div class="short-card-body"><div class="short-gap"><div class="sc-big short-label">{html.escape(meta.get('short_label','天气提醒'))}</div></div><div class="sc-text short-desc-fixed">{html.escape(meta.get('short_desc','提前看一眼，安排更从容。'))}</div></div></div></div>
</div>
<div class="indices">{box(title_with_icon(ICON['coat'], '穿衣指数', 'ibox-title'), meta.get('indices',{}).get('穿衣指数',{}))}{box(title_with_icon(ICON['cold'], '感冒指数', 'ibox-title'), meta.get('indices',{}).get('感冒指数',{}))}{box(title_with_icon(ICON['run'], '运动指数', 'ibox-title'), meta.get('indices',{}).get('运动指数',{}))}{box(title_with_icon(ICON['sun'], '紫外线指数', 'ibox-title'), meta.get('indices',{}).get('紫外线指数',{}))}</div>
<div class="hourly"><div class="section-title">{ICON['clock']} {html.escape(hourly_title)}</div><div class="hourly-grid">{hourly_html}</div></div>
<div class="future"><div class="section-title">{ICON['calendar']} 未来 3 天天气速览</div><div class="future-grid">{future_html}</div></div>
</div></body></html>'''

HTML.write_text(html_doc, encoding='utf-8')
print(str(HTML))
print('rendered with hourly + future layout')
