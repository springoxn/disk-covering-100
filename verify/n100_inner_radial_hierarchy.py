"""Parameterized Voronoi inner-target center-count bounds and box screening."""
from pathlib import Path
from fractions import Fraction as F
from math import factorial
import json,hashlib
from n100_recursive_inner_envelope import root,need,ROOT

def main():
 U=F(1154469548855829,10**16);pl=F(314159,100000);ph=F(314160,100000);f6=(F(3,2)*root(F(3))[0],F(3,2)*root(F(3))[1]);f5=(F(5,8)*root(10+2*root(F(5))[0])[0],F(5,8)*root(10+2*root(F(5))[1])[1]);cuts=[]
 for s in [F(2,5),F(1,2),F(3,5),F(7,10),1-2*U]:
  t=U/s;coef=F(1);angle=F(0)
  for j in range(20):
   angle+=coef*t**(2*j+1);coef*=F((2*j+1)**2,2*(j+1)*(2*j+3))
  angle+=coef*t**41/(1-t*t);T=F(angle.numerator*10**6//angle.denominator+1,10**6);B=(pl/T).numerator//(pl/T).denominator+1;need((B-1)*T<pl and 0<t<T<F(1,3),'angle domain');H=sum((F((-1)**j,factorial(2*j+1))*(2*T)**(2*j) for j in range(8)),F(0));excluded=[]
  for n in range(1,101):
   c=n-6-B;G=c*f6[1 if c>=0 else 0]+(6+B)*f5[1];margin=pl*H-t*t*G
   if margin>0:excluded.append((n,margin,G))
  n,margin,G=excluded[-1];cuts.append({'target_radius':str(s),'center_norm_strict_upper':str(s+U),'normalized_radius':str(t),'angle_upper':str(T),'boundary_arcs_lower':B,'excluded_disk_count_upper':n,'minimum_centers':n+1,'sinc_lower':str(H),'G_upper':str(G),'strict_margin':str(margin)})
 source=ROOT/'verify/out/n100-spatial-leaf-joint.json';joint=json.loads(source.read_text(encoding='utf-8'));arc=json.loads((ROOT/'verify/out/n100-arc-center-projection.json').read_text(encoding='utf-8'));candidate=next(c for c in arc['cases'] if c['source_node'] is None);cases=[('candidate',candidate['result']['boxes'])]+[(str(c['tree_node']),c['arc_result']['boxes']) for c in joint['leaves'] if not c['excluded']];rows=[]
 for name,boxes in cases:
  norms=[]
  for box in boxes[:100]:
   mins=[];maxs=[]
   for j in (0,2):
    a,b=F(box[j],2**20),F(box[j+1],2**20);mins.append(F(0) if a<=0<=b else min(a*a,b*b));maxs.append(max(a*a,b*b))
   norms.append((sum(mins),sum(maxs)))
  counts=[]
  for cut in cuts:
   R2=F(cut['center_norm_strict_upper'])**2;possible=[i for i,(a,b) in enumerate(norms) if a<R2];certain=[i for i,(a,b) in enumerate(norms) if b<R2];counts.append({'possible_centers':possible,'certain_centers':certain,'excluded':len(possible)<cut['minimum_centers']})
  rows.append({'case':name,'cuts':counts,'excluded':any(c['excluded'] for c in counts)})
 need(not rows[0]['excluded'],'candidate retained');out=ROOT/'verify/out/n100-inner-radial-hierarchy.json';need(not out.exists(),'overwrite');out.write_text(json.dumps({'schema':'n100-inner-radial-hierarchy/v1','radius_upper':str(U),'pi_bracket':[str(pl),str(ph)],'f6_interval':list(map(str,f6)),'f5_interval':list(map(str,f5)),'cuts':cuts,'box_rows':rows,'excluded_box_count':sum(r['excluded'] for r in rows),'analytic_dependencies':['disks with center norm>=s+U do not enter open target disk of radius s','remaining disks cover target closure; use generic normalized Voronoi polygon envelope','monotone sinc and positive arcsin series tail bound','strict open radial ball center-count necessary condition'],'scope':'five concentric target radii, safe cardinality screening of 33 saved center-box domains; no total count-family update beyond stage101','global_optimality':False,'input_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()},indent=2)+'\n',encoding='utf-8');print('PASS inner radial hierarchy',[(c['target_radius'],c['minimum_centers']) for c in cuts],'excluded boxes',sum(r['excluded'] for r in rows))
if __name__=='__main__':main()
