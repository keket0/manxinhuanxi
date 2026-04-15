import requests,re,html
from urllib.parse import quote
proxy='http://192.168.50.2:5898'
proxies={'http':proxy,'https':proxy}
headers={'User-Agent':'Mozilla/5.0'}
url='https://search.dangdang.com/?key='+quote('iPhone 15')+'&act=input'
text=requests.get(url,headers=headers,proxies=proxies,timeout=25).text
items=[]
for m in re.finditer(r'<li[^>]*class="line\d+"[^>]*id="(\d+)"[^>]*>.*?<p class="price"[^>]*>\s*<span class="price_n">&yen;([0-9\.]+)</span>.*?<p class="name"[^>]*>\s*<a[^>]*href="([^"]+)"[^>]*>(.*?)</a>', text, re.S):
    pid, price, href, raw_title = m.groups()
    title=re.sub(r'<[^>]+>','',raw_title)
    title=html.unescape(title).strip()
    url='https:'+href if href.startswith('//') else href
    items.append((pid,price,title,url))
print('items',len(items))
noise=['手机壳','保护套','钢化膜','数据线','充电器','壳','贴膜','耳机','镜头膜','背盖']
kept=[]
for pid,price,title,url in items:
    if not any(n in title for n in noise):
        kept.append((pid,price,title,url))
for row in kept[:20]:
    print('KEEP|'+'|'.join(row))
if not kept:
    print('NO_CLEAN_RESULTS')
    for row in items[:20]:
        print('RAW|'+'|'.join(row))
