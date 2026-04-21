#!/usr/bin/env python3
import html
import json
import math
import re
import ssl
import urllib.parse
import os
import random
from datetime import datetime
from pathlib import Path
from urllib.request import Request, urlopen

from lunardate import LunarDate

BASE = Path(__file__).resolve().parent.parent
TEMPLATE_CONFIG = json.loads((BASE / 'assets' / 'template-config.json').read_text(encoding='utf-8'))
OUTPUT_DIR = Path(os.environ.get('WEATHER_OUTPUT_DIR', '/www/manmanai/openclaw/任务推送/天气'))
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
HTML = OUTPUT_DIR / 'weather_card.html'
META = OUTPUT_DIR / 'weather_card_meta.json'
PNG = OUTPUT_DIR / 'weather_card.png'
TEXT = OUTPUT_DIR / 'weather_card_caption.txt'
RAW = OUTPUT_DIR / 'weather_raw.json'

WTTR_QUERY = os.environ.get('WEATHER_WTTR_QUERY', '枣庄')
TARGET_CITY = os.environ.get('WEATHER_TARGET_CITY', '枣庄地区')
TARGET_LAT = float(os.environ.get('WEATHER_TARGET_LAT', '34.81071'))
TARGET_LON = float(os.environ.get('WEATHER_TARGET_LON', '117.32373'))
TARGET_TZ = os.environ.get('WEATHER_TARGET_TZ', 'Asia/Shanghai')
OPEN_METEO_GEOCODE = os.environ.get('WEATHER_OPEN_METEO_GEOCODE', 'https://geocoding-api.open-meteo.com/v1/search?name=%E6%9E%A3%E5%BA%84%E5%B8%82&count=5&language=zh&format=json')

ctx = ssl.create_default_context()
weekday_map = '一二三四五六日'
LUNAR_MONTHS = ['正月', '二月', '三月', '四月', '五月', '六月', '七月', '八月', '九月', '十月', '冬月', '腊月']
LUNAR_DAYS = ['初一', '初二', '初三', '初四', '初五', '初六', '初七', '初八', '初九', '初十', '十一', '十二', '十三', '十四', '十五', '十六', '十七', '十八', '十九', '二十', '廿一', '廿二', '廿三', '廿四', '廿五', '廿六', '廿七', '廿八', '廿九', '三十']
SOLAR_FESTIVALS = {
    (1, 1): '元旦',
    (2, 14): '情人节',
    (3, 8): '妇女节',
    (5, 1): '劳动节',
    (6, 1): '儿童节',
    (10, 1): '国庆节',
    (12, 25): '圣诞节',
}
LUNAR_FESTIVALS = {
    (1, 1): '春节',
    (1, 15): '元宵节',
    (5, 5): '端午节',
    (7, 7): '七夕',
    (8, 15): '中秋节',
    (9, 9): '重阳节',
    (12, 8): '腊八节',
    (12, 23): '小年',
}
WEATHER_CODE_MAP = {
    113: '晴', 116: '多云', 119: '阴', 122: '阴', 143: '雾', 176: '小雨', 179: '雨夹雪', 182: '雨夹雪', 185: '冻雨',
    200: '雷暴', 227: '飘雪', 230: '暴雪', 248: '雾', 260: '雾', 263: '小雨', 266: '小雨', 281: '冻雨', 284: '冻雨',
    293: '小雨', 296: '小雨', 299: '中雨', 302: '中雨', 305: '大雨', 308: '大雨', 311: '冻雨', 314: '冻雨',
    317: '雨夹雪', 320: '雨夹雪', 323: '小雪', 326: '小雪', 329: '中雪', 332: '中雪', 335: '大雪', 338: '大雪',
    350: '阵雪', 353: '阵雨', 356: '中雨', 359: '大雨', 362: '雨夹雪', 365: '雨夹雪', 368: '阵雪', 371: '大雪',
    374: '冰粒', 377: '冰粒', 386: '雷阵雨', 389: '强雷阵雨', 392: '雷阵雪', 395: '暴雪'
}
OPEN_METEO_CODE_MAP = {
    0: '晴', 1: '晴', 2: '多云', 3: '阴', 45: '雾', 48: '雾凇', 51: '毛毛雨', 53: '毛毛雨', 55: '毛毛雨',
    56: '冻毛毛雨', 57: '冻毛毛雨', 61: '小雨', 63: '中雨', 65: '大雨', 66: '冻雨', 67: '冻雨', 71: '小雪',
    73: '中雪', 75: '大雪', 77: '雪粒', 80: '阵雨', 81: '阵雨', 82: '暴雨', 85: '阵雪', 86: '阵雪',
    95: '雷暴', 96: '雷暴冰雹', 99: '强雷暴冰雹'
}
TAGLINE_POOL = TEMPLATE_CONFIG.get('taglines', [
    '天气早知道，出门不慌张。'
])
DIR16_TO_CN = {
    'N': '北风', 'NNE': '东北偏北风', 'NE': '东北风', 'ENE': '东北偏东风',
    'E': '东风', 'ESE': '东南偏东风', 'SE': '东南风', 'SSE': '东南偏南风',
    'S': '南风', 'SSW': '西南偏南风', 'SW': '西南风', 'WSW': '西南偏西风',
    'W': '西风', 'WNW': '西北偏西风', 'NW': '西北风', 'NNW': '西北偏北风'
}


