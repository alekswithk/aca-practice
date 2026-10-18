import {STORAGE_KEY,emptyState,shuffle,makeAttempt,grade,available,followup,topicStats,latestAttempts,validateBackup,mergeBackups} from './core.mjs';

const $=s=>document.querySelector(s);
const $$=s=>document.querySelectorAll(s);
const h=s=>String(s??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const optionText=o=>o.text.replace(/None of the above(?: answers)?/gi,'None of the other answers').replace(/All of the above/gi,'All of the other answers');
const root=document.documentElement;
root.dataset.input='keyboard';
document.addEventListener('keydown',()=>{if(root.dataset.input!=='keyboard')root.dataset.input='keyboard';});
document.addEventListener('pointerdown',()=>{if(root.dataset.input!=='pointer')root.dataset.input='pointer';},{passive:true});

const label={correct:'Correct',incorrect:'Incorrect',unknown:'I don’t know'};
let bank,state,storageBlocked=false,unreadable=null,pendingImport=null,view='practice';
let appMode='practice'; // 'practice' or 'exam'
let examTimerInterval=null;
let examTimerPaused=false;

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
  ]
};

function initTheme(){
  const saved=localStorage.getItem('aca_theme');
  const prefersDark=window.matchMedia&&window.matchMedia('(prefers-color-scheme: dark)').matches;
  const isDark=saved==='dark'||(!saved&&prefersDark);
  if(isDark)root.classList.add('dark');else root.classList.remove('dark');
  $('#theme-toggle').setAttribute('aria-checked',String(isDark));
}
function toggleTheme(){
  const isDark=root.classList.toggle('dark');
  localStorage.setItem('aca_theme',isDark?'dark':'light');
  $('#theme-toggle').setAttribute('aria-checked',String(isDark));
}

function notify(message){
  $('#notice').textContent=message;$('#notice').hidden=false;
  if(unreadable&&storageBlocked){const button=document.createElement('button');button.textContent='Download unreadable data';button.onclick=()=>download(unreadable,'aca-recovery.json');$('#notice').append(' ',button);}
}

