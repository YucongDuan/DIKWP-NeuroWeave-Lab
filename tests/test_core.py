"""Core correctness tests; synthetic tasks do not establish biological validity."""
import json
import math
from pathlib import Path
import sqlite3
import tempfile
import unittest
from dataclasses import asdict
from neuroweave.util import canonical, digest, finite, integer, load_json, atomic_json
from neuroweave.evidence import Evidence, assess, claim_support
from neuroweave.ledger import Ledger, IntegrityError, ConflictError, GENESIS
from neuroweave.memory import Memory
from neuroweave.labs import make_memory, memory_demo, context_demo, purpose_demo, semantic_diff, consent_demo
from neuroweave.purpose import Purpose, ConsentSession


class ValidationTests(unittest.TestCase):
    def test_canonical_key_order(self): self.assertEqual(digest({'a':1,'b':2}),digest({'b':2,'a':1}))
    def test_nan_rejected(self):
        with self.assertRaises(ValueError): canonical({'x':math.nan})
    def test_infinity_rejected(self):
        with self.assertRaises(ValueError): finite(math.inf,'x')
    def test_boolean_not_numeric(self):
        with self.assertRaises(ValueError): finite(True,'x')
    def test_integer_bounds(self):
        with self.assertRaises(ValueError): integer(-1,'seed',0,100)
    def test_atomic_output(self):
        with tempfile.TemporaryDirectory() as d:
            path=Path(d)/'x.json';atomic_json(path,{'a':1});self.assertEqual(load_json(path),{'a':1})
    def test_strict_json(self):
        with tempfile.TemporaryDirectory() as d:
            path=Path(d)/'x.json';path.write_text('{"x":NaN}')
            with self.assertRaises(ValueError): load_json(path)


class EvidenceTests(unittest.TestCase):
    def e(self,id='a',low=1,high=2,**kwargs):
        values=dict(id=id,source='s',kind='synthetic',context='c',unit='mV',low=low,high=high,source_group='g',observed_at='t0');values.update(kwargs)
        return Evidence(**values)
    def test_missing(self): self.assertEqual(assess([])['status'],'incomplete')
    def test_conflict(self): self.assertEqual(assess([self.e(),self.e('b',3,4)])['status'],'inconsistent')
    def test_imprecision(self): self.assertEqual(assess([self.e()])['status'],'imprecise')
    def test_precision(self): self.assertEqual(assess([self.e(low=1,high=1)])['status'],'precise')
    def test_missing_flag(self): self.assertTrue(assess([self.e(),self.e('b',None,None)])['has_missing'])
    def test_context_not_merged(self): self.assertEqual(assess([self.e(),self.e('b',context='else')])['status'],'not_comparable')
    def test_time_not_merged(self): self.assertEqual(assess([self.e(),self.e('b',observed_at='t1')])['status'],'not_comparable')
    def test_units_not_merged(self): self.assertEqual(assess([self.e(),self.e('b',unit='V')])['status'],'not_comparable')
    def test_duplicate_rejected(self):
        with self.assertRaises(ValueError): assess([self.e(),self.e()])
    def test_source_group_not_double_counted(self): self.assertEqual(assess([self.e(),self.e('b')])['independent_source_groups'],1)
    def test_bounds_rejected(self):
        with self.assertRaises(ValueError): self.e(low=4,high=1)
    def test_one_missing_bound_rejected(self):
        with self.assertRaises(ValueError): self.e(low=None,high=1)
    def test_synthetic_cannot_validate_biology(self): self.assertEqual(claim_support('biological',[self.e()])['status'],'unsupported')
    def test_no_experience_verdict(self): self.assertEqual(claim_support('subjective_experience',[self.e()])['status'],'unresolved')


