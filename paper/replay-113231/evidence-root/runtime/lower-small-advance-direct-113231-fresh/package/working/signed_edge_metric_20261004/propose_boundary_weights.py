"""Reconstructed numerical arc proposals; exact acceptance is separate."""
import numpy as np
R=.1131;T=R*R;TL=.04;TU=np.arcsin(R)
def arc_maximum(a,b):
 a=np.asarray(a);b=np.asarray(b)
 A=4*(a-1);B=-4*T*(a+b)-(a+b)**2+4*(T+b)+(T+b)**2;C=T*(a+b)**2-(T+b)**2
 disc=B*B-4*A*C;root=np.sqrt(np.maximum(0,disc))
 points=[np.full_like(a,TL),np.full_like(a,TU)]
 for sign in (-1,1):
  u=(-B+sign*root)/(2*A);good=(disc>=0)&(u>=np.sin(TL)**2)&(u<=T)
  points.append(np.where(good,np.arcsin(np.sqrt(np.clip(u,0,T))),np.nan))
 angles=np.stack(points);s=np.sin(angles);c=np.cos(angles);h=np.sqrt(np.maximum(0,T-s*s))
 eta=np.arcsin(np.clip(s/R,0,1))-angles
 values=(1-a[None])*angles-s*c+s*h+b[None]*eta
 values=np.where(np.isnan(values),-np.inf,values);chosen=np.argmax(values,axis=0)
 return (np.take_along_axis(values,chosen[None],axis=0)[0],
         np.take_along_axis(angles,chosen[None],axis=0)[0],
         np.take_along_axis(eta,chosen[None],axis=0)[0])
