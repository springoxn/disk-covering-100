"""Independent integer/rational replay of cap-area branch certificate."""
from pathlib import Path
from fractions import Fraction as F
from math import isqrt
import json,hashlib
R=Path(__file__).resolve().parents[1]
def need(x,m):
    if not x:raise ValueError(m)
def atan(q,n):
    x=F(1,q);return sum((-1)**j*x**(2*j+1)/(2*j+1) for j in range(n))
def sqrt_upper(x):
    S=10**20;n=isqrt((x.numerator*S*S)//x.denominator);u=F(n+1,S);need(u*u>x,'sqrt upper');return u
def cap(r,d):return F(4,3)*sqrt_upper(2*r*d**3)
if __name__=='__main__':
    p=R/'verify/out/n100-boundary-cap-area-branch.json';z=json.loads(p.read_text(encoding='utf-8'));need(hashlib.sha256((R/'verify/n100_boundary_cap_area_branch.py').read_bytes()).hexdigest()==z['checker_sha256'],'script binding')
    pi=(16*atan(5,8)-4*atan(239,7),16*atan(5,7)-4*atan(239,8));need(pi[0]<pi[1] and pi[0]>F(314159,100000) and pi[1]<F(314160,100000),'pi')
    r=F(23,200);d=F(1,125);C=cap(r,d);margin=pi[0]*(1-2*r+d)**2-45*pi[1]*r*r-55*C;need(margin>0,'main margin');need(str(C)==z['main_certificate']['one_boundary_disk_cap_area_upper'],'cap agreement');need(str(margin)==z['main_certificate']['area_deficit_lower'],'margin agreement')
    # Endpoint control: same rigorous upper cap cannot exclude at U with this bound.
    U=F(1154469548855829,10**16);Cu=cap(U,d);marginU=pi[0]*(1-2*U+d)**2-45*pi[1]*U*U-55*Cu;need(marginU<=0,'endpoint control')
    # Ensure the old zero-penetration area comparison is indeed inconclusive at r=23/200.
    need((1-2*r)**2<45*r*r,'old bound inconclusive')
    bad=[]
    for label in ('understated_cap','wrong_saved_margin','wrong_pi_binding'):
        try:
            if label=='understated_cap':need((C/2)**2>=F(16,9)*2*r*d**3,'cap does not upper-bound integral')
            elif label=='wrong_saved_margin':need(margin+1==F(z['main_certificate']['area_deficit_lower']),'saved margin mismatch')
            else:need(F(3)==F(z['pi_interval'][0]),'pi bound mismatch')
        except ValueError:bad.append(label)
    need(len(bad)==3,'controls')
    out=R/'verify/out/n100-boundary-cap-area-independent.json';need(not out.exists(),'overwrite');out.write_text(json.dumps({'verified':True,'pi_interval':list(map(str,pi)),'cap_upper':str(C),'main_margin':str(margin),'endpoint_margin_upper_bound':str(marginU),'old_zero_penetration_inconclusive':True,'rejected_controls':bad,'method':'independent alternating sums, integer sqrt ceiling and rational area arithmetic','scope':'independent replay of k=55 branch at r<=23/200; no full count-branch enumeration or global optimality','input_sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'checker_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'global_optimality':False,'minimal_polynomial_obtained':False},indent=2)+'\n',encoding='utf-8');print('PASS independent cap-area margin and endpoint control;old bound inconclusive;3 controls rejected')
