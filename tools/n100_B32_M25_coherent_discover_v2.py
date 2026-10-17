"""Second M25 discovery: actual ear cap and jointly variable high/boundary potentials.
Previous discovery artifacts remain untouched. No mathematical acceptance.
"""
from pathlib import Path
from fractions import Fraction as F
import sys,json,copy,math,hashlib
from scipy.optimize import differential_evolution,minimize
ROOT=Path(__file__).resolve().parents[1];source=ROOT/'tools/n100_B32_M25_coherent_discover.py';W=ROOT/'runtime/disk100-release-lf-67ebf1c/certified_bounds_11323/working';sys.path.insert(0,str(W))
from verify_jensen_slab_ear_support import cap
from verify_star_lp_duals import S
z=cap(F(11324,100000),F(11,25));EAR=float(F(z.u,S));namespace={'__file__':str(source),'__name__':'discovery_kernel'};text=source.read_text(encoding='utf-8');assert text.count('e*1.332634')==1;text=text.split('def main():')[0].replace('e*1.332634','e*EAR');namespace['EAR']=EAR;exec(compile(text,str(source),'exec'),namespace);kernel=namespace['evaluate']
def objective(p,full=False):
 a,b,eps,tau=map(float,p);namespace['a']=a;namespace['b']=b;namespace['labels']=[-a,-b,0.];return kernel([eps,tau],full)
def main():
 initial=[-namespace['DATA']['labels'][0]/10**12,-namespace['DATA']['labels'][1]/10**12,.5,1.3];baseline=objective(initial,True);opt=differential_evolution(objective,[(.15,.36),(.14,.4),(.3,.65),(1.27,1.3090169)],seed=1422,popsize=7,maxiter=55,tol=1e-9,polish=False,workers=1);ref=minimize(objective,opt.x,method='Nelder-Mead',options={'maxiter':650,'fatol':1e-10,'xatol':1e-9});p=ref.x if ref.fun<=opt.fun else opt.x;p=[F(float(x)).limit_denominator(100000) for x in p];best=objective(list(map(float,p)),True);assert best;DATA=namespace['DATA'];D=10**12;variables=best['variables'];candidate=copy.deepcopy(DATA);candidate.update(radius='2831/25000',epsilon=[p[2].numerator,p[2].denominator],perimeter_penalty=[p[3].numerator,p[3].denominator],labels=[-round(float(p[0])*D),-round(float(p[1])*D),0],charges=[round(x*D) for x in variables[:3]],outside_allowances=[round(x*D) for x in variables[3:5]],interface_H=round(variables[5]*D),face_rows=best['face_rows'],outside_rows=best['outside_rows'],stars=best['stars']);RAD=.11324;mu=math.pi/32;s=math.sin(mu);h=math.sqrt(RAD*RAD-s*s);outer=32*(s*h+mu-s*math.cos(mu)+.44*RAD*s*(math.cos(mu)-h));margin=lambda z:math.pi-RAD*RAD*z['normalized_worst_center']-outer;folder=ROOT/'runtime/B32-M25-coherent-discovery-v2-142';assert not folder.exists();folder.mkdir(parents=True);(folder/'proposal.json').write_text(json.dumps(candidate,indent=2)+'\n',encoding='utf-8');(folder/'receipt.json').write_text(json.dumps({'discovery_only':True,'exact_acceptance':False,'parameters':list(map(str,p)),'numeric_area_margin':margin(best),'baseline_numeric_area_margin':margin(baseline),'actual_ear_upper_exact':str(F(z.u,S)),'best':best,'function_evaluations':int(opt.nfev)+int(ref.nfev),'slope':'1189/20000','bindings':{str(t.relative_to(ROOT)):hashlib.sha256(t.read_bytes()).hexdigest() for t in (Path(__file__),source)}},indent=2)+'\n',encoding='utf-8');print('DISCOVERY-V2 minimum margin',margin(best),'baseline',margin(baseline),'parameters',list(map(str,p)),flush=True)
if __name__=='__main__':main()
