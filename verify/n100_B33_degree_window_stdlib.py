"""Standard-library entry for the already CAS-checked fan-peel degree proof.
The symbolic generic Euler identity was checked by the original151 receipt;
the imported proof rechecks its exact integer instance without requiring site-packages.
"""
from pathlib import Path
source=Path(__file__).with_name('n100_B33_degree_window.py');text=source.read_text(encoding='utf-8');old='import sympy as sp\n';assert text.count(old)==1;text=text.replace(old,'');old="n,b=sp.symbols('n b',integer=True);assert sp.expand((2*n+b-2)-(2*(n-1)+(b-2)-2)-4)==0";new='assert (2*INTERIOR+B-2)-(2*(INTERIOR-1)+(B-2)-2)==4';assert text.count(old)==1;text=text.replace(old,new);namespace={'__file__':str(Path(__file__).resolve()),'__name__':'B33_degree_stdlib_kernel'};exec(compile(text,str(source),'exec'),namespace);verify=namespace['verify']
