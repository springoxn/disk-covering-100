"""Discovery-only B35 M26 single-chord metric for residual three7 profiles."""
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];source=ROOT/'tools/n100_B34_onechord_labelled_discover.py';text=source.read_text(encoding='utf-8')
rules=[('for high in ((8,),(7,7)):','for high in ((7,7,7),):'),('for ph in range(minimum,maximum+1):','for ph in (9+ear,):'),('pr=34-ph','pr=35-ph'),("'DDD':59","'DDD':57"),('center=59*','center=57*'),("(m['pH']-2)","(m['pH']-3)"),('math.pi/34','math.pi/35'),('outer=34*','outer=35*'),("'B':34","'B':35"),('B34-onechord-labelled/v1','B35-M26-onechord-labelled/v1'),('B34-onechord-labelled-discovery-178','B35-M26-onechord-discovery-194'),('B34 ONECHORD DISCOVERY','B35 M26 ONECHORD DISCOVERY')]
for old,new in rules:assert old in text,old;text=text.replace(old,new)
exec(compile(text,str(Path(__file__).resolve()),'exec'),{'__file__':str(Path(__file__).resolve()),'__name__':'__main__'})
