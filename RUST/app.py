"""Rustbound: local Python website and SQLite-backed learning game."""
import json
import os
from pathlib import Path
import secrets
import shutil
import sqlite3
import subprocess
import tempfile
import threading
import hashlib
import re
import time
from collections import deque
from http.cookies import SimpleCookie, CookieError
from contextlib import contextmanager
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlparse
from curriculum import LEVELS, REGIONS, UPDATED_IDS
from learning import LESSONS, MODULES, MODULE_DETAILS
from scenarios import SCENARIOS, REVIEWED
from mcq import QUESTIONS, public_questions

ROOT = Path(__file__).resolve().parent
DB = Path(os.environ.get('RUSTBOUND_DB', ROOT / 'progress.sqlite3'))
TOKEN = secrets.token_urlsafe(32)
RUN_LOCK = threading.Lock()
AUTH_LOCK = threading.Lock()
AUTH_REQUESTS = deque()
SESSION_AGE = 7 * 24 * 60 * 60
TRACK = 'course100-v2'
MCQ_VERSION = 'mcq-v1'

def mcq_state(user_id):
    with connect() as db:
        rows=[dict(row) for row in db.execute('SELECT question,choice,correct,created_at FROM mcq_attempts WHERE user_id=? AND version=? ORDER BY id',(user_id,MCQ_VERSION))]
    progress={}
    for row in rows:
        previous=progress.get(row['question'])
        progress[row['question']]={**row,'attempts':previous['attempts']+1 if previous else 1,'first_correct':previous['first_correct'] if previous else row['correct']}
    return dict(progress=progress,total_attempts=len(rows),answered=len(progress),first_correct=sum(x['first_correct'] for x in progress.values()),latest_correct=sum(x['correct'] for x in progress.values()))

def account_details(body):
    email=body.get('email','')
    name=body.get('display_name','')
    hint=body.get('hint_question','')
    if not isinstance(email,str) or len(email)>254 or not re.fullmatch(r'[^\s@]+@[^\s@]+\.[^\s@]+',email.strip()):
        raise ValueError('Enter a valid email address.')
    if not isinstance(name,str) or len(name.strip())>60:
        raise ValueError('Name must be at most 60 characters.')
    if not isinstance(hint,str) or not 5<=len(hint.strip())<=160:
        raise ValueError('Enter a password hint question of 5–160 characters. Do not include your password.')
    return email.strip().casefold(),name.strip(),hint.strip()

def password_hash(password, salt):
    return hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), bytes.fromhex(salt), 600_000).hex()

def token_hash(value):
    return hashlib.sha256(value.encode()).hexdigest()

@contextmanager
def connect():
    db = sqlite3.connect(DB, timeout=10)
    db.row_factory = sqlite3.Row
    db.execute('PRAGMA foreign_keys=ON')
    try:
        with db:
            yield db
    finally:
        db.close()

