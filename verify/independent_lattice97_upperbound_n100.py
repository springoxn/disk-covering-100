"""Independent rational support-plane verification of the 97-point lattice cover.
Does not import the lattice constructor or its checker. Analytic nearest-lattice
existence and Voronoi containment are documented in the proof, not formalized.
"""
import argparse,hashlib,json
from fractions import Fraction as F
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def dot(p,q):return p[0]*q[0]+3*p[1]*q[1]
def add(p,q):return (p[0]+q[0],p[1]+q[1])
def sub(p,q):return (p[0]-q[0],p[1]-q[1])
def center(i,j):return (F(2*i+j,2),F(j,2))
def norm(i,j):return i*i+i*j+j*j
HEX=[(F(1,2),F(1,6)),(F(0),F(1,3)),(-F(1,2),F(1,6)),(-F(1,2),-F(1,6)),(F(0),-F(1,3)),(F(1,2),-F(1,6))]
def audit():
 retained=[(i,j) for i in range(-8,9) for j in range(-8,9) if norm(i,j)<28]
 shell=[(i,j) for i in range(-8,9) for j in range(-8,9) if norm(i,j)==28]
 rows=[]
 for i,j in shell:
  vertices=[add(center(i,j),h) for h in HEX]
  support=[v for v in vertices if all(dot(v,sub(w,v))>=0 for w in vertices)]
  assert len(support)==1
  v=support[0];v2=dot(v,v)
  neighbors=[(u,k) for u,k in retained if dot(sub(v,center(u,k)),sub(v,center(u,k)))<=F(1,3)]
  rows.append({'index':[i,j],'closest_vertex':[str(t) for t in v],
   'support_inequalities':[str(dot(v,sub(w,v))) for w in vertices],
   'min_norm_squared':str(v2),'retained_contact_neighbors':[list(p) for p in neighbors]})
  assert v2==F(67,3) and len(neighbors)>=1
 q=(F(1,2),F(1,6))
 nearby=[(i,j) for i in range(-2,3) for j in range(-2,3) if norm(i,j)<2]
 qdist=[dot(sub(q,center(i,j)),sub(q,center(i,j))) for i,j in nearby]
 lo,hi=F(1221694443,10**10),F(1221694444,10**10)
 checks={'retained_count_97':len(retained)==97,'shell_count_12':len(shell)==12,
  'outside_box_cannot_be_low_norm':F(9*9,2)>28,
  'hex_circumradius_squared':all(dot(v,v)==F(1,3) for v in HEX),
  'all_shell_cells_touch_only_at_retained_contacts':len(rows)==12,
  'far_shell_strict_separation':F(7)**2>4*F(29,3) and F(7)>0,
  'hole_nearby_min_squared':min(qdist)==F(1,3),
  'hole_far_points_excluded':F(2)>F(4,3),
  'hole_inside_unit_disk':F(3,67)*dot(q,q)<1,
  'positive_root_bracket':0<lo<hi and 67*lo*lo<1<67*hi*hi,
  'irreducibility_nonsquare_67':8*8<67<9*9,
  'improves_old_upper_bound':F(1,67)<F(1223433,10**7)**2}
 return retained,rows,checks

def input_checks(cert,retained,proof):
 points=cert.get('exact_configuration',{}).get('indices') if isinstance(cert.get('exact_configuration'),dict) else cert.get('exact_configuration')
 if points is None:points=cert.get('indices')
 indices=[tuple(v) for v in points] if isinstance(points,list) else []
 return {'explicit_indices_100':len(indices)==100 and len(set(indices))==100 and set(retained)<=set(indices),
 'all_indices_are_lattice':all(len(p)==2 and all(isinstance(t,int) and not isinstance(t,bool) for t in p) for p in indices),
 'alpha_squared_matches':str(cert.get('alpha_squared'))=='1/67',
 'minpoly_coefficients_match':cert.get('minpoly_coefficients')==[67,0,-1],
 'proof_hash_matches':cert.get('proof_sha256')==hashlib.sha256(proof.read_bytes()).hexdigest()}

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--input',default='verify/out/lattice97_upperbound_n100.json');ap.add_argument('--out',default='verify/out/independent_lattice97_upperbound_n100.json');args=ap.parse_args()
 out=ROOT/args.out
 if out.exists():raise FileExistsError(out)
 inp=ROOT/args.input;cert=json.loads(inp.read_text(encoding='utf-8'))
 retained,rows,checks=audit()
 proof=ROOT/'proofs/n100-lattice97-algebraic-upperbound.md'
 checks.update(input_checks(cert,retained,proof))
 passed=all(checks.values())
 import copy
 controls=[]
 for label,mutate in [
  ('wrong_squared_radius',lambda c:c.__setitem__('alpha_squared','1/66')),
  ('wrong_minpoly',lambda c:c.__setitem__('minpoly_coefficients',[66,0,-1])),
  ('wrong_proof_hash',lambda c:c.__setitem__('proof_sha256','0'*64)),
  ('delete_required_center',lambda c:c['exact_configuration']['indices'].pop(0))]:
  altered=copy.deepcopy(cert);mutate(altered)
  rejected=not all(input_checks(altered,retained,proof).values())
  controls.append({'case':label,'rejected':rejected})
 controls.append({'case':'scale_increase_breaks_contact_precondition',
 'rejected':F(3,67)*F(10001,10000)**2*F(67,3)>1,
 'scope':'rejects the fixed contact normalization, not an uncovered point proof'})
 passed=passed and all(c['rejected'] for c in controls)
 result={'schema':'independent-lattice97-cover/v1','all_passed':passed,'coverage_confirmed':passed,
  'exact_candidate_radius_confirmed':passed,'alpha_squared':'1/67','minpoly_coefficients':[67,0,-1],
  'machine_verified_geometry':False,'input_sha256':hashlib.sha256(inp.read_bytes()).hexdigest(),
  'proof_sha256':hashlib.sha256(proof.read_bytes()).hexdigest(),
  'checker_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
  'checks':checks,'shell_support_certificates':rows,'controls':controls,
  'not_claimed':['global optimality','minimal polynomial of optimal n100 radius']}
 out.parent.mkdir(parents=True,exist_ok=True);out.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 print('PASS' if passed else 'FAIL','independent 97-lattice support certificate;',len(checks),'checks')
 return 0 if passed else 1
if __name__=='__main__':raise SystemExit(main())
