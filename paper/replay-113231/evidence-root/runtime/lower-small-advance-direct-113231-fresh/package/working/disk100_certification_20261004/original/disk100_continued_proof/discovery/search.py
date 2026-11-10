"""Numerical discovery only. Exact cover check is separate."""
import numpy as np,json,time,sys
from scipy.spatial import Voronoi,Delaunay
from scipy.optimize import minimize


def triangles(C,T):
    P=C[T];a=P[:,0];u=P[:,1]-a;v=P[:,2]-a
    d=u[:,0]*v[:,1]-u[:,1]*v[:,0]
    uu=np.einsum('ij,ij->i',u,u);vv=np.einsum('ij,ij->i',v,v)
    pr=np.stack((uu*v[:,1]-vv*u[:,1],u[:,0]*vv-v[:,0]*uu),1)/(2*d[:,None])
    p=a+pr; g=np.einsum('ij,ij->i',pr,pr)
    w1=(pr[:,0]*v[:,1]-pr[:,1]*v[:,0])/d
    w2=(u[:,0]*pr[:,1]-u[:,1]*pr[:,0])/d
    w=np.stack((1-w1-w2,w1,w2),1)
    grad=2*w[:,:,None]*(P-p[:,None,:])
    return g,p,grad

def boundary(C,E,sg):
    a,b=C[E[:,0]],C[E[:,1]];u=b-a
    ss=np.einsum('ij,ij->i',u,u);h=(np.einsum('ij,ij->i',b,b)-np.einsum('ij,ij->i',a,a))/2
    z=np.sqrt(np.maximum(1e-20,ss-h*h))
    up=np.stack((-u[:,1],u[:,0]),1)
    q=(h[:,None]*u+(sg*z)[:,None]*up)/ss[:,None]
    tangent=np.stack((-q[:,1],q[:,0]),1)
    wi=np.einsum('ij,ij->i',b,tangent)/np.einsum('ij,ij->i',u,tangent)
    w=np.stack((wi,1-wi),1)
    grad=2*w[:,:,None]*(C[E]-q[:,None,:])
    g=np.einsum('ij,ij->i',q-a,q-a)
    return g,q,grad

def topology(C):
    dt=Delaunay(C);T=dt.simplices.copy()
    g,p,grad=triangles(C,T)
    T=T[np.sum(p*p,axis=1)<1]
    # Use all Delaunay edges to find the relevant bisector intersections.
    ep=np.sort(np.concatenate((dt.simplices[:,[0,1]],dt.simplices[:,[1,2]],dt.simplices[:,[0,2]])),axis=1)
    E=np.unique(ep,axis=0);E=np.repeat(E,2,axis=0);sg=np.tile([-1,1],len(E)//2)
    g,q,_=boundary(C,E,sg)
    ds=np.sum((q[:,None,:]-C[None,:,:])**2,axis=-1)
    valid=np.min(ds,axis=1)>g-1e-10
    E,sg,q=E[valid],sg[valid],q[valid]
    order=np.argsort(np.arctan2(q[:,1],q[:,0]));E,sg=E[order],sg[order]
    return T,E,sg

def covering(C):
    T,E,sg=topology(C)
    tg,p,_=triangles(C,T);bg,q,_=boundary(C,E,sg)
    return np.sqrt(max(tg.max(),bg.max())),(T,E,sg)

class Model:
    def __init__(self,C,top):
        self.T,self.E,self.sg=top;self.n=len(C);self.mt=len(self.T);self.m=self.mt+len(self.E);self.last=None
        self.tcols=(2*self.T[:,:,None]+np.array([0,1])[None,None,:]).reshape((self.mt,6))
        self.ecols=(2*self.E[:,:,None]+np.array([0,1])[None,None,:]).reshape((len(self.E),4))
    def ev(self,x):
        if self.last is not None and np.array_equal(x,self.last):return self.gv,self.gj
        C=x[:-1].reshape(-1,2);r=x[-1]
        tg,p,tj=triangles(C,self.T);bg,q,bj=boundary(C,self.E,self.sg)
        g=np.r_[tg,bg];J=np.zeros((self.m,2*self.n+1))
        J[np.arange(self.mt)[:,None],self.tcols]=tj.reshape(self.mt,6)
        J[self.mt+np.arange(len(bg))[:,None],self.ecols]=bj.reshape(len(bg),4)
        J[:,-1]=-2*r
        self.gv=(r*r-g)*100;self.gj=-100*J;self.last=x.copy()
        return self.gv,self.gj
    def con(self,x):return self.ev(x)[0]
    def jac(self,x):return self.ev(x)[1]

def refine(C,maxiter=500,steps=3,verbose=False,trust=.06):
    C=C.copy();best_r,top=covering(C);best=C.copy()
    for step in range(steps):
        model=Model(C,top);r,_=covering(C);x0=np.r_[C.reshape(-1),r+1e-10]
        lower=np.r_[C.reshape(-1)-trust,.1];upper=np.r_[C.reshape(-1)+trust,.2]
        res=minimize(lambda x:x[-1],x0,jac=lambda x:np.r_[np.zeros(2*len(C)),1.],method='SLSQP',
            constraints=[{'type':'ineq','fun':model.con,'jac':model.jac}],
            bounds=list(zip(lower,upper)),options={'maxiter':maxiter,'ftol':1e-13,'disp':False})
        C=res.x[:-1].reshape(-1,2);r,top=covering(C)
        if verbose:print('step',step,'radius',r,'objective',res.x[-1],'nit',res.nit,'message',res.message,flush=True)
        if r<best_r:best_r=r;best=C.copy()
        if res.success and abs(r-res.x[-1])<1e-10:break
    return best_r,best

if __name__=='__main__':
    C=np.load(__import__('pathlib').Path(__file__).resolve().parent/'initial.npy')
    t=time.time();r,C=refine(C,verbose=True,steps=5)
    print('FINAL',r,'seconds',time.time()-t,flush=True)
    np.save(__import__('pathlib').Path(__file__).resolve().parent/'local_best.npy',C)
