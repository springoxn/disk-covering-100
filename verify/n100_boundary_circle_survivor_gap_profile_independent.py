"""Independent aggregation of survivor/excluded gap profiles."""
from pathlib import Path
from collections import Counter
import json,hashlib,argparse
ROOT=Path(__file__).resolve().parents[1]
def need(x,m):
 if not x:raise ValueError(m)
def gaps(p):return tuple((p[(i+1)%4]-p[i])%32 for i in range(4))
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--out',default='verify/out/n100-boundary-circle-survivor-gap-profile-independent.json');args=ap.parse_args();load=lambda p:json.loads(p.read_text(encoding='utf-8'))
 dom=load(ROOT/'verify/out/n100-boundary-circle-survivor-domain.json');st=load(ROOT/'verify/out/n100-boundary-circle-exclusion-stats.json');prof=load(ROOT/'verify/out/n100-boundary-circle-survivor-gap-profile.json');S={tuple(p) for p in dom['survivor_axis_edge_placements']};E={tuple(p) for p in st['excluded_placements']};need(len(S)==4200 and len(E)==576 and S.isdisjoint(E),'sets')
 sc=Counter(gaps(p) for p in S);ec=Counter(gaps(p) for p in E);rows=[{'gaps':list(k),'survivors':sc[k],'excluded':ec[k],'total':sc[k]+ec[k],'survivor_fraction_num':sc[k],'survivor_fraction_den':sc[k]+ec[k]} for k in sorted(set(sc)|set(ec))];need(rows==prof['profiles'],'profile equal');need(len(rows)==165 and not [r for r in rows if r['survivors']==0],'165 all represented');need((30,6,14,22) in S,'candidate')
 out=ROOT/args.out;need(not out.exists(),'overwrite');out.write_text(json.dumps({'schema':'n100-boundary-circle-survivor-gap-profile-independent/v1','verified':True,'gap_class_count':len(rows),'profile_equal':True,'all165_classes_have_survivors':True,'survivors':len(S),'excluded':len(E),'candidate_retained':True,'method':'independent set aggregation from survivor and exclusion certificates','machine_verified_geometry':False,'global_optimality':False,'bindings':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in (ROOT/'verify/out/n100-boundary-circle-survivor-domain.json',ROOT/'verify/out/n100-boundary-circle-exclusion-stats.json',ROOT/'verify/out/n100-boundary-circle-survivor-gap-profile.json')},'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()},indent=2)+'\n',encoding='utf-8');print('PASS independent gap profile',len(rows),'classes; all have survivors')
if __name__=='__main__':main()
