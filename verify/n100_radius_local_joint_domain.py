"""Intersect radius-local outer joint-area constraints with recursive count strata."""
from pathlib import Path
from fractions import Fraction as F
from functools import lru_cache
import sys,json,hashlib
R=Path(__file__).resolve().parents[1];P=R/'runtime/disk100-release-lf-67ebf1c/certified_bounds_11323/working/lower_bounds_extension_20261004/verify_extension.py';sys.path.insert(0,str(P.parent));import verify_extension as E
E.trig=lru_cache(None)(E.trig)
def main():
 source=R/'verify/out/n100-radius-count-strata.json';z=json.loads(source.read_text(encoding='utf-8'));layers=[]
 for layer in z['layers']:
  radius=F(layer['radius_upper']);old=set(map(tuple,layer['triples']));families=sorted({t[:2] for t in old});rows=[{'m':m,**E.classify(m,B,radius)} for m,B in families];alive={(c['m'],c['B']) for c in rows if c['status']=='not excluded'};new=sorted(t for t in old if t[:2] in alive);removed=sorted(old-set(new));E.need((100,32,32) in new,'candidate integer-label control');layers.append({'label':layer['label'],'radius_upper':str(radius),'minimum_nonserving':layer['minimum_nonserving'],'outer_family_rows':rows,'prior_triple_count':len(old),'remaining_triples':new,'removed_triples':removed,'remaining_triple_count':len(new),'remaining_family_count':len(alive),'removed_family_count':len(families)-len(alive)});print('LAYER',layer['label'],'triples',len(old),'->',len(new),'families',len(families),'->',len(alive),flush=True)
 domains=[set(map(tuple,l['remaining_triples'])) for l in layers];E.need(all(a<=b for a,b in zip(domains,domains[1:])),'nested strengthened strata');out=R/'verify/out/n100-radius-local-joint-domain.json';E.need(not out.exists(),'overwrite');out.write_text(json.dumps({'schema':'n100-radius-local-joint-domain/v1','layers':layers,'candidate_count_control_retained_all_layers':True,'nested_domains':True,'scope':'each saved upper-radius outer count area test intersected with certified recursive counts; valid below each upper endpoint by radius monotonicity; inherited normalized diagram analytic dependencies; not feasible covering construction or full graph enumeration','global_optimality':False,'source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()},indent=2)+'\n',encoding='utf-8');print('PASS radius-local outer/inner intersection')
if __name__=='__main__':main()
