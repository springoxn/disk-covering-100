"""Discovery jointly synchronizes K with the true numeric hinge support.
All floating sampled supports remain discovery-only; exact replay mandatory.
"""
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];source=ROOT/'tools/n100_B33_high_row_discover.py';text=source.read_text(encoding='utf-8');needle='def evaluate(params,full=False):';helper='''def slope_for_K(K):
 mu=math.pi/33;rr=R*R;sm=math.sin(mu);cm=math.cos(mu);hm=math.sqrt(rr-sm*sm);bt=rr*K*(hm*cm+sm*sm)/R;ar=math.asin(R)
 def outer(t):
  s=math.sin(t);c=math.cos(t);h=math.sqrt(rr-s*s);return s*h+t-s*c+bt*(math.asin(s/R)-t),c*(rr-2*s*s)/h+2*s*s+bt*(c/h-1)
 fm,dm=outer(mu)
 def ratio(t):
  u=math.sin(t)/R;a=math.asin(u);Z=(math.pi/2-ar+t-a)/2
  def der(z):return K*math.cos(z)-u*math.sin(2*z+a)
  if der(Z)>=0:z=Z
  elif der(0)<=0:z=0
  else:z=brentq(der,0,Z,xtol=1e-12)
  penalty=2*rr*math.sin(z)*(K-u*math.sin(z+a));ft,_=outer(t);gap=fm+dm*(t-mu)-ft-penalty;return gap/(T-t)
 grid=np.linspace(0,T-1e-6,33);values=[ratio(float(t)) for t in grid];j=int(np.argmin(values));lo=float(grid[max(0,j-1)]);hi=float(grid[min(len(grid)-1,j+1)]);ref=minimize_scalar(ratio,bounds=(lo,hi),method='bounded');raw=min(min(values),float(ref.fun));return max(0,math.floor(.995*raw*10**8)/10**8)

def evaluate(params,full=False):''';assert text.count(needle)==1;text=text.replace(needle,helper);old='from scipy.optimize import linprog,differential_evolution,minimize';new='from scipy.optimize import linprog,differential_evolution,minimize,minimize_scalar,brentq';assert text.count(old)==1;text=text.replace(old,new);old='support.K=K;C0=support.conjugate(0.);rows=[];rhs=[];faces=[]';new='C=slope_for_K(K)\n if C<=0:return None if full else 1e9\n support.K=K;C0=support.conjugate(0.);rows=[];rhs=[];faces=[]';assert text.count(old)==1;text=text.replace(old,new);old="'parameters':[a,b,c,K]}";new="'parameters':[a,b,c,K],'hinge_slope':C}";assert text.count(old)==1;text=text.replace(old,new);old="candidate['radius']='2831/25000';candidate['halfside_multiplier']";new="candidate['radius']='2831/25000';cc=F(round(best['hinge_slope']*10**8),10**8);candidate['hinge_slope']=[cc.numerator,cc.denominator];candidate['hinge_zero']=[23,250];candidate['halfside_multiplier']";assert text.count(old)==1;text=text.replace(old,new);text=text.replace('B33-high-row-discovery-154','B33-high-row-discovery-156');old="'hinge_slope':str(F(3,100))";assert text.count(old)==1;text=text.replace(old,"'hinge_slope':str(cc)");old="'K',params[3],'baseline reoptimized'";assert text.count(old)==1;text=text.replace(old,"'K',params[3],'slope',cc,'baseline reoptimized'");exec(compile(text,str(Path(__file__).resolve()),'exec'),{'__file__':str(Path(__file__).resolve()),'__name__':'__main__'})
