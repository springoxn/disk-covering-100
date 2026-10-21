"""Idempotent normalisation of the monograph sources (English and Chinese alike).

Applies the same four mechanical transforms to every part file, so that the English and Chinese
editions stay structurally identical at the source level:
  1. tables set in \\footnotesize;
  2. normalised column widths for the wide catalogue/ledger tables;
  3. line-break opportunities inside long monospaced identifiers (paths, digests, JSON keys);
  4. long monospaced tokens set in \\footnotesize so they fit their column.

It never changes a digit, a path, a label, a ref key, an environment or a math payload.
"""
from __future__ import annotations

import io
import re
from pathlib import Path

D = Path(__file__).resolve().parent / 'sections'
RR = r'>{\raggedright\arraybackslash}'
AB = '\\allowbreak{}'

WIDTH_SUBS = [
    ('@{}' + RR + r'p{0.16\textwidth}' + RR + r'p{0.20\textwidth}' + RR + r'p{0.24\textwidth}' + RR + r'p{0.26\textwidth}@{}',
     '@{}' + RR + r'p{0.15\textwidth}' + RR + r'p{0.19\textwidth}' + RR + r'p{0.23\textwidth}' + RR + r'p{0.25\textwidth}@{}'),
    ('@{}' + RR + r'p{0.30\textwidth}' + RR + r'p{0.16\textwidth}' + RR + r'p{0.42\textwidth}@{}',
     '@{}' + RR + r'p{0.28\textwidth}' + RR + r'p{0.15\textwidth}' + RR + r'p{0.40\textwidth}@{}'),
    (r'@{}p{0.24\textwidth}p{0.40\textwidth}p{0.12\textwidth}p{0.20\textwidth}@{}',
     '@{}' + RR + r'p{0.20\textwidth}' + RR + r'p{0.36\textwidth}' + RR + r'p{0.14\textwidth}' + RR + r'p{0.18\textwidth}@{}'),
    (r'@{}p{0.24\textwidth}p{0.42\textwidth}p{0.12\textwidth}p{0.18\textwidth}@{}',
     '@{}' + RR + r'p{0.20\textwidth}' + RR + r'p{0.36\textwidth}' + RR + r'p{0.14\textwidth}' + RR + r'p{0.18\textwidth}@{}'),
    (r'@{}p{0.24\textwidth}p{0.44\textwidth}p{0.12\textwidth}p{0.16\textwidth}@{}',
     '@{}' + RR + r'p{0.20\textwidth}' + RR + r'p{0.38\textwidth}' + RR + r'p{0.14\textwidth}' + RR + r'p{0.16\textwidth}@{}'),
]


def process_idents(body: str) -> str:
    out, i = [], 0
    while i < len(body):
        if body.startswith('\\_', i):
            out.append('\\_'); i += 2
            if not body.startswith(AB, i):
                out.append(AB)
            continue
        c = body[i]
        if c == '-' and not body.startswith('--', i) and not (i and body[i - 1] == '-'):
            out.append('-'); i += 1
            if not body.startswith(AB, i):
                out.append(AB)
            continue
        if c == '/' and not body.startswith(AB, i + 1):
            out.append('/'); i += 1; out.append(AB); continue
        out.append(c); i += 1
    return ''.join(out)


def rewrite_texttt(s: str) -> str:
    res, i, key = [], 0, '\\texttt{'
    while True:
        j = s.find(key, i)
        if j < 0:
            res.append(s[i:]); break
        res.append(s[i:j + len(key)])
        k, depth = j + len(key), 1
        while k < len(s) and depth:
            if s[k] == '\\':
                k += 2; continue
            if s[k] == '{':
                depth += 1
            elif s[k] == '}':
                depth -= 1
                if depth == 0:
                    break
            k += 1
        res.append(process_idents(s[j + len(key):k]))
        res.append('}')
        i = k + 1
    return ''.join(res)


TT = re.compile(r'\\texttt\{((?:[^{}]|\{[^{}]*\})*)\}')


def longest_run(body: str) -> int:
    b = body.replace(AB, '\x00')
    return max((len(r) for r in re.split(r'[\x00\s]', b)), default=0)


def shrink_long(s: str) -> str:
    def sub(m):
        body = m.group(1)
        if longest_run(body) >= 34 and not m.group(0).startswith('{\\footnotesize'):
            return '{\\footnotesize\\texttt{' + body + '}}'
        return m.group(0)
    return TT.sub(sub, s)


def normalise(s: str) -> str:
    s = s.replace('\\begin{center}\n\\small\n\\begin{tabular}',
                  '\\begin{center}\n\\footnotesize\n\\begin{tabular}')
    for a, b in WIDTH_SUBS:
        s = s.replace(a, b)
    s = rewrite_texttt(s)
    s = shrink_long(s)
    return s


if __name__ == '__main__':
    changed = 0
    for p in sorted(D.glob('m*.tex')):
        s = io.open(p, encoding='utf-8').read()
        s2 = normalise(s)
        if s2 != s:
            io.open(p, 'w', encoding='utf-8', newline='\n').write(s2)
            changed += 1
            print('normalised:', p.name)
    print('files changed:', changed)
