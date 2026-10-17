"""Exact polynomial refutations, model bindings and SymPy cross-checks."""
from pathlib import Path
from fractions import Fraction as F
import json,copy,hashlib
import sympy as S
import n100_algebra_proof_interfaces as I
R=Path(__file__).resolve().parents[1]
U=F(1154469548855829,10**16)
def expression(terms,symbols,values=None):
 out=S.S.Zero
 for coefficient,indices in terms:
  term=S.Rational(str(coefficient))
  for i in indices:term*=S.Rational(str(values[str(i)])) if values and str(i) in values else symbols[i]
  out+=term
 return out

def sympy_check(model,proof):
 x=S.symbols('x:'+str(model['variables']));values=proof['fixed_variables']
 def sigma(entries):return sum((S.Rational(e['weight'])*expression(e['poly'],x)**2 for e in entries),S.S.Zero)
 rhs=sigma(proof['free_sos']);ineq=model['inequalities']+[{'terms':[[proof['squared_radius_upper'],[]],['-1',[model['t_index']]]]}]
 for term in proof['inequality_multipliers']:rhs+=sigma(term['sos'])*expression(ineq[term['index']]['terms'],x,values)
 for term in proof['equality_multipliers']:rhs+=expression(term['poly'],x)*expression(model['equalities'][term['index']]['terms'],x,values)
 assert S.Poly(S.expand(rhs+1),*x).is_zero

def main():
 source=R/'verify/out/n100-generic-map-compiler.json';saved=json.loads(source.read_text(encoding='utf-8'));rows=[]
 for e in saved['small_models']:
  model,bridge=I.compile_map(e['map']);assert model==e['model'];result=I.two_axis_filter(e['map'],U*U);assert result['status']=='EXCLUDED';sympy_check(model,result['proof_input']);rows.append({'chord':e['chord'],'result':result});assert I.two_axis_filter(e['map'],F(1))['status']=='NOT_EXCLUDED'
 g=json.loads((R/'verify/out/n100-candidate-clipped-map.json').read_text(encoding='utf-8'));model,bridge=I.compile_map(g);assert model==saved['candidate_model'];candidate=I.two_axis_filter(g,U*U);assert candidate['status']=='NOT_EXCLUDED'
 # General identity in arbitrary point coordinates, independent of primary sparse code.
 cx,cy,px,py,qx,qy,t=S.symbols('cx cy px py qx qy t',real=True);gp=t-(cx-px)**2-(cy-py)**2;gq=t-(cx-qx)**2-(cy-qy)**2;L=((px-qx)**2+(py-qy)**2)/4;assert S.expand(t-L-(gp+gq)/2-(cx-(px+qx)/2)**2-(cy-(py+qy)/2)**2)==0
 controls=[];e=saved['small_models'][0];model=e['model'];proof=rows[0]['result']['proof_input']
 for label,change in [('negative_sos_weight',lambda p:p['free_sos'][0].update(weight='-1')),('wrong_model',lambda p:p.update(model_fingerprint='foreign-model')),('radius_not_squared',lambda p:p.update(radius_units='radius')),('float_coefficient',lambda p:p['free_sos'][0]['poly'][0].__setitem__(0,0.5)),('unjustified_substitution',lambda p:p['fixed_variables'].update({'8':'0'})),('wrong_inequality',lambda p:p['inequality_multipliers'][0].update(index=999)),('false_square_offset',lambda p:p['free_sos'][0]['poly'][1].__setitem__(0,'1/3'))]:
  bad=copy.deepcopy(proof);change(bad);assert I.verify_refutation(model,bad)['status']=='PRECONDITION_MISSING';controls.append(label)
 for label,change in [('disconnected_map',lambda h:h['vertices'].update({'ghost':{}})),('incorrect_face_owner',lambda h:h['edges'][0].update(faces=[999]))]:
  bad=copy.deepcopy(e['map']);change(bad)
  try:I.compile_map(bad)
  except (ValueError,KeyError,IndexError):controls.append(label)
  else:raise AssertionError(label)
 # Farkas and equality-ideal terms are special cases, not just the two-axis builder.
 m={'variables':1,'t_index':0,'equalities':[],'inequalities':[{'terms':[['1',[0]],['-1',[]]]}]};p={'model_fingerprint':I.fingerprint(m),'radius_units':'squared','squared_radius_upper':'0','free_sos':[],'inequality_multipliers':[{'index':i,'sos':[{'weight':'1','poly':[['1',[]]]}]} for i in (0,1)],'equality_multipliers':[]};assert I.verify_refutation(m,p)['status']=='EXCLUDED'
 m2={'variables':1,'t_index':0,'equalities':[{'terms':[['1',[0]],['-1',[]]]}],'inequalities':[]};p2=copy.deepcopy(p);p2.update(model_fingerprint=I.fingerprint(m2),inequality_multipliers=[{'index':0,'sos':[{'weight':'1','poly':[['1',[]]]}]}],equality_multipliers=[{'index':0,'poly':[['1',[]]]}]);assert I.verify_refutation(m2,p2)['status']=='EXCLUDED'
 out=R/'verify/out/n100-algebra-proof-interface-contracts.json';assert not out.exists();paths=[R/'verify/n100_algebra_proof_interfaces.py',R/'verify/n100_generic_map_compiler.py',R/'verify/n100_face_axis_global_exclusion.py',source,R/'verify/out/n100-candidate-clipped-map.json'];out.write_text(json.dumps({'schema':'n100-algebra-proof-interface-contracts/v1','six_connected_small_maps_negative_one_certificates':rows,'candidate_polynomials_identical':True,'candidate_model_bridge':bridge,'candidate_two_axis_filter':candidate,'six_refutations_independent_sympy_expansion_zero':True,'general_two_point_identity_sympy_zero':True,'farkas_special_case_verified':True,'equality_ideal_special_case_verified':True,'negative_controls':controls,'sympy_version':S.__version__,'scope':'whole declared polynomial domains and one-map compilation; all-map enumeration and geometry completeness not established','global_optimality':False,'bindings':{str(p.relative_to(R)):hashlib.sha256(p.read_bytes()).hexdigest() for p in paths},'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()},indent=2)+'\n',encoding='utf-8');print('PASS algebra interfaces;6 exact negative-one identities;SymPy cross-checks;candidate retained;controls',len(controls))
if __name__=='__main__':main()
