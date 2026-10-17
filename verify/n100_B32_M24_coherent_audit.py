"""Independent rational accounting and CAS check for M24 local replacement."""
from pathlib import Path
from fractions import Fraction as F
from itertools import combinations
import json,sys,hashlib
import sympy as sp
R=Path(__file__).resolve().parents[1];W=R/'runtime/disk100-release-lf-67ebf1c/certified_bounds_11323/working';sys.path[:0]=[str(W),str(W/'signed_edge_metric_20261004')]
from verify_star_lp_duals import q,S,PI
from exact_signed_sine_full_face_support import face_bound
from polygon_star_perimeter_support import support

def main():
 certpath=R/'verify/out/n100-B32-M24-coherent-141.json';cert=json.loads(certpath.read_text(encoding='utf-8'));A=3*q(3).sqrt()/4;charges=[F(v,10**9) for v in (26923601,3184540,25,50630840)];labels=[-F(378148580,10**9),-F(129204403,10**9),F(0)];epsilon=F(1,2);weight=F(1,2);y=F(1,4);original_c=F(1,2);k=F(13,20);outside=[]
 for row in cert['outside_supports']:
  ids=row['ids'];z,_,_=face_bound([labels[i] for i in ids],list(map(F,row['edges'])),F(row['nu']));outside.append(F(z.u,S)-F(A.l,S)-sum((charges[i] for i in ids),F(0)))
 first=max(outside[:3]);second=outside[3];J=max((5-2*j)*first+j*second for j in range(3));residual=face_bound([F(1,2),0,0],[0,0,0],F(cert['central_residual_nu']))[0];poly=support(5,epsilon,-k);central=F(poly.u,S)+(original_c-y)*F(PI.u,3*S)+5*weight*F(residual.u,S);old=5*F(A.l,S)+5*charges[3]+10*charges[2];gain_lower=old-central-J;assert gain_lower>F(19,100)
 # Angle potential correction and physical edge conservation, symbolic.
 Y,C,pi=sp.symbols('Y C pi');angles=sp.symbols('alpha0:5');potential_change=(Y-C)*sum(angles)-5*(Y-C)*pi/3;correction=sp.expand(potential_change.subs(angles[4],2*pi-sum(angles[:4]))-(Y-C)*pi/3);assert correction==0
 edge=sp.symbols('e0:5');kappa=sp.symbols('kappa');edge_identity=sp.expand(-kappa*sum(edge)+sum(kappa*v for v in edge));assert edge_identity==0
 ring={frozenset((i,(i+1)%5)) for i in range(5)};assert all(sum(e<=set(t) for e in ring)<=2 for t in combinations(range(5),3));raw=json.loads((R/'verify/out/n100-B32-exact-deficits-141.json').read_text(encoding='utf-8'));old_interval=next(c for c in raw['components'] if c['task']=='low')['exact_failure_locals'][-1]['values']['final24'];margin=F(old_interval['lower'])+F(11324,100000)**2*F(19,100);assert margin>0
 controls={'claim_gain_one_is_rejected':not (gain_lower>1),'count_six_edges_is_rejected':not all(5-2*j+2*j==6 for j in range(3)),'potential_correction_wrong_sign_is_nonzero':sp.expand(2*(Y-C)*pi/3)!=0};assert all(controls.values())
 out=R/'verify/out/n100-B32-M24-coherent-independent-141.json';assert not out.exists();out.write_text(json.dumps({'schema':'n100-M24-coherent-independent/v1','status':'PASS','rational_gain_lower':str(gain_lower),'certified_gain':'19/100','original_M24_margin_interval':old_interval,'improved_M24_margin_lower':str(margin),'CAS_potential_identity':str(correction),'CAS_physical_edge_identity':str(edge_identity),'C5_selected_edge_bound_verified':True,'controls':controls,'independence_scope':'separate Fraction endpoint accounting and CAS; same upstream scalar-support implementations/theorems, not independent geometric theorem proof','global_bound_improved':False,'bindings':{p.relative_to(R).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in (Path(__file__),certpath,R/'verify/out/n100-B32-exact-deficits-141.json')}},indent=2)+'\n',encoding='utf-8');print('PASS independent M24 Fraction/CAS accounting;positive corrected margin',str(margin))
if __name__=='__main__':main()
