from pathlib import Path
import re,sys
ROOT=Path(__file__).resolve().parent
errors=[]
for main in ('paper.tex','paper_zh.tex'):
 s=(ROOT/main).read_text(encoding='utf-8')
 inputs=re.findall(r'\\input\{([^}]+)\}',s)
 if len(inputs)!=6: errors.append(f'{main}: expected 6 inputs, got {len(inputs)}')
 for x in inputs:
  p=ROOT/(x+'.tex')
  if not p.exists(): errors.append(f'{main}: missing {p}')
 if len(s)>10000: errors.append(f'{main}: monolithic main file')
for p in ROOT.glob('sections/*.tex'):
 s=p.read_text(encoding='utf-8')
 if '\ufffd' in s: errors.append(f'{p}: replacement character')
if errors:
 print('\n'.join(errors));sys.exit(1)
print('STRUCTURE PASS: modular English/Chinese sources and six sections each')
