"""Independent incidence reconstruction plus exact midpoint planar embedding audit."""
from pathlib import Path
from itertools import combinations
from fractions import Fraction as F
import json,hashlib
R=Path(__file__).resolve().parents[1];S='runtime/external-disk100-strict-local-replay/source/'
def need(ok,msg):
    if not ok:raise ValueError(msg)
def orient(a,b,c):return (b[0]-a[0])*(c[1]-a[1])-(b[1]-a[1])*(c[0]-a[0])
def overlap(a,b,c,d):
    return all(max(min(a[i],b[i]),min(c[i],d[i]))<=min(max(a[i],b[i]),max(c[i],d[i])) for i in (0,1))
def main():
    t=json.loads((R/(S+'algebraic_cover_topology.json')).read_text(encoding='utf-8'))
    m=json.loads((R/(S+'rational_midpoint.json')).read_text(encoding='utf-8'));D=int(m['denominator']);v=list(map(int,m['numerators']));C=list(zip(v[:200:2],v[1:200:2]))
    incidence={}
    for index,(a,b,c) in enumerate(t['triangles']):
        need(orient(C[a],C[b],C[c])!=0,'noncollinear face')
        for e in ((a,b),(b,c),(c,a)):incidence.setdefault(tuple(sorted(e)),[]).append(index)
    E=sorted(incidence);outer={e for e,faces in incidence.items() if len(faces)==1}
    hull=t['hull'];need(outer=={tuple(sorted((a,b))) for a,b in zip(hull,hull[1:]+hull[:1])},'outer incidence')
    need(all(len(f)==(1 if e in outer else 2) for e,f in incidence.items()),'face multiplicity')
    tested=0
    for (a,b),(c,d) in combinations(E,2):
        if {a,b}&{c,d}:continue
        A,B,Cp,Dp=C[a],C[b],C[c],C[d]
        if overlap(A,B,Cp,Dp):
            o1,o2=orient(A,B,Cp),orient(A,B,Dp);o3,o4=orient(Cp,Dp,A),orient(Cp,Dp,B)
            need(not(o1*o2<=0 and o3*o4<=0),'crossing or nonincident contact')
        tested+=1
    circum=[]
    for a,b,c in t['triangles']:
        A,B,P=C[a],C[b],C[c];ux,uy=B[0]-A[0],B[1]-A[1];vx,vy=P[0]-A[0],P[1]-A[1]
        det=2*(ux*vy-uy*vx);u=ux*ux+uy*uy;w=vx*vx+vy*vy
        qx=F(A[0],D)+F(u*vy-w*uy,det*D);qy=F(A[1],D)+F(ux*w-vx*u,det*D)
        circum.append(qx*qx+qy*qy)
    interior=sum(z<1 for z in circum);exterior=sum(z>1 for z in circum);on=sum(z==1 for z in circum)
    primary=R/'verify/out/n100-candidate-topology-audit.json';audit=json.loads(primary.read_text(encoding='utf-8'))
    need(audit['distinct_vertices']==100 and audit['distinct_edges']==len(E)==277 and len(t['triangles'])+1==179,'primary agreement')
    op=R/'verify/out/n100-candidate-map-embedding.json';need(not op.exists(),'overwrite')
    op.write_text(json.dumps({'verified':True,'method':'separate edge-face reconstruction and integer segment intersection',
        'nonincident_edge_pairs_checked':tested,'noncollinear_faces':len(circum),
        'midpoint_circumcenters_inside_D':interior,'midpoint_circumcenters_outside_D':exterior,'midpoint_circumcenters_on_boundary':on,
        'full_triangle_count':178,'active_hole_count':114,
        'scope':'exact rational midpoint embedding and incidence only; no root-box Delaunay classification or full clipped Voronoi map certification',
        'global_optimality':False,'minimal_polynomial_obtained':False,
        'bindings':{p:hashlib.sha256((R/p).read_bytes()).hexdigest() for p in [S+'algebraic_cover_topology.json',S+'rational_midpoint.json','verify/out/n100-candidate-topology-audit.json']},
        'checker_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()},indent=2)+'\n',encoding='utf-8')
    print('PASS exact embedding;',tested,'nonincident edge pairs; circumcenters inside/outside/on=',interior,exterior,on)
if __name__=='__main__':main()