def fetch_text(url: str, headers=None) -> str:
    req = Request(url, headers=headers or {'User-Agent': 'Mozilla/5.0'})
    with urlopen(req, timeout=20, context=ctx) as resp:
        return resp.read().decode('utf-8', 'replace')


def fetch_json(url: str, headers=None):
    return json.loads(fetch_text(url, headers=headers))


def clean_text(s: str, default='--') -> str:
    s = html.unescape((s or '').strip())
    s = re.sub(r'\s+', ' ', s).strip(' ，,;；')
    return s or default


def celsius_text(v) -> str:
    if v is None or v == '--':
        return '--'
    n = float(v)
    if abs(n - round(n)) < 0.05:
        return f'{int(round(n))}℃'
    return f'{n:.1f}℃'


def temp_number_text(v) -> str:
    n = float(v)
    if abs(n - round(n)) < 0.05:
        return str(int(round(n)))
    return f'{n:.1f}'


def haversine_km(lat1, lon1, lat2, lon2):
    r = 6371.0
    p1 = math.radians(float(lat1))
    p2 = math.radians(float(lat2))
    dp = math.radians(float(lat2) - float(lat1))
    dl = math.radians(float(lon2) - float(lon1))
    a = math.sin(dp / 2) ** 2 + math.cos(p1) * math.cos(p2) * math.sin(dl / 2) ** 2
    return r * 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))


def weather_bucket(text: str) -> str:
    s = text or ''
    if '雷' in s:
        return 'storm'
    if any(x in s for x in ['雪', '冰']):
        return 'snow'
    if any(x in s for x in ['雨', '毛毛']):
        return 'rain'
    if '雾' in s:
        return 'fog'
    if '晴' in s:
        return 'clear'
    if any(x in s for x in ['云', '阴']):
        return 'cloud'
    return 'other'


def wttr_desc(item):
    desc = clean_text((item.get('weatherDesc') or [{'value': '--'}])[0].get('value', '--'))
    code = item.get('weatherCode')
    try:
        code = int(code)
    except Exception:
        code = None
    return WEATHER_CODE_MAP.get(code, desc)


def open_meteo_desc(code):
    try:
        code = int(code)
    except Exception:
        return '--'
    return OPEN_METEO_CODE_MAP.get(code, f'天气码{code}')


def wind_level(speed_kmh: float | None) -> int | None:
    if speed_kmh is None:
        return None
    thresholds = [1, 6, 12, 20, 29, 39, 50, 62, 75, 89, 103, 118, 1000]
    for i, threshold in enumerate(thresholds):
        if speed_kmh < threshold:
            return i
    return 12