def init_db():
    with connect() as db:
        db.executescript('''
        CREATE TABLE IF NOT EXISTS progress(level INTEGER PRIMARY KEY, code TEXT NOT NULL DEFAULT '', passed INTEGER NOT NULL DEFAULT 0, attempts INTEGER NOT NULL DEFAULT 0, completed_at TEXT);
        CREATE TABLE IF NOT EXISTS attempts(id INTEGER PRIMARY KEY, level INTEGER NOT NULL, passed INTEGER NOT NULL, created_at TEXT DEFAULT CURRENT_TIMESTAMP);
        CREATE TABLE IF NOT EXISTS users(id INTEGER PRIMARY KEY, username TEXT NOT NULL COLLATE NOCASE UNIQUE, salt TEXT NOT NULL, password_hash TEXT NOT NULL, created_at TEXT DEFAULT CURRENT_TIMESTAMP);
        CREATE TABLE IF NOT EXISTS sessions(token_hash TEXT PRIMARY KEY, user_id INTEGER NOT NULL REFERENCES users(id), csrf TEXT NOT NULL, expires_at REAL NOT NULL);
        CREATE TABLE IF NOT EXISTS account_progress(user_id INTEGER NOT NULL REFERENCES users(id), level INTEGER NOT NULL, code TEXT NOT NULL DEFAULT '', passed INTEGER NOT NULL DEFAULT 0, attempts INTEGER NOT NULL DEFAULT 0, completed_at TEXT, PRIMARY KEY(user_id,level));
        CREATE TABLE IF NOT EXISTS account_attempts(id INTEGER PRIMARY KEY, user_id INTEGER NOT NULL REFERENCES users(id), level INTEGER NOT NULL, passed INTEGER NOT NULL, created_at TEXT DEFAULT CURRENT_TIMESTAMP);
        CREATE INDEX IF NOT EXISTS account_attempts_user ON account_attempts(user_id, id);
        CREATE TABLE IF NOT EXISTS interview_progress(user_id INTEGER NOT NULL REFERENCES users(id), level INTEGER NOT NULL, code TEXT NOT NULL DEFAULT '', passed INTEGER NOT NULL DEFAULT 0, attempts INTEGER NOT NULL DEFAULT 0, completed_at TEXT, PRIMARY KEY(user_id,level));
        CREATE TABLE IF NOT EXISTS interview_attempts(id INTEGER PRIMARY KEY, user_id INTEGER NOT NULL REFERENCES users(id), level INTEGER NOT NULL, passed INTEGER NOT NULL, created_at TEXT DEFAULT CURRENT_TIMESTAMP);
        CREATE INDEX IF NOT EXISTS interview_attempts_user ON interview_attempts(user_id,id);
        CREATE TABLE IF NOT EXISTS course_progress(user_id INTEGER NOT NULL REFERENCES users(id), level INTEGER NOT NULL, code TEXT NOT NULL DEFAULT '', passed INTEGER NOT NULL DEFAULT 0, attempts INTEGER NOT NULL DEFAULT 0, completed_at TEXT, PRIMARY KEY(user_id,level));
        CREATE TABLE IF NOT EXISTS course_attempts(id INTEGER PRIMARY KEY, user_id INTEGER NOT NULL REFERENCES users(id), level INTEGER NOT NULL, passed INTEGER NOT NULL, created_at TEXT DEFAULT CURRENT_TIMESTAMP);
        CREATE INDEX IF NOT EXISTS course_attempts_user ON course_attempts(user_id,id);
        CREATE TABLE IF NOT EXISTS migrations(name TEXT PRIMARY KEY);
        CREATE TABLE IF NOT EXISTS reviewed_progress(user_id INTEGER NOT NULL REFERENCES users(id), level INTEGER NOT NULL, code TEXT NOT NULL DEFAULT '', passed INTEGER NOT NULL DEFAULT 0, attempts INTEGER NOT NULL DEFAULT 0, completed_at TEXT, PRIMARY KEY(user_id,level));
        CREATE TABLE IF NOT EXISTS reviewed_attempts(id INTEGER PRIMARY KEY, user_id INTEGER NOT NULL REFERENCES users(id), level INTEGER NOT NULL, passed INTEGER NOT NULL, created_at TEXT DEFAULT CURRENT_TIMESTAMP);
        CREATE INDEX IF NOT EXISTS reviewed_attempts_user ON reviewed_attempts(user_id,id);
        CREATE TABLE IF NOT EXISTS reading_progress(user_id INTEGER NOT NULL REFERENCES users(id), kind TEXT NOT NULL, item TEXT NOT NULL, completed_at TEXT DEFAULT CURRENT_TIMESTAMP, PRIMARY KEY(user_id,kind,item));
        CREATE TABLE IF NOT EXISTS mcq_attempts(id INTEGER PRIMARY KEY, user_id INTEGER NOT NULL REFERENCES users(id), version TEXT NOT NULL, question TEXT NOT NULL, choice INTEGER NOT NULL, correct INTEGER NOT NULL, created_at TEXT DEFAULT CURRENT_TIMESTAMP);
        CREATE INDEX IF NOT EXISTS mcq_attempts_user ON mcq_attempts(user_id,version,id);

        ''')
        db.execute('BEGIN IMMEDIATE')
        columns={row['name'] for row in db.execute('PRAGMA table_info(users)')}
        for column,definition in [('email','TEXT COLLATE NOCASE'),('display_name',"TEXT NOT NULL DEFAULT ''"),('hint_question',"TEXT NOT NULL DEFAULT ''")]:
            if column not in columns: db.execute(f'ALTER TABLE users ADD COLUMN {column} {definition}')
        db.execute('CREATE UNIQUE INDEX IF NOT EXISTS users_email ON users(email) WHERE email IS NOT NULL')
        if not db.execute('SELECT 1 FROM migrations WHERE name=?',('course100-v1',)).fetchone():
            for level in LEVELS:
                if level.get('legacy_id'):
                    db.execute('INSERT OR IGNORE INTO course_progress SELECT user_id,?,code,passed,attempts,completed_at FROM interview_progress WHERE level=?',(level['id'],level['legacy_id']))
                    db.execute('INSERT INTO course_attempts(user_id,level,passed,created_at) SELECT user_id,?,passed,created_at FROM interview_attempts WHERE level=?',(level['id'],level['legacy_id']))
            db.execute('INSERT INTO migrations VALUES(?)',('course100-v1',))
        if not db.execute('SELECT 1 FROM migrations WHERE name=?',(TRACK,)).fetchone():
            for level in LEVELS:
                if level['id'] not in UPDATED_IDS:
                    db.execute('INSERT OR IGNORE INTO reviewed_progress SELECT * FROM course_progress WHERE level=?',(level['id'],))
                    db.execute('INSERT INTO reviewed_attempts(user_id,level,passed,created_at) SELECT user_id,level,passed,created_at FROM course_attempts WHERE level=?',(level['id'],))
            db.execute('INSERT INTO migrations VALUES(?)',(TRACK,))

