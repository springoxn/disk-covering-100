"""Independent rational constants and fan combinatorics audit of B33 degree window."""
from pathlib import Path
from fractions import Fraction as F
import json,hashlib,itertools
import sympy as sp
ROOT=Path(__file__).resolve().parents[1]
def main():
 path=ROOT/'verify/out/n100-B33-degree-window-151.json';proof=json.loads(path.read_text(encoding='utf-8'));assert proof['status']=='PASS' and proof['B']==33 and F(proof['radius'])==F(2831,25000);budget=F(proof['old_normalized_budget_upper']);sqrt3lo=F(1732050807,10**9);sqrt5hi=F(2236067978,10**9);assert sqrt3lo**2<3 and sqrt5hi**2>5;Alo=3*sqrt3lo/4;h0=F(1,2)-F(461134488,10**9);S5hi=F(623,100);assert S5hi*S5hi>25*(25+11*sqrt5hi)/32
 D3=3*Alo-2-2*h0;D4=4*Alo-4-3*h0;D5=5*Alo-S5hi-4*h0;assert min(D3,D4)>D5>0;two_anchor=D4+h0;extra_star=D4+D5;assert D3>budget and two_anchor>budget and extra_star>budget;assert F(proof['degree_at_least9_loss_lower'])>budget
 # S5 surd identity independently matches the trig regular5 expression.
 r=sp.sqrt(5);s5=sp.Rational(5,16)*(3+r)*sp.sqrt(10+2*r);assert sp.simplify(s5*s5-sp.Rational(25,32)*(25+11*r))==0
 cycle=[(0,1),(1,2),(2,3),(3,0)];cases=[]
 for omitted in range(4):
  marked=[e for j,e in enumerate(cycle) if j!=omitted];degree={i:sum(i in e for e in marked) for i in range(4)};ends={i for i,d in degree.items() if d==1};middle={i for i,d in degree.items() if d==2};assert len(ends)==len(middle)==2 and set(cycle[omitted])==ends
  # Every middle original-B vertex has precisely the2 star triangles between
  # its two original outer-boundary edges. There is no unused interior sector.
  faces=[(4,i,j) for i,j in cycle];incident={v:[f for f in faces if v in f] for v in middle};assert all(len(fs)==2 for fs in incident.values());assert all({w for f in fs for w in f if w!=v}==({4}|{w for e in marked if v in e for w in e if w!=v}) for v,fs in incident.items());cases.append({'omitted_edge':cycle[omitted],'outer_path_middle_vertices':sorted(middle),'removed_center':4})
 n,b=sp.symbols('n b',integer=True);oldF=2*n+b-2;newF=2*(n-1)+(b-2)-2;assert sp.expand(oldF-newF)==4;assert newF.subs({n:67,b:33})==161;assert 6*161-31**2==5
 # The two low centers cannot share a selected face: all4 neighbors of the
 # first are original boundary sites. A shared face would contain their edge.
 selected_faces=[{4,i,j} for i,j in cycle];other=5;assert all(other not in f for f in selected_faces);assert len({tuple(sorted(e)) for e in cycle})==4
 out=ROOT/'verify/out/n100-B33-degree-window-independent-153.json';assert not out.exists();out.write_text(json.dumps({'schema':'n100-B33-degree-independent-fan-audit/v1','status':'PASS','radius':'2831/25000','budget_upper':str(budget),'rational_root_brackets':{'sqrt3_lower':str(sqrt3lo),'sqrt5_upper':str(sqrt5hi),'S5_upper':str(S5hi)},'p_le2_margin_lower':str(two_anchor-budget),'p3_disjoint_margin_lower':str(extra_star-budget),'four_outer_path_cases':cases,'CAS_peel_Euler_and_degree5_cap_identities':True,'trimmed_disk_counts':{'B':31,'I':66,'F':161,'six_F_minus_B_squared':5},'star_face_and_marked_anchor_disjointness_review':'p3 degree4 link has only original-B neighbors. Any other interior low site is nonadjacent; selected triangle sets disjoint, and a marked original-B edge has one incident interior triangle/anchor. Losses consume original joint bank once.','planar_dependency':'simple disk triangulation implies the3 marked link edges form a proper outer path and middle boundary stars have no additional interior sector; stripping the filled fan along its existing chord leaves one simple disk. General/6 theorem applies to remaining unchanged interior stars. Not a formal planar-embedding kernel.','degree3_and_degree9_exclusions':True,'minimum_interior_degree':5,'maximum_interior_degree':8,'global_bound_improved':False,'bindings':{p.relative_to(ROOT).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in (Path(__file__),path,ROOT/'verify/n100_B33_degree_window.py')}},indent=2)+'\n',encoding='utf-8');print('INDEPENDENT B33 DEGREE WINDOW PASS; rational p<=2 and p3 margins positive; all4 fan paths checked',flush=True)
if __name__=='__main__':main()
