import json
import math
import statistics
import tempfile
from pathlib import Path
from dataclasses import fields
import unittest
from neuroweave.models import lif, causal, homeostasis, mechanism_trace, network, plasticity
from neuroweave.evaluation import Observation, Prediction, Truth, predict, generate, score, benchmark, mean_ci
from neuroweave.labs import run_lab, chapters, context_demo
from neuroweave.reporting import write_report
from neuroweave.util import digest


class NumericalTests(unittest.TestCase):
    def test_passive_exact_solution(self):
        result=lif(current_na=.1,duration_ms=20)
        self.assertAlmostEqual(result['series'][-1][1],-65+10*(1-math.exp(-1)),places=11)
    def test_subthreshold_no_spikes(self): self.assertEqual(lif(current_na=.1)['spike_count'],0)
    def test_first_spike_analytic(self): self.assertAlmostEqual(lif()['spike_times_ms'][0],20*math.log(4),places=10)
    def test_interspike_analytic(self):
        spikes=lif()['spike_times_ms']
        self.assertAlmostEqual(spikes[1]-spikes[0],2+20*math.log(4),places=10)
    def test_recording_interval_invariance(self):
        a,b=lif(dt_ms=.3),lif(dt_ms=.8)
        self.assertEqual(len(a['spike_times_ms']),len(b['spike_times_ms']))
        for x,y in zip(a['spike_times_ms'],b['spike_times_ms']):self.assertAlmostEqual(x,y,places=9)
    def test_invalid_dt(self):
        with self.assertRaises(ValueError):lif(dt_ms=0)
    def test_nonfinite_input(self):
        with self.assertRaises(ValueError):lif(current_na=math.nan)
    def test_invalid_reset(self):
        with self.assertRaises(ValueError):lif(reset_mv=-40)
    def test_causal_observation_slope(self):self.assertAlmostEqual(causal(17)['observational_slope'],2,delta=.08)
    def test_causal_do_effect(self):self.assertAlmostEqual(causal(17)['paired_do_effect'],1,places=12)
    def test_no_confounder_slope(self):self.assertAlmostEqual(causal(17,gamma=0)['observational_slope'],1,delta=.08)
    def test_budget_conservation(self):
        for p in homeostasis(17)['policies'].values():self.assertAlmostEqual(p['balance_residual'],0,places=10)
    def test_resource_aware_work(self):
        p=homeostasis(17)['policies'];self.assertGreater(p['resource_aware']['completed_work_steps'],p['always_work']['completed_work_steps'])
    def test_matched_behavior(self):self.assertEqual(mechanism_trace(17,'recurrent_workspace','baseline')['series'],mechanism_trace(17,'sensory_filter','baseline')['series'])
    def test_lesion_discriminates(self):self.assertNotEqual(mechanism_trace(17,'recurrent_workspace','workspace_lesion')['series'],mechanism_trace(17,'sensory_filter','workspace_lesion')['series'])
    def test_sham(self):self.assertEqual(mechanism_trace(17,'recurrent_workspace','baseline')['series'],mechanism_trace(17,'recurrent_workspace','sham')['series'])
    def test_rescue(self):self.assertEqual(mechanism_trace(17,'recurrent_workspace','baseline')['series'],mechanism_trace(17,'recurrent_workspace','rescue')['series'])
    def test_report_not_latent(self):
        result=mechanism_trace(17,'recurrent_workspace','report_lesion');self.assertEqual(result['report_energy'],0);self.assertGreater(result['latent_energy'],0)
    def test_chain_dies_cycle_persists(self):
        result=network(17)['networks'];self.assertEqual(result['chain']['terminal_activity'],0);self.assertGreater(result['cycle']['terminal_activity'],0)
    def test_plasticity_reversal(self):
        r=plasticity(17)['estimators'];self.assertLess(r['adaptive_ema']['post_change_prediction_mse'],r['running_average']['post_change_prediction_mse'])


