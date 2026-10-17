"""Compile and interval-verify one complete quadratic covering model.
Exact symbolic zero identities are discharged via accepted KKT root equations.
"""
from pathlib import Path
from fractions import Fraction as F
import json,hashlib
R=Path(__file__).resolve().parents[1];S='runtime/external-disk100-strict-local-replay/source/'
def need(v,msg):
    if not v:raise ValueError(msg)
def load(p):return json.loads((R/p).read_text(encoding='utf-8'))
def sha(p):return hashlib.sha256((R/p).read_bytes()).hexdigest()
def add(a,b):return a[0]+b[0],a[1]+b[1]
def neg(a):return -a[1],-a[0]
def sub(a,b):return add(a,neg(b))
def mul(a,b):
    v=[x*y for x in a for y in b];return min(v),max(v)
def sq(a):return (F(0) if a[0]<=0<=a[1] else min(a[0]**2,a[1]**2),max(a[0]**2,a[1]**2))
def norm(p):return add(sq(p[0]),sq(p[1]))
def polynomial(constant=0,linear=(),squares=(),crosses=()):
    terms=[]
    if constant:terms.append([constant,[]])
    terms.extend([c,[v]] for c,v in linear);terms.extend([c,[v,v]] for c,v in squares)
    terms.extend([c,sorted((a,b))] for c,a,b in crosses)
    return sorted(terms,key=lambda t:(len(t[1]),t[1]))

