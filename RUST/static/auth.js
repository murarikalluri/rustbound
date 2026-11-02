'use strict';
const $=id=>document.getElementById(id);
let mode='login',token='',pending=false;
function setMode(next){
 if(pending)return;
 mode=next;const register=mode==='register';
 $('forgot-panel').hidden=true;$('auth-form').hidden=false;$('forgot-password').hidden=register;
 $('registration-fields').hidden=!register;
 for(const id of ['email','display-name','hint-question']){$(id).disabled=!register;$(id).required=register&&id!=='display-name';}
 $('auth-title').textContent=register?'Your adventure awaits.':'Welcome back.';
 $('auth-subtitle').textContent=register?'Create an account and make this journey yours.':'Sign in and continue your Rust adventure.';
 $('auth-submit').textContent=register?'Create account →':'Sign in →';
 $('confirm-field').hidden=!register;$('confirm-password').required=register;
 $('password').autocomplete=register?'new-password':'current-password';
 for(const m of ['login','register']){ $(m+'-mode').classList.toggle('selected',m===mode);$(m+'-mode').setAttribute('aria-pressed',String(m===mode)); }
 $('auth-error').hidden=true;
}
$('login-mode').onclick=()=>setMode('login');$('register-mode').onclick=()=>setMode('register');
$('toggle-password').onclick=()=>{const show=$('password').type==='password';$('password').type=show?'text':'password';$('toggle-password').textContent=show?'Hide':'Show';$('toggle-password').setAttribute('aria-label',show?'Hide password':'Show password');$('toggle-password').setAttribute('aria-pressed',String(show));};
$('auth-form').addEventListener('submit',async e=>{
 e.preventDefault();if(pending || !token)return;
 $('auth-error').hidden=true;
 if(mode==='register' && $('password').value!==$('confirm-password').value){$('auth-error').textContent='Your passwords do not match.';$('auth-error').hidden=false;return;}
 pending=true;$('auth-submit').disabled=true;$('auth-submit').textContent='Opening your expedition…';
 try{
  const response=await fetch('/api/'+mode,{method:'POST',headers:{'Content-Type':'application/json','X-Rustbound-Token':token},body:JSON.stringify({username:$('username').value,password:$('password').value,confirm_password:$('confirm-password').value,email:$('email').value,display_name:$('display-name').value,hint_question:$('hint-question').value})});
  const result=await response.json();if(!response.ok)throw new Error(result.error||'Unable to sign in. Try again.');
  window.location.replace('/');
 }catch(error){$('auth-error').textContent=error.message;$('auth-error').hidden=false;pending=false;$('auth-submit').disabled=false;$('auth-submit').textContent=mode==='register'?'Create account →':'Sign in →';}
});
(async()=>{try{const response=await fetch('/api/session');if(!response.ok)throw new Error();const info=await response.json();if(info.user){window.location.replace('/');return;}token=info.token;$('legacy-note').hidden=!info.legacy_available;if(info.legacy_available)setMode('register');$('auth-submit').disabled=false;}catch{$('auth-error').textContent='Cannot connect. Check that the Rustbound launcher is running, then reload.';$('auth-error').hidden=false;}})();

$('forgot-password').onclick=()=>{if(pending)return;$('auth-form').hidden=true;$('forgot-panel').hidden=false;$('forgot-password').hidden=true;$('auth-error').hidden=true;$('recovery-email').focus();};
$('back-to-login').onclick=()=>setMode('login');
