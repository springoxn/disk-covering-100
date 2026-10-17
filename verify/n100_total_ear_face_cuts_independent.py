"""Exhaustive small boundary-word check, independent ear-triple set packing."""
from pathlib import Path
import json,hashlib
R=Path(__file__).resolve().parents[1]
def exact_packing(B,tipmask):
 triples=[(1<<((i-1)%B))|(1<<i)|(1<<((i+1)%B)) for i in range(B) if tipmask>>i&1]
 def search(j,used):
  if j==len(triples):return 0
  skip=search(j+1,used)
  return max(skip,1+search(j+1,used|triples[j])) if not used&triples[j] else skip
 return search(0,0)
def independent_ceiling(B,p):
 valid=[]
 for e in range(B//2+1):
  # Lower bound on maximal disjoint packing for total e ears.
  exceptional=B%4==2 and e==B//2
  required=(e-1)//2 if exceptional else (e+1)//2
  if required<=p:valid.append(e)
 return max(valid)
def main():
 path=R/'verify/out/n100-total-ear-face-cuts.json';z=json.loads(path.read_text(encoding='utf-8'));sp=R/'verify/out/n100-disjoint-ear-group-cuts-independent.json';s=json.loads(sp.read_text(encoding='utf-8'));checked=0;trials=0;byB=[]
 for B in range(5,17):
  full=(1<<B)-1;local=0
  for mask in range(1<<B):
   if mask&(((mask<<1)&full)|(mask>>(B-1))):continue
   ears=mask.bit_count();pack=exact_packing(B,mask);need_bound=independent_ceiling(B,pack);assert ears<=need_bound,(B,mask,ears,pack,need_bound);checked+=1;local+=1
   for p in range(pack,B//3+1):assert ears<=independent_ceiling(B,p);trials+=1
  byB.append({'B':B,'all_nonadjacent_tip_words':local})
 assert len(z['family_rows'])==len(s['results'])==17
 for row,prior in zip(z['family_rows'],s['results']):
  m,B,p=row['m'],row['B'],row['maximum_disjoint_ear_triples'];assert (m,B,p)==(prior['m'],prior['B'],prior['maximum_disjoint_ear_groups']);assert row['maximum_total_ear_faces']==independent_ceiling(B,p);assert row['minimum_distinct_boundary_incident_faces']==B-row['maximum_total_ear_faces']
  for e in range(row['maximum_total_ear_faces']+1):
   f2=e;f1=B-2*e;f0=2*m-2*B-2+e;assert min(f0,f1,f2)>=0 and f1+2*f2==B and f0+f1+f2==2*m-B-2
 out=R/'verify/out/n100-total-ear-face-cuts-independent.json';assert not out.exists();out.write_text(json.dumps({'schema':'n100-total-ear-face-cuts-independent/v1','verified_all_small_nonadjacent_tip_words':True,'small_boundary_sizes':list(range(5,17)),'tip_words_checked':checked,'packing_bound_trials':trials,'counts_by_boundary_size':byB,'family_rows_checked':17,'verified_all_allowed_ear_count_face_incidence':True,'scope':'all cyclic nonadjacent tip words B5..16 with exact triple set packing; independent formula reconstruction for actual B29..39, not exhaustive geometric maps at those sizes; general conflict graph lemma remains analytic','global_optimality':False,'input_sha256':hashlib.sha256(path.read_bytes()).hexdigest()},indent=2)+'\n',encoding='utf-8');print('PASS independent all small tip words',checked,'packing trials',trials,'and17 family ear-face tables')
if __name__=='__main__':main()