function save(){
  try{
    if(storageBlocked)throw new Error('Existing data needs recovery.');
    localStorage.setItem(STORAGE_KEY,JSON.stringify(state));
    $('#global-save').textContent='Saved in this browser';$('#global-save').classList.remove('failed');
    $$('.save-status').forEach(el=>{el.textContent='Saved in this browser';el.classList.remove('failed');});
    return true;
  }catch(error){
    $('#global-save').textContent='Not saved — export a backup';$('#global-save').classList.add('failed');
    $$('.save-status').forEach(el=>{el.textContent='Not saved — export a backup';el.classList.add('failed');});
    notify('Browser saving is unavailable, full or paused. Keep this page open and export JSON to preserve your current work.');
    return false;
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
  $$('textarea[data-notes]').forEach(el=>el.addEventListener('input',()=>{
    const id=el.dataset.notes;const prev=state.drafts[id]||{selected:null};state.drafts[id]={...prev,notes:el.value,updatedAt:now()};save();
  }));
}

function notes(q,compact=false){
  const d=state.drafts[q.id];const ident=`notes-${q.id}`;
  return `<div class="notes-panel"><label for="${ident}">Calculations / reasoning / notes</label><textarea id="${ident}" data-notes="${h(q.id)}" maxlength="1000000" ${compact?'class="review-notes"':''} placeholder="Write your formulas, steps and assumptions here…">${h(d?.notes||'')}</textarea><p class="save-status" role="status">${storageBlocked?'Not saved — export a backup':'Saved drafts stay in this browser'}</p><p class="notes-help">${q.status==='review'?'You can save a question note.':'Submitting saves a copy of these notes with the attempt.'}</p></div>`;
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
  view=next;state.view=next;save();render();if(focus)$('#main').focus();
}

function setAppMode(mode){
  appMode=mode;
  $('#tab-mode-practice').classList.toggle('active',mode==='practice');
  $('#tab-mode-practice').setAttribute('aria-selected',String(mode==='practice'));
  $('#tab-mode-exam').classList.toggle('active',mode==='exam');
  $('#tab-mode-exam').setAttribute('aria-selected',String(mode==='exam'));
  $('#practice-panel').classList.toggle('hidden',mode!=='practice');
  $('#exam-panel').classList.toggle('hidden',mode!=='exam');

  // When switching to Exam Mode, do NOT start timer automatically!
  if(mode==='exam'&&(!state.session||!state.session.mode.startsWith('exam'))){
    renderExamOverview();
  }else if(mode==='practice'&&state.session&&state.session.mode.startsWith('exam')){
    stopExamTimer();
    renderPractice();
  }
}

function render(){
  $$('[data-view]').forEach(el=>el.setAttribute('aria-pressed',String(el.dataset.view===view)));
  if(view==='history')renderHistory();
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
  setView('practice');
}

function retry(id){startSession([id],'retry');}

// =================== PRACTICE MODE ===================
function renderPractice(){
  const session=state.session;
  if(!session){
    const scored=bank.questions.filter(q=>q.status==='validated'),latest=latestAttempts(state.attempts);
    const revisit=[...latest.values()].filter(a=>a.outcome!=='correct').length;
    $('#main').innerHTML=`<section class="welcome study-hero"><span class="eyebrow">YOUR STUDY SPACE</span><h2>Think it through.<br>Build your confidence.</h2><p>Work through scenarios, keep calculations in your notebook, and learn from step-by-step worked solutions.</p><div class="actions"><button class="primary" id="welcome-start">${state.attempts.length?'Keep practising':'Start practising'} <span aria-hidden="true">→</span></button><button id="welcome-exam">Launch Exam Mode ⏱️</button></div></section><div class="study-stats" aria-label="Study overview"><div><strong>${state.attempts.length}</strong><span>Attempts logged</span></div><div><strong>${revisit}</strong><span>Questions to revisit</span></div><div><strong>${scored.length}</strong><span>Validated questions</span></div></div><section class="topic-section"><div class="section-heading"><h2>Find your focus</h2><p class="muted">Choose a topic to jump straight in.</p></div><div class="topic-grid">${[...new Set(scored.map(q=>q.topic))].map((topic,index)=>{const pool=scored.filter(q=>q.topic===topic),seen=pool.filter(q=>latest.has(q.id)).length;return `<button class="topic-card" data-topic="${h(topic)}"><span class="topic-number" aria-hidden="true">0${index+1}</span><span class="topic-title">${h(topic)}</span><span class="topic-count">${pool.length} questions · ${seen} explored</span><span class="topic-track" aria-hidden="true"><span style="width:${100*seen/pool.length}%"></span></span><span class="topic-arrow" aria-hidden="true">→</span></button>`;}).join('')}</div></section>`;
    $('#welcome-start').onclick=()=>$('#setup').requestSubmit();
    $('#welcome-exam').onclick=()=>setAppMode('exam');
    $$('[data-topic]').forEach(el=>el.onclick=()=>{
      $('#topic').value=el.dataset.topic;populateSubtopics(el.dataset.topic);$('#subtopic').value='';$('#difficulty').value='';$('#setup').requestSubmit();
    });
    return;
  }

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
      <article class="question">
        ${q.scenario?`<div class="scenario">${format(q.scenario)}</div>`:''}
        <div class="prompt" id="question-prompt">${format(q.prompt.replace(/^\d+(?:\.\d+)?\.?\s*(?:\(\d+ marks?\)\s*)?/,''))}</div>
        ${q.assumptions.length?`<details class="assumptions"><summary>Assumptions for this question</summary>${q.assumptions.map(s=>`<p>${h(s)}</p>`).join('')}</details>`:''}
        <form id="answer-form">
          <fieldset class="options" ${attempt?'disabled':''}>
            <legend class="visually-hidden">Choose one answer</legend>
            ${session.order.map((id,idx)=>{
              const o=q.options.find(o=>o.id===id);
              const isChecked=(attempt?attempt.optionId:d?.selected)===id;
              return `<label class="option ${attempt&&id===q.correctOptionId?'correct-option':''} ${attempt?.outcome==='incorrect'&&id===attempt.optionId?'wrong-option':''}">
                <input type="radio" name="answer" value="${h(id)}" ${isChecked?'checked':''}>
                <span><strong>${h(o.id.toUpperCase())}.</strong> ${h(optionText(o))}</span>
              </label>`;
            }).join('')}
          </fieldset>
          <p id="answer-error" class="danger" role="alert"></p>
          <div class="action-bar">
            <span class="action-hint">${!attempt?'Select an answer, then press Enter or click Check.':'Press Enter to advance to the next question.'}</span>
            <div class="action-buttons">
              ${!attempt?`<button type="button" id="unknown" class="quiet">I don’t know / Skip</button>`:''}
              <button class="primary" type="submit" id="btn-action" ${!attempt&&!d?.selected?'disabled':''}>
                ${!attempt?'Check answer':(session.index+1<session.queue.length?'Next question →':'See results')}
              </button>
            </div>
          </div>
        </form>
        <div id="feedback">${attempt?feedback(q,attempt):''}</div>
      </article>
      <aside id="notebook" class="notes-panel" aria-label="Question notebook">
        ${notes(q)}
        ${attempt?`<details><summary>Notes saved with this attempt</summary><div class="snapshot">${h(attempt.notesSnapshot||'No notes at submission.')}</div><p class="muted">${h(new Date(attempt.timestamp).toLocaleString())}</p></details>`:''}
      </aside>
    </div>
  `;

  // Option selection enables Check Answer
  $$('input[name=answer]').forEach(el=>el.addEventListener('change',()=>{
    state.drafts[q.id]={notes:state.drafts[q.id]?.notes||'',selected:el.value,updatedAt:now()};
    save();
    if(!attempt&&$('#btn-action'))$('#btn-action').disabled=false;
  }));

  $('#answer-form').onsubmit=e=>{
    e.preventDefault();
    if(!attempt){
      const selected=document.querySelector('input[name=answer]:checked');
      if(!selected){$('#answer-error').textContent='Please choose an answer or use “I don’t know”.';return;}
      submit(q,selected.value);
    }else{
      advanceQuestion();
    }
  };

  $('#unknown')?.addEventListener('click',()=>submit(q,null));
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
  return `
    <section class="feedback" data-outcome="${h(a.outcome)}">
      <h3 class="outcome-${h(a.outcome)}" id="feedback-heading" tabindex="-1">${label[a.outcome]}</h3>
      <p><strong>Correct answer:</strong> ${h(optionText(correct))}</p>
      <p>${h(q.explanation)}</p>
      ${q.workedCalculation?`<div class="calculation">${h(q.workedCalculation)}</div>`:''}
      ${a.outcome==='incorrect'?`<p><strong>Why your choice is wrong:</strong> ${h(selected.explanation)}</p>`:''}
      <details><summary>Explain all answer options</summary><ul>${q.options.map(o=>`<li><strong>${h(optionText(o))}</strong>${o.id===correct.id?' — correct':''}<br>${h(o.explanation)}</li>`).join('')}</ul></details>
      ${suggested?`<div class="actions"><button id="followup" data-question="${h(suggested.id)}">Try relevant follow-up question</button></div>`:''}
    </section>
  `;
}

function bindFeedback(q,attempt){
  if(!attempt)return;
  $('#followup')?.addEventListener('click',e=>{
    const id=e.currentTarget.dataset.question;const s=state.session;
    s.queue=[...s.queue.slice(0,s.index+1),id,...s.queue.slice(s.index+1).filter(x=>x!==id)];
    s.index++;s.attemptId=null;s.order=shuffle(question(id).options.map(o=>o.id));save();render();$('#main').focus();
  });
}

function advanceQuestion(){
  const s=state.session;
  if(s.index+1>=s.queue.length){showResults();return;}
  s.index++;s.attemptId=null;s.order=shuffle(question(s.queue[s.index]).options.map(o=>o.id));
  save();render();$('#main').focus();
}

// =================== EXAM MODE ===================
function renderExamOverview(){
  stopExamTimer();
  $('#main').innerHTML=`
    <section class="welcome study-hero">
      <span class="eyebrow">ACA PAST EXAM REPLICATION</span>
      <h2>Exam Mode</h2>
      <p>Test yourself under real exam conditions matching past course sittings. The timer will <strong>not</strong> start until you explicitly click Begin below.</p>
      <div class="actions">
        <button class="primary" id="btn-begin-exam-part1">Begin Part 1: Accounting & Auditing (45m) →</button>
        <button id="btn-begin-exam-part2">Begin Part 2: Controlling (45m) →</button>
      </div>
    </section>
    <div class="study-stats">
      <div><strong>45 min</strong><span>Duration per part</span></div>
      <div><strong>Single-choice</strong><span>Only 1 correct option</span></div>
      <div><strong>0 penalties</strong><span>Wrong answers count as 0</span></div>
    </div>
    <section class="topic-section">
      <div class="section-heading"><h2>Exam Structure Reference</h2><p class="muted">Based directly on official sittings (Prof. Eugster & Prof. Fehrenbacher).</p></div>
      <div class="topic-grid">
        <div class="topic-card">
          <span class="topic-number">PART 1 · 45 MINUTES · 45 MARKS</span>
          <span class="topic-title">Accounting & Auditing</span>
          <span class="topic-count">Topic 1: Accounting (30 Marks) · Topic 2: Auditing (15 Marks)<br>Total 30 Exercises.</span>
        </div>
        <div class="topic-card">
          <span class="topic-number">PART 2 · 45 MINUTES · 45 MARKS</span>
          <span class="topic-title">Controlling</span>
          <span class="topic-count">Topic: Management Accounting & Cost Systems (45 Marks)<br>Total ~20 Exercises.</span>
        </div>
      </div>
    </section>
  `;
  $('#btn-begin-exam-part1').onclick=()=>launchExam('part1');
  $('#btn-begin-exam-part2').onclick=()=>launchExam('part2');
}

function launchExam(part){
  let pool=[];
  if(part==='part1'){
    // 20 accounting + 10 auditing = 30
    const acct=shuffle(bank.questions.filter(q=>q.status==='validated'&&(q.topic==='Consolidated Statements'||q.topic==='Financial Reporting'))).slice(0,20);
    const audit=shuffle(bank.questions.filter(q=>q.status==='validated'&&q.topic==='Auditing')).slice(0,10);
    pool=[...acct,...audit].map(q=>q.id);
  }else if(part==='part2'){
    pool=shuffle(bank.questions.filter(q=>q.status==='validated'&&q.topic==='Management Accounting')).slice(0,20).map(q=>q.id);
  }else{
    const acct=shuffle(bank.questions.filter(q=>q.status==='validated'&&(q.topic==='Consolidated Statements'||q.topic==='Financial Reporting'))).slice(0,20);
    const audit=shuffle(bank.questions.filter(q=>q.status==='validated'&&q.topic==='Auditing')).slice(0,10);
    const ma=shuffle(bank.questions.filter(q=>q.status==='validated'&&q.topic==='Management Accounting')).slice(0,20);
    pool=[...acct,...audit,...ma].map(q=>q.id);
  }

  const q=question(pool[0]);
  state.session={
    queue:pool,
    index:0,
    order:shuffle(q.options.map(o=>o.id)),
    mode:part==='part1'?'exam-part1':part==='part2'?'exam-part2':'exam-full',
    attemptId:null,
    attemptIds:[],
    examTimeRemaining:part==='full'?90*60:45*60,
    examFlags:{}
  };
  save();
  startExamTimer();
  render();
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

function renderExamActive(){
  const s=state.session;
  const q=question(s.queue[s.index]);
  const d=state.drafts[q.id];
  const m=Math.floor((s.examTimeRemaining||0)/60),sec=(s.examTimeRemaining||0)%60;
  const isPart1=s.mode==='exam-part1',isPart2=s.mode==='exam-part2';
  const examTitle=isPart1?'Part 1: Accounting & Auditing':isPart2?'Part 2: Controlling':'Full ACA Exam';

  $('#main').innerHTML=`
    <div class="exam-banner">
      <div>
        <h2>Exam Mode — ${h(examTitle)}</h2>
        <p>Exercise ${s.index+1} of ${s.queue.length} · Single choice · No deduction for wrong answers</p>
      </div>
      <div class="exam-timer-box">
        <span class="exam-timer-display" id="exam-timer">${String(m).padStart(2,'0')}:${String(sec).padStart(2,'0')}</span>
        <button id="timer-toggle-btn" class="exam-timer-toggle" type="button">${examTimerPaused?'▶ Resume':'⏸ Pause'}</button>
      </div>
    </div>
    <div class="palette-card">
      <div class="palette-header">
        <span>Exercise Matrix (${s.queue.length} exercises)</span>
        <div class="palette-legend">
          <span><span class="legend-dot" style="background:var(--green)"></span> Answered</span>
          <span><span class="legend-dot" style="background:#fde047"></span> Flagged</span>
          <span><span class="legend-dot" style="background:var(--line)"></span> Unanswered</span>
        </div>
      </div>
      <div class="palette-grid">
        ${s.queue.map((id,idx)=>{
          const ans=state.drafts[id]?.selected;
          const flg=s.examFlags?.[id];
          const cur=idx===s.index;
          return `<button type="button" class="palette-btn ${ans?'answered':''} ${flg?'flagged':''} ${cur?'current':''}" data-jump="${idx}">${idx+1}</button>`;
        }).join('')}
      </div>
    </div>
    <div class="question-layout">
      <article class="question">
        <div class="exam-exercise-head">
          <div class="exam-exercise-title">
            <span class="exam-badge">Exercise ${s.index+1}</span>
            <span class="exam-marks">${q.marks?`(${q.marks} Marks)`:'(1–2 Marks)'}</span>
          </div>
          <button type="button" id="btn-flag" class="flag-btn ${s.examFlags?.[q.id]?'flagged':''}">
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
              <span><strong>${h(o.id.toUpperCase())}.</strong> ${h(optionText(o))}</span>
            </label>`;
          }).join('')}
        </fieldset>
        <div class="exam-nav-bar">
          <button type="button" id="btn-exam-prev" ${s.index===0?'disabled':''}>← Previous</button>
          <button type="button" id="btn-exam-finish" class="danger">End & Submit Exam</button>
          <button type="button" id="btn-exam-next" class="primary">${s.index+1<s.queue.length?'Next exercise →':'Finish exam'}</button>
        </div>
      </article>
      <aside id="notebook" class="notes-panel" aria-label="Exercise scratchpad">
        ${notes(q)}
      </aside>
    </div>
  `;

  // Option change autosaves selection
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
    save();render();
  });

  $('#btn-exam-prev').onclick=()=>{
    if(s.index>0){s.index--;s.order=shuffle(question(s.queue[s.index]).options.map(o=>o.id));save();render();}
  };

  $('#btn-exam-next').onclick=()=>{
    if(s.index+1<s.queue.length){s.index++;s.order=shuffle(question(s.queue[s.index]).options.map(o=>o.id));save();render();}
    else finishExam();
  };

  $('#btn-exam-finish').onclick=finishExam;
  $('#timer-toggle-btn').onclick=toggleExamTimer;
}

