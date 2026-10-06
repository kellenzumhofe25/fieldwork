from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
from pathlib import Path
import json, os, threading

PORT = int(os.environ.get('PORT', '4173'))
ROOT = Path(__file__).resolve().parent
DATA = ROOT / 'collection.json'
LOCK = threading.Lock()
SEED = [
 dict(id='sample-1',name='Forest home shirt',team='Woodland FC',type='Soccer',color='Green',year=1996,size='M',condition='Excellent',number='9',notes='A classic forest-green home shirt with white details.',sample=True,photo='',tile=0),
 dict(id='sample-2',name='Sunday pinstripes',team='Riverside Club',type='Baseball',color='Cream',year=2003,size='L',condition='Good',number='',notes='Cream pinstripes and a timeless blue trim.',sample=True,photo='',tile=1),
 dict(id='sample-3',name='Sky blue away shirt',team='Coastal United',type='Soccer',color='Blue',year=2010,size='M',condition='Excellent',number='10',notes='A light blue away shirt inspired by the coast.',sample=True,photo='',tile=2),
 dict(id='sample-4',name='The rust court jersey',team='Canyon Basketball',type='Basketball',color='Red',year=1998,size='L',condition='Good',number='23',notes='Warm rust red, contrasting white trim.',sample=True,photo='',tile=3),
 dict(id='sample-5',name='Navy game-day classic',team='Northfield Football',type='Football',color='Navy',year=1988,size='XL',condition='Worn',number='12',notes='A navy-and-cream piece with vintage character.',sample=True,photo='',tile=4),
 dict(id='sample-6',name='Meadow training shirt',team='Meadow Athletic',type='Soccer',color='Yellow',year=2022,size='S',condition='Like new',number='',notes='Soft yellow with green trim.',sample=True,photo='',tile=5),
]
class Handler(SimpleHTTPRequestHandler):
 def __init__(self,*args,**kwargs): super().__init__(*args,directory=str(ROOT/'dist'),**kwargs)
 def reply(self,status,data):
  raw=json.dumps(data).encode(); self.send_response(status); self.send_header('Content-Type','application/json'); self.send_header('Cache-Control','no-store'); self.send_header('Content-Length',str(len(raw))); self.end_headers(); self.wfile.write(raw)
 def do_GET(self):
  if self.path=='/api/collection':
   try:
    with LOCK: records=json.loads(DATA.read_text()) if DATA.exists() else SEED
    self.reply(200,records)
   except Exception: self.reply(500,{'error':'Could not read the collection. Your saved file has been preserved.'})
  else: super().do_GET()
 def do_POST(self):
  if self.path!='/api/collection': return self.reply(404,{'error':'Not found'})
  if self.headers.get('Origin') not in (None,f'http://127.0.0.1:{PORT}',f'http://localhost:{PORT}'): return self.reply(403,{'error':'Origin not allowed'})
  try:
   length=int(self.headers.get('Content-Length','0'))
   if length>30_000_000: return self.reply(413,{'error':'Collection is too large. Try smaller photos.'})
   records=json.loads(self.rfile.read(length))
   if not isinstance(records,list) or len(records)>3000: raise ValueError('Invalid collection')
   ids=set()
   for item in records:
    if not isinstance(item,dict) or not isinstance(item.get('id'),str) or not item.get('name') or item['id'] in ids: raise ValueError('Each jersey needs a unique ID and name.')
    ids.add(item['id'])
    if not isinstance(item.get('year'),int) or not 1900<=item['year']<=2100: raise ValueError('Invalid jersey year.')
    for key in ['name','team','type','color','size','condition','number','notes','photo']:
     if not isinstance(item.get(key,''),str): raise ValueError('Invalid jersey details.')
    photo=item.get('photo','')
    if photo and not photo.startswith(('data:image/jpeg;base64,','data:image/png;base64,','data:image/webp;base64,')): raise ValueError('Invalid photo format.')
   with LOCK:
    temporary=DATA.with_suffix('.tmp'); temporary.write_text(json.dumps(records,indent=2)); os.replace(temporary,DATA)
   self.reply(200,{'ok':True})
  except (ValueError,TypeError,json.JSONDecodeError) as e: self.reply(400,{'error':str(e)})
  except Exception: self.reply(500,{'error':'Could not save. Keep this page open and try again.'})
if __name__=='__main__':
 print(f'Jersey portfolio: http://127.0.0.1:{PORT}',flush=True)
 ThreadingHTTPServer(('127.0.0.1',PORT),Handler).serve_forever()
