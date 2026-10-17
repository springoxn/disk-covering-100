"""Independent verification of maximum-survivor gap-class priority."""
from pathlib import Path
from collections import Counter
import json,hashlib,argparse
ROOT=Path(__file__).resolve().parents[1]
def need(x,m):
 if not x:raise ValueError(m)
def gaps(p):return tuple((p[(i+1)%4]-p[i])%32 for i in range(4))
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--out',default='verify/out/n100-boundary-circle-branch-priority-independent.json');args=ap.parse_args();load=lambda p:json.loads(p.read_text(encoding='utf-8'))
 dom=load(ROOT/'verify/out/n100-boundary-circle-survivor-domain.json');z=load(ROOT/'verify/out/n100-boundary-circle-branch-priority.json');S=[tuple(p) for p in dom['survivor_axis_edge_placements']];c=Counter(gaps(p) for p in S);m=max(c.values());classes=sorted(k for k,v in c.items() if v==m);selected=classes[0];rep=min(p for p in S if gaps(p)==selected);need(list(selected)==z['selected_gaps'] and m==z['survivor_count'] and list(rep)==z['representative'],'priority replay');need(len(c)==165 and m==32,'profile')
 out=ROOT/args.out;need(not out.exists(),'overwrite');out.write_text(json.dumps({'schema':'n100-boundary-circle-branch-priority-independent/v1','verified':True,'gap_classes':len(c),'maximum_survivor_count':m,'selected_gaps':list(selected),'representative':list(rep),'priority_equal':True,'candidate_retained':tuple(z['representative']) in S,'method':'independent survivor-list Counter, maximum count and lexicographic tie rule','machine_verified_geometry':False,'global_optimality':False,'bindings':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in (ROOT/'verify/out/n100-boundary-circle-survivor-domain.json',ROOT/'verify/out/n100-boundary-circle-branch-priority.json')},'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()},indent=2)+'\n',encoding='utf-8');print('PASS priority independent',len(c),'classes max',m,selected,rep)
if __name__=='__main__':main()
