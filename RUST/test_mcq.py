import tempfile
import unittest
from pathlib import Path
import app
from mcq import QUESTIONS
from test_release import Client

class MCQTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory();self.old=app.DB;app.DB=Path(self.temp.name)/'mcq.sqlite3';app.init_db();app.AUTH_REQUESTS.clear();self.c=Client();self.c.register()
    def tearDown(self):app.DB=self.old;self.temp.cleanup()
    def submit(self,q,choice,**extra):return self.c.request('/api/mcq/answer',dict(version=app.MCQ_VERSION,question=q['id'],choice=choice,**extra))
    def test_questions_do_not_leak_answer_keys(self):
        self.assertEqual(Client().request('/api/mcq')[0],401)
        state=self.c.request('/api/mcq')[1]
        self.assertEqual(len(state['questions']),40)
        self.assertEqual(len({q['topic'] for q in QUESTIONS}),10)
        for q in state['questions']:
            self.assertNotIn('answer',q);self.assertNotIn('rationales',q);self.assertNotIn('explanation',q)
        for q in QUESTIONS:
            self.assertEqual(len(q['options']),4);self.assertEqual(len(set(q['options'])),4)
            self.assertEqual(len(q['rationales']),4);self.assertTrue(all(q['rationales']))
    def test_grading_all_questions(self):
        for q in QUESTIONS:
            status,result=self.submit(q,q['answer'])
            self.assertEqual(status,200);self.assertTrue(result['correct']);self.assertEqual(result['answer'],q['answer'])
        self.assertEqual(result['first_correct'],40);self.assertEqual(result['answered'],40)
    def test_first_attempt_retry_and_account_isolation(self):
        q=QUESTIONS[0];wrong=(q['answer']+1)%4
        self.assertFalse(self.submit(q,wrong)[1]['correct'])
        state=self.submit(q,q['answer'])[1]
        self.assertEqual(state['first_correct'],0);self.assertEqual(state['latest_correct'],1);self.assertEqual(state['total_attempts'],2)
        app.init_db();self.assertEqual(self.c.request('/api/mcq')[1]['progress'][q['id']]['attempts'],2)
        other=Client();other.register('bobby');self.assertEqual(other.request('/api/mcq')[1]['answered'],0)
        self.assertEqual(self.c.request('/api/state')[1]['progress'],{})
    def test_auth_csrf_and_validation(self):
        body=dict(version=app.MCQ_VERSION,question=QUESTIONS[0]['id'],choice=0)
        self.assertEqual(Client().request('/api/mcq/answer',body)[0],401)
        self.assertEqual(self.c.request('/api/mcq/answer',body,token='wrong')[0],403)
        for updates in ({'choice':True},{'choice':-1},{'choice':4},{'choice':'0'},{'question':'missing'}):
            self.assertEqual(self.c.request('/api/mcq/answer',{**body,**updates})[0],400)
        self.assertEqual(self.c.request('/api/mcq/answer',{**body,'version':'old'})[0],409)
        self.assertEqual(self.c.request('/api/mcq')[1]['total_attempts'],0)

if __name__=='__main__':unittest.main()
