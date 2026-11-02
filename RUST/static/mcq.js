'use strict';
(() => {
 const el=id=>document.getElementById(id),escape=s=>String(s).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
 let bank=null,loading=null,selected=null,topic='',mode='all',pending=false;
 const feedback=new Map();
 async function load(){
  if(bank)return bank;
  if(!loading)loading=(async()=>{const r=await fetch('/api/mcq');if(r.status===401){window.location.replace('/login');throw Error('Please sign in again.');}if(!r.ok)throw Error('Could not load MCQ practice.');bank=await r.json();summary();return bank;})().finally(()=>loading=null);
  return loading;
 }
 function summary(){
  if(!bank)return;
  el('mcq-summary').innerHTML=`<span class="eyebrow">MCQ PRACTICE</span><h3>${bank.answered} / ${bank.questions.length} questions attempted</h3><p>${bank.first_correct} correct on first attempt · ${bank.latest_correct} correct on latest attempt · ${bank.total_attempts} total submissions</p><button class="subtle" id="progress-open-mcq">Practise Rust MCQs →</button>`;
  el('progress-open-mcq').onclick=()=>showView('mcq');
 }
 function filtered(){return bank.questions.filter(q=>(!topic||q.topic===topic)&&(mode==='all'||mode==='unanswered'&&!bank.progress[q.id]||mode==='missed'&&bank.progress[q.id]&&!bank.progress[q.id].correct));}
 async function open(){
  try{await load();render();}catch(error){el('mcq-view').innerHTML=`<p role="alert">${escape(error.message)}</p><button class="subtle" id="mcq-reload">Retry</button>`;el('mcq-reload').onclick=open;}
 }
 function render(){
  const items=filtered();if(!selected)selected=items[0]?.id;
  el('mcq-view').innerHTML=`<div class="library-banner quiz-banner"><div><span class="eyebrow">RUST KNOWLEDGE CHECK</span><h2>Choose. Explain. Improve.</h2><p>${bank.questions.length} original questions across ${new Set(bank.questions.map(x=>x.topic)).size} topics. Submit one answer to reveal the reasoning for every option.</p></div><div class="library-number">${bank.first_correct}<small>first-attempt correct / ${bank.answered}</small></div></div><p class="library-note">Practice is untimed. Every submission is saved to your account; retries never change your first-attempt score. MCQs are separate from coding XP and reading completion.</p><div class="library-tools"><label>Topic<select id="mcq-topic"><option value="">All topics</option>${[...new Set(bank.questions.map(x=>x.topic))].map(t=>`<option value="${escape(t)}" ${t===topic?'selected':''}>${escape(t)}</option>`).join('')}</select></label><label>Practice mode<select id="mcq-mode"><option value="all" ${mode==='all'?'selected':''}>All questions</option><option value="unanswered" ${mode==='unanswered'?'selected':''}>Not attempted</option><option value="missed" ${mode==='missed'?'selected':''}>Review missed answers</option></select></label></div><div class="library-layout"><nav class="library-list" id="mcq-list" aria-label="MCQ questions"><p class="library-result">${items.length} matching questions</p>${items.map(q=>`<button class="reading-item ${selected===q.id?'selected':''}" data-mcq="${q.id}" ${selected===q.id?'aria-current="page"':''}><span class="reading-category">${escape(q.topic)}</span><strong>${escape(q.prompt)}</strong><small>${!bank.progress[q.id]?'Not attempted':bank.progress[q.id].correct?'✓ Latest answer correct':'Review needed'}</small></button>`).join('')}</nav><article id="mcq-reader" class="reader"></article></div>`;
  el('mcq-topic').onchange=e=>{topic=e.target.value;selected=filtered()[0]?.id;render();};
  el('mcq-mode').onchange=e=>{mode=e.target.value;selected=filtered()[0]?.id;render();};
  el('mcq-list').querySelectorAll('[data-mcq]').forEach(button=>button.onclick=()=>{if(pending)return;selected=button.dataset.mcq;render();el('mcq-question')?.focus();});
  el('mcq-topic').disabled=pending;el('mcq-mode').disabled=pending;
  reader();
 }
 function reader(){
  const q=bank.questions.find(x=>x.id===selected);
  if(!q){el('mcq-reader').innerHTML='<h2>No questions in this view</h2><p>Choose all questions or another topic. You may have completed every question matching this filter.</p>';return;}
  const result=feedback.get(q.id),index=bank.questions.indexOf(q);
  el('mcq-reader').innerHTML=`<div class="reader-meta"><span>${escape(q.topic)}</span><span>${index+1} / ${bank.questions.length}</span></div><h2 id="mcq-question" tabindex="-1">${escape(q.prompt)}</h2>${q.code?`<pre class="reading-code"><code>${escape(q.code)}</code></pre>`:''}<form id="mcq-form"><fieldset ${result||pending?'disabled':''}><legend>Select one answer</legend>${q.options.map((option,i)=>`<label class="mcq-option ${result?(i===result.answer?'answer-correct':i===result.choice?'answer-wrong':''):''}"><input type="radio" name="choice" value="${i}" required ${result?.choice===i?'checked':''}><span><b>${String.fromCharCode(65+i)}.</b> ${escape(option)}</span></label>`).join('')}</fieldset><button class="primary" id="mcq-submit" ${result||pending?'disabled':''}>${pending?'Checking…':'Check answer'}</button><p id="mcq-status" role="status"></p></form>${result?`<section class="mcq-feedback" aria-live="polite"><h3>${result.correct?'Correct — here is why':'Not quite — review the reasoning'}</h3><p>${escape(result.explanation)}</p><h4>Why each option is right or wrong</h4><ol type="A">${result.rationales.map((why,i)=>`<li><strong>${i===result.answer?'Correct. ':'Incorrect. '}</strong>${escape(why)}</li>`).join('')}</ol><p>Progress saved. First-attempt results remain unchanged by retries.</p></section><div class="reader-actions"><button class="subtle" id="mcq-retry">Try this question again</button><button class="primary" id="mcq-next">Next question →</button></div>`:''}`;
  el('mcq-form').onsubmit=async event=>{
   event.preventDefault();if(pending||feedback.has(q.id))return;
   const input=el('mcq-form').querySelector('input:checked');if(!input){el('mcq-status').textContent='Select an answer first.';return;}
   const choice=Number(input.value);pending=true;el('mcq-submit').disabled=true;el('mcq-submit').textContent='Checking…';el('mcq-form').querySelector('fieldset').disabled=true;el('mcq-topic').disabled=true;el('mcq-mode').disabled=true;
   try{
    const r=await fetch('/api/mcq/answer',{method:'POST',headers:{'Content-Type':'application/json','X-Rustbound-Token':bank.token},body:JSON.stringify({version:bank.version,question:q.id,choice})});
    if(r.status===401){window.location.replace('/login');throw Error('Please sign in again.');}
    const data=await r.json();if(!r.ok)throw Error(data.error||'Could not save the answer.');
    Object.assign(bank,{progress:data.progress,total_attempts:data.total_attempts,answered:data.answered,first_correct:data.first_correct,latest_correct:data.latest_correct});feedback.set(q.id,{...data,choice});pending=false;summary();render();el('mcq-reader').querySelector('.mcq-feedback').scrollIntoView({block:'nearest'});
   }catch(error){pending=false;reader();el('mcq-status').textContent=error.message;el('mcq-topic').disabled=false;el('mcq-mode').disabled=false;}
  };
  if(result){el('mcq-retry').onclick=()=>{feedback.delete(q.id);reader();};el('mcq-next').onclick=()=>{const items=filtered(),current=items.findIndex(x=>x.id===q.id);selected=items.length?items[(current+1)%items.length].id:null;render();el('mcq-question')?.focus();};}
 }
 document.addEventListener('rustbound:view',event=>{if(event.detail==='mcq')open();if(event.detail==='progress')load().then(summary).catch(()=>{el('mcq-summary').textContent='MCQ progress could not load. Open MCQ practice to retry.';});});
 load().catch(()=>{el('mcq-summary').textContent='Open MCQ practice to load your results.';});
})();
