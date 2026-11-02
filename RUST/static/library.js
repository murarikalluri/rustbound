'use strict';
(() => {
 const el=id=>document.getElementById(id);
 const safe=s=>String(s).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
 let library=null, loading=null;
 const state={learn:{query:'',filter:'',selected:null,overview:true},production:{query:'',filter:'',selected:null}};
 const kind=view=>view==='learn'?'lesson':'scenario';
 const catalog=view=>view==='learn'?library.lessons:library.scenarios;
 const done=(view,id)=>library.completed.some(r=>r.kind===kind(view)&&r.item===id);
 const block=(title,text)=>`<section class="reading-block"><h3>${title}</h3><p>${safe(text)}</p></section>`;
 async function load() {
  if(library)return library;
  if(!loading) loading=(async()=>{
   const response=await fetch('/api/library');
   if(response.status===401){window.location.replace('/login');throw Error('Please sign in again.');}
   if(!response.ok)throw Error('Could not load the library. Try again.');
   library=await response.json(); summary(); return library;
  })().finally(()=>loading=null);
  return loading;
 }
 function summary(){
  const lessons=library.completed.filter(r=>r.kind==='lesson').length;
  const cases=library.completed.filter(r=>r.kind==='scenario').length;
  el('reading-summary').innerHTML=`<div class="reading-summary"><div><span class="eyebrow">YOUR LEARNING LIBRARY</span><h3>${lessons} / ${library.lessons.length} lessons · ${cases} / ${library.scenarios.length} case studies</h3><p>Reading progress is saved to your account, separately from coding XP. Completion is your self-assessment.</p></div><div><button class="subtle" id="continue-reading">Continue reading →</button><button class="subtle" id="continue-cases">Open production lab →</button></div></div>`;
  el('continue-reading').onclick=()=>{state.learn.selected=library.lessons.find(l=>!done('learn',l.id))?.id||library.lessons[0].id;state.learn.overview=false;showView('learn');};
  el('continue-cases').onclick=()=>showView('production');
 }
 async function open(view){
  if(!['learn','production','progress'].includes(view))return;
  const host=view==='progress'?el('reading-summary'):el(view+'-view');
  try {await load();if(view==='progress'){summary();return;}render(view);}
  catch(error){host.innerHTML=`<p role="alert">${safe(error.message)}</p><button class="subtle" type="button">Retry loading</button>`;host.querySelector('button').onclick=()=>open(view);}
 }
 function render(view){
  const isLearn=view==='learn', s=state[view], items=catalog(view);
  if(isLearn&&s.overview){courseHome();return;}
  const filters=isLearn?library.modules:[...new Set(items.map(x=>x.category))];
  el(view+'-view').innerHTML=`<div class="library-banner ${isLearn?'':'case-banner'}"><div><span class="eyebrow">${isLearn?'THE LEARNING PATH':'THE PRODUCTION LAB'}</span><h2>${isLearn?'From your first line to systems thinking.':'Debug the problem. Defend the decision.'}</h2><p>${isLearn?`${items.length} lessons across ${library.modules.length} modules. Read in order or revisit any topic; every lesson is unlocked.`:`${items.length} curated cases, including documented advisories and clearly labeled practice scenarios. Sources reviewed ${library.reviewed}.`}</p></div><div class="library-number">${items.filter(x=>done(view,x.id)).length}<small>of ${items.length} read</small></div></div>
   ${!isLearn?'<p class="library-note">Work the incident before opening the debrief. All incident stories, timelines, and metrics are fictional teaching simulations. Advisory-backed cases link the real underlying issue; this is a dated collection, not a live incident feed.</p>':''}
   ${isLearn?'<button class="subtle" id="course-back">← All learning modules</button>':''}
   <div class="library-tools"><label>Search ${isLearn?'lessons':'cases'}<input id="${view}-search" type="search" placeholder="${isLearn?'Try ownership, async, or testing':'Try memory, timeout, or security'}" value="${safe(s.query)}"></label><label>${isLearn?'Module':'Category'}<select id="${view}-filter"><option value="">All ${isLearn?'modules':'categories'}</option>${filters.map(f=>`<option ${s.filter===f?'selected':''} value="${safe(f)}">${safe(f)}</option>`).join('')}</select></label></div>
   <div class="library-layout"><nav class="library-list" id="${view}-list" aria-label="${isLearn?'Lessons':'Case studies'}"></nav><article class="reader" id="${view}-reader" aria-label="${isLearn?'Lesson':'Case study'} reader"></article></div>`;
  el(view+'-search').oninput=e=>{s.query=e.target.value;list(view);};
  el(view+'-filter').onchange=e=>{s.filter=e.target.value;list(view);};
  if(isLearn)el('course-back').onclick=()=>{s.overview=true;courseHome();};
  if(!s.selected)s.selected=items[0].id;
  list(view);reader(view);
 }
 function enterLesson(id){
  const item=library.lessons.find(x=>x.id===id);
  state.learn.selected=id;state.learn.overview=false;state.learn.query='';state.learn.filter=item.module;
  render('learn');el('learn-reader').querySelector('h2').focus();
 }
 function courseHome(){
  const completed=library.lessons.filter(x=>done('learn',x.id)).length;
  const next=library.lessons.find(x=>!done('learn',x.id))||library.lessons[0];
  const groups=[...new Set(library.lessons.map(x=>x.group))];
  el('learn-view').innerHTML=`<div class="library-banner course-banner"><div><span class="eyebrow">LEARN RUST · ONE TOPIC AT A TIME</span><h2>Small lessons.<br>Clear explanations.</h2><p>${library.lessons.length} individual topic modules. Each follows the same five steps: understand it, see where it is used, read the syntax, follow an example, and try one small lab.</p><button class="primary" id="course-resume">${completed?'Continue':'Start'} learning →</button></div><div class="library-number">${completed}<small>of ${library.lessons.length} completed</small></div></div><p class="library-note">Start with the simple explanation. Open “A closer look” when you want the professional detail. Young learners can work through examples with a helper; advanced topics build on earlier ideas. The Rust Book guides the learning order, with additional practical topics at the end.</p><p class="reading-source"><a href="https://doc.rust-lang.org/book/" target="_blank" rel="noopener noreferrer">Official Rust Book ↗</a><a href="https://doc.rust-lang.org/reference/" target="_blank" rel="noopener noreferrer">Rust Reference ↗</a></p><div class="library-tools"><label>Find a topic<input id="course-search" type="search" placeholder="Variables, match, Ok, Err…"></label><label>Learning area<select id="course-group"><option value="">All areas</option>${groups.map(g=>`<option value="${safe(g)}">${safe(g)}</option>`).join('')}</select></label></div><p class="library-result" id="course-result-count" role="status"></p><div id="course-search-results" hidden></div><div class="course-module-grid" id="topic-grid"></div><p class="library-note">This curriculum covers core Rust, practical tooling, and selected advanced subjects. It is not an exhaustive catalog of every external crate or unstable language feature.</p>`;
  el('course-resume').onclick=()=>enterLesson(next.id);
  const cards=()=>{
   const query=el('course-search').value.trim().toLowerCase(),group=el('course-group').value;
   const matches=library.lessons.filter(x=>(!group||x.group===group)&&(!query||[x.title,x.simple,x.group].join(' ').toLowerCase().includes(query)));
   el('course-result-count').textContent=`${matches.length} topics`;
   el('topic-grid').innerHTML=matches.map(item=>`<article class="course-module"><div class="module-topline"><span class="eyebrow">TOPIC ${item.day}</span><span>${done('learn',item.id)?'✓ Completed':'Ready to learn'}</span></div><h3>${safe(item.title)}</h3><p>${safe(item.simple)}</p><p class="module-prereq">${safe(item.group)}</p><button class="subtle" data-course-lesson="${item.id}" data-course-module="${item.day-1}">${done('learn',item.id)?'Review':'Learn this topic'} →</button></article>`).join('')||(query?'<p>No matching topics. Try a shorter phrase.</p>':'<p>No topics in this area.</p>');
   el('topic-grid').querySelectorAll('[data-course-lesson]').forEach(b=>b.onclick=()=>enterLesson(b.dataset.courseLesson));
  };
  el('course-search').oninput=cards;el('course-group').onchange=cards;cards();
 }
 function list(view){
  const s=state[view];const items=catalog(view).filter(x=>(!s.filter||(x.module||x.category)===s.filter)&&JSON.stringify(x).toLowerCase().includes(s.query.toLowerCase().trim()));
  el(view+'-list').innerHTML=`<p class="library-result" role="status">${items.length} ${view==='learn'?'lessons':'cases'} found</p>`+items.map(x=>`<button class="reading-item ${s.selected===x.id?'selected':''}" data-item="${x.id}" ${s.selected===x.id?'aria-current="page"':''}><span class="reading-category">${safe(x.module||x.category)}</span><strong>${safe(x.title)}</strong><small>${done(view,x.id)?'✓ Completed':safe(x.stage||x.kind)}</small></button>`).join('')+(items.length?'':'<p class="library-empty">No matches. Try another phrase or choose all categories.</p>');
  el(view+'-list').querySelectorAll('[data-item]').forEach(b=>b.onclick=()=>{s.selected=b.dataset.item;list(view);reader(view);el(view+'-reader').querySelector('h2').focus();});
 }
 function reader(view){
  const items=catalog(view),index=items.findIndex(x=>x.id===state[view].selected),item=items[index];
  if(!item)return;
  const isLearn=view==='learn',completed=done(view,item.id);
  const labels={'rust':'Standalone Rust · edition 2024','rust-library':'Rust library · compile with --crate-type lib','rust-dependency':'Rust · external dependency required','shell':'Terminal commands','sql':'SQL sketch','pseudocode':'Design sketch · not executable'};
  const code=(text,label)=>`<p class="library-note">${safe(label)}</p><pre class="reading-code"><code>${safe(text)}</code></pre>`;
  const section=(title,content)=>`<section class="reading-block lesson-part"><h3>${title}</h3>${content}</section>`;
  let body;
  if(isLearn){
   body=section('1. What it is and how it works',`<p>${safe(item.simple)}</p><details class="professional-detail"><summary>A closer look</summary><p>${safe(item.explain)}</p>${item.paragraphs.map(t=>`<p>${safe(t)}</p>`).join('')}</details>`)
    +section('2. Where you use it',`<p>${safe(item.use)}</p>`)
    +section('3. How to write it',code(item.syntax,item.syntax_label))
    +section('4. An example',`<button class="subtle" id="learn-copy">Copy example</button>`+code(item.code,labels[item.language])+`<p>${safe(item.walkthrough)}</p>`)
    +section('5. One simple lab',`<div class="guided-lab"><p>${safe(item.simple_lab)}</p><p class="library-note">Try this in your study project. Labs are self-reviewed, separate from graded coding questions.</p><details class="review-explanation"><summary>Review your understanding</summary><p>${safe(item.review)}</p></details></div>`);
  }else{
   body=`<p class="library-note">${safe(item.simulation)}</p>`
    +section('1. What is happening',`<p>${safe(item.simple)}</p>`)
    +section('2. Where it happens',`<p>${safe(item.context)}</p>`)
    +section('3. Code or evidence to inspect',code(item.syntax,item.syntax_label))
    +section('4. Follow the example',`<ol class="incident-timeline">${item.timeline.map(t=>`<li>${safe(t)}</li>`).join('')}</ol>`)
    +section('5. One simple lab',`<div class="guided-lab"><p>${safe(item.simple_lab)}</p><details class="professional-detail"><summary>Questions to guide you</summary><ul>${item.investigation_questions.map(t=>`<li>${safe(t)}</li>`).join('')}</ul></details></div><details class="incident-debrief"><summary>See the solution and how to check it</summary>${block('Why it happened',item.cause)+block('How to fix it',item.fix)+block('Check your fix',item.verify)+block('Keep it from happening again',item.prevention)}<details class="professional-detail"><summary>More investigation detail</summary><p>${safe(item.diagnosis)}</p><p>${safe(item.symptom)}</p></details></details>`);
  }
  el(view+'-reader').innerHTML=`<div class="reader-meta"><span>${safe(isLearn?'ONE TOPIC':item.ticket+' · '+item.kind)}</span><span>${index+1} / ${items.length}</span></div><h2 tabindex="-1">${safe(item.title)}</h2>${body}<label class="library-note" for="${view}-reflection">Your notes · not saved</label><textarea class="topic-notes" id="${view}-reflection" placeholder="What did you notice? Explain it in your own words."></textarea><p class="reading-source"><a href="${safe(item.source)}" target="_blank" rel="noopener noreferrer">Supporting documentation ↗</a>${item.book_source?`<a href="${safe(item.book_source)}" target="_blank" rel="noopener noreferrer">Related Rust Book chapter ↗</a>`:''}</p>${isLearn?'':'<button class="subtle" id="related-lesson">Learn the Rust topic behind this issue →</button>'}<div class="reader-actions"><button class="subtle" id="${view}-previous" ${index===0?'disabled':''}>← Previous</button><button class="primary" id="${view}-complete" aria-pressed="${completed}">${completed?'✓ Completed · mark unread':'Mark as completed'}</button><button class="subtle" id="${view}-next" ${index===items.length-1?'disabled':''}>Next →</button></div><p id="${view}-save-status" role="status" class="library-note">Completion is your self-assessment and does not pass a coding challenge.</p>`;
  const navigate=delta=>{state[view].selected=items[index+delta].id;if(isLearn){state.learn.filter=items[index+delta].module;state.learn.query='';el('learn-filter').value=state.learn.filter;el('learn-search').value='';}list(view);reader(view);el(view+'-reader').querySelector('h2').focus();};
  el(view+'-previous').onclick=()=>navigate(-1);el(view+'-next').onclick=()=>navigate(1);
  if(isLearn)el('learn-copy').onclick=async()=>{try{await navigator.clipboard.writeText(item.code);el('learn-copy').textContent='Copied';}catch{el('learn-save-status').textContent='Select the example text to copy it manually.';}};
  else el('related-lesson').onclick=()=>{state.learn.selected=item.lesson;state.learn.overview=false;state.learn.query='';state.learn.filter='';showView('learn');};
  el(view+'-complete').onclick=async()=>{
   const button=el(view+'-complete');button.disabled=true;
   try{
    const response=await fetch('/api/reading',{method:'POST',headers:{'Content-Type':'application/json','X-Rustbound-Token':library.token},body:JSON.stringify({kind:kind(view),item:item.id,completed:!completed})});
    if(response.status===401){window.location.replace('/login');throw Error('Please sign in again.');}
    const result=await response.json();if(!response.ok)throw Error(result.error||'Unable to save progress.');
    library.completed=library.completed.filter(r=>!(r.kind===kind(view)&&r.item===item.id));if(!completed)library.completed.push({kind:kind(view),item:item.id});summary();
    if(view==='learn'&&state.learn.overview){courseHome();return;}
    list(view);const count=el(view+'-view').querySelector('.library-number');if(count)count.innerHTML=`${catalog(view).filter(x=>done(view,x.id)).length}<small>of ${catalog(view).length} read</small>`;
    if(state[view].selected===item.id){const notes=el(view+'-reflection').value,open=el(view+'-reader').querySelector('.incident-debrief')?.open;reader(view);el(view+'-reflection').value=notes;if(!isLearn)el(view+'-reader').querySelector('.incident-debrief').open=!!open;el(view+'-save-status').textContent='Progress saved to your account.';el(view+'-complete').focus();}
   }catch(error){if(el(view+'-save-status'))el(view+'-save-status').textContent=error.message;button.disabled=false;}
  };
 }
 document.addEventListener('rustbound:view',event=>open(event.detail));
 // Load reading counts independently without delaying the coding workspace.
 open('progress');
})();
