"""Exact arithmetic for the B35 M25 core-profile obstruction."""
from pathlib import Path
import json,hashlib
import sympy as sp
from fractions import Fraction as F
ROOT=Path(__file__).resolve().parents[1]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 if not __debug__:raise RuntimeError('Assertions must remain enabled')
 doc=ROOT/'runtime/disk100-release-lf-67ebf1c/certified_bounds_11323/working/B35_M25_CORE_PROFILE_OBSTRUCTION.md';diag=ROOT/'verify/out/n100-B35-profile-diagnostic-186.json';d=json.loads(diag.read_text(encoding='utf-8'));assert d['status']=='PASS_PREMISES';branch=d['replay']['result']['branches'][3];assert branch['M']==25 and branch['restricted'];R=F(d['radius']);assert R==F(2831,25000)
 # c>=2, bridge, two blocks, chord and degree-two comparisons from the written lemma.
 checks={'components':105*6-21**2,'bridge':103*6-23**2,'two_blocks':103*6-(3**2+22**2),'chord':103*6-(3**2+24**2)};assert all(v>0 for v in checks.values())
 I,M,c,n3=sp.symbols('I M c n3',integer=True);Fcore=2*I-2-M+2*(c-1)+n3;P= M-4*(c-1)-n3;assert Fcore.subs({I:65,M:25,c:1,n3:0})==103 and P.subs({M:25,c:1,n3:0})==25
 assert sp.expand((M-4*(c-1)-n3)**2-6*(2*I-2-M+2*(c-1)+n3)).subs({I:65,M:25,c:2,n3:0})<0
 # degree identity: sum(deg-6)=B-6-U=4 at B35,U25.
 assert 35-6-25==4
 # Four q=4/d7 marked apices each have at least 5 boundary neighbours;
 # full degree leaves <=2 core neighbours, contradicting core minimum3.
 assert 4+1==5 and 7-5==2 and 2<3
 out=ROOT/'verify/out/n100-B35-M25-core-obstruction-187.json';assert not out.exists();out.write_text(json.dumps({'schema':'B35-M25-core-profile-obstruction/v1','status':'PASS_ARITHMETIC_LEMMA','radius':str(R),'B':35,'M':25,'core_vertices':65,'core_faces':103,'core_boundary':25,'integer_checks':checks,'core_identities':{'F_core':'2I-2-M+2(c-1)+n3','P_walk':'M-4(c-1)-n3','base_F':103,'base_P':25},'curvature_identity':'sum(deg-6)=4','forbidden_profile':'all four degree-seven vertices are ordinary p=4 marked apices','endpoint_contradiction':{'marked_boundary_edges':4,'minimum_boundary_neighbors':5,'maximum_core_neighbors':2,'core_minimum_core_neighbors':3},'scope':'Arithmetic/CAS replay of the written topology lemma. It does not yet prove the current-radius B35 negative row reduces to this profile; p<=3 degree-seven and degree>=8 residuals remain explicit.','B35_closed':False,'global_bound_improved':False,'bindings':{p.relative_to(ROOT).as_posix():sha(p) for p in (Path(__file__),doc,diag)}},indent=2)+'\n',encoding='utf-8');print('B35 M25 OBSTRUCTION ARITHMETIC PASS; profile reduction pending',flush=True)
if __name__=='__main__':main()
