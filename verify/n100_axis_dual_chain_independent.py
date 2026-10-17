"""Independent face ownership/path check and integer Floyd replay of axis cuts."""
from pathlib import Path
from fractions import Fraction as F
import json,hashlib,argparse,copy
ROOT=Path(__file__).resolve().parents[1]
def need(x,msg):
    if not x:raise ValueError(msg)
def cycles(p):
    unseen=set(range(len(p)));rows=[]
    while unseen:
        start=min(unseen);row=[];cur=start
        while cur in unseen:unseen.remove(cur);row.append(cur);cur=p[cur]
        need(cur==start,'cycle');rows.append(row)
    return rows
def audit(z,core,prior):
    A=core['alpha'];faces=cycles(core['phi']);N=len(faces);own={d:i for i,row in enumerate(faces) for d in row};outside=z['outer_face']
    need(all(core['core_tags'][d][0]=='outer' for d in faces[outside]),'outer type')
    boundary=[A[d] for d in reversed(faces[outside])];sites=[own[d] for d in boundary];need(sites==z['boundary_face_owners'],'owners')
    inf=1000;D=[[inf]*N for _ in range(N)]
    for i in range(N):D[i][i]=0
    for d,e in enumerate(A):
        x,y=own[d],own[e]
        if outside not in (x,y):D[x][y]=D[y][x]=1
    for k in range(N):
        if k==outside:continue
        for i in range(N):
            if D[i][k]==inf:continue
            for j in range(N):
                D[i][j]=min(D[i][j],D[i][k]+D[k][j])
    U=F(z['radius']);coords=((1,0),(0,1),(-1,0),(0,-1));expected_retained=set();expected_excluded=set()
    for p in prior['retained_axis_edge_placements']:
        fail=False
        for i in range(4):
            for j in range(i+1,4):
                d2=sum((coords[i][a]-coords[j][a])**2 for a in (0,1));k=D[sites[p[i]]][sites[p[j]]]+1
                if F(d2)>4*k*k*U*U:fail=True
        (expected_excluded if fail else expected_retained).add(tuple(p))
    seen=set()
    for row in z['excluded']:
        p=tuple(row['placement']);need(p not in seen,'duplicate');seen.add(p);w=row['witness'];i,j=w['axis_pair'];path=w['face_path'];darts=w['directed_core_edge_darts']
        need(i<j and path[0]==sites[p[i]] and path[-1]==sites[p[j]] and outside not in path,'path endpoints')
        need(len(darts)==len(path)-1 and len(path)==w['disk_chain_length'],'path length')
        for a,b,d in zip(path,path[1:],darts):need(own[d]==a and own[A[d]]==b,'shared edge witness')
        d2=sum((coords[i][q]-coords[j][q])**2 for q in (0,1));gap=F(d2)-4*len(path)**2*U*U
        need(gap>0 and gap==F(w['squared_distance_gap']) and d2==w['axis_distance_squared'],'strict metric contradiction')
    need(seen==expected_excluded,'excluded set mismatch')
    saved=z['retained_axis_edge_placements'];need(len(saved)==len(set(map(tuple,saved))) and set(map(tuple,saved))==expected_retained,'retained set mismatch')
    need(z['excluded_count']==len(seen) and z['retained_count']==len(saved),'totals')
    need(tuple(prior['candidate_axis_edge_indices']) in expected_retained,'candidate retained')
    return {'excluded':len(seen),'retained':len(saved),'all_path_witnesses_verified':True,'independent_floyd_partition_matches':True}
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--out',default='verify/out/n100-axis-dual-chain-independent.json');args=ap.parse_args()
    cp=ROOT/'verify/out/n100-cubic-core-roundtrip.json';pp=ROOT/'verify/out/n100-axis-subdivision-pruning.json';src=ROOT/'verify/out/n100-axis-dual-chain-pruning.json'
    load=lambda p:json.loads(p.read_text(encoding='utf-8'));core=load(cp)['core'];prior=load(pp);z=load(src);r=audit(z,core,prior)
    controls=[]
    for name,change in [('broken_edge_path',lambda q:q['excluded'][0]['witness']['directed_core_edge_darts'].__setitem__(0,-999)),('missing_exclusion',lambda q:q['excluded'].pop())]:
        q=copy.deepcopy(z);change(q)
        try:audit(q,core,prior)
        except (ValueError,KeyError,IndexError):controls.append(name)
    need(len(controls)==2,'negative controls')
    out=ROOT/args.out;need(not out.exists(),'overwrite');out.write_text(json.dumps({'schema':'n100-axis-dual-chain-independent/v1','verified':True,'result':r,'rejected_controls':controls,'method':'independent face cycles and all-pairs Floyd integer distances versus primary BFS paths; rational gap replay','bindings':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in (cp,pp,src)},'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'machine_verified_geometry':False,'global_optimality':False,'scope':'one fixed n100 core axis-insertion partition; not enumeration of all cores'},indent=2)+'\n',encoding='utf-8');print('PASS independent Floyd partition and504 shared-edge path witnesses;',r,';2 corruptions rejected')
if __name__=='__main__':main()
