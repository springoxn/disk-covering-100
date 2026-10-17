"""Exact finite cycle support, ordered-prefix state and parent-bound nogoods."""
from itertools import product
import copy,json,hashlib
from n100_arc_nogood_state_dp import state_dp,make_marks
from n100_arc_cycle_support import bit_dp,set_dp
from n100_arc_pair_consistency import labels,mask
from n100_proof_interfaces import require,exact_data
import n100_continuous_proof_interfaces as C

def digest(z):return hashlib.sha256(json.dumps(z,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def learn_nogood(parent,tiles,literals):
 exact_data(parent);exact_data(tiles);require(bool(literals) and len({v for v,j in literals})==len(literals),'distinct nogood variables');restricted=copy.deepcopy(parent);empty=False
 for v,j in literals:
  require(type(v) is int and type(j) is int and 0<=v<len(parent['boxes']),'nogood variable');tile=tiles[str(v)][str(j)];require(len(tile)==4 and all(type(x) is int for x in tile) and tile[0]<=tile[1] and tile[2]<=tile[3],'tile real box');b=restricted['boxes'][v];b=[max(b[0],tile[0]),min(b[1],tile[1]),max(b[2],tile[2]),min(b[3],tile[3])];restricted['boxes'][v]=b;empty=empty or b[0]>b[1] or b[2]>b[3]
 result={'status':'EXCLUDED','scope':'empty restricted real box'} if empty else C.run(restricted);require(result['status']=='EXCLUDED','no verified continuous conflict')
 return {'literals':literals,'parent_fingerprint':digest(parent),'tiles_fingerprint':digest(tiles),'proof':result,'scope':'only this continuous parent and tile realization','global_optimality':False}

def ordered_oracle(D,T,same):
 expanded=[mask(2*j+flag for j in labels(bits) for flag in ((0,) if i==0 else (0,1))) for i,bits in enumerate(D)];tables=[]
 for i,bits in enumerate(expanded):
  row={}
  for state in labels(bits):
   j,M=state//2,state//2+state%2;targets=[]
   for k in labels(T[i][j]&D[(i+1)%len(D)]):
    if same[i] and M>k+1:continue
    target=2*k+(max(M,k)-k if same[i] else 0)
    if expanded[(i+1)%len(D)]&(1<<target):targets.append(target)
   row[state]=mask(targets)
  tables.append(row)
 a,w=bit_dp(expanded,tables);require(a==set_dp(expanded,tables),'independent cycle recurrences');return [mask({s//2 for s in labels(bits)}) for bits in a]

def run(payload):
 try:
  exact_data(payload);ctx=payload['context'];require(ctx.get('semantics_id')=='finite-ordered-arc-relaxation/v1' and all(isinstance(ctx.get(k),str) and ctx[k] for k in ('map_id','frame_id','parent_box_id','radius_domain_id')),'finite context');variables=payload['variables'];D=payload['domains'];n=len(D);require(n>=2 and len(variables)==n and len(set(variables))==n and all(type(v) is int for v in variables),'cycle variables');require(all(type(d) is int and d>=0 for d in D),'domain masks');same=payload['same_quadrant'];require(len(same)==n and all(type(x) is bool for x in same) and not same[-1],'anchor after quadrant switch');rawT=payload['tables'];require(all(type(j) in (int,str) and str(j)==str(int(j)) and int(j)>=0 for row in rawT for j in row),'canonical integer relation keys');T=[{int(j):bits for j,bits in t.items()} for t in rawT];require(len(T)==n,'cycle tables')
  for i,row in enumerate(T):
   require(all(j in row for j in labels(D[i])) and all(type(bits) is int and bits>=0 for bits in row.values()),'complete nonnegative transition masks')
  records=payload.get('nogoods',[]);clauses=[]
  for record in records:
   parent=payload['continuous_parent'];require(all(ctx[k]==parent['context'][k] for k in ('map_id','frame_id','parent_box_id','radius_domain_id')),'nogood context transfer');require(learn_nogood(parent,payload['tiles'],record['literals'])==record,'nogood replay');clause=[]
   for v,j in record['literals']:
    require(v in variables and D[variables.index(v)]&(1<<j),'nogood labels outside finite domain');clause.append([variables.index(v),j])
   clauses.append(clause)
  branch_count=1
  for c in clauses:branch_count*=len(c)
  budget=payload.get('oracle_branch_budget',4096);require(type(budget) is int and budget>0,'oracle branch budget')
  if branch_count>budget or 2*max((d.bit_count() for d in D),default=0)*(1<<len(clauses))>1000000:return {'status':'UNDECIDED','reason':'declared finite verification budget exceeded','global_optimality':False}
  marks=make_marks(list(range(n)),dict(enumerate(D)),clauses);support,witnesses,stats=state_dp(D,T,same,marks,len(clauses));oracle=[0]*n
  for choices in product(*clauses):
   sub=D[:]
   for v,j in choices:sub[v]&=~(1<<j)
   row=ordered_oracle(sub,T,same);oracle=[a|b for a,b in zip(oracle,row)]
  require(support==oracle,'state-DP / union-of-subdomains mismatch')
  for witness in witnesses:
   assignment=[s[0] for s in witness];require(all(D[i]&(1<<j) for i,j in enumerate(assignment)) and all(T[i][assignment[i]]&(1<<assignment[(i+1)%n]) for i in range(n)),'cycle witness');require(all(any(assignment[v]!=j for v,j in c) for c in clauses),'witness violates learned nogood')
  return {'status':'EXCLUDED' if not any(support) else 'NOT_EXCLUDED','supported_domains':support,'witnesses':witnesses,'statistics':stats,'oracle_subdomains':branch_count,'model_fingerprint':digest(payload),'proof_input':payload,'scope':'exact finite necessary relaxation; model-to-geometry bridge inherited separately','covering_exclusion_authorized_without_bridge':False,'global_optimality':False}
 except (ValueError,KeyError,TypeError,ZeroDivisionError) as e:return {'status':'PRECONDITION_MISSING','reason':str(e),'global_optimality':False}
