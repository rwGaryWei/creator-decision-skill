import copy
import importlib.util
from pathlib import Path
import tempfile
import unittest

ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('harness',ROOT/'evaluations/harness.py')
h=importlib.util.module_from_spec(spec); spec.loader.exec_module(h)


class EvaluationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.pilot=h.load(ROOT/'evaluations/cases/pilot.json')
        cls.candidates=h.load(ROOT/'evaluations/cases/test-candidates.json')

    def test_pilot_count_and_no_generated_results(self):
        m=h.prepare(self.pilot)
        self.assertEqual(len(m['jobs']),36)
        self.assertTrue(all(j['status']=='planned' and 'response' not in j for j in m['jobs']))

    def test_full_balanced_conditions(self):
        m=h.prepare(self.candidates,'full')
        self.assertEqual(len(m['jobs']),432)
        self.assertEqual(len({j['id'] for j in m['jobs']}),432)
        for c in self.candidates['cases']:
            self.assertEqual(sum(j['case_id']==c['id'] for j in m['jobs']),18)

    def test_reduced_count(self):
        m=h.prepare(self.candidates,'reduced')
        self.assertEqual(len(m['jobs']),180)
        selected={j['case_id'] for j in m['jobs'] if j['evidence']=='E1'}
        self.assertEqual(len(selected),12)
        for domain in ('web_tool','video','short_drama','game'):
            self.assertEqual(sum(c['id'] in selected for c in self.candidates['cases'] if c['domain']==domain),3)

    def test_reproducible_order(self):
        self.assertEqual(h.prepare(self.pilot),h.prepare(self.pilot))
        a=h.prepare(self.pilot); b=h.prepare(self.pilot,seed=10)
        self.assertNotEqual([j['id'] for j in a['jobs']],[j['id'] for j in b['jobs']])

    def test_incomplete_cases_refused(self):
        c=copy.deepcopy(self.candidates); c['cases'][0]['goal']='TO_BE_SPECIFIED'
        with self.assertRaises(ValueError): h.prepare(c,'full')

    def test_wrong_split_refused(self):
        c=copy.deepcopy(self.pilot); c['cases'][0]['split']='development'
        with self.assertRaises(ValueError): h.prepare(c)

    def test_duplicate_project_refused(self):
        c=copy.deepcopy(self.pilot); c['cases'][1]['project_group']=c['cases'][0]['project_group']
        with self.assertRaises(ValueError): h.prepare(c)

    def record(self,manifest):
        j=manifest['jobs'][0]
        return {'job_id':j['id'],'input_sha256':j['input_sha256'],'model':'UNIT-TEST-FIXTURE',
                'host':'test','settings':{'fixture':True},'started_at':'2026-09-25T00:00:00Z',
                'finished_at':'2026-09-25T00:00:01Z','provenance':'Synthetic pipeline test, not a model run',
                'status':'completed','response':'Fictional fixture response only.'}

    def test_input_binding(self):
        m=h.prepare(self.pilot); r=self.record(m); r['input_sha256']='wrong'
        with self.assertRaises(ValueError): h.ingest(m,r)

    def test_failed_run_needs_reason(self):
        m=h.prepare(self.pilot); r=self.record(m); r['status']='failed'
        with self.assertRaises(ValueError): h.ingest(m,r)
        r['error']='Fixture timeout'; self.assertEqual(h.ingest(m,r)['status'],'failed')

    def test_unexposed_timing_stays_unknown(self):
        m=h.prepare(self.pilot); r=self.record(m); r['started_at']=None
        with self.assertRaises(ValueError): h.ingest(m,r)
        r['timing_note']='Host did not expose model start time; no latency inferred.'
        self.assertIsNone(h.ingest(m,r)['started_at'])

    def test_blind_packet_preserves_text(self):
        m=h.prepare(self.pilot); r=self.record(m)
        packet,key=h.blind(m,[r]); item=packet['items'][0]
        self.assertEqual(item['response'],r['response'])
        self.assertNotIn('method',item)
        self.assertNotIn('system',item)
        self.assertEqual(key[item['blind_id']]['job_id'],r['job_id'])

    def test_duplicate_run_refused(self):
        m=h.prepare(self.pilot); r=self.record(m)
        with self.assertRaises(ValueError): h.blind(m,[r,r])

    def test_missing_results_not_success(self):
        m=h.prepare(self.pilot); result=h.analyze(m,[])
        self.assertEqual(result['complete_project_pairs'],0)
        self.assertIsNone(result['mean_S_minus_B0'])

    def test_known_paired_fixture(self):
        m=h.prepare(self.pilot); group=m['jobs'][0]['project_group']; ratings=[]
        for j in m['jobs']:
            if j['project_group']==group:
                ratings.append({'job_id':j['id'],'rater_id':'fixture','rater_type':'author',
                    'scores':{k:(2 if j['method']=='S' else 1) for k in h.METRICS},
                    'rationale':'Artificial values to verify paired arithmetic only.'})
        result=h.analyze(m,ratings)
        self.assertEqual(result['complete_project_pairs'],1)
        self.assertEqual(result['mean_S_minus_B0'],1)
        ratings[0]['scores']['actionability']=None
        with self.assertRaises(ValueError): h.analyze(m,ratings)

    def test_no_overwrite(self):
        with tempfile.TemporaryDirectory() as folder:
            p=Path(folder)/'record.json'; h.save(p,{'original':True})
            with self.assertRaises(FileExistsError): h.save(p,{'original':False})
            self.assertEqual(h.load(p),{'original':True})
