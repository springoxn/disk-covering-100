"""Independent annular integer cuts and safe box-domain screening."""
from pathlib import Path
from fractions import Fraction as F
import json,hashlib
ROOT=Path(__file__).resolve().parents[1]
def need(c,m):
 if not c:raise ValueError(m)
def load(p):return json.loads((ROOT/p).read_text(encoding='utf-8'))
def main():
 path=ROOT/'verify/out/n100-annular-center-cuts.json';z=json.loads(path.read_text(encoding='utf-8'));r=F(z['radius_upper']);Q=2**20
 for cut in z['universal_cuts']:
  a,b=F(cut['annulus_inner']),F(cut['annulus_outer']);n=cut['minimum_centers'];need(F(n-1)*r*r<b*b-a*a<=F(n)*r*r,'integer threshold');need(F(cut['center_norm_lower'])==max(F(0),a-r) and F(cut['center_norm_upper'])==b+r,'triangle band');need(cut['all_counted_centers_non_circle_serving']==(b+r<1-r),'nonserving label')
 a,b=map(F,z['rejected_specific_radial_multiset']['empty_open_annulus']);
 for row in z['rejected_specific_radial_multiset']['separations']:
  d=F(row['distance']);need(d+r<a or d-r>b,'strict annulus empty')
 arc=load('verify/out/n100-arc-center-projection.json');candidate=next(c for c in arc['cases'] if c['source_node'] is None);joint=load('verify/out/n100-spatial-leaf-joint.json');cases=[('candidate',candidate['result']['boxes'])]+[(str(c['tree_node']),c['arc_result']['boxes']) for c in joint['leaves'] if not c['excluded']];rows=[]
 for name,boxes in cases:
  summaries=[]
  for cut in z['universal_cuts']:
   lo=F(cut['center_norm_lower']);hi=F(cut['center_norm_upper']);possible=[];certain=[]
   for v,box in enumerate(boxes[:100]):
    lows=[];highs=[]
    for j in (0,2):
     A,B=F(box[j],Q),F(box[j+1],Q);lows.append(F(0) if A<=0<=B else min(A*A,B*B));highs.append(max(A*A,B*B))
    L=sum(lows);H=sum(highs)
    if L<=hi*hi and H>=lo*lo:possible.append(v)
    if lo*lo<=L and H<=hi*hi:certain.append(v)
   summaries.append({'annulus':[cut['annulus_inner'],cut['annulus_outer']],'required':cut['minimum_centers'],'possible_center_count':len(possible),'certain_center_count':len(certain),'possible_centers':possible,'excluded':len(possible)<cut['minimum_centers']})
  excluded=any(c['excluded'] for c in summaries)
  if name=='candidate':need(not excluded,'candidate rejected: investigate')
  rows.append({'case':name,'excluded':excluded,'cuts':summaries})
 out=ROOT/'verify/out/n100-annular-center-cuts-independent.json';need(not out.exists(),'overwrite');out.write_text(json.dumps({'schema':'n100-annular-center-cuts-independent/v1','verified_integer_annular_counts':True,'specific_radial_multiset_rejected':True,'candidate_retained':True,'screened_box_cases':len(rows),'excluded_box_cases':sum(c['excluded'] for c in rows),'rows':rows,'scope':'safe squared-norm possibility count screening on center boxes; box overlap with norm band only necessary; no full global cover proof','global_optimality':False,'input_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()},indent=2)+'\n',encoding='utf-8');print('PASS independent annular cuts','cases',len(rows),'excluded',sum(c['excluded'] for c in rows),'candidate retained')
if __name__=='__main__':main()
