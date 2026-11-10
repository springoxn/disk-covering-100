#!/usr/bin/env python3
"""Complete normalized B33 R23 branch, with a coherent unique-five replacement."""
from pathlib import Path
from fractions import Fraction as F
import sys,subprocess,os,json,hashlib
ROOT=Path(__file__).resolve().parent
BASE=ROOT if (ROOT/'verify_star_lp_duals.py').exists() else ROOT.parent/'working'
R=F(113231,1000000)
def run(name,radius_override=False):
    p=ROOT/name if (ROOT/name).exists() else BASE/name
    env=dict(os.environ);env['PYTHONPATH']=os.pathsep.join(map(str,[ROOT,BASE,BASE/'lower_bounds_extension_20261004']))
    if radius_override:
        code="import json,importlib;from fractions import Fraction;v=importlib.import_module(%r);v.R=Fraction(%r);print(json.dumps(v.verify()))"%(p.stem,str(R))
        args=[sys.executable,'-B','-S','-c',code]
    else:args=[sys.executable,'-B','-S',str(p)]
    z=json.loads(subprocess.run(args,cwd=BASE,env=env,check=True,capture_output=True,text=True).stdout)
    assert z['status']=='PASS'
    if 'radius' in z:
        assert z['radius']==str(R) and z['B']==33
        assert F(z['required_center_norm_squared_upper'])==1-R*R
    return dict(source=name,sha256=hashlib.sha256(p.read_bytes()).hexdigest(),result=z)
def verify():
    if not __debug__:raise RuntimeError('Assertions must remain enabled')
    low=run('verify_B33_lowM_prerequisites_0p11323.py')
    assert low['result']['M_domain']=='M<=25'
    replacement=run('verify_B33_M25_coherent_five.py')
    olddata=json.loads((BASE/'hinge_B33_lowM_0p11322_proposals.json').read_text())
    newdata=json.loads((ROOT/'B33_lowM_prerequisites_0p11323_proposals.json').read_text())
    assert olddata['rows']==newdata['rows']
    M25=low['result']['branches'][-1];assert M25['M']==25
    assert F(M25['unique_global_five_margin'])>0
    gain=F(replacement['result']['minimum_normalized_gain'])
    final25=F(M25['ordinary_area_margin'])+R*R*gain;assert final25>0
    high=run('verify_B33_highM_any_five_0p11323.py')
    assert high['result']['M_domain']=='M>=26'
    # The core is connected in the M26/e0 case; a boundary chord would
    # enclose an empty-side polygon and force a q2 ear. Thus b1/e0 is
    # impossible, regardless of the radius or signed metric coefficients.
    assert F(22**2,6)<108
    M26=run('verify_N26_seven_face_metric_0p11322.py',True)
    M27=run('verify_N27_metric_chord_cases_0p11322.py',True)
    ear=run('verify_B33_one_ear_metric_0p11323.py')
    margins=[F(low['result']['minimum_area_margin']),final25,
        F(high['result']['degree5_contradiction_margin']),F(M26['result']['minimum_area_margin']),
        F(M27['result']['minimum_area_margin']),F(ear['result']['area_margin'])]
    assert min(margins)>0
    return dict(status='PASS',radius=str(R),B=33,m_maximum=100,
        scope='Complete normalized B33 branch only; other boundary counts are separate',
        required_center_norm_squared_upper=str(1-R*R),graph_catalog_dependency=False,
        quadratic_radial_bootstrap_dependency=False,M25_coherent_area_margin=str(final25),
        minimum_reported_area_margin=str(min(margins)),
        components=[low,replacement,high,M26,M27,ear])
if __name__=='__main__':print(json.dumps(verify(),indent=2),flush=True)
