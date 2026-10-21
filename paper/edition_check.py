"""Four-layer edition check for the bilingual n=100 monograph.

Layer 1  source level  : numeric multiset, label/ref keys, environment and item counts, \\texttt payloads
Layer 2  math segments : multiset of inline and display math payloads
Layer 3  artifact level: both PDFs exist, page counts, unresolved references, missing characters
Layer 4  visual        : reported only (page counts and overfull-box census), never a hard failure

Exit codes: 0 all required checks pass, 1 a check failed, 2 the checker could not run.
"""
from __future__ import annotations

import io
import re
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SECTIONS = ROOT / 'sections'
BUILD = ROOT / 'build'
PAIRS = [
    ('m0_preface', 'm0_preface_zh'),
    ('m1_problem', 'm1_problem_zh'),
    ('m2_upper', 'm2_upper_zh'),
    ('m3_universal', 'm3_universal_zh'),
    ('m4_sixbranch', 'm4_sixbranch_zh'),
    ('m5_frontier', 'm5_frontier_zh'),
    ('m6_catalogue', 'm6_catalogue_zh'),
    ('m7_reproduce', 'm7_reproduce_zh'),
    ('m8_open', 'm8_open_zh'),
    ('m9_appendix', 'm9_appendix_zh'),
]

NUM = re.compile(r'(?<![\w.])\d[\d,\.]*(?:/\d[\d,\.]*)?(?![\w])')


def norm_num(tok: str) -> str:
    """Normalise a numeric literal for comparison: drop trailing sentence punctuation."""
    return tok.rstrip('.,')


def norm_math(tok: str) -> str:
    """Normalise a math payload: collapse whitespace and drop trailing punctuation.

    Re-wrapping a formula across source lines, or moving a sentence comma inside/outside the math,
    is an acceptable residual of translation (paper-edition skill, failure mode 8), not a change of
    mathematical content.
    """
    return re.sub(r'\s+', '', tok).rstrip('.,;:')


def norm_tt(tok: str) -> str:
    """Normalise a monospaced payload: a source line break inside \\texttt is layout, not content."""
    return re.sub(r'\s+', ' ', tok).strip()
TEXTTT = re.compile(r'\\texttt\{((?:[^{}]|\{[^{}]*\})*)\}')
ENVS = re.compile(r'\\begin\{([A-Za-z*]+)\}')
LABELS = re.compile(r'\\label\{([^}]+)\}')
REFS = re.compile(r'\\(?:ref|eqref|pageref)\{([^}]+)\}')
INLINE_MATH = re.compile(r'(?<!\$)\$(?!\$)((?:[^$&]|\\[^\\])+?)\$(?!\$)')
DISPLAY_MATH = re.compile(r'\\\[(.*?)\\\]', re.S)
ITEM = re.compile(r'\\item\b')
ROWEND = re.compile(r'\\\\\s*$', re.M)


def read(p: Path) -> str:
    return io.open(p, encoding='utf-8').read()


def profile(s: str) -> dict:
    return {
        'numbers': Counter(norm_num(t) for t in NUM.findall(s)),
        'texttt': Counter(norm_tt(t) for t in TEXTTT.findall(s)),
        'envs': Counter(ENVS.findall(s)),
        'labels': Counter(LABELS.findall(s)),
        'refs': Counter(REFS.findall(s)),
        'items': len(ITEM.findall(s)),
        'rows': len(ROWEND.findall(s)),
        'display': Counter(norm_math(m) for m in DISPLAY_MATH.findall(s)),
        'inline': Counter(norm_math(m) for m in INLINE_MATH.findall(s)),
        'brace_open': s.count('{') - s.count('\\{'),
        'brace_close': s.count('}') - s.count('\\}'),
        'dollars': s.count('$'),
    }


def diff(name: str, a: Counter, b: Counter, limit: int = 6) -> list[str]:
    out = []
    for k in sorted(set(a) | set(b)):
        if a[k] != b[k]:
            out.append(f'  {name}: {k!r} en={a[k]} zh={b[k]}')
    return out[:limit]


