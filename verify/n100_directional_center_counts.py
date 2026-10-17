"""Directional target-disk count cuts on all 4200 inherited placement boxes."""
from pathlib import Path
from fractions import Fraction as F
import json,hashlib
ROOT=Path(__file__).resolve().parents[1]
def need(c,m):
 if not c:raise ValueError(m)
def main():
 cp=ROOT/'verify/out/n100-inner-radial-hierarchy.json';hier=json.loads(cp.read_text(encoding='utf-8'));U=F(hier['radius_upper']);queries=[];Q=2**20;D=100
 for cut,rho in zip(hier['cuts'],[F(3,5),F(1,2),F(2,5),F(3,10),F(1,5)]):
  s=F(cut['target_radius']);need(rho+s<=1,'target contained');directions=[(F(1),F(0)),(F(3,5),F(4,5)),(F(4,5),F(3,5)),(F(0),F(1))]
  points=set((sx*x*rho,sy*y*rho) for x,y in directions for sx in (-1,1) for sy in (-1,1))
  for x,y in sorted(points):
   need(x*x+y*y==rho*rho and (x*D).denominator==(y*D).denominator==1,'rational target center');queries.append({'target_radius':str(s),'target_center':[str(x),str(y)],'region_radius':str(s+U),'required':cut['minimum_centers']})
 dompath=ROOT/'verify/out/n100-boundary-circle-survivor-domain.json';domain=json.loads(dompath.read_text(encoding='utf-8'));keys=set(map(tuple,domain['survivor_axis_edge_placements']));roots=json.loads((ROOT/'verify/out/n100-axis-coupled-boxes.json').read_text(encoding='utf-8'))['retained'];cases=[{'id':r['placement'],'boxes':r['boxes']} for r in roots if tuple(r['placement']) in keys];need(len(cases)==4200,'full survivor placement domain');joint=json.loads((ROOT/'verify/out/n100-spatial-leaf-joint.json').read_text(encoding='utf-8'));extra=[{'id':str(r['tree_node']),'boxes':r['arc_result']['boxes']} for r in joint['leaves'] if not r['excluded']];candidate=next(c for c in json.loads((ROOT/'verify/out/n100-arc-center-projection.json').read_text(encoding='utf-8'))['cases'] if c['source_node'] is None);extra.append({'id':'candidate','boxes':candidate['result']['boxes']});prepared=[]
 for q in queries:
  x,y=map(F,q['target_center']);X=int(x*D*Q);Y=int(y*D*Q);threshold=F(q['region_radius'])**2*(D*Q)**2;prepared.append((X,Y,threshold.numerator,threshold.denominator))
 results=[];minimum=[100]*len(queries)
 for case in cases+extra:
  counts=[];scaled=[tuple(v*D for v in b) for b in case['boxes'][:100]]
  for qi,(X,Y,A,B) in enumerate(prepared):
   count=0
   for x0,x1,y0,y1 in scaled:
    dx=x0-X if X<x0 else X-x1 if X>x1 else 0;dy=y0-Y if Y<y0 else Y-y1 if Y>y1 else 0
    count+=(dx*dx+dy*dy)*B<A
   counts.append(count);minimum[qi]=min(minimum[qi],count)
  bad=[i for i,(count,q) in enumerate(zip(counts,queries)) if count<q['required']];need(case['id']!='candidate' or not bad,'candidate control');results.append({'case':case['id'],'possible_counts':counts,'violated_queries':bad})
 out=ROOT/'verify/out/n100-directional-center-counts.json';need(not out.exists(),'overwrite');out.write_text(json.dumps({'schema':'n100-directional-center-counts/v1','radius_upper':str(U),'queries':queries,'query_count':len(queries),'placement_cases':4200,'extra_cases':len(extra),'minimum_possible_counts':minimum,'results':results,'excluded_placement_count':sum(bool(r['violated_queries']) for r in results[:4200]),'excluded_extra_count':sum(bool(r['violated_queries']) for r in results[4200:]),'scope':'all4200 surviving labels screened on inherited wider stage-axis boxes, not full downstream per-placement propagation; plus32 refined spatial leaves and candidate; target disks contained exactly in unit disk','global_optimality':False,'bindings':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in [cp,dompath]},'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()},indent=2)+'\n',encoding='utf-8');print('PASS directional counts','queries',len(queries),'placements',4200,'excluded',sum(bool(r['violated_queries']) for r in results[:4200]),'extra excluded',sum(bool(r['violated_queries']) for r in results[4200:]))
if __name__=='__main__':main()
