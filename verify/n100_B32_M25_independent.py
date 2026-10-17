"""Independent Fraction interval composition for the complete81 M25 rows.
Shares analytic scalar support checkers; rederives area ledger without original verify.
"""
from pathlib import Path
from fractions import Fraction as F
import sys,json,hashlib,importlib.util,itertools
import sympy as sp
ROOT=Path(__file__).resolve().parents[1];P=ROOT/'runtime/disk100-release-lf-67ebf1c/certified_bounds_11323';W=P/'working';S=P/'lower_staging';sys.path[:0]=[str(ROOT/'verify'),str(S),str(W),str(W/'signed_edge_metric_20261004')]
from verify_star_lp_duals import q,S as SCALE,PI
from verify_potential_star_duals import sine,cosine
from exact_linear_halfside_marked_conjugate import conjugate
from exact_signed_sine_full_face_support import face_bound
from exact_range_one_face_support import face_bound as ordinary_bound
from polygon_star_perimeter_support import support
from verify_jensen_slab_ear_support import cap
from n100_B32_M25_specialized import key,universe
class I:
 def __init__(self,x,y=None):self.l=F(x);self.u=F(x if y is None else y);assert self.l<=self.u
 def __add__(self,o):o=o if isinstance(o,I) else I(o);return I(self.l+o.l,self.u+o.u)
 __radd__=__add__
 def __neg__(self):return I(-self.u,-self.l)
 def __sub__(self,o):return self+-asI(o)
 def __rsub__(self,o):return asI(o)+-self
 def __mul__(self,o):o=asI(o);vs=[x*y for x in (self.l,self.u) for y in (o.l,o.u)];return I(min(vs),max(vs))
 __rmul__=__mul__
 def __truediv__(self,o):o=asI(o);assert o.l*o.u>0;return self*I(1/o.u,1/o.l)
