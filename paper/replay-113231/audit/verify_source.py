from __future__ import annotations
import re
import sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=Path(__file__).resolve().parent/'source-audit.txt'
def main():
    tex=(ROOT/'paper.tex').read_text(encoding='utf-8')
    required=[r'\\begin\{document\}',r'\\end\{document\}',r'\\bibliography\{references\}',r'\\label\{sec:geometry\}',r'\\label\{app:ledger\}',r'\\begin\{theorem\}',r'\\end\{theorem\}']
    for pattern in required: assert re.search(pattern,tex),f'missing source structure: {pattern}'
    for env in ('equation','align','longtable','enumerate','itemize','center'):
        begins=len(re.findall(rf'\\begin\{{{env}\}}',tex));ends=len(re.findall(rf'\\end\{{{env}\}}',tex));assert begins==ends,(env,begins,ends)
    opens=len(re.findall(r'(?<!\\)\{',tex));closes=len(re.findall(r'(?<!\\)\}',tex));assert opens==closes,(opens,closes)
    assert '0.113231' in tex and r'113231}{1000000' in tex
    assert '987178740639}{10^{12}' in tex
    assert 'not formalized' in tex and 'No saved branch PASS report' in tex
    OUT.write_text('PASS: balanced environments, braces, theorem structure, evidence-bound scope markers\n',encoding='utf-8')
    print(OUT.read_text(encoding='utf-8'),end='')
if __name__=='__main__':
    try:main()
    except AssertionError as e:print(f'SOURCE AUDIT FAIL: {e}',file=sys.stderr);raise SystemExit(1)
    except Exception as e:print(f'SOURCE AUDIT ERROR: {type(e).__name__}: {e}',file=sys.stderr);raise SystemExit(2)
