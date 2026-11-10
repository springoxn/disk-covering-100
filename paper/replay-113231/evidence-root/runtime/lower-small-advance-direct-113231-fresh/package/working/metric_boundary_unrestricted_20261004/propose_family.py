#!/usr/bin/env python3
"""Numerical proposal only: full potentials with cyclic boundary differences."""
from pathlib import Path
from fractions import Fraction
import sys,json,time
import numpy as np
from scipy.optimize import minimize,LinearConstraint
ROOT=Path(__file__).resolve().parent.parent
M=ROOT/'signed_edge_metric_B32_20261004';sys.path.insert(0,str(M))
from propose_boundary_metric import Model
import argparse
parser=argparse.ArgumentParser();parser.add_argument('family',choices=['B32_P26_F108_'+str(i).zfill(3) for i in range(16)]);args=parser.parse_args()
g=json.loads((M/'graphs'/(args.family+'.json')).read_text())
old=json.loads((M/'proposals'/(args.family+'.json')).read_text())
m=Model(g,Fraction(283,2500));E=len(m.edges)
m.keys=[('vertex',i) for i in range(100)];m.V=np.eye(100);m.vi=np.arange(100)
m.D=np.eye(E);m.fkeys=list(range(E))
x=np.r_[old['u'],old['tau']];x[:100]-=np.mean(x[m.outer])
rows=[];lo=[];hi=[]
for face in m.faces:
 for i in range(3):
  row=np.zeros(100+E);row[face[i]]=1;row[face[(i+1)%3]]=-1
  rows.append(row);lo.append(-.3);hi.append(.3)
for i,a in enumerate(m.outer):
 b=m.outer[(i+1)%m.B];row=np.zeros(100+E);row[a]=1;row[b]=-1
 rows.append(row);lo.append(-.025);hi.append(.025)
for apex,base in zip(m.apex,m.base):
 row=np.zeros(100+E);row[apex]=1;row[base]-=.5
 rows.append(row);lo.append(-.49);hi.append(2.9)
gauge=np.zeros(100+E);gauge[m.outer]=1/m.B
constraints=[LinearConstraint(np.array(rows),lo,hi),LinearConstraint(gauge[None,:],0,0)]
initial=m.objective(x,True);started=time.monotonic()
result=minimize(m.objective,x,jac=True,method='SLSQP',
 bounds=[(-3,3)]*100+[(-.25,.25)]*E,constraints=constraints,
 options={'maxiter':180,'ftol':1e-11,'disp':False})
z=result.x*(1-1e-8);data=m.objective(z,True)
for key in ('pure_center_bound','pure_face_multipliers','vertex_labels','face_labels','vertex_label_indices','face_label_indices','vertex_label_potentials','face_label_potentials'):data.pop(key,None)
data.update(scope='NUMERICAL PROPOSAL ONLY; geometry window must use the independent frozen pure certificate',
 family_id=g['family_id'],optimizer_success=bool(result.success),optimizer_message=str(result.message),
 iterations=int(result.nit),seconds=time.monotonic()-started,
 initial_area_margin=initial['area_margin'],maximum_absolute_boundary_weight=float(max(abs(z[m.outer]))),
 mean_boundary_weight=float(np.mean(z[m.outer])),variables=len(z),independent_bootstrap='B32 frozen pure certificate and C<=230 window')
out=Path(__file__).parent/'full_boundary_proposals'/(args.family+'.json');out.write_text(json.dumps(data,indent=2))
print(json.dumps({k:v for k,v in data.items() if k not in ('u','tau','face_multipliers','edge_ids','half_arcs')},indent=2))