def asI(x):return x if isinstance(x,I) else I(x)
def iv(x):return I(F(x.l,SCALE),F(x.u,SCALE))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 proofpath=ROOT/'verify/out/n100-B32-M25-specialized-K-145.json';proof=json.loads(proofpath.read_text(encoding='utf-8'));assert proof['status']=='PASS' and proof['full_M25_closed'];radius=F(2831,25000);assert F(proof['radius'])==radius;total=universe();seen=set();records=[];minimum=None;A=iv(3*q(3).sqrt()/4);pi=iv(PI);ang=pi/3
 paths=[S/'B32_M25_direct_interface_0p11323_proposal.json',ROOT/'runtime/B32-M25-specialized-K-discovery-145/proposal.json']
 for run,path in zip(proof['runs'],paths):
  data=json.loads(path.read_text(encoding='utf-8'));den=data['denominator'];rat=lambda x:F(x,den);labels=list(map(rat,data['labels']));charges=list(map(rat,data['charges']));D=list(map(rat,data['outside_allowances']));a,b=-labels[0],-labels[1];K=F(*data['halfside_multiplier']);eps=F(*data['epsilon']);tau=F(*data['perimeter_penalty']);weight=1-eps;interface=rat(data['interface_H']);assert run['status']=='PASS' and F(run['K'])==K;assert 0<K<1 and 0<eps<1
  credit=lambda ids:interface*sum({ids[i],ids[(i+1)%3]}=={0,1} for i in range(3));slacks=[]
  assert len(data['face_rows'])==9 and len(data['outside_rows'])==18
  for row in data['face_rows']:
   ids=row['ids'];bound,_,_=face_bound([labels[i] for i in ids],[0,0,0],rat(row['nu']));gap=(A+sum(charges[i] for i in ids)-credit(ids)-iv(bound)).l;assert gap>0;slacks.append(gap)
  for row in data['outside_rows']:
   n=row['selected_edges'];ids=row['ids'];ts=[0,0,eps*tau] if n==1 else [eps*tau,0,eps*tau];bound,_,_=face_bound([labels[i] for i in ids],ts,rat(row['nu']));gap=(A+sum(charges[i] for i in ids)-credit(ids)+D[n-1]-iv(bound)).l;assert gap>0;slacks.append(gap)
  J=max((5-2*j)*D[0]+j*D[1] for j in range(3));stars=[]
  for st in data['stars']:
   y=rat(st['center_potential']);v=eps*iv(support(5,1,-tau))-y*ang
   for f in st['faces']:
    h=f['high_base_vertices'];ls=[y]+[-a]*h+[F(0)]*(2-h);normal=[x/weight for x in ls];assert max(normal)-min(normal)<1;bound,_,_=ordinary_bound(normal,rat(f['nu']));v+=st['counts'][h]*weight*iv(bound)
   stars.append(v)
  C0=iv(conjugate(K,F(0)));ear=iv(cap(radius,K));c_b=iv(conjugate(K,b));c_h=iv(conjugate(K,b-a));s=sine(PI/32);c=cosine(PI/32);root=(q(radius).sq()-s.sq()).sqrt();H=iv(s*root)+pi/32-iv(s*c);outer=32*(H+K*radius*iv(s)*(iv(c)-iv(root)));FAN=F(run['FAN']);scalar=run['result']['same_radius_boundary_scalar'];assert scalar['status']=='PASS' and F(scalar['radius'])==radius and F(scalar['halfside_multiplier'])==K and F(scalar['hinge_slope'])==F(run['hinge_slope']);assert F(scalar['required_center_norm_squared_upper'])==1-radius*radius
  for row in run['result']['rows']:
   kkey=key(row);assert kkey not in seen;seen.add(kkey);e,degrees,ps,si=kkey;high=len(degrees);ordinary=67-high;U=25+2*e;po=32-2*e-sum(ps);k=data['stars'][si]['high_neighbors']
   if run['label']=='newK8':assert all(p<3 for p in ps) and FAN==0 and F(run['hinge_slope'])==0
   interior=(134+e)*A+(32-2*e)*C0+e*ear+po*(c_b-C0)-b*((2-e)*pi+U*ang)
   for d,p in zip(degrees,ps):interior+=p*(c_h-C0)+a*(6-d+p)*ang-FAN*int(p==3)-2*interface*int(p>0)
   charge=(sum(d-p for d,p in zip(degrees,ps))-2*k)*charges[0]+U*charges[1]+(6*ordinary-po+5-(15-2*k))*charges[2];center=interior-5*A+stars[si]+J+charge;margin=pi-radius*radius*center-outer;assert margin.l>0;minimum=margin.l if minimum is None else min(minimum,margin.l);records.append({'profile':[e,list(degrees),list(ps),si],'row':run['label'],'independent_margin_lower':str(margin.l),'primary_margin_lower':row['area_margin_lower']})
 assert seen==total and len(records)==81
 # CAS verifies independent grouping of all variable endpoint/interface charges.
 dh,pm,k,oo,po,U,g0,g1,g2,t,J=sp.symbols('dh pm k oo po U g0 g1 g2 t J');left=(dh-pm-2*k)*g0+U*g1+(6*oo-po+5-(15-2*k))*g2+J;right=(dh-pm)*g0+U*g1+(6*oo-po)*g2+J-2*k*g0+(2*k-10)*g2;assert sp.expand(left-right)==0
 out=ROOT/'verify/out/n100-B32-M25-independent-146.json';assert not out.exists();out.write_text(json.dumps({'schema':'n100-M25-independent-fraction-ledger/v1','status':'PASS','radius':str(radius),'profiles':81,'profile_partition_complete':True,'all_independent_margin_lowers_positive':True,'minimum_margin_lower':str(minimum),'CAS_charge_regrouping_identity':0,'zero_hinge_spend_only_in_no_p3_domain_checked':True,'scope':'Independent rational interval recomposition and full local face/outside/star support replay, sharing upstream scalar primitives; geometric hypotheses inherited and not formalized','records':records,'full_B32_closed':False,'global_bound_improved':False,'bindings':{p.relative_to(ROOT).as_posix():sha(p) for p in [Path(__file__),proofpath,*paths]}},indent=2)+'\n',encoding='utf-8');print('INDEPENDENT PASS81 positive margins; minimum',float(minimum),'exact endpoint in receipt',flush=True)
if __name__=='__main__':main()
