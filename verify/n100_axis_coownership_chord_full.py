"""Fixed-axis co-ownership chord lower bounds on all retained placements."""
from pathlib import Path
from itertools import combinations
from collections import Counter
from fractions import Fraction as F
import json,hashlib,argparse
from n100_dart_independent_canonicalization import loops,need
ROOT=Path(__file__).resolve().parents[1];U=F(1154469548855829,10**16);AX=((1,0),(0,1),(-1,0),(0,-1))
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--out',default='verify/out/n100-axis-coownership-chord-full.json');args=ap.parse_args();load=lambda p:json.loads(p.read_text(encoding='utf-8'))
 cp=ROOT/'verify/out/n100-cubic-core-roundtrip.json';bp=ROOT/'verify/out/n100-axis-dual-chain-pruning.json';core=load(cp)['core'];prior=load(bp);A=core['alpha'];fc=loops(core['phi']);own={d:i for i,row in enumerate(fc) for d in row};outer=next(i for i,row in enumerate(fc) if core['core_tags'][row[0]][0]=='outer');boundary=[A[d] for d in reversed(fc[outer])];owners=[own[d] for d in boundary];bad=[];hist=Counter()
 for p in prior['retained_axis_edge_placements']:
  by={i:owners[p[i]] for i in range(4)};fails=[]
  for i,j in combinations(range(4),2):
   if by[i]!=by[j]:continue
   d2=sum((AX[i][q]-AX[j][q])**2 for q in (0,1));lb=F(d2,4)
   if lb>U*U:fails.append({'pair':[i,j],'face_pair':[by[i],by[j]],'lower_t':str(lb),'gap':str(lb-U*U)})
  if fails:bad.append({'placement':p,'fails':fails});hist[len(fails)]+=1
 candidate=load(ROOT/'verify/out/n100-axis-subdivision-pruning.json')['candidate_axis_edge_indices'];out=ROOT/args.out;need(not out.exists(),'overwrite');out.write_text(json.dumps({'schema':'n100-axis-coownership-chord-full/v1','verified':True,'placements':len(prior['retained_axis_edge_placements']),'excluded_count':len(bad),'excluded':bad,'candidate_retained':candidate not in [x['placement'] for x in bad],'axis_pair_lower_t':str(F(1,2)),'u_squared':str(U*U),'scope':'all retained placements; tests only whether one face owns two fixed axes, no unknown boundary angles','machine_verified_geometry':False,'global_optimality':False,'histogram':dict(hist),'bindings':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in (cp,bp)},'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()},indent=2)+'\n',encoding='utf-8');print('PASS axis coownership full scan',len(prior['retained_axis_edge_placements']),'placements;excluded',len(bad))
if __name__=='__main__':main()
