import {STORAGE_KEY,emptyState,shuffle,makeAttempt,grade,available,followup,topicStats,latestAttempts,validateBackup,mergeBackups} from './core.mjs';
import {createProgressSync,progressKey} from './cloud.mjs';
import {supabaseConfig} from './supabase-config.mjs';

const $=s=>document.querySelector(s);
const $$=s=>document.querySelectorAll(s);
const h=s=>String(s??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const optionText=o=>o.text.replace(/None of the above(?: answers)?/gi,'None of the other answers').replace(/All of the above/gi,'All of the other answers');
const shownLabel=(order,id)=>String.fromCharCode(65+order.indexOf(id));
const root=document.documentElement;
root.dataset.input='keyboard';
document.addEventListener('keydown',()=>{if(root.dataset.input!=='keyboard')root.dataset.input='keyboard';});
document.addEventListener('pointerdown',()=>{if(root.dataset.input!=='pointer')root.dataset.input='pointer';},{passive:true});

const label={correct:'Correct',incorrect:'Incorrect',unknown:'I don’t know'};
const controllingTopics=['Management Accounting','Budgeting','Variances','Capital Budgeting','Cost and Performance Management'];
let bank,state,storageBlocked=false,unreadable=null,pendingImport=null,view='practice';
let appMode='practice'; // 'practice' or 'exam'
let examTimerInterval=null;
let examTimerPaused=false;
let themeChanging=false;
let activeUser=null,cloud=null,storageKey=STORAGE_KEY;

const now=()=>new Date().toISOString();
const question=id=>bank.questions.find(q=>q.id===id);

const preciseSubtopics={
  "Financial Reporting":[
    {val:"",text:"All Financial Reporting Areas"},
    {val:"Deferred taxes",text:"Deferred Taxes (DTA/DTL & Temporary Differences)"},
    {val:"Leases",text:"IFRS 16 Leases (PV, Carrying Amount & Split)"},
    {val:"Impairment",text:"Impairment of Assets & Impairment Tests"},
    {val:"Goodwill",text:"Goodwill Subsequent Measurement (IFRS vs FER)"},
    {val:"Accounting frameworks",text:"Frameworks: Principle- vs Rule-based & Swiss CO"},
    {val:"Pensions",text:"Employee Benefits & Defined-Benefit Pension Risk"}
  ],
  "Consolidated Statements":[
    {val:"",text:"All Consolidation Areas"},
    {val:"Acquisition accounting",text:"Acquisition Mechanics, Reserves & Goodwill"},
    {val:"Equity method",text:"Equity Method & Associate Roll-Forwards"},
    {val:"Consolidation concepts",text:"Group Scope, Elimination Logic & NCI Concepts"},
    {val:"Accounting frameworks",text:"Consolidation Frameworks & Swiss CO Overlay"}
  ],
  "Auditing":[
    {val:"",text:"All Auditing Areas"},
    {val:"Audit procedures",text:"Substantive & Analytical Audit Procedures"},
    {val:"Materiality",text:"Materiality Benchmarks & Misstatements"},
    {val:"Audit purpose",text:"Audit Purpose, Objectives & Credibility"},
    {val:"Audit scope",text:"Swiss OR Triggers: Ordinary vs Limited Audit"},
    {val:"Assurance",text:"Levels of Assurance (Reasonable vs Limited)"},
    {val:"Audit opinions",text:"Audit Opinions, Modifications & Reports"},
    {val:"Key Audit Matters",text:"Key Audit Matters (KAMs) Purpose & Disclosures"},
    {val:"Going concern",text:"Going Concern Assessment & Reporting"},
    {val:"Expectation gap",text:"The Audit Expectation Gap"},
    {val:"Internal controls",text:"Internal Control System (ICS) & Governance"}
  ],
  "Management Accounting":[
    {val:"",text:"All Management Accounting Areas"},
    {val:"CVP analysis",text:"Cost-Volume-Profit (CVP) & Breakeven Analysis"},
    {val:"Manufacturing cost flows",text:"Manufacturing Cost Flows & COGM / COGS"},
    {val:"Pricing and target costing",text:"Target Costing & Markup Pricing"},
    {val:"Job costing",text:"Job Costing & Manufacturing Overhead Allocation"},
    {val:"Cost concepts",text:"Direct vs Indirect & Fixed vs Variable Costs"}
  ],
  "Budgeting":[
    {val:"",text:"All Budgeting Areas"},
    {val:"Cash collections",text:"Cash Collections & Cash Budgets"},
    {val:"Activity-based budgeting",text:"Activity-Based Budgeting (ABB)"},
    {val:"Production budget",text:"Production & Materials Budgets"},
    {val:"Sales budget",text:"Sales Forecasting & Operating Budgets"},
    {val:"Purchases budget",text:"Direct Materials Purchases Budget"},
    {val:"Income statement budget",text:"Budgeted Income Statement & Master Budget"}
  ],
  "Variances":[
    {val:"",text:"All Variance Analysis Areas"},
    {val:"Flexible budgets",text:"Flexible Budgets vs Static Budgets"},
    {val:"Flexible-budget variance",text:"Flexible-Budget & Sales-Volume Variances"},
    {val:"Direct material variances",text:"Direct Material Price & Efficiency Variances"},
    {val:"Direct labor price variance",text:"Direct Labor Rate & Efficiency Variances"},
    {val:"Fixed-overhead variances",text:"Fixed & Variable Overhead Variance Analysis"}
  ]
};

function initTheme(){
  const saved=localStorage.getItem('aca_theme');
  const prefersDark=window.matchMedia&&window.matchMedia('(prefers-color-scheme: dark)').matches;
  const isDark=saved==='dark'||(!saved&&prefersDark);
  if(isDark)root.classList.add('dark');else root.classList.remove('dark');
  $('#theme-toggle').setAttribute('aria-checked',String(isDark));
}
async function toggleTheme(){
  if(themeChanging)return;
  const update=()=>{
    const isDark=root.classList.toggle('dark');
    try{localStorage.setItem('aca_theme',isDark?'dark':'light');}catch{notify('Theme changed for this visit. Browser storage is unavailable.');}
    $('#theme-toggle').setAttribute('aria-checked',String(isDark));
  };
  if(!document.startViewTransition||matchMedia('(prefers-reduced-motion: reduce)').matches){update();return;}
  const rect=$('#theme-toggle').getBoundingClientRect();
  const x=rect.left+rect.width/2,y=rect.top+rect.height/2;
  const radius=Math.hypot(Math.max(x,innerWidth-x),Math.max(y,innerHeight-y));
  themeChanging=true;root.classList.add('theme-changing');
  const transition=document.startViewTransition(update);
  try{
    await transition.ready;
    await root.animate({clipPath:[`circle(0px at ${x}px ${y}px)`,`circle(${radius}px at ${x}px ${y}px)`]},{duration:650,easing:'cubic-bezier(.22,1,.36,1)',pseudoElement:'::view-transition-new(root)'}).finished;
  }catch{
    // A skipped transition still applies its update callback.
    await transition.updateCallbackDone.catch(()=>{});
  }finally{
    await transition.finished.catch(()=>{});
    root.classList.remove('theme-changing');themeChanging=false;
  }
}

function notify(message){
  $('#notice').textContent=message;$('#notice').hidden=false;
  if(unreadable&&storageBlocked){const button=document.createElement('button');button.textContent='Download unreadable data';button.onclick=()=>download(unreadable,'aca-recovery.json');$('#notice').append(' ',button);}
}

function save(sync=true){
  try{
    if(storageBlocked)throw new Error('Existing data needs recovery.');
    localStorage.setItem(storageKey,JSON.stringify(state));
    $('#global-save').textContent='Saved in this browser';$('#global-save').classList.remove('failed');
    $$('.save-status').forEach(el=>{el.textContent='Saved in this browser';el.classList.remove('failed');});
    if(sync)cloud?.schedule();
    return true;
  }catch(error){
    $('#global-save').textContent='Not saved — export a backup';$('#global-save').classList.add('failed');
    $$('.save-status').forEach(el=>{el.textContent='Not saved — export a backup';el.classList.add('failed');});
    notify('Browser saving is unavailable, full or paused. Keep this page open and export JSON to preserve your current work.');
    return false;
  }
}

function loadProgress(){
  state=emptyState(bank.bankVersion);storageBlocked=false;unreadable=null;
  try{
    const raw=localStorage.getItem(storageKey);
    if(raw)state=validateBackup(JSON.parse(raw),bank);
    return Boolean(raw);
  }catch{
    try{unreadable=localStorage.getItem(storageKey);}catch{}
    storageBlocked=true;notify('Saved browser data could not be read. Export a recovery copy before resetting.');
  }
}

function restoreProgressView(){
  stopExamTimer();view=state.view;
  state.preferences.origin='';$('#origin').value='';
  $('#topic').value=state.preferences.topic;
  populateSubtopics(state.preferences.topic);
  $('#subtopic').value=state.preferences.subtopic;
  $('#difficulty').value=state.preferences.difficulty;
  setAppMode(state.session?.mode.startsWith('exam')?'exam':'practice',false);
  if(state.session?.mode.startsWith('exam')&&view==='practice')startExamTimer();
  render();
}

function showAccountAnnouncement(){
  const key='aca-account-announcement-v1';
  try{if(localStorage.getItem(key)||sessionStorage.getItem(key))return;}catch{}
  if(!activeUser)$('#account-announcement').showModal();
  try{localStorage.setItem(key,'seen');}catch{try{sessionStorage.setItem(key,'seen');}catch{}}
}

async function initCloud(){
  const status=message=>{$('#cloud-status').textContent=message;};
  try{
    const {createClient}=await import('https://cdn.jsdelivr.net/npm/@supabase/supabase-js@2.118.0/+esm');
    const client=createClient(supabaseConfig.url,supabaseConfig.publishableKey);
    cloud=createProgressSync({client,getState:()=>state,validate:value=>validateBackup(value,bank),onStatus:status,
      applyState(next){
        const changed=JSON.stringify(next)!==JSON.stringify(state);
        state=next;
        if(!save(false))throw new Error('Browser saving is unavailable. Export a backup first.');
        if(changed){
          const focused=document.activeElement,notesId=focused?.dataset.notes;
          const selection=notesId?[focused.selectionStart,focused.selectionEnd]:null;
          restoreProgressView();
          if(notesId){const field=$$('textarea[data-notes]').find(el=>el.dataset.notes===notesId);field?.focus();if(field)field.setSelectionRange(...selection);}
        }
      },
    });
    let initialized=false;
    const changeUser=user=>{
      const sameUser=activeUser?.id===user?.id;
      if(initialized&&sameUser)return;
      initialized=true;cloud.setUser(null);
      activeUser=user;storageKey=progressKey(STORAGE_KEY,user?.id);
      let cached=true;
      if(!sameUser){cached=loadProgress();restoreProgressView();}
      $('#account-user').textContent=user?`Signed in as ${user.email}`:'Use an account to save progress across devices.';
      $('#google-login').hidden=Boolean(user);$('#account-actions').hidden=!user;
      $('#reset').disabled=Boolean(user);
      $('#reset').title=user?'Sign out to reset guest data. Account history is retained.':'';
      cloud.setUser(user?.id??null,!cached);
      status(user?'Loading account progress…':'Guest progress is saved in this browser.');
      if(!storageBlocked){save(false);if(user)void cloud.flush();}
      else status('Cloud sync paused. Export the unreadable browser copy before continuing.');
    };
    // Defer work outside the auth callback to avoid holding the SDK's auth lock.
    client.auth.onAuthStateChange((_event,session)=>{
      if(activeUser?.id!==session?.user?.id)cloud.setUser(null);
      setTimeout(()=>changeUser(session?.user??null),0);
    });
    const {data,error}=await client.auth.getSession();
    if(error)throw error;
    changeUser(data.session?.user??null);
    $('#google-login').disabled=false;
    const signIn=async()=>{
      $('#google-login').disabled=true;status('Opening Google sign-in…');
      $('#announcement-login').disabled=true;
      $('#announcement-status').hidden=true;
      try{
        const {error}=await client.auth.signInWithOAuth({provider:'google',options:{redirectTo:new URL('./',location.href).href}});
        if(error)throw error;
      }catch(error){
        const message=`Sign-in failed. ${error.message}`;status(message);
        $('#announcement-status').textContent=message;$('#announcement-status').hidden=false;
      }
      finally{$('#google-login').disabled=false;$('#announcement-login').disabled=false;}
    };
    $('#google-login').onclick=signIn;
    $('#announcement-login').onclick=signIn;
    $('#announcement-dismiss').onclick=()=>$('#account-announcement').close();
    $('#sync-now').onclick=()=>{
      if(storageBlocked){status('Cloud sync paused. Export a recovery copy first.');return;}
      void cloud.flush();
    };
    $('#sign-out').onclick=async()=>{
      $('#sign-out').disabled=true;
      try{
        const saved=!storageBlocked&&await cloud.flush();
        if(!saved&&!confirm('Some progress has not synced. A browser copy will be kept for this account. Sign out anyway?'))return;
        const {error}=await client.auth.signOut({scope:'local'});
        if(error)throw error;
        changeUser(null);
      }catch(error){status(`Sign-out failed. ${error.message}`);}
      finally{$('#sign-out').disabled=false;}
    };
    $('#merge-guest').onclick=()=>{
      try{
        if(storageBlocked)throw new Error('Export a recovery copy first.');
        const raw=localStorage.getItem(STORAGE_KEY);
        if(!raw){status('There is no guest progress to add.');return;}
        state=mergeBackups(state,validateBackup(JSON.parse(raw),bank));
        save();restoreProgressView();
      }catch(error){status(error.message);}
    };
    addEventListener('online',()=>{if(!storageBlocked)void cloud.flush();});
    addEventListener('focus',()=>{if(!storageBlocked)void cloud.flush();});
    document.addEventListener('visibilitychange',()=>{
      if(document.visibilityState==='hidden'&&!storageBlocked){save();void cloud.flush();}
    });
    showAccountAnnouncement();
  }catch(error){
    status(`Account connection unavailable. ${error.message} Guest saving still works.`);
    $('#google-login').disabled=true;
  }
}

function format(text){
  const lines=String(text).split('\n');let result='',plain=[];
  const flush=()=>{if(plain.length){result+=`<div class="text-block">${h(plain.join('\n'))}</div>`;plain=[];}};
  for(let i=0;i<lines.length;i++){
    if(lines[i].trim().startsWith('|')){
      flush();const rows=[];
      while(i<lines.length&&lines[i].trim().startsWith('|')){rows.push(lines[i].trim().slice(1,-1).split('|').map(x=>x.trim()));i++;}i--;
      const header=rows.shift();const alignment=rows[0]?.every(x=>/^:?-+:?$/.test(x))?rows.shift():[];
      const numeric=col=>alignment[col]?.endsWith(':')?' class="numeric"':'';
      result+=`<div class="table-wrap exercise-table" role="region" aria-label="Exercise data" tabindex="0"><table><thead><tr>${header.map((x,col)=>`<th scope="col"${numeric(col)}>${h(x)}</th>`).join('')}</tr></thead><tbody>${rows.map(row=>`<tr>${row.map((x,col)=>col===0?`<th scope="row">${h(x)}</th>`:`<td${numeric(col)}>${h(x)}</td>`).join('')}</tr>`).join('')}</tbody></table></div>`;
    }else plain.push(lines[i]);
  }flush();return result;
}

function bindNotes(){
  $$('textarea[data-notes]').forEach(el=>el.addEventListener('input',()=>{
    const id=el.dataset.notes;const prev=state.drafts[id]||{selected:null};state.drafts[id]={...prev,notes:el.value,updatedAt:now()};save();
  }));
}

function notes(q,compact=false){
  const d=state.drafts[q.id];const ident=`notes-${q.id}`;
  return `<div class="notes-panel"><label for="${ident}">Calculations / reasoning / notes</label><textarea id="${ident}" data-notes="${h(q.id)}" maxlength="1000000" ${compact?'class="review-notes"':''}>${h(d?.notes||'')}</textarea><p class="save-status" role="status">${storageBlocked?'Not saved — export a backup':'Saved'}</p></div>`;
}

function populateSubtopics(topic){
  const select=$('#subtopic');
  select.innerHTML='';
  if(!topic){
    select.add(new Option('All specific focus areas',''));
    for(const [t,subs] of Object.entries(preciseSubtopics)){
      const group=document.createElement('optgroup');group.label=t;
      subs.slice(1).forEach(s=>group.appendChild(new Option(s.text,s.val)));
      select.appendChild(group);
    }
  }else{
    const list=preciseSubtopics[topic]||[{val:'',text:`All ${topic} areas`}];
    list.forEach(s=>select.add(new Option(s.text,s.val)));
  }
}

function updateAvailable(){
  if(!bank)return;
  const prefs=Object.fromEntries(['topic','subtopic','difficulty','origin'].map(k=>[k,$('#'+k)?.value||'']));
  const n=available(bank.questions,prefs,$('#mode').value,state.attempts).length;
  $('#available').textContent=`${n} matching validated question${n===1?'':'s'}`;
  $('#start').disabled=!n;
}

function setView(next,focus=true){
  view=next;state.view=next;
  if(next==='practice'&&appMode==='exam'&&state.session?.mode.startsWith('exam'))startExamTimer();
  else stopExamTimer();
  save();render();
  if(focus){$('#main').focus();if(next==='home')window.scrollTo(0,0);}
}

function focusQuestion(){
  const target=$('.question');
  if(!target)return;
  $('#session-settings').open=false;
  const top=$('.masthead').offsetHeight+16;
  const main=$('#main');
  const fits=target.getBoundingClientRect().bottom-main.getBoundingClientRect().top<=innerHeight-top-16;
  const scrollTarget=fits?main:target;
  scrollTarget.style.scrollMarginTop=`${top}px`;
  target.focus({preventScroll:true});
  scrollTarget.scrollIntoView({block:'start'});
}

function setAppMode(mode,show=true){
  appMode=mode;
  $('#tab-mode-practice').classList.toggle('active',mode==='practice');
  $('#tab-mode-practice').setAttribute('aria-selected',String(mode==='practice'));
  $('#tab-mode-exam').classList.toggle('active',mode==='exam');
  $('#tab-mode-exam').setAttribute('aria-selected',String(mode==='exam'));
  $('#practice-panel').classList.toggle('hidden',mode!=='practice');
  $('#exam-panel').classList.toggle('hidden',mode!=='exam');

  if(mode==='exam'){
    if(!state.session||!state.session.mode.startsWith('exam')){
      // Reset any drafted answers when entering exam mode
      if(bank){
        bank.questions.forEach(q=>{
          if(state.drafts[q.id]?.selected){
            state.drafts[q.id]={notes:state.drafts[q.id].notes||'',selected:null,updatedAt:now()};
          }
        });
      }
      save();
    }
  }
  if(show)setView('practice');
}

function render(){
  const activeView=view==='practice'&&!state.session&&appMode==='practice'?'home':view;
  $$('[data-view]').forEach(el=>el.setAttribute('aria-pressed',String(el.dataset.view===activeView)));
  if(view==='home')renderHome();
  else if(view==='history')renderHistory();
  else if(appMode==='exam'&&state.session&&state.session.mode.startsWith('exam'))renderExamActive();
  else if(appMode==='exam'&&(!state.session||!state.session.mode.startsWith('exam')))renderExamOverview();
  else renderPractice();
  bindNotes();updateAvailable();
  if($('#global-save').classList.contains('failed'))$$('.save-status').forEach(el=>{el.textContent='Not saved — export a backup';el.classList.add('failed');});
}

function startSession(ids,mode){
  stopExamTimer();
  const q=question(ids[0]);
  state.session={queue:ids,index:0,order:shuffle(q.options.map(o=>o.id)),mode,attemptId:null,attemptIds:[],examFlags:{}};
  setAppMode('practice',false);
  setView('practice',false);
  focusQuestion();
}

function retry(id){startSession([id],'retry');}

// =================== PRACTICE MODE ===================
function renderHome(){
    const scored=bank.questions.filter(q=>q.status==='validated'),latest=latestAttempts(state.attempts);
    const revisit=[...latest.values()].filter(a=>a.outcome!=='correct').length;
    $('#main').innerHTML=`<section class="welcome study-hero"><span class="eyebrow">YOUR STUDY SPACE</span><h2>Think it through.<br>Build your confidence.</h2><div class="actions"><button class="primary" id="welcome-start">${state.attempts.length?'Keep practising':'Start practising'} <span aria-hidden="true">→</span></button><button id="welcome-exam">Launch Exam Mode ⏱️</button></div></section><div class="study-stats" aria-label="Study overview"><div><strong>${state.attempts.length}</strong><span>Attempts logged</span></div><div><strong>${revisit}</strong><span>Questions to revisit</span></div><div><strong>${scored.length}</strong><span>Validated questions</span></div></div><section class="topic-section"><div class="section-heading"><h2>Find your focus</h2></div><div class="topic-grid">${[...new Set(scored.map(q=>q.topic))].map((topic,index)=>{const pool=scored.filter(q=>q.topic===topic),seen=pool.filter(q=>latest.has(q.id)).length;return `<button class="topic-card" data-topic="${h(topic)}"><span class="topic-number" aria-hidden="true">0${index+1}</span><span class="topic-title">${h(topic)}</span><span class="topic-count">${pool.length} questions · ${seen} explored</span><span class="topic-track" aria-hidden="true"><span style="width:${100*seen/pool.length}%"></span></span><span class="topic-arrow" aria-hidden="true">→</span></button>`;}).join('')}</div></section>`;
    if(state.session)$('#welcome-start').textContent='Resume session →';
    $('#welcome-start').onclick=()=>state.session?$('#nav-study').click():$('#setup').requestSubmit();
    $('#welcome-exam').onclick=()=>setAppMode('exam');
    $$('[data-topic]').forEach(el=>el.onclick=()=>{
      $('#topic').value=el.dataset.topic;populateSubtopics(el.dataset.topic);$('#subtopic').value='';$('#difficulty').value='';$('#setup').requestSubmit();
    });
}

function renderPractice(){
  const session=state.session;
  if(!session){renderHome();return;}

  const q=question(session.queue[session.index]);
  const attempt=state.attempts.find(a=>a.id===session.attemptId);
  const d=state.drafts[q.id];
  const completed=session.attemptIds.length;

  $('#main').innerHTML=`
    <div class="session-head">
      <div>
        <h2>Question ${session.index+1} of ${session.queue.length}</h2>
        <p class="muted">${h(session.mode==='missed'?'Review missed / unknown':session.mode==='retry'?'Retry':'Practice mode')} · ${completed} submitted in this session</p>
      </div>
      <button id="end-session">End session & see results</button>
    </div>
    <progress max="${session.queue.length}" value="${session.index+(attempt?1:0)}" aria-label="Session progress"></progress>
    <div class="question-layout">
      <article class="question" tabindex="-1" aria-label="Current question">
        ${q.scenario?`<div class="scenario">${format(q.scenario)}</div>`:''}
        <div class="prompt" id="question-prompt">${format(q.prompt.replace(/^\d+(?:\.\d+)?\.?\s*(?:\(\d+ marks?\)\s*)?/,''))}</div>
        ${q.assumptions.length?`<details class="assumptions"><summary>Assumptions for this question</summary>${q.assumptions.map(s=>`<p>${h(s)}</p>`).join('')}</details>`:''}
        <form id="answer-form">
          <fieldset class="options" ${attempt?'disabled':''}>
            <legend class="visually-hidden">Choose one answer</legend>
            ${session.order.map((id,idx)=>{
              const o=q.options.find(o=>o.id===id);
              const isChecked=(attempt?attempt.optionId:d?.selected)===id;
              return `<label class="option ${attempt&&isChecked?(id===q.correctOptionId?'correct-option':'wrong-option'):''}">
                <input type="radio" name="answer" value="${h(id)}" ${isChecked?'checked':''}>
                <span><strong>${h(shownLabel(session.order,id))}.</strong> ${h(optionText(o))}</span>
                ${attempt&&isChecked?`<small class="answer-result">${id===q.correctOptionId?'Correct':'Incorrect'}</small>`:''}
              </label>`;
            }).join('')}
          </fieldset>
          <p id="answer-error" class="danger" role="alert"></p>
          <div class="action-bar">
            <button type="button" id="previous-question" ${session.index===0?'disabled':''}>Previous</button>
            <div class="action-buttons">
              ${!attempt?`<button type="button" id="unknown" class="quiet">Skip</button>`:''}
              <button class="primary" type="submit" id="btn-action" ${!attempt&&!d?.selected?'disabled':''}>
                ${!attempt?'Check answer':(session.index+1<session.queue.length?'Next question →':'See results')}
              </button>
            </div>
          </div>
        </form>
      </article>
      <aside id="feedback" class="explanation-panel" aria-label="Question explanation">${attempt?feedback(q,attempt):'<h3>Explanation</h3><p class="muted">Not checked</p>'}</aside>
      <details id="notebook" class="notes-panel optional-notes" ${d?.notes?'open':''}>
        <summary>Calculations & notes <span class="muted">Optional</span></summary>
        ${notes(q)}
        ${attempt?`<details><summary>Notes saved with this attempt</summary><div class="snapshot">${h(attempt.notesSnapshot||'No notes at submission.')}</div><p class="muted">${h(new Date(attempt.timestamp).toLocaleString())}</p></details>`:''}
      </details>
    </div>
  `;

  $$('input[name=answer]').forEach(el=>el.addEventListener('change',()=>{
    state.drafts[q.id]={notes:state.drafts[q.id]?.notes||'',selected:el.value,updatedAt:now()};
    save();
    if(!attempt&&$('#btn-action'))$('#btn-action').disabled=false;
  }));

  $('#answer-form').onsubmit=e=>{
    e.preventDefault();
    if(!attempt){
      const selected=document.querySelector('input[name=answer]:checked');
      if(!selected){$('#answer-error').textContent='Choose an answer or Skip.';return;}
      submit(q,selected.value);
    }else{
      advanceQuestion();
    }
  };

  $('#unknown')?.addEventListener('click',()=>submit(q,null));
  $('#previous-question').onclick=()=>{if(session.index>0)goToQuestion(session.index-1);};
  $('#end-session').onclick=showResults;
  bindFeedback(q,attempt);
}

function submit(q,optionId){
  if(state.session.attemptId)return;
  const attempt=makeAttempt(q,optionId,state.drafts[q.id]?.notes||'',now(),crypto.randomUUID(),bank.bankVersion);
  state.attempts.push(attempt);
  state.session.attemptId=attempt.id;
  state.session.attemptIds.push(attempt.id);
  save();
  render();
  $('#feedback-heading')?.focus();
}

function feedback(q,a){
  const correct=q.options.find(o=>o.id===q.correctOptionId),selected=q.options.find(o=>o.id===a.optionId),suggested=a.outcome!=='correct'?followup(q,a,bank.questions,state.attempts):null;
  const order=state.session.order;
  return `
    <section class="feedback" data-outcome="${h(a.outcome)}">
      <h3 class="outcome-${h(a.outcome)}" id="feedback-heading" tabindex="-1">${label[a.outcome]}</h3>
      <p><strong>Correct answer:</strong> ${h(shownLabel(order,correct.id))}. ${h(optionText(correct))}</p>
      <p>${h(q.explanation)}</p>
      ${q.workedCalculation?`<div class="calculation">${h(q.workedCalculation)}</div>`:''}
      ${a.outcome==='incorrect'?`<p><strong>Why your choice is wrong:</strong> ${h(selected.explanation)}</p>`:''}
      <details><summary>Explain all answer options</summary><ul>${order.map(id=>{const o=q.options.find(o=>o.id===id);return `<li><strong>${h(shownLabel(order,id))}. ${h(optionText(o))}</strong>${o.id===correct.id?' — correct':''}<br>${h(o.explanation)}</li>`;}).join('')}</ul></details>
      ${suggested?`<div class="actions"><button id="followup" data-question="${h(suggested.id)}">Try relevant follow-up question</button></div>`:''}
    </section>
  `;
}

function bindFeedback(q,attempt){
  if(!attempt)return;
  $('#followup')?.addEventListener('click',e=>{
    const id=e.currentTarget.dataset.question;const s=state.session;
    const existing=s.queue.indexOf(id);
    if(existing<0)s.queue.splice(s.index+1,0,id);
    goToQuestion(existing<0?s.index+1:existing);
  });
}

function advanceQuestion(){
  const s=state.session;
  if(s.index+1>=s.queue.length){showResults();return;}
  goToQuestion(s.index+1);
}

function goToQuestion(index){
  const s=state.session;
  s.questionOrders=s.questionOrders||{};
  s.questionOrders[s.queue[s.index]]=[...s.order];
  s.index=index;
  const id=s.queue[index];
  s.attemptId=state.attempts.find(a=>a.questionId===id&&s.attemptIds.includes(a.id))?.id||null;
  s.order=s.questionOrders[id]||shuffle(question(id).options.map(o=>o.id));
  save();render();focusQuestion();
}

// =================== EXAM MODE ===================
function renderExamOverview(){
  stopExamTimer();
  const selectedPart=document.querySelector('input[name="exam-part"]:checked')?.value||'full';
  const selectedTopic=$('#exam-topic-select')?.value||'Financial Reporting';

  let config={
    title:'Whole Exam (Both Parts)',
    duration:'90 minutes',
    exerciseCount:'50 exercises',
    marks:'90 marks total',
    description:'Full-length mock exam replicating official past ACA exam papers across all course modules.',
    modules:[
      {title:'Part 1: Accounting & Auditing (45m · 45 Marks)',desc:'30 exercises: Financial Reporting & Consolidation (30 marks) + Auditing (15 marks).'},
      {title:'Part 2: Controlling (45m · 45 Marks)',desc:'20 exercises across management accounting, budgeting, variances, capital budgeting and performance management.'}
    ]
  };

  if(selectedPart==='part1'){
    config={
      title:'Part 1: Accounting & Auditing',
      duration:'45 minutes',
      exerciseCount:'30 exercises',
      marks:'45 marks total',
      description:'Replication of Part 1 from official past ACA exam papers. Strictly 45 minutes.',
      modules:[
        {title:'Accounting (30 Marks · 20 Exercises)',desc:'Financial reporting standards, deferred taxes, leases, revenue recognition & consolidated balance sheets.'},
        {title:'Auditing (15 Marks · 10 Exercises)',desc:'Audit risk assessment, internal controls, substantive testing procedures & audit opinion formulation.'}
      ]
    };
  }else if(selectedPart==='part2'){
    config={
      title:'Part 2: Controlling',
      duration:'45 minutes',
      exerciseCount:'~20 exercises',
      marks:'45 marks total',
      description:'Replication of Part 2 from official past ACA exam papers. Strictly 45 minutes.',
      modules:[
        {title:'Management Accounting & Cost Systems (30 Marks)',desc:'Absorption vs. variable costing, contribution margin, breakeven analysis & cost allocations.'},
        {title:'Budgeting, Variances & Investment Decisions',desc:'Operating budgets, variance analysis, capital budgeting, balanced scorecards and performance measures.'}
      ]
    };
  }else if(selectedPart==='topic'){
    const count=bank?bank.questions.filter(q=>q.status==='validated'&&q.topic===selectedTopic).length:0;
    config={
      title:`Topic Focus Exam: ${selectedTopic}`,
      duration:'45 minutes',
      exerciseCount:`${Math.min(20,count)} exercises`,
      marks:'45 marks total',
      description:`Intensive timed exam sitting focused exclusively on ${selectedTopic} under strict exam conditions.`,
      modules:[
        {title:`${selectedTopic} Focus (${Math.min(20,count)} Exercises)`,desc:`Simulated exam pool selected exclusively from validated ${selectedTopic} question bank (${count} questions available).`}
      ]
    };
  }

  $('#main').innerHTML=`
    <section class="welcome study-hero">
      <span class="eyebrow">CHOSEN EXAM CONFIGURATION</span>
      <h2>${h(config.title)}</h2>
      <p class="exam-lead">${h(config.description)}</p>
    </section>

    <div class="study-stats">
      <div><strong>${h(config.duration)}</strong><span>Duration</span></div>
      <div><strong>${h(config.exerciseCount)}</strong><span>Exercise count</span></div>
      <div><strong>${h(config.marks)}</strong><span>Total marks</span></div>
    </div>

    <section class="topic-section">
      <div class="section-heading">
        <h2>Syllabus Coverage for Selected Exam</h2>
        <p class="muted">Based directly on official past exam papers.</p>
      </div>
      <div class="topic-grid">
        ${config.modules.map((m,idx)=>`
          <div class="topic-card">
            <span class="topic-number">SECTION 0${idx+1}</span>
            <span class="topic-title">${h(m.title)}</span>
            <span class="topic-count">${h(m.desc)}</span>
          </div>
        `).join('')}
      </div>
    </section>

    <p class="muted">One correct answer per question. No deductions for incorrect answers.</p>
  `;
}

function launchExam(part,topic){
  let pool=[];
  let durationSeconds=45*60;
  let modeName='exam-part1';
  let examTopicName=null;

  if(part==='full'){
    const acct=shuffle(bank.questions.filter(q=>q.status==='validated'&&(q.topic==='Consolidated Statements'||q.topic==='Financial Reporting'))).slice(0,20);
    const audit=shuffle(bank.questions.filter(q=>q.status==='validated'&&q.topic==='Auditing')).slice(0,10);
    const controlling=shuffle(bank.questions.filter(q=>q.status==='validated'&&controllingTopics.includes(q.topic))).slice(0,20);
    pool=[...acct,...audit,...controlling].map(q=>q.id);
    durationSeconds=90*60;
    modeName='exam-full';
  }else if(part==='part1'){
    const acct=shuffle(bank.questions.filter(q=>q.status==='validated'&&(q.topic==='Consolidated Statements'||q.topic==='Financial Reporting'))).slice(0,20);
    const audit=shuffle(bank.questions.filter(q=>q.status==='validated'&&q.topic==='Auditing')).slice(0,10);
    pool=[...acct,...audit].map(q=>q.id);
    durationSeconds=45*60;
    modeName='exam-part1';
  }else if(part==='part2'){
    pool=shuffle(bank.questions.filter(q=>q.status==='validated'&&controllingTopics.includes(q.topic))).slice(0,20).map(q=>q.id);
    durationSeconds=45*60;
    modeName='exam-part2';
  }else if(part==='topic'){
    const chosenTopic=topic||$('#exam-topic-select')?.value||'Financial Reporting';
    examTopicName=chosenTopic;
    pool=shuffle(bank.questions.filter(q=>q.status==='validated'&&q.topic===chosenTopic)).slice(0,20).map(q=>q.id);
    durationSeconds=45*60;
    modeName='exam-topic';
  }

  if(!pool.length){
    alert('No validated questions found for this exam selection.');
    return;
  }

  // RESET ALL DRAFTS / ANSWERS FOR EXAM POOL
  pool.forEach(id=>{
    state.drafts[id]={notes:'',selected:null,updatedAt:now()};
  });

  const q=question(pool[0]);
  state.session={
    queue:pool,
    index:0,
    order:shuffle(q.options.map(o=>o.id)),
    mode:modeName,
    examTopic:examTopicName,
    attemptId:null,
    attemptIds:[],
    examInitialDuration:durationSeconds,
    examTimeRemaining:durationSeconds,
    examFlags:{}
  };
  setView('practice',false);
  focusQuestion();
}

function startExamTimer(){
  stopExamTimer();
  examTimerPaused=false;
  examTimerInterval=setInterval(()=>{
    if(!state.session||!state.session.mode.startsWith('exam'))return stopExamTimer();
    if(examTimerPaused)return;
    state.session.examTimeRemaining=Math.max(0,(state.session.examTimeRemaining||0)-1);
    const el=$('#exam-timer');
    if(el){
      const m=Math.floor(state.session.examTimeRemaining/60),s=state.session.examTimeRemaining%60;
      el.textContent=`${String(m).padStart(2,'0')}:${String(s).padStart(2,'0')}`;
    }
    if(state.session.examTimeRemaining<=0){
      stopExamTimer();
      alert('Time is up! Your exam will now be submitted.');
      finishExam();
    }
  },1000);
}

function stopExamTimer(){
  if(examTimerInterval){clearInterval(examTimerInterval);examTimerInterval=null;}
}

function toggleExamTimer(){
  examTimerPaused=!examTimerPaused;
  const btn=$('#timer-toggle-btn');
  if(btn)btn.textContent=examTimerPaused?'▶ Resume':'⏸ Pause';
}

function resetExamTimer(){
  if(!state.session||!state.session.mode.startsWith('exam'))return;
  const initial=state.session.examInitialDuration||(state.session.mode==='exam-full'?90*60:45*60);
  state.session.examTimeRemaining=initial;
  const m=Math.floor(initial/60),s=initial%60;
  const el=$('#exam-timer');
  if(el)el.textContent=`${String(m).padStart(2,'0')}:${String(s).padStart(2,'0')}`;
  save();
}

function cancelExam(){
  if(!state.session||!state.session.mode.startsWith('exam'))return;
  if(!confirm('Are you sure you want to cancel this exam sitting? All answered questions will be cleared, timer stopped, and no attempts will be logged.'))return;
  stopExamTimer();
  state.session.queue.forEach(id=>{
    state.drafts[id]={notes:'',selected:null,updatedAt:now()};
  });
  state.session=null;
  save();
  renderExamOverview();
  $('#main').focus();
}

function renderExamActive(){
  const s=state.session;
  const q=question(s.queue[s.index]);
  const d=state.drafts[q.id];
  const m=Math.floor((s.examTimeRemaining||0)/60),sec=(s.examTimeRemaining||0)%60;
  const isPart1=s.mode==='exam-part1',isPart2=s.mode==='exam-part2',isFull=s.mode==='exam-full';
  const examTitle=isPart1?'Part 1: Accounting & Auditing':isPart2?'Part 2: Controlling':isFull?'Whole Mock Exam':(s.examTopic?`Topic: ${s.examTopic}`:'Topic Exam');

  $('#main').innerHTML=`
    <div class="exam-banner">
      <div>
        <h2>Exam Mode — ${h(examTitle)}</h2>
        <p>Exercise ${s.index+1} of ${s.queue.length} · Single choice · No deduction for wrong answers</p>
      </div>
      <div class="exam-banner-controls">
        <div class="exam-timer-box">
          <span class="exam-timer-display" id="exam-timer">${String(m).padStart(2,'0')}:${String(sec).padStart(2,'0')}</span>
          <button id="timer-toggle-btn" class="exam-timer-toggle" type="button" title="Pause or resume timer">${examTimerPaused?'▶ Resume':'⏸ Pause'}</button>
          <button id="timer-reset-btn" class="exam-timer-toggle" type="button" title="Reset countdown timer">🔄 Reset Timer</button>
        </div>
        <button type="button" id="btn-banner-cancel-exam" class="exam-cancel-btn" title="Cancel this exam sitting">Cancel Exam ✕</button>
      </div>
    </div>
    <div class="palette-card">
      <div class="palette-header">
        <span>Exercise Matrix (${s.queue.length} exercises)</span>
        <div class="palette-legend">
          <span><span class="legend-dot" style="background:var(--green)"></span> Answered</span>
          <span><span class="review-flag" aria-hidden="true">⚑</span> Flagged</span>
          <span><span class="legend-dot" style="background:var(--line)"></span> Unanswered</span>
        </div>
      </div>
      <div class="palette-grid">
        ${s.queue.map((id,idx)=>{
          const ans=state.drafts[id]?.selected;
          const flg=s.examFlags?.[id];
          const cur=idx===s.index;
          return `<button type="button" class="palette-btn ${ans?'answered':''} ${cur?'current':''}" data-jump="${idx}" aria-label="Question ${idx+1}${flg?', flagged for review':''}${ans?', answered':''}" ${cur?'aria-current="step"':''}>${idx+1}${flg?'<span class="review-flag" aria-hidden="true">⚑</span>':''}</button>`;
        }).join('')}
      </div>
    </div>
    <div class="question-layout exam-question-layout">
      <article class="question" tabindex="-1" aria-label="Current question">
        <div class="exam-exercise-head">
          <div class="exam-exercise-title">
            <span class="exam-badge">Exercise ${s.index+1}</span>
            <span class="exam-marks">${q.marks?`(${q.marks} Marks)`:'(1–2 Marks)'}</span>
          </div>
          <button type="button" id="btn-flag" class="flag-btn ${s.examFlags?.[q.id]?'flagged':''}" aria-pressed="${Boolean(s.examFlags?.[q.id])}">
            ${s.examFlags?.[q.id]?'Flagged for review ⚑':'Flag for review ⚑'}
          </button>
        </div>
        ${q.scenario?`<div class="scenario">${format(q.scenario)}</div>`:''}
        <div class="prompt">${format(q.prompt.replace(/^\d+(?:\.\d+)?\.?\s*(?:\(\d+ marks?\)\s*)?/,''))}</div>
        <fieldset class="options">
          <legend class="visually-hidden">Choose one answer</legend>
          ${s.order.map(id=>{
            const o=q.options.find(o=>o.id===id);
            const isChecked=d?.selected===id;
            return `<label class="option">
              <input type="radio" name="exam-answer" value="${h(id)}" ${isChecked?'checked':''}>
              <span><strong>${h(shownLabel(s.order,id))}.</strong> ${h(optionText(o))}</span>
            </label>`;
          }).join('')}
        </fieldset>
        <div class="exam-nav-bar">
          <div class="exam-nav-left">
            <button type="button" id="btn-exam-prev" ${s.index===0?'disabled':''}>← Previous</button>
            <button type="button" id="btn-exam-cancel" class="quiet danger">Cancel Exam ✕</button>
          </div>
          <div class="exam-nav-right">
            <button type="button" id="btn-exam-finish" class="danger">End & Submit Exam</button>
            <button type="button" id="btn-exam-next" class="primary">${s.index+1<s.queue.length?'Next':'Finish'}</button>
          </div>
        </div>
      </article>
      <details id="notebook" class="notes-panel optional-notes" ${d?.notes?'open':''}>
        <summary>Calculations & notes <span class="muted">Optional</span></summary>
        ${notes(q)}
      </details>
    </div>
  `;

  $$('input[name=exam-answer]').forEach(el=>el.addEventListener('change',()=>{
    state.drafts[q.id]={notes:state.drafts[q.id]?.notes||'',selected:el.value,updatedAt:now()};
    save();
    render();
  }));

  $('#btn-flag').onclick=()=>{
    s.examFlags=s.examFlags||{};
    s.examFlags[q.id]=!s.examFlags[q.id];
    save();render();
  };

  $$('[data-jump]').forEach(btn=>btn.onclick=()=>{
    s.index=Number(btn.dataset.jump);
    s.order=shuffle(question(s.queue[s.index]).options.map(o=>o.id));
    save();render();focusQuestion();
  });

  $('#btn-exam-prev').onclick=()=>{
    if(s.index>0){s.index--;s.order=shuffle(question(s.queue[s.index]).options.map(o=>o.id));save();render();focusQuestion();}
  };

  $('#btn-exam-next').onclick=()=>{
    if(s.index+1<s.queue.length){s.index++;s.order=shuffle(question(s.queue[s.index]).options.map(o=>o.id));save();render();focusQuestion();}
    else finishExam();
  };

  $('#btn-exam-finish').onclick=finishExam;
  $('#timer-toggle-btn').onclick=toggleExamTimer;
  $('#timer-reset-btn').onclick=resetExamTimer;
  $('#btn-banner-cancel-exam').onclick=cancelExam;
  $('#btn-exam-cancel').onclick=cancelExam;
}

function finishExam(){
  const s=state.session;
  const answered=s.queue.filter(id=>state.drafts[id]?.selected).length;
  if(!confirm(`You answered ${answered} of ${s.queue.length} exercises. Ready to submit this exam?`))return;
  stopExamTimer();
  s.queue.forEach(id=>{
    const q=question(id);
    const chosen=state.drafts[id]?.selected||null;
    const attempt=makeAttempt(q,chosen,state.drafts[id]?.notes||'',now(),crypto.randomUUID(),bank.bankVersion);
    state.attempts.push(attempt);
    s.attemptIds.push(attempt.id);
  });
  save();
  showExamResults();
}

function showExamResults(){
  const s=state.session;
  const rows=state.attempts.filter(a=>s.attemptIds.includes(a.id));
  const correct=rows.filter(a=>a.outcome==='correct').length;
  const incorrect=rows.filter(a=>a.outcome==='incorrect').length;
  const unanswered=rows.length-correct-incorrect;
  const scorePct=rows.length?Math.round((correct/rows.length)*100):0;
  state.session=null;
  save();

  $('#main').innerHTML=`
    <section class="welcome">
      <span class="eyebrow">EXAM MODE RESULTS</span>
      <h2>Exam Score: ${correct} / ${rows.length} (${scorePct}%)</h2>
      <p>Passing benchmark is typically 50%. Wrong answers incurred zero deductions.</p>
      <div class="result-grid">
        <div><strong>${correct}</strong>Correct marks</div>
        <div><strong>${incorrect}</strong>Incorrect</div>
        <div><strong>${unanswered}</strong>Unanswered</div>
      </div>
      <div class="actions">
        <button class="primary" id="btn-exam-again">Take Another Exam</button>
        <button id="btn-exam-history">View Learning History</button>
      </div>
    </section>
    <section class="dashboard-section">
      <h3>Review Exam Exercises</h3>
      ${rows.map(a=>{
        const q=question(a.questionId);
        const correctOpt=q.options.find(o=>o.id===q.correctOptionId);
        const chosenOpt=q.options.find(o=>o.id===a.optionId);
        return `
          <details class="history-item">
            <summary><strong class="outcome-${h(a.outcome)}">${label[a.outcome]}</strong> — ${h(q.topic)} · ${h(q.prompt.slice(0,90))}…</summary>
            ${q.scenario?`<div class="scenario">${format(q.scenario)}</div>`:''}
            <div class="prompt">${format(q.prompt)}</div>
            <p><strong>Your answer:</strong> ${chosenOpt?h(optionText(chosenOpt)):'Unanswered'}</p>
            <p><strong>Correct answer:</strong> ${h(optionText(correctOpt))}</p>
            <div class="options" aria-label="Reviewed answer options">${q.options.map(o=>`<div class="option ${o.id===a.optionId?(o.id===q.correctOptionId?'correct-option':'wrong-option'):''}"><span>${h(optionText(o))}${o.id===a.optionId?' (your answer)':''}</span>${o.id===a.optionId?`<small class="answer-result">${o.id===q.correctOptionId?'Correct':'Incorrect'}</small>`:''}</div>`).join('')}</div>
            <p>${h(q.explanation)}</p>
            ${q.workedCalculation?`<div class="calculation">${h(q.workedCalculation)}</div>`:''}
          </details>
        `;
      }).join('')}
    </section>
  `;
  $('#btn-exam-again').onclick=()=>setAppMode('exam');
  $('#btn-exam-history').onclick=()=>setView('history');
}

// =================== RESULTS & HISTORY ===================
function showResults(){
  const session=state.session;
  const rows=state.attempts.filter(a=>session.attemptIds.includes(a.id));
  const correct=rows.filter(a=>a.outcome==='correct').length;
  const incorrect=rows.filter(a=>a.outcome==='incorrect').length;
  const unknown=rows.length-correct-incorrect;
  state.session=null;
  save();
  $('#main').innerHTML=`
    <section class="welcome">
      <h2>Session Results</h2>
      <p>${rows.length} submitted of ${session.queue.length} questions.</p>
      <div class="result-grid">
        <div><strong>${correct}</strong>Correct</div>
        <div><strong>${incorrect}</strong>Incorrect</div>
        <div><strong>${unknown}</strong>I don’t know</div>
      </div>
      <p>Accuracy among answered attempts: <strong>${correct+incorrect?Math.round(100*correct/(correct+incorrect))+'%':'No answered attempts'}</strong>.</p>
      <div class="actions">
        <button class="primary" id="again">Start Another Session</button>
        <button id="results-history">See Learning History</button>
      </div>
    </section>
  `;
  $('#again').onclick=()=>$('#setup').requestSubmit();
  $('#results-history').onclick=()=>setView('history');
  $('#main').focus();
  updateAvailable();
}

function renderHistory(){
  stopExamTimer();
  const latest=latestAttempts(state.attempts);
  const retryable=bank.questions.filter(q=>q.status==='validated'&&latest.has(q.id)&&latest.get(q.id).outcome!=='correct');
  const tags={};state.attempts.forEach(a=>{if(a.misconception)tags[a.misconception]=(tags[a.misconception]||0)+1;});
  const touched=bank.questions.filter(q=>state.drafts[q.id]||state.attempts.some(a=>a.questionId===q.id));

  $('#main').innerHTML=`
    <h2>Learning History</h2>
    <p class="muted">All submitted attempts are retained. Repeated attempts count separately and help reinforce difficult topics.</p>
    <div class="table-wrap">
      <table>
        <caption>Attempts by Topic</caption>
        <thead>
          <tr><th scope="col">Topic</th><th scope="col">Attempts</th><th scope="col">Correct</th><th scope="col">Incorrect</th><th scope="col">Unknown</th><th scope="col">Accuracy</th></tr>
        </thead>
        <tbody>
          ${topicStats(bank.questions,state.attempts).map(s=>`<tr><th scope="row">${h(s.topic)}</th><td>${s.total}</td><td>${s.correct}</td><td>${s.incorrect}</td><td>${s.unknown}</td><td>${s.accuracy===null?'—':s.accuracy+'%'}</td></tr>`).join('')}
        </tbody>
      </table>
    </div>
    <section class="dashboard-section">
      <h3>Questions to Revisit (${retryable.length})</h3>
      ${retryable.length?retryable.map(q=>`<div class="history-item"><p><strong>${h(q.topic)} · ${h(q.prompt.slice(0,90))}…</strong> — ${label[latest.get(q.id).outcome]}</p><button data-retry="${h(q.id)}">Retry question</button></div>`).join(''):'<p class="empty">No outstanding missed questions. Great work!</p>'}
    </section>
    <section class="dashboard-section">
      <h3>Saved Notes & Submissions (${touched.length} questions)</h3>
      ${touched.length?touched.map(q=>{
        const rows=state.attempts.filter(a=>a.questionId===q.id).slice().reverse();
        return `<details class="history-item">
          <summary>${h(q.topic)} — ${rows.length} attempt${rows.length===1?'':'s'}</summary>
          ${q.scenario?`<div class="scenario">${format(q.scenario)}</div>`:''}
          <div class="scenario">${format(q.prompt)}</div>
          ${notes(q,true)}
          <button data-retry="${h(q.id)}">Retry as new attempt</button>
          ${rows.map(a=>`<details><summary>${label[a.outcome]} · ${h(new Date(a.timestamp).toLocaleString())}</summary><p>Selected: ${h(q.options.find(o=>o.id===a.optionId)?.text||'I don’t know')}</p><div class="snapshot">${h(a.notesSnapshot||'No notes at submission.')}</div></details>`).join('')}
        </details>`;
      }).join(''):'<p class="muted">Your question notes and submissions will appear here.</p>'}
    </section>
  `;
  $$('[data-retry]').forEach(el=>el.onclick=()=>retry(el.dataset.retry));
}

function download(text,name){
  const url=URL.createObjectURL(new Blob([text],{type:'application/json'}));
  const a=document.createElement('a');a.href=url;a.download=name;a.click();
  setTimeout(()=>URL.revokeObjectURL(url),1000);
}

async function init(){
  try{
    initTheme();
    $('#theme-toggle').onclick=toggleTheme;
    if(matchMedia('(max-width: 760px)').matches)$('#session-settings').open=false;

    const response=await fetch('./content/questions.json');
    if(!response.ok)throw new Error('Question data could not be loaded.');
    bank=await response.json();
    state=emptyState(bank.bankVersion);

    loadProgress();

    // The source filter is no longer shown in the interface. Older saved
    // preferences could leave it set to "generated", silently hiding every
    // original exam-bank question (including Budgeting and Variances).
    state.preferences.origin='';
    $('#origin').value='';

    view=state.view;

    // Populate topics
    const topics=[...new Set(bank.questions.filter(q=>q.status==='validated').map(q=>q.topic))].sort();
    topics.forEach(t=>{
      for(const select of [$('#topic'),$('#exam-topic-select')]){
        if(![...select.options].some(o=>o.value===t))select.add(new Option(t,t));
      }
      if(!preciseSubtopics[t])preciseSubtopics[t]=[
        {val:'',text:`All ${t} areas`},
        ...[...new Set(bank.questions.filter(q=>q.status==='validated'&&q.topic===t).map(q=>q.subtopic))].sort().map(s=>({val:s,text:s}))
      ];
    });
    populateSubtopics(state.preferences.topic||'');

    for(const key of ['topic','difficulty']){
      if($('#'+key)&&state.preferences[key])$('#'+key).value=state.preferences[key];
    }
    if(state.preferences.subtopic)$('#subtopic').value=state.preferences.subtopic;

    // Single Mode Pill Selector
    $('#tab-mode-practice').onclick=()=>setAppMode('practice');
    $('#tab-mode-exam').onclick=()=>setAppMode('exam');

    // Slider
    $('#length-slider').oninput=e=>{
      const val=e.target.value;
      $('#slider-badge').textContent=`${val} questions`;
      e.target.setAttribute('aria-valuetext',`${val} questions`);
      $('#length').value=val;
      updateAvailable();
    };

    // Topic change updates subtopics precisely
    $('#topic').onchange=()=>{
      populateSubtopics($('#topic').value);
      state.preferences.topic=$('#topic').value;
      state.preferences.subtopic=$('#subtopic').value;
      save();updateAvailable();
    };

    $('#subtopic').onchange=()=>{
      state.preferences.subtopic=$('#subtopic').value;
      save();updateAvailable();
    };

    $('#difficulty').onchange=()=>{
      state.preferences.difficulty=$('#difficulty').value;
      save();updateAvailable();
    };

    $('#setup').onsubmit=e=>{
      e.preventDefault();
      const prefs=Object.fromEntries(['topic','subtopic','difficulty','origin'].map(k=>[k,$('#'+k)?.value||'']));
      state.preferences=prefs;
      const pool=shuffle(available(bank.questions,prefs,'mixed',state.attempts)).map(q=>q.id);
      if(!pool.length){notify('No questions match these filters. Try selecting All topics.');return;}
      const length=Number($('#length-slider')?.value||$('#length')?.value||15);
      startSession(pool.slice(0,length),'mixed');
    };

    // Exam start button: explicit start from left pane!
    $('#start-exam').onclick=()=>{
      const selectedPart=document.querySelector('input[name="exam-part"]:checked')?.value||'full';
      const selectedTopic=$('#exam-topic-select')?.value||'Financial Reporting';
      launchExam(selectedPart,selectedTopic);
    };

    $$('input[name="exam-part"]').forEach(el=>el.addEventListener('change',()=>{
      const isTopic=el.value==='topic';
      $('#exam-topic-select-wrap')?.classList.toggle('hidden',!isTopic);
      if(appMode==='exam'&&(!state.session||!state.session.mode.startsWith('exam'))){
        renderExamOverview();
      }
    }));

    $('#exam-topic-select')?.addEventListener('change',()=>{
      if(appMode==='exam'&&(!state.session||!state.session.mode.startsWith('exam'))){
        renderExamOverview();
      }
    });

    // Tax focus legacy hook
    $('#tax-focus').onclick=()=>{
      $('#topic').value='Financial Reporting';
      populateSubtopics('Financial Reporting');
      $('#subtopic').value='Deferred taxes';
      $('#difficulty').value='';
      $('#setup').requestSubmit();
    };

    // Navigation
    $('#nav-home').onclick=()=>setView('home');
    $('#brand-home').onclick=()=>setView('home');
    $('#nav-study').onclick=()=>{
      if(state.session)setAppMode(state.session.mode.startsWith('exam')?'exam':'practice',false);
      setView('practice',!state.session);focusQuestion();
    };
    $('#nav-history').onclick=()=>setView('history');

    // Export/import
    $('#export').onclick=()=>download(JSON.stringify({...state,exportedAt:now()},null,2),`aca-backup-${now().slice(0,10)}.json`);
    $('#import').onchange=async e=>{
      const file=e.target.files[0];if(!file)return;
      try{
        if(file.size>8*1024*1024)throw new Error('Backup is larger than 8 MB.');
        pendingImport=validateBackup(JSON.parse(await file.text()),bank);
        $('#import-summary').textContent=`This backup contains ${pendingImport.attempts.length} attempts and ${Object.keys(pendingImport.drafts).length} question drafts.`;
        $('#import-dialog').returnValue='cancel';
        $('#import-dialog').showModal();
      }catch(error){notify(error.message);}finally{e.target.value='';}
    };

    $('#import-dialog').onclose=()=>{
      if($('#import-dialog').returnValue==='confirm'&&pendingImport){
        try{
          state=mergeBackups(state,pendingImport);
          storageBlocked=false;unreadable=null;save();render();
          notify('Backup merged successfully.');
        }catch(error){notify(error.message);}
      }pendingImport=null;
    };

    $('#reset').onclick=()=>{$('#reset-dialog').returnValue='cancel';$('#reset-dialog').showModal();};
    $('#reset-dialog').onclose=()=>{
      if($('#reset-dialog').returnValue==='confirm'){
        if(activeUser){notify('Sign out to reset guest data. Account history is retained.');return;}
        try{localStorage.removeItem(storageKey);}catch{notify('Browser storage could not be reset.');return;}
        state=emptyState(bank.bankVersion);storageBlocked=false;unreadable=null;view='practice';
        save();render();notify('Study data has been reset in this browser.');
      }
    };

    if(state.session?.mode.startsWith('exam')){setAppMode('exam',false);if(view==='practice')startExamTimer();}
    render();
    focusQuestion();
    if(!storageBlocked)save();
    void initCloud();
  }catch(error){
    $('#main').innerHTML=`<h2>Unable to launch practice</h2><p>${h(error.message)}</p>`;
  }
}

// Global keyboard shortcuts (Enter to check/advance, 1-5 / A-E to select)
document.addEventListener('pointerdown',e=>{
  const button=e.target.closest('button.primary:not(:disabled)');
  if(!button||matchMedia('(prefers-reduced-motion: reduce)').matches)return;
  const rect=button.getBoundingClientRect(),size=Math.max(rect.width,rect.height)*2;
  const ripple=document.createElement('span');ripple.className='button-ripple';ripple.setAttribute('aria-hidden','true');
  Object.assign(ripple.style,{width:`${size}px`,height:`${size}px`,left:`${e.clientX-rect.left}px`,top:`${e.clientY-rect.top}px`});
  button.append(ripple);setTimeout(()=>ripple.remove(),550);
},{passive:true});

document.addEventListener('keydown',e=>{
  if(e.defaultPrevented||e.target.closest('input,textarea,select,button,summary,[contenteditable="true"]'))return;
  if(view!=='practice'||!state.session)return;
  if(e.key==='Enter'){
    const btn=$('#btn-action');
    if(btn&&!btn.disabled&&!btn.classList.contains('visually-hidden')){
      btn.click();
    }
  }else if(!state.session.attemptId&&!state.session.mode.startsWith('exam')){
    const key=e.key.toLowerCase();
    const map={'1':0,'2':1,'3':2,'4':3,'5':4,'a':0,'b':1,'c':2,'d':3,'e':4};
    if(map[key]!==undefined){
      const radios=$$('input[name=answer]');
      if(radios[map[key]]){
        radios[map[key]].checked=true;
        radios[map[key]].dispatchEvent(new Event('change'));
      }
    }
  }
});

init();
