"""B35 profile diagnostic v3 attaches degree windows to each report."""
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1];source=ROOT/'verify/n100_B35_profile_diagnostic_v2.py';text=source.read_text(encoding='utf-8');old="            if restricted and (M in (25,26)) and d in (6,7,8,9,10,12,20,50,99): z.setdefault('profile_gaps',[]).append([p,d,str(F(gap,S))])";assert text.count(old)==1;text=text.replace(old,'')
old2="         return report,margin,coefficient,gaps,shifted_ear,bad";new2="         if restricted and M in (25,26): report['profile_gaps']=[[p,d,str(v)] for (p,d),v in sorted(gaps.items()) if d in (6,7,8,9,10,12,20,50,99)]\n         return report,margin,coefficient,gaps,shifted_ear,bad";assert text.count(old2)==1;text=text.replace(old2,new2).replace('n100-B35-profile-diagnostic-186.json','n100-B35-profile-diagnostic-188.json');exec(compile(text,str(Path(__file__).resolve()),'exec'),{'__file__':str(Path(__file__).resolve()),'__name__':'__main__'})
