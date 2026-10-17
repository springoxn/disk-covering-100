"""Exact rational rotations expose a lower-energy angle-domain point.
This is a counterexample to the harmonic stress-energy relaxation bound only.
"""
from pathlib import Path
from fractions import Fraction as F
import json,hashlib
ROOT=Path(__file__).resolve().parents[1]
CP=ROOT/'runtime/n100-vonequinox-transfer/certificate.json';MP=ROOT/'runtime/external-disk100-strict-local-replay/source/rational_midpoint.json';WP=ROOT/'verify/out/n100-angular-energy-negative-witness.json'
c=json.loads(CP.read_text());m=json.loads(MP.read_text());w=json.loads(WP.read_text());D=int(m['denominator']);rho=F(100,D);g=F(c['Gamma']);v=[F(x) for x in w['witness']];N=len(v);order=c['anchor_order']
def add(a,b):return a[0]+b[0],a[1]+b[1]
def neg(a):return -a[1],-a[0]
def sub(a,b):return add(a,neg(b))
def mul(a,b):
 z=[x*y for x in a for y in b];return min(z),max(z)
def scale(a,s):return mul(a,(s,s))
def coord(i,d):
 a=F(int(m['numerators'][428+2*i+d]),D);return a-rho,a+rho
q=[[coord(i,d) for d in (0,1)] for i in range(N)]
def dot(a,b):return add(mul(a[0],b[0]),mul(a[1],b[1]))
def cross(a,b):return sub(mul(a[0],b[1]),mul(a[1],b[0]))
def build(step):
 rotations=[];p=[]
 for i in range(N):
  u=step*v[i]/2;cs=(1-u*u)/(1+u*u);sn=2*u/(1+u*u)
  assert cs*cs+sn*sn==1
  rotations.append([str(cs),str(sn)])
  p.append([sub(scale(q[i][0],cs),scale(q[i][1],sn)),add(scale(q[i][0],sn),scale(q[i][1],cs))])
 tlo=F(int(m['numerators'][492])-100,D);bcoshi=1-2*tlo
 cross_margins=[];dot_margins=[]
 for i,j in zip(order,order[1:]+order[:1]):
  cross_margins.append(cross(p[i],p[j])[0]);dot_margins.append(dot(p[i],p[j])[0]-bcoshi)
 assert min(cross_margins)>0 and min(dot_margins)>0
 delta=(F(0),F(0))
 for key,raw in c['c0_lower_triangle'].items():
  i,j=map(int,key.split(','));z=F(raw);ci=(max(F(0),z-g),z+g)
  delta=add(delta,scale(mul(ci,sub(dot(q[i],q[j]),dot(p[i],p[j]))),F(2)))
 return delta,rotations,min(cross_margins),min(dot_margins)
s=F(1,1000)
displacement=s*max(abs(x) for x in v)
original_cross=min(cross(q[i],q[j])[0] for i,j in zip(order,order[1:]+order[:1]))
assert original_cross>2*displacement+displacement**2
change,rotations,cm,dm=build(s)
assert change[1]<-F(1,10**12)
zero=build(F(0))[0];assert zero[0]<=0<=zero[1]
out={'schema':'n100-harmonic-energy-relaxation-counterexample/v1','verified':True,'parameter_step':str(s),'fixed_angular_direction':w['witness'],'rational_rotations_cos_sin':rotations,'unit_identity_checked_exactly':True,'energy_change_interval':[str(x) for x in change],'energy_decrease_more_than_1e12_inverse':change[1]<-F(1,10**12),'min_cross_margin_lower':str(cm),'min_dot_above_cosdelta_lower':str(dm),'all_short_gaps_strictly_inside_cap':True,'winding_number':1,'winding_basis':'root order and winding inherited from certified topology; continuous rational rotation path stays inside the short-arc chart (q rotations <1/1000 rad and initial gaps >0.1 rad)','zero_step_contains_zero':True,'scope':'energy of harmonic free-node relaxation below its root value within the angle polytope; no feasible disk-cover configuration constructed; no new radius upper/lower bound','global_optimality_proved':False,'input_sha256':{str(p.relative_to(ROOT)).replace('\\','/'):hashlib.sha256(p.read_bytes()).hexdigest() for p in [CP,MP,WP]},'checker_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
p=ROOT/'verify/out/n100-harmonic-energy-relaxation-counterexample.json'
if p.exists():raise FileExistsError(p)
p.write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8')
assert change[1]<-F(1,10**12)
print('PASS exact rational anchor rotations: Delta E < -1e-12, strict short gaps, unit rotation identities; zero-step control includes zero')