def state(user_id, csrf):
    with connect() as db:
        progress = {r['level']: dict(r) for r in db.execute('SELECT level,code,passed,attempts,completed_at FROM reviewed_progress WHERE user_id=?',(user_id,))}
        archived = db.execute('SELECT COUNT(*) FROM account_progress WHERE user_id=? AND passed=1',(user_id,)).fetchone()[0]
        user = dict(db.execute('SELECT id,username,created_at,email,display_name,hint_question FROM users WHERE id=?',(user_id,)).fetchone())
        activity = [dict(r) for r in db.execute('SELECT level,passed,created_at FROM reviewed_attempts WHERE user_id=? ORDER BY id DESC LIMIT 10',(user_id,))]
    return dict(track=TRACK, archived_completed=archived, user=user, activity=activity, levels=[{k:v for k,v in l.items() if k not in ('solution','tests','expected','legacy_id','io_cases')} | {'test_count':len(l['io_cases']) if l.get('io_cases') else len(l['tests']) if l['tests'] else 1} for l in LEVELS], regions=REGIONS, progress=progress, token=csrf, compiler=bool(shutil.which('rustc')))

def run_process(command, cwd, timeout, input_text=None):
    # Output goes to disk to avoid unbounded in-memory capture.
    with tempfile.TemporaryFile() as out:
        try:
            result = subprocess.run(command, cwd=cwd, stdout=out, stderr=out, timeout=timeout, input=input_text.encode('utf-8') if input_text is not None else b'',
                                    creationflags=subprocess.CREATE_NO_WINDOW if os.name=='nt' else 0)
            out.seek(0)
            return result.returncode, out.read(16000).decode('utf-8', errors='replace')
        except subprocess.TimeoutExpired:
            return -1, f'Time limit reached ({timeout}s). Check for an infinite loop or blocked thread.'

