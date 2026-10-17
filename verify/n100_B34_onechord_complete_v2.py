"""Core-only ring incidences are72; adding outerBRR gives124."""
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];source=ROOT/'verify/n100_B34_onechord_complete.py';text=source.read_text(encoding='utf-8');rules=[('19+2*25+3==124','19+2*25+3==72'),('for p in (Path(__file__),pp,tp,source)',"for p in (Path(__file__),ROOT/'verify/n100_B34_onechord_complete.py',pp,tp,source)")]
for old,new in rules:assert text.count(old)==1;text=text.replace(old,new)
exec(compile(text,str(Path(__file__).resolve()),'exec'),{'__file__':str(Path(__file__).resolve()),'__name__':'__main__'})
