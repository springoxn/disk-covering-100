"""Floating discovery only: proposed long-boundary-chord area penalty."""
import json,hashlib,math
from pathlib import Path
from scipy.optimize import brentq
ROOT=Path(__file__).resolve().parents[1]
def model(r):
 bmin=math.ceil(math.pi/math.asin(r))
 options=[]
 for b in range(bmin,595):
  edge=594-b
  if edge<2*b:continue
  g=2*math.pi/b
  ratio=math.sin(g/2)/r
  theta=2*math.asin(min(1,ratio))
  penalty=max(theta-math.pi/3,0)**2
  coeff=(edge*(math.sqrt(3)/2-math.pi/6)+100*math.pi)/2-b*penalty/8
  options.append((coeff,b))
 top=max(options)
 low=math.pi*math.sin(2*math.asin(r))/(2*math.asin(r))
 return low-r*r*top[0],top[1],top[0]
def main():
 samples=[{'r':r,'residual':model(r)[0],'maximizing_B':model(r)[1],'coefficient':model(r)[2]} for r in (.1111720153,.112,.113,.114,.115,.116)]
 root=brentq(lambda r:model(r)[0],.11,.12)
 out=ROOT/'runtime/n100-long-chord-model-discovery.json'
 if out.exists():raise FileExistsError(out)
 obj={'schema':'n100-long-chord-model-discovery/v1','discovery_only':True,
 'samples':samples,'root_discovery':root,'maximizing_B_at_root':model(root)[1],
 'geometry_proved':False,'universal_lower_bound_accepted':False,
 'unresolved':['long-chord angle lower bound restricted l>=r','uniform quadratic sine bound','multi-arc Jensen','degenerate cells and nominal padding','exact arithmetic'],
 'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
 out.write_text(json.dumps(obj,indent=2)+'\n',encoding='utf-8')
 print('DISCOVERY proposed chord penalty root',root,'B',model(root)[1]);print(samples)
if __name__=='__main__':main()
