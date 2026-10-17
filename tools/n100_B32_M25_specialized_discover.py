"""Discover a dedicated coherent row for the8 failing M25 profiles only."""
from pathlib import Path
from fractions import Fraction as F
import sys,json,copy,math,hashlib
from scipy.optimize import differential_evolution,minimize
ROOT=Path(__file__).resolve().parents[1];source=ROOT/'tools/n100_B32_M25_coherent_discover.py';W=ROOT/'runtime/disk100-release-lf-67ebf1c/certified_bounds_11323/working';sys.path.insert(0,str(W))
from verify_jensen_slab_ear_support import cap
from verify_star_lp_duals import S
z=cap(F(11324,100000),F(11,25));EAR=float(F(z.u,S));ns={'__file__':str(source),'__name__':'specialized_discovery_kernel','EAR':EAR};text=source.read_text(encoding='utf-8').split('def main():')[0];rules=[('e*1.332634','e*EAR'),('for e,degrees in [(0,[7,7]),(0,[8]),(1,[7]),(2,[])]:','for e,degrees in [(0,[7,7])]: '),('for ps in itertools.product(range(4),repeat=high):','for ps in itertools.product((0,2),repeat=high):'),('if k>high:continue','if k>high or si not in (2,3):continue'),('bounds=(.00001,w-a-.00001)','bounds=(-.9*w,w-a-.00001)')]
for old,new in rules:assert text.count(old)==1;text=text.replace(old,new)
exec(compile(text,str(source),'exec'),ns);kernel=ns['evaluate']
def objective(p,full=False):
 a,b,eps,tau=map(float,p)
 if a<=0 or b<=0 or b>=.9 or eps<=0 or eps>=.85 or tau<=0:return None if full else 1000.
 ns['a']=a;ns['b']=b;ns['labels']=[-a,-b,0.];return kernel([eps,tau],full)
def main():
 original=[-ns['DATA']['labels'][0]/10**12,-ns['DATA']['labels'][1]/10**12,.5,1.3];base=objective(original,True);opt=differential_evolution(objective,[(.12,.5),(.12,.5),(.2,.7),(1.15,1.309017)],seed=144,popsize=6,maxiter=55,tol=1e-9,polish=False,workers=1);ref=minimize(objective,opt.x,method='Nelder-Mead',options={'maxiter':800,'fatol':1e-10,'xatol':1e-9});p=ref.x if ref.fun<opt.fun else opt.x;p=[F(float(v)).limit_denominator(10**6) for v in p];best=objective(list(map(float,p)),True);assert best;D=10**12;v=best['variables'];candidate=copy.deepcopy(ns['DATA']);candidate.update(radius='2831/25000',epsilon=[p[2].numerator,p[2].denominator],perimeter_penalty=[p[3].numerator,p[3].denominator],labels=[-round(float(p[0])*D),-round(float(p[1])*D),0],charges=[round(x*D) for x in v[:3]],outside_allowances=[round(x*D) for x in v[3:5]],interface_H=round(v[5]*D),face_rows=best['face_rows'],outside_rows=best['outside_rows'],stars=best['stars']);RAD=.11324;mu=math.pi/32;s=math.sin(mu);h=math.sqrt(RAD*RAD-s*s);outer=32*(s*h+mu-s*math.cos(mu)+.44*RAD*s*(math.cos(mu)-h));margin=lambda r:math.pi-RAD*RAD*r['normalized_worst_center']-outer;folder=ROOT/'runtime/B32-M25-specialized-discovery-144';assert not folder.exists();folder.mkdir(parents=True);(folder/'proposal.json').write_text(json.dumps(candidate,indent=2)+'\n',encoding='utf-8');(folder/'receipt.json').write_text(json.dumps({'discovery_only':True,'exact_acceptance':False,'profile_domain':'e0;degrees7,7;marked0/2 each;star2/3:8 cases','parameters':list(map(str,p)),'numeric_area_margin':margin(best),'baseline_numeric_area_margin':margin(base),'best':best,'evaluations':int(opt.nfev)+int(ref.nfev),'slope':'1189/20000','bindings':{str(t.relative_to(ROOT)):hashlib.sha256(t.read_bytes()).hexdigest() for t in (Path(__file__),source)}},indent=2)+'\n',encoding='utf-8');print('SPECIALIZED DISCOVERY8',margin(best),'baseline',margin(base),'parameters',list(map(str,p)),flush=True)
if __name__=='__main__':main()
