"""B34 complete lowM and strict highM reduction at R=.11324."""
from pathlib import Path
from fractions import Fraction as F
import json,sys,hashlib
import sympy as sp
ROOT=Path(__file__).resolve().parents[1];W=ROOT/'runtime/disk100-release-lf-67ebf1c/certified_bounds_11323/working';SROOT=W.parent/'lower_staging/B34_0p11323';sys.path[:0]=[str(W),str(W/'lower_bounds_extension_20261004')]
from verify_star_lp_duals import q,S,PI
from verify_complete_star_area_caps import cap
R=F(2831,25000)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 if not __debug__:raise RuntimeError('Assertions must remain enabled')
 dp=ROOT/'verify/out/n100-B34-diagnostic-170.json';diag=json.loads(dp.read_text(encoding='utf-8'));assert diag['status']=='PASS_PREMISES';base=diag['replay']['result'];assert F(base['radius'])==R;rows=base['branches'];assert len(rows)==3 and F(rows[0]['area_margin'])>0;low=rows[1];high=rows[2];lm=F(low['area_margin']);hm=F(high['area_margin']);assert lm<0 and hm<0
 def shifted(row,base):return {'next_M':base-R*R*F(row['M_slope_upper']),'ear':base-R*R*F(row['shifted_ear_upper']),'bad_q1':base-R*R*F(row['bad_q1_coefficient_upper'])}
 low_shift=shifted(low,lm);high_shift=shifted(high,hm);assert min(*low_shift.values(),*high_shift.values())>0
 neutral_low=min(F(v) for p,d,v in low['neutral_low_slacks']);positive34=min(F(v) for p,d,v in low['positive_low_slacks'] if d in (3,4));neutral_high=min(F(v) for p,d,v in high['neutral_low_slacks']);extra_low=lm+R*R*neutral_low;selected34=lm+R*R*positive34;any_high_low=hm+R*R*neutral_high;assert min(extra_low,selected34,any_high_low)>0
 # Remaining M24 has unique global5, chosen strict-interior. Use radius-free
 # B34 isolated-five theorem, replay every separating integer inequality.
 assert 5*108>20**2 and 5*107>23**2 and 5*106>22**2 and 5*106>3**2+21**2
 assert F(24+17)+F(17**2,5)<106;assert F(24+19)+F(19**2,6)<106
 assert 5*64>16**2 and 5*64>3**2+15**2
 assert F(18+12)+F(12**2,5)<64;assert F(18+13)+F(13**2,6)<64
 # No high neighbour: first possible deep7 must lie on the first stripped
 # ring, while the5 cannot touch that ring by a /6 contradiction.
 proposal=SROOT/'hinge_B34_0p11323_proposals.json';row=json.loads(proposal.read_text(encoding='utf-8'))['rows'][1];D=row['denominator'];PD=row['potential_denominator'];c=F(row['deep_potential'],PD);gd=F(row['charge_deep'],D);g0=F(row['charge_0'],D);A=3*q(3).sqrt()/4;previous=5*A+q(5*gd+10*g0);replacement=cap(5)+q(c)*PI/3;gain=F((previous-replacement).l,S);assert gain>F(7,100);isolated=lm+R*R*gain;assert isolated>0
 # CAS: exact face and first-peel counts used by the isolated5 proof.
 I,M,cnt,n3=sp.symbols('I M components allB',integer=True);Fcore=2*I-M-2+2*(cnt-1)+n3;assert Fcore.subs({I:66,M:24,cnt:1,n3:0})==106;assert 106-24-18==64
 # High after shifts/no-low: M26/e0/b0,total positive excess2.
 assert 28-26==2;remaining=[[7,7],[8]]
 out=ROOT/'verify/out/n100-B34-low-and-high-reduction-171.json';assert not out.exists();out.write_text(json.dumps({'schema':'n100-B34-low-complete-high-reduction/v1','status':'PASS','radius':str(R),'B':34,'m':100,'required_center_norm_squared_upper':str(1-R*R),'low_M_closed':True,'low_M_domain':'M<=25','M22_23_margin':rows[0]['area_margin'],'M25_and_shift_margins':{k:str(v) for k,v in low_shift.items()},'additional_global_low_margin':str(extra_low),'selected_deep_degree3_or4_margin':str(selected34),'M24_unique5_all_neighbours_degree6':True,'isolated5_gain_lower':str(gain),'isolated5_area_margin':str(isolated),'low_minimum_reported_margin':str(min(F(rows[0]['area_margin']),*low_shift.values(),extra_low,selected34,isolated)),'high_M27_and_shifts':{k:str(v) for k,v in high_shift.items()},'any_low_high_M_margin':str(any_high_low),'high_remaining':{'M':26,'ears':0,'bad_q1':0,'all_interior_degrees_at_least':6,'positive_excess':2,'degree_profiles':remaining},'high_M_closed':False,'full_B34_closed':False,'global_bound_improved':False,'budget_review':'Original valid K=.5 and q4 paid.02 support reused in one complete original row at a time. Vertex reduced costs consumed once; isolated5 raw complete-star cap replaces its5(P,0,0) faces once without any edge/hinge payment. Pure topology restricts face labels; it spends no second scalar deficit.','geometric_dependencies':'Inherited one-positive-curvature /5 isoperimetry and chord-aware first peel, common core identity with I66 and M24; isolated5 refinement freshly checked as analytic argument plus integer/CAS conditions, not formal embedding kernel.','bindings':{p.relative_to(ROOT).as_posix():sha(p) for p in (Path(__file__),dp,proposal,W/'B34_M24_ISOLATED_FIVE_REFINEMENT.md',W/'GENERAL_FIRST_BOUNDARY_PEEL_CHORDS.md',W/'verify_complete_star_area_caps.py')}},indent=2)+'\n',encoding='utf-8');print('B34 LOW COMPLETE PASS gain',gain,'high residual M26 no-low,2high curvature',flush=True)
if __name__=='__main__':main()
