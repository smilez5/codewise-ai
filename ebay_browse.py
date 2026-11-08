import base64, json, os, urllib.parse, urllib.request
from datetime import date
from pathlib import Path

API = 'https://api.ebay.com'

def request(url, headers, data=None):
    req = urllib.request.Request(url, headers=headers, data=data)
    with urllib.request.urlopen(req, timeout=30) as res:
        return json.load(res)

def main():
    cid, secret = os.environ['EBAY_CLIENT_ID'], os.environ['EBAY_CLIENT_SECRET']
    basic = base64.b64encode(f'{cid}:{secret}'.encode()).decode()
    token = request(API+'/identity/v1/oauth2/token', {'Authorization':'Basic '+basic,'Content-Type':'application/x-www-form-urlencoded'}, urllib.parse.urlencode({'grant_type':'client_credentials','scope':'https://api.ebay.com/oauth/api_scope'}).encode())['access_token']
    queries = ['headphones','home improvement','clothing','electronics']
    offers=[]
    for query in queries:
        params=urllib.parse.urlencode({'q':query,'limit':50,'filter':'buyingOptions:{FIXED_PRICE}'})
        data=request(API+'/buy/browse/v1/item_summary/search?'+params, {'Authorization':'Bearer '+token,'X-EBAY-C-MARKETPLACE-ID':'EBAY_US'})
        for item in data.get('itemSummaries',[]):
            price=item.get('price') or {}; original=item.get('marketingPrice',{}).get('originalPrice') or {}
            try: now=float(price['value']); before=float(original['value'])
            except (KeyError,TypeError,ValueError): continue
            if before<=now or price.get('currency')!='USD' or original.get('currency')!='USD': continue
            link=item.get('itemWebUrl','')
            if not link.startswith('https://'): continue
            title=item.get('title','eBay item')
            pct=round((before-now)/before*100)
            offers.append({'id':'ebay-'+item['itemId'],'merchant':'eBay','category':'shopping','offer':f'{pct}% below listed original price','code':'','min':0,'terms':f'{title}. Listed price ${now:.2f}; original price ${before:.2f}. Prices and availability can change. Verify on eBay.','sourceUrl':link,'reviewed':date.today().isoformat(),'status':'published'})
    unique=list({x['id']:x for x in offers}.values())[:150]
    path=Path('data/approved-offers.json');path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps({'schema':'codewise-offers-v1','offers':unique},indent=2)+'\n')
    print(f'Published {len(unique)} listings with original-price comparisons')

if __name__=='__main__': main()
