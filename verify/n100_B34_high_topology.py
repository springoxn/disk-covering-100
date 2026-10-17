"""Radius-free topology narrowing for B34 M26/F104 no-low residual."""
from pathlib import Path
from fractions import Fraction as F
import json,hashlib
import sympy as sp
ROOT=Path(__file__).resolve().parents[1]
def main():
 if not __debug__:raise RuntimeError('Assertions must remain enabled')
 cp=ROOT/'verify/out/n100-B34-low-and-high-reduction-171.json';proof=json.loads(cp.read_text(encoding='utf-8'));assert proof['status']=='PASS' and proof['high_remaining']['positive_excess']==2
 # Before first peel core connectivity/simple-frontier enforced by /6.
 # I66 M26 e0/b0: F104. Disconnected components and bridges lose>=4 or2
 # total cyclic-frontier units, stronger than needed.
 assert all(6*(104+2*(c-1))>(26-4*(c-1))**2 for c in range(2,8));assert 6*104>24**2 and 6*104>3**2+23**2
 # Chords C, empty all-boundary faces f3, a=C-f3. Strict degree excessh.
 # b=20-h-C-3a; deleted=46-h-C-a. /6 for stripped blocks yields
 # F<=46-h-C-a + (20-h-C-3a)^2/6. Enumerate all integer feasible slots.
 survivors=[]
 for h in range(3):
  for C in range(24):
   for a in range(C+1):
    frontier=20-h-C-3*a
    if frontier<0:continue
    bound=F(46-h-C-a)+F(frontier**2,6)
    if bound>=104:survivors.append({'deep_excess':h,'chords':C,'empty_boundary_triangles':C-a,'a':a,'inner_frontier':frontier,'removed_faces':46-h-C-a,'remaining_faces':104-(46-h-C-a),'peel_upper':str(bound)})
 assert {(r['deep_excess'],r['chords'],r['a']) for r in survivors}=={(0,0,0),(1,0,0),(0,1,0)}
 # Check CAS general count and all6 face multiplicities. C1/a0 has one
 # empty boundary triangle, so exactly one core ear and one diagonal.
 h,C,a=sp.symbols('h C a',integer=True);b=20-h-C-3*a;removed=46-h-C-a;assert sp.expand((26+b+2*a)-removed)==0
 x,y=sp.symbols('DDD DDR');f3=C-a;f2=26+2*C-3*f3;solution=sp.solve([x+y+f2+f3-104,3*x+2*y+f2-(240+h)],(x,y));assert sp.expand(solution[x]-(58+C+h))==0;assert sp.expand(solution[y]-(20-C-h-3*a))==0
 original=ROOT/'runtime/disk100-release-lf-67ebf1c/certified_bounds_11323/working/GENERAL_FIRST_BOUNDARY_PEEL_CHORDS.md';out=ROOT/'verify/out/n100-B34-high-topology-174.json';assert not out.exists();out.write_text(json.dumps({'schema':'n100-B34-high-topology-residual/v1','status':'PASS_REDUCTION','radius':'2831/25000','B':34,'core_vertices':66,'core_faces':104,'core_boundary':26,'deep_vertices':40,'core_connected_simple_single_block':True,'topology_slots':survivors,'chordless_slots':{'deep_excess':[0,1],'DDD':'58+h','DDR':'20-h','DRR':26,'BRR':26},'one_chord_slot':{'deep_excess':0,'empty_core_boundary_triangles':1,'DDD':59,'DDR':19,'DRR':25,'BRR_paired':24,'BRR_unpaired':2,'RRR':1,'inner_frontier':19,'inner_faces':59},'CAS_chord_aware_count_identities':True,'interpretation':'One-chord case necessarily bounds a single empty triangular region; deep original degrees all6, total high curvature2 lies on ring. Chordless case permits h0/all high curvature on ring or h1/one deep7 and one ring7. No actual high profile is discarded by metric discovery.','high_M_closed':False,'full_B34_closed':False,'global_bound_improved':False,'dependencies':'General/6 isoperimetry for retained strict-star blocks, common core Euler identities and chord-aware first peel; analytic separation inherited, integer slots fully enumerated.','bindings':{p.relative_to(ROOT).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in (Path(__file__),cp,original)}},indent=2)+'\n',encoding='utf-8');print('B34 HIGH TOPOLOGY PASS exactly3 slots: chordlessh0/h1, onechordh0',flush=True)
if __name__=='__main__':main()
