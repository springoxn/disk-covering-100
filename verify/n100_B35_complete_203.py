"""Independent Fraction recomposition of B35 lowM and full branch assembly."""
from pathlib import Path
from fractions import Fraction as F
import json,hashlib
ROOT=Path(__file__).resolve().parents[1]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 if not __debug__:raise RuntimeError('Assertions must remain enabled')
 paths=[ROOT/'verify/out/n100-B35-full-gaps-190.json',ROOT/'verify/out/n100-B35-profile-reduction-191.json',ROOT/'verify/out/n100-B35-M25-M26-complete-201.json',ROOT/'verify/out/n100-B35-lowM-complete-202.json'];diag,red,high,low=[json.loads(p.read_text(encoding='utf-8')) for p in paths];R=F(2831,25000)
 assert diag['status']=='PASS_PREMISES' and red['status']=='PASS_REDUCTION' and high['status']==low['status']=='PASS' and high['M25_closed'] and high['M26_closed'] and low['low_M_closed'];assert all(F(x['radius'])==R for x in (diag,red,high,low))
 for c in (diag,red,high,low):
  for rel,h in c['bindings'].items():assert sha(ROOT/rel)==h
 row=diag['replay']['result']['branches'][0];g={(p,d):F(v) for p,d,v in row['full_vertex_gaps']};ordinary=F(row['ordinary_margin']);slope=F(row['M_slope'][0]);assert slope>0
 independent=[]
 # Enumerate every possible M after U>=0,e<=17 -> M>=-34.
 for M in range(-34,25):
  base=ordinary+R*R*(24-M)*slope
  selected=min(g[0,d] for d in (3,4));assert base+R*R*selected>0
  flagged=base+R*R*g[0,5];margins=[flagged+R*R*min(v for (p,d),v in g.items() if d<=5),flagged+R*R*min(v for (p,d),v in g.items() if d>=8),flagged+R*R*min(g[p,7] for p in range(4)),flagged-R*R*F(row['shifted_ear_upper']),flagged-R*R*F(row['bad_q1_upper'])];assert min(margins)>0;independent.extend(margins)
 # Independent outer walk bounds: F>=128-M and b<=M, so M<=22
 # impossible under/5; disconnected frontier loses4 and adds>=2faces.
 assert all(5*(128-M)>M*M for M in range(23))
 for M in (23,24):
  assert 5*(130-M)>(M-4)**2
  assert 5*(128-M)>(M-2)**2 and 5*(128-M)>9+(M-3)**2
  assert 5*(126-M)>(M-2)**2
  assert 30-M>=6 and 7-(4+1)==2
 # Two ears removal has original strict stars at retained strict vertices:
 # a removed boundary ear touches only boundary neighbours, and introduces
 # no deficit at any strict vertex, so at most one strictdegree5 remains.
 out=ROOT/'verify/out/n100-B35-complete-203.json';assert not out.exists();out.write_text(json.dumps({'schema':'n100-B35-complete-independent/v1','status':'PASS','radius':str(R),'B':35,'m':100,'required_center_norm_squared_upper':str(1-R*R),'full_B35_closed':True,'M_partition':['M<=24','M25','M26','M>=27'],'independent_lowM_margin_min':str(min(independent)),'M25_M26_independent_margins':high['independent_fraction_margins'],'source_hashes_checked':True,'budget_review':'LowM and highM use separate complete conditional contradictions. LowM uses one original scalar payment and vertex slacks once; unique5/core-ear topology consumes none. High16-model ledgers each use their own verified boundaryK and exact one-time physical-edge cancellation; original variance payment not spent twice.','geometric_dependencies':'Original normalized center triangulation, general /6 disk isoperimetry and inherited /5 for at most one strictdegree5; two nonadjacent boundary-ear deletion preserves strict original stars. Arithmetic and Fraction/CAS are executable; analytic planar arguments remain reviewed prose rather than formal kernel.','global_bound_improved':False,'pending_other_B':['B>=36'],'bindings':{p.relative_to(ROOT).as_posix():sha(p) for p in [Path(__file__),*paths]}},indent=2)+'\n',encoding='utf-8');print('B35 COMPLETE PASS independent lowM59values/high16models; tailpending',flush=True)
if __name__=='__main__':main()
