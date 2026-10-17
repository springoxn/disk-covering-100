"""Independent directional sphere-count audit on deterministic placements and all leaves."""
from pathlib import Path
from fractions import Fraction as F
import json,hashlib
ROOT=Path(__file__).resolve().parents[1]
def need(c,m):
 if not c:raise ValueError(m)
def load(s):return json.loads((ROOT/s).read_text(encoding='utf-8'))
def main():
 path=ROOT/'verify/out/n100-directional-center-counts.json';z=load(str(path.relative_to(ROOT)));h=load('verify/out/n100-inner-radial-hierarchy.json');ind=load('verify/out/n100-inner-radial-hierarchy-independent.json');need(ind['input_sha256']==hashlib.sha256((ROOT/'verify/out/n100-inner-radial-hierarchy.json').read_bytes()).hexdigest(),'independently checked local demands binding');U=F(z['radius_upper']);demands={F(c['target_radius']):c['minimum_centers'] for c in h['cuts']}
 for q in z['queries']:
  s=F(q['target_radius']);x,y=map(F,q['target_center']);need(x*x+y*y<=(1-s)**2 and F(q['region_radius'])==s+U and q['required']==demands[s],'contained target and correct demand')
 roots={tuple(r['placement']):r['boxes'] for r in load('verify/out/n100-axis-coupled-boxes.json')['retained']};leaf={str(c['tree_node']):c['arc_result']['boxes'] for c in load('verify/out/n100-spatial-leaf-joint.json')['leaves'] if not c['excluded']};leaf['candidate']=next(c for c in load('verify/out/n100-arc-center-projection.json')['cases'] if c['source_node'] is None)['result']['boxes'];indices=sorted(set([i*4199//20 for i in range(21)]+list(range(4200,len(z['results'])))+[i for i,r in enumerate(z['results']) if r['violated_queries']]));checked=[]
 for index in indices:
  row=z['results'][index];key=row['case'];boxes=roots[tuple(key)] if isinstance(key,list) else leaf[key];rects=[]
  for b in boxes[:100]:
   x0,x1,y0,y1=[F(v,2**20) for v in b];rects.append(((x0+x1)/2,(y0+y1)/2,(x1-x0)/2,(y1-y0)/2))
  counts=[]
  for q in z['queries']:
   x,y=map(F,q['target_center']);R2=F(q['region_radius'])**2;count=0
   for mx,my,hx,hy in rects:
    dx=max(F(0),abs(x-mx)-hx);dy=max(F(0),abs(y-my)-hy);count+=dx*dx+dy*dy<R2
   counts.append(count)
  bad=[j for j,(v,q) in enumerate(zip(counts,z['queries'])) if v<q['required']];need(counts==row['possible_counts'] and bad==row['violated_queries'],'direct fractional midpoint-box distances');checked.append(index)
 out=ROOT/'verify/out/n100-directional-center-counts-independent.json';need(not out.exists(),'overwrite');out.write_text(json.dumps({'schema':'n100-directional-center-counts-independent/v1','verified_contained_targets_and_sampled_counts':True,'queries_checked':len(z['queries']),'sampled_placement_cases':sum(i<4200 for i in checked),'all_extra_cases_checked':sum(i>=4200 for i in checked),'checked_indices':checked,'independently_checked_exclusions':sum(bool(z['results'][i]['violated_queries']) for i in checked),'scope':'independent direct Fraction midpoint-distance counts for21 evenly spaced placements, all32 leaves and candidate, and all production exclusions; not independent replay of all4200 placements; demand constants inherited from independently bound hierarchy certificate','global_optimality':False,'input_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()},indent=2)+'\n',encoding='utf-8');print('PASS independent directional audit','queries',len(z['queries']),'placement sample',sum(i<4200 for i in checked),'extra',sum(i>=4200 for i in checked))
if __name__=='__main__':main()
