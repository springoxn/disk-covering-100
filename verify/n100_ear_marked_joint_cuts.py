"""Joint actual-ear count area and guaranteed disjoint-ear concentration."""
from pathlib import Path
from fractions import Fraction as F
import json,hashlib
from n100_recursive_ear_obstruction import E,H_upper,ROOT

def main():
 p=ROOT/'verify/out/n100-total-ear-face-cuts.json';z=json.loads(p.read_text(encoding='utf-8'));angles=json.loads((ROOT/'verify/out/n100-disjoint-ear-group-cuts.json').read_text(encoding='utf-8'));r=F(z['radius_upper_inclusive']);g=F(angles['three_arc_sum_upper']);arc=F(angles['individual_arc_upper']);A=E.AH;G1=E.sqrt_bounds((207+33*E.sqrt_bounds(F(33))[1])/128)[1];G2=E.sqrt_bounds(9+6*E.sqrt_bounds(F(3))[1])[1]/2;rows=[]
 for c in z['family_rows']:
  m,B,emax=c['m'],c['B'],c['maximum_total_ear_faces'];tests=[]
  for e in range(emax+1):
   f0=2*m-2*B-2+e;f1=B-2*e;base=(f0*A+f1*G1+e*G2)*r*r;q=(e-1)//2 if B%4==2 and e==B//2 else (e+1)//2;k=B-3*q;capacity=2*E.PL-q*g-k*arc
   if capacity>0:status='excluded by arc capacity';gap=capacity
   else:
    E.need(k>0,'nonempty remainder');lo=(2*E.PL-q*g)/k;hi=(2*E.PH-q*g)/k
    if E.sin_at(hi/2)[1]>=r:status='undecided domain';gap=F(0)
    else:
     hs=(3*q*H_upper(r,g/3,g/3) if q else 0)+k*H_upper(r,lo,hi);gap=E.PL-base-hs;status='excluded by joint area' if gap>0 else 'not excluded'
   tests.append({'ear_count':e,'guaranteed_disjoint_groups':q,'status':status,'gap':str(gap)})
  kept=[t['ear_count'] for t in tests if not t['status'].startswith('excluded')];rows.append({'m':m,'B':B,'prior_ear_upper':emax,'remaining_ear_counts':kept,'tests':tests})
 out=ROOT/'verify/out/n100-ear-marked-joint-cuts.json';E.need(not out.exists(),'overwrite');out.write_text(json.dumps({'schema':'n100-ear-marked-joint-cuts/v1','radius_upper_inclusive':str(r),'root_upper_constants':{'A':str(A),'G1':str(G1),'G2':str(G2)},'family_rows':rows,'analytic_dependencies':['joint marked-face geometric bounds G0=A,G1=sqrt((207+33sqrt33)/128),G2=sqrt(9+6sqrt3)/2 from original GLOBAL_LOWER_PROOF sections5.1-5.3','actual ear count e forces f0=2m-2B-2+e,f1=B-2e,f2=e; marked areas charged once','disjoint-ear packing lower bound from stage113; then concentrated arc Jensen upper as stage112','all upper-radius replacements valid uniformly below saved radius, with fixed actual ear count treated anew per diagram'],'scope':'ear-count-specific topology refinement; not graph census or feasibility proof; undecided domain retained','global_optimality':False,'input_sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()},indent=2)+'\n',encoding='utf-8');print('PASS ear-marked joint',[(c['m'],c['B'],c['prior_ear_upper'],max(c['remaining_ear_counts'],default=-1)) for c in rows])
if __name__=='__main__':main()
