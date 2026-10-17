"""Exact algebra behind strict-radius generic clipped-Voronoi reduction.
Certifies identities and nonzero obstruction polynomials, not density/topology.
"""
from pathlib import Path
from collections import Counter
from fractions import Fraction as F
import sympy as S
import json,hashlib,argparse
from n100_dart_map_canonicalization import permutations
from n100_dart_independent_canonicalization import loops
ROOT=Path(__file__).resolve().parents[1]
def need(x,msg):
    if not x:raise ValueError(msg)
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--out',default='verify/out/n100-generic-strict-map-reduction.json');args=ap.parse_args()
    rho,h,x,y=S.symbols('rho h x y',real=True);checks={}
    # Outside center (rho,0), rho>1, projection (1,0), x<=1.
    checks['projection_gap']=S.expand((x-rho)**2+y*y-((x-1)**2+y*y)-(rho-1)*(rho+1-2*x))==0
    # Lipschitz estimate follows from triangle inequality; certify norm-square expansion.
    ax,ay,dx,dy=S.symbols('ax ay dx dy',real=True)
    checks['perturbation_norm_square']=S.expand((ax+dx)**2+(ay+dy)**2-(ax*ax+ay*ay+2*(ax*dx+ay*dy)+dx*dx+dy*dy))==0
    X=S.symbols('x0:4');Y=S.symbols('y0:4')
    a=S.Matrix([X[1]-X[0],Y[1]-Y[0]]);b=S.Matrix([X[2]-X[0],Y[2]-Y[0]]);det=a[0]*b[1]-a[1]*b[0]
    # Circumcenter = N/(2det), in unscaled coordinates.
    aa=a.dot(a);bb=b.dot(b);Nx=2*det*X[0]+aa*b[1]-bb*a[1];Ny=2*det*Y[0]+a[0]*bb-b[0]*aa
    cx,cy=Nx/(2*det),Ny/(2*det)
    checks['circumcenter_pair01']=S.factor((cx-X[0])**2+(cy-Y[0])**2-(cx-X[1])**2-(cy-Y[1])**2)==0
    checks['circumcenter_pair02']=S.factor((cx-X[0])**2+(cy-Y[0])**2-(cx-X[2])**2-(cy-Y[2])**2)==0
    predicates={
        'pair_coincidence':(X[0]-X[1])**2+(Y[0]-Y[1])**2,
        'three_collinear':det,
        'four_cocircular':S.det(S.Matrix([[X[i],Y[i],X[i]**2+Y[i]**2,1] for i in range(4)])),
        'triple_circumcenter_on_unit_circle':S.expand(Nx*Nx+Ny*Ny-4*det*det)}
    for j,(px,py) in enumerate(((1,0),(0,1),(-1,0),(0,-1))):predicates['pair_tie_at_axis_'+str(j)]=(X[0]-px)**2+(Y[0]-py)**2-(X[1]-px)**2-(Y[1]-py)**2
    sample={X[0]:0,Y[0]:0,X[1]:S.Rational(1,4),Y[1]:0,X[2]:0,Y[2]:S.Rational(1,4),X[3]:S.Rational(1,2),Y[3]:S.Rational(1,2)}
    nonzero={}
    for label,poly in predicates.items():
        value=S.expand(poly).subs(sample);need(value!=0,'nonzero witness '+label)
        nonzero[label]={'polynomial':str(S.expand(poly)),'degree':int(S.Poly(poly,*X,*Y).total_degree()),'rational_sample_value':str(value),'not_identically_zero':True}
    # Bisector passes through midpoint of two interior sites, hence cannot be tangent to circle.
    # This convexity claim is explicitly analytic, no extra tangent hypersurface needed.
    V,E,m=S.symbols('V E m',integer=True)
    solution=S.solve([V-E+m-1,2*E-3*V+4],[V,E]);need(solution=={V:2*m+2,E:3*m+1},'budget')
    checks['generic_euler_budget']=True
    need(all(checks.values()),'identities')
    source=ROOT/'verify/out/n100-candidate-clipped-map.json';g=json.loads(source.read_text(encoding='utf-8'));phi,tags=permutations(g);vc=loops([phi[d^1] for d in range(len(phi))]);hist=Counter(map(len,vc))
    need(hist==Counter({3:198,2:4}),'candidate generic degree inventory')
    need((len(g['vertices']),len(g['edges']),len(g['faces']))==(202,301,100),'candidate budget')
    # Recover exact axis tags per vertex orbit, ensure all four degree2 vertices are axes.
    degree2=[]
    for row in vc:
        if len(row)==2:
            mark={tags[d][1] for d in row};need(len(mark)==1 and '' not in mark,'axis degree2');degree2.append(next(iter(mark)))
    need(sorted(degree2)==list('0123'),'axis tags')
    out=ROOT/args.out;need(not out.exists(),'overwrite')
    output={'schema':'n100-generic-strict-map-reduction/v1','verified_symbolic_and_integer':True,'checks':checks,'proper_algebraic_obstructions':nonzero,'template_instance_reason':'Distinct-index instances are obtained from each nonzero template by renaming site variables; this automorphism preserves nonzero polynomials. Only one witness per template is computed.', 'projection_identity_scope':'rotated outside-center case only; full metric projection and Lipschitz estimates are analytic dependencies', 'bisector_transversality_scope':'distinct sites strictly in the open unit disk; midpoint has norm<1 and lies on the bisector', 'sample_sites':[['0','0'],['1/4','0'],['0','1/4'],['1/2','1/2']],
        'generic_budget':{'vertices':'2*m+2','edges':'3*m+1','axes_degree':2,'other_vertices_degree':3,'boundary_intersection_budget':'V_int=2*m-b-2, V=V_int+b+4=2*m+2; b is free'},'candidate_degree_histogram':dict(hist),'candidate_budget_matches':True,
        'analytic_dependencies':['metric projection onto unit disk does not increase distances to target points','covering radius is 1-Lipschitz in maximum center displacement','interior distinct configurations avoiding finitely many nonzero polynomial zero sets are dense','clipped nearest-site cells of distinct interior sites are full-dimensional convex Jordan cells and cover the disk','generic Voronoi vertices have exactly3 cells; no triple tie on circle; bisectors meet circle transversely','inserting four axis points absent from original skeleton creates exactly four degree2 vertices','Euler formula for a connected disk cell decomposition'],
        'conditional_theorem':'Every cover of radius r<R<1 with n disks admits a compiler-valid generic clipped-Voronoi map at radius r_prime<R with m<=n, V=2m+2 and E=3m+1, under the listed analytic lemmas. No claim at an isolated exact cutoff without slack.',
        'machine_verified_geometry':False,'complete_n100_map_enumeration':False,'global_optimality':False,'scope':'strict-cutoff necessity reduction, not enumeration completeness or exclusion; m and boundary-service counts are not asserted invariant under projection',
        'bindings':{str(source.relative_to(ROOT)):hashlib.sha256(source.read_bytes()).hexdigest()},'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'sympy_version':S.__version__}
    out.write_text(json.dumps(output,indent=2)+'\n',encoding='utf-8');print('PASS strict generic reduction: projection/circumcenter identities;8 proper algebraic obstructions;Euler exact budgets;candidate degrees198x3+4x2;analytic density/topology nonformal')
if __name__=='__main__':main()
