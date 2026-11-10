"""Trace actual proof processes without changing transformed proof source.
Recursively instruments Python subprocesses and saves entered verifier radii.
"""
from pathlib import Path
from fractions import Fraction
import sys,os,json,atexit,subprocess,runpy,hashlib
SCRIPT=Path(__file__).resolve()
def main():
 logdir=Path(sys.argv[1]);logdir.mkdir(parents=True,exist_ok=True);args=sys.argv[2:];assert args;original=subprocess.Popen;entries={};observed=set();package=Path(os.environ['N100_AUDIT_PACKAGE']).resolve()
 def trace(frame,event,arg):
  if event!='call':return
  name=frame.f_code.co_name
  if not(name.startswith('verify') or name in ('classify','exclude_all','cluster_exclusion','pair_replay','triangle_checks_34','main','reduce_profiles','four_face_metric','direct_deep_five')):return
  try:p=Path(frame.f_code.co_filename).resolve();rel=p.relative_to(package).as_posix()
  except (ValueError,OSError):return
  fields={}
  for k in ('R','R2','B','K','LAM','LAMBDA34','CURVATURE'):
   v=frame.f_globals.get(k)
   if isinstance(v,(int,Fraction)):fields[k]=str(v)
  for k in ('radius','r','R','B','lam','mu','intercept'):
   v=frame.f_locals.get(k)
   if isinstance(v,(int,Fraction)):fields['argument_'+k]=str(v)
  key=json.dumps([rel,name,fields],sort_keys=True);entries[key]={'source':rel,'function':name,'parameters':fields};observed.add(rel)
 def popen(command,*a,**kw):
  if isinstance(command,(list,tuple)) and len(command)>1 and Path(str(command[0])).name.lower() in ('python','python.exe','python3','python3.exe'):
   rest=list(command[1:]);flags=[]
   while rest and rest[0] in ('-B','-S','-u'):flags.append(rest.pop(0))
   if rest and str(rest[0])!=str(SCRIPT):command=[command[0],*flags,str(SCRIPT),str(logdir),*rest]
  return original(command,*a,**kw)
 def save():
  sys.setprofile(None);subprocess.Popen=original;modules={}
  for name,m in list(sys.modules.items()):
   path=getattr(m,'__file__',None)
   if not path:continue
   try:p=Path(path).resolve();rel=p.relative_to(package).as_posix()
   except (ValueError,OSError):continue
   if p.is_file():modules[rel]=hashlib.sha256(p.read_bytes()).hexdigest()
  output={'pid':os.getpid(),'argv':args,'verifier_entries':list(entries.values()),'loaded_package_modules':modules};(logdir/f'process-{os.getpid()}.json').write_text(json.dumps(output,indent=2)+'\n',encoding='utf-8')
 atexit.register(save);subprocess.Popen=popen;sys.setprofile(trace)
 if args[0]=='-c':sys.argv=['-c',*args[2:]];exec(compile(args[1],'<string>','exec'),{'__name__':'__main__'})
 else:sys.argv=args;runpy.run_path(args[0],run_name='__main__')
if __name__=='__main__':main()
