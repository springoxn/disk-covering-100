"""Rational counterexample: disconnected boundary ownership is not a pruning rule."""
from pathlib import Path
from fractions import Fraction as F
import json,hashlib
R=Path(__file__).resolve().parents[1]
def need(x,m):
    if not x:raise ValueError(m)
def norm(p):return sum(x*x for x in p)
def dist(p,q):return sum((a-b)**2 for a,b in zip(p,q))
def sequence(g):
    b=g['boundary_cycle'];s=[]
    for a,c in zip(b,b[1:]+b[:1]):
        e=[e for e in g['edges'] if len(e['faces'])==1 and e['ends'] in ([a,c],[c,a])];need(len(e)==1,'boundary identity');s.append(e[0]['faces'][0])
    counts={f:sum(s[i]==f and s[i-1]!=f for i in range(len(s))) for f in set(s)}
    if len(counts)==1:counts[s[0]]=1
    return s,counts
if __name__=='__main__':
    A=(F(99,100),F(0));B=(F(1),F(0));P=(F(323,325),F(36,325));Q=(P[0],-P[1]);M=(F(1),F(0));U=F(1154469548855829,10**16);T=U*U;cut=F(199,200)
    need(norm(P)==norm(Q)==norm(M)==1 and norm(A)<=1 and norm(B)<=1,'normalized geometry')
    for p in (P,Q):need(dist(p,A)<dist(p,B) and dist(p,A)<T,'endpoint nearest/covered')
    need(dist(M,B)<dist(M,A) and dist(M,B)<T,'middle nearest')
    need((norm(B)-norm(A))/(2*(B[0]-A[0]))==cut and P[0]<cut<1,'exact bisector')
    need(1+norm(A)-2*A[0]*P[0]==dist(P,A)<T,'whole short arc maximum')
    paths=['verify/out/n100-candidate-clipped-map.json','verify/out/n100-generic-map-compiler.json'];G=json.loads((R/paths[0]).read_text(encoding='utf-8'));s,k=sequence(G);models=json.loads((R/paths[1]).read_text(encoding='utf-8'));small=[]
    for e in models['small_models']:
        q,b=sequence(e['map']);small.append({'chord':e['chord'],'sequence':q,'cyclic_blocks':b})
    out=R/'verify/out/n100-disconnected-boundary-owner-counterexample.json';need(not out.exists(),'overwrite')
    out.write_text(json.dumps({'verified_exact_counterexample':True,'centers':[[str(v) for v in c] for c in (A,B)],'points':[[str(v) for v in c] for c in (Q,M,P)],'radius_upper':str(U),'bisector_x':str(cut),'endpoint_distance_squared':str(dist(P,A)),'endpoint_coverage_margin':str(T-dist(P,A)),'whole_short_arc_served_by_A':True,'nearest_owner_sequence_on_three_points':['A','B','A'],'candidate_sequence':s,'candidate_cyclic_blocks':k,'small_maps':small,'invalid_pruning_rule':'discard a map solely because a face owns separated boundary arcs','scope':'local geometric counterexample to ownership-connectivity inference; not a full unit-disk cover at U or global bound','bindings':{p:hashlib.sha256((R/p).read_bytes()).hexdigest() for p in paths},'checker_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'global_optimality':False,'minimal_polynomial_obtained':False},indent=2)+'\n',encoding='utf-8')
    print('PASS rational counterexample at U:connected service short arc,nearest ownership A-B-A;pruning inference invalid')
