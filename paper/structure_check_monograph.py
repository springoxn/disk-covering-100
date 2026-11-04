"""Structure gate for the n=100 monograph (English edition).

The monograph was once maintained in two editions; the Chinese one was retired, so this
gate now checks a single source set:

  * the document is modular (a small main file that only assembles);
  * every \\input target exists, sits under sections/, and is reachable from the main file;
  * no part file is orphaned (present on disk, never included);
  * the sources carry no replacement or control characters;
  * the build script does not write back into any .tex source.

Exit 0 = pass, 1 = structural failure, 2 = tool error.
"""
from __future__ import annotations

import io
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SECTIONS = ROOT / 'sections'
MAIN = 'monograph.tex'
EXPECTED_INPUTS = 11
MAX_MAIN_BYTES = 10000

errors: list[str] = []
notes: list[str] = []


def read(p: Path) -> str:
    return io.open(p, encoding='utf-8').read()


try:
    main = ROOT / MAIN
    if not main.is_file():
        errors.append(f'{MAIN}: missing main file')
        inputs: list[str] = []
        s = ''
    else:
        s = read(main)
        if len(s.encode('utf-8')) > MAX_MAIN_BYTES:
            errors.append(f'{MAIN}: monolithic main file ({len(s.encode("utf-8"))} bytes)')
        inputs = re.findall(r'\\input\{([^}]+)\}', s)
        if len(inputs) != EXPECTED_INPUTS:
            errors.append(f'{MAIN}: expected {EXPECTED_INPUTS} inputs, got {len(inputs)}')
        for x in inputs:
            t = ROOT / (x + '.tex')
            if not t.is_file():
                errors.append(f'{MAIN}: missing input target {t}')
            if not x.startswith('sections/'):
                errors.append(f'{MAIN}: input outside sections/: {x}')
        if '\\begin{document}' not in s or '\\end{document}' not in s:
            errors.append(f'{MAIN}: missing document environment')

    # every monograph part on disk must be included; the short paper's six sections
    # (background, upper_bound, ...) live in the same directory and belong to paper.tex
    included = {x.split('/')[-1] for x in inputs}
    for p in sorted(SECTIONS.glob('m*.tex')):
        if p.stem not in included:
            errors.append(f'orphan part, never \\input: sections/{p.name}')

    # no replacement characters / control characters in any source
    for p in sorted(SECTIONS.glob('*.tex')) + ([main] if main.is_file() else []):
        text = read(p)
        if '\ufffd' in text:
            errors.append(f'{p.name}: replacement character (encoding damage)')
        bad = [hex(ord(c)) for c in text if ord(c) < 32 and c not in '\n\t']
        if bad:
            errors.append(f'{p.name}: control characters {bad[:4]}')

    # build scripts must not write back to sources
    for p in sorted(ROOT.glob('build*.ps1')):
        text = read(p)
        for pat in ('Set-Content', 'Out-File', 'write_text'):
            for m in re.finditer(pat, text):
                line = text[m.start():text.find('\n', m.start()) if '\n' in text[m.start():] else len(text)]
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
print('STRUCTURE PASS: modular sources, %d parts, all input targets present' % EXPECTED_INPUTS)
