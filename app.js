import {STORAGE_KEY,emptyState,shuffle,makeAttempt,available,followup,topicStats,latestAttempts,validateBackup,mergeBackups} from './core.mjs';
const $=s=>document.querySelector(s);
const h=s=>String(s??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const optionText=o=>o.text.replace(/None of the above(?: answers)?/gi,'None of the other answers').replace(/All of the above/gi,'All of the other answers');
const label={correct:'Correct',incorrect:'Incorrect',unknown:'I don’t know'};
let bank,state,storageBlocked=false,unreadable=null,pendingImport=null,view='practice';
const now=()=>new Date().toISOString();
const question=id=>bank.questions.find(q=>q.id===id);
function notify(message){
  $('#notice').textContent=message;$('#notice').hidden=false;
  if(unreadable&&storageBlocked){const button=document.createElement('button');button.textContent='Download unreadable data';button.onclick=()=>download(unreadable,'aca-recovery.json');$('#notice').append(' ',button);}
}
function save(){
  // shortcut: full localStorage snapshots; move to IndexedDB if history exceeds browser quota.
  try{
    if(storageBlocked)throw new Error('Existing data needs recovery.');
    localStorage.setItem(STORAGE_KEY,JSON.stringify(state));
    $('#global-save').textContent='Saved in this browser';$('#global-save').classList.remove('failed');
    document.querySelectorAll('.save-status').forEach(el=>{el.textContent='Saved in this browser';el.classList.remove('failed');});
    return true;
  }catch(error){
    $('#global-save').textContent='Not saved — export a backup';$('#global-save').classList.add('failed');
    document.querySelectorAll('.save-status').forEach(el=>{el.textContent='Not saved — export a backup';el.classList.add('failed');});
    notify('Browser saving is unavailable, full or paused. Keep this page open and export JSON to preserve your current work. '+(unreadable?'Existing unreadable data is protected; use the recovery download before reset or import.':storageBlocked?'Another tab changed the saved data. Export your work before reloading.':''));return false;
  }
}
function format(text){
  const lines=String(text).split('\n');let result='',plain=[];
  const flush=()=>{if(plain.length){result+=`<div class="text-block">${h(plain.join('\n'))}</div>`;plain=[];}};
  for(let i=0;i<lines.length;i++){
    if(lines[i].trim().startsWith('|')){
      flush();const rows=[];
      while(i<lines.length&&lines[i].trim().startsWith('|')){rows.push(lines[i].trim().slice(1,-1).split('|').map(x=>x.trim()));i++;}i--;
      const header=rows.shift();if(rows[0]?.every(x=>/^:?-+:?$/.test(x)))rows.shift();
      result+=`<div class="table-wrap"><table><thead><tr>${header.map(x=>`<th scope="col">${h(x)}</th>`).join('')}</tr></thead><tbody>${rows.map(row=>`<tr>${row.map(x=>`<td>${h(x)}</td>`).join('')}</tr>`).join('')}</tbody></table></div>`;
    }else plain.push(lines[i]);
  }flush();return result;
}
function bindNotes(){
  document.querySelectorAll('textarea[data-notes]').forEach(el=>el.addEventListener('input',()=>{
    const id=el.dataset.notes;const prev=state.drafts[id]||{selected:null};state.drafts[id]={...prev,notes:el.value,updatedAt:now()};save();
  }));
}
function notes(q,compact=false){
  const d=state.drafts[q.id];const ident=`notes-${q.id}`;
  return `<div class="notes-panel"><label for="${ident}">Calculations / reasoning / notes</label><textarea id="${ident}" data-notes="${h(q.id)}" maxlength="1000000" ${compact?'class="review-notes"':''} placeholder="Write your steps, units and assumptions here…">${h(d?.notes||'')}</textarea><p class="save-status" role="status">${storageBlocked?'Not saved — export a backup':'Saved drafts stay in this browser'}</p><p class="notes-help">${q.status==='review'?'You can save a question or clarification for review.':'Submitting saves a copy of these notes with the attempt. Later edits change only this draft.'}</p></div>`;
}
function source(q,reveal=false){
  return `<details class="source-details"><summary>Source & validation details</summary><p>${h(q.id)} · ${h(q.source.path)}${q.source.line?` · line ${q.source.line}`:''}</p><p>${h(q.source.heading)} / Q${h(q.source.number)}</p>${q.evidence.map(e=>`<p>${h(e.path)} — ${h(e.section)} ${e.url?`<a href="${h(e.url)}" target="_blank" rel="noopener">Primary reference</a>`:''}</p>`).join('')}${q.options.some(o=>optionText(o)!==o.text)?'<p>Display clarification: “above” is shown as “the other answers” so its meaning survives option shuffling. Original option text is preserved in the source excerpt.</p>':''}${q.changes.length?`<p><strong>Study clarifications</strong></p><ul>${q.changes.map(x=>`<li>${h(x)}</li>`).join('')}</ul>`:''}${q.original&&reveal?`<details><summary>Preserved original question (student answer unverified)</summary><pre>${h(q.original.raw)}</pre></details>`:''}</details>`;
}
function updateAvailable(){
  if(!bank)return;const prefs=Object.fromEntries(['topic','subtopic','difficulty','origin'].map(k=>[k,$('#'+k).value]));
  const n=available(bank.questions,prefs,$('#mode').value,state.attempts).length;
  $('#available').textContent=`${n} matching validated question${n===1?'':'s'}`;$('#start').disabled=!n;
}
function setView(next,focus=true){
  view=next;state.view=next;save();render();if(focus)$('#main').focus();
}
function render(){
  document.querySelectorAll('[data-view]').forEach(el=>el.setAttribute('aria-pressed',String(el.dataset.view===view)));
  if(view==='history')renderHistory();else if(view==='review')renderReview();else renderPractice();
  positionNotebook();bindNotes();updateAvailable();
  if($('#global-save').classList.contains('failed'))document.querySelectorAll('.save-status').forEach(el=>{el.textContent='Not saved — export a backup';el.classList.add('failed');});
}
function startSession(ids,mode){
  const q=question(ids[0]);state.session={queue:ids,index:0,order:shuffle(q.options.map(o=>o.id)),mode,attemptId:null,attemptIds:[]};
  if(matchMedia('(max-width:760px)').matches){$('#session-settings').open=false;$('.storage').open=false;}
  setView('practice');
}
function retry(id){startSession([id],'retry');}
const narrowLayout=matchMedia('(max-width:1150px)');
function positionNotebook(){
  if(matchMedia('(max-width:760px)').matches){$('#session-settings').open=false;$('.storage').open=false;}
  const notebook=$('#notebook');if(!notebook)return;
  const parent=narrowLayout.matches?$('#notebook-slot'):$('.question-layout');
  if(notebook.parentElement!==parent)parent.append(notebook);
}
narrowLayout.addEventListener('change',positionNotebook);
function renderPractice(){
  const session=state.session;
  if(!session){
    const scored=bank.questions.filter(q=>q.status==='validated'),latest=latestAttempts(state.attempts);
    const revisit=[...latest.values()].filter(a=>a.outcome!=='correct').length;
    $('#main').innerHTML=`<section class="welcome study-hero"><span class="eyebrow">YOUR STUDY SPACE</span><h2>Think it through.<br>Build your confidence.</h2><p>Work through the scenario, keep your calculations, and learn from the rule behind each answer.</p><div class="actions"><button class="primary" id="welcome-start">${state.attempts.length?'Keep practising':'Start practising'} <span aria-hidden="true">↗</span></button><span class="hero-note">One question at a time. Your notes stay with you.</span></div></section><div class="study-stats" aria-label="Study overview"><div><strong>${state.attempts.length}</strong><span>Attempts logged</span></div><div><strong>${revisit}</strong><span>Questions to revisit</span></div><div><strong>${scored.length}</strong><span>Validated questions</span></div></div><section class="topic-section"><div class="section-heading"><h2>Find your focus</h2><p class="muted">Choose a topic for your next session.</p></div><div class="topic-grid">${[...new Set(scored.map(q=>q.topic))].map((topic,index)=>{const pool=scored.filter(q=>q.topic===topic),seen=pool.filter(q=>latest.has(q.id)).length;return `<button class="topic-card" data-topic="${h(topic)}"><span class="topic-number" aria-hidden="true">0${index+1}</span><span class="topic-title">${h(topic)}</span><span class="topic-count">${pool.length} questions · ${seen} explored</span><span class="topic-track" aria-hidden="true"><span style="width:${100*seen/pool.length}%"></span></span><span class="topic-arrow" aria-hidden="true">↗</span></button>`;}).join('')}</div></section><section class="study-tip"><span class="eyebrow">A USEFUL CHECK · DEFERRED TAX</span><h3>Difference first. Tax rate second.</h3><p>Temporary difference × tax rate = deferred tax amount. Compare an ordinary asset’s carrying amount with its tax base to decide whether that amount is an asset or a liability.</p><p class="muted">${bank.questions.filter(q=>q.status==='review').length} unresolved originals are available in Source review. Study results describe your attempts and do not establish mastery.</p></section>`;
    $('#welcome-start').onclick=()=>$('#setup').requestSubmit();
    document.querySelectorAll('[data-topic]').forEach(el=>el.onclick=()=>{
      $('#topic').value=el.dataset.topic;for(const key of ['subtopic','difficulty','origin'])$('#'+key).value='';$('#mode').value='topic';$('#setup').requestSubmit();
    });return;
  }
  const q=question(session.queue[session.index]);const attempt=state.attempts.find(a=>a.id===session.attemptId);const d=state.drafts[q.id];
  const completed=session.attemptIds.length;
  $('#main').innerHTML=`<div class="session-head"><div><h2>Question ${session.index+1} of ${session.queue.length}</h2><p class="muted">${h(session.mode==='missed'?'Review missed / unknown':session.mode==='followup'?'Suggested follow-up':session.mode==='retry'?'Retry':session.mode==='topic'?'Topic practice':'Mixed practice')} · ${completed} submitted in this session</p></div><button id="end-session">End session & see results</button></div><progress max="${session.queue.length}" value="${session.index+(attempt?1:0)}" aria-label="Session progress"></progress><div class="question-layout"><article class="question"><div class="metadata"><span>${h(q.topic)}</span><span>${h(q.subtopic)}</span><span>${h(q.difficulty)} · study estimate</span><span>${q.origin==='original'?'Original bank':'Generated'}</span>${q.marks!==null?`<span>${q.marks} source mark${q.marks===1?'':'s'}</span>`:''}</div>${q.scenario?`<div class="scenario">${format(q.scenario)}</div>`:''}<div class="prompt" id="question-prompt">${format(q.prompt.replace(/^\d+(?:\.\d+)?\.?\s*(?:\(\d+ marks?\)\s*)?/,''))}</div>${q.assumptions.length?`<details class="assumptions" open><summary>Assumptions for this question</summary>${q.assumptions.map(s=>`<p>${h(s)}</p>`).join('')}</details>`:''}<form id="answer-form"><fieldset class="options" ${attempt?'disabled':''}><legend>Choose one answer <span class="muted">· shuffled, with original labels</span></legend>${session.order.map(id=>{const o=q.options.find(o=>o.id===id);return `<label class="option ${attempt&&id===q.correctOptionId?'correct-option':''} ${attempt?.outcome==='incorrect'&&id===attempt.optionId?'wrong-option':''}"><input type="radio" name="answer" value="${h(id)}" ${((attempt?attempt.optionId:d?.selected)===id)?'checked':''}><span>${h(o.id.toUpperCase())}. ${h(optionText(o))}</span></label>`;}).join('')}</fieldset><div id="notebook-slot"></div><p id="answer-error" class="danger" role="alert"></p>${!attempt?`<div class="actions"><button class="primary" type="submit">Submit answer</button><button type="button" id="unknown">I don’t know</button></div>`:''}</form><div id="feedback">${attempt?feedback(q,attempt):''}</div>${source(q,!!attempt)}</article><aside id="notebook" class="notes-panel" aria-label="Question notebook">${notes(q)}${attempt?`<details><summary>Notes saved with this attempt</summary><div class="snapshot">${h(attempt.notesSnapshot||'No notes at submission.')}</div><p class="muted">${h(new Date(attempt.timestamp).toLocaleString())}</p></details>`:''}</aside></div>`;
  $('#answer-form').onsubmit=e=>{e.preventDefault();const selected=document.querySelector('input[name=answer]:checked');if(!selected){$('#answer-error').textContent='Choose an answer or use “I don’t know”.';document.querySelector('input[name=answer]').focus();return;}submit(q,selected.value);};
  $('#unknown')?.addEventListener('click',()=>submit(q,null));
  document.querySelectorAll('input[name=answer]').forEach(el=>el.addEventListener('change',()=>{state.drafts[q.id]={notes:state.drafts[q.id]?.notes||'',selected:el.value,updatedAt:now()};save();}));
  $('#end-session').onclick=showResults;bindFeedback(q,attempt);
}
function submit(q,optionId){
  if(state.session.attemptId)return;
  const attempt=makeAttempt(q,optionId,state.drafts[q.id]?.notes||'',now(),crypto.randomUUID(),bank.bankVersion);
  state.attempts.push(attempt);state.session.attemptId=attempt.id;state.session.attemptIds.push(attempt.id);save();render();
  $('#feedback-heading').focus();
}
function feedback(q,a){
  const correct=q.options.find(o=>o.id===q.correctOptionId),selected=q.options.find(o=>o.id===a.optionId),suggested=a.outcome!=='correct'?followup(q,a,bank.questions,state.attempts):null;
  return `<section class="feedback" data-outcome="${h(a.outcome)}"><h3 class="outcome-${h(a.outcome)}" id="feedback-heading" tabindex="-1">${label[a.outcome]}</h3><p><strong>Correct answer:</strong> ${h(optionText(correct))}</p><p>${h(q.explanation)}</p>${q.workedCalculation?`<div class="calculation">${h(q.workedCalculation)}</div>`:''}${a.outcome==='incorrect'?`<p><strong>Why your choice is wrong:</strong> ${h(selected.explanation)}</p><p class="tag"><strong>Misconception:</strong> ${h(selected.misconception.replaceAll('-',' '))}</p>`:a.outcome==='unknown'?'<p>You chose “I don’t know”. This is counted separately from an incorrect answer.</p>':''}<details><summary>Explain all answer options</summary><ul>${q.options.map(o=>`<li><strong>${h(optionText(o))}</strong>${o.id===correct.id?' — correct':''}<br>${h(o.explanation)}${o.misconception?`<br><span class="tag">Misconception: ${h(o.misconception.replaceAll('-',' '))}</span>`:''}</li>`).join('')}</ul></details><div class="actions"><button id="next-question" class="primary">${state.session.index+1<state.session.queue.length?'Next question':'See session results'}</button>${suggested?`<button id="followup" data-question="${h(suggested.id)}">Try a relevant follow-up</button>`:''}</div>${suggested?`<p class="muted">Suggested focus: ${h(suggested.subtopic)} with a different scenario.</p>`:''}</section>`;
}
function bindFeedback(q,attempt){
  if(!attempt)return;
  $('#next-question').onclick=()=>{
    const s=state.session;if(s.index+1>=s.queue.length){showResults();return;}s.index++;s.attemptId=null;s.order=shuffle(question(s.queue[s.index]).options.map(o=>o.id));save();render();$('#main').focus();
  };
  $('#followup')?.addEventListener('click',e=>{
    const id=e.currentTarget.dataset.question;const s=state.session;
    // Move the suggested question next within this session, keeping all submitted attempts.
    s.queue=[...s.queue.slice(0,s.index+1),id,...s.queue.slice(s.index+1).filter(x=>x!==id)];
    if(s.queue.slice(0,s.index+1).includes(id)){startSession([id],'followup');return;}
    s.index++;s.attemptId=null;s.order=shuffle(question(id).options.map(o=>o.id));save();render();$('#main').focus();
  });
}
function showResults(){
  const session=state.session;const rows=state.attempts.filter(a=>session.attemptIds.includes(a.id));const correct=rows.filter(a=>a.outcome==='correct').length,incorrect=rows.filter(a=>a.outcome==='incorrect').length,unknown=rows.length-correct-incorrect;
  state.session=null;save();
  $('#main').innerHTML=`<section class="welcome"><h2>Session results</h2><p>${rows.length} submitted of ${session.queue.length} questions. Each retry is a separate attempt.</p><div class="result-grid"><div><strong>${correct}</strong>Correct</div><div><strong>${incorrect}</strong>Incorrect</div><div><strong>${unknown}</strong>I don’t know</div></div><p>Accuracy among answered attempts: <strong>${correct+incorrect?Math.round(100*correct/(correct+incorrect))+'%':'No answered attempts'}</strong>. Unknown responses are excluded from this percentage.</p><p class="muted">This result describes this session; it does not establish mastery. Your calculations and original attempt snapshots are saved in Learning history.</p><div class="actions"><button class="primary" id="again">Start another session</button><button id="results-history">See learning history</button></div></section>`;
  $('#again').onclick=()=>$('#setup').requestSubmit();$('#results-history').onclick=()=>setView('history');$('#main').focus();updateAvailable();
}
function renderHistory(){
  const latest=latestAttempts(state.attempts);const retryable=bank.questions.filter(q=>q.status==='validated'&&latest.has(q.id)&&latest.get(q.id).outcome!=='correct');
  const tags={};state.attempts.forEach(a=>{if(a.misconception)tags[a.misconception]=(tags[a.misconception]||0)+1;});
  const touched=bank.questions.filter(q=>state.drafts[q.id]||state.attempts.some(a=>a.questionId===q.id));
  $('#main').innerHTML=`<h2>Learning history</h2><p class="muted">All submitted attempts are retained. Accuracy is correct ÷ (correct + incorrect); “I don’t know” is listed separately. Repeated attempts count separately and do not establish mastery.</p><div class="table-wrap"><table><caption>Attempts by topic</caption><thead><tr><th scope="col">Topic</th><th scope="col">Attempts</th><th scope="col">Correct</th><th scope="col">Incorrect</th><th scope="col">I don’t know</th><th scope="col">Accuracy</th></tr></thead><tbody>${topicStats(bank.questions,state.attempts).map(s=>`<tr><th scope="row">${h(s.topic)}</th><td>${s.total}</td><td>${s.correct}</td><td>${s.incorrect}</td><td>${s.unknown}</td><td>${s.accuracy===null?'—':s.accuracy+'%'}</td></tr>`).join('')}</tbody></table></div><section class="dashboard-section"><h3>Misconceptions across attempts</h3>${Object.keys(tags).length?`<ul>${Object.entries(tags).sort((a,b)=>b[1]-a[1]).map(([tag,n])=>`<li>${h(tag.replaceAll('-',' '))}: ${n} incorrect attempt${n===1?'':'s'}${n>1?' — recurring':''}</li>`).join('')}</ul>`:'<p class="muted">No misconception tags recorded yet.</p>'}</section><section class="dashboard-section"><h3>Available for retry (${retryable.length})</h3><p class="muted">Questions whose latest attempt is incorrect or “I don’t know”. Earlier misses remain in the history after a correct retry.</p>${retryable.length?retryable.map(q=>`<div class="history-item"><p><strong>${h(q.id)} · ${h(q.subtopic)}</strong> — ${label[latest.get(q.id).outcome]}</p><button data-retry="${h(q.id)}">Retry question</button></div>`).join(''):'<p class="empty">No outstanding missed questions. Start a session to add learning history.</p>'}</section><section class="dashboard-section"><h3>Saved notes & past attempts (${touched.length} questions)</h3>${touched.length?touched.map(q=>{
    const rows=state.attempts.filter(a=>a.questionId===q.id).slice().reverse();
    return `<details class="history-item"><summary>${h(q.id)} · ${h(q.subtopic)} — ${rows.length} attempt${rows.length===1?'':'s'}</summary><div class="scenario">${format(q.prompt)}</div>${notes(q,true)}${q.status==='validated'?`<button data-retry="${h(q.id)}">Retry as a new attempt</button>`:'<p class="review-label">Unresolved source — excluded from scoring</p>'}${rows.map(a=>`<details><summary>${label[a.outcome]} · ${h(new Date(a.timestamp).toLocaleString())}</summary><p>Selected: ${h(q.options.find(o=>o.id===a.optionId)?.text||'I don’t know')}</p><p class="muted">Bank ${h(a.bankVersion)} · Attempt ${h(a.id)}</p><strong>Notes at submission (preserved snapshot)</strong><div class="snapshot">${h(a.notesSnapshot||'No notes at submission.')}</div>${a.misconception?`<p class="tag">Misconception: ${h(a.misconception.replaceAll('-',' '))}</p>`:''}</details>`).join('')}</details>`;
  }).join(''):'<p class="muted">Your question notes and submissions will appear here.</p>'}</section>`;
  document.querySelectorAll('[data-retry]').forEach(el=>el.onclick=()=>retry(el.dataset.retry));
}
function renderReview(){
  const rows=bank.questions.filter(q=>q.status==='review');
  $('#main').innerHTML=`<h2>Unresolved source questions</h2><p>These ${rows.length} questions are excluded from every scored session. The original wording and unverified student responses are preserved here. Save a note if you want to check one with the course team.</p>${rows.map(q=>`<details class="review-item"><summary>${h(q.id)} · ${h(q.source.heading)} / Q${h(q.source.number)}</summary><p class="review-label">Unresolved — no scored answer key</p><p>${h(q.reviewReason)}</p>${q.scenario?`<div class="scenario">${format(q.scenario)}</div>`:''}<div class="scenario">${format(q.prompt)}</div><ul>${q.options.map(o=>`<li>${h(o.id)}. ${h(o.text)}</li>`).join('')}</ul>${notes(q,true)}${source(q,true)}</details>`).join('')}`;
}
function download(text,name){const url=URL.createObjectURL(new Blob([text],{type:'application/json'}));const a=document.createElement('a');a.href=url;a.download=name;a.click();setTimeout(()=>URL.revokeObjectURL(url),1000);}
async function init(){
  try{
    const response=await fetch('./content/questions.json');if(!response.ok)throw new Error('Question data could not be loaded.');bank=await response.json();state=emptyState(bank.bankVersion);
    try{const raw=localStorage.getItem(STORAGE_KEY);if(raw)state=validateBackup(JSON.parse(raw),bank);}catch(error){
      try{unreadable=localStorage.getItem(STORAGE_KEY);}catch{}
      storageBlocked=true;notify('Saved browser data could not be read. It has been left untouched. Download the recovery file before importing a valid backup or resetting.');
    }
    view=state.view;
    for(const key of ['topic','subtopic'])[...new Set(bank.questions.filter(q=>q.status==='validated').map(q=>q[key]))].sort().forEach(v=>{const o=new Option(v,v);$('#'+key).add(o);});
    for(const key of ['topic','subtopic','difficulty','origin'])$('#'+key).value=state.preferences[key];
    $('#review-count').textContent=`(${bank.questions.filter(q=>q.status==='review').length})`;
    $('#setup').onsubmit=e=>{e.preventDefault();const mode=$('#mode').value;state.preferences=Object.fromEntries(['topic','subtopic','difficulty','origin'].map(k=>[k,$('#'+k).value]));
      if(mode==='topic'&&!state.preferences.topic&&!state.preferences.subtopic){notify('Choose a topic or focus for topic practice.');$('#topic').focus();return;}
      const pool=shuffle(available(bank.questions,state.preferences,mode,state.attempts)).map(q=>q.id);if(!pool.length){notify('No validated questions match these filters. Adjust the filters or try mixed practice.');return;}
      const length=$('#length').value;startSession(length==='all'?pool:pool.slice(0,Number(length)),mode);
    };
    for(const key of ['topic','subtopic','difficulty','origin','mode'])$('#'+key).onchange=()=>{
      if(key==='topic' && $('#subtopic').value && !bank.questions.some(q=>q.topic===$('#topic').value&&q.subtopic===$('#subtopic').value))$('#subtopic').value='';
      state.preferences=Object.fromEntries(['topic','subtopic','difficulty','origin'].map(k=>[k,$('#'+k).value]));save();updateAvailable();
    };
    $('#tax-focus').onclick=()=>{$('#topic').value='Financial Reporting';$('#subtopic').value='Deferred taxes';$('#origin').value='generated';$('#difficulty').value='';$('#mode').value='topic';$('#setup').requestSubmit();};
    document.querySelectorAll('[data-view]').forEach(el=>el.onclick=()=>setView(el.dataset.view));
    $('#export').onclick=()=>download(JSON.stringify({...state,exportedAt:now()},null,2),`aca-backup-${now().slice(0,10)}.json`);
    $('#import').onchange=async e=>{
      const file=e.target.files[0];if(!file)return;
      try{if(file.size>8*1024*1024)throw new Error('Backup is larger than 8 MB. No data was changed.');pendingImport=validateBackup(JSON.parse(await file.text()),bank);$('#import-summary').textContent=`This backup contains ${pendingImport.attempts.length} attempts and ${Object.keys(pendingImport.drafts).length} question drafts.`;$('#import-dialog').returnValue='cancel';$('#import-dialog').showModal();}catch(error){notify(error.message);}finally{e.target.value='';}
    };
    $('#import-dialog').onclose=()=>{
      if($('#import-dialog').returnValue==='confirm'&&pendingImport){
        try{const merged=mergeBackups(state,pendingImport);state=merged;storageBlocked=false;unreadable=null;const saved=save();render();notify(saved?'Backup merged. All distinct attempts are preserved.':'Backup merged in memory; browser saving failed. Export JSON before closing.');}catch(error){notify(error.message);}
      }pendingImport=null;
    };
    $('#reset').onclick=()=>{$('#reset-dialog').returnValue='cancel';$('#reset-dialog').showModal();};
    $('#reset-dialog').onclose=()=>{if($('#reset-dialog').returnValue==='confirm'){
      try{localStorage.removeItem(STORAGE_KEY);}catch{notify('Browser storage could not be reset. Your data has been kept.');return;}
      state=emptyState(bank.bankVersion);storageBlocked=false;unreadable=null;view='practice';for(const k of ['topic','subtopic','difficulty','origin'])$('#'+k).value='';save();render();notify('Study data has been reset in this browser.');
    }};
    window.addEventListener('storage',e=>{if(e.key===STORAGE_KEY){storageBlocked=true;$('#global-save').textContent='Saving paused — another tab changed data';$('#global-save').classList.add('failed');notify('Study data changed in another tab. Saving is paused to preserve both copies. Export your work before reloading to load those changes.');}});
    render();if(!storageBlocked)save();else{$('#global-save').textContent='Existing data needs recovery';$('#global-save').classList.add('failed');}
  }catch(error){$('#main').innerHTML=`<h2>Unable to launch practice</h2><p>${h(error.message)}</p><p>Launch a local server from this folder with <code>python3 -m http.server 8000</code>, then open <a href="http://localhost:8000">http://localhost:8000</a>. See <a href="README.md">the launch instructions</a>.</p>`;}
}
init();
