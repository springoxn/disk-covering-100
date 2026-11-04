from pathlib import Path
import re,sys
ROOT=Path(__file__).resolve().parent
errors=[]
main='paper.tex'
s=(ROOT/main).read_text(encoding='utf-8')
inputs=re.findall(r'\\input\{([^}]+)\}',s)
if len(inputs)!=6: errors.append(f'{main}: expected 6 inputs, got {len(inputs)}')
for x in inputs:
 p=ROOT/(x+'.tex')
 if not p.exists(): errors.append(f'{main}: missing {p}')
if len(s)>10000: errors.append(f'{main}: monolithic main file')
if errors:
 print('\n'.join(errors));sys.exit(1)
print('STRUCTURE PASS: modular short-paper sources, six sections')
