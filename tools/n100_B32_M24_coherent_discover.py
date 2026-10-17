"""Discover a coherent M24 five-star replacement; exact scalar candidate bounds.
Geometry incidence/cancellation still requires independent audit.
"""
from pathlib import Path
from fractions import Fraction as F
import sys,json,hashlib
from scipy.optimize import minimize_scalar
R=Path(__file__).resolve().parents[1];W=R/'runtime/disk100-release-lf-67ebf1c/certified_bounds_11323/working';sys.path[:0]=[str(W),str(W/'signed_edge_metric_20261004')]
from verify_star_lp_duals import q,S,PI,I
from exact_signed_sine_full_face_support import face_bound
from polygon_star_perimeter_support import support
A=3*q(3).sqrt()/4;ANG=PI/3;labels=[-F(378148580,10**9),-F(129204403,10**9),F(0)];charges=list(map(lambda v:F(v,10**9),[26923601,3184540,25,50630840]));center=F(1,2)
def inter(z):return [str(F(z.l,S)),str(F(z.u,S))]
def cell(ids,edges):
 def val(x):return face_bound([labels[i] for i in ids],edges,F(round(float(x)*10**9),10**9))[0]
 opt=minimize_scalar(lambda x:float(F(val(x).u,S)),bounds=(-1.4,.7),method='bounded',options={'xatol':1e-8});nu=F(round(opt.x*10**9),10**9);cap=face_bound([labels[i] for i in ids],edges,nu)[0];allow=A+q(sum((charges[i] for i in ids),F(0)));return {'ids':list(ids),'edges':[str(v) for v in edges],'nu':str(nu),'bound':inter(cap),'extra':inter(cap-allow)},cap-allow

def main():
 cases=[]
 for eps,tau in [(F(3,10),F(13,10)),(F(1,2),F(13,10)),(F(1,5),F(13,10)),(F(3,10),F(6,5)),(F(3,10),F(7,5))]:
  weight=1-eps;k=eps*tau;outside=[];d=[]
  for i in range(3):row,z=cell([2,2,i],[F(0),F(0),k]);outside.append(row);d.append(z)
  D1=I(max(v.l for v in d),max(v.u for v in d));row,D2=cell([2,2,2],[k,F(0),k]);outside.append(row);js=[(5-2*j)*D1+j*D2 for j in range(3)];J=I(max(z.l for z in js),max(z.u for z in js));y=weight/2;nu=F(-309016994,10**9);residual=face_bound([y/weight,F(0),F(0)],[F(0)]*3,nu)[0];joint=support(5,eps,-k)-q(y-center)*ANG+5*q(weight)*residual;old=5*A+q(5*charges[3]+10*charges[2]);gain=old-joint-J;cases.append({'epsilon':str(eps),'tau':str(tau),'center_potential':str(y),'residual_nu':str(nu),'outside':outside,'D1':inter(D1),'D2':inter(D2),'J':inter(J),'joint':inter(joint),'old_allowance':inter(old),'normalized_gain':inter(gain)});print('CANDIDATE',eps,tau,'exact gain',inter(gain),flush=True)
 folder=R/'runtime/B32-M24-coherent-discovery-141';assert not folder.exists();folder.mkdir(parents=True);(folder/'candidates.json').write_text(json.dumps({'schema':'n100-M24-coherent-discovery/v1','discovery_only':True,'cases':cases,'geometry_required':['unique deep degree5, all five neighbors ordinary degree6','outside faces have no other positive center','ring five edges: each outside triangle owns at most two','signed halfedge penalties cancel once per physical ring edge','old face/vertex charges unchanged; existing forced-degree5 credit used once'],'global_bound_improved':False,'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()},indent=2)+'\n',encoding='utf-8')
if __name__=='__main__':main()
