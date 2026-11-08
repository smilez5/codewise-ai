import json, os, urllib.parse, urllib.request, base64, datetime, pathlib
ROOT=pathlib.Path(__file__).parent
OUT=ROOT/'approved-offers.json'
now=datetime.datetime.now(datetime.timezone.utc)
client=os.getenv('EBAY_CLIENT_ID',''); secret=os.getenv('EBAY_CLIENT_SECRET','')
if not client or not secret:
    raise SystemExit('Missing eBay API credentials; existing offers preserved.')
def request(url,headers=None,data=None):
    req=urllib.request.Request(url,headers=headers or {},data=data)
    with urllib.request.urlopen(req,timeout=25) as r:return json.load(r)
auth=base64.b64encode(f'{client}:{secret}'.encode()).decode()
token=request('https://api.ebay.com/identity/v1/oauth2/token',{'Authorization':'Basic '+auth,'Content-Type':'application/x-www-form-urlencoded'},b'grant_type=client_credentials&scope=https%3A%2F%2Fapi.ebay.com%2Foauth%2Fapi_scope')['access_token']
queries=['headphones','home improvement','kitchen appliances']
items=[]; seen=set()
for q in queries:
    url='https://api.ebay.com/buy/browse/v1/item_summary/search?'+urllib.parse.urlencode({'q':q,'limit':20,'filter':'buyingOptions:{FIXED_PRICE}'})
    data=request(url,{'Authorization':'Bearer '+token,'X-EBAY-C-MARKETPLACE-ID':'EBAY_US'})
    for x in data.get('itemSummaries',[]):
        ident=x.get('itemId'); price=x.get('price',{}); link=x.get('itemWebUrl')
        if not ident or ident in seen or not link or not price.get('value') or price.get('currency')!='USD':continue
        seen.add(ident)
        items.append({'id':ident,'title':x.get('title','Item'),'price':price['value'],'currency':'USD','url':link,'image':x.get('image',{}).get('imageUrl'),'source':'eBay','category':q})
if not items:raise SystemExit('No valid offers returned; existing data preserved.')
payload={'version':'0.6','updated_at':now.isoformat(),'source':'eBay Browse API','offers':items[:45]}
tmp=OUT.with_suffix('.tmp');tmp.write_text(json.dumps(payload,indent=2)+'\n');tmp.replace(OUT)
print(f'Published {len(payload["offers"])} listings')
