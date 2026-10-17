"""K discovery objective includes the K-dependent boundary cost and safe domain.
Earlier K discovery source stays untouched; no proof acceptance here.
"""
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];path=ROOT/'tools/n100_B32_M25_specialized_K_discover.py';driver=path.read_text(encoding='utf-8');needle="exec(compile(text,str(Path(__file__).resolve()),'exec'),{'__file__':str(Path(__file__).resolve()),'__name__':'__main__'})";assert driver.count(needle)==1
patch="""
old='if a<=0 or b<=0 or b>=.9 or eps<=0 or eps>=.85 or tau<=0:'
new='if a<=0 or b<=0 or b>=.9 or eps<=0 or eps>=.85 or tau<=0 or not .25<=K<=.6 or a+eps>=.99:'
assert text.count(old)==1;text=text.replace(old,new)
old='return result\\ndef main():'
new='if full:return result\\n RAD=.11324;mu=math.pi/32;s=math.sin(mu);h=math.sqrt(RAD*RAD-s*s);outer=32*(s*h+mu-s*math.cos(mu)+K*RAD*s*(math.cos(mu)-h));return result+outer/(RAD*RAD)\\ndef main():'
assert text.count(old)==1;text=text.replace(old,new)
"""
driver=driver.replace(needle,patch+'\n'+needle);exec(compile(driver,str(Path(__file__).resolve()),'exec'),{'__file__':str(Path(__file__).resolve()),'__name__':'__main__'})
