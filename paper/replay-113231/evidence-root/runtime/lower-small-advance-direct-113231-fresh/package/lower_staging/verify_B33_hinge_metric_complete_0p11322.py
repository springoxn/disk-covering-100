#!/usr/bin/env python3
"""Fresh-process complete normalized B33 branch at R=.11322."""
from pathlib import Path
from fractions import Fraction as F
import subprocess,sys,os,json,hashlib
ROOT=Path(__file__).resolve().parent
BASE=ROOT if (ROOT/'verify_star_lp_duals.py').exists() else ROOT.parent/'working'
SOURCES=['verify_hinge_B33_lowM_0p11322.py','verify_B33_highM_no_ears_0p11322.py',
         'verify_N26_seven_face_metric_0p11322.py','verify_N27_metric_chord_cases_0p11322.py']
def verify():
    if not __debug__:raise RuntimeError('Assertions must remain enabled')
    R=F(5661,50000);rows=[]
    # M26 topology checks, supplementing the written induced-core proof.
    assert F(22**2,6)<108 and F(24**2,6)<106
    assert F(3**2+23**2,6)<106 and F(3**2+25**2,6)<106
    assert 26+19+F(19**2,6)<106
    for name in SOURCES:
        p=ROOT/name if (ROOT/name).exists() else BASE/name
        env=dict(os.environ);env['PYTHONPATH']=os.pathsep.join(map(str,[ROOT,BASE,BASE/'lower_bounds_extension_20261004']))
        done=subprocess.run([sys.executable,'-B','-S',str(p)],cwd=BASE,env=env,check=True,text=True,capture_output=True)
        z=json.loads(done.stdout);assert z['status']=='PASS' and z['radius']==str(R) and z['B']==33
        assert F(z['required_center_norm_squared_upper'])==1-R*R
        rows.append(dict(source=name,sha256=hashlib.sha256(p.read_bytes()).hexdigest(),result=z))
    assert rows[0]['result']['M_domain']=='M<=25'
    high=rows[1]['result'];assert high['M_domain']=='M>=26'
    assert high['remaining_Euler_cases']==[dict(M=26,ears=0,bad_q1=0,degree_excess=1),dict(M=27,ears=0,bad_q1=0,degree_excess=0)]
    margins=[F(rows[0]['result']['minimum_area_margin']),F(high['ear_contradiction_margin']),
             F(rows[2]['result']['minimum_area_margin']),F(rows[3]['result']['minimum_area_margin'])]
    assert min(margins)>0
    return dict(status='PASS',radius=str(R),B=33,m_maximum=100,
        scope='Complete B33 branch after whole-cover normalization; all other B values require separate branches',
        required_center_norm_squared_upper=str(1-R*R),
        graph_catalog_dependency=False,quadratic_radial_bootstrap_dependency=False,
        minimum_reported_area_margin=str(min(margins)),components=rows)
if __name__=='__main__':print(json.dumps(verify(),indent=2),flush=True)
