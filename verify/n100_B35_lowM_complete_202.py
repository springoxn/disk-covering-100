"""B35 lowM exact profile reduction and core-ear obstruction."""
from pathlib import Path
from fractions import Fraction as F
import json,hashlib
import sympy as sp
ROOT=Path(__file__).resolve().parents[1]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 if not __debug__:raise RuntimeError('Assertions must remain enabled')
 dp=ROOT/'verify/out/n100-B35-full-gaps-190.json';j=json.loads(dp.read_text(encoding='utf-8'));assert j['status']=='PASS_PREMISES';R=F(j['radius']);assert R==F(2831,25000);row=j['replay']['result']['branches'][0];assert row['M']==24 and not row['restricted'];g={(p,d):F(v) for p,d,v in row['full_vertex_gaps']};assert set(g)=={(p,d) for p in range(5) for d in range(max(3,p+1),100)}
 for rel,h in j['bindings'].items():assert sha(ROOT/rel)==h
 base=F(row['M_le24_flagged_margin']);slope=F(row['M_slope'][0]);assert slope>0
 # Conservative minimum over entire finite M<=24 domain; original M slope is positive.
 # M may be negative in shifted notation: U>=0 and e<=B/2 yields M>=-34.
 Mmin=-34;worst=base+(24-Mmin)*R*R*slope
 margins={}
 margins['selected_witness_degree3or4']=F(row['ordinary_margin'])+R*R*min(g[0,3],g[0,4])
 margins['additional_low_degree']=worst+R*R*min(v for (p,d),v in g.items() if d<=5)
 margins['any_degree8plus']=worst+R*R*min(v for (p,d),v in g.items() if d>=8)
 margins['any_degree7_p_le3']=worst+R*R*min(g[p,7] for p in range(4))
 margins['one_ear']=worst-R*R*F(row['shifted_ear_upper'])
 margins['one_bad_q1']=worst-R*R*F(row['bad_q1_upper'])
 assert all(v>0 for v in margins.values()),margins
 # Thus unique degree5 is the compulsory unmarked p0 witness; all other
 # interiors6/7, every7 hasp4, e=b0. Euler implies N7=30-M>=6.
 N7,M=sp.symbols('N7 M',integer=True);assert sp.solve(sp.Eq(N7-1,29-M),N7)==[30-M]
 # One strict positive curvature unit permits inherited blockwise /5.
 # I65, e0: F=128-M+2(c-1)+n3, b=M-4(c-1)-n3.
 # Enumerate all feasible components and n3; b nonnegative is necessary.
 possible=[]
 for mm in range(Mmin,25):
  for c in range(1,66):
   for n3 in range(2*(c-1)+1):
    b=mm-4*(c-1)-n3;faces=128-mm+2*(c-1)+n3
    if b>=0 and 5*faces<=b*b:possible.append((mm,c,n3,b,faces))
 assert possible==[(23,1,0,23,105),(24,1,0,24,104)]
 # Bridges/multiple blocks consume frontier; /5 excludes both remaining cases.
 topology=[]
 for mm,c,n3,b,faces in possible:
  assert 5*faces>(b-2)**2 and 5*faces>9+(b-3)**2
  # Every7 with4 distinct owned boundary edges has >=5 boundary neighbours;
  # hence <=2 core neighbours. Simple core disk has degree>=2 -> core ear.
  # Distinct core degree2 vertices cannot be adjacent in boundary cycleP>3:
  # each link contains its two boundary neighbours joined by an edge, which
  # would force the other degree2 vertex to have a third neighbour.
  # Remove two nonadjacent ears: simple diskP-2/F-2, strict stars unchanged.
  assert 5*(faces-2)>(b-2)**2
  assert 30-mm>=6
  topology.append({'M':mm,'core_faces':faces,'core_boundary':b,'required_core_ears_min':30-mm,'two_ear_contradiction_integer_margin':5*(faces-2)-(b-2)**2})
 out=ROOT/'verify/out/n100-B35-lowM-complete-202.json';assert not out.exists();out.write_text(json.dumps({'schema':'n100-B35-lowM-complete/v1','status':'PASS','radius':str(R),'B':35,'low_M_closed':True,'domain':'M<=24','required_center_norm_squared_upper':str(1-R*R),'M_min_conservative':Mmin,'profile_margins':{k:str(v) for k,v in margins.items()},'forced_profile':'e=b0; unique unmarkeddegree5; all other interior degrees6/7; every7 owns4 marked edges','CAS_curvature_identity':'N7=30-M','remaining_core_topologies_before_ear_contradiction':topology,'geometric_argument':'Inherited one-positive-curvature disk /5 applied blockwise: only simpleP23/F105 orP24/F104 cores survive. A degree7 owner of4 boundary edges has>=5 original-boundary neighbours, hence exactly2 core neighbours and is a core ear. Two degree2 boundary vertices in a simple triangulated diskP>3 are nonadjacent and can be deleted together, giving simple disk(P-2,F-2) with at most one strictdegree5 and other strictdegrees>=6; /5 fails in both cases. Euler requires at least6 such ears. No metric payment is added for this topology argument.','dependencies':'Same-radius compulsory unmarked low-degree core obstruction, reviewed /5 disk lemma, common normalized center triangulation and degree/Euler identities. Analytic combinatorial proof with exact integer/CAS checks, not formal embedding kernel.','full_B35_closed':False,'global_bound_improved':False,'bindings':{p.relative_to(ROOT).as_posix():sha(p) for p in (Path(__file__),dp)}},indent=2)+'\n',encoding='utf-8');print('B35 LOWM COMPLETE PASS: unique5/allhighq4 -> >=6coreears but atmost1',flush=True)
if __name__=='__main__':main()
