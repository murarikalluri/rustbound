'use strict';
const $ = id => document.getElementById(id);
let data, current = 1, busy = false, saveTimer, toastTimer, signingOut=false, hintIndex=0;
const escapeHTML = s => String(s).replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const regionStories = [
 ['THE QUIET SHORE', 'The shore is quiet. An old beacon could guide you home — if you can bring it back to life.', 'A new world is waiting for your first line of code.', 'Light the beacon'],
 ['THE BORROWED WOODS', 'The forest shares its secrets with careful explorers. Repair the crossing without losing what you carry.', 'Borrow wisely. Leave the forest better than you found it.', 'Restore the forest path'],
 ['CLOCKWORK CANYON', 'Beyond the canyon, ancient machinery waits for someone who speaks its language. Give the gears a purpose.', 'One elegant solution can set a whole world in motion.', 'Power the machinery'],
 ['THE HIGH SUMMIT', 'The last ascent calls for everything you have learned. Synchronize the observatory and send a signal to the stars.', 'The summit is close. Make every line count.', 'Activate the observatory']
];
function toast(message) { $('toast').textContent=message; $('toast').hidden=false; clearTimeout(toastTimer); toastTimer=setTimeout(()=>$('toast').hidden=true,3500); }
async function api(path, body) {
 const response = await fetch('/api/'+path, {method:'POST',headers:{'Content-Type':'application/json','X-Rustbound-Token':data.token},body:JSON.stringify({...body,track:data.track})});
 const result = await response.json(); if(response.status===401){data=null;window.location.replace('/login');throw new Error('Please sign in again.');} if (!response.ok) throw new Error(result.error || 'Request failed'); return result;
}
async function fetchState() { const r=await fetch('/api/state'); if(r.status===401){data=null;window.location.replace('/login');throw new Error('Please sign in again.');}if(!r.ok) throw new Error('Cannot connect to the local server.'); const next=await r.json();if(data && data.user.id!==next.user.id){data=null;window.location.reload();throw new Error('Your account changed. Reloading.');}data=next; }
function isPassed(id) { return !!data.progress[id]?.passed; }
function unlocked(id) { return id===1 || isPassed(id) || isPassed(id-1); }
function updateStats() {
 const passed=data.levels.filter(l=>isPassed(l.id));
 $('track-notice').hidden=!data.archived_completed;
 $('track-notice').textContent=`Your ${data.archived_completed} original exercise completions are archived. Existing interview achievements are mapped into this 100-question course.`;
 $('user-name').textContent=data.user.display_name||data.user.username;$('user-avatar').textContent=data.user.username[0].toUpperCase();
 $('xp').textContent=passed.reduce((sum,l)=>sum+l.xp,0).toLocaleString();
 $('rank').textContent=passed.length===data.levels.length?'Summit explorer':passed.length>=18?'Rust adventurer':passed.length>=9?'Trail finder':'Rust apprentice';
 const region=data.levels[current-1].region;
 const regionDone=passed.filter(l=>l.region===region).length;const regionTotal=data.levels.filter(l=>l.region===region).length;
 $('side-region').textContent=data.regions[region][0];
 document.querySelector('.region-icon').textContent=data.regions[region][2];
 $('side-sub').textContent=data.regions[region][1];
 $('side-progress').style.width=`${regionDone/regionTotal*100}%`;
 $('side-count').textContent=`${regionDone} of ${regionTotal} questions complete`;
 $('breadcrumb').textContent=data.regions[region][0];
 $('region-strip').innerHTML=data.regions.map((r,i)=>`<button class="region-card ${i===region?'current':''}" data-region="${i}"><span class="region-emoji">${r[2]}</span><div><strong>${r[0]}</strong><small>${r[1]} · ${data.levels.filter(l=>l.region===i).length} questions</small></div><span class="region-mark">${i===region?'◉':unlocked(data.levels.find(l=>l.region===i).id)?'◇':'⌑'}</span></button>`).join('');
 document.querySelectorAll('[data-region]').forEach(b=>b.onclick=()=>{showView('map');document.getElementById('region-'+b.dataset.region)?.scrollIntoView({behavior:'smooth',block:'start'});});
 $('total-progress').textContent=`${passed.length} / ${data.levels.length} completed`;
 renderMap();renderJournal();renderProgress();populateProfile();
}
function showView(view) {
 if (busy) return toast('Your code is still running.');
 for(const name of ['play','map','progress','learn','production','mcq']) $(name+'-view').hidden=name!==view;
 $('region-strip').hidden=!['play','map'].includes(view);
 document.dispatchEvent(new CustomEvent('rustbound:view',{detail:view}));
 document.querySelectorAll('[data-view]').forEach(b=>b.classList.toggle('active',b.dataset.view===view));
}
function tree(x,y,s=1,color='#608c73') { return `<g transform="translate(${x},${y}) scale(${s})"><path d="M-3 0h6v-27h-6" fill="#554c3c"/><path d="M0-90L-27-30H27Z" fill="${color}"/><path d="M0-70L-32-12H32Z" fill="${color}"/><path d="M0-90V-12H32L18-38H27Z" fill="#173f3d" opacity=".3"/></g>`; }
function scene(region) {
 const palettes=[['#89aa79','#5a8066','#375348'],['#6d9b82','#456b5b','#294e45'],['#b69870','#8f7152','#574d43'],['#a4bbba','#6d8e92','#455b67']];
 region=region%4; const [top,side,rock]=palettes[region];
 const feature=region===1?'<g><path d="M271 125l-19 17 30 20-14 23 42 31" fill="none" stroke="#5d9f9f" stroke-width="16"/><g class="restored-bridge" stroke="#e4c79a" stroke-width="5"><path d="M251 163l45 14M254 157l45 14M257 151l45 14M260 145l45 14"/></g></g>':region===2?'<g transform="translate(307 157)"><g class="gear"><circle r="23" fill="#617671" stroke="#d7b984" stroke-width="8" stroke-dasharray="8 5"/><circle r="8" fill="#d7b984"/><path d="M0-15v30M-15 0h30" stroke="#d7b984" stroke-width="4"/></g></g>':region===3?'<g class="satellite" transform="translate(310 79)"><circle r="7" fill="#e4c494"/><path d="M-8-5h-20v10h20M8-5h20v10H8" fill="#8aafbf" stroke="#c3d7d8"/><path d="M0 8v9" stroke="#e4c494"/></g>':'';
 const trees = region<2 ? tree(153,146,.62)+tree(200,120,.8)+tree(443,176,.8)+tree(479,197,.5)+tree(128,173,.45) : region===2 ? '<g fill="#cda77c"><path d="M153 153v-60l22-13 22 13v60l-22 12z"/><path d="M444 187v-42l18-9 18 9v42l-18 10z"/></g>' : '<g fill="#d0dfd8"><path d="M117 152l50-95 52 96-52 22z"/><path d="M404 156l40-82 45 91-45 18z"/></g>';
 $('scene').innerHTML=`<svg viewBox="0 0 620 280" role="img" aria-label="An isometric island with a robot explorer, a winding path, and a robot that walks along the trail when your code passes"><defs><linearGradient id="sky" x2="0" y2="1"><stop stop-color="#a6e88d" stop-opacity=".65"/><stop offset="1" stop-color="#a6e88d" stop-opacity="0"/></linearGradient><radialGradient id="halo"><stop stop-color="#e1ff94" stop-opacity=".8"/><stop offset="1" stop-color="#e1ff94" stop-opacity="0"/></radialGradient></defs>
 <g class="stars" fill="#9ccab5"><circle cx="96" cy="75" r="1.5"/><circle cx="525" cy="97" r="1"/><circle cx="310" cy="42" r="1"/><path d="M512 55v8m-4-4h8M72 135v6m-3-3h6" stroke="#93c1ab" opacity=".5"/></g>
 <ellipse cx="314" cy="251" rx="177" ry="15" fill="#0b2228" opacity=".5"/>
 <g class="floating"><path d="M92 172L271 95l258 81-191 80z" fill="${rock}"/><path d="M92 172v32l246 65v-33z" fill="${side}"/><path d="M338 236l191-60v30l-191 63z" fill="${rock}"/><path d="M92 172l188-84 249 88-191 81z" fill="${top}"/>
 <path d="M101 177l237 67 182-66" fill="none" stroke="#bbcf8f" stroke-opacity=".3" stroke-width="5"/><path d="M156 183l68-29 93 31 87-39" fill="none" stroke="#ccd2a7" stroke-width="19" stroke-linecap="round"/><path d="M156 183l68-29 93 31 87-39" fill="none" stroke="#7e8b69" stroke-width="1" stroke-dasharray="3 12"/>
 <g fill="#527359" opacity=".6"><ellipse cx="245" cy="218" rx="9" ry="3"/><ellipse cx="377" cy="216" rx="14" ry="4"/><ellipse cx="462" cy="174" rx="8" ry="3"/></g>${trees}
 <g class="beacon-glow"><path d="M370 114L332 16h124l-39 98z" fill="url(#sky)"/><ellipse cx="395" cy="116" rx="68" ry="49" fill="url(#halo)"/></g>
 <g transform="translate(390 144)"><ellipse cy="16" rx="39" ry="12" fill="#35564d" opacity=".4"/><path d="M-28 8L0-6 28 8 0 23z" fill="#d0d3b4"/><path d="M-18 5v-39l18-9 18 9V5L0 14z" fill="#bcc5a7"/><path d="M0-43l18 9V5L0 14z" fill="#889e89"/><path d="M-23-34l23-12 23 12L0-22z" fill="#d6d8bc"/><path d="M-13-35v-26l13-7 13 7v26l-13 7z" fill="#40594e"/><path class="beacon-light" d="M-9-39v-19l9-4 9 4v19l-9 5z" fill="#a5ad73"/><path d="M-19-62l19-20 19 20L0-53z" fill="#e4a57f"/><path d="M0-82v29l19-9z" fill="#bd785c"/><path d="M0-80v-12" stroke="#d7c5a2" stroke-width="3"/></g>
 ${feature}<g id="walker" transform="translate(156 183)"><g class="explorer"><ellipse cy="15" rx="16" ry="5" fill="#3b5b48" opacity=".6"/><path class="leg leg-left" d="M-7 3v12" stroke="#233e3d" stroke-width="5" stroke-linecap="round"/><path class="leg leg-right" d="M7 3v12" stroke="#233e3d" stroke-width="5" stroke-linecap="round"/><rect x="-12" y="-21" width="25" height="27" rx="8" fill="#eaa67c"/><path d="M-10-6l-8 7m29-9l7 8" stroke="#d48a65" stroke-width="5" stroke-linecap="round"/><rect x="-9" y="-18" width="19" height="12" rx="5" fill="#25423f"/><g fill="#cfecae"><circle cx="-4" cy="-12" r="2"/><circle cx="5" cy="-12" r="2"/></g><path d="M0-22v-7" stroke="#c8c39c" stroke-width="2"/><circle cy="-30" r="3" fill="#d1eaa8"/></g></g>
 <g transform="translate(310 213)"><path d="M0 0v-29" stroke="#576d51" stroke-width="3"/><path d="M1-28l19 6-19 8z" fill="#e4ad7f"/></g>
 <g stroke="#456f52" stroke-width="2"><path d="M181 202v-8m0 7l-5-5m5 5l5-6M361 226v-7m0 4l5-4"/></g><g fill="#e3d49b"><circle cx="180" cy="191" r="2"/><circle cx="365" cy="217" r="2"/></g>
 </g></svg>`;
}
function selectLevel(id) {
 if(busy) return;
 if(!unlocked(id)) return toast('Complete the previous problem to unlock this path.');
 if(saveTimer){clearTimeout(saveTimer);saveDraft(current,data.progress[current].code);saveTimer=null;}
 current=id;
 const level=data.levels[id-1],story=regionStories[level.region%4];
 $('mission-number').textContent=`QUESTION ${String(id).padStart(2,'0')} / ${data.levels.length}`;
 $('mission-title').textContent=level.title;
 $('difficulty').textContent=`● ${level.difficulty} · +${level.xp} XP`;
 $('quest-title').textContent=level.mode==='program'?'Build a complete program':'Think it through';$('story').textContent=level.mode==='program'?(level.test_count>1?'The runner supplies several stdin inputs to the same compiled program. Handle the general case.':'Write your first complete Rust program inside main.'):'Read the contract, plan your approach, then implement and test it.';$('objective').textContent=level.mode==='program'?(level.test_count>1?'Read stdin, apply the rules, and handle boundary cases. A sample-only printout will not pass.':'Print the exact greeting to verify your Rust setup. This is the only fixed-output warm-up.'):'Handle the examples and edge cases. Keep the supplied signatures and explain your choices.';$('lesson').textContent=level.lesson;
 $('problem-topic').textContent=level.topic;$('problem-task').textContent=level.task;
 $('problem-constraints').innerHTML=level.constraints.map(c=>`<li>${escapeHTML(c)}</li>`).join('');
 $('problem-examples').innerHTML=level.examples.map(([input,output],i)=>`<div class="example-case"><span>EXAMPLE ${i+1}</span><pre>${escapeHTML(input)}</pre><small>Expected</small><pre>${escapeHTML(output)}</pre></div>`).join('');
 $('problem-followup').textContent=level.follow_up;
 document.querySelector('.interview-followup').open=false;
 hintIndex=0;renderHint();
 $('reward-xp').textContent=level.xp+' XP';$('scene-location').textContent=data.regions[level.region][0].toUpperCase();
 $('editor').value=data.progress[id]?.code ?? level.starter;
 $('save-status').textContent='Saved locally';
 $('output').textContent=isPassed(id)?'You completed this problem. Try another approach or continue exploring.':'Ready to compile. Write your solution, then run the code.';
 $('check-count').textContent=`${level.test_count} check${level.test_count>1?'s':''} to pass`;
 $('test-results').innerHTML='';document.querySelector('.console').className='console';
 scene(level.region);setWon(isPassed(id));lineNumbers();setTab('lesson');updateStats();showView('play');
}
function setWon(won,animate=false) {
 const world=document.querySelector('.world');world.classList.remove('walking');world.classList.toggle('won',won);
 if(won&&animate){void world.offsetWidth;world.classList.add('walking');}
 $('success-panel').hidden=!won;
 $('scene-status').textContent=won?'PATH COMPLETED':'READY FOR YOUR CODE';
 $('scene-message').textContent=won?'Your explorer made it across! Continue to the next challenge.':'Every completed question moves your explorer along the trail.';
 $('next').textContent=current===data.levels.length?'View completed expedition →':'Next question →';
}
function lineNumbers() { $('line-numbers').textContent=Array.from({length:$('editor').value.split('\n').length},(_,i)=>i+1).join('\n'); }
function setTab(tab) { $('lesson-content').hidden=tab!=='lesson';$('hint-content').hidden=tab!=='hint';$('lesson-tab').classList.toggle('selected',tab==='lesson');$('hint-tab').classList.toggle('selected',tab==='hint'); }
function renderHint(){const hints=data.levels[current-1].hints;$('hint-text').textContent=hints[hintIndex];$('hint-counter').textContent=`Hint ${hintIndex+1} of ${hints.length}`;$('next-hint').disabled=hintIndex>=hints.length-1;}
async function saveDraft(id,code) {
 try { await api('save',{level:id,code});if(current===id && $('editor').value===code) $('save-status').textContent='Saved locally'; }
 catch(e){if(current===id)$('save-status').textContent='Not saved';toast(e.message);}
}
function edited() {
 lineNumbers(); const id=current,code=$('editor').value;
 data.progress[id]={...(data.progress[id]||{}),code};
 $('save-status').textContent='Saving…'; clearTimeout(saveTimer);
 saveTimer=setTimeout(()=>{saveTimer=null;saveDraft(id,code);},450);
}
async function runCode() {
 if(busy)return;
 busy=true;clearTimeout(saveTimer);saveTimer=null;$('run').disabled=true;$('editor').readOnly=true;$('reset').disabled=true;
 $('run').textContent='◌ Compiling…';$('output').textContent='Compiling your Rust code, then running the mission checks…';
 document.querySelector('.world').classList.add('running');
 try {
  const result=await api('run',{level:current,code:$('editor').value});
  $('output').textContent=result.output;
  $('check-count').textContent=result.passed?'All checks passed':result.phase==='compile'?'Compiler feedback':'Try again — you’ve got this';
  document.querySelector('.console').className='console '+(result.passed?'passed':'failed');
  $('test-results').innerHTML=result.checks.map((ok,i)=>`<span class="${ok?'':'fail'}">${ok?'✓':'×'} Check ${i+1}</span>`).join('');
  const already=isPassed(current);
  await fetchState();updateStats();setWon(result.passed || isPassed(current),result.passed);
  $('save-status').textContent='Saved locally';
  if(result.passed)toast(already?'Problem solved again. Nicely done!':`Path unlocked! +${data.levels[current-1].xp} XP`);
 } catch(e) { $('output').textContent=e.message;document.querySelector('.console').className='console failed'; }
 finally {busy=false;$('run').disabled=false;$('editor').readOnly=false;$('reset').disabled=false;$('run').textContent='▶ Run code';document.querySelector('.world').classList.remove('running');}
}
function renderMap() {
 $('map-regions').innerHTML=data.regions.map((r,i)=>`<section class="map-region" id="region-${i}"><h3>${r[2]} ${r[0]} <small>${r[1]}</small></h3><div class="mission-grid">${data.levels.filter(l=>l.region===i).map(l=>`<button class="map-mission ${isPassed(l.id)?'done':!unlocked(l.id)?'locked':''}" data-level="${l.id}" aria-label="${escapeHTML(l.title)}${unlocked(l.id)?'':', locked'}"><span class="mission-num">${isPassed(l.id)?'✓':String(l.id).padStart(2,'0')}</span><span><strong>${escapeHTML(l.title)}</strong><small>${isPassed(l.id)?'Completed':unlocked(l.id)?'Ready to explore':'Solve question '+(l.id-1)} · ${l.xp} XP</small></span></button>`).join('')}</div></section>`).join('');
 document.querySelectorAll('[data-level]').forEach(b=>b.onclick=()=>selectLevel(Number(b.dataset.level)));
}
function renderJournal() {
 const done=data.levels.filter(l=>isPassed(l.id));
 $('journal').innerHTML=done.length?done.map(l=>`<article class="journal-entry"><div class="eyebrow">QUESTION ${String(l.id).padStart(2,'0')} · COMPLETED</div><h3>${escapeHTML(l.title)}</h3><p>${escapeHTML(l.lesson)}</p><button class="subtle" data-revisit="${l.id}">Revisit problem ↗</button></article>`).join(''):'<article class="journal-entry"><div class="quest-icon">▤</div><h3>Your story starts here.</h3><p>Complete your first problem to add a page to your journal. Your progress and code are saved automatically.</p><button class="subtle" data-revisit="1">Start the first problem →</button></article>';
 document.querySelectorAll('[data-revisit]').forEach(b=>b.onclick=()=>selectLevel(Number(b.dataset.revisit)));
}
function renderProgress(){
 const passed=data.levels.filter(l=>isPassed(l.id));
 $('progress-title').textContent=`${data.user.username}’s expedition`;
 $('stat-completed').textContent=`${passed.length} / ${data.levels.length}`;
 $('stat-xp').textContent=passed.reduce((sum,l)=>sum+l.xp,0).toLocaleString();
 $('stat-attempts').textContent=Object.values(data.progress).reduce((sum,p)=>sum+(p.attempts||0),0).toLocaleString();
 $('stat-percent').textContent=Math.round(passed.length/data.levels.length*100)+'%';
 $('stat-rank').textContent=$('rank').textContent;
 $('personal-regions').innerHTML=data.regions.map((r,i)=>{const levels=data.levels.filter(l=>l.region===i),count=levels.filter(l=>isPassed(l.id)).length;return `<div class="personal-region"><div><span>${r[2]} ${escapeHTML(r[0])}</span><small>${count} / ${levels.length}</small></div><progress value="${count}" max="${levels.length}" aria-label="${escapeHTML(r[0])} progress"></progress></div>`;}).join('');
 $('personal-activity').innerHTML=data.activity.length?data.activity.map(a=>`<div class="activity-item"><span class="activity-icon ${a.passed?'':'retry'}">${a.passed?'✓':'↻'}</span><div><strong>${escapeHTML(data.levels[a.level-1]?.title||'Mission')}</strong><small>${a.passed?'Passed':'Practiced'} · ${escapeHTML(new Date(a.created_at.replace(' ','T')+'Z').toLocaleString(undefined,{month:'short',day:'numeric',hour:'2-digit',minute:'2-digit'}))}</small></div></div>`).join(''):'<p class="muted">Your story is just beginning. Run your first problem to see your activity here.</p>';
}
document.querySelectorAll('[data-view]').forEach(b=>b.onclick=()=>showView(b.dataset.view));
$('map-shortcut').onclick=()=>showView('map');
$('lesson-tab').onclick=()=>setTab('lesson');$('hint-tab').onclick=()=>setTab('hint');
$('next-hint').onclick=()=>{hintIndex=Math.min(hintIndex+1,data.levels[current-1].hints.length-1);renderHint();};
$('editor').addEventListener('input',edited);
$('editor').addEventListener('scroll',()=>{$('line-numbers').scrollTop=$('editor').scrollTop;});
$('editor').addEventListener('keydown',e=>{if(e.key==='Tab'){e.preventDefault();const t=e.target,start=t.selectionStart,end=t.selectionEnd;t.setRangeText('    ',start,end,'end');edited();}if((e.ctrlKey||e.metaKey)&&e.key==='Enter'){e.preventDefault();runCode();}});
$('run').onclick=runCode;
$('reset').onclick=()=>{if(confirm('Restore this problem’s starter code? Your current draft will be replaced.')){$('editor').value=data.levels[current-1].starter;edited();}};
$('next').onclick=()=>{if(current===data.levels.length){showView('map');toast('Expedition complete! All 100 questions solved.');}else selectLevel(current+1);};
$('resume').onclick=()=>selectLevel(data.levels.find(l=>!isPassed(l.id))?.id||data.levels.length);
$('logout').onclick=async()=>{if(busy)return toast('Wait for your code to finish, then sign out.');if(signingOut)return;signingOut=true;$('logout').disabled=true;$('editor').readOnly=true;$('run').disabled=true;clearTimeout(saveTimer);saveTimer=null;try{await api('save',{level:current,code:$('editor').value});await api('logout',{});data=null;window.location.replace('/login');}catch(e){toast(e.message);signingOut=false;$('logout').disabled=false;$('editor').readOnly=false;$('run').disabled=false;}};
window.addEventListener('beforeunload',()=>{if(data && !signingOut){fetch('/api/save',{method:'POST',headers:{'Content-Type':'application/json','X-Rustbound-Token':data.token},body:JSON.stringify({level:current,code:$('editor').value,track:data.track}),keepalive:true}).catch(()=>{});}});
(async()=>{try{await fetchState();selectLevel(data.levels.find(l=>!isPassed(l.id))?.id||data.levels.length);if(!data.compiler){$('connection').hidden=false;$('connection').textContent='Rust compiler not found. Install Rust from rustup.rs and restart the launcher to run challenges.';}}catch(e){$('connection').hidden=false;$('connection').textContent='Unable to connect. Start launcher.py or app.py, then reload this page.';$('run').disabled=true;}})();

