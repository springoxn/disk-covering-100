"""Independent exact outer radius-local classifications and full domain replay."""
from pathlib import Path
from fractions import Fraction as F
from functools import lru_cache
import json,hashlib
from n100_recursive_joint_area_independent import atan,rnd,series,sqrtiv,need
R=Path(__file__).resolve().parents[1]
def main():
 path=R/'verify/out/n100-radius-local-joint-domain.json';z=json.loads(path.read_text(encoding='utf-8'));sp=R/'verify/out/n100-radius-count-strata.json';source=json.loads(sp.read_text(encoding='utf-8'));need(z['source_sha256']==hashlib.sha256(sp.read_bytes()).hexdigest(),'source binding');pl,ph=rnd(16*atan(F(1,5),40)-4*atan(F(1,239),41),16*atan(F(1,5),41)-4*atan(F(1,239),40));al,ah=[3*x/4 for x in sqrtiv(F(3))];kap=F(461134488,10**9)
 @lru_cache(None)
 def trig(B):return (*rnd(series(pl/B)[0],series(ph/B)[1]),*rnd(series(ph/B,True)[0],series(pl/B,True)[1]))
 reports=[];domains=[];checked=0
 need(len(z['layers'])==len(source['layers'])==4,'four layers')
 for layer,src in zip(z['layers'],source['layers']):
  r=F(layer['radius_upper']);need(r==F(src['radius_upper']) and layer['minimum_nonserving']==src['minimum_nonserving'],'layer identity');old=set(map(tuple,src['triples']));families={t[:2] for t in old};need([(c['m'],c['B']) for c in layer['outer_family_rows']]==sorted(families),'all family rows');alive=set()
  for row in layer['outer_family_rows']:
   m,B=row['m'],row['B'];sl,sh,cl,ch=trig(B);checked+=1
   if sl>r:status='arc exclusion'
   else:
    need(sh<r,'arc interval');coef=F(2*m-2,B)-1;low=(coef*al+kap)*r*r+sl*sqrtiv(r*r-sh*sh)[0]-sh*ch;high=(coef*ah+kap)*r*r+sh*sqrtiv(r*r-sl*sl)[1]-sl*cl
    if high<0:status='area exclusion'
    else:need(low>0,'area undecided');status='not excluded';alive.add((m,B))
   need(status==row['status'],'independent classification')
  new={t for t in old if t[:2] in alive};need(sorted(new)==list(map(tuple,layer['remaining_triples'])) and sorted(old-new)==list(map(tuple,layer['removed_triples'])),'all retained and removed triples');need(len(new)==layer['remaining_triple_count'] and len(alive)==layer['remaining_family_count'],'counts');need((100,32,32) in new,'candidate label control');domains.append(new);reports.append({'label':layer['label'],'radius_upper':str(r),'prior_triples':len(old),'remaining_triples':len(new),'removed_triples':len(old-new),'prior_families':len(families),'remaining_families':len(alive)})
 need(all(a<=b for a,b in zip(domains,domains[1:])),'nested domains');out=R/'verify/out/n100-radius-local-joint-domain-independent.json';need(not out.exists(),'overwrite');out.write_text(json.dumps({'schema':'n100-radius-local-joint-domain-independent/v1','verified_all_radius_local_families_and_triples':True,'outer_family_cases_checked':checked,'layers':reports,'candidate_count_control_retained_all_layers':True,'scope':'independent interval classifications and complete finite domain intersection; geometric normalization, boundary concavity and triangle-area premises inherited; no new global radius lower bound','global_optimality':False,'input_sha256':hashlib.sha256(path.read_bytes()).hexdigest()},indent=2)+'\n',encoding='utf-8');print('PASS independent radius-local joint domains',[(l['label'],l['remaining_triples'],l['remaining_families']) for l in reports],'family cases',checked)
if __name__=='__main__':main()
