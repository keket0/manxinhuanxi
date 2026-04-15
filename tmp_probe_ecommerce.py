import requests,re,html
from urllib.parse import quote
proxy='http://192.168.50.2:5898'
proxies={'http':proxy,'https':proxy}
headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0 Safari/537.36'}
cases={
 'suning':f'https://search.suning.com/{quote("iPhone 15")}/',
 'pdd':f'https://mobile.yangkeduo.com/search_result.html?search_key={quote("iPhone 15")}',
 'vip':f'https://category.vip.com/suggest.php?keyword={quote("iPhone 15")}',
}
url_re=re.compile(r"https?://[^\"'\\s<>]+")
for name,url in cases.items():
    r=requests.get(url,headers=headers,proxies=proxies,timeout=25)
    text=r.text
    print(f'\n===== {name} len={len(text)} final={r.url}')
    pats=[
        r'window\.__INITIAL_STATE__\s*=\s*(\{.*?\})\s*;',
        r'window\.__NEXT_DATA__\s*=\s*(\{.*?\})\s*;',
        r'__NEXT_DATA__"[^>]*>(\{.*?\})</script>',
        r'window\.__PRELOADED_STATE__\s*=\s*(\{.*?\})\s*;',
        r'sn\.pageConfig\s*=\s*(\{.*?\})\s*;',
        r'searchData\s*=\s*(\{.*?\})\s*;',
    ]
    hit=False
    for p in pats:
        m=re.search(p,text,re.S)
        if m:
            print('json_hit',p[:35],'size',len(m.group(1)))
            print(m.group(1)[:1200])
            hit=True
            break
    if not hit:
        print('json_hit none')
    for needle in ['commodityInfo','productCode','saleInfo','item_price','goods_id','goodsName','productName','sellingPoint','pcItemInfo','price','title']:
        c=text.count(needle)
        if c:
            print('count',needle,c)
    seen=0
    for m in url_re.finditer(text):
        u=html.unescape(m.group(0))
        if name=='suning' and ('product.suning.com' in u or 'shop.suning.com' in u):
            print('url',u[:240]); seen+=1
        elif name=='pdd' and ('mobile.yangkeduo.com/goods' in u or 'yangkeduo.com/goods' in u):
            print('url',u[:240]); seen+=1
        elif name=='vip' and ('detail.vip.com/detail-' in u or 'category.vip.com/s' in u):
            print('url',u[:240]); seen+=1
        if seen>=5:
            break
