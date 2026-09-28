"""Check the supplied release checksum list. This does not authenticate its author."""
from pathlib import Path
import hashlib
import sys
ROOT=Path(__file__).resolve().parents[1]
failures=[]
for line in (ROOT/'SHA256SUMS').read_text().splitlines():
    expected,name=line.split('  ',1)
    path=(ROOT/name).resolve()
    if not path.is_relative_to(ROOT) or not path.is_file():
        failures.append(name);continue
    actual=hashlib.sha256(path.read_bytes()).hexdigest()
    if actual!=expected:failures.append(name)
print('PASS: all listed release bytes match' if not failures else 'FAIL: '+', '.join(failures))
sys.exit(bool(failures))