def deg_to_cn(deg: float | None) -> str:
    if deg is None:
        return '--'
    dirs = ['北风', '东北风', '东风', '东南风', '南风', '西南风', '西风', '西北风']
    idx = int(((deg % 360) + 22.5) // 45) % 8
    return dirs[idx]


def format_wind(speed_kmh: float | None, direction=None, direction_type='deg') -> str:
    level = wind_level(speed_kmh)
    if level is None:
        return '--'
    if direction_type == 'cardinal':
        direction_text = DIR16_TO_CN.get(str(direction or '').upper(), '北风')
    else:
        direction_text = deg_to_cn(None if direction is None else float(direction))
    return f'{direction_text}{level}级'


def build_indices(weather: str, high_c: float | None, low_c: float | None, wind_kmh: float | None):
    delta = None if high_c is None or low_c is None else high_c - low_c
    wear_level = '舒适'
    wear_desc = '早晚有点凉，分层穿衣最稳。'
    if low_c is not None and low_c <= 0:
        wear_level = '偏冷'
        wear_desc = '早晚温度低，厚外套别省。'
    elif low_c is not None and low_c <= 6:
        wear_level = '微凉'
        wear_desc = '早晚加一层，白天再灵活减衣。'
    cold_level = '较低'
    cold_desc = '注意保暖补水，别被温差偷袭。'
    if delta is not None and delta >= 12:
        cold_level = '较高'
        cold_desc = '昼夜温差大，最容易着凉。'
    elif weather_bucket(weather) in {'rain', 'snow', 'fog'}:
        cold_level = '中等'
        cold_desc = '有降水或湿冷感，出门记得防风。'
    sport_level = '适宜'
    sport_desc = '空气和体感都还行，安排活动没问题。'
    if weather_bucket(weather) in {'rain', 'snow', 'storm'}:
        sport_level = '一般'
        sport_desc = '有降水，运动尽量改室内更稳。'
    elif wind_kmh is not None and wind_kmh >= 25:
        sport_level = '一般'
        sport_desc = '风有点大，户外活动别太猛。'
    uv_level = '弱'
    uv_desc = '常规通勤问题不大。'
    if '晴' in weather:
        uv_level = '中等'
        uv_desc = '中午日照更强，长时间户外注意防晒。'
    return {
        '穿衣指数': {'level': wear_level, 'desc': wear_desc},
        '感冒指数': {'level': cold_level, 'desc': cold_desc},
        '运动指数': {'level': sport_level, 'desc': sport_desc},
        '紫外线指数': {'level': uv_level, 'desc': uv_desc},
    }


def build_suggestion(weather: str, source_used: str, anomaly_reasons, hourly_cards=None):
    hourly_cards = hourly_cards or []
    rainy_soon = [x for x in hourly_cards if str(x.get('rain_prob', '0')).rstrip('%').isdigit() and int(str(x.get('rain_prob')).rstrip('%')) >= 40]
    if weather_bucket(weather) in {'rain', 'snow', 'storm'}:
        tip = '有降水迹象，路面可能湿滑，通勤优先防水防风，出门记得带伞。'
    elif rainy_soon:
        first_rain = rainy_soon[0].get('time', '')
        tip = f'{first_rain}后降水概率明显升高，出门最好随身带伞。'
    elif '晴' in weather:
        tip = '天气还不错，出门效率高，早晚注意温差。'
    else:
        tip = '整体还算平稳，按温差灵活增减衣物就行。'
    return tip


def get_lunar_text(dt: datetime) -> tuple[str, str]:
    lunar = LunarDate.fromSolarDate(dt.year, dt.month, dt.day)
    month_name = LUNAR_MONTHS[lunar.month - 1]
    if lunar.isLeapMonth:
        month_name = '闰' + month_name
    day_name = LUNAR_DAYS[lunar.day - 1]
    lunar_text = f'农历{month_name}{day_name}'
    festival = SOLAR_FESTIVALS.get((dt.month, dt.day)) or LUNAR_FESTIVALS.get((lunar.month, lunar.day)) or ''
    return lunar_text, festival


def format_hour_text(hour: int) -> str:
    return f'{hour}:00'



def summarize_precip_windows(hourly_precip_windows):
    if not hourly_precip_windows:
        return ''
    parts = []
    for item in hourly_precip_windows:
        label = item.get('label', '降水')
        start = item.get('start_hour')
        end = item.get('end_hour')
        max_prob = item.get('max_prob')
        if start is None or end is None:
            continue
        if end >= 24:
            time_text = f'{format_hour_text(start)}后'
        else:
            time_text = f'{format_hour_text(start)}-{format_hour_text(end)}'
        prob_text = f'，最高概率{max_prob}%' if isinstance(max_prob, int) and max_prob >= 0 else ''
        parts.append(f'{label}{time_text}{prob_text}')
    return '；'.join(parts)



def build_precip_timing_text(hourly_precip_windows, now_hour=None):
    hourly_precip_windows = hourly_precip_windows or []
    if not hourly_precip_windows:
        return ''
    now_hour = datetime.now().hour if now_hour is None else now_hour
    parts = []
    for item in hourly_precip_windows:
        label = item.get('label', '降水')
        start = item.get('start_hour')
        end = item.get('end_hour')
        max_prob = item.get('max_prob')
        if start is None or end is None:
            continue
        end_text = '午夜前后' if end >= 24 else format_hour_text(end)
        if end <= now_hour:
            text = f'{label}已过，主要在{format_hour_text(start)}-{end_text}'
        elif start <= now_hour < end:
            text = f'{label}正在持续，预计{end_text}前后逐渐停'
            if isinstance(max_prob, int) and max_prob >= 0:
                text += f'，最高概率{max_prob}%'
        else:
            text = f'{label}预计{format_hour_text(start)}开始，{end_text}前后逐渐停'
            if isinstance(max_prob, int) and max_prob >= 0:
                text += f'，最高概率{max_prob}%'
        parts.append(text)
    return '；'.join(parts)



def build_one_liner(date_text: str, lunar_text: str, festival: str, city: str, weather: str, temp: str, wind: str, source_note: str, suggestion: str, hourly_cards=None, future_rows=None, hourly_precip_windows=None):
    prefix = f'主人，今天是{date_text}，{lunar_text}'
    if festival:
        prefix += f'，也是{festival}'
    precip_note = ''
    hourly_cards = hourly_cards or []
    future_rows = future_rows or []
    hourly_precip_windows = hourly_precip_windows or []
    precip_windows_summary = summarize_precip_windows(hourly_precip_windows)
    precip_timing_text = build_precip_timing_text(hourly_precip_windows)
    rainy_soon = [x for x in hourly_cards if any(k in str(x.get('weather', '')) for k in ['雨', '雪']) or (str(x.get('rain_prob', '0')).rstrip('%').isdigit() and int(str(x.get('rain_prob')).rstrip('%')) >= 40)]
    if precip_timing_text:
        precip_note = f'，{precip_timing_text}'
    elif precip_windows_summary:
        labels = {item.get('label') for item in hourly_precip_windows if item.get('label')}
        if labels == {'降雨'}:
            title = '全天降雨时段'
        elif labels == {'降雪'}:
            title = '全天降雪时段'
        else:
            title = '全天降水时段'
        precip_note = f'，{title}：{precip_windows_summary}'
    elif rainy_soon:
        first = rainy_soon[0]
        prob = str(first.get('rain_prob', '--'))
        kind = '降雪' if '雪' in str(first.get('weather', '')) else '降雨'
        precip_note = f'，{first.get("time", "稍后")}起{kind}概率{prob}'
    elif any(any(k in str(x.get('weather', '')) for k in ['雨', '雪']) for x in future_rows):
        for row in future_rows:
            w = str(row.get('weather', ''))
            if '雨' in w or '雪' in w:
                kind = '降雪' if '雪' in w else '降雨'
                precip_note = f'，未来天气有{kind}过程'
                break
    weather_line = f'{city}今日{weather}，气温{temp}，{wind}{precip_note}。'
    text = clean_text(f'{prefix}。{weather_line}{suggestion}')
    return f'**{text}**'


def pick_tagline() -> str:
    return random.choice(TAGLINE_POOL)


def build_short_reminder(weather: str, high_c: float | None, low_c: float | None, wind_kmh: float | None, hourly_cards, future_rows, hourly_precip_windows=None):
    delta = None if high_c is None or low_c is None else high_c - low_c
    hourly_precip_windows = hourly_precip_windows or []
    if hourly_precip_windows:
        first = hourly_precip_windows[0]
        label = first.get('label', '雨雪')
        start = first.get('start_hour')
        end = first.get('end_hour')
        if start is not None and end is not None:
            if end >= 24:
                return f'今天{label}{format_hour_text(start)}后更明显。'
            return f'今天{label}{format_hour_text(start)}开始，{format_hour_text(end)}前后停。'
    if weather_bucket(weather) in {'rain', 'snow', 'storm'}:
        return '出门带伞，鞋子尽量防滑。'
    if delta is not None and delta >= 12:
        return '早晚偏凉，外套先别收。'
    if wind_kmh is not None and wind_kmh >= 25:
        return '今天风偏大，骑车注意侧风。'
    if '晴' in weather and high_c is not None and high_c >= 26:
        return '中午偏晒，外出注意防晒补水。'
    rainy_hours = [x.get('time') for x in (hourly_cards or []) if str(x.get('rain_prob', '0')).rstrip('%').isdigit() and int(str(x.get('rain_prob')).rstrip('%')) >= 40]
    if rainy_hours:
        return f'{rainy_hours[0]}后降水概率升高，早点出门更稳。'
    if future_rows:
        tomorrow = future_rows[0]
        t_weather = str(tomorrow.get('weather', ''))
        if any(x in t_weather for x in ['雨', '雪']):
            return f'明天{t_weather}，随身雨具可先备上。'
    return '通勤按常规安排，留意早晚温差。'


def build_precip_windows(hourly_times, hourly_weather_codes, hourly_precip_probs):
    today = datetime.now().date()
    windows = []
    current = None
    for idx, slot in enumerate(hourly_times):
        try:
            slot_dt = datetime.fromisoformat(slot)
        except Exception:
            continue
        if slot_dt.date() != today:
            continue
        weather = open_meteo_desc(hourly_weather_codes[idx])
        prob = int(round(float(hourly_precip_probs[idx])))
        is_snow = '雪' in weather
        is_rain = ('雨' in weather or '毛毛' in weather) and not is_snow
        if not (is_rain or is_snow):
            if current:
                current['end_hour'] = slot_dt.hour
                windows.append(current)
                current = None
            continue
        label = '降雪' if is_snow else '降雨'
        if current and current['label'] == label and slot_dt.hour <= current['end_hour'] + 1:
            current['end_hour'] = slot_dt.hour + 1
            current['max_prob'] = max(current['max_prob'], prob)
        else:
            if current:
                windows.append(current)
            current = {
                'label': label,
                'start_hour': slot_dt.hour,
                'end_hour': slot_dt.hour + 1,
                'max_prob': prob,
            }
    if current:
        windows.append(current)
    return windows



def fetch_open_meteo():
    geo = fetch_json(OPEN_METEO_GEOCODE)
    pick = (geo.get('results') or [None])[0]
    if not pick:
        raise RuntimeError('Open-Meteo geocoding missing')
    lat, lon = pick['latitude'], pick['longitude']
    url = 'https://api.open-meteo.com/v1/forecast?' + urllib.parse.urlencode({
        'latitude': lat,
        'longitude': lon,
        'current': 'temperature_2m,relative_humidity_2m,apparent_temperature,precipitation,weather_code,wind_speed_10m,wind_direction_10m',
        'hourly': 'temperature_2m,precipitation_probability,weather_code,wind_speed_10m,wind_direction_10m',
        'daily': 'weather_code,temperature_2m_max,temperature_2m_min,precipitation_probability_max,precipitation_sum',
        'timezone': TARGET_TZ,
        'forecast_days': 4,
    })
    data = fetch_json(url)
    daily = data['daily']
    future = []
    for i in range(1, min(len(daily['time']), 5)):
        future.append({
            'day': daily['time'][i][5:],
            'weather': open_meteo_desc(daily['weather_code'][i]),
            'temp': f"{celsius_text(daily['temperature_2m_max'][i])}/{celsius_text(daily['temperature_2m_min'][i])}",
            'wind': '--'
        })
    hourly = data['hourly']
    hourly_cards = []
    now_local = datetime.now()
    current_hour = now_local.replace(minute=0, second=0, microsecond=0)
    hourly_times = hourly['time']
    for idx, slot in enumerate(hourly_times):
        try:
            slot_dt = datetime.fromisoformat(slot)
        except Exception:
            continue
        if slot_dt < current_hour:
            continue
        hourly_cards.append({
            'time': f'{slot_dt.hour}:00',
            'temp': celsius_text(hourly['temperature_2m'][idx]),
            'weather': open_meteo_desc(hourly['weather_code'][idx]),
            'rain_prob': f'{int(round(float(hourly["precipitation_probability"][idx])))}%',
            'wind': format_wind(float(hourly['wind_speed_10m'][idx]), float(hourly['wind_direction_10m'][idx]), 'deg')
        })
        if len(hourly_cards) >= 4:
            break
    current = data['current']
    precip_windows = build_precip_windows(hourly['time'], hourly['weather_code'], hourly['precipitation_probability'])
    return {
        'source': 'open-meteo',
        'location': {'name': pick.get('name', '枣庄市'), 'latitude': lat, 'longitude': lon},
        'weather': open_meteo_desc(current.get('weather_code')),
        'temp': f"{celsius_text(daily['temperature_2m_max'][0])}/{celsius_text(daily['temperature_2m_min'][0])}",
        'wind': format_wind(float(current.get('wind_speed_10m')), float(current.get('wind_direction_10m')), 'deg'),
        'wind_speed_kmh': float(current.get('wind_speed_10m')),
        'wind_direction': float(current.get('wind_direction_10m')),
        'humidity': current.get('relative_humidity_2m'),
        'current_temp_c': float(current.get('temperature_2m')),
        'high_c': float(daily['temperature_2m_max'][0]),
        'low_c': float(daily['temperature_2m_min'][0]),
        'future': future,
        'hourly_cards': hourly_cards,
        'hourly_precip_windows': precip_windows,
        'raw': data,
    }


def fetch_wttr():
    wttr_url = 'https://wttr.in/' + urllib.parse.quote(WTTR_QUERY) + '?format=j1'
    data = fetch_json(wttr_url, headers={'User-Agent': 'curl/8.0'})
    current = data['current_condition'][0]
    nearest = data['nearest_area'][0]
    weather_days = data.get('weather', [])
    today = weather_days[0]
    future = []
    for item in weather_days[1:4]:
        hourly_list = item.get('hourly', [{}])
        probe = hourly_list[4] if len(hourly_list) > 4 else hourly_list[0]
        future.append({
            'day': item.get('date', '--')[5:],
            'weather': wttr_desc(probe),
            'temp': f"{celsius_text(item.get('maxtempC'))}/{celsius_text(item.get('mintempC'))}",
            'wind': '--'
        })
    lat = float(nearest['latitude'])
    lon = float(nearest['longitude'])
    wind_speed = float(current.get('windspeedKmph'))
    return {
        'source': 'wttr.in',
        'query': WTTR_QUERY,
        'location': {
            'name': nearest['areaName'][0]['value'], 'region': nearest['region'][0]['value'], 'country': nearest['country'][0]['value'],
            'latitude': lat, 'longitude': lon,
        },
        'weather': wttr_desc(current),
        'temp': f"{celsius_text(today.get('maxtempC'))}/{celsius_text(today.get('mintempC'))}",
        'wind': format_wind(wind_speed, current.get('winddir16Point'), 'cardinal'),
        'wind_speed_kmh': wind_speed,
        'wind_direction': current.get('winddir16Point'),
        'humidity': int(current.get('humidity')) if str(current.get('humidity', '')).isdigit() else current.get('humidity'),
        'current_temp_c': float(current.get('temp_C')),
        'high_c': float(today.get('maxtempC')),
        'low_c': float(today.get('mintempC')),
        'future': future,
        'raw': data,
    }


def choose_source(primary, secondary):
    reasons = []
    loc = primary['location']
    distance = haversine_km(loc['latitude'], loc['longitude'], TARGET_LAT, TARGET_LON)
    if distance > 25:
        reasons.append(f'{primary["source"]} 定位偏离目标城市约 {distance:.1f}km')
    if primary['high_c'] < primary['low_c']:
        reasons.append(f'{primary["source"]} 最高温低于最低温')
    if primary.get('current_temp_c') is not None and secondary.get('current_temp_c') is not None and abs(primary['current_temp_c'] - secondary['current_temp_c']) > 6:
        reasons.append(f'双源当前温差 {abs(primary["current_temp_c"] - secondary["current_temp_c"]):.1f}℃')
    if abs(primary['high_c'] - secondary['high_c']) > 6:
        reasons.append(f'双源最高温差 {abs(primary["high_c"] - secondary["high_c"]):.1f}℃')
    if weather_bucket(primary['weather']) != weather_bucket(secondary['weather']) and primary.get('current_temp_c') is not None and secondary.get('current_temp_c') is not None and abs(primary['current_temp_c'] - secondary['current_temp_c']) >= 4:
        reasons.append(f'天气类型不一致：{primary["source"]}={primary["weather"]} / Open-Meteo={secondary["weather"]}')
    if primary['weather'] == '--' or primary['temp'] == '--':
        reasons.append(f'{primary["source"]} 字段缺失')
    return (primary if not reasons else secondary), reasons


def main():
    now = datetime.now()
    date_text = f"{now.month}月{now.day}日 周{weekday_map[now.weekday()]}"
    lunar_text, festival = get_lunar_text(now)
    wttr_error = None
    wttr = None
    open_meteo = fetch_open_meteo()
    try:
        wttr = fetch_wttr()
    except Exception as exc:
        wttr_error = f'{type(exc).__name__}: {exc}'
        wttr = {
            'source': 'wttr.in',
            'query': WTTR_QUERY,
            'location': {
                'name': WTTR_QUERY, 'region': '--', 'country': '--',
                'latitude': TARGET_LAT, 'longitude': TARGET_LON,
            },
            'weather': '--',
            'temp': '--',
            'wind': '--',
            'wind_speed_kmh': None,
            'wind_direction': None,
            'humidity': None,
            'current_temp_c': None,
            'high_c': open_meteo['high_c'],
            'low_c': open_meteo['low_c'],
            'future': [],
            'raw': {'error': wttr_error},
        }
    chosen, anomaly_reasons = choose_source(wttr, open_meteo)
    if wttr_error:
        anomaly_reasons = [f'wttr.in 请求失败: {wttr_error}'] + anomaly_reasons
    source_note = f'主源 wttr.in/{WTTR_QUERY} · Open-Meteo 校验'
    ref = source_note if chosen['source'] == 'wttr.in' and not wttr_error else f'wttr.in/{WTTR_QUERY} 异常 · 已切换 Open-Meteo'
    suggestion = build_suggestion(chosen['weather'], chosen['source'], anomaly_reasons, open_meteo['hourly_cards'])
    indices = build_indices(chosen['weather'], chosen['high_c'], chosen['low_c'], chosen.get('wind_speed_kmh'))
    future_rows = list(chosen['future'][:3])
    if len(future_rows) < 3:
        existing_days = {x.get('day') for x in future_rows}
        for item in open_meteo['future']:
            if item.get('day') in existing_days:
                continue
            future_rows.append(item)
            existing_days.add(item.get('day'))
            if len(future_rows) >= 3:
                break
    one_liner = build_one_liner(date_text, lunar_text, festival, TARGET_CITY, chosen['weather'], chosen['temp'], chosen['wind'], source_note if chosen['source'] == 'wttr.in' else ref, suggestion, open_meteo['hourly_cards'], future_rows, open_meteo.get('hourly_precip_windows'))
    short_desc = build_short_reminder(chosen['weather'], chosen['high_c'], chosen['low_c'], chosen.get('wind_speed_kmh'), open_meteo['hourly_cards'], future_rows, open_meteo.get('hourly_precip_windows'))
    if len(short_desc) > 24:
        short_desc = short_desc[:24].rstrip('，。；; ') + '…'
    payload = {
        'date': date_text,
        'city': TARGET_CITY,
        'lunar': lunar_text,
        'festival': festival,
        'ref': ref,
        'weather': chosen['weather'],
        'temp': chosen['temp'],
        'wind': chosen['wind'],
        'indices': indices,
        'hourly_cards': open_meteo['hourly_cards'],
        'hourly_precip_windows': open_meteo.get('hourly_precip_windows', []),
        'future': future_rows,
        'suggestion': suggestion,
        'one_liner': one_liner,
        'tagline': pick_tagline(),
        'short_label': chosen['weather'],
        'short_desc': short_desc,
        'html': str(HTML),
        'png': str(PNG),
        'source_used': chosen['source'],
        'source_note': source_note,
        'anomaly_reasons': anomaly_reasons,
        'wttr': {'weather': wttr['weather'], 'temp': wttr['temp'], 'wind': wttr['wind'], 'location': wttr['location'], 'error': wttr_error},
        'open_meteo': {'weather': open_meteo['weather'], 'temp': open_meteo['temp'], 'wind': open_meteo['wind'], 'location': open_meteo['location']}
    }
    META.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding='utf-8')
    TEXT.write_text(one_liner, encoding='utf-8')
    RAW.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding='utf-8')
    print(HTML)
    print(PNG)
    print(TEXT)
    print(one_liner)


if __name__ == '__main__':
    main()
