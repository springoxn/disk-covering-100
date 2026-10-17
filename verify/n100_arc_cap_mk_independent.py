"""Independent m-k arithmetic replay and exact q=m-k>=46 consequence at U."""
from pathlib import Path
from fractions import Fraction as F
import argparse,json,hashlib,copy
ROOT=Path(__file__).resolve().parents[1]
def require(ok,msg):
    if not ok:raise ValueError(msg)
def check(front,support,domain):
    radius=F(support['radius']);d=F(support['delta']);a=F(support['slope']);M=F(support['maximum_half_arc_upper'])
    pl,ph=F(314159,100000),F(314160,100000)
    # Direct rearrangement: deficit = fixed - m*disk_area + k*(disk_area-a*M).
    disk=ph*radius**2;gain=disk-a*M;fixed=pl*((1-2*radius+d)**2+a)
    require(gain>0,'gain')
    table={};allrows=[]
    for m in range(76,101):
        accepted=[];excluded=[]
        for k in range(m+1):
            (excluded if fixed-m*disk+k*gain>0 else accepted).append(k)
        row=front['frontier'][m-76]
        require(row['m']==m and row['excluded_k']==excluded and row['largest_not_excluded_k']==max(accepted,default=-1),'frontier')
        table[m]=accepted
        require(all(m-k>=46 for k in accepted),'nonserving count')
        allrows.append({'m':m,'nonserving_count_lower':46,'max_service_count':max(accepted,default=-1)})
    surviving=[]
    for m,b in domain['surviving_m_B_families']:
        compatible=[k for k in table[m] if k>=b]
        require(bool(compatible),'unexpected removed family')
        surviving.append([m,b,min(compatible),max(compatible)])
    require(front['remaining_m_B_families']==surviving and not front['removed_m_B_families'],'family domain')
    return {'verified':True,'nonserving_disks_at_least':46,'frontier':allrows,'retained_m_B_families':len(surviving),'compatible_m_B_k_triples':sum(row[3]-row[2]+1 for row in surviving)}
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--out',default='verify/out/n100-arc-cap-mk-independent.json');args=ap.parse_args()
    fp=ROOT/'verify/out/n100-arc-cap-mk-frontier.json';sp=ROOT/'verify/out/n100-arc-cap-rational-support.json';dp=ROOT/'verify/out/n100-vonequinox-count-domain-bound.json'
    front=json.loads(fp.read_text(encoding='utf-8'));support=json.loads(sp.read_text(encoding='utf-8'));domain=json.loads(dp.read_text(encoding='utf-8'))
    require(front['input_sha256']==hashlib.sha256(sp.read_bytes()).hexdigest(),'support binding')
    result=check(front,support,domain);rejected=[]
    for label,change in [('false_m100_k54_exclusion',lambda q:q['frontier'][-1]['excluded_k'].insert(0,54)),('false_family_removal',lambda q:q['removed_m_B_families'].append([100,54])),('wrong_m96_frontier',lambda q:q['frontier'][20].__setitem__('largest_not_excluded_k',49))]:
        q=copy.deepcopy(front);change(q)
        try:check(q,support,domain)
        except ValueError:rejected.append(label)
    require(len(rejected)==3,'negative controls')
    out=ROOT/args.out;require(not out.exists(),'overwrite')
    out.write_text(json.dumps({'schema':'n100-arc-cap-mk-independent/v1','result':result,'rejected_controls':rejected,'bindings':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in (fp,sp,dp)},'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'global_optimality':False,'new_count_families_excluded':0,'machine_verified_geometry':False,'scope':'independent arithmetic consequence of analytic arc-cap support; at least46 nonserving effective disks at U'},indent=2)+'\n',encoding='utf-8');print('PASS independent m-k frontier; at least46 nonserving disks; 87 families retained;',result['compatible_m_B_k_triples'],'compatible triples; 3 corruptions rejected')
if __name__=='__main__':main()
