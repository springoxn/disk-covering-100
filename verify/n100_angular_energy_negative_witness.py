"""Exact negative witness for the true reduced angular energy Hessian at the root box."""
from pathlib import Path
from fractions import Fraction as F
import json,hashlib,math
ROOT=Path(__file__).resolve().parents[1]
HERE=ROOT/'runtime/n100-vonequinox-transfer'
CERT=json.loads((HERE/'certificate.json').read_text())
MID=json.loads((ROOT/'runtime/external-disk100-strict-local-replay/source/rational_midpoint.json').read_text())
D=int(MID['denominator']);rho=F(100,D);GRID=int(CERT['grid_denominator']);G=F(CERT['Gamma'])
N=32
q=[]
for i in range(N):
 x=F(int(MID['numerators'][428+2*i]),D);y=F(int(MID['numerators'][429+2*i]),D);q.append((x,y))
C=[[F(0)]*N for _ in range(N)]
for key,val in CERT['c0_lower_triangle'].items():
 i,j=map(int,key.split(','));c0=F(val);cl=F(math.floor(max(F(0),c0-G)*GRID),GRID);ch=F(math.ceil((c0+G)*GRID),GRID);C[i][j]=C[j][i]=(cl+ch)/2
H=[[F(0)]*N for _ in range(N)]
for i in range(N):
 for j in range(i+1,N):
  z=q[i][0]*q[j][0]+q[i][1]*q[j][1];a=2*C[i][j]*z
  H[i][i]+=a;H[j][j]+=a;H[i][j]-=a;H[j][i]-=a
# fixed rational eigenvector found from exploratory solve, denominator 1e12
v=[F(x,10**12) for x in [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]]
# replace by a deterministic vector from numpy output stored separately in this script below
import numpy as np
A=np.array([[float(x) for x in row] for row in H]);w,V=np.linalg.eigh(A[1:,1:]);vv=V[:,0];v=[F(0)]+[F(int(round(x*10**12)),10**12) for x in vv]
q0=sum(v[i]*H[i][j]*v[j] for i in range(N) for j in range(N))
# conservative interval: each coordinate perturbation <=rho; |d(q_i dot q_j)| <= 4rho+2rho^2;
# each H entry has at most N incident conductances, and |dc| <= G + 1/GRID.
doterr=4*rho+2*rho*rho; cerr=G+F(1,GRID)
entryerr=2*(cerr+(max(max(row) for row in C)+cerr)*doterr)
err=entryerr*sum((v[i]-v[j])**2 for i in range(N) for j in range(i+1,N))
assert q0+err<0
out={'schema':'n100-angular-energy-negative-witness/v1','source_analysis':'runtime/n100-vonequinox-transfer/analysis.py','root_box_denominator':D,'root_box_radius':'1e-58','gamma':str(G),'witness_denominator':10**12,'witness':[str(x) for x in v], 'midpoint_quadratic_form':str(q0),'root_box_abs_error_bound':str(err),'interval_upper_bound':str(q0+err),'strictly_negative':q0+err<0,'interpretation':'true reduced harmonic energy Hessian is not PSD at this candidate root box; this rejects the convexity certificate route, not the covering optimum and not the local constrained SOSC','checker_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
p=ROOT/'verify/out/n100-angular-energy-negative-witness.json'
if p.exists(): raise FileExistsError(p)
p.write_text(json.dumps(out,indent=2)+'\n')
print('PASS exact angular Hessian witness',q0,'error',err,'upper',q0+err)