def main() -> int:
    failures: list[str] = []
    reports: list[str] = []

    for en_name, zh_name in PAIRS:
        pen, pzh = SECTIONS / (en_name + '.tex'), SECTIONS / (zh_name + '.tex')
        if not pen.is_file() or not pzh.is_file():
            failures.append(f'{en_name}: missing source pair ({pen.is_file()=}, {pzh.is_file()=})')
            continue
        en, zh = profile(read(pen)), profile(read(pzh))

        # layer 1 -- numbers, monospaced payloads, labels, refs, environment census
        d = diff('numbers', en['numbers'], zh['numbers'])
        if d:
            failures.append(f'{en_name}: numeric multiset differs\n' + '\n'.join(d))
        d = diff('texttt', en['texttt'], zh['texttt'])
        if d:
            failures.append(f'{en_name}: \\texttt payload multiset differs\n' + '\n'.join(d))
        d = diff('labels', en['labels'], zh['labels'])
        if d:
            failures.append(f'{en_name}: \\label keys differ\n' + '\n'.join(d))
        d = diff('refs', en['refs'], zh['refs'])
        if d:
            failures.append(f'{en_name}: \\ref/\\eqref targets differ\n' + '\n'.join(d))
        d = diff('envs', en['envs'], zh['envs'])
        if d:
            failures.append(f'{en_name}: environment census differs\n' + '\n'.join(d))
        for key in ('items', 'rows'):
            if en[key] != zh[key]:
                failures.append(f'{en_name}: {key} count differs en={en[key]} zh={zh[key]}')
        if en['brace_open'] != en['brace_close']:
            failures.append(f'{en_name}: unbalanced braces in English source')
        if zh['brace_open'] != zh['brace_close']:
            failures.append(f'{en_name}: unbalanced braces in Chinese source')

        # layer 2 -- math payload multisets
        d = diff('display math', en['display'], zh['display'])
        if d:
            failures.append(f'{en_name}: display-math multiset differs\n' + '\n'.join(d))
        d = diff('inline math', en['inline'], zh['inline'])
        if d:
            failures.append(f'{en_name}: inline-math multiset differs\n' + '\n'.join(d))
        reports.append(f'{en_name}: numbers {sum(en["numbers"].values())}, '
                       f'texttt {sum(en["texttt"].values())}, items {en["items"]}, '
                       f'inline-math {sum(en["inline"].values())}, display-math {sum(en["display"].values())}')

    # layer 3 -- artifact level
    for main, pdf in (('monograph.tex', 'monograph.pdf'), ('monograph_zh.tex', 'monograph_zh.pdf')):
        p = BUILD / pdf
        log = BUILD / pdf.replace('.pdf', '.log')
        if not p.is_file():
            failures.append(f'artifact missing: {pdf}')
            continue
        if p.stat().st_size < 20000:
            failures.append(f'artifact suspiciously small: {pdf} ({p.stat().st_size} bytes)')
        if log.is_file():
            s = read(log)
            pages = re.findall(r'Output written on \S+ \((\d+) pages', s)
            reports.append(f'{pdf}: {pages[0] if pages else "?"} pages, {p.stat().st_size} bytes')
            if 'LaTeX Warning: There were undefined references' in s:
                failures.append(f'{pdf}: undefined references in the log')
            if 'Missing character' in s:
                failures.append(f'{pdf}: missing characters in the log')
        else:
            reports.append(f'{pdf}: {p.stat().st_size} bytes (no log found)')

    # layer 4 -- visual census, reported only
    warn = BUILD / 'warnings.txt'
    if warn.is_file():
        raw = warn.read_bytes()
        txt = raw.decode('utf-16' if raw[:2] in (b'\xff\xfe', b'\xfe\xff') else 'utf-8', errors='replace')
        over = len(re.findall(re.escape('Overfull \\hbox'), txt))
        vbox = len(re.findall(re.escape('Overfull \\vbox'), txt))
        reports.append(f'overfull census (English build): hbox {over}, vbox {vbox}')

    for r in reports:
        print('report:', r)
    if failures:
        for f in failures:
            print('FAIL:', f)
        print(f'EDITION CHECK FAILED: {len(failures)} item(s)')
        return 1
    print('EDITION CHECK PASS: source, math and artifact layers all consistent')
    return 0


if __name__ == '__main__':
    try:
        sys.exit(main())
    except Exception as exc:
        print(f'EDITION CHECK TOOL ERROR: {exc!r}')
        sys.exit(2)
