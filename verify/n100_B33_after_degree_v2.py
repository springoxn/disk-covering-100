"""Replay B33 with standard-library new degree window in python -S children."""
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];path=ROOT/'verify/n100_B33_after_degree.py';text=path.read_text(encoding='utf-8');rules=[('from n100_B33_degree_window import verify as check_degrees','from n100_B33_degree_window_stdlib import verify as check_degrees'),('B33-new-degree-replay-152','B33-new-degree-replay-152v2'),("ROOT/'verify/n100_B33_degree_window.py',ROOT/'verify/out", "ROOT/'verify/n100_B33_degree_window.py',ROOT/'verify/n100_B33_degree_window_stdlib.py',ROOT/'verify/n100_B33_after_degree.py',ROOT/'verify/out")]
for old,new in rules:assert text.count(old)==1;text=text.replace(old,new)
exec(compile(text,str(Path(__file__).resolve()),'exec'),{'__file__':str(Path(__file__).resolve()),'__name__':'__main__'})
