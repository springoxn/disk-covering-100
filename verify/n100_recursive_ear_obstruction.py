"""Ear-triangle obstruction for the first surviving recursive inner count."""
from pathlib import Path
from fractions import Fraction as F
from functools import lru_cache
import sys,json,hashlib
ROOT=Path(__file__).resolve().parents[1];P=ROOT/'runtime/disk100-release-lf-67ebf1c/certified_bounds_11323/working/lower_bounds_extension_20261004/verify_extension.py';sys.path.insert(0,str(P.parent));import verify_extension as E

def H_upper(t,a,b):
 E.need(0<a<=b<F(1),'angle interval');sl=E.sin_at(a/2)[0];sh=E.sin_at(b/2)[1];E.need(0<sl<=sh<t,'H sqrt positive');return sh*E.sqrt_bounds(t*t-sl*sl)[1]+(b-E.sin_at(a)[0])/2

def main():
 priorpath=ROOT/'verify/out/n100-recursive-joint-area.json';prior=json.loads(priorpath.read_text(encoding='utf-8'));t=F(prior['normalized_radius']);n=prior['minimum_non_circle_serving_disks'];Blist=prior['count_rows'][-1]['not_excluded_B'];x=2*t;coef=F(1);v=F(0)
 for j in range(30):v+=coef*x**(2*j+1);coef*=F((2*j+1)**2,2*(j+1)*(2*j+3))
 cap=2*(v+coef*x**61/(1-x*x));S=10**30;gamma=F(cap.numerator*S//cap.denominator+1,S);rows=[]
 for B in Blist:
  E.need(gamma*B<6*E.PL,'concentration below equal mean');small=gamma/3;lo=(2*E.PL-gamma)/(B-3);hi=(2*E.PH-gamma)/(B-3);hs=3*H_upper(t,small,small)+(B-3)*H_upper(t,lo,hi);base=((2*n-B-2)*E.AH+B*E.KAPPA)*t*t;deficit=E.PL-base-hs;rows.append({'inner_boundary_cells':B,'three_arc_sum_upper':str(gamma),'three_arc_mean':str(small),'other_arc_mean_interval':[str(lo),str(hi)],'boundary_function_sum_upper':str(hs),'triangle_anchor_base_upper':str(base),'strict_area_deficit':str(deficit),'ear_excluded':deficit>0})
 out=ROOT/'verify/out/n100-recursive-ear-obstruction.json';E.need(not out.exists(),'overwrite');out.write_text(json.dumps({'schema':'n100-recursive-ear-obstruction/v1','outer_radius_upper':prior['radius_upper'],'normalized_inner_radius':str(t),'inner_disk_count':n,'three_arc_angle_upper':str(gamma),'rows':rows,'no_ear_B':[r['inner_boundary_cells'] for r in rows if r['ear_excluded']],'not_excluded_B':[r['inner_boundary_cells'] for r in rows if not r['ear_excluded']],'analytic_dependencies':['same normalized inner triangulation as stage105','ear face with2boundary edges has3consecutive boundary sites within t of a common Voronoi point; their3assigned arcs lie in radius2t disk, hence sum angle<=2asin(2t)','boundary H_t concavity, Jensen within3arc group and remaining group','three-group Jensen bound increases with concentrated group sum up to equal means, so substitute gamma upper below6pi/B','joint center-anchor area base valid even before no-ear restriction'],'scope':'topology constraint for inner58-disk normalized covers, not exclusion of58disks or unconditional outer triple pruning','global_optimality':False,'bindings':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in [P,priorpath]},'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()},indent=2)+'\n',encoding='utf-8');print('PASS recursive ear test','excluded ears at B',[r['inner_boundary_cells'] for r in rows if r['ear_excluded']],'unresolved',[r['inner_boundary_cells'] for r in rows if not r['ear_excluded']])
if __name__=='__main__':main()
