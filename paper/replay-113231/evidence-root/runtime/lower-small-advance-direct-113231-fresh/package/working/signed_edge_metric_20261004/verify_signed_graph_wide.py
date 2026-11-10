#!/usr/bin/env python3
"""Same exact graph checks with the wider proved localization backend."""
from pathlib import Path
import argparse,json
import verify_signed_graph as base
import wide_metric_conjugates as wide

def verify(graph,certificate):
 if not __debug__:raise RuntimeError('Assertions must be enabled')
 proof=[wide.verify_wide_localization(i) for i in range(len(wide.TABLE))]
 base.localization_guards=wide.localization_guards;base.triangle_support=wide.triangle_support
 out=base.verify(graph,certificate);out['wide_localization']=proof;return out
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('graph');p.add_argument('certificate');p.add_argument('--output');a=p.parse_args();out=verify(a.graph,json.loads(Path(a.certificate).read_text()))
 if a.output:Path(a.output).write_text(json.dumps(out,indent=2))
 print(json.dumps(out,indent=2))
