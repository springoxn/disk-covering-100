"""Independent obstruction check by clearing denominators, no Fraction import."""
from pathlib import Path
import json,hashlib
R=Path(__file__).resolve().parents[1]
p=R/'verify/out/n100-witness-dual-obstruction.json';z=json.loads(p.read_text(encoding='utf-8'))
def rat(s):
    a,sep,b=s.partition('/');return int(a),int(b) if sep else 1
def need(ok):
    if not ok:raise ValueError('independent rational comparison')
rows=[]
for key,ck in [('lower_radius','dual_weight_upper_at_lower'),('upper_radius','dual_weight_upper_at_upper')]:
    a,b=rat(z[key]);u,v=rat(z[ck]);need(a>0 and b>0 and 9*a>b)
    need(u*a*a==v*(a+b)*(a+b))
    margin=100*a*a-(a+b)*(a+b);need(margin>0)
    need(margin==(9*a-b)*(11*a+b))
    rows.append({'radius':z[key],'cleared_strict_margin':str(margin),'critical_comparison':'9*numerator > denominator'})
# A finite-sum integration identity can be checked termwise without a limiting argument.
# All masses are nonnegative; serving-center sets each have exactly pi*r² area.
need(100*1-(1+9)**2==0)
need(100*1-(1+10)**2<0)
need(hashlib.sha256((R/'verify/n100_uniform_area_dual_limit.py').read_bytes()).hexdigest()==z['script_sha256'])
out=R/'verify/out/n100-witness-dual-obstruction-independent.json';need(not out.exists())
out.write_text(json.dumps({'verified':True,'rows':rows,'method':'integer denominator clearing and factored strict gaps',
    'scope':'independent endpoint arithmetic; analytic area-average proof is stated in report, not formalized',
    'input_sha256':hashlib.sha256(p.read_bytes()).hexdigest(),
    'checker_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()},indent=2)+'\n',encoding='utf-8')
print('PASS independent integer arithmetic, both strict endpoint gaps, critical/subcritical controls')
