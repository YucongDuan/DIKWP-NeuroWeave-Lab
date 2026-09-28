"""Run from project root: python examples/reconstructive_memory.py"""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from neuroweave.memory import Memory
from neuroweave.ledger import Ledger

# For durable storage use Ledger('my-memory.sqlite'). This example is ephemeral.
log=Ledger()
m=Memory(log)
m.add_source('temperature',6,source='synthetic://sensor',context='trial')
m.derive('scaled',['temperature'],{'op':'scale','factor':2},context='trial')
m.derive('flag',['scaled'],{'op':'threshold_gt','threshold':10},context='trial',unit='boolean')
print('Before correction:',m.read('flag'))
print('Invalidated:',m.revise('temperature',2,reason='Synthetic correction'))
try:m.read('flag')
except ValueError as error:print('Expected rejection:',error)
m.recompute()
print('After reconstruction:',m.read('flag'))
print('Checkpoint:',log.verify())
print('Exact replay:',Memory(log).snapshot()==m.snapshot())
log.close()