class EvaluationTests(unittest.TestCase):
    def test_observation_has_no_label(self):self.assertNotIn('label',{x.name for x in fields(Observation)})
    def test_dict_with_label_rejected(self):
        with self.assertRaises(TypeError):predict({'id':'x','label':1},'precision_weighted')
    def test_probability_no_truth_dependency(self):
        observations,labels=generate(10,40)
        before=[predict(o,'precision_weighted') for o in observations]
        flipped=[Truth(t.id,1-t.label) for t in labels]
        after=[predict(o,'precision_weighted') for o in observations]
        self.assertEqual(before,after)
        self.assertNotEqual(score(labels,before)['accuracy_all_cases'],score(flipped,after)['accuracy_all_cases'])
    def test_unknown_model(self):
        with self.assertRaises(ValueError):predict(Observation('a',1,1,1,1),'unknown')
    def test_sigma_zero(self):
        with self.assertRaises(ValueError):Observation('a',1,1,0,1)
    def test_nan_prediction(self):
        with self.assertRaises(ValueError):Prediction('a',math.nan)
    def test_invalid_truth(self):
        with self.assertRaises(ValueError):Truth('a',2)
    def test_missing_penalizes_accuracy(self):self.assertEqual(score([Truth('a',1),Truth('b',0)],[Prediction('a',1)])['accuracy_all_cases'],.5)
    def test_missing_penalizes_brier(self):self.assertEqual(score([Truth('a',1),Truth('b',0)],[Prediction('a',1)])['brier_all_cases_missing_penalty_1'],.5)
    def test_observed_accuracy_distinct(self):self.assertEqual(score([Truth('a',1),Truth('b',0)],[Prediction('a',1)])['accuracy_observed_only'],1)
    def test_all_missing(self):
        r=score([Truth('a',1)],[]);self.assertEqual(r['coverage'],0);self.assertEqual(r['brier_all_cases_missing_penalty_1'],1);self.assertIsNone(r['accuracy_observed_only'])
    def test_duplicate_predictions(self):
        with self.assertRaises(ValueError):score([Truth('a',1)],[Prediction('a',1),Prediction('a',0)])
    def test_unknown_predictions(self):
        with self.assertRaises(ValueError):score([Truth('a',1)],[Prediction('b',1)])
    def test_duplicate_truths(self):
        with self.assertRaises(ValueError):score([Truth('a',1),Truth('a',0)],[])
    def test_empty_eval(self):
        with self.assertRaises(ValueError):score([],[])
    def test_brier_analytic(self):self.assertAlmostEqual(score([Truth('a',1),Truth('b',0)],[Prediction('a',.8),Prediction('b',.1)])['brier_all_cases_missing_penalty_1'],.025)
    def test_perfect_probability_bins(self):self.assertEqual(score([Truth('a',1)],[Prediction('a',1)])['calibration_bins_observed_only'][-1]['n'],1)
    def test_seed_determinism(self):self.assertEqual(generate(7),generate(7))
    def test_bootstrap_determinism(self):self.assertEqual(mean_ci([1,2,3]),mean_ci([1,2,3]))
    def test_bootstrap_units(self):self.assertEqual(mean_ci([1,2,3])['n_independent_seeds'],3)
    def test_benchmark_protocol(self):
        b=benchmark([1000,1001],30);self.assertEqual(b['protocol_hash'],digest(b['protocol']));self.assertFalse(b['independent_external_validation'])
    def test_benchmark_duplicate_seeds(self):
        with self.assertRaises(ValueError):benchmark([1,1],30)


class ChapterTests(unittest.TestCase):
    def test_eighteen_chapters(self):self.assertEqual(len(chapters()),18)
    def test_context_proposition_witness(self):
        r=context_demo();self.assertEqual(r['observations'][0],r['observations'][1]);self.assertNotEqual(r['required_actions'][0],r['required_actions'][1])
    def test_unknown_id(self):
        with self.assertRaises(ValueError):run_lab('unknown')
    def test_parameter_allowlist(self):
        with self.assertRaises(ValueError):run_lab('chapter-07',parameters={'shell':'hello'})
    def test_parameter_copy(self):
        params={'current_na':.2};r=run_lab('chapter-07',parameters=params);params['current_na']=4;self.assertEqual(digest(r['protocol']),r['protocol_hash'])
    def test_invalid_seed(self):
        with self.assertRaises(ValueError):run_lab('chapter-10',seed=-1)
    def test_integrated_state_partitions(self):
        r=run_lab('chapter-16')['result'];self.assertEqual(set(r['initial']),set('OEKVPB'));self.assertTrue(r['facts_preserved_under_goal_change']);self.assertTrue(r['replay_equal'])
    def test_html_escapes_text(self):
        r=run_lab('chapter-01');r['chapter']['lab_title']='<script>alert(1)</script>'
        with tempfile.TemporaryDirectory() as d:
            write_report(d,[r]);text=(Path(d)/'index.html').read_text();self.assertIn('&lt;script&gt;',text);self.assertNotIn('<script>',text)

# Each recipe is an independently counted runnable / deterministic test.
def recipe_test(id):
    def test(self):
        a,b=run_lab(id,17),run_lab(id,17)
        self.assertEqual(a,b);self.assertEqual(digest(a['result']),a['result_hash']);self.assertEqual(digest(a['protocol']),a['protocol_hash']);self.assertFalse(a['biological_validation']);json.dumps(a,allow_nan=False)
    return test
for chapter in chapters():setattr(ChapterTests,'test_'+chapter['id'].replace('-','_'),recipe_test(chapter['id']))