class MemoryTests(unittest.TestCase):
    def setUp(self): self.m=make_memory()
    def tearDown(self): self.m.ledger.close()
    def test_multihop(self): self.assertEqual(self.m.read('above_threshold'),1)
    def test_exact_invalidation_set(self): self.assertEqual(self.m.revise('sensor',2,reason='r'),['above_threshold','scaled'])
    def test_stale_read_rejected(self):
        self.m.revise('sensor',2,reason='r')
        with self.assertRaises(ValueError): self.m.read('above_threshold')
    def test_recompute_value(self):
        self.m.revise('sensor',2,reason='r');self.m.recompute();self.assertEqual(self.m.read('above_threshold'),0)
    def test_unrelated_unchanged(self):
        original=self.m.snapshot()['unrelated'];self.m.revise('sensor',2,reason='r');self.m.recompute()
        self.assertEqual(original,self.m.snapshot()['unrelated'])
    def test_prior_source_retained(self):
        self.m.revise('sensor',2,reason='r');self.assertEqual(self.m.ledger.events()[0]['payload']['value'],6)
    def test_revision_pinned(self):
        self.m.revise('sensor',2,reason='r');self.m.recompute();self.assertEqual(self.m.nodes['scaled']['dependency_revisions']['sensor'],2)
    def test_retraction_not_recomputed(self):
        self.m.retract('sensor',reason='r');self.m.recompute();self.assertEqual(self.m.nodes['scaled']['status'],'stale')
    def test_reactivation_by_explicit_revision(self):
        self.m.retract('sensor',reason='r');self.m.revise('sensor',8,reason='new evidence');self.m.recompute();self.assertEqual(self.m.read('scaled'),16)
    def test_replay(self):
        self.m.revise('sensor',2,reason='r');self.m.recompute();self.assertEqual(self.m.snapshot(),Memory(self.m.ledger).snapshot())
    def test_snapshot_is_copy(self):
        snap=self.m.snapshot();snap['sensor']['value']=99;self.assertEqual(self.m.read('sensor'),6)
    def test_duplicate_node(self):
        with self.assertRaises(ValueError): self.m.add_source('sensor',7,source='s',context='c')
    def test_cycle_rejected(self):
        with self.assertRaises(ValueError): self.m.derive('self',['self'],{'op':'sum'},context='c')
    def test_missing_dependency(self):
        with self.assertRaises(ValueError): self.m.derive('new',['missing'],{'op':'sum'},context='c')
    def test_cross_context_rejected(self):
        with self.assertRaises(ValueError): self.m.derive('new',['sensor'],{'op':'sum'},context='different')
    def test_unit_mismatch_rejected(self):
        with self.assertRaises(ValueError): self.m.derive('new',['sensor'],{'op':'sum'},context='trial',unit='V')
    def test_no_eval(self):
        with self.assertRaises(ValueError): self.m.derive('new',['sensor'],{'op':'__import__'},context='trial')
    def test_failed_write_atomic(self):
        head=self.m.ledger.head;snap=self.m.snapshot()
        with self.assertRaises(ValueError): self.m.revise('sensor',math.nan,reason='r')
        self.assertEqual(head,self.m.ledger.head);self.assertEqual(snap,self.m.snapshot())
    def test_derived_revision_rejected(self):
        with self.assertRaises(ValueError): self.m.revise('scaled',7,reason='r')
    def test_conflicting_writer(self):
        second=Memory(self.m.ledger);self.m.revise('sensor',2,reason='r')
        with self.assertRaises(ConflictError): second.revise('sensor',3,reason='r')
        self.assertEqual(second.read('sensor'),6)
    def test_persistence_after_close(self):
        with tempfile.TemporaryDirectory() as d:
            path=Path(d)/'memory.sqlite';log=Ledger(path);m=Memory(log);m.add_source('a',3,source='s',context='c');head=log.head;log.close()
            log=Ledger(path);self.assertEqual(Memory(log).read('a'),3);self.assertEqual(log.verify(head),head);log.close()


class LedgerTests(unittest.TestCase):
    def setUp(self): self.log=Ledger();self.log.append('a',{'v':1});self.log.append('b',{'v':2})
    def tearDown(self): self.log.close()
    def test_validate(self): self.assertEqual(self.log.verify(),self.log.head)
    def test_payload_tamper(self):
        with self.log.connection: self.log.connection.execute("UPDATE events SET payload=? WHERE seq=1",('{"v":9}',))
        with self.assertRaises(IntegrityError): self.log.verify()
    def test_middle_deletion(self):
        with self.log.connection: self.log.connection.execute('DELETE FROM events WHERE seq=1')
        with self.assertRaises(IntegrityError): self.log.verify()
    def test_checkpoint_detects_tail_deletion(self):
        head=self.log.head
        with self.log.connection: self.log.connection.execute('DELETE FROM events WHERE seq=2')
        with self.assertRaises(IntegrityError): self.log.verify(head)
    def test_unanchored_tail_limit_documented(self):
        with self.log.connection: self.log.connection.execute('DELETE FROM events WHERE seq=2')
        self.assertIsInstance(self.log.verify(),str)
    def test_append_on_corrupted_log_rejected(self):
        with self.log.connection: self.log.connection.execute("UPDATE events SET hash='x' WHERE seq=1")
        with self.assertRaises(IntegrityError): self.log.append('c',{})


