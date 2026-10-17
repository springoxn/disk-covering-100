"""Stress audit for independent dart canonicalization on many random relabelings."""
from pathlib import Path
import json,hashlib,random,copy
from n100_dart_independent_canonicalization import canon,need
from n100_dart_map_canonicalization import permutations as adapt
ROOT=Path(__file__).resolve().parents[1]
def relabel(data,seed):
    a,p,t=data;n=len(a);rng=random.Random(seed);labels=list(range(n));rng.shuffle(labels);A=[0]*n;P=[0]*n;T=[None]*n
    for d,e in enumerate(labels):A[e]=labels[a[d]];P[e]=labels[p[d]];T[e]=t[d]
    return A,P,T,labels
def main():
    source=ROOT/'verify/out/n100-candidate-clipped-map.json';z=json.loads(source.read_text(encoding='utf-8'));p,t=adapt(z);base=([d^1 for d in range(len(p))],p,[t[d] for d in range(len(p))]);code=canon(*base)[0]
    witnesses=[]
    for seed in range(100):
        q=relabel(base,seed);need(canon(q[0],q[1],q[2])[0]==code,'random relabel code');witnesses.append({'seed':seed,'bijection':len(set(q[3]))==len(q[3])})
    rejected=[]
    tag_changed=False
    for label,mutate in [('broken_pair',lambda q:q[0].__setitem__(0,q[0][2])),('broken_phi',lambda q:q[1].__setitem__(0,q[1][1]))]:
        q=[list(v) for v in base];mutate(q)
        try:canon(q[0],q[1],q[2])
        except (ValueError,KeyError,TypeError):rejected.append(label)
    q=[list(v) for v in base];q[2][0]=['bad','tag'];tag_changed=canon(q[0],q[1],q[2])[0]!=code
    need(len(rejected)==2 and tag_changed,'negative controls')
    # Ensure the original independent result remains bound and not silently replaced.
    old=ROOT/'verify/out/n100-dart-independent-canonicalization.json';oldz=json.loads(old.read_text(encoding='utf-8'));need(oldz['candidate_darts']==len(p),'candidate count')
    out=ROOT/'verify/out/n100-dart-canonicalization-stress.json';need(not out.exists(),'overwrite');out.write_text(json.dumps({'schema':'n100-dart-canonicalization-stress/v1','verified':True,'random_relabelings':100,'all_codes_equal':True,'bijections_checked':100,'negative_controls_rejected':rejected,'changed_tag_code_detected':tag_changed,'input_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'prior_independent_certificate_sha256':hashlib.sha256(old.read_bytes()).hexdigest(),'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'scope':'implementation stress only; no n100 map enumeration or global optimality','global_optimality':False,'minimal_polynomial_obtained':False},indent=2)+'\n',encoding='utf-8');print('PASS 100 random dart relabelings;2 malformed permutations rejected;changed tag gives different code;no enumeration claim')
if __name__=='__main__':main()
