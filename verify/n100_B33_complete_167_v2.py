"""Protected completeB33 entry: explicitly reject Python optimized mode."""
from pathlib import Path
if not __debug__:raise RuntimeError('Assertions must remain enabled')
ROOT=Path(__file__).resolve().parents[1];source=ROOT/'verify/n100_B33_complete_167.py';text=source.read_text(encoding='utf-8');rules=[('n100-B33-complete-167.json','n100-B33-complete-167-v2.json'),('[Path(__file__),*paths,pp',"[Path(__file__),ROOT/'verify/n100_B33_complete_167.py',*paths,pp")]
for old,new in rules:assert text.count(old)==1;text=text.replace(old,new)
exec(compile(text,str(Path(__file__).resolve()),'exec'),{'__file__':str(Path(__file__).resolve()),'__name__':'__main__'})
