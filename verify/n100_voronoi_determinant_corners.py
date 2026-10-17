"""Exact determinant extrema on independent center boxes (multi-affine polynomial)."""
from pathlib import Path
from itertools import product,combinations
import json,hashlib
from n100_circle_center_alternating import ROOT,load,need
from n100_boundary_circle_propagation import setup
from n100_voronoi_bisector_vertex import coord,sub,mul

def main():
 source='verify/out/n100-voronoi-joint-cramer.json';z=load(source);core=load('verify/out/n100-cubic-core-roundtrip.json')['core'];prior={tuple(c['placement']):c['boxes'] for c in load('verify/out/n100-axis-coupled-boxes.json')['retained']};rows=[]
 for row in z['rows']:
  p=row['summary']['placement'];B=row['boxes'];_,E,q=setup(core,p,prior[tuple(p)]);inc={}
  for f,v in E:inc.setdefault(v,set()).add(f)
  results=[]
  for v,owners in sorted(inc.items()):
   for faces in combinations(sorted(owners),3):
    a,b,c=[B[f] for f in faces];C=[sub(coord(b,k),coord(a,k)) for k in (0,1)];D=[sub(coord(c,k),coord(a,k)) for k in (0,1)];naive=sub(mul(C[0],D[1]),mul(C[1],D[0]));values=[];corners=[]
    for corner in product(*[coord(site,k) for site in (a,b,c) for k in (0,1)]):
     ax,ay,bx,by,cx,cy=corner;det=(bx-ax)*(cy-ay)-(by-ay)*(cx-ax);expanded=bx*cy-bx*ay-ax*cy-by*cx+by*ax+ay*cx;need(det==expanded,'determinant corner identity');values.append(det);corners.append(corner)
    lo=min(values);hi=max(values);need(naive[0]<=lo<=hi<=naive[1],'exact corner range within ordinary interval range');results.append({'vertex':v,'centers':faces,'naive_determinant':naive,'exact_box_determinant':[lo,hi],'min_corner':corners[values.index(lo)],'max_corner':corners[values.index(hi)],'excludes_zero':lo>0 or hi<0})
  summary={'child':row['summary']['child'],'placement':p,'triples':len(results),'naive_excludes_zero':sum(r['naive_determinant'][0]>0 or r['naive_determinant'][1]<0 for r in results),'exact_box_excludes_zero':sum(r['excludes_zero'] for r in results),'ranges_strictly_tightened':sum(tuple(r['exact_box_determinant'])!=tuple(r['naive_determinant']) for r in results)};rows.append({'summary':summary,'triples':results});print('EXACT DET',summary,flush=True)
 out=ROOT/'verify/out/n100-voronoi-determinant-corners.json';need(not out.exists(),'overwrite');paths=[source,'verify/out/n100-cubic-core-roundtrip.json','verify/out/n100-axis-coupled-boxes.json','verify/n100_voronoi_joint_cramer.py','verify/n100_voronoi_bisector_vertex.py'];out.write_text(json.dumps({'schema':'n100-voronoi-determinant-corners/v1','verified_integer_corner_ranges':True,'corner_count_per_triple':64,'all_corner_polynomial_identities_equal':True,'all_exact_ranges_nested_in_naive':True,'rows':rows,'analytic_dependency':'oriented area determinant is affine in each of six scalar center coordinates separately, so box extrema occur at corners; continuity on connected box implies every intermediate determinant attained','scope':'extrema on independent coordinate boxes, not on jointly constrained Voronoi configurations; corner witnesses need not satisfy other geometry','machine_verified_geometry':False,'global_optimality':False,'bindings':{s:hashlib.sha256((ROOT/s).read_bytes()).hexdigest() for s in paths},'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()},indent=2)+'\n',encoding='utf-8');print('PASS exact determinant corner audit')
if __name__=='__main__':main()
