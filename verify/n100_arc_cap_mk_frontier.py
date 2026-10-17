"""Discover service-count consequences of the certified arc-cap support.
The existing support certificate is reused only as an arithmetic bound; no B=k bridge.
"""
from pathlib import Path
from fractions import Fraction as F
from math import ceil
import json,hashlib,argparse
ROOT=Path(__file__).resolve().parents[1]
def need(ok,msg):
    if not ok:raise ValueError(msg)
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--out',default='verify/out/n100-arc-cap-mk-frontier.json');args=ap.parse_args()
    p=ROOT/'verify/out/n100-arc-cap-rational-support.json';z=json.loads(p.read_text(encoding='utf-8'))
    r=F(z['radius']);delta=F(z['delta']);a=F(z['slope']);M=F(z['maximum_half_arc_upper']);pl,ph=F(314159,100000),F(314160,100000)
    # For each effective site count m, find largest k excluded by the same support.
    rows=[]
    for m in range(76,101):
        excluded=[]
        for k in range(0,m+1):
            s=1-2*r+delta;margin=pl*s*s-(m-k)*ph*r*r-a*(k*M-pl)
            if margin>0:excluded.append(k)
        max_allowed=max([k for k in range(m+1) if k not in excluded],default=-1)
        rows.append({'m':m,'excluded_k':excluded,'largest_not_excluded_k':max_allowed})
    need(rows[-1]['excluded_k']==list(range(55,101)),'m100 frontier')
    # Existing 87-family domain.
    front=json.loads((ROOT/'verify/out/n100-vonequinox-count-domain-bound.json').read_text(encoding='utf-8'))['surviving_m_B_families']
    family=[];removed=[]
    for m,b in front:
        # B<=k means any compatible k must satisfy k>=B; remove only if every k>=B is excluded.
        row=rows[m-76];possible=[k for k in range(b,m+1) if k not in row['excluded_k']]
        if possible:family.append([m,b,possible[0],possible[-1]])
        else:removed.append([m,b])
    need(len(removed)==0 and len(family)==87,'no family overclaim')
    out=ROOT/args.out;need(not out.exists(),'overwrite')
    out.write_text(json.dumps({'schema':'n100-arc-cap-mk-frontier/v1','verified':True,'frontier':rows,'surviving_m_B_families':len(front),'removed_m_B_families':removed,'remaining_m_B_families':family,'bridge_used':'only B<=k; no equality','new_m_B_families_excluded':0,'global_optimality':False,'machine_verified_geometry':False,'input_sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'scope':'arithmetic consequence of stage28 support; analytic geometry dependencies inherited; no global map enumeration'},indent=2)+'\n',encoding='utf-8');print('PASS m-k frontier:',[(r['m'],r['largest_not_excluded_k']) for r in rows[-5:]],'; 87 families retained')
if __name__=='__main__':main()
