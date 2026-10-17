"""Specialized8 discovery with independently adjustable halfside multiplier K.
Profiles have no p3 so no hinge charge is used in this new row.
"""
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];path=ROOT/'tools/n100_B32_M25_specialized_discover.py';text=path.read_text(encoding='utf-8');rules=[('a,b,eps,tau=map(float,p)','a,b,eps,tau,K=map(float,p)'),("ns['a']=a;ns['b']=b;ns['labels']=[-a,-b,0.];return kernel([eps,tau],full)","ns['a']=a;ns['b']=b;ns['labels']=[-a,-b,0.];ns['K']=K;ns['C0']=ns['conjugate'](0.);result=kernel([eps,tau],full)\n if not full and result==100.:return 1e6\n return result"),("/10**12,.5,1.3];base=objective", "/10**12,.5,1.3,.44];base=objective"),("(.2,.7),(1.15,1.309017)]","(.2,.7),(1.15,1.309017),(.25,.6)]"),("candidate.update(radius='2831/25000',epsilon=","candidate.update(radius='2831/25000',halfside_multiplier=[p[4].numerator,p[4].denominator],epsilon="),("+.44*RAD*s*(math.cos(mu)-h)","+float(p[4])*RAD*s*(math.cos(mu)-h)"),("B32-M25-specialized-discovery-144","B32-M25-specialized-K-discovery-145"),("SPECIALIZED DISCOVERY8","SPECIALIZED K DISCOVERY8")]
for old,new in rules:assert text.count(old)==1,(old,text.count(old));text=text.replace(old,new)
exec(compile(text,str(Path(__file__).resolve()),'exec'),{'__file__':str(Path(__file__).resolve()),'__name__':'__main__'})
