import os
os.environ['OPENBLAS_NUM_THREADS']='1';os.environ['OMP_NUM_THREADS']='1'
from multiprocessing import Pool
import numpy as np,json,time
from pathlib import Path
from search import refine,covering,triangles
D=Path(__file__).resolve().parent

def run(seed):
    rng=np.random.default_rng(11745+seed);C=np.load(D/'best_search.npy');r,_=covering(C)
    best=r;bestC=C.copy();records=[];t=time.time()
    for it in range(220):
        start=C.copy();amp=rng.choice([.006,.015,.03,.045,.065,.09],p=[.12,.18,.25,.2,.15,.1]);mode=rng.integers(5)
        if mode==0:
            start+=rng.normal(size=start.shape)*amp
        elif mode==1:
            p=C[rng.integers(100)];w=np.exp(-np.sum((C-p)**2,1)/rng.choice([.04,.12,.25]));start+=rng.normal(size=start.shape)*amp*w[:,None]
        elif mode==2:
            _,top=covering(C);g,p,_=triangles(C,top[0]);j=rng.integers(100)
            kk=np.argsort(g)[rng.integers(max(0,len(g)-55),len(g))];start[j]=p[kk]+rng.normal(size=2)*.02
            start+=rng.normal(size=start.shape)*.001
        elif mode==3:
            angle=rng.uniform(0,2*np.pi);u=np.array([np.cos(angle),np.sin(angle)]);v=np.array([-u[1],u[0]])
            region=np.sign(start@u)*np.exp(-((start@u)/.3)**2)
            start+=region[:,None]*v[None,:]*amp
        else:
            p=C[rng.integers(100)];w=np.exp(-np.sum((C-p)**2,1)/.15)
            rot=rng.uniform(-1,1)*amp*12
            rel=start-p;step=np.stack([-rel[:,1],rel[:,0]],1)
            start+=rot*w[:,None]*step
        try:nr,nc=refine(start,maxiter=180,steps=2,trust=.12)
        except Exception as e:
            records.append({'it':it,'error':str(e)});continue
        T=0.00012*(.3+.7*(1-(it%55)/55))
        acc=nr<r or rng.random()<np.exp(min(0,(r-nr)/T))
        if acc:r,C=nr,nc
        if nr<best:
            best,bestC=nr,nc.copy();np.save(D/f'basin_best_{seed}.npy',bestC)
            print('BEST',seed,it,best,'elapsed',time.time()-t,flush=True)
        records.append({'it':it,'radius':nr,'accepted':bool(acc),'best':best,'mode':int(mode),'amp':float(amp)})
        if it%25==24:
            print('PROGRESS',seed,it+1,best,'elapsed',time.time()-t,flush=True)
            (D/f'basin_{seed}.json').write_text(json.dumps(records,indent=2))
        if it%55==54:
            C=bestC.copy();r=best
    (D/f'basin_{seed}.json').write_text(json.dumps(records,indent=2))
    return seed,best

if __name__=='__main__':
    with Pool(4) as pool:
        for x in pool.imap_unordered(run,range(4)):print('DONE',x,flush=True)
