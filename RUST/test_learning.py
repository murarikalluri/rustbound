"""Reading persistence, access control, and executable educational examples."""
import subprocess
import tempfile
import unittest
from pathlib import Path
import app
from learning import LESSONS, MODULES, MODULE_DETAILS
from scenarios import SCENARIOS
from test_release import Client

class LibraryTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory(); self.old=app.DB
        app.DB=Path(self.temp.name)/'reading.sqlite3'; app.init_db(); app.AUTH_REQUESTS.clear()
    def tearDown(self):
        app.DB=self.old; self.temp.cleanup()
    def test_account_progress_and_reopen(self):
        alice=Client(); bob=Client(); self.assertEqual(alice.register()[0],200); self.assertEqual(bob.register('bobby')[0],200)
        self.assertEqual(Client().request('/api/library')[0],401)
        self.assertEqual(Client().request('/api/reading',{})[0],401)
        for kind,item in [('lesson','hello'),('scenario','lock-await')]:
            body=dict(kind=kind,item=item,completed=True)
            self.assertEqual(alice.request('/api/reading',body,token='wrong')[0],403)
            self.assertEqual(alice.request('/api/reading',body)[0],200)
            self.assertEqual(alice.request('/api/reading',body)[0],200)
        app.init_db()
        self.assertEqual(len(alice.request('/api/library')[1]['completed']),2)
        self.assertEqual(bob.request('/api/library')[1]['completed'],[])
        self.assertEqual(alice.request('/api/state')[1]['progress'],{})
        self.assertEqual(alice.request('/api/reading',dict(kind='lesson',item='hello',completed=False))[0],200)
        self.assertEqual(len(alice.request('/api/library')[1]['completed']),1)
        for body in [dict(kind='lesson',item='missing',completed=True),dict(kind='lesson',item='hello',completed=1),dict(kind='bad',item='hello',completed=True),dict(kind='lesson',item=[],completed=True)]:
            self.assertEqual(alice.request('/api/reading',body)[0],400)
    def test_catalog_integrity(self):
        self.assertEqual(len(LESSONS),92);self.assertEqual(len(MODULES),92)
        self.assertEqual(len(MODULE_DETAILS),92)
        self.assertEqual(len(SCENARIOS),40)
        self.assertEqual({x['book_chapter'] for x in LESSONS if x.get('book_chapter')},set(range(1,22)))
        ids={x['id'] for x in LESSONS};self.assertEqual(len(ids),len(LESSONS))
        self.assertEqual(len({s['id'] for s in SCENARIOS}),len(SCENARIOS))
        for item in LESSONS:
            for key in ('explain','code','walkthrough','use','question','source'):self.assertTrue(item[key],(item['id'],key))
            self.assertTrue(item['paragraphs'])
            for key in ('simple','syntax','simple_lab','group'):self.assertTrue(item[key],(item['id'],key))
            self.assertEqual(sum(x['module']==item['module'] for x in LESSONS),1)
            self.assertTrue(item['review'])
        self.assertEqual([x['day'] for x in LESSONS],list(range(1,93)))
        for index,item in enumerate(LESSONS):
            self.assertEqual(item['prerequisite'],LESSONS[index-1]['id'] if index else None)
        for module in MODULE_DETAILS:
            self.assertTrue(module['topics']);self.assertTrue(module['project'])
        for item in SCENARIOS:
            self.assertIn(item['lesson'],ids);self.assertTrue(item['source'].startswith('https://'))
            self.assertEqual(len(item['timeline']),3);self.assertEqual(len(item['investigation_questions']),3)
            self.assertTrue(item['context']);self.assertTrue(item['evidence']);self.assertIn('Fictional',item['simulation'])
            for key in ('symptom','diagnosis','cause','fix','verify','prevention','question'):self.assertTrue(item[key],(item['id'],key))
    def test_standalone_examples(self):
        for item in LESSONS:
            if item['language'] not in ('rust','rust-library'):continue
            with self.subTest(lesson=item['id']), tempfile.TemporaryDirectory() as folder:
                root=Path(folder); source=root/'example.rs'; binary=root/'example.exe';source.write_text(item['code'],encoding='utf-8')
                args=['rustc','--edition=2024',str(source),'-o',str(binary)]
                if item['language']=='rust-library':args+=['--crate-type','lib']
                result=subprocess.run(args,capture_output=True,text=True,timeout=30)
                self.assertEqual(result.returncode,0,result.stderr)
                if item['language']=='rust':
                    run=subprocess.run([str(binary)],capture_output=True,text=True,timeout=5)
                    self.assertEqual(run.returncode,0,run.stderr)
                if item['id']=='unit-tests':
                    result=subprocess.run(['rustc','--edition=2024','--test',str(source),'-o',str(binary)],capture_output=True,text=True,timeout=30)
                    self.assertEqual(result.returncode,0,result.stderr)
                    self.assertEqual(subprocess.run([str(binary)],capture_output=True,timeout=5).returncode,0)

if __name__=='__main__':unittest.main()
