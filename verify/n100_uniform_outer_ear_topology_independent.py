"""Independent finite checks for uniform ear flags and incidence identities."""
from pathlib import Path
from fractions import Fraction as F
import json,hashlib
from n100_recursive_joint_area_independent import series,need
R=Path(__file__).resolve().parents[1]
def main():
 p=R/'verify/out/n100-uniform-outer-ear-topology.json';z=json.loads(p.read_text(encoding='utf-8'));basep=R/'verify/out/n100-outer-ear-family-cuts-independent.json';base=json.loads(basep.read_text(encoding='utf-8'));primary=json.loads((R/'verify/out/n100-outer-ear-family-cuts.json').read_text(encoding='utf-8'));rho=F(z['radius_upper']);g=F(primary['three_arc_sum_upper']);need(rho==F(base['radius']) and 0<rho<F(1,5),'radius');need(z['bindings'][str(basep.relative_to(R))]==hashlib.sha256(basep.read_bytes()).hexdigest(),'binding');flags=[]
 for c in z['rows']:
  m,B=c['m'],c['B'];s=next(a for a in base['rows'] if (a['m'],a['B'])==(m,B));need(F(s['independent_deficit'])==F(c['independent_positive_gap'])>0,'independent strict gap');need(g*B<6*F(314159,100000),'concentration argument order');need(series(g/6)[1]<rho and series((2*F(314160,100000)-g)/(2*(B-3)))[1]<rho,'both target means in H domain');Ftot=c['total_triangles'];f0=c['faces_with_zero_boundary_edges'];f1=c['faces_with_one_boundary_edge'];f2=c['faces_with_two_boundary_edges'];E=m+Ftot-1;need(f2==0 and f1==B and f0+f1+f2==Ftot,'boundary incidence');need(3*Ftot==2*E-B and E==3*m-B-3,'triangle edge/Euler identities');need(Ftot==2*m-B-2 and f0==2*m-2*B-2,'eliminated formulas');flags.append([m,B])
 need(sorted(flags)==sorted(base['no_ear_families']),'all certified flags');out=R/'verify/out/n100-uniform-outer-ear-topology-independent.json';need(not out.exists(),'overwrite');out.write_text(json.dumps({'schema':'n100-uniform-outer-ear-topology-independent/v1','verified_source_gaps_and_Jensen_domains':True,'verified_Euler_and_boundary_face_incidence':True,'uniform_noear_families':flags,'radius_upper_inclusive':str(rho),'scope':'independent finite endpoint/domain/incidence checks; radius-uniform monotonicity/Jensen and topology proof analytic as listed in source, not machine-formal geometry; no family or radius exclusion','global_optimality':False,'input_sha256':hashlib.sha256(p.read_bytes()).hexdigest()},indent=2)+'\n',encoding='utf-8');print('PASS independent uniform ear flags and incidence identities',flags)
if __name__=='__main__':main()
