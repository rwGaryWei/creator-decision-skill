import copy
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('decision',ROOT/'skills/creator-decision/scripts/decision.py')
d=importlib.util.module_from_spec(spec); spec.loader.exec_module(d)


def fixture():
    content='The supplied prototype has an undo control. Repeat usage is unknown.'
    return {'schema_version':'1.0',
        'project':{'id':'P-demo','title':'课程重排','domain':'web_tool','stage':'prototype','goal':'Reduce rescheduling effort','current_decision':'Add ten new screens?','constraints':['Solo creator'],'preserve':['Editable suggestions']},
        'report':{'id':'R-one','revision':1,'parent_report_id':None,'created_at':'2026-09-25T00:00:00Z','mode':'offline','summary':'Test the current task before adding screens.','observed_scope':['Supplied text only'],'limitations':['No browser use or audience testing'],'capabilities':{'network':'unavailable'}},
        'artifacts':[{'id':'ART-one','title':'description','version':'v1','kind':'text','access':'full','observed':['supplied description'],'not_observed':['working interaction']}],
        'sources':[{'id':'SRC-one','title':'Supplied description','kind':'user','synthetic':False,'access':'full','content':content,'sha256':d.digest(content.encode()),'retrieved_at':'2026-09-25T00:00:00Z','redistribution':'test fixture; original project material'}],
        'claims':[{'id':'CL-one','text':'The description includes undo.','kind':'user_statement','status':'supported','limitations':['Not run'],'evidence':[{'source_id':'SRC-one','quote':'has an undo control','location':'sentence 1'}]}],
        'assumptions':[{'id':'AS-one','text':'Undo is understandable.','state':'unknown','claim_ids':['CL-one'],'change_condition':'Observe recovery task.'}],
        'recommendations':[{'id':'REC-one','action':'test','target':'current recovery flow','reason':'Description is not interaction evidence.','keep':['Editable suggestions'],'tradeoff':'Delay expansion','condition':'Expand if correction effort is acceptable.','rationale_ids':['CL-one','AS-one']}],
        'experiments':[{'id':'EXP-one','assumption_ids':['AS-one'],'task':'Walk one conflict and undo.','observe':'Can change be understood and reversed?','decision_rule':'Fix confusion before adding screens; provisional project rule.','resource_limit':'One creator walkthrough','status':'planned','results':None}]}


class Validation(unittest.TestCase):
    def setUp(self): self.data=fixture()
    def rejects(self):
        with self.assertRaises(d.Invalid): d.validate(self.data)
    def test_valid_unicode_report(self): self.assertTrue(d.validate(self.data)['valid'])
    def test_literal_check_not_semantics(self):
        self.data['claims'][0]['text']='Every person will love this tool.'
        self.assertEqual(d.validate(self.data)['semantic_support'],'not_checked')
    def test_duplicate_json_keys(self):
        with self.assertRaises(d.Invalid): d.parse(b'{"id":1,"id":2}')
    def test_nan_not_json(self):
        with self.assertRaises(d.Invalid): d.parse(b'{"x":NaN}')
    def test_invalid_utf8(self):
        with self.assertRaises(d.Invalid): d.parse(b'\xff')
    def test_size_limit(self):
        with self.assertRaises(d.Invalid): d.parse(b' '*(d.MAX_BYTES+1))
    def test_schema_version(self): self.data['schema_version']='99'; self.rejects()
    def test_boolean_revision(self): self.data['report']['revision']=True; self.rejects()
    def test_timezone_required(self): self.data['report']['created_at']='2026-09-25'; self.rejects()
    def test_duplicate_object(self): self.data['claims'][0]['id']='SRC-one'; self.rejects()
    def test_cross_project_object(self): self.data['claims'][0]['project_id']='another'; self.rejects()
    def test_traversal_id(self): self.data['project']['id']='../private'; self.rejects()
    def test_reserved_filename(self): self.data['project']['id']='CON'; self.rejects()
    def test_missing_source(self): self.data['claims'][0]['evidence'][0]['source_id']='SRC-missing'; self.rejects()
    def test_mismatched_quote(self): self.data['claims'][0]['evidence'][0]['quote']='has ten screens'; self.rejects()
    def test_changed_capture(self): self.data['sources'][0]['content']='Changed'; self.rejects()
    def test_failed_source_not_observed(self): self.data['sources'][0]['access']='failed'; self.rejects()
    def test_failed_artifact_not_observed(self): self.data['artifacts'][0]['access']='failed'; self.rejects()
    def test_supported_external_needs_source(self): self.data['claims'][0].update(kind='external',evidence=[]); self.rejects()
    def test_unknown_external_allowed_with_warning(self):
        self.data['claims'][0].update(kind='external',status='unverified',evidence=[])
        self.assertTrue(d.validate(self.data)['warnings'])
    def test_synthetic_consistency(self): self.data['sources'][0]['synthetic']=True; self.rejects()
    def test_synthetic_cannot_prove_external(self):
        self.data['sources'][0].update(kind='synthetic',synthetic=True)
        self.data['claims'][0].update(kind='external'); self.rejects()
    def test_synthetic_inference_kept_unknown(self):
        self.data['sources'][0].update(kind='synthetic',synthetic=True)
        self.data['claims'][0].update(kind='inference',status='unverified')
        self.assertTrue(d.validate(self.data)['valid'])
    def test_unknown_assumption_reference(self): self.data['experiments'][0]['assumption_ids']=['missing']; self.rejects()
    def test_unknown_rationale(self): self.data['recommendations'][0]['rationale_ids']=['missing']; self.rejects()
    def test_missing_recommendation(self): self.data['recommendations']=[]; self.rejects()
    def test_expand_allowed(self): self.data['recommendations'][0]['action']='expand'; self.assertTrue(d.validate(self.data)['valid'])
    def test_planned_is_not_completed(self): self.data['experiments'][0]['results']='20 users liked it'; self.rejects()
    def test_completed_requires_results(self): self.data['experiments'][0]['status']='completed'; self.rejects()
    def test_no_fake_approval_in_report(self): self.data['approved']=True; self.rejects()
    def test_unsafe_link(self): self.data['sources'][0]['url']='javascript:alert(1)'; self.rejects()
    def test_credential_link(self): self.data['sources'][0]['url']='https://user:secret@example.com'; self.rejects()
    def test_bad_port(self): self.data['sources'][0]['url']='https://example.com:bad'; self.rejects()
    def test_html_and_markdown_are_text(self):
        self.data['report']['summary']='<script>alert(1)</script> [private](file:///secret)\n# malicious'
        out=d.render(self.data)
        self.assertNotIn('<script>',out); self.assertNotIn('[private](file:',out)
    def test_domain_is_not_steam_required(self):
        for domain in d.DOMAINS:
            self.data['project']['domain']=domain
            self.assertTrue(d.validate(self.data)['valid'])
    def test_compare_rejects_different_projects(self):
        other=copy.deepcopy(self.data); other['project']['id']='P-other'
        with self.assertRaises(d.Invalid): d.compare(self.data,other)
    def test_compare_goal_change(self):
        other=copy.deepcopy(self.data); other['project']['goal']='Artistic expression'
        self.assertIn('project',d.compare(self.data,other)['changed'])


