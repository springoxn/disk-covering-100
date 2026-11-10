"""Reconstructed numerical proposal kernel; never an acceptance backend."""
import numpy as np
def scalar(tau,w):
 disc=np.sqrt(np.maximum(0,tau*tau+8*(1+w)))
 candidates=[np.zeros_like(w),np.full_like(w,np.pi/2)]
 for sign in (-1,1):
  root=(-tau+sign*disc)/4
  angle=np.arccos(np.clip(root,0,1))
  angle=np.where((tau*tau+8*(1+w)>=0)&(root>=0)&(root<=1),angle,np.nan)
  candidates.append(angle)
 angles=np.stack(candidates);values=.5*np.sin(2*angles)+tau[None]*np.sin(angles)-w[None]*angles
 values=np.where(np.isnan(values),-np.inf,values);chosen=np.argmax(values,axis=0)
 return np.take_along_axis(values,chosen[None],axis=0)[0],np.take_along_axis(angles,chosen[None],axis=0)[0]
def triangle_support(c,tau):
 lo=-1-np.max(abs(tau),axis=1)-c.max(axis=1)-.001
 hi=1+np.max(abs(tau),axis=1)-c.min(axis=1)+.001
 lam=-.5-c.mean(axis=1)
 for unused in range(45):
  v,a=scalar(tau,c+lam[:,None]);derivative=np.pi-a.sum(axis=1)
  lo=np.where(derivative<0,lam,lo);hi=np.where(derivative>=0,lam,hi)
  denom=2*np.sin(2*a)+tau*np.sin(a)
  interior=(a>1e-10)&(a<np.pi/2-1e-10)&(denom>1e-12)
  curvature=np.sum(np.where(interior,1/np.maximum(denom,1e-12),0),axis=1)
  trial=lam-derivative/np.maximum(curvature,1e-12)
  if max(abs(derivative))<1e-11:break
  lam=np.where((trial>lo)&(trial<hi),trial,(lo+hi)/2)
 v,a=scalar(tau,c+lam[:,None])
 return np.pi*lam+v.sum(axis=1),a,lam