function finishExam(){
  const s=state.session;
  const answered=s.queue.filter(id=>state.drafts[id]?.selected).length;
  if(!confirm(`You answered ${answered} of ${s.queue.length} exercises. Ready to submit this exam?`))return;
  stopExamTimer();
  // Grade each question
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
            <summary><strong>${label[a.outcome]}</strong> — ${h(q.topic)} · ${h(q.prompt.slice(0,90))}…</summary>
            ${q.scenario?`<div class="scenario">${format(q.scenario)}</div>`:''}
            <div class="prompt">${format(q.prompt)}</div>
            <p><strong>Your answer:</strong> ${chosenOpt?h(optionText(chosenOpt)):'Unanswered'}</p>
            <p><strong>Correct answer:</strong> ${h(optionText(correctOpt))}</p>
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

    const response=await fetch('./content/questions.json');
    if(!response.ok)throw new Error('Question data could not be loaded.');
    bank=await response.json();
    state=emptyState(bank.bankVersion);

    try{
      const raw=localStorage.getItem(STORAGE_KEY);
      if(raw)state=validateBackup(JSON.parse(raw),bank);
    }catch(error){
      try{unreadable=localStorage.getItem(STORAGE_KEY);}catch{}
      storageBlocked=true;
      notify('Saved browser data could not be read.');
    }

    view=state.view;

    // Populate topics
    const topics=[...new Set(bank.questions.filter(q=>q.status==='validated').map(q=>q.topic))].sort();
    topics.forEach(t=>{if(![...$('#topic').options].some(o=>o.value===t))$('#topic').add(new Option(t,t));});
    populateSubtopics(state.preferences.topic||'');

    for(const key of ['topic','difficulty','origin']){
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

    // Exam start button: explicit start!
    $('#start-exam').onclick=()=>{
      const selectedPart=document.querySelector('input[name="exam-part"]:checked')?.value||'part1';
      launchExam(selectedPart);
    };

    // Tax focus legacy hook
    $('#tax-focus').onclick=()=>{
      $('#topic').value='Financial Reporting';
      populateSubtopics('Financial Reporting');
      $('#subtopic').value='Deferred taxes';
      $('#difficulty').value='';
      $('#setup').requestSubmit();
    };

    // Navigation
    $('#nav-study').onclick=()=>setView('practice');
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
        try{localStorage.removeItem(STORAGE_KEY);}catch{notify('Browser storage could not be reset.');return;}
        state=emptyState(bank.bankVersion);storageBlocked=false;unreadable=null;view='practice';
        save();render();notify('Study data has been reset in this browser.');
      }
    };

    render();
    if(!storageBlocked)save();
  }catch(error){
    $('#main').innerHTML=`<h2>Unable to launch practice</h2><p>${h(error.message)}</p>`;
  }
}

// Global keyboard shortcuts (Enter to check/advance, 1-5 / A-E to select)
document.addEventListener('keydown',e=>{
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
