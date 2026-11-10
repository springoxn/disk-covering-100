"""Reconstructed numerical graph model; no proof relies on this optimizer."""
from pathlib import Path
import sys
import numpy as np
ROOT=Path(__file__).resolve().parent.parent
sys.path.insert(0,str(ROOT/'signed_edge_metric_20261004'))
from propose_signed_graph import triangle_support
import propose_boundary_weights as old_arc
class Model:
 def __init__(self,graph,radius):
  self.g=graph;self.R=float(radius);self.T=self.R*self.R
  self.inner=graph['interior_ids'];self.outer=np.array(graph['outer_boundary_ids']);self.I=len(self.inner);self.B=len(self.outer);self.n=self.I+self.B
  assert self.inner==list(range(self.I)) and set(self.outer)==set(range(self.I,self.n))
  self.faces=np.array(graph['core_q0_triangles']+graph['ring_q0_triangles']);q1=graph['q1_triangles']
  self.apex=np.array([f['interior_apex'] for f in q1]);self.base=np.array([[x for x in f['vertices'] if x!=f['interior_apex']] for f in q1])
  inc={}
  for f,tri in enumerate(self.faces):
   for i in range(3):inc.setdefault(tuple(sorted((int(tri[(i+1)%3]),int(tri[(i+2)%3])))),[]).append((f,i))
  self.edges=[];self.inc=[]
  for edge,entries in sorted(inc.items()):
   assert len(entries) in (1,2)
   if len(entries)==2:self.edges.append(edge);self.inc.append(entries)
  self.keys=[('vertex',i) for i in range(self.n)];self.V=np.eye(self.n);self.vi=np.arange(self.n)
  self.fkeys=list(range(len(self.edges)));self.D=np.eye(len(self.edges));self.fi=np.arange(len(self.faces))
 def arc_maximum(self,a,b):
  old_arc.R=self.R;old_arc.T=self.T;old_arc.TU=np.arcsin(self.R)
  return old_arc.arc_maximum(a,b)
 def boundary(self,w):
  b=self.T*(np.roll(w,1)-2*w+np.roll(w,-1))/2;mean=np.pi/self.B;s=np.sin(mean);c=np.cos(mean);h=np.sqrt(self.T-s*s)
  z=2*s*s+c*(self.T-2*s*s)/h+b*(c/h-1)-2*self.T*w
  lo=float(min(z));hi=float(max(z));zeta=(lo+hi)/2
  for unused in range(50):
   val,t,eta=self.arc_maximum(2*self.T*w+zeta,b);derivative=np.pi-t.sum()
   if abs(derivative)<1e-11:break
   if derivative<0:lo=zeta
   else:hi=zeta
   ss=np.sin(t);cc=np.cos(t);hh=np.sqrt(np.maximum(1e-30,self.T-ss*ss))
   curvature=2*ss*(cc-hh)**2/hh+(self.T-b)*ss*(1-self.T)/hh**3
   usable=(t>old_arc.TL+1e-10)&(t<np.arcsin(self.R)-1e-10)
   second=np.sum(np.where(usable,1/np.maximum(curvature,1e-30),0));trial=zeta-derivative/max(second,1e-30)
   zeta=trial if lo<trial<hi else (lo+hi)/2
  val,t,eta=self.arc_maximum(2*self.T*w+zeta,b)
  value=(np.pi*zeta+val.sum())/self.T+np.pi*w.sum()
  gradient=np.pi-2*t-eta+(np.roll(eta,1)+np.roll(eta,-1))/2
  return value,gradient,zeta,t
 def objective(self,z,details=False):
  vk=len(self.keys);u=self.V@z[:vk];edge=self.D@z[vk:];ts=np.zeros((len(self.faces),3))
  for value,((f,i),(h,j)) in zip(edge,self.inc):ts[f,i]=value;ts[h,j]=-value
  q0,angles,eta=triangle_support(u[self.faces],ts)
  means=u[self.base].mean(axis=1);difference=u[self.base[:,0]]-u[self.base[:,1]];tilt=u[self.apex]-means
  y=(-1+np.sqrt(33+16*tilt))/8;gamma=np.arccos(y)
  marked=np.sin(gamma)*(1+2*y)-tilt*gamma-np.pi*means+(25/16)*difference*difference
  bv,bg,zeta,arcs=self.boundary(u[self.outer]);value=2*np.pi*u[:self.I].sum()+q0.sum()+marked.sum()+bv
  gu=np.zeros(self.n);gu[:self.I]=2*np.pi
  np.add.at(gu,self.faces.ravel(),-angles.ravel());np.add.at(gu,self.apex,-gamma)
  np.add.at(gu,self.base[:,0],(gamma-np.pi)/2+(25/8)*difference)
  np.add.at(gu,self.base[:,1],(gamma-np.pi)/2-(25/8)*difference);gu[self.outer]+=bg
  ge=np.array([np.sin(angles[f,i])-np.sin(angles[h,j]) for ((f,i),(h,j)) in self.inc]);gradient=np.r_[self.V.T@gu,self.D.T@ge]
  if not details:return float(value),gradient
  pu=u.copy();pu[self.outer]=0;pure_q0,_,pure_eta=triangle_support(pu[self.faces],ts)
  yy=(-1+np.sqrt(33+16*u[self.apex]))/8;gg=np.arccos(yy)
  pure=2*np.pi*u[:self.I].sum()+pure_q0.sum()+np.sum(np.sin(gg)*(1+2*yy)-u[self.apex]*gg)
  return dict(normalized_total_bound=float(value),radius=self.R,area_margin=float(np.pi-self.T*value),pure_center_bound=float(pure),
    u=u.tolist(),tau=edge.tolist(),face_multipliers=eta.tolist(),pure_face_multipliers=pure_eta.tolist(),
    arc_sum_multiplier=float(zeta),half_arcs=arcs.tolist(),edge_ids=[list(e) for e in self.edges],
    vertex_labels=self.keys,face_labels=self.fkeys,vertex_label_indices=self.vi.tolist(),face_label_indices=self.fi.tolist(),
    vertex_label_potentials=z[:vk].tolist(),face_label_potentials=z[vk:].tolist(),
    maximum_face_range=float(max(np.ptp(u[self.faces],axis=1))),
    maximum_boundary_weight_difference=float(max(abs(u[self.outer]-np.roll(u[self.outer],1)))))