class Storage(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory(); self.addCleanup(self.temp.cleanup)
        self.root=Path(self.temp.name)/'中文 folder'; self.input=Path(self.temp.name)/'input.json'
        self.data=fixture(); self.input.write_bytes(d.encode(self.data)); d.save_report(self.root,self.input)
    def decide(self,**kw):
        return d.decide(self.root,'P-demo','R-one','REC-one','accept','Yes, accept this recommendation.',**kw)
    def test_pending_by_default(self): self.assertEqual(d.decisions_for(self.root,'P-demo','R-one')[0]['decision'],'pending')
    def test_silence_not_acceptance(self):
        with self.assertRaises(d.Invalid): self.decide()
    def test_decision_and_readback(self):
        self.decide(confirmed=True)
        self.assertEqual(d.decisions_for(self.root,'P-demo','R-one')[0]['decision'],'accept')
    def test_repeat_does_not_duplicate(self):
        self.decide(confirmed=True); self.assertTrue(self.decide(confirmed=True)['duplicate'])
    def test_modified_report_invalidates_binding(self):
        self.decide(confirmed=True)
        self.data['report']['summary']='Different recommendation context.'
        (self.root/'P-demo/reports/R-one.json').write_bytes(d.encode(self.data))
        self.assertEqual(d.decisions_for(self.root,'P-demo','R-one')[0]['decision'],'pending')
    def test_new_version_stays_pending(self):
        self.decide(confirmed=True)
        self.data['report'].update(id='R-two',parent_report_id='R-one',revision=2)
        self.input.write_bytes(d.encode(self.data)); d.save_report(self.root,self.input)
        self.assertEqual(d.decisions_for(self.root,'P-demo','R-two')[0]['decision'],'pending')
    def test_revision_must_increase(self):
        self.data['report'].update(id='R-two',parent_report_id='R-one',revision=1)
        self.input.write_bytes(d.encode(self.data))
        with self.assertRaises(d.Invalid): d.save_report(self.root,self.input)
    def test_snapshot_never_overwrites(self):
        with self.assertRaises(d.Invalid): d.save_report(self.root,self.input)
    def test_interrupted_journal_is_preserved(self):
        log=self.root/'P-demo/decisions.jsonl'; log.write_bytes(b'{"broken":')
        with self.assertRaises(d.Invalid): self.decide(confirmed=True)
        self.assertEqual(log.read_bytes(),b'{"broken":')
    def test_journal_tamper_detected_locally(self):
        self.decide(confirmed=True); log=self.root/'P-demo/decisions.jsonl'
        log.write_text(log.read_text().replace('accept','reject'),encoding='utf-8')
        with self.assertRaises(d.Invalid): d.journal_read(log)
    def test_cross_project_journal_rejected(self):
        self.decide(confirmed=True); log=self.root/'P-demo/decisions.jsonl'; rows=d.journal_read(log)
        rows[0]['project_id']='P-other'; rows[0].pop('event_hash'); rows[0]['event_hash']=d.digest(d.encode(rows[0]))
        log.write_text(json.dumps(rows[0])+'\n')
        with self.assertRaises(d.Invalid): d.decisions_for(self.root,'P-demo','R-one')
    def test_lock_prevents_concurrent_overwrite(self):
        marker=self.root/'P-demo/.write.lock'; marker.write_text('another writer')
        with self.assertRaises(d.Invalid): self.decide(confirmed=True)
        self.assertTrue(marker.exists())
    def test_modify_requires_replacement(self):
        with self.assertRaises(d.Invalid): d.decide(self.root,'P-demo','R-one','REC-one','modify','Change it',True)
    def test_containment(self):
        with self.assertRaises(d.Invalid): d.contained(self.root,'..','private')
    def test_output_exclusive(self):
        p=self.root/'file.txt'; d.atomic(p,b'one')
        with self.assertRaises(d.Invalid): d.atomic(p,b'two')
        self.assertEqual(p.read_bytes(),b'one')


if __name__=='__main__': unittest.main()
