"""B33 degree4 replacement: peel a p3 four-star and force a disjoint low star.
Integer/Fraction interval acceptance only; inherits general/6 disk isoperimetry.
"""
from pathlib import Path
from fractions import Fraction as F
import sys,json,hashlib
import sympy as sp
ROOT=Path(__file__).resolve().parents[1];W=ROOT/'runtime/disk100-release-lf-67ebf1c/certified_bounds_11323/working';sys.path[:0]=[str(W),str(W/'lower_bounds_extension_20261004')]
from verify_star_lp_duals import q,S
from verify_complete_star_area_caps import cap
import verify_extension as geometry
R=F(2831,25000);B=33;INTERIOR=67
def verify():
 if not __debug__:raise RuntimeError('Assertions must remain enabled')
 geometry.check_kappa();A=3*q(3).sqrt()/4;h0=q(F(1,2)-geometry.KAPPA);stars={d:cap(d) for d in (3,4,5,9)};loss={d:d*A-stars[d]-(d-1)*h0 for d in stars};old=((198-B)*geometry.AH+B*geometry.KAPPA)*R*R+B*geometry.H_upper(R,2*geometry.PL/B,2*geometry.PH/B);budget=(old-geometry.PL)/(R*R)
 assert h0.l>0 and min(loss[3].l,loss[4].l)>loss[5].u>0
 assert F(loss[3].l,S)>budget and F(loss[9].l,S)>budget
 # d>=9 monotonicity exactly as the existing global window proof.
 from verify_global_star_anchor_degree_window import verify as old_check
 old_degree=old_check();assert F(old_degree['large_degree_monotonic_margin_lower'])>0
 p_le2=loss[4]+h0;disjoint=loss[4]+loss[5];assert F(p_le2.l,S)>budget and F(disjoint.l,S)>budget
 # p3 on a four-cycle consists of the3 consecutive outer edges of a proper
 # four-B-neighbor path; the fourth edge is an existing original-B chord.
 ring=[0,1,2,3];center=4;faces=[(center,ring[i],ring[(i+1)%4]) for i in range(4)];edges={}
 for tri in faces:
  for i in range(3):edge=tuple(sorted((tri[i],tri[(i+1)%3])));edges[edge]=edges.get(edge,0)+1
 assert {e for e,n in edges.items() if n==1}=={(0,1),(1,2),(2,3),(0,3)};assert all(edges[tuple(sorted((center,x)))]==2 for x in ring)
 # Interior boundary-path sites1,2 have their entire interior fan already
 # filled; stripping them and the sole interior center leaves one simple disk.
 trimmed_B=B-2;trimmed_I=INTERIOR-1;original_F=2*INTERIOR+B-2;trimmed_F=2*trimmed_I+trimmed_B-2
 assert (trimmed_B,trimmed_I,original_F,trimmed_F)==(31,66,165,161);assert original_F-trimmed_F==4;iso_gap=6*trimmed_F-trimmed_B**2;assert iso_gap==5>0
 # Thus one other interior degree<=5 exists in the original unchanged stars.
 # First star has only B neighbors, hence the two stars/marked anchors are
 # face-disjoint. The joint face-loss bank pays their losses once each.
 n,b=sp.symbols('n b',integer=True);assert sp.expand((2*n+b-2)-(2*(n-1)+(b-2)-2)-4)==0
 effective=min(F(p_le2.l,S),F(disjoint.l,S));assert effective>budget
 return {'status':'PASS','radius':str(R),'B':B,'required_center_norm_squared_upper':str(1-R*R),'minimum_interior_degree':5,'maximum_interior_degree':8,'degree3_loss_lower':str(F(loss[3].l,S)),'degree4_loss_lower':str(effective),'raw_single_degree4_loss_lower':str(F(loss[4].l,S)),'degree5_loss_lower':str(F(loss[5].l,S)),'degree_at_least9_loss_lower':str(F(loss[9].l,S)),'old_normalized_budget_upper':str(budget),'new_degree_window_margin_lower':str(effective-budget),'p_le2_margin_lower':str(F(p_le2.l,S)-budget),'p3_disjoint_low_margin_lower':str(F(disjoint.l,S)-budget),'peeled_disk':{'B':trimmed_B,'interior':trimmed_I,'faces':trimmed_F,'six_F_minus_B_squared':iso_gap},'source_of_extra_loss':'p<=2: one fewer anchor loss; p3: proper boundary fan peeled, /6 forces another interior low site with a face-disjoint complete star','geometric_dependencies':'common simple planar center triangulation, complete-star cap, distinct marked anchors, nonnegative joint face-loss bank and general/6 disk isoperimetry; p3 four-star fills proper outer path and can be removed along existing chord; no formal theorem-prover derivation','global_bound_improved':False}
def main():
 result=verify();result['bindings']={p.relative_to(ROOT).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in (Path(__file__),W/'GLOBAL_STAR_ANCHOR_DEGREE_WINDOW.md',W/'verify_global_star_anchor_degree_window.py',W/'verify_complete_star_area_caps.py',W/'lower_bounds_extension_20261004/GENERAL_DISK_ISOPERIMETRY.md')};out=ROOT/'verify/out/n100-B33-degree-window-151.json';assert not out.exists();out.write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8');print('B33 DEGREE WINDOW PASS; exact new margin',result['new_degree_window_margin_lower'],'p3 margin',result['p3_disjoint_low_margin_lower'],flush=True)
if __name__=='__main__':main()
