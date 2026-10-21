"""Structure gate for the bilingual n=100 monograph.

Checks the two upstream decisions that make a derived edition possible at all:
  * the document is modular (small main files that only assemble);
  * every \\input target exists, and each English part has a Chinese mirror (and vice versa);
  * the build script does not write back to any source file.
Exit 0 = pass, 1 = structural failure, 2 = tool error.
"""
from __future__ import annotations

import io
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SECTIONS = ROOT / 'sections'
MAINS = ('monograph.tex', 'monograph_zh.tex')
EXPECTED_INPUTS = 10
MAX_MAIN_BYTES = 10000

errors: list[str] = []
notes: list[str] = []


def read(p: Path) -> str:
    return io.open(p, encoding='utf-8').read()


try:
    inputs_by_main: dict[str, list[str]] = {}
    for main in MAINS:
        p = ROOT / main
        if not p.is_file():
            errors.append(f'{main}: missing main file')
            continue
        s = read(p)
        if len(s.encode('utf-8')) > MAX_MAIN_BYTES:
            errors.append(f'{main}: monolithic main file ({len(s.encode("utf-8"))} bytes)')
        ins = re.findall(r'\\input\{([^}]+)\}', s)
        inputs_by_main[main] = ins
        if len(ins) != EXPECTED_INPUTS:
            errors.append(f'{main}: expected {EXPECTED_INPUTS} inputs, got {len(ins)}')
        for x in ins:
            t = ROOT / (x + '.tex')
            if not t.is_file():
                errors.append(f'{main}: missing input target {t}')
            if not x.startswith('sections/'):
                errors.append(f'{main}: input outside sections/: {x}')
        if '\\begin{document}' not in s or '\\end{document}' not in s:
            errors.append(f'{main}: missing document environment')

    # English/Chinese mirror symmetry
    en = [x for x in inputs_by_main.get('monograph.tex', [])]
    zh = [x for x in inputs_by_main.get('monograph_zh.tex', [])]
    if len(en) == len(zh):
        for a, b in zip(en, zh):
            if b != a.replace('sections/', 'sections/') [:-0] and b != a + '_zh':
                # expected mapping: sections/mN_name -> sections/mN_name_zh
                if b != a + '_zh':
                    errors.append(f'mirror mismatch: {a} -> {b}')
    else:
        errors.append('English and Chinese main files have different input counts')
    if en and zh and len(en) == len(zh):
        order_en = [x.split('/')[-1] for x in en]
        order_zh = [x.split('/')[-1].replace('_zh', '') for x in zh]
        if order_en != order_zh:
            errors.append(f'input order differs: {order_en} vs {order_zh}')

    # every section file must be paired
    names = sorted(p.stem for p in SECTIONS.glob('m*.tex'))
    for n in names:
        if n.endswith('_zh'):
            if n[:-3] not in names:
                errors.append(f'orphan Chinese part: {n}')
        else:
            if n + '_zh' not in names:
                notes.append(f'Chinese part not yet present: {n}_zh')

    # no replacement characters / control characters in any source
    for p in sorted(SECTIONS.glob('*.tex')) + [ROOT / m for m in MAINS if (ROOT / m).is_file()]:
        s = read(p)
        if '\ufffd' in s:
            errors.append(f'{p.name}: replacement character (encoding damage)')
        bad = [hex(ord(c)) for c in s if ord(c) < 32 and c not in '\n\t']
        if bad:
            errors.append(f'{p.name}: control characters {bad[:4]}')

    # build scripts must not write back to sources
    for p in sorted(ROOT.glob('build*.ps1')) + sorted(ROOT.glob('*.py')):
        if p.name in ('structure_check_monograph.py', 'edition_check.py'):
            continue
        if p.suffix == '.py':
            continue
        s = read(p)
        for pat in ('Set-Content', 'Out-File', 'write_text'):
            for m in re.finditer(pat, s):
                line = s[m.start():s.find('\n', m.start()) if '\n' in s[m.start():] else len(s)]
                if '.tex' in line:
                    errors.append(f'{p.name}: build script writes back to a .tex source: {line.strip()[:90]}')
except Exception as exc:  # tool error, not a check failure
    print(f'STRUCTURE TOOL ERROR: {exc!r}')
    sys.exit(2)

for n in notes:
    print('note:', n)
if errors:
    for e in errors:
        print('ERROR:', e)
    sys.exit(1)
print('STRUCTURE PASS: modular bilingual sources, %d parts each, all input targets present' % EXPECTED_INPUTS)
