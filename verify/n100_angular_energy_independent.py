"""Independent interval evaluation of a true angular-Hessian negative witness.
No NumPy, no eigensolver, no imports from the witness generator.
"""
from pathlib import Path
from fractions import Fraction as F
import json,hashlib,copy
ROOT=Path(__file__).resolve().parents[1]
CBASE=ROOT/'runtime/n100-vonequinox-transfer'
SRC=ROOT/'runtime/external-disk100-strict-local-replay/source'
def h(p):return hashlib.sha256(p.read_bytes()).hexdigest()
c=json.loads((CBASE/'certificate.json').read_text());wpath=ROOT/'verify/out/n100-angular-energy-negative-witness.json';w=json.loads(wpath.read_text());m=json.loads((SRC/'rational_midpoint.json').read_text());k=json.loads((SRC/'krawczyk_verification.json').read_text());binding=json.loads((SRC.parent/'SOURCE_BINDING.json').read_text())
assert c['generator_sha256']==h(CBASE/'analysis.py')
for f,d in binding['files'].items():assert h(SRC/f)==d
assert k['verified'] and k['box_radius']==[1,10**58] and k['midpoint_denominator']==10**60
D=int(m['denominator']);radius=F(100,D);gamma=F(c['Gamma']);nums=m['numerators'];order=c['anchor_order'];N=len(order)
assert N==32 and sorted(order)==list(range(32))
def add(a,b):return (a[0]+b[0],a[1]+b[1])
def mul(a,b):
 v=[x*y for x in a for y in b];return min(v),max(v)
def neg(a):return -a[1],-a[0]
def coord(i,d):
 v=F(int(nums[428+2*i+d]),D);return v-radius,v+radius
q=[[coord(i,d) for d in (0,1)] for i in range(N)]
def dot(i,j):return add(mul(q[i][0],q[j][0]),mul(q[i][1],q[j][1]))
def cross(i,j):return add(mul(q[i][0],q[j][1]),neg(mul(q[i][1],q[j][0])))
# Root is interior of the convex angular domain: consecutive gaps in (0,delta).
# Unit-circle root identities are supplied by the bound KKT verification; cross>0
# selects the short positively oriented arc and dot>1-2t makes it <2asin(r).
tlo=F(int(nums[492])-100,D);threshold=(1-2*tlo,1-2*(tlo+2*radius))
margin_dot=[];margin_cross=[]
for a,b in zip(order,order[1:]+order[:1]):
 cr=cross(a,b)[0];ma=dot(a,b)[0]-threshold[0]
 assert cr>0 and ma>0
 margin_cross.append(cr);margin_dot.append(ma)
def evaluate(witness):
 v=[F(x) for x in witness];assert len(v)==N and v[0]==0
 total=(F(0),F(0))
 for key,raw in c['c0_lower_triangle'].items():
  i,j=map(int,key.split(','));c0=F(raw)
  ci=(max(F(0),c0-gamma),c0+gamma);assert ci[1]>=ci[0]
  term=mul(ci,dot(i,j));factor=2*(v[i]-v[j])**2
  total=add(total,(factor*term[0],factor*term[1]))
 return total
iv=evaluate(w['witness']);assert iv[1]<0
rejected=[]
for name,v in [('zero_vector',['0']*N),('constant_gauge_vector',['1']*N)]:
 try:
  got=evaluate(v);assert got[1]<0
 except AssertionError:rejected.append(name)
assert len(rejected)==2
out={'schema':'n100-angular-energy-independent/v1','verified':True,'interval_quadratic_form':[str(x) for x in iv],'strictly_negative':True,'rational_upper_less_than_minus_1e5':iv[1]<-F(1,100000),'root_is_interior_of_angular_domain':True,'min_consecutive_cross_lower':str(min(margin_cross)),'min_consecutive_dot_above_cosdelta':str(min(margin_dot)),'angle_domain_claim':'all root gaps strictly between 0 and 2asin(r_root); whole winding/order are inherited from bound coverage topology','negative_controls_rejected':rejected,'inputs':{str(p.relative_to(ROOT)).replace('\\','/'):h(p) for p in [CBASE/'certificate.json',SRC/'rational_midpoint.json',SRC/'krawczyk_verification.json',wpath]},'checker_sha256':h(Path(__file__)),'scope':'true harmonic-extension stress energy fails convexity at root in candidate angle domain; not a feasible covering counterexample; constrained SOSC remains valid','global_optimality_proved':False}
p=ROOT/'verify/out/n100-angular-energy-independent.json'
if p.exists():raise FileExistsError(p)
p.write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8')
print('PASS exact interval negative true-energy Hessian; upper < -1/100000:',out['rational_upper_less_than_minus_1e5'],'strict arc interior:',True,'negative controls:',len(rejected))
