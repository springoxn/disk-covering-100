#!/usr/bin/env python3
"""Verify release file integrity; no mathematical PASS is inferred."""
from pathlib import Path
import hashlib,json
ROOT=Path(__file__).resolve().parent

def verify():
    if not __debug__:
        raise RuntimeError('Assertions must remain enabled')
    manifest=json.loads((ROOT/'MANIFEST_SHA256.json').read_text())
    assert manifest['format']=='disk100-release-sha256-v1'
    checked_bytes=0
    for row in manifest['files']:
        rel=Path(row['path'])
        assert not rel.is_absolute() and '..' not in rel.parts
        data=(ROOT/rel).read_bytes()
        assert len(data)==row['bytes'],('size',str(rel))
        assert hashlib.sha256(data).hexdigest()==row['sha256'],('hash',str(rel))
        checked_bytes+=len(data)
    assert len(manifest['files'])==manifest['file_count']
    assert checked_bytes==manifest['total_payload_bytes']
    return {'status':'PASS','scope':'Release integrity only; mathematical results require replay',
            'files':len(manifest['files']),'bytes':checked_bytes}

if __name__=='__main__':
    print(json.dumps(verify(),indent=2))
