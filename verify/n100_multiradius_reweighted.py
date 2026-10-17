"""Reweight certified actual radial profiles to satisfy both arcs and all tested areas."""
from pathlib import Path
from fractions import Fraction as F
from math import comb
import json,hashlib
ROOT=Path(__file__).resolve().parents[1]
def need(x,m):
 if not x:raise ValueError(m)
def main():
 path=ROOT/'verify/out/n100-multiradius-capacity.json';z=json.loads(path.read_text(encoding='utf-8'));r=F(z['radius']);pl,ph=map(F,z['pi_interval']);types={t['kind']:t for t in z['types']};counts={'near':33,'tail':21};arc=F(0);arcproof=[]
 for name,ty in types.items():
  d=F(ty['distance']);cos=(1-r*r+d*d)/(2*d);sin2=1-cos*cos;S=10**24
  # Recover the floor sqrt by exact integer comparisons through bisection.
  lo=0;hi=S
  while hi-lo>1:
   mid=(lo+hi)//2
   if mid*mid*sin2.denominator<=sin2.numerator*S*S:lo=mid
   else:hi=mid
  x=F(lo,S);lower=sum((F(comb(2*j,j),4**j*(2*j+1))*x**(2*j+1) for j in range(8)),F(0));need(lower==F(ty['half_arc_lower']),'independent binary sqrt and arc series');arc+=counts[name]*lower;arcproof.append({'type':name,'sqrt_lower':str(x),'count':counts[name],'half_arc_lower':str(lower)})
 need(arc>ph,'strict true arc surplus');rows=[]
 for p in z['profiles']:
  t=F(p['target_radius']);L=46*pl*min(t,r)**2;U=46*ph*min(t,r)**2
  for part in p['parts']:L+=counts[part['type']]*F(part['lower']);U+=counts[part['type']]*F(part['upper'])
  need(L>ph*t*t,'all reweighted capacity lower sums strict');rows.append({'target_radius':str(t),'capacity_lower':str(L),'target_area_upper':str(ph*t*t),'strict_surplus':str(L-ph*t*t)})
 out=ROOT/'verify/out/n100-multiradius-reweighted.json';need(not out.exists(),'overwrite');out.write_text(json.dumps({'schema':'n100-multiradius-reweighted/v1','verified_integer_radial_budget_witness':True,'counts':{'near':33,'tail':21,'central_nonserving':46},'arc_proof':arcproof,'arc_sum_lower':str(arc),'arc_surplus_over_pi_upper':str(arc-ph),'profiles':rows,'strict_capacity_passes':len(rows),'scope':'actual radial distances and rigorous per-disk intersection integrals, 100 selected target radii only; no angular positions, no union coverage, no full continuum of radii','global_optimality':False,'input_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()},indent=2)+'\n',encoding='utf-8');print('PASS reweighted actual radial witness 33+21+46','arc strictly certified','inner circles',len(rows))
if __name__=='__main__':main()