def evaluate(level, code):
    compiler = shutil.which('rustc')
    if not compiler:
        return dict(passed=False, output='Rust compiler not found. Install Rust from rustup.rs, then restart Rustbound.', checks=[])
    with tempfile.TemporaryDirectory(prefix='rustbound-') as temp:
        folder = Path(temp)
        source = code
        if level['tests']:
            checks = '\n'.join(f'assert_eq!({expr}, {expected}, "Check {i+1}"); println!("CHECK_{i+1}_OK");' for i,(expr,expected) in enumerate(level['tests']))
            source += '\nfn main() {\n' + checks + '\n}\n'
        (folder/'main.rs').write_text(source, encoding='utf-8')
        exe = folder/('challenge.exe' if os.name=='nt' else 'challenge')
        status, output = run_process([compiler,'--edition=2024','--color=never',str(folder/'main.rs'),'-o',str(exe)], temp, 30)
        output = output.replace(str(folder), '<challenge>')
        if status:
            return dict(passed=False, output=output, checks=[], phase='compile')
        if level.get('io_cases'):
            checks=[];messages=[]
            for i,(stdin,expected) in enumerate(level['io_cases']):
                status,runtime=run_process([str(exe)],temp,5,stdin)
                ok=status==0 and runtime.replace('\r\n','\n').rstrip('\n')==expected
                checks.append(ok)
                if not ok:
                    messages.append(f'Case {i+1} failed. Input: {stdin!r}\nExpected: {expected!r}\nReceived: {runtime[:2000]!r}')
            return dict(passed=all(checks),checks=checks,phase='run',output='\n\n'.join(messages) or 'All input cases passed. Your implementation handles the tested variations.')
        status, runtime = run_process([str(exe)], temp, 5)
        if level['tests']:
            checks = [f'CHECK_{i+1}_OK' in runtime.splitlines() for i in range(len(level['tests']))]
            passed = status==0 and all(checks)
        else:
            passed = status==0 and runtime.replace('\r\n','\n').rstrip('\n')==level['expected']
            checks = [passed]
        readable = '\n'.join(line for line in runtime.splitlines() if not line.startswith('CHECK_'))
        return dict(passed=passed, checks=checks, phase='run', output=readable or ('All checks passed. The path is clear!' if passed else 'The output did not match. Try again.'))

