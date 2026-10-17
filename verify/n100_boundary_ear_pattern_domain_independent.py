"""Independent transfer DP, primitive-period orbit counts and small-word enumeration."""
from pathlib import Path
from functools import lru_cache
from math import gcd
import json,hashlib
R=Path(__file__).resolve().parents[1]
@lru_cache(None)
def words(n,e):
 states={(first,first,first):1 for first in (0,1)}
 for pos in range(1,n):
  nxt={}
  for (first,last,w),count in states.items():
   for bit in (0,1):
    if last and bit:continue
    if w+bit>e:continue
    key=(first,bit,w+bit);nxt[key]=nxt.get(key,0)+count
  states=nxt
 return sum(v for (first,last,w),v in states.items() if w==e and not(first and last))
@lru_cache(None)
def primitive(n,e):
 v=words(n,e)
 for d in range(1,n):
  if n%d==0 and e%(n//d)==0:v-=primitive(d,e//(n//d))
 assert v>=0 and v%n==0
 return v

def orbits(n,e):
 return sum(primitive(d,e//(n//d))//d for d in range(1,n+1) if n%d==0 and e%(n//d)==0)
def main():
 p=R/'verify/out/n100-boundary-ear-pattern-domain.json';z=json.loads(p.read_text(encoding='utf-8'));srcp=R/'verify/out/n100-ear-marked-joint-cuts.json';src=json.loads(srcp.read_text(encoding='utf-8'));assert z['input_sha256']==hashlib.sha256(srcp.read_bytes()).hexdigest();small=[];enumerated=0
 for n in range(1,15):
  full=(1<<n)-1;labels={};canonical={}
  for mask in range(1<<n):
   rotate=((mask<<1)&full)|(mask>>(n-1))
   if mask&rotate:continue
   w=mask.bit_count();labels[w]=labels.get(w,0)+1;key=min(((mask<<s)&full)|(mask>>(n-s)) for s in range(n));canonical.setdefault(w,set()).add(key);enumerated+=1
  for e in range(n//2+1):assert labels.get(e,0)==words(n,e) and len(canonical.get(e,set()))==orbits(n,e)
  small.append({'n':n,'nonadjacent_words':sum(labels.values()),'rotation_orbits':sum(map(len,canonical.values()))})
 assert len(z['families'])==len(src['family_rows'])==17
 for r,s in zip(z['families'],src['family_rows']):
  n=r['B'];allowed=r['allowed_ear_counts'];assert (r['m'],n,allowed)==(s['m'],s['B'],s['remaining_ear_counts']);assert r['labelled_cyclic_words']==sum(words(n,e) for e in allowed);assert r['rotation_orbits']==sum(orbits(n,e) for e in allowed)
  fixed=[]
  for shift in range(n):
   d=gcd(n,shift);repeat=n//d;fixed.append(sum(words(d,e//repeat) for e in allowed if e%repeat==0))
  assert fixed==r['fixed_counts_by_rotation_shift']
 out=R/'verify/out/n100-boundary-ear-pattern-domain-independent.json';assert not out.exists();out.write_text(json.dumps({'schema':'n100-boundary-ear-pattern-domain-independent/v1','verified_all17_families_by_transfer_DP_and_primitive_periods':True,'small_boundary_sizes_checked':list(range(1,15)),'small_nonadjacent_words_enumerated':enumerated,'small_checks':small,'scope':'complete necessary boundary word relaxation, independent count formulas and small exhaustive orbit checks; not geometric diagrams or interior triangulations; no whole-family exclusion','global_optimality':False,'input_sha256':hashlib.sha256(p.read_bytes()).hexdigest()},indent=2)+'\n',encoding='utf-8');print('PASS independent DP/primitive orbit counts all17 families;small words',enumerated)
if __name__=='__main__':main()