class PurposeTests(unittest.TestCase):
    def setUp(self):
        self.p=Purpose('a','p','preserve',4);self.payload={'action':'simulated_message','text':'no'};self.s=ConsentSession();self.f=self.s.propose('id',self.payload,self.p,now=0,ttl=10)
    def test_goal_changes_action_not_facts(self):
        r=purpose_demo();self.assertNotEqual(r['action_a'],r['action_b']);self.assertEqual(r['facts_hash_before'],r['facts_hash_after'])
    def test_low_budget_rest(self): self.assertEqual(Purpose('a','p','explore',0).choose(.4),'rest')
    def test_unconfirmed(self):
        with self.assertRaises(PermissionError): self.s.execute('id',self.payload,self.p,actor='a',now=1)
    def test_wrong_actor(self):
        with self.assertRaises(PermissionError): self.s.confirm('id',self.f,actor='b',now=1)
    def test_changed_payload(self):
        self.s.confirm('id',self.f,actor='a',now=1)
        with self.assertRaises(PermissionError): self.s.execute('id',{**self.payload,'text':'yes'},self.p,actor='a',now=2)
    def test_changed_purpose(self):
        self.s.confirm('id',self.f,actor='a',now=1)
        with self.assertRaises(PermissionError): self.s.execute('id',self.payload,Purpose('a','q','explore',4),actor='a',now=2)
    def test_confirm_execute(self):
        self.s.confirm('id',self.f,actor='a',now=1);self.assertFalse(self.s.execute('id',self.payload,self.p,actor='a',now=2)['external_side_effect'])
    def test_no_replay(self):
        self.s.confirm('id',self.f,actor='a',now=1);self.s.execute('id',self.payload,self.p,actor='a',now=2)
        with self.assertRaises(PermissionError): self.s.execute('id',self.payload,self.p,actor='a',now=3)
    def test_revoke(self):
        self.s.confirm('id',self.f,actor='a',now=1);self.s.revoke('id',actor='a',now=2)
        with self.assertRaises(PermissionError): self.s.execute('id',self.payload,self.p,actor='a',now=3)
    def test_expiry(self):
        with self.assertRaises(PermissionError): self.s.confirm('id',self.f,actor='a',now=10)
    def test_time_reversal(self):
        self.s.confirm('id',self.f,actor='a',now=2)
        with self.assertRaises(ValueError): self.s.execute('id',self.payload,self.p,actor='a',now=1)
    def test_no_real_action(self):
        with self.assertRaises(ValueError): self.s.propose('real',{'action':'send_email'},self.p,now=1)
    def test_negation_preservation(self):
        a={'owner':'a','action':'send','negated':True,'context':'private'}
        self.assertFalse(semantic_diff(a,{**a,'negated':False})['faithful'])

from neuroweave.runtime import ResearchRuntime

class RuntimeTests(unittest.TestCase):
    def setUp(self):self.m=make_memory();self.r=ResearchRuntime(self.m,Purpose('a','p','explore',2))
    def tearDown(self):self.m.ledger.close()
    def test_state_partitions(self):self.assertEqual(set(self.r.state()),set('OEKVPB'))
    def test_plan_pins_revision(self):
        p=self.r.propose('x','scaled',now=0);self.assertEqual(p['payload']['node_revision'],1)
    def test_changed_evidence_invalidates_plan(self):
        self.r.propose('x','scaled',now=0);self.m.revise('sensor',2,reason='r')
        with self.assertRaises(PermissionError):self.r.confirm('x',actor='a',now=1)
    def test_changed_goal_invalidates_plan(self):
        self.r.propose('x','scaled',now=0);self.r.set_purpose(Purpose('a','q','preserve',2))
        with self.assertRaises(PermissionError):self.r.confirm('x',actor='a',now=1)
    def test_cannot_plan_stale_node(self):
        self.m.revise('sensor',2,reason='r')
        with self.assertRaises(ValueError):self.r.propose('x','scaled',now=0)
    def test_budget_enforced(self):
        with self.assertRaises(PermissionError):self.r.propose('x','scaled',now=0,cost=3)
    def test_resource_debited(self):
        self.r.propose('x','scaled',now=0);self.r.confirm('x',actor='a',now=1);self.r.execute('x',actor='a',now=2,seed=17)
        self.assertEqual(self.r.remaining,1.5)
    def test_feedback_is_synthetic(self):
        self.r.propose('x','scaled',now=0);self.r.confirm('x',actor='a',now=1);self.r.execute('x',actor='a',now=2,seed=17)
        self.assertEqual(self.m.nodes['feedback:x']['evidence_kind'],'synthetic')
    def test_pending_plan_invalidated_by_other_execution(self):
        self.r.propose('x','scaled',now=0);self.r.propose('y','scaled',now=0);self.r.confirm('x',actor='a',now=1);self.r.execute('x',actor='a',now=2,seed=17)
        with self.assertRaises(PermissionError):self.r.confirm('y',actor='a',now=3)
    def test_cannot_change_owner(self):
        with self.assertRaises(PermissionError):self.r.set_purpose(Purpose('b','p','explore',2))
