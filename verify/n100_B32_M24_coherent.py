"""Exact coherent M24 five-star replacement for the original fixed row.
Local geometric premises are explicit and are not inferred from this scalar test.
"""
from pathlib import Path
from fractions import Fraction as F
from itertools import combinations
import sys,json,hashlib
R=Path(__file__).resolve().parents[1];W=R/'runtime/disk100-release-lf-67ebf1c/certified_bounds_11323/working';sys.path[:0]=[str(W),str(W/'signed_edge_metric_20261004')]
from verify_star_lp_duals import q,S,PI,I
from exact_signed_sine_full_face_support import face_bound
from polygon_star_perimeter_support import support

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def interval(z):return [str(F(z.l,S)),str(F(z.u,S))]
def verify():
 source=R/'runtime/B32-M24-coherent-discovery-141/candidates.json';data=json.loads(source.read_text(encoding='utf-8'));candidate=next(z for z in data['cases'] if F(z['epsilon'])==F(1,2) and F(z['tau'])==F(13,10));eps=F(1,2);tau=F(13,10);k=eps*tau;weight=1-eps;y=F(1,4);c=F(1,2);labels=[-F(378148580,10**9),-F(129204403,10**9),F(0)];charges=[F(v,10**9) for v in (26923601,3184540,25,50630840)];A=3*q(3).sqrt()/4;ANG=PI/3
 expected=[([2,2,i],[F(0),F(0),k]) for i in range(3)]+[([2,2,2],[k,F(0),k])];assert len(candidate['outside'])==4;rows=[];extras=[]
 for saved,(ids,edges) in zip(candidate['outside'],expected):
  assert saved['ids']==ids and list(map(F,saved['edges']))==edges;nu=F(saved['nu']);value,acute,boundaries=face_bound([labels[i] for i in ids],edges,nu);assert all(value.u>=v.u for v in [acute]+boundaries);old=A+q(sum((charges[i] for i in ids),F(0)));extra=value-old;extras.append(extra);rows.append({'ids':ids,'edges':[str(e) for e in edges],'nu':str(nu),'upper':str(F(value.u,S)),'old_allowance_lower':str(F(old.l,S)),'extra_upper':str(F(extra.u,S))})
 D1=I(max(v.l for v in extras[:3]),max(v.u for v in extras[:3]));D2=extras[3];compositions=[(5-2*j,j) for j in range(3)];payments=[n*D1+j*D2 for n,j in compositions];J=I(max(z.l for z in payments),max(z.u for z in payments))
 cycle={frozenset((i,(i+1)%5)) for i in range(5)};types=[]
 for triangle in combinations(range(5),3):types.append(sum(edge<=set(triangle) for edge in cycle))
 assert max(types)==2 and 3 not in types;assert all(n+2*j==5 for n,j in compositions)
 residual,acute,boundaries=face_bound([y/weight,F(0),F(0)],[F(0)]*3,F(candidate['residual_nu']));assert all(residual.u>=v.u for v in [acute]+boundaries);joint=support(5,eps,-k)-q(y-c)*ANG+5*q(weight)*residual;old=5*A+q(5*charges[3]+10*charges[2]);gain=old-joint-J;assert gain.l>q(F(19,100)).u
 # Formal scalar accounting: five centers sum2pi, five corner means5pi/3.
 assert F(2)-F(5,3)==F(1,3);assert eps+weight==1 and k==eps*tau
 return {'status':'PASS','certified_normalized_gain':'19/100','computed_gain_interval':interval(gain),'fixed_original_LOW24':{'a':378148580,'lb':129204403,'c':500000000,'charges':[26923601,3184540,25,50630840],'denominator':10**9},'epsilon':str(eps),'tau':str(tau),'free_center_potential':str(y),'central_residual_nu':candidate['residual_nu'],'central_upper':str(F(joint.u,S)),'old_central_allowance_lower':str(F(old.l,S)),'outside_total_upper':str(F(J.u,S)),'outside_supports':rows,'outside_edge_compositions':[list(t) for t in compositions],'C5_ring_triangle_selected_edge_counts':types,'central_angle_balance_coefficient':'1/3','physical_edge_cancellation':'one -k*ell/(2R) inside and one +k*ell/(2R) outside per each of5 ring edges; outside sine support conservatively dominates length term','required_geometry':['selected unique deep degree5 center','all five distinct neighbors have ordinary label0 (degree6) in the original LOW24 row','no other positive-labelled site in outside faces','every selected ring edge is interior and has exactly one outside face','complete-star polygon area/half-perimeter support inherited from audited upstream theorem'],'scope':'conditional local replacement; does not establish profile existence or full B32','bindings':{p.relative_to(R).as_posix():sha(p) for p in (source,W/'exact_signed_sine_full_face_support.py',W/'polygon_star_perimeter_support.py',Path(__file__))}}
def main():
 result=verify();out=R/'verify/out/n100-B32-M24-coherent-141.json';assert not out.exists();out.write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8');print('PASS exact M24 coherent gain19/100;4 complete-simplex outside supports;C5 edge accounting')
if __name__=='__main__':main()
