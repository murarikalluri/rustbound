"""Integration checks using the real Rust compiler and an isolated SQLite file."""
import json
import os
from pathlib import Path
import tempfile
import threading
import unittest
from io import BytesIO
from types import SimpleNamespace
from urllib.request import Request, urlopen, build_opener, HTTPCookieProcessor
from http.cookiejar import CookieJar
from urllib.error import HTTPError
import app
from curriculum import LEVELS

class CurriculumTests(unittest.TestCase):
    def test_cli_questions_reject_sample_output_only_programs(self):
        fixed=[l for l in LEVELS if l['mode']=='program' and not l.get('io_cases')]
        self.assertEqual([l['id'] for l in fixed],[1])
        for level in LEVELS:
            if not level.get('io_cases'): continue
            with self.subTest(level=level['id']):
                self.assertGreaterEqual(len(level['io_cases']),3)
                expected={out for _,out in level['io_cases']}
                self.assertGreater(len(expected),1)
                literal=json.dumps(level['io_cases'][0][1],ensure_ascii=False)
                sample_only='fn main() { println!("{}", '+literal+'); }'
                self.assertFalse(app.evaluate(level,sample_only)['passed'])

    def test_all_reference_solutions(self):
        for level in LEVELS:
            with self.subTest(level=level['id'],title=level['title']):
                result=app.evaluate(level,level['solution'])
                self.assertTrue(result['passed'],result['output'])
                print(f"PASS {level['id']:02}: {level['title']}", flush=True)

    def test_compile_error_and_wrong_answer(self):
        self.assertEqual(app.evaluate(LEVELS[0],'fn main( {')['phase'],'compile')
        self.assertFalse(app.evaluate(next(l for l in LEVELS if l['title'].startswith('Two Sum')),'fn two_sum(_: &[i32], _: i32) -> Option<(usize,usize)> { None }')['passed'])
        # This common bug reuses the same item for both indices.
        wrong='fn two_sum(a:&[i32],t:i32)->Option<(usize,usize)>{for j in 0..a.len(){for i in 0..=j{if a[i]+a[j]==t{return Some((i,j));}}}None}'
        self.assertFalse(app.evaluate(next(l for l in LEVELS if l['title'].startswith('Two Sum')),wrong)['passed'])

    def test_all_starters_require_a_solution(self):
        for level in LEVELS:
            with self.subTest(level=level['id']):
                self.assertFalse(app.evaluate(level,level['starter'])['passed'])
                self.assertGreaterEqual(len(level['tests']),2) if level['tests'] else self.assertTrue(level.get('io_cases') or level['expected'] is not None)
                for field in ('constraints','examples','hints','follow_up','complexity'):
                    self.assertTrue(level[field])

    def test_runtime_timeout(self):
        result=app.evaluate(LEVELS[0],'fn main() { loop { std::thread::sleep(std::time::Duration::from_secs(1)); } }')
        self.assertFalse(result['passed'])
        self.assertIn('Time limit',result['output'])

class AnswerVisibilityTests(unittest.TestCase):
    def test_answers_are_absent_from_course_and_removed_endpoint(self):
        original=app.DB
        with tempfile.TemporaryDirectory() as temp:
            try:
                app.DB=Path(temp)/'answers.sqlite3'
                app.init_db()
                with app.connect() as db:
                    uid=db.execute('INSERT INTO users(username,salt,password_hash) VALUES(?,?,?)',('visibility','unused','unused')).lastrowid
                payload=app.state(uid,'csrf')
                for level in payload['levels']:
                    self.assertNotIn('solution',level)
                    self.assertNotIn('tests',level)
                    self.assertNotEqual(level['starter'],LEVELS[level['id']-1]['solution'])
                # Exercise the real POST handler without opening a network socket.
                body=json.dumps({'level':1,'track':app.TRACK}).encode()
                handler=app.Handler.__new__(app.Handler)
                handler.server=SimpleNamespace(server_port=8765)
                handler.headers={'Host':'127.0.0.1:8765','X-Rustbound-Token':'csrf','Content-Length':str(len(body))}
                handler.path='/api/hint'
                handler.rfile=BytesIO(body)
                handler.session=lambda:{'user_id':uid,'csrf':'csrf'}
                responses=[]
                handler.respond=lambda data,status=200,**kwargs:responses.append((status,data))
                handler.do_POST()
                self.assertEqual(responses,[(404,{'error':'Not found'})])
                for filename in ('index.html','game.js','style.css'):
                    content=(app.ROOT/'static'/filename).read_text(encoding='utf-8')
                    self.assertNotIn('show-solution',content)
                    self.assertNotIn('solution-complexity',content)
            finally:
                app.DB=original

class ServerTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory()
        self.original=app.DB
        app.DB=Path(self.temp.name)/'test.sqlite3'
        self.server=app.make_server(0)
        self.thread=threading.Thread(target=self.server.serve_forever,daemon=True)
        self.thread.start()
        self.url=f'http://127.0.0.1:{self.server.server_port}'
        self.jar=CookieJar()
        self.client=build_opener(HTTPCookieProcessor(self.jar))
        self.token=app.TOKEN
        app.AUTH_REQUESTS.clear()

    def tearDown(self):
        self.server.shutdown();self.server.server_close();self.thread.join()
        app.DB=self.original;self.temp.cleanup()

    def request(self,path,body=None,token=None):
        if path=='/api/register' and isinstance(body,dict):
            body={'email':str(body.get('username','test'))+'@example.test','hint_question':'Which book inspired my password?','confirm_password':body.get('password'),**body}
        if isinstance(body,dict) and 'level' in body:
            body={'track':app.TRACK,**body}
        headers={'Content-Type':'application/json','X-Rustbound-Token':self.token if token is None else token}
        req=Request(self.url+path,data=json.dumps(body).encode() if body is not None else None,headers=headers)
        with self.client.open(req) as response:
            return json.loads(response.read())

    def register(self,name='explorer'):
        result=self.request('/api/register',{'username':name,'password':'A-test-password-42'},token=app.TOKEN)
        self.token=self.request('/api/state')['token']
        return result

    def assert_status(self,status,path,body=None,token=None):
        with self.assertRaises(HTTPError) as error:
            self.request(path,body,token)
        self.assertEqual(error.exception.code,status)

    def test_progress_drafts_locks_and_auth(self):
        self.register()
        with self.assertRaises(HTTPError) as error:
            self.request('/api/run',{'level':2,'code':LEVELS[1]['solution']})
        self.assertEqual(error.exception.code,403)
        with self.assertRaises(HTTPError) as error:
            self.request('/api/save',{'level':1,'code':'draft'},token='incorrect')
        self.assertEqual(error.exception.code,403)
        self.request('/api/save',{'level':1,'code':'draft'})
        self.assertEqual(self.request('/api/state')['progress']['1']['code'],'draft')
        self.assertTrue(self.request('/api/run',{'level':1,'code':LEVELS[0]['solution']})['passed'])
        self.assertTrue(self.request('/api/run',{'level':1,'code':LEVELS[0]['solution']})['passed'])
        self.assertFalse(self.request('/api/run',{'level':1,'code':'broken'})['passed'])
        state=self.request('/api/state')
        self.assertEqual(state['track'],app.TRACK)
        self.assertEqual(state['progress']['1']['passed'],1)
        self.assertEqual(state['progress']['1']['attempts'],3)
        self.assertNotIn('solution',state['levels'][0])
        self.assertTrue(state['levels'][0]['examples'])
        self.assert_status(409,'/api/save',{'level':1,'code':'stale code','track':'old'})
        self.assertTrue(self.request('/api/run',{'level':2,'code':LEVELS[1]['solution']})['passed'])
        # Re-open the database to verify durable, independent connection reads.
        app.init_db()
        self.assertEqual(self.request('/api/state')['progress']['2']['passed'],1)
        with self.client.open(self.url+'/') as response:
            self.assertEqual(response.status,200)
            self.assertIn(b'Rustbound',response.read())

    def test_registration_login_logout_and_expiry(self):
        self.assert_status(401,'/api/state')
        self.assert_status(401,'/api/save',{'level':1,'code':'private'})
        with self.client.open(self.url+'/') as response:
            self.assertTrue(response.url.endswith('/login'))
        self.assert_status(400,'/api/register',{'username':'xy','password':'short'})
        self.register('Explorer')
        cookie=list(self.jar)[0]
        self.assertIn('HttpOnly',cookie._rest)
        self.assertEqual(cookie._rest['SameSite'],'Strict')
        with app.connect() as db:
            user=db.execute('SELECT * FROM users').fetchone()
            self.assertNotEqual(user['password_hash'],'A-test-password-42')
            self.assertNotEqual(db.execute('SELECT token_hash FROM sessions').fetchone()[0],cookie.value)
        self.assert_status(409,'/api/register',{'username':'explorer','password':'Another-password'},app.TOKEN)
        self.request('/api/logout',{})
        self.assert_status(401,'/api/state')
        self.assertEqual(len(self.jar),0)
        self.assert_status(401,'/api/login',{'username':'Explorer','password':'wrong-password'},app.TOKEN)
        self.request('/api/login',{'username':'EXPLORER','password':'A-test-password-42'},app.TOKEN)
        self.token=self.request('/api/state')['token']
        self.assert_status(403,'/api/save',{'level':1,'code':'x'},app.TOKEN)
        with app.connect() as db:
            db.execute('UPDATE sessions SET expires_at=0')
        self.assert_status(401,'/api/state')

    def test_two_users_have_isolated_drafts_unlocks_and_activity(self):
        self.register('alice')
        alice_client,alice_token=self.client,self.token
        self.request('/api/run',{'level':1,'code':LEVELS[0]['solution']})
        alice_state=self.request('/api/state')
        alice_id=alice_state['user']['id']
        self.jar=CookieJar();self.client=build_opener(HTTPCookieProcessor(self.jar))
        self.register('bob')
        bob=self.request('/api/state')
        self.assertEqual(bob['progress'],{})
        self.assertEqual(bob['activity'],[])
        self.assert_status(403,'/api/run',{'level':2,'code':LEVELS[1]['solution']})
        # A submitted user_id must never choose whose progress is modified.
        self.request('/api/save',{'level':1,'code':'bob draft','user_id':alice_id})
        self.assertEqual(self.request('/api/state')['progress']['1']['code'],'bob draft')
        self.assert_status(403,'/api/save',{'level':1,'code':'stale alice tab'},alice_token)
        self.client,self.token=alice_client,alice_token
        alice=self.request('/api/state')
        self.assertEqual(alice['progress']['1']['code'],LEVELS[0]['solution'])
        self.assertEqual(alice['progress']['1']['passed'],1)
        self.assertEqual(len(alice['activity']),1)

    def test_legacy_progress_is_imported_once_without_deletion(self):
        with app.connect() as db:
            db.execute('INSERT INTO progress(level,code,passed,attempts,completed_at) VALUES(1,?,1,3,?)',('legacy draft','2026-10-29 00:00:00'))
            db.execute('INSERT INTO attempts(level,passed) VALUES(1,1)')
        self.assertTrue(self.request('/api/session')['legacy_available'])
        self.assertTrue(self.register('owner')['imported'])
        state=self.request('/api/state')
        self.assertEqual(state['progress'],{})
        self.assertEqual(state['archived_completed'],1)
        self.assertEqual(state['activity'],[])
        app.init_db()
        self.assertEqual(self.request('/api/state')['archived_completed'],1)
        self.request('/api/logout',{})
        self.assertFalse(self.register('newcomer')['imported'])
        self.assertEqual(self.request('/api/state')['progress'],{})
        with app.connect() as db:
            self.assertEqual(db.execute('SELECT code FROM progress').fetchone()[0],'legacy draft')
            self.assertEqual(db.execute('SELECT code FROM account_progress').fetchone()[0],'legacy draft')

    def test_existing_account_progress_is_kept_separate(self):
        self.register()
        user_id=self.request('/api/state')['user']['id']
        with app.connect() as db:
            db.execute('INSERT INTO account_progress(user_id,level,code,passed,attempts) VALUES(?,1,?,1,4)',(user_id,'old exercise draft'))
        app.init_db()
        state=self.request('/api/state')
        self.assertEqual(state['archived_completed'],1)
        self.assertEqual(state['progress'],{})
        self.assert_status(403,'/api/run',{'level':2,'code':LEVELS[1]['solution']})
        self.request('/api/save',{'level':1,'code':'new interview draft'})
        with app.connect() as db:
            self.assertEqual(db.execute('SELECT code FROM account_progress WHERE user_id=?',(user_id,)).fetchone()[0],'old exercise draft')
            self.assertEqual(db.execute('SELECT code FROM reviewed_progress WHERE user_id=?',(user_id,)).fetchone()[0],'new interview draft')

    def test_origin_validation_and_auth_rate_limit(self):
        req=Request(self.url+'/api/register',data=json.dumps({'username':'test','password':'test-password'}).encode(),headers={'Origin':'https://example.com','X-Rustbound-Token':app.TOKEN})
        with self.assertRaises(HTTPError) as error: self.client.open(req)
        self.assertEqual(error.exception.code,403)
        app.AUTH_REQUESTS.extend([app.time.time()]*20)
        self.assert_status(429,'/api/login',{'username':'test','password':'test-password'},app.TOKEN)

if __name__=='__main__': unittest.main(verbosity=2)
