import requests,re,html
from urllib.parse import quote
proxy='http://192.168.50.2:5898'
proxies={'http':proxy,'https':proxy}
headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0 Safari/537.36'}
queries=['苹果 iPhone 15','Apple iPhone 15','iPhone 15 手机','iPhone15 Pro 手机']
noise_words=['换外屏','换内屏','后玻璃','听筒','扬声器','声音异常','数据线','充电头','充电器','钢化膜','手机壳','维修','到店修','非原厂','配件','外屏碎','内屏碎','碎','玻璃','苏宁服务','门店服务']
phone_words=['手机','iPhone15','iPhone 15','苹果']
def parse_price(block):
    txt=' '.join(block.split())
    m=re.search(r'¥\s*([0-9]+(?:\.[0-9]{2})?)',txt)
    if m:
        return m.group(1)
    m=re.search(r'<span class="price">.*?<span[^>]*>([0-9]+)</span>\s*<span[^>]*>\.([0-9]{2})</span>',block,re.S)
    if m:
        return m.group(1)+'.'+m.group(2)
    return ''
for q in queries:
    url=f'https://search.suning.com/{quote(q)}/'
    r=requests.get(url,headers=headers,proxies=proxies,timeout=25)
    text=r.text
    print('\n===== QUERY',q,'FINAL',r.url,'LEN',len(text))
    blocks=re.findall(r'(<li docType="1".*?</li>)', text, re.S)
    rows=[]
    for block in blocks:
        hm=re.search(r'href="(//product\.suning\.com/[^"]+)"',block)
        tm=re.search(r'<img[^>]*alt="([^"]+)"',block)
        if not hm or not tm:
            continue
        title=html.unescape(tm.group(1)).strip()
        url='https:'+hm.group(1)
        price=parse_price(block)
        title_l=title.lower()
        noise=any(w.lower() in title_l for w in noise_words)
        phone_like=any(w.lower() in title_l for w in phone_words)
        rows.append((title,price,url,noise,phone_like))
    print('rows',len(rows))
    kept=[]
    for title,price,url,noise,phone_like in rows:
        if phone_like and not noise:
            kept.append((title,price,url))
    if kept:
        for title,price,url in kept[:10]:
            print('KEEP|'+price+'|'+title+'|'+url)
    else:
        print('NO_CLEAN_RESULTS')
        for title,price,url,noise,phone_like in rows[:10]:
            print(('RAWPHONE' if phone_like else 'RAW')+'|'+price+'|'+title+'|'+url)
