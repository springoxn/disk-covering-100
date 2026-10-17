"""Exact algebraic checks for projection and cover transfer relations.
Analytic set-containment proofs are stated in docs/n100-lifting-and-cover-transfers.md.
"""
import json,hashlib
from pathlib import Path
import sympy as s
from fractions import Fraction as F
ROOT=Path(__file__).resolve().parents[1]
x,y,cx,cy,z,r=s.symbols('x y cx cy z r',real=True)
projection=s.expand((x-cx)**2+(y-cy)**2+z*z-((x-cx)**2+(y-cy)**2))
assert projection==z*z
# Rational tilt: cos beta=3/5, sin beta=4/5; regular C5 ring lifts as
# (cos theta, (3/5)sin theta, (4/5)sin theta); its projected dot metric differs.
a,b=s.symbols('a b',real=True)
lift=s.Matrix([s.cos(a),s.Rational(3,5)*s.sin(a),s.Rational(4,5)*s.sin(a)])
liftb=lift.subs(a,b)
assert s.trigsimp(lift.dot(liftb)-s.cos(a-b))==0
proj=lift[:2];projb=liftb[:2]
loss=s.trigsimp(lift.dot(liftb)-sum(xx*yy for xx,yy in zip(proj,projb)))
assert s.simplify(loss-s.Rational(16,25)*s.sin(a)*s.sin(b))==0
# C5 rotation cannot preserve projected norms: theta=0 norm=1;
# theta=2pi/5 gives norm^2=1-(16/25)sin^2(2pi/5)<1.
sin2=s.simplify(s.sin(2*s.pi/5)**2)
assert sin2== (5+s.sqrt(5))/8
assert s.simplify(1-(s.cos(2*s.pi/5)**2+s.Rational(9,25)*sin2))==(10+2*s.sqrt(5))/25
# exact example of refinement center formula: z_j+a*d_l.
# Relative distance to refined center = (x-z_j)-a*d_l, obeys scaling identity.
xx,yy,aa,dx,dy=s.symbols('xx yy aa dx dy',real=True)
assert s.expand((aa*xx-aa*dx)**2+(aa*yy-aa*dy)**2-aa**2*((xx-dx)**2+(yy-dy)**2))==0
# Coarsening square inequality algebra: |u+v|<=a+r from CS and norm bounds.
A,R=s.symbols('A R',nonnegative=True)
assert s.expand(A*A+2*A*R+R*R-(A+R)**2)==0
checks={'orthogonal_projection_distance_loss_squared':str(projection),'tilted_C5_lift_Gram_identity':True,'projection_metric_loss':str(loss),'projected_C5_norm_noninvariance_exact':str((10+2*s.sqrt(5))/25),'refinement_scaling_identity':True,'coarsening_triangle_bound_identity':True}
out={'schema':'cover-transfer-identities/v1','verified':True,'checks':checks,'analytic_premises':'orthogonal projection Pythagoras, triangle inequality, covering set containment; separately proved in linked note','transfer_inequalities':['r_D(k*m) <= r_D(k)*r_D(m)','grouped known n-cover yields k-cover with radius r+max group enclosure radii'],'converse_equality_claimed':False,'n100_global_optimality_proved':False,'checker_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
p=ROOT/'verify/out/n100-cover-transfer-identities.json'
if p.exists():raise FileExistsError(p)
p.write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8');print('PASS projection, hidden-C5 example, refinement and coarsening exact identities; no optimality equivalence claimed')