function progressTab(name){for(const tab of ['overview','journal','account']){$(tab+'-pane').hidden=tab!==name;$(tab+'-tab').setAttribute('aria-selected',String(tab===name));$(tab+'-tab').tabIndex=tab===name?0:-1;}}
for(const name of ['overview','journal','account'])$(name+'-tab').onclick=()=>progressTab(name);
function populateProfile(){if(document.activeElement?.closest('#profile-form'))return;$('profile-email').value=data.user.email||'';$('profile-name').value=data.user.display_name||'';$('profile-hint').value=data.user.hint_question||'';$('profile-note').textContent=data.user.email?'Email OTP recovery is on hold. Your hint is a private reminder, not a reset method.':'Add an email and a hint question to complete your existing account. OTP recovery is currently on hold.';}
$('profile-form').onsubmit=async e=>{e.preventDefault();$('profile-save').disabled=true;try{await api('profile',{email:$('profile-email').value,display_name:$('profile-name').value,hint_question:$('profile-hint').value,current_password:$('profile-password').value});$('profile-password').value='';await fetchState();updateStats();$('profile-status').textContent='Account details saved.';}catch(e){$('profile-status').textContent=e.message;}finally{$('profile-save').disabled=false;}};

progressTab('overview');
document.querySelector('.progress-tabs').addEventListener('keydown',e=>{const tabs=['overview','journal','account'];const current=tabs.findIndex(n=>$(n+'-tab')===document.activeElement);if(current<0)return;let next;if(e.key==='ArrowRight')next=(current+1)%3;else if(e.key==='ArrowLeft')next=(current+2)%3;else if(e.key==='Home')next=0;else if(e.key==='End')next=2;else return;e.preventDefault();progressTab(tabs[next]);$(tabs[next]+'-tab').focus();});
