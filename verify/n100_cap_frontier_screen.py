"""Rational cap-area screening; no identification of k with diagram B is asserted.
Run: python verify/n100_cap_frontier_screen.py
"""
from pathlib import Path
from fractions import Fraction as F
from math import isqrt
import json, hashlib
ROOT = Path(__file__).resolve().parents[1]
U = F(1154469548855829, 10**16)
PLO, PHI = F(314159, 100000), F(314160, 100000)
def require(ok, message):
    if not ok:
        raise ValueError(message)
def sqrt_upper(x):
    scale = 10**24
    z = isqrt(x.numerator * scale**2 // x.denominator)
    upper = F(z + 1, scale)
    require(upper**2 > x, 'invalid square-root bound')
    return upper
def score(m, k, delta):
    s = 1 - 2*U + delta
    cap = F(4,3)*sqrt_upper(2*U*delta**3)
    return PLO*s*s - (m-k)*PHI*U*U - k*cap

def main():
    # Machin's formula, four-term lower and three-term upper alternating sums.
    def atan(q, n):
        return sum(((-1)**j * F(1, q)**(2*j+1)/(2*j+1) for j in range(n)), F(0))
    require(16*atan(5,8)-4*atan(239,7)>PLO, 'pi lower')
    require(16*atan(5,7)-4*atan(239,8)<PHI, 'pi upper')
    source = ROOT/'verify/out/n100-vonequinox-count-domain-bound.json'
    families = json.loads(source.read_text(encoding='utf-8'))['surviving_m_B_families']
    grid = [F(j,10000) for j in range(1, int(2*U*10000))]
    # Values are illustrative under k=B, not an accepted geometric bridge.
    caps = [(d, F(4,3)*sqrt_upper(2*U*d**3)) for d in grid]
    rows=[]
    for m,b in families:
        best,d = max((PLO*(1-2*U+d)**2-(m-b)*PHI*U*U-b*c,d) for d,c in caps)
        rows.append({'m':m,'B':b,'hypothetical_k':b,'best_delta':str(d),'best_margin':str(best),'positive':best>0})
    require(len(rows)==87 and not any(x['positive'] for x in rows), 'unexpected screening result')
    delta=F(41,5000)
    margin=score(100,56,delta)
    require(margin>0, 'k56 branch failed')
    cap=F(4,3)*sqrt_upper(2*U*delta**3)
    gain=PHI*U*U-cap
    require(gain>0, 'count monotonicity')
    # Independent integer inequalities for the cap rounding and final gap.
    require(cap**2>F(32,9)*U*delta**3, 'integral upper bound')
    require(PLO*(1-2*U+delta)**2>44*PHI*U*U+56*cap, 'independent area check')
    rejected=[]
    for label, value in [('understated_cap', cap/2), ('negative_cap', -cap)]:
        try:
            require(value>0 and value**2>=F(32,9)*U*delta**3, 'bad cap')
        except ValueError:
            rejected.append(label)
    require(len(rejected)==2, 'negative controls')
    result={'schema':'n100-cap-frontier-screen/v1','arithmetic':'integer/Fraction only',
        'radius_upper':str(U),'pi_bracket':[str(PLO),str(PHI)],
        'universal_serving_count_exclusion':{'m_upper':100,'k_lower':56,'delta':str(delta),'cap_upper':str(cap),'positive_margin':str(margin),'gain_per_extra_serving_disk':str(gain)},
        'hypothetical_k_equals_B_grid_screen':rows,'grid_denominator':10000,'grid_size':len(grid),
        'grid_screen_is_not_continuous_domain_exclusion':True,'k_equals_B_bridge_accepted':False,
        'new_m_B_families_excluded':0,'negative_controls_rejected':rejected,
        'analytic_dependencies':['Machin identity and alternating series','circle-serving center norm >= 1-r','inner-target intersection is contained in cap of penetration delta','cap integral <= (4/3)sqrt(2r delta^3)','area subadditivity','radius monotonicity: enlarge all disks to U before service classification'],
        'machine_verified_geometry':False,'global_optimality':False,'minimal_polynomial_obtained':False,
        'input_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
    out=ROOT/'verify/out/n100-cap-frontier-screen.json'
    require(not out.exists(),'refuse overwrite')
    out.write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print('PASS exact k>=56 exclusion at U; 87 hypothetical k=B families have no positive sampled margin; no new count families excluded')
if __name__=='__main__':
    main()
