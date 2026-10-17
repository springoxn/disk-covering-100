"""Independent squared-inequality audit of rational arc/cap supports."""
from pathlib import Path
from fractions import Fraction as F
import json,hashlib,argparse
ROOT=Path(__file__).resolve().parents[1]
def require(ok,msg):
    if not ok:raise ValueError(msg)
def audit(z):
    r=F(z['radius']);delta=F(z['delta']);a=F(z['slope']);M=F(z['maximum_half_arc_upper']);c=r/M;C2=1-r*r
    require(0<c and c*c<=C2,'norm bound');last=F(0);minimum=None
    for row in z['steps']:
        lo,hi=F(row['u_lower']),F(row['u_upper']);require(lo==last and lo<hi<=delta,'partition');last=hi
        d=1-r+hi;co=(C2+d*d)/(2*d);p=F(row['arc_half_upper']);cap=F(row['cap_upper']);depth=delta-lo;factor=F(4,3)-depth/(5*r)
        require(0<co<=1 and d*d<C2,'arc monotonicity domain')
        require(p>=0 and p*p*c*c>=1-co*co,'arc bound')
        require(factor>0 and cap>0 and cap*cap>=2*r*depth**3*factor**2,'cap bound')
        gap=a*(M-p)-cap;require(gap>0 and gap==F(row['gap']),'support')
        minimum=gap if minimum is None else min(minimum,gap)
    require(last==delta,'missing tail')
    # Deliberately use coarser independent pi bounds; ensure the conclusion survives.
    pl,ph=F(314159,100000),F(314160,100000)
    # Certified pi via independent alternating atan computation.
    def alt(q,count):return sum((F((-1)**j,(2*j+1)*q**(2*j+1)) for j in range(count)),F(0))
    require(pl<16*alt(5,10)-4*alt(239,9) and ph>16*alt(5,9)-4*alt(239,10),'pi')
    margin=pl*(1-2*r+delta)**2-45*ph*r*r-a*(55*M-pl)
    require(margin>0 and ph*r*r>a*M,'strict area gap')
    require(margin==F(z['k55_area_margin_lower']),'margin')
    return {'verified':True,'segments':len(z['steps']),'minimum_support_gap':str(minimum),'area_margin_lower':str(margin)}
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--out',default='verify/out/n100-arc-cap-independent.json');args=ap.parse_args()
    p=ROOT/'verify/out/n100-arc-cap-rational-support.json';z=json.loads(p.read_text(encoding='utf-8'))
    require(hashlib.sha256((ROOT/'verify/n100_arc_cap_rational_support.py').read_bytes()).hexdigest()==z['script_sha256'],'binding')
    result=audit(z);import copy
    rejected=[]
    for label,change in [('understated_cap',lambda q:q['steps'][0].__setitem__('cap_upper','0')),('partition_gap',lambda q:q['steps'].pop(0)),('false_arc_upper',lambda q:q['steps'][100].__setitem__('arc_half_upper','0'))]:
        q=copy.deepcopy(z);change(q)
        try:audit(q)
        except ValueError:rejected.append(label)
    require(len(rejected)==3,'controls')
    out=ROOT/args.out;require(not out.exists(),'overwrite');out.write_text(json.dumps({'schema':'n100-arc-cap-independent/v1','result':result,'rejected_controls':rejected,'method':'squared rational inequalities and independent partition/area computation; imports no primary geometry functions','input_sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'analytic_dependencies_not_formalized':z['analytic_dependencies'],'machine_verified_geometry':False,'global_optimality':False,'count_families_excluded':0},indent=2)+'\n',encoding='utf-8');print('PASS independent arc-cap:',result['segments'],'segments, positive area margin; 3 corruptions rejected')
if __name__=='__main__':main()
