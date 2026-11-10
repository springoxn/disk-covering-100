import os
os.environ['OPENBLAS_NUM_THREADS']='1';os.environ['OMP_NUM_THREADS']='1'
import numpy as np,time,json,sys
from multiprocessing import Pool
from search import refine,covering
DIR=os.path.dirname(os.path.abspath(__file__))

def seed_C(idx):
    rng=np.random.default_rng(920481+idx)
    if idx<120:
        C=np.load(DIR+'/local_best.npy')
        amps=[.008,.02,.04,.065,.09,.14]
        amp=amps[idx%6]
        # heterogeneous/local rearrangements mixed with global small perturbations
        if idx%3==0:
            p=C[rng.integers(100)];ww=np.exp(-np.sum((C-p)**2,1)/.12)
            C+=rng.normal(size=C.shape)*amp*ww[:,None]
        elif idx%3==1:C+=rng.normal(size=C.shape)*amp
        else:
            j=rng.integers(100);r,top=covering(C)
            from search import triangles
            g,p,gr=triangles(C,top[0]);order=np.argsort(g)
            pick=order[rng.integers(max(0,len(order)-40),len(order))]
            C[j]=p[pick]+rng.normal(size=2)*amp
            C+=rng.normal(size=C.shape)*.002
        return C
    if idx<240:
        v=np.array([(a+b*.5,b*np.sqrt(3)/2) for a in range(-12,13) for b in range(-12,13)])
        v+=rng.uniform(-.6,.6,2)
        v[:,0]*=rng.uniform(.94,1.06)
        val=np.sum(v*v,axis=1);v=v[np.argsort(val)[:100]]
        v*=rng.uniform(.93,1.04)/np.max(np.linalg.norm(v,axis=1))
        # smooth compress boundary layer
        v+=rng.normal(size=v.shape)*rng.choice([.001,.003,.01,.02])
        return v
    sets=[([1,6,12,21,27,33],[0,.195,.385,.57,.753,.938]),
          ([1,6,12,18,30,33],[0,.195,.385,.57,.753,.938]),
          ([1,6,12,18,27,36],[0,.195,.385,.57,.753,.938]),
          ([1,7,13,21,25,33],[0,.195,.385,.57,.753,.938]),
          ([1,6,13,20,26,34],[0,.195,.385,.57,.753,.938]),
          ([1,7,14,21,27,30],[0,.195,.385,.57,.753,.938]),
          ([4,12,20,28,36],[.108,.308,.516,.724,.935]),
          ([5,10,20,30,35],[.108,.308,.516,.724,.935]),
          ([3,10,21,32,34],[.095,.3,.51,.72,.935]),
          ([2,8,19,31,40],[.07,.27,.49,.71,.935]),
          ([3,9,18,30,40],[.09,.29,.505,.725,.937]),
          ([1,8,15,22,24,30],[0,.198,.39,.575,.755,.94])]
    counts,rads=sets[(idx-240)%len(sets)]
    C=[]
    for n,r in zip(counts,rads):
        a=np.arange(n)*2*np.pi/n+rng.uniform(0,2*np.pi)
        C.extend(np.stack([r*np.cos(a),r*np.sin(a)],1))
    C=np.array(C);C+=rng.normal(size=C.shape)*rng.choice([1e-5,.001,.005,.01,.03])
    return C

def job(idx):
    try:
        t=time.time();C=seed_C(idx);r0,_=covering(C)
        r,C=refine(C,maxiter=200,steps=3,trust=.11 if idx>=120 else .075)
        np.save(f'{DIR}/trials/{idx:04}.npy',C)
        return {'idx':idx,'initial':r0,'radius':r,'seconds':time.time()-t}
    except Exception as e:return {'idx':idx,'error':str(e)}

if __name__=='__main__':
    os.makedirs(DIR+'/trials',exist_ok=True);ts=time.time();best=.11573102001;out=[]
    n=int(sys.argv[1]) if len(sys.argv)>1 else 360
    with Pool(4) as pool:
        for x in pool.imap_unordered(job,range(n),chunksize=1):
            out.append(x)
            if 'radius'in x and x['radius']<best:
                best=x['radius'];np.save(DIR+'/best_search.npy',np.load(f'{DIR}/trials/{x["idx"]:04}.npy'))
                print('BEST',x,flush=True)
            if len(out)%20==0:print('PROGRESS',len(out),n,'best',best,'elapsed',time.time()-ts,flush=True)
            with open(DIR+'/multistart_results.json','w')as f:json.dump(out,f,indent=2)
    print('DONE',best,time.time()-ts,flush=True)
