"""Discovery-only first-order active-contact LP at the exact lattice candidate.
LP float results do not certify local or global optimality.
"""
import json,itertools,hashlib,time
from pathlib import Path
from fractions import Fraction as F
import numpy as np
from scipy.optimize import linprog
ROOT=Path(__file__).resolve().parents[1]
def dot(a,b):return a[0]*b[0]+3*a[1]*b[1]
def sub(a,b):return (a[0]-b[0],a[1]-b[1])
def pos(i,j):return (F(2*i+j,2),F(j,2))
def norm(i,j):return i*i+i*j+j*j

def main():
 start=time.perf_counter()
 indices=sorted([(i,j) for i in range(-8,9) for j in range(-8,9) if norm(i,j)<28]+[(-6,4),(-2,-4),(2,4)])
 lookup={p:k for k,p in enumerate(indices)}
 neighbors=[(1,0),(0,1),(-1,1),(-1,0),(0,-1),(1,-1)]
 holes=set()
 for i in range(-8,9):
  for j in range(-8,9):
   for d,e in zip(neighbors,neighbors[1:]+neighbors[:1]):
    tri=[pos(i,j),pos(i+d[0],j+d[1]),pos(i+e[0],j+e[1])]
    q=tuple(sum((p[k] for p in tri),F(0))/3 for k in (0,1))
    if dot(q,q)<=F(67,3):holes.add(q)
 rows=[];records=[]
 for q in sorted(holes):
  active=[k for k,p in enumerate(indices) if dot(sub(q,pos(*p)),sub(q,pos(*p)))==F(1,3)]
  if len(active)<2:raise AssertionError((q,active))
  boundary=dot(q,q)==F(67,3)
  weights={k:F(1,3) for k in active}
  if boundary and len(active)==2:
   tangent=(-3*q[1],q[0]);a,b=active
   ta=dot(sub(q,pos(*indices[a])),tangent);tb=dot(sub(q,pos(*indices[b])),tangent)
   weights={a:-tb/(ta-tb),b:ta/(ta-tb)}
  assert len(active)==3 or boundary
  assert sum(weights.values())==1 and all(w>=0 for w in weights.values())
  row=[F(0)]*201
  for k,w in weights.items():
   delta=sub(pos(*indices[k]),q)
   row[2*k]=2*w*delta[0];row[2*k+1]=6*w*delta[1]
  row[-1]=F(1)
  rows.append(row)
  records.append({'q_uv':[str(t) for t in q],'boundary':boundary,'active':active,'weights':{str(k):str(w) for k,w in weights.items()}})
 matrix=np.array([[float(v) for v in row] for row in rows])
 objective=np.zeros(201);objective[-1]=-1
 solution=linprog(objective,A_ub=matrix,b_ub=np.zeros(len(rows)),bounds=[(-1,1)]*200+[(None,None)],method='highs')
 out=ROOT/'runtime/n100-contact-lp-discovery.json'
 if out.exists():raise FileExistsError(out)
 result={'schema':'n100-contact-lp-discovery/v1','discovery_only':True,'all_contacts_exactly_constructed':True,
 'contact_count':len(records),'boundary_contact_count':sum(x['boundary'] for x in records),
 'solver_success':bool(solution.success),'solver_message':solution.message,
 't_discovery':float(solution.x[-1]) if solution.success else None,
 'direction_uv_discovery':solution.x[:-1].reshape(100,2).tolist() if solution.success else None,
 'contacts':records,'elapsed_seconds_metadata_only':time.perf_counter()-start,
 'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
 'not_claimed':['local optimality','global optimality','rigorous improvement from first-order LP','minimal polynomial of optimal radius']}
 out.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 print('contact LP discovery',len(records),'contacts; boundary',result['boundary_contact_count'],'t',result['t_discovery'])
if __name__=='__main__':main()
