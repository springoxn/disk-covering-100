"""Discovery/replay for enlarging the source-derived hole witness pool.
Outputs a fresh report; this is not a complete graph-domain proof.
"""
from pathlib import Path
from fractions import Fraction as F
import json,hashlib
from n100_box_aware_capacity import search,independent,need
ROOT=Path(__file__).resolve().parents[1];SRC=ROOT/'runtime/external-disk100-strict-local-replay/source'
def cover_by_distinct_centers(box,raw):
    points=[tuple(map(F,p)) for p in raw];t=F(box[-1][1]);n=(len(box)-1)//2
    projected={};adj=[]
    for i,p in enumerate(points):
        row=[]
        for j in range(n):
            c=tuple(min(max(p[d],F(box[2*j+d][0])),F(box[2*j+d][1])) for d in (0,1))
            if sum((p[d]-c[d])**2 for d in (0,1))<=t:
                row.append(j);projected[i,j]=c
        adj.append(row)
    match={}
    def augment(i,seen):
        for j in adj[i]:
            if j in seen:continue
            seen.add(j)
            if j not in match or augment(match[j],seen):match[j]=i;return True
        return False
    for i in range(len(points)):
        if not augment(i,set()):return {'found':False,'meaning':'no injective singleton cover found; feasibility undecided'}
    centers=[[(F(box[2*j+d][0])+F(box[2*j+d][1]))/2 for d in (0,1)] for j in range(n)]
    assignment={}
    for j,i in match.items():centers[j]=list(projected[i,j]);assignment[i]=j
    for j,c in enumerate(centers):need(all(F(box[2*j+d][0])<=c[d]<=F(box[2*j+d][1]) for d in (0,1)),'center box')
    margins=[t-sum((points[i][d]-centers[assignment[i]][d])**2 for d in (0,1)) for i in range(len(points))]
    need(min(margins)>=0,'explicit finite cover')
    return {'found':True,'centers':[[str(v) for v in c] for c in centers],'assignment':[assignment[i] for i in range(len(points))],'minimum_margin':str(min(margins)),'scope':'finite supplied points only; no continuous target coverage claim'}

def main():
    mp=SRC/'rational_midpoint.json';sp=SRC/'polynomial_system.json'
    mid=json.loads(mp.read_text(encoding='utf-8'));sys=json.loads(sp.read_text(encoding='utf-8'));D=int(mid['denominator']);x=[F(int(v),D) for v in mid['numerators']]
    holes=sorted({int(z['hole']) for z in sys['constraint_metadata'] if z['kind']=='distance'})
    need(len(holes)>=32,'expected full hole inventory')
    u=F(1154469548855829,10**16);t=u*u;centers=[x[2*j:2*j+2] for j in range(100)]
    # Reconstruct the 32 parent boxes and use all available hole subsets.
    cases=[];previous=json.loads((ROOT/'verify/out/n100-candidate-pattern-pruning.json').read_text(encoding='utf-8'))
    for old in previous['cases']:
        h=old['source_hole'];support=old['result']
        p=x[200+2*h:202+2*h];box=old['box']
        cases.append({'hole':h,'box':box,'support':sorted({z['center'] for z in sys['constraint_metadata'] if z['kind']=='distance' and z['hole']==h})})
    rows=[]
    pools=[8,16,24,32]
    for limit in pools:
        pts=[[str(v) for v in x[200+2*h:202+2*h]] for h in holes[:limit]]
        need(all(sum(F(v)**2 for v in p)<1 for p in pts),'hole in target')
        excluded=0;fresh=0;case_results=[]
        for index,case in enumerate(cases):
            finite=cover_by_distinct_centers(case['box'],pts)
            window_results=[]
            for start in range(0,limit,8):
                window=pts[start:min(start+8,limit)]
                result=search(case['box'],window);audit=independent(case['box'],window,result)
                window_results.append({'start':start,'result':result,'independent':audit})
            is_excluded=any(w['result']['excluded'] for w in window_results)
            need(not (finite['found'] and is_excluded),'finite cover contradicts exclusion')
            excluded+=is_excluded
            fresh+=int(is_excluded and not previous['cases'][index]['result']['excluded'])
            case_results.append({'hole':case['hole'],'excluded_by_window':is_excluded,'window_results':window_results,'finite_cover':finite})
        rows.append({'pool_holes':limit,'excluded':excluded,'unresolved':len(cases)-excluded,'newly_excluded_after_pool8':fresh,'finite_covers_found':sum(c['finite_cover']['found'] for c in case_results),'cases':case_results})
    need(rows[0]['excluded']==16,'baseline changed')
    # A source-derived negative control: centered boxes at first three widths remain nonexcluded for the full pool.
    controls=[]
    for width in (F(1,10**6),F(1,1000),F(1,100)):
        box=[[str(v-width),str(v+width)] for c in centers for v in c]+[['0',str(t)]]
        pts=[[str(v) for v in x[200+2*h:202+2*h]] for h in holes[:32]]
        cover=cover_by_distinct_centers(box,pts);need(cover['found'],'finite candidate cover not found');controls.append({'half_width':str(width),'explicit_finite_cover':cover})
    out=ROOT/'verify/out/n100-expanded-hole-pool.json';need(not out.exists(),'refuse overwrite')
    out.write_text(json.dumps({'schema':'n100-expanded-hole-pool/v1','verified':True,'pool_results':rows,'candidate_controls':controls,'source_hole_count':len(holes),'scope':'32 source-derived boxes and first 32 rational midpoint holes; not graph-domain exhaustive','points_are_rational_midpoints':True,'global_optimality':False,'count_families_excluded':0,'bindings':{'rational_midpoint.json':hashlib.sha256(mp.read_bytes()).hexdigest(),'polynomial_system.json':hashlib.sha256(sp.read_bytes()).hexdigest(),'box_checker':hashlib.sha256((ROOT/'verify/n100_box_aware_capacity.py').read_bytes()).hexdigest(),'prior_certificate':hashlib.sha256((ROOT/'verify/out/n100-candidate-pattern-pruning.json').read_bytes()).hexdigest()},'script_sha256':hashlib.sha256(__file__.encode() if False else Path(__file__).read_bytes()).hexdigest()},indent=2)+'\n',encoding='utf-8')
    print('PASS expanded hole pools:',[(z['pool_holes'],z['excluded'],z['unresolved']) for z in rows],'; candidate controls retained')
if __name__=='__main__':main()
