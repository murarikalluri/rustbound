"""Account and upgrade tests exercising the HTTP handler without network sockets."""
import json
import tempfile
import unittest
from io import BytesIO
from pathlib import Path
from types import SimpleNamespace
from http.cookies import SimpleCookie
import app
from curriculum import LEVELS,REGIONS,MODULE_SIZES

class Client:
    def __init__(self): self.cookie='';self.csrf=app.TOKEN
    def request(self,path,body=None,token=None):
        h=app.Handler.__new__(app.Handler)
        h.server=SimpleNamespace(server_port=8765)
        h.headers={'Host':'127.0.0.1:8765','Cookie':self.cookie,'X-Rustbound-Token':token or self.csrf}
        h.path=path;results=[]
        def respond(data,status=200,content_type=None,headers=None):
            if headers and 'Set-Cookie' in headers:self.cookie=headers['Set-Cookie'].split(';')[0]
            results.append((status,data))
        h.respond=respond
        if body is None:h.do_GET()
        else:
            raw=json.dumps(body).encode();h.headers['Content-Length']=str(len(raw));h.rfile=BytesIO(raw);h.do_POST()
        return results[0]
    def register(self,name='alice',**extra):
        body=dict(username=name,password='Test-password-42',confirm_password='Test-password-42',email=name+'@example.test',display_name='Alice Explorer',hint_question='Which book inspired my password?')
        body.update(extra)
        result=self.request('/api/register',body,app.TOKEN)
        if result[0]==200:self.csrf=self.request('/api/state')[1]['token']
        return result

class ReleaseTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory();self.old=app.DB;app.DB=Path(self.temp.name)/'test.sqlite3';app.init_db();app.AUTH_REQUESTS.clear();self.c=Client()
    def tearDown(self):app.DB=self.old;self.temp.cleanup()
    def test_registration_fields_and_uniqueness(self):
        self.assertEqual(self.c.register(email='invalid')[0],400)
        self.assertEqual(self.c.register(confirm_password='different')[0],400)
        self.assertEqual(self.c.register(hint_question='')[0],400)
        self.assertEqual(self.c.register(hint_question='My password is Test-password-42')[0],400)
        self.assertEqual(self.c.register()[0],200)
        state=self.c.request('/api/state')[1]
        self.assertEqual(state['user']['email'],'alice@example.test')
        self.assertEqual(state['user']['display_name'],'Alice Explorer')
        self.assertNotIn('password_hash',state['user'])
        self.assertEqual(Client().register('bob',email='ALICE@example.test')[0],409)
        self.assertEqual(Client().request('/api/state')[0],401)
    def test_profile_password_and_isolation(self):
        self.c.register();other=Client();other.register('bob')
        body=dict(email='new@example.test',display_name='Updated',hint_question='Which place do I remember?',current_password='wrong-password')
        self.assertEqual(self.c.request('/api/profile',body)[0],400)
        body['current_password']='Test-password-42'
        self.assertEqual(self.c.request('/api/profile',body)[0],200)
        self.assertEqual(self.c.request('/api/state')[1]['user']['email'],'new@example.test')
        self.assertEqual(other.request('/api/state')[1]['user']['email'],'bob@example.test')
        self.assertEqual(self.c.request('/api/profile',{**body,'email':'bob@example.test'})[0],409)
    def test_course_shape_private_answers_and_locks(self):
        self.c.register();state=self.c.request('/api/state')[1]
        self.assertEqual(len(state['levels']),100);self.assertEqual(len(REGIONS),8)
        self.assertEqual([sum(l['region']==i for l in LEVELS) for i in range(8)],MODULE_SIZES)
        self.assertEqual(LEVELS[0]['title'],'Hello, world!')
        self.assertEqual(len({l['title'] for l in LEVELS}),100)
        for l in state['levels']:
            self.assertNotIn('solution',l);self.assertNotIn('tests',l)
        self.assertEqual(self.c.request('/api/hint',dict(level=1,track=app.TRACK))[0],404)
        self.assertEqual(self.c.request('/api/save',dict(level=2,code='x',track=app.TRACK))[0],403)
        self.assertEqual(self.c.request('/api/save',dict(level=1,code='draft',track='interview-v1'))[0],409)
        self.assertEqual(self.c.request('/api/save',dict(level=1,code='draft',track=app.TRACK))[0],200)
        self.assertEqual(self.c.request('/api/state')[1]['progress'][1]['code'],'draft')
    def test_old_interviews_migrate_once_without_erasing_basics(self):
        self.c.register();uid=self.c.request('/api/state')[1]['user']['id']
        with app.connect() as db:
            db.execute('INSERT INTO interview_progress(user_id,level,code,passed,attempts) VALUES(?,1,?,1,3)',(uid,'old two sum'))
            db.execute('INSERT INTO interview_attempts(user_id,level,passed) VALUES(?,1,1)',(uid,))
            db.execute('DELETE FROM migrations WHERE name IN (?,?)',(app.TRACK,'course100-v1'))
        app.init_db();app.init_db()
        target=next(l['id'] for l in LEVELS if l.get('legacy_id')==1)
        state=self.c.request('/api/state')[1]
        self.assertEqual(state['progress'][target]['code'],'old two sum')
        self.assertEqual(state['progress'][target]['attempts'],3)
        self.assertNotIn(1,state['progress'])
        self.assertEqual(len(state['activity']),1)
        with app.connect() as db:self.assertEqual(db.execute('SELECT code FROM interview_progress').fetchone()[0],'old two sum')
    def test_existing_account_can_add_required_details(self):
        with app.connect() as db:
            salt='00'*16
            db.execute('INSERT INTO users(username,salt,password_hash) VALUES(?,?,?)',('olduser',salt,app.password_hash('Test-password-42',salt)))
        self.assertEqual(self.c.request('/api/login',dict(username='olduser',password='Test-password-42'),app.TOKEN)[0],200)
        self.c.csrf=self.c.request('/api/state')[1]['token']
        self.assertIsNone(self.c.request('/api/state')[1]['user']['email'])
        self.assertEqual(self.c.request('/api/profile',dict(email='old@example.test',display_name='Old user',hint_question='Which book do I like?',current_password='Test-password-42'))[0],200)

    def test_replaced_questions_are_archived_unchanged_questions_preserved(self):
        self.c.register();uid=self.c.request('/api/state')[1]['user']['id']
        with app.connect() as db:
            for number in (2,26):
                db.execute('INSERT INTO course_progress(user_id,level,code,passed,attempts) VALUES(?,?,?,1,2)',(uid,number,'old draft'))
                db.execute('INSERT INTO course_attempts(user_id,level,passed) VALUES(?,?,1)',(uid,number))
            db.execute('DELETE FROM migrations WHERE name=?',(app.TRACK,))
        app.init_db();app.init_db()
        state=self.c.request('/api/state')[1]
        self.assertNotIn(2,state['progress'])
        self.assertEqual(state['progress'][26]['code'],'old draft')
        self.assertEqual(len(state['activity']),1)
        self.assertEqual(self.c.request('/api/save',dict(level=1,code='old tab',track='course100-v1'))[0],409)
        with app.connect() as db:
            self.assertEqual(db.execute('SELECT COUNT(*) FROM course_progress').fetchone()[0],2)

if __name__=='__main__':unittest.main(verbosity=2)
