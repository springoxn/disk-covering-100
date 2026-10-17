"""Apply exact box-aware witness pruning to source-derived candidate perturbation boxes.
No claim that these boxes exhaust a graph domain or surround every candidate.
"""
from pathlib import Path
from fractions import Fraction as F
import json,hashlib,copy
from n100_box_aware_capacity import search, independent, need
ROOT=Path(__file__).resolve().parents[1]
SOURCE=ROOT/'runtime/external-disk100-strict-local-replay/source'
def main():
    mp=SOURCE/'rational_midpoint.json';sp=SOURCE/'polynomial_system.json'
    mid=json.loads(mp.read_text(encoding='utf-8'));sys=json.loads(sp.read_text(encoding='utf-8'))
    x=[F(int(v),int(mid['denominator'])) for v in mid['numerators']]
    u=F(1154469548855829,10**16);t=u*u
    holes=sorted({z['hole'] for z in sys['constraint_metadata'] if z['kind']=='distance'})[:8]
    points=[[str(v) for v in x[200+2*h:202+2*h]] for h in holes]
    need(all(sum(F(v)**2 for v in p)<1 for p in points),'interior hole witnesses')
    centers=[x[2*j:2*j+2] for j in range(100)]
    rows=[];excluded=0
    for h in holes:
        p=x[200+2*h:202+2*h]
        support=sorted({z['center'] for z in sys['constraint_metadata'] if z['kind']=='distance' and z['hole']==h})
        need(len(support)==3,'triple support')
        for width in (F(1,10**6),F(1,10**4),F(1,1000),F(1,100)):
            box=[]
            for j,c in enumerate(centers):
                shifted=[c[d]+(c[d]-p[d])/100 if j in support else c[d] for d in (0,1)]
                box.extend([[str(v-width),str(v+width)] for v in shifted])
            box.append(['0',str(t)])
            result=search(box,points);audit=independent(box,points,result)
            excluded+=result['excluded']
            rows.append({'source_hole':h,'support':support,'outward_scale':'1/100','half_width':str(width),'box':box,'result':result,'independent':audit})
    need(excluded>0,'no source-derived exclusion')
    controls=[]
    for width in (F(1,10**6),F(1,1000),F(1,100)):
        box=[[str(v-width),str(v+width)] for c in centers for v in c]+[['0',str(t)]]
        result=search(box,points);need(not result['excluded'],'unperturbed candidate excluded');independent(box,points,result)
        controls.append({'half_width':str(width),'excluded':False})
    # Certification of a split tree: each capacity leaf receives its inherited box.
    selected=next(row for row in rows if row['result']['excluded'])
    box=selected['box'];coordinate=2*selected['support'][0]
    a,b=map(F,box[coordinate]);cut=(a+b)/2;children=[]
    for interval in ((a,cut),(cut,b)):
        child=copy.deepcopy(box);child[coordinate]=list(map(str,interval));result=search(child,points)
        need(result['excluded'],'child exclusion lost');audit=independent(child,points,result)
        children.append({'box':child,'result':result,'independent':audit})
    output={'schema':'n100-candidate-pattern-pruning/v1','verified':True,'points':points,'cases':rows,'excluded_case_count':excluded,'unresolved_case_count':len(rows)-excluded,
        'candidate_controls':controls,'inherited_split':{'coordinate':coordinate,'cut':str(cut),'parent_box':box,'children':children},
        'global_optimality':False,'count_families_excluded':0,'domain_exhaustive':False,
        'scope':'32 explicit source-derived perturbation boxes; not complete candidate graph domain; nonexcluded boxes unresolved',
        'arithmetic':'Fraction only','points_are_rational_midpoints_not_exact_algebraic_holes':True,
        'bindings':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in (mp,sp,ROOT/'verify/n100_box_aware_capacity.py')},
        'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
    out=ROOT/'verify/out/n100-candidate-pattern-pruning.json';need(not out.exists(),'refuse overwrite');out.write_text(json.dumps(output,indent=2)+'\n',encoding='utf-8')
    print('PASS source-derived candidate boxes:',excluded,'excluded,',len(rows)-excluded,'unresolved; 3 genuine candidate controls and inherited split verified')
if __name__=='__main__':main()
