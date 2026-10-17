"""Guard infeasible discovery sentinel before specialized optimization.
Keeps failed first discovery source unchanged; no exact acceptance here.
"""
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];path=ROOT/'tools/n100_B32_M25_specialized_discover.py';text=path.read_text(encoding='utf-8');old="return kernel([eps,tau],full)";assert text.count(old)==1;text=text.replace(old,"result=kernel([eps,tau],full)\n if not full and result==100.:return 1e6\n return result");exec(compile(text,str(Path(__file__).resolve()),'exec'),{'__file__':str(Path(__file__).resolve()),'__name__':'__main__'})
