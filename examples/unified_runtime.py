"""Run from project root: python examples/unified_runtime.py"""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from neuroweave.labs import make_memory
from neuroweave.runtime import ResearchRuntime
from neuroweave.purpose import Purpose

memory=make_memory()
runtime=ResearchRuntime(memory,Purpose('researcher','sample-protocol','explore',2))
runtime.propose('trial-1','above_threshold',now=0,cost=.5)
runtime.confirm('trial-1',actor='researcher',now=1)
receipt=runtime.execute('trial-1',actor='researcher',now=2,seed=17)
print('External side effect:',receipt['receipt']['external_side_effect'])
print('Resource remaining:',receipt['resource_remaining'])
print('State partitions:',sorted(receipt['state_after']))
print('Feedback evidence kind:',memory.nodes['feedback:trial-1']['evidence_kind'])
memory.ledger.close()
