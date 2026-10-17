"""Discovery-only search for B36 constants with exact center-distance branch."""
from pathlib import Path
import json,hashlib,math
import numpy as np
from scipy.optimize import differential_evolution,minimize
ROOT=Path(__file__).resolve().parents[1];src=ROOT/'tools/n100_tail_synchronized_discover_208.py';text=src.read_text(encoding='utf-8');# reuse its evaluated objective, which already takes min(original,direct)
ns={'__file__':str(src),'__name__':'discovery214'};exec(compile(text,str(src),'exec'),ns);R=ns['R'];evaluate=ns['evaluate'];triangleK=ns['triangleK']
def obj(p):
 try:return evaluate(p)
 except Exception:return 1e3
def main():
 opt=differential_evolution(obj,[(.001,.2),(-.05,.08)],seed=214,popsize=18,maxiter=80,tol=1e-10,polish=True);loc=minimize(obj,opt.x,method='Nelder-Mead',options={'maxiter':1200,'xatol':1e-11,'fatol':1e-14});best=evaluate(loc.x,True);out=ROOT/'runtime/n100-tail-directterm-discovery-214.json';assert not out.exists();out.write_text(json.dumps({'discovery_only':True,'radius':'2831/25000','candidate':best,'source_sha256':hashlib.sha256(src.read_bytes()).hexdigest()},indent=2)+'\n');print(json.dumps(best),flush=True)
if __name__=='__main__':main()
