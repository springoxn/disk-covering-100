from pathlib import Path
import json,hashlib
import sympy as s
R=Path(__file__).resolve().parents[1]
X=s.Matrix([[0,0],[1,0],[0,2],[2,1],[-1,-2]])
n=X.rows;one=s.ones(n,1);X=X-one*(one.T*X)/n
G=X*X.T;P=s.eye(n)-one*one.T/n;lam=s.trace(G)+1;Z=lam*P-G
assert G*one==s.zeros(n,1) and Z*one==s.zeros(n,1)
# exact principal-minor PSD test for this five-point example
from itertools import combinations
minors=[]
for k in range(1,n+1):
 for idx in combinations(range(n),k):
  det=Z.extract(idx,idx).det();assert det>=0;minors.append(str(det))
S=G+Z
assert S==lam*P
assert all(S[i,i]+S[j,j]-2*S[i,j]==2*lam for i in range(n) for j in range(i+1,n))
p=R/'verify/out/n100-simplex-lift-example.json'
assert not p.exists()
p.write_text(json.dumps({'schema':'finite-point-simplex-lift-example/v1','verified':True,'centered_X':[[str(x) for x in row] for row in X.tolist()],'lambda':str(lam),'extra_coordinate_Gram_PSD_all_principal_minors':True,'principal_minors_checked':len(minors),'lifted_Gram_is_lambda_projection':True,'all_pair_distances_squared':str(2*lam),'general_argument':'center X; choose lambda>=trace(XX^T); lambda P-XX^T PSD; factor as YY^T to get regular-simplex lift','optimization_equivalence_claimed':False,'checker_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()},indent=2)+'\n')
print('PASS exact Gram lift for irregular 5-point example; 31 PSD principal minors, common squared edge distance',2*lam)
