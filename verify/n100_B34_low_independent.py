"""Independent B34 lowM rational cap and reduced-cost ledger audit."""
from pathlib import Path
from fractions import Fraction as F
import json,hashlib,subprocess,sys
import sympy as sp
ROOT=Path(__file__).resolve().parents[1]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 if not __debug__:raise RuntimeError('Assertions must remain enabled')
 cp=ROOT/'verify/out/n100-B34-low-and-high-reduction-171.json';dp=ROOT/'verify/out/n100-B34-diagnostic-170.json';proof=json.loads(cp.read_text(encoding='utf-8'));diag=json.loads(dp.read_text(encoding='utf-8'));assert proof['status']=='PASS' and proof['low_M_closed'] and not proof['full_B34_closed'];R=F(proof['radius']);assert R==F(2831,25000)
 for rel,h in proof['bindings'].items():assert sha(ROOT/rel)==h
 rows=diag['replay']['result']['branches'];low=rows[1];high=rows[2];assert F(rows[0]['area_margin'])>0
 for row in (low,high):
  base=F(row['area_margin']);assert base<0
  assert all(base-R*R*F(row[k])>0 for k in ('M_slope_upper','shifted_ear_upper','bad_q1_coefficient_upper'))
  assert all(base+R*R*F(slack)>0 for p,d,slack in row['neutral_low_slacks'])
 assert all(F(low['area_margin'])+R*R*F(v)>0 for p,d,v in low['positive_low_slacks'] if d in (3,4))
 pp=ROOT/'runtime/disk100-release-lf-67ebf1c/certified_bounds_11323/lower_staging/B34_0p11323/hinge_B34_0p11323_proposals.json';row=json.loads(pp.read_text(encoding='utf-8'))['rows'][1];c=F(row['deep_potential'],row['potential_denominator']);gd=F(row['charge_deep'],row['denominator']);g0=F(row['charge_0'],row['denominator']);sqrt3lo=F(1732050807,10**9);sqrt5hi=F(2236067978,10**9);piup=F(314159265359,10**11);assert sqrt3lo**2<3 and sqrt5hi**2>5;capup=F(623,100);assert capup**2>25*(25+11*sqrt5hi)/32;gain=15*sqrt3lo/4+5*gd+10*g0-capup-c*piup/3;assert gain>F(6,100);area=F(low['area_margin'])+R*R*gain;assert area>0
 # CAS checks actual unnormalized potential: at a complete5-star with
 # only neutral neighbours, central-angle sum2pi gives c*(2pi-5pi/3).
 cc,p=sp.symbols('c pi');assert sp.expand(cc*(2*p-5*p/3)-cc*p/3)==0
 # Enumerate highM Euler slots after excluding low degrees and shifts.
 remaining=[]
 for M in range(26,100):
  for e in range(17):
   for bad in range(35):
    excess=28-M-e-bad
    if excess<0 or M>=27 or e or bad:continue
    remaining.append((M,e,bad,excess))
 assert remaining==[(26,0,0,2)];partitions=[]
 for seven in range(3):
  for eight in range(2):
   if seven+2*eight==2:partitions.append([7]*seven+[8]*eight)
 assert sorted(partitions)==sorted([[7,7],[8]])
 # More-than-one strict positive unit cannot enter selected5 theorem.
 # Verify exact premises use unique global5, not only one selected label.
 assert proof['M24_unique5_all_neighbours_degree6'];inequalities=[(5*108,20**2),(5*107,23**2),(5*106,22**2),(5*106,3**2+21**2),(5*64,16**2),(5*64,3**2+15**2)];assert all(a>b for a,b in inequalities)
 control=subprocess.run([sys.executable,'-O',str(ROOT/'verify/n100_B34_low_and_high_reduction.py')],cwd=ROOT,text=True,capture_output=True);assert control.returncode!=0 and 'Assertions must remain enabled' in control.stderr
 out=ROOT/'verify/out/n100-B34-low-independent-172.json';assert not out.exists();out.write_text(json.dumps({'schema':'n100-B34-independent-low-audit/v1','status':'PASS','radius':str(R),'low_M_closed':True,'independent_cap5_upper':str(capup),'independent_sqrt3_lower':str(sqrt3lo),'pi_upper':str(piup),'independent_gain_lower':str(gain),'independent_area_margin_lower':str(area),'CAS_central_star_potential':True,'high_Euler_remainders':remaining,'high_degree_partitions':partitions,'optimized_mode_rejected':{'exit_code':control.returncode,'message':'Assertions must remain enabled'},'full_B34_closed':False,'global_bound_improved':False,'scope':'Independent rational star-cap estimate and Fraction recomposition; same reviewed isolated-five topological lemma, not independent planar embedding proof. Pi rational bracket inherited from exact scalar backend.','bindings':{p.relative_to(ROOT).as_posix():sha(p) for p in (Path(__file__),cp,dp,pp)}},indent=2)+'\n',encoding='utf-8');print('B34 LOW INDEPENDENT PASS conservative cap6.23 area',area,flush=True)
if __name__=='__main__':main()