class Handler(BaseHTTPRequestHandler):
    def log_message(self, *_):
        pass

    def respond(self, data, status=200, content_type='application/json', headers=None):
        if not isinstance(data, bytes):
            data = json.dumps(data).encode()
        self.send_response(status)
        self.send_header('Content-Type', content_type)
        self.send_header('Content-Length', str(len(data)))
        self.send_header('Cache-Control', 'no-store')
        self.send_header('X-Content-Type-Options', 'nosniff')
        for name, value in (headers or {}).items():
            self.send_header(name, value)
        self.send_header('Content-Security-Policy', "default-src 'self'; style-src 'self' 'unsafe-inline'; script-src 'self'; img-src 'self' data:; frame-ancestors 'none'")
        self.end_headers()
        self.wfile.write(data)

    def valid_host(self):
        return self.headers.get('Host') in (f'127.0.0.1:{self.server.server_port}', f'localhost:{self.server.server_port}')

    def cookie_name(self):
        return f'rustbound_session_{self.server.server_port}'

    def session(self):
        cookie=SimpleCookie()
        try:
            cookie.load(self.headers.get('Cookie',''))
            token=cookie.get(self.cookie_name())
            if not token: return None
            with connect() as db:
                row=db.execute('SELECT s.*,u.username FROM sessions s JOIN users u ON u.id=s.user_id WHERE s.token_hash=? AND s.expires_at>?',(token_hash(token.value),time.time())).fetchone()
                return dict(row) if row else None
        except CookieError:
            return None

    def authenticate(self, body, register):
        # Limit costly password checks and repeated guesses on this local instance.
        with AUTH_LOCK:
            now=time.time()
            while AUTH_REQUESTS and AUTH_REQUESTS[0]<now-60: AUTH_REQUESTS.popleft()
            if len(AUTH_REQUESTS)>=20:
                return self.respond({'error':'Too many attempts. Please wait a minute and try again.'},429)
            AUTH_REQUESTS.append(now)
        username=body.get('username','')
        password=body.get('password','')
        if not isinstance(username,str) or not re.fullmatch(r'[A-Za-z0-9_]{3,24}',username):
            raise ValueError('Use a username of 3–24 letters, numbers, or underscores.')
        if not isinstance(password,str) or not 8<=len(password)<=128:
            raise ValueError('Use a password with 8–128 characters.')
        imported=False
        if register:
            email,name,hint=account_details(body)
            if body.get('confirm_password')!=password: raise ValueError('Your passwords do not match.')
            if password.casefold() in hint.casefold(): raise ValueError('Do not include your password in the hint question.')
            salt=secrets.token_hex(16)
            digest=password_hash(password,salt)
            try:
                with connect() as db:
                    db.execute('BEGIN IMMEDIATE')
                    first=db.execute('SELECT COUNT(*) FROM users').fetchone()[0]==0
                    user_id=db.execute('INSERT INTO users(username,salt,password_hash,email,display_name,hint_question) VALUES(?,?,?,?,?,?)',(username,salt,digest,email,name,hint)).lastrowid
                    # Preserve the old local expedition for the first account only.
                    if first:
                        imported=db.execute('SELECT COUNT(*) FROM progress').fetchone()[0]>0
                        db.execute('INSERT INTO account_progress SELECT ?,level,code,passed,attempts,completed_at FROM progress',(user_id,))
                        db.execute('INSERT INTO account_attempts(user_id,level,passed,created_at) SELECT ?,level,passed,created_at FROM attempts',(user_id,))
            except sqlite3.IntegrityError:
                return self.respond({'error':'That username or email is already registered. Choose another or sign in.'},409)
        else:
            with connect() as db:
                user=db.execute('SELECT * FROM users WHERE username=?',(username,)).fetchone()
            # Also derive a hash for unknown names, avoiding a fast account-existence check.
            digest=password_hash(password,user['salt'] if user else '00'*16)
            if not user or not secrets.compare_digest(digest,user['password_hash']):
                return self.respond({'error':'Incorrect username or password.'},401)
            user_id=user['id']
        token=secrets.token_urlsafe(32)
        csrf=secrets.token_urlsafe(32)
        old=self.session()
        with connect() as db:
            db.execute('DELETE FROM sessions WHERE expires_at<=?',(time.time(),))
            if old: db.execute('DELETE FROM sessions WHERE token_hash=?',(old['token_hash'],))
            db.execute('INSERT INTO sessions VALUES(?,?,?,?)',(token_hash(token),user_id,csrf,time.time()+SESSION_AGE))
        self.respond({'ok':True,'imported':imported},headers={'Set-Cookie':f'{self.cookie_name()}={token}; Path=/; HttpOnly; SameSite=Strict; Max-Age={SESSION_AGE}'})

    def do_GET(self):
        if not self.valid_host():
            return self.respond({'error':'Invalid host'},403)
        path = urlparse(self.path).path
        session=self.session()
        if path=='/api/session':
            with connect() as db:
                legacy=not db.execute('SELECT 1 FROM users LIMIT 1').fetchone() and bool(db.execute('SELECT 1 FROM progress LIMIT 1').fetchone())
            return self.respond({'user':{'username':session['username']} if session else None,'token':TOKEN,'legacy_available':legacy})
        if path=='/api/mcq':
            if not session: return self.respond({'error':'Please sign in to continue.'},401)
            return self.respond(dict(questions=public_questions(),version=MCQ_VERSION,token=session['csrf'],**mcq_state(session['user_id'])))
        if path=='/api/library':
            if not session: return self.respond({'error':'Please sign in to continue.'},401)
            with connect() as db:
                completed=[dict(r) for r in db.execute('SELECT kind,item,completed_at FROM reading_progress WHERE user_id=?',(session['user_id'],))]
            return self.respond(dict(lessons=LESSONS,modules=MODULES,module_details=MODULE_DETAILS,scenarios=SCENARIOS,reviewed=REVIEWED,completed=completed,token=session['csrf']))
        if path=='/api/state':
            if not session: return self.respond({'error':'Please sign in to continue.'},401)
            return self.respond(state(session['user_id'],session['csrf']))
        if path=='/' and not session:
            return self.respond(b'',302,headers={'Location':'/login'})
        if path=='/login' and session:
            return self.respond(b'',302,headers={'Location':'/'})
        files = {'/':('index.html','text/html; charset=utf-8'), '/login':('login.html','text/html; charset=utf-8'), '/auth.js':('auth.js','text/javascript'), '/theme.js':('theme.js','text/javascript'), '/style.css':('style.css','text/css'), '/game.js':('game.js','text/javascript')}
        files.update({'/library.js':('library.js','text/javascript'), '/library.css':('library.css','text/css'), '/course.css':('course.css','text/css'), '/mcq.js':('mcq.js','text/javascript'), '/practice.css':('practice.css','text/css')})
        files['/topics.css']=('topics.css','text/css')
        if path not in files:
            return self.respond({'error':'Not found'},404)
        name, mime = files[path]
        self.respond((ROOT/'static'/name).read_bytes(), content_type=mime)

    def do_POST(self):
        if not self.valid_host():
            return self.respond({'error':'Refresh the page to reconnect.'},403)
        origin = self.headers.get('Origin')
        if origin and origin not in (f'http://127.0.0.1:{self.server.server_port}', f'http://localhost:{self.server.server_port}'):
            return self.respond({'error':'Invalid origin'},403)
        auth_route=self.path in ('/api/login','/api/register')
        session=self.session()
        if not auth_route and not session:
            return self.respond({'error':'Please sign in to continue.'},401)
        expected=TOKEN if auth_route else session['csrf']
        if not secrets.compare_digest(self.headers.get('X-Rustbound-Token',''),expected):
            return self.respond({'error':'Your session changed. Refresh this page before continuing.'},403)
        try:
            size = int(self.headers.get('Content-Length',0))
            if not 0 < size <= 50000:
                raise ValueError('Request must be 1–50,000 bytes.')
            body = json.loads(self.rfile.read(size))
            if not isinstance(body,dict): raise ValueError('Expected a JSON object.')
            if auth_route:
                return self.authenticate(body,self.path=='/api/register')
            user_id=session['user_id']
            if self.path=='/api/mcq/answer':
                if body.get('version')!=MCQ_VERSION:
                    return self.respond({'error':'The question bank changed. Reload before answering.'},409)
                question=next((q for q in QUESTIONS if q['id']==body.get('question')),None)
                choice=body.get('choice')
                if question is None or type(choice) is not int or not 0<=choice<len(question['options']):
                    raise ValueError('Choose a valid question and one answer option.')
                correct=int(choice==question['answer'])
                with connect() as db:
                    db.execute('INSERT INTO mcq_attempts(user_id,version,question,choice,correct) VALUES(?,?,?,?,?)',(user_id,MCQ_VERSION,question['id'],choice,correct))
                return self.respond(dict(correct=bool(correct),answer=question['answer'],explanation=question['explanation'],rationales=question['rationales'],**mcq_state(user_id)))
            if self.path=='/api/reading':
                kind=body.get('kind'); item=body.get('item'); completed=body.get('completed')
                catalog=LESSONS if kind=='lesson' else SCENARIOS if kind=='scenario' else []
                if not isinstance(item,str) or item not in {entry['id'] for entry in catalog} or type(completed) is not bool:
                    raise ValueError('Choose a valid lesson or scenario and completion state.')
                with connect() as db:
                    if completed:
                        db.execute('INSERT OR IGNORE INTO reading_progress(user_id,kind,item) VALUES(?,?,?)',(user_id,kind,item))
                    else:
                        db.execute('DELETE FROM reading_progress WHERE user_id=? AND kind=? AND item=?',(user_id,kind,item))
                return self.respond({'saved':True})
            if self.path=='/api/logout':
                with connect() as db:
                    db.execute('DELETE FROM sessions WHERE token_hash=?',(session['token_hash'],))
                return self.respond({'ok':True},headers={'Set-Cookie':f'{self.cookie_name()}=; Path=/; HttpOnly; SameSite=Strict; Max-Age=0'})
            if self.path=='/api/profile':
                email,name,hint=account_details(body)
                password=body.get('current_password','')
                if not isinstance(password,str) or not 8<=len(password)<=128: raise ValueError('Enter your current password to update account details.')
                with connect() as db:
                    user=db.execute('SELECT salt,password_hash FROM users WHERE id=?',(user_id,)).fetchone()
                    if not secrets.compare_digest(password_hash(password,user['salt']),user['password_hash']):
                        return self.respond({'error':'Current password is incorrect.'},400)
                    if password.casefold() in hint.casefold(): raise ValueError('Do not include your password in the hint question.')
                    try: db.execute('UPDATE users SET email=?,display_name=?,hint_question=? WHERE id=?',(email,name,hint,user_id))
                    except sqlite3.IntegrityError: return self.respond({'error':'That email is already registered.'},409)
                return self.respond({'saved':True})
            if body.get('track')!=TRACK:
                return self.respond({'error':'The question set has changed. Reload the page before saving or running code.'},409)
            number = body.get('level')
            if type(number)!=int or not 1<=number<=len(LEVELS):
                raise ValueError('Unknown level.')
            level = LEVELS[number-1]
            with connect() as db:
                if number>1 and not db.execute('SELECT 1 FROM reviewed_progress WHERE user_id=? AND level IN (?,?) AND passed=1',(user_id,number-1,number)).fetchone():
                    return self.respond({'error':'Complete the previous level first.'},403)
            if self.path not in ('/api/save','/api/run'):
                return self.respond({'error':'Not found'},404)
            code = body.get('code')
            if not isinstance(code,str) or len(code)>20000:
                raise ValueError('Code must be text, up to 20,000 characters.')
            with connect() as db:
                db.execute('INSERT INTO reviewed_progress(user_id,level,code) VALUES(?,?,?) ON CONFLICT(user_id,level) DO UPDATE SET code=excluded.code',(user_id,number,code))
            if self.path=='/api/save':
                return self.respond({'saved':True})
            if not RUN_LOCK.acquire(blocking=False):
                return self.respond({'error':'Another challenge is running. Try again shortly.'},409)
            try:
                result = evaluate(level,code)
                with connect() as db:
                    db.execute('UPDATE reviewed_progress SET passed=MAX(passed,?), attempts=attempts+1, completed_at=CASE WHEN ?=1 AND completed_at IS NULL THEN CURRENT_TIMESTAMP ELSE completed_at END WHERE user_id=? AND level=?',(int(result['passed']),int(result['passed']),user_id,number))
                    db.execute('INSERT INTO reviewed_attempts(user_id,level,passed) VALUES(?,?,?)',(user_id,number,int(result['passed'])))
                self.respond(result)
            finally:
                RUN_LOCK.release()
        except (ValueError,TypeError,json.JSONDecodeError) as e:
            self.respond({'error':str(e)},400)
        except Exception:
            self.respond({'error':'The local runner encountered an error. Check that Rust and its linker are installed.'},500)

def make_server(port=8765):
    init_db()
    return ThreadingHTTPServer(('127.0.0.1', port), Handler)

if __name__=='__main__':
    import argparse
    parser=argparse.ArgumentParser(description='Rustbound local learning server')
    parser.add_argument('--port',type=int,default=8765)
    args=parser.parse_args()
    server=make_server(args.port)
    print(f'Rustbound: http://127.0.0.1:{server.server_port}', flush=True)
    print('Local personal-use runner: submitted Rust runs with your user permissions. Only run code you trust.', flush=True)
    try: server.serve_forever()
    except KeyboardInterrupt: pass
    finally: server.server_close()