def main():
    G=load('verify/out/n100-candidate-clipped-map.json');audit=load('verify/out/n100-candidate-clipped-map-independent.json');inv=load('verify/out/n100-full-circumcenter-root-box.json');m=load(S+'rational_midpoint.json');sys=load(S+'polynomial_system.json');kr=load(S+'krawczyk_verification.json')
    need(audit['verified'] and audit['input_sha256']==sha('verify/out/n100-candidate-clipped-map.json'),'map audit')
    for receipt in (G,inv):
        for p,h in receipt['bindings'].items():need(sha(p)==h,'binding')
    need(kr['verified'] and kr['box_radius']==[1,10**58],'root')
    D=int(m['denominator']);rho=F(1,10**58);x=[(F(int(v),D)-rho,F(int(v),D)+rho) for v in m['numerators']];T=x[492];C=[x[2*j:2*j+2] for j in range(100)]
    rows={r['triangle_index']:r for r in inv['rows']};active={tuple(sorted(s)):h for h,s in enumerate(sys['internal_active_triangles'])}
    names=list(G['vertices']);pidx={v:[2*j,2*j+1] for j,v in enumerate(names)};cidx={j:[404+2*j,405+2*j] for j in range(100)};ti=604
    P={};point_sources={}
    for v in names:
        raw=G['vertices'][v]
        if raw['type']=='axis':P[v]=[(F(z),F(z)) for z in raw['coordinates']];point_sources[v]={'type':'exact_rational_axis'}
        elif raw['type']=='boundary_root_hole':
            h=raw['hole_index'];P[v]=x[428+2*h:430+2*h];point_sources[v]={'type':'KKT_boundary_hole','hole':h}
        else:
            row=rows[raw['triangle_index']];P[v]=[tuple(map(F,I)) for I in row['circumcenter_box']]
            point_sources[v]={'type':'unique_equidistant_circumcenter','triangle_index':raw['triangle_index']}
    eq=[];ineq=[];zeros=[];min_slack=None
    def inequality(kind,poly,interval,metadata=None,zero=None):
        nonlocal min_slack
        if zero is None:
            need(interval[0]>=0,kind+' interval not nonnegative');min_slack=interval[0] if min_slack is None else min(min_slack,interval[0])
        else:zeros.append({'constraint_index':len(ineq),'reason':zero})
        ineq.append({'kind':kind,'terms':poly,'metadata':metadata,'acceptance':'root_identity' if zero else 'interval_nonnegative','lower':str(interval[0]),'upper':str(interval[1])})
    inequality('t_nonnegative',polynomial(linear=[(1,ti)]),T)
    inequality('t_at_most_one',polynomial(1,linear=[(-1,ti)]),sub((F(1),F(1)),T))
    for v in names:
        a,b=pidx[v];I=sub((F(1),F(1)),norm(P[v]));boundary=v in G['boundary_cycle']
        inequality('vertex_in_D',polynomial(1,squares=[(-1,a),(-1,b)]),I,{'vertex':v},'unit_circle_identity' if boundary else None)
    for j in range(100):
        a,b=cidx[j];inequality('center_in_D',polynomial(1,squares=[(-1,a),(-1,b)]),sub((F(1),F(1)),norm(C[j])),{'center':j})
    incidences=0
    for face in G['faces']:
        j=face['center'];a,b=cidx[j]
        for v in face['vertices']:
            u,w=pidx[v];distance=norm([sub(P[v][d],C[j][d]) for d in (0,1)]);I=sub(T,distance);raw=G['vertices'][v];zero=None
            if raw['type']=='boundary_root_hole':need(j in sys['boundary_active_pairs'][raw['hole_index']],'boundary support');zero='accepted_boundary_distance_equation'
            elif raw['type']=='circumcenter':
                row=rows[raw['triangle_index']];need(j in row['support'],'circumcenter support')
                if row['active']:zero='unique_equidistant_point_equals_accepted_KKT_active_hole'
            polynomial_terms=polynomial(linear=[(1,ti)],squares=[(-1,u),(-1,w),(-1,a),(-1,b)],crosses=[(2,u,a),(2,w,b)])
            inequality('face_vertex_distance',polynomial_terms,I,{'center':j,'vertex':v},zero);incidences+=1
    boundary=G['boundary_cycle'];axis={'E':(1,0),'N':(0,1),'W':(-1,0),'S':(0,-1)}
    for v in boundary:
        a,b=pidx[v];eq.append({'kind':'boundary_unit_circle','terms':polynomial(-1,squares=[(1,a),(1,b)]),'metadata':{'vertex':v},'root_identity':True})
    for v,point in axis.items():
        for d,value in enumerate(point):eq.append({'kind':'axis_coordinate','terms':polynomial(-value,linear=[(1,pidx[v][d])]),'metadata':{'vertex':v,'coordinate':d},'root_identity':True})
    chains=[]
    marks=['E','N','W','S']
    for quadrant,(start,end) in enumerate(zip(marks,marks[1:]+marks[:1])):
        chain=[start];at=boundary.index(start)
        while chain[-1]!=end:at=(at+1)%len(boundary);chain.append(boundary[at]);need(len(chain)<=37,'axis cyclic order')
        chains.append(chain);signs=[(1,1),(-1,1),(-1,-1),(1,-1)][quadrant]
        for v in chain:
            for d,sign in enumerate(signs):
                I=P[v][d] if sign==1 else neg(P[v][d]);inequality('quadrant_sign',polynomial(linear=[(sign,pidx[v][d])]),I,{'quadrant':quadrant,'vertex':v,'coordinate':d})
        coordinate=[1,0,1,0][quadrant];direction=[1,-1,-1,1][quadrant]
        for a,b in zip(chain,chain[1:]):
            I=sub(P[b][coordinate],P[a][coordinate]);I=I if direction==1 else neg(I)
            inequality('boundary_monotone',polynomial(linear=[(direction,pidx[b][coordinate]),(-direction,pidx[a][coordinate])]),I,{'quadrant':quadrant,'from':a,'to':b,'coordinate':coordinate})
    need(incidences==2*301-36==566,'incidences');need(len(eq)==44 and len(ineq)==986,'actual model size')
    need(all(abs(term[0])<=2 and len(term[1])<=2 for c in eq+ineq for term in c['terms']),'quadratic small coefficients')
    out=R/'verify/out/n100-candidate-quadratic-cover-model.json';need(not out.exists(),'overwrite')
    deps=['verify/out/n100-candidate-clipped-map.json','verify/out/n100-candidate-clipped-map-independent.json','verify/out/n100-full-circumcenter-root-box.json',S+'rational_midpoint.json',S+'polynomial_system.json',S+'krawczyk_verification.json']
    out.write_text(json.dumps({'schema':'n100-candidate-quadratic-cover-model/v1','verified_compilation_and_feasibility':True,'variable_count':605,'t_index':ti,'vertex_variables':pidx,'center_variables':cidx,'vertex_sources':point_sources,'equalities':eq,'inequalities':ineq,'zero_discharges':zeros,'quadrant_chains':chains,'point_boxes':{v:[[str(a),str(b)] for a,b in P[v]] for v in names},'counts':{'equalities':len(eq),'inequalities':len(ineq),'face_vertex_incidence':incidences},'minimum_nonnegative_slack':str(min_slack),
        'analytic_dependencies':['accepted KKT root equations','unique noncollinear circumcenter','combinatorial disk manifold','folded disk filling/winding lemma','same-quadrant short-arc convex covering lemma'],
        'scope':'one feasible quadratic covering model at the local algebraic candidate; complete global map enumeration absent','formal_kernel_verified':False,'bindings':{p:sha(p) for p in deps},'checker_sha256':sha('verify/n100_candidate_quadratic_cover_model.py'),'global_optimality':False,'minimal_polynomial_obtained':False},indent=2)+'\n',encoding='utf-8')
    print('PASS candidate quadratic cover model:605 vars,44 equations,986 inequalities,566 incidences; root zero identities discharged explicitly')
if __name__=='__main__':main()
