import {STORAGE_KEY,emptyState,shuffle,unexploredFirst,shuffleOptions,pinNoneLast,makeAttempt,isGuess,grade,available,followup,latestAttempts,validateBackup,mergeBackups,topicProgress,recommendTopics,reviewQueue,topicBreakdown,flaggedIds,inPractice,mockExam} from './core.mjs';
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
let examSource='bank'; // 'bank' = random mix from the question bank, 'mock' = the separate AI mock exam
const aiBadge=q=>q?.aiGenerated?'<span class="ai-badge" title="Written by AI for practice. Figures were checked by script; not from an official exam.">AI-generated</span>':'';
let examTimerInterval=null;
let examTimerPaused=false;
let themeChanging=false;
let activeUser=null,cloud=null,storageKey=STORAGE_KEY;
// Sure / Guessing choice for the open practice question, kept until it is checked.
let confidence={id:null,value:'sure'};

const now=()=>new Date().toISOString();
const reduceMotion=()=>matchMedia('(prefers-reduced-motion: reduce)').matches;
const question=id=>bank.questions.find(q=>q.id===id);

const preciseSubtopics={
  "Financial Reporting":[
    {val:"",text:"All financial reporting areas"},
    {val:"Deferred taxes",text:"Deferred taxes (DTA/DTL and temporary differences)"},
    {val:"Leases",text:"IFRS 16 leases (PV, carrying amount and split)"},
    {val:"Impairment",text:"Impairment of assets and impairment tests"},
    {val:"Goodwill",text:"Goodwill subsequent measurement (IFRS vs FER)"},
    {val:"Accounting frameworks",text:"Frameworks: principle- vs rule-based and Swiss CO"},
    {val:"Pensions",text:"Employee benefits and defined-benefit pension risk"},
    {val:"Financial instruments",text:"IFRS 9 classification and bonds (effective interest)"},
    {val:"Presentation (IFRS 18)",text:"IFRS 18 income statement categories and MPMs"},
    {val:"Intangible assets",text:"Intangible assets (IAS 38 recognition)"}
  ],
  "Consolidated Statements":[
    {val:"",text:"All consolidation areas"},
    {val:"Acquisition accounting",text:"Acquisition mechanics, reserves and goodwill"},
    {val:"Equity method",text:"Equity method and associate roll-forwards"},
    {val:"Consolidation concepts",text:"Group scope, elimination logic and NCI concepts"},
    {val:"Accounting frameworks",text:"Consolidation frameworks and Swiss CO overlay"}
  ],
  "Auditing":[
    {val:"",text:"All auditing areas"},
    {val:"Audit procedures",text:"Substantive and analytical audit procedures"},
    {val:"Materiality",text:"Materiality benchmarks and misstatements"},
    {val:"Audit purpose",text:"Audit purpose, objectives and credibility"},
    {val:"Audit scope",text:"Swiss OR triggers: ordinary vs limited audit"},
    {val:"Assurance",text:"Levels of assurance (reasonable vs limited)"},
    {val:"Audit opinions",text:"Audit opinions, modifications and reports"},
    {val:"Key Audit Matters",text:"Key audit matters (KAMs): purpose and disclosures"},
    {val:"Going concern",text:"Going concern assessment and reporting"},
    {val:"Expectation gap",text:"The audit expectation gap"},
    {val:"Internal controls",text:"Internal control system (ICS) and governance"},
    {val:"Audit risk",text:"Audit risk model (inherent, control, detection risk)"}
  ],
  "Management Accounting":[
    {val:"",text:"All management accounting areas"},
    {val:"CVP analysis",text:"Cost-volume-profit (CVP) and breakeven analysis"},
    {val:"Manufacturing cost flows",text:"Manufacturing cost flows and COGM / COGS"},
    {val:"Pricing and target costing",text:"Target costing and markup pricing"},
    {val:"Job costing",text:"Job costing and manufacturing overhead allocation"},
    {val:"Cost concepts",text:"Direct vs indirect and fixed vs variable costs"},
    {val:"Activity-based costing",text:"Activity-based costing (ABC) overhead per unit"}
  ],
  "Budgeting":[
    {val:"",text:"All budgeting areas"},
    {val:"Cash collections",text:"Cash collections and cash budgets"},
    {val:"Activity-based budgeting",text:"Activity-based budgeting (ABB)"},
    {val:"Production budget",text:"Production and materials budgets"},
    {val:"Sales budget",text:"Sales forecasting and operating budgets"},
    {val:"Purchases budget",text:"Direct materials purchases budget"},
    {val:"Income statement budget",text:"Budgeted income statement and master budget"}
  ],
  "Variances":[
    {val:"",text:"All variance analysis areas"},
    {val:"Flexible budgets",text:"Flexible budgets vs static budgets"},
    {val:"Flexible-budget variance",text:"Flexible-budget and sales-volume variances"},
    {val:"Direct material variances",text:"Direct material price and efficiency variances"},
    {val:"Direct labor price variance",text:"Direct labor rate and efficiency variances"},
    {val:"Fixed-overhead variances",text:"Fixed and variable overhead variance analysis"}
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
  if(reduceMotion()){update();return;}
  // Knob: slides with ease-in-out and stretches ~12% at mid-slide, then settles.
  const knob=()=>{const on=root.classList.contains('dark'),[a,b]=on?[0,24]:[24,0];$('.theme-switch-thumb').animate([{transform:`translateX(${a}px)`,width:'22px'},{transform:`translateX(${(a+b)/2-1.5}px)`,width:'25px'},{transform:`translateX(${b}px)`,width:'22px'}],{duration:300,easing:'ease-in-out'});};
  if(!document.startViewTransition){update();knob();return;}
  delete root.dataset.vt; // no page-transition names inside the theme snapshot
  const rect=$('#theme-toggle').getBoundingClientRect();
  const x=rect.left+rect.width/2,y=rect.top+rect.height/2;
  const radius=Math.hypot(Math.max(x,innerWidth-x),Math.max(y,innerHeight-y));
  themeChanging=true;root.classList.add('theme-changing');
  const transition=document.startViewTransition(()=>{update();knob();});
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
  const pool=available(bank.questions,prefs,$('#mode').value,state.attempts),n=pool.length;
  const seen=new Set(state.attempts.map(a=>a.questionId)),fresh=pool.filter(q=>!seen.has(q.id)).length;
  $('#available').textContent=`${n} matching validated question${n===1?'':'s'}`+(n?` · ${fresh} unexplored`:'');
  $('#start').disabled=!n;
  const length=$('#length-slider')?.value||15;
  const scope=prefs.subtopic||prefs.topic||'All topics';
  $('#setup-hint').textContent=appMode==='exam'?'Exam mode':`Practice · ${scope} · ${length} questions`;
}

function setView(next,focus=true){
  view=next;state.view=next;
  if(next==='practice'&&appMode==='exam'&&state.session?.mode.startsWith('exam'))startExamTimer();
  else stopExamTimer();
  save();render();
  if(focus){$('#main').focus();if(next==='home')window.scrollTo(0,0);}
}

// Page transitions (View Transitions API). html[data-vt] switches on the
// view-transition-names for one transition only, so names stay unique and the
// theme reveal never sees them. Instant when unsupported, reduced or mid theme change.
let vtPending=false,vtToken=0,lastScreen='';
function pageTransition(kind,update){
  if(!document.startViewTransition||reduceMotion()||themeChanging){update();return;}
  if(vtPending)return; // ignore repeat input before the first update has run
  const token=++vtToken;vtPending=true;root.dataset.vt=kind;
  const t=document.startViewTransition(()=>{vtPending=false;update();});
  t.finished.catch(()=>{}).finally(()=>{if(token===vtToken)delete root.dataset.vt;});
}
// True the first time a screen renders, false on re-renders of it (save, sync):
// entrance staggers play once per visit.
function freshScreen(key){const fresh=key!==lastScreen;lastScreen=key;return fresh;}

function focusQuestion(){
  const target=$('.question');
  if(!target)return;
  $('#session-settings').open=false;
  const top=($('.masthead').offsetHeight||$('#header-show').offsetHeight)+16;
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
  updateAvailable();
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
  if(view!=='home'&&!(view==='practice'&&!state.session&&appMode==='practice'))lastScreen=view+appMode;
  bindNotes();updateAvailable();
  if($('#global-save').classList.contains('failed'))$$('.save-status').forEach(el=>{el.textContent='Not saved — export a backup';el.classList.add('failed');});
}

function startSession(ids,mode,scope){
  stopExamTimer();
  const q=question(ids[0]);
  state.session={queue:ids,index:0,order:shuffleOptions(q.options),mode,attemptId:null,attemptIds:[],examFlags:{}};
  if(scope)state.session.scope={topic:scope.topic||'',subtopic:scope.subtopic||'',difficulty:scope.difficulty||''};
  setAppMode('practice',false);
  setView('practice',false);
  focusQuestion();
}

// A topic session is titled by what it tests. A mixed session shows its
// position and length instead.
function subtopicLabel(topic,subtopic){
  const lists=topic?[preciseSubtopics[topic]||[]]:Object.values(preciseSubtopics);
  for(const list of lists){const hit=list.find(s=>s.val===subtopic);if(hit)return hit.text;}
  return subtopic;
}
function sessionTopic(session){
  const scope=session.scope;
  if(scope?.topic)return scope.topic;
  if(scope?.subtopic)return question(session.queue[0])?.topic||'';
  return '';
}
function sessionTitle(session){
  const topic=session.mode==='mixed'?sessionTopic(session):'';
  if(!topic)return `Question ${session.index+1} of ${session.queue.length}`;
  return session.scope.subtopic?subtopicLabel(topic,session.scope.subtopic):topic;
}
function sessionSubtitle(session,completed){
  const topic=session.mode==='mixed'?sessionTopic(session):'';
  const parts=[];
  if(topic){
    if(session.scope.subtopic)parts.push(topic);
    if(session.scope.difficulty)parts.push(session.scope.difficulty);
  }else{
    parts.push(session.mode==='missed'?'Review missed / unknown':session.mode==='retry'?(session.queue.length>1?'Wrong answers from your last session':'Retry'):session.mode==='review'?'Due for review':session.mode==='flagged'?'Flagged questions':session.mode==='mixed'?'Mixed topics':'Practice mode');
    if(session.mode==='mixed'&&session.scope?.difficulty)parts.push(session.scope.difficulty);
  }
  if(session.aiOnly)parts.push('AI-generated only');
  parts.push(`${completed} of ${session.queue.length} submitted`);
  return parts.join(' · ');
}

// "today at 14:30", "tomorrow at 9:05", "on Fri 13 Nov"
function dueText(iso){
  const at=new Date(iso),day=d=>new Date(d.getFullYear(),d.getMonth(),d.getDate()).getTime();
  const days=Math.round((day(at)-day(new Date()))/864e5),time=at.toLocaleTimeString([],{hour:'2-digit',minute:'2-digit'});
  return days<=0?`today at ${time}`:days===1?`tomorrow at ${time}`:`on ${at.toLocaleDateString([],{weekday:'short',day:'numeric',month:'short'})}`;
}
function homeQueues(){
  const review=reviewQueue(bank.questions,state.attempts,Date.now()),n=review.due.length,items=[];
  if(n)items.push(`<div class="queue-item"><div><strong>Due for review</strong><span class="muted">${n===1?'1 question you missed, skipped or guessed is':`${n} questions you missed, skipped or guessed are`} ready for another try.</span></div><button type="button" id="review-due">Review ${n===1?'1 question':`${n} questions`}</button></div>`);
  else if(review.nextAt)items.push(`<div class="queue-item"><div><strong>Due for review</strong><span class="muted">Nothing due right now. The next question comes back ${h(dueText(review.nextAt))}.</span></div></div>`);
  const flagged=flaggedIds(bank.questions,state.flags);
  if(flagged.length)items.push(`<div class="queue-item"><div><strong>Flagged (${flagged.length})</strong><span class="muted">Questions you marked to come back to. Unflag them on the question.</span></div><button type="button" id="review-flagged">Practice flagged</button></div>`);
  return {html:items.length?`<section class="home-queues" aria-label="Review">${items.join('')}</section>`:'',review,flagged};
}

// =================== PRACTICE MODE ===================
function renderHome(){
    const scored=bank.questions.filter(inPractice),latest=latestAttempts(state.attempts);
    const revisit=[...latest.values()].filter(a=>a.outcome!=='correct').length,queues=homeQueues(),stagger=freshScreen('home')?' stagger':'';
    $('#main').innerHTML=`<div class="home-top"><section class="welcome study-hero"><h2>Practice by topic or run a mixed session.</h2><p class="muted">Every answer comes with a worked explanation, including why each wrong option is wrong.</p><div class="actions"><button class="primary" id="welcome-start">${state.attempts.length?'Keep practicing':'Start practicing'}</button><button id="welcome-exam">Launch exam mode</button></div></section><div class="study-stats" aria-label="Study overview"><div><strong>${state.attempts.length}</strong><span>Attempts logged</span></div><div><strong>${revisit}</strong><span>Questions to revisit</span></div><div><strong>${scored.length}</strong><span>Validated questions</span></div></div></div>${queues.html}<section class="topic-section"><div class="section-heading"><h2>Find your focus</h2></div><div class="topic-grid${stagger}">${[...new Set(scored.map(q=>q.topic))].map((topic,index)=>{const pool=scored.filter(q=>q.topic===topic),seen=pool.filter(q=>latest.has(q.id)).length;return `<button class="topic-card" data-topic="${h(topic)}" style="--i:${index}"><span class="topic-number" aria-hidden="true">${String(index+1).padStart(2,'0')}</span><span class="topic-title">${h(topic)}</span><span class="topic-count">${pool.length} questions · ${seen} explored</span><span class="topic-track" aria-hidden="true"><span style="width:${100*seen/pool.length}%"></span></span></button>`;}).join('')}</div></section>`;
    if(state.session)$('#welcome-start').textContent='Resume session';
    $('#welcome-start').onclick=()=>state.session?$('#nav-study').click():$('#setup').requestSubmit();
    $('#welcome-exam').onclick=()=>setAppMode('exam');
    $('#review-due')?.addEventListener('click',()=>startSession(shuffle(queues.review.due),'review'));
    $('#review-flagged')?.addEventListener('click',()=>startSession(shuffle(queues.flagged),'flagged'));
    // The clicked card's title morphs into the session heading, if that heading
    // ends up on screen (a long question scrolls it under the header: plain fade then).
    $$('[data-topic]').forEach(el=>el.onclick=()=>{el.classList.add('vt-source');pageTransition('topic',()=>{
      startTopicSession(el.dataset.topic);
      const title=$('.session-head h2');
      if(root.dataset.vt&&(!title||title.getBoundingClientRect().top<$('.masthead').getBoundingClientRect().bottom))root.dataset.vt='topic-fade';
    });});
}

// Starts a mixed-difficulty practice session limited to one topic.
function startTopicSession(topic){
  $('#topic').value=topic;populateSubtopics(topic);$('#subtopic').value='';$('#difficulty').value='';$('#setup').requestSubmit();
}

// End-of-session cards: the questions answered wrong in this session (to look
// at again, exactly those), and the least covered topic overall.
function recommendationCards(sessionAttempts,stagger=false){
  const scored=bank.questions.filter(inPractice);
  const {leastCovered}=recommendTopics(scored,sessionAttempts,state.attempts);
  const pick=test=>[...new Set(sessionAttempts.filter(test).map(a=>a.questionId))].filter(id=>question(id)&&inPractice(question(id)));
  const wrong=pick(a=>a.outcome==='incorrect'),guessed=pick(isGuess).filter(id=>!wrong.includes(id)),ids=[...wrong,...guessed];
  const cards=[];
  if(ids.length)cards.push(`<div class="recommendation wrong-review"><p>${guessed.length?'Look again at these':'Look again at your wrong answers'}</p><ol class="wrong-list${stagger?' stagger':''}">${ids.map((id,i)=>{const q=question(id);const text=q.prompt.replace(/^\d+(?:\.\d+)?\.?\s*(?:\(\d+ marks?\)\s*)?/,'');return `<li style="--i:${i}"><span class="muted">${h(q.topic)}${guessed.includes(id)?' (guessed)':''}</span>${h(text.length>110?text.slice(0,110).trimEnd()+'…':text)}</li>`;}).join('')}</ol><button type="button" class="primary" id="retry-wrong" data-retry-ids="${h(ids.join(','))}">Retry ${ids.length===1?'this question':`these ${ids.length} questions`}</button></div>`);
  if(leastCovered)cards.push(`<div class="recommendation"><p>Least covered: ${h(leastCovered)}</p><button type="button" data-recommend-topic="${h(leastCovered)}">Practice ${h(leastCovered)}</button></div>`);
  if(!cards.length)return '';
  return `<div class="recommendations">${cards.join('')}</div>`;
}

function bindRecommendations(){
  $$('[data-recommend-topic]').forEach(el=>el.onclick=()=>startTopicSession(el.dataset.recommendTopic));
  const retry=$('#retry-wrong');
  if(retry)retry.onclick=()=>startSession(shuffle(retry.dataset.retryIds.split(',')),'retry');
}

function renderPractice(){
  const session=state.session;
  if(!session){renderHome();return;}

  const q=question(session.queue[session.index]);
  const attempt=state.attempts.find(a=>a.id===session.attemptId);
  const d=state.drafts[q.id];
  const completed=session.attemptIds.length;
  // A question answered in an earlier session is not preselected. Its earlier
  // answer is cleared from the draft, so only a new choice in this session is shown.
  const earlier=attempt?null:state.attempts.filter(a=>a.questionId===q.id&&!session.attemptIds.includes(a.id)).sort((a,b)=>Date.parse(a.timestamp)-Date.parse(b.timestamp)).at(-1)||null;
  if(earlier&&d?.selected&&d.selected===earlier.optionId)state.drafts[q.id]={...d,selected:null};
  const selectedId=earlier?null:d?.selected;

  $('#main').innerHTML=`
    <div class="session-head">
      <div>
        <h2>${h(sessionTitle(session))}</h2>
        <p class="muted">${h(sessionSubtitle(session,completed))}</p>
      </div>
      <div class="session-actions">
        <button type="button" id="ai-only" class="ai-only-btn${session.aiOnly?' active':''}" aria-pressed="${Boolean(session.aiOnly)}" title="${session.aiOnly?'Back to all questions for the rest of this session':'Use only AI-generated questions for the rest of this session'}">AI questions only</button>
        <button id="end-session">End session & see results</button>
      </div>
    </div>
    <progress max="${session.queue.length}" value="${session.index+(attempt?1:0)}" aria-label="Session progress"></progress>
    <div class="question-layout">
      <article class="question" tabindex="-1" aria-label="Current question">
        ${q.aiGenerated?`<div class="question-tags">${aiBadge(q)}</div>`:''}
        ${q.scenario?`<div class="scenario">${format(q.scenario)}</div>`:''}
        <div class="prompt" id="question-prompt">${format(q.prompt.replace(/^\d+(?:\.\d+)?\.?\s*(?:\(\d+ marks?\)\s*)?/,''))}</div>
        ${q.assumptions.length?`<details class="assumptions"><summary>Assumptions for this question</summary>${q.assumptions.map(s=>`<p>${h(s)}</p>`).join('')}</details>`:''}
        <form id="answer-form">
          ${earlier?'<p class="muted repeat-hint">Repeat: answered before</p>':''}
          <fieldset class="options" ${attempt?'disabled':''}>
            <legend class="visually-hidden">Choose one answer</legend>
            ${session.order.map((id,idx)=>{
              const o=q.options.find(o=>o.id===id);
              const isChecked=(attempt?attempt.optionId:selectedId)===id;
              return `<label class="option ${attempt&&isChecked?(id===q.correctOptionId?'correct-option':'wrong-option'):''}">
                <input type="radio" name="answer" value="${h(id)}" ${isChecked?'checked':''}>
                <span><strong>${h(shownLabel(session.order,id))}.</strong> ${h(optionText(o))}</span>
                ${attempt&&isChecked?`<small class="answer-result">${id===q.correctOptionId?'Correct':'Incorrect'}</small>`:''}
              </label>`;
            }).join('')}
          </fieldset>
          <p id="answer-error" class="danger" role="alert"></p>
          <div class="action-bar">
            <div class="action-left">
              <button type="button" id="previous-question" ${session.index===0?'disabled':''}>Previous</button>
              ${flagButton(Boolean(state.flags[q.id]?.flagged))}
            </div>
            <div class="action-buttons">
              ${attempt?'':`<div class="confidence" role="radiogroup" aria-label="How sure are you?"><div class="confidence-pills">${[['sure','Sure'],['guess','Guessing']].map(([v,t])=>`<label><input type="radio" name="confidence" value="${v}" ${(confidence.id===q.id?confidence.value:'sure')===v?'checked':''}><span>${t}</span></label>`).join('')}</div></div>`}
              ${!attempt?`<button type="button" id="unknown" class="quiet">Skip</button>`:''}
              <button class="primary" type="submit" id="btn-action" ${!attempt&&!selectedId?'disabled':''}>
                ${!attempt?'Check answer':(session.index+1<session.queue.length?'Next question':'See results')}
              </button>
            </div>
          </div>
        </form>
      </article>
      <aside id="feedback" class="explanation-panel" aria-label="Question explanation">${attempt?feedback(q,attempt):'<h3>Explanation</h3><p class="muted">Check your answer to see the worked solution and why each option is right or wrong.</p>'}</aside>
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

  $$('input[name=confidence]').forEach(el=>el.addEventListener('change',()=>{confidence={id:q.id,value:el.value};}));
  $('#unknown')?.addEventListener('click',()=>submit(q,null));
  const toggleFlag=()=>{
    const on=!state.flags[q.id]?.flagged;state.flags[q.id]={flagged:on,updatedAt:now()};save();
    $('#practice-flag').outerHTML=flagButton(on);$('#practice-flag').onclick=toggleFlag;$('#practice-flag').focus();
  };
  $('#practice-flag').onclick=toggleFlag;
  $('#previous-question').onclick=()=>{if(session.index>0)goToQuestion(session.index-1);};
  $('#end-session').onclick=showResults;
  $('#ai-only').onclick=toggleAiOnly;
  bindFeedback(q,attempt);
}

const flagButton=on=>`<button type="button" id="practice-flag" class="flag-btn ${on?'flagged':''}" aria-pressed="${on}" title="${on?'Remove from your flagged questions':'Keep this question in your flagged list on Home'}">${on?'Flagged':'Flag'} <span aria-hidden="true">⚑</span></button>`;

function submit(q,optionId){
  if(state.session.attemptId)return;
  const sure=confidence.id===q.id?confidence.value:'sure';confidence={id:null,value:'sure'};
  const attempt=makeAttempt(q,optionId,state.drafts[q.id]?.notes||'',now(),crypto.randomUUID(),bank.bankVersion,sure);
  state.attempts.push(attempt);
  state.session.attemptId=attempt.id;
  state.session.attemptIds.push(attempt.id);
  save();
  render();
  // One soft ring on the correct option; wrong answers get no extra motion.
  if(attempt.outcome==='correct')$('.option.correct-option')?.classList.add('pulse');
  $('#feedback-heading')?.focus();
}

function feedback(q,a){
  const correct=q.options.find(o=>o.id===q.correctOptionId),suggested=a.outcome!=='correct'?followup(q,a,bank.questions,state.attempts):null;
  const order=state.session.order;
  return `
    <section class="feedback" data-outcome="${h(a.outcome)}">
      <h3 class="outcome-${h(a.outcome)}" id="feedback-heading" tabindex="-1">${label[a.outcome]}</h3>
      ${isGuess(a)?'<p class="muted">You marked this as a guess, so it comes back for review tomorrow.</p>':''}
      <p><strong>Correct answer:</strong> ${h(shownLabel(order,correct.id))}. ${h(optionText(correct))}</p>
      <p>${h(q.explanation)}</p>
      ${q.workedCalculation?`<div class="calculation">${h(q.workedCalculation)}</div>`:''}
      <details class="option-explanations" open><summary>Every option explained</summary><ul>${order.map(id=>{const o=q.options.find(o=>o.id===id),cls=o.id===correct.id?'is-correct':o.id===a.optionId?'is-chosen':'';return `<li class="${cls}"><span class="option-line"><strong>${h(shownLabel(order,id))}. ${h(optionText(o))}</strong>${o.id===correct.id?'<small>Correct</small>':o.id===a.optionId?'<small>Your answer</small>':''}</span><span>${h(o.explanation.replace(/^Correct answer\.\s*/,''))}</span></li>`;}).join('')}</ul></details>
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

// Switches the questions still ahead in this session to AI-generated ones only,
// and back. Answered questions stay where they are; so does the current one once
// it is answered. A mixed session refills from its topic, focus area and
// difficulty; other sessions (review, flagged, retry) keep only their AI questions.
function toggleAiOnly(){
  const s=state.session,on=!s.aiOnly;
  const answered=s.attemptId?s.index+1:s.index;
  const done=s.queue.slice(0,answered),rest=s.queue.slice(answered),currentId=s.queue[s.index];
  let next;
  if(on){
    if(!rest.length){notify('No questions left in this session to switch.');return;}
    const ai=rest.filter(id=>question(id)?.aiGenerated);
    if(s.mode==='mixed'){
      const scope={topic:s.scope?.topic||'',subtopic:s.scope?.subtopic||'',difficulty:s.scope?.difficulty||''};
      const pool=available(bank.questions,scope,'mixed',state.attempts).filter(q=>q.aiGenerated&&!s.queue.includes(q.id));
      next=[...ai,...unexploredFirst(shuffle(pool).map(q=>q.id),state.attempts)].slice(0,rest.length);
    }else next=ai;
    if(!next.length){notify('No AI-generated questions match this session.');return;}
    s.aiOffQueue=rest;s.aiOnly=true;
  }else{
    next=(s.aiOffQueue||[]).filter(id=>!done.includes(id)&&question(id));
    if(!next.length)next=rest;
    delete s.aiOffQueue;delete s.aiOnly;
  }
  s.queue=[...done,...next];
  if(s.questionOrders)for(const id of Object.keys(s.questionOrders))if(!s.queue.includes(id))delete s.questionOrders[id];
  const id=s.queue[s.index];
  if(id!==currentId)s.order=s.questionOrders?.[id]?pinNoneLast(s.questionOrders[id],question(id).options):shuffleOptions(question(id).options);
  save();render();
  $('#ai-only')?.focus();
}

function advanceQuestion(){
  const s=state.session;
  if(s.index+1>=s.queue.length){showResults();return;}
  goToQuestion(s.index+1);
}

// The session head and progress bar hold still while the question area crossfades.
function goToQuestion(index){pageTransition('question',()=>showQuestion(index));}
function showQuestion(index){
  const s=state.session;
  s.questionOrders=s.questionOrders||{};
  s.questionOrders[s.queue[s.index]]=[...s.order];
  s.index=index;
  const id=s.queue[index];
  s.attemptId=state.attempts.find(a=>a.questionId===id&&s.attemptIds.includes(a.id))?.id||null;
  s.order=s.questionOrders[id]?pinNoneLast(s.questionOrders[id],question(id).options):shuffleOptions(question(id).options);
  save();render();focusQuestion();
}

// =================== EXAM MODE ===================
function renderExamOverview(){
  stopExamTimer();
  let selectedPart=document.querySelector('input[name="exam-part"]:checked')?.value||'full';
  if(examSource==='mock'&&selectedPart==='topic'){selectedPart='full';const radio=document.querySelector('input[name="exam-part"][value="full"]');if(radio)radio.checked=true;$('#exam-topic-select-wrap')?.classList.add('hidden');}
  const selectedTopic=$('#exam-topic-select')?.value||'Financial Reporting';

  let config={
    title:'Whole exam (both parts)',
    duration:'90 minutes',
    exerciseCount:'50 exercises',
    marks:'90 marks total',
    description:'Full-length mock exam replicating official past ACA exam papers across all course modules.',
    modules:[
      {title:'Part 1: Accounting & auditing (45 min · 45 marks)',desc:'30 exercises: Financial Reporting & Consolidation (30 marks) + Auditing (15 marks).'},
      {title:'Part 2: Controlling (45 min · 45 marks)',desc:'20 exercises across management accounting, budgeting, variances, capital budgeting and performance management.'}
    ]
  };

  if(selectedPart==='part1'){
    config={
      title:'Part 1: Accounting & auditing',
      duration:'45 minutes',
      exerciseCount:'30 exercises',
      marks:'45 marks total',
      description:'Replication of Part 1 from official past ACA exam papers. Strictly 45 minutes.',
      modules:[
        {title:'Accounting (30 marks · 20 exercises)',desc:'Financial reporting standards, deferred taxes, leases, revenue recognition & consolidated balance sheets.'},
        {title:'Auditing (15 marks · 10 exercises)',desc:'Audit risk assessment, internal controls, substantive testing procedures & audit opinion formulation.'}
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
        {title:'Management accounting & cost systems (30 marks)',desc:'Absorption vs. variable costing, contribution margin, breakeven analysis & cost allocations.'},
        {title:'Budgeting, Variances & Investment Decisions',desc:'Operating budgets, variance analysis, capital budgeting, balanced scorecards and performance measures.'}
      ]
    };
  }else if(selectedPart==='topic'){
    const count=bank?bank.questions.filter(q=>inPractice(q)&&q.topic===selectedTopic).length:0;
    config={
      title:`Topic focus exam: ${selectedTopic}`,
      duration:'45 minutes',
      exerciseCount:`${Math.min(20,count)} exercises`,
      marks:'45 marks total',
      description:`Intensive timed exam sitting focused exclusively on ${selectedTopic} under strict exam conditions.`,
      modules:[
        {title:`${selectedTopic} focus (${Math.min(20,count)} exercises)`,desc:`Simulated exam pool selected exclusively from validated ${selectedTopic} question bank (${count} questions available).`}
      ]
    };
  }

  if(examSource==='mock'){
    const p1=mockExam(bank?.questions||[],1),p2=mockExam(bank?.questions||[],2);
    const marks=list=>list.reduce((sum,q)=>sum+(q.marks||0),0);
    const count=(list,topics)=>list.filter(q=>topics.includes(q.topic)).length;
    const part1={title:`Part 1: Accounting & auditing (45 min · ${marks(p1)} marks)`,desc:`${p1.length} exercises: ${count(p1,['Consolidated Statements','Financial Reporting'])} Financial Reporting & Consolidation, ${count(p1,['Auditing'])} Auditing.`};
    const part2={title:`Part 2: Controlling (45 min · ${marks(p2)} marks)`,desc:`${p2.length} exercises: ${controllingTopics.map(t=>`${count(p2,[t])} ${t}`).join(', ')}.`};
    const pick=selectedPart==='part1'?[p1,[part1]]:selectedPart==='part2'?[p2,[part2]]:[[...p1,...p2],[part1,part2]];
    config={
      title:selectedPart==='part1'?'AI mock exam · Part 1':selectedPart==='part2'?'AI mock exam · Part 2':'AI mock exam · Both parts',
      duration:selectedPart==='full'?'90 minutes':'45 minutes',
      exerciseCount:`${pick[0].length} exercises`,
      marks:`${marks(pick[0])} marks total`,
      description:'A fixed paper of new AI-generated questions in the layout of the past exams. None of these questions appear in practice or in the mixed exams, so the paper stays fresh.',
      modules:pick[1]
    };
  }
  const scopes=examSource==='mock'?[['part1','Part 1'],['part2','Part 2'],['full','Whole exam']]:[['part1','Part 1'],['part2','Part 2'],['full','Whole exam'],['topic','One topic']];
  const sources=[['bank','Mixed from question bank'],['mock','AI mock exam']];
  const topics=[...$('#exam-topic-select').options].map(o=>o.value);
  $('#main').innerHTML=`
    <div class="home-top">
      <section class="welcome study-hero">
        <div class="scope-picker source-picker" role="radiogroup" aria-label="Exam questions">
          ${sources.map(([value,name])=>`<button type="button" role="radio" aria-checked="${value===examSource}" data-exam-source="${value}">${name}</button>`).join('')}
        </div>
        <div class="scope-picker" role="radiogroup" aria-label="Exam scope">
          ${scopes.map(([value,name])=>`<button type="button" role="radio" aria-checked="${value===selectedPart}" data-exam-scope="${value}">${name}</button>`).join('')}
        </div>
        <h2>${h(config.title)}</h2>
        <p class="exam-lead">${h(config.description)}</p>
        ${selectedPart==='topic'?`<label class="overview-topic">Topic <select id="overview-topic">${topics.map(t=>`<option ${t===selectedTopic?'selected':''}>${h(t)}</option>`).join('')}</select></label>`:''}
        <div class="actions"><button class="primary" type="button" id="overview-start">Start exam</button></div>
      </section>
      <div class="study-stats">
        <div><strong>${h(config.duration.replace(' minutes',''))}</strong><span>Minutes</span></div>
        <div><strong>${h(config.exerciseCount.replace(' exercises',''))}</strong><span>Exercises</span></div>
        <div><strong>${h(config.marks.replace(' marks total',''))}</strong><span>Marks</span></div>
      </div>
    </div>

    <section class="topic-section">
      <div class="section-heading">
        <h2>What this exam covers</h2>
        <p class="muted">${examSource==='mock'?'AI-generated paper. Same structure as the past papers; not an official exam.':'Based directly on official past exam papers.'}</p>
      </div>
      <div class="topic-grid">
        ${config.modules.map((m,idx)=>`
          <div class="topic-card">
            <span class="topic-number">Section ${idx+1}</span>
            <span class="topic-title">${h(m.title)}</span>
            <span class="topic-count">${h(m.desc)}</span>
          </div>
        `).join('')}
      </div>
    </section>

    <p class="muted">One correct answer per question. No deductions for incorrect answers.</p>
  `;
  $$('[data-exam-scope]').forEach(el=>el.onclick=()=>{
    const radio=document.querySelector(`input[name="exam-part"][value="${el.dataset.examScope}"]`);
    radio.checked=true;radio.dispatchEvent(new Event('change'));
  });
  $$('[data-exam-source]').forEach(el=>el.onclick=()=>{examSource=el.dataset.examSource;renderExamOverview();});
  $('#overview-topic')?.addEventListener('change',e=>{$('#exam-topic-select').value=e.target.value;renderExamOverview();});
  $('#overview-start').onclick=()=>{closeOptionsMenu();$('#start-exam').click();};
}

function launchExam(part,topic){
  let pool=[];
  let durationSeconds=45*60;
  let modeName='exam-part1';
  let examTopicName=null;
  const source=examSource==='mock'&&part!=='topic'?'mock':'bank';

  if(source==='mock'){
    pool=mockExam(bank.questions,part==='part1'?1:part==='part2'?2:null).map(q=>q.id);
    durationSeconds=part==='full'?90*60:45*60;
    modeName=part==='full'?'exam-full':part==='part2'?'exam-part2':'exam-part1';
  }else if(part==='full'){
    const acct=shuffle(bank.questions.filter(q=>inPractice(q)&&(q.topic==='Consolidated Statements'||q.topic==='Financial Reporting'))).slice(0,20);
    const audit=shuffle(bank.questions.filter(q=>inPractice(q)&&q.topic==='Auditing')).slice(0,10);
    const controlling=shuffle(bank.questions.filter(q=>inPractice(q)&&controllingTopics.includes(q.topic))).slice(0,20);
    pool=[...acct,...audit,...controlling].map(q=>q.id);
    durationSeconds=90*60;
    modeName='exam-full';
  }else if(part==='part1'){
    const acct=shuffle(bank.questions.filter(q=>inPractice(q)&&(q.topic==='Consolidated Statements'||q.topic==='Financial Reporting'))).slice(0,20);
    const audit=shuffle(bank.questions.filter(q=>inPractice(q)&&q.topic==='Auditing')).slice(0,10);
    pool=[...acct,...audit].map(q=>q.id);
    durationSeconds=45*60;
    modeName='exam-part1';
  }else if(part==='part2'){
    pool=shuffle(bank.questions.filter(q=>inPractice(q)&&controllingTopics.includes(q.topic))).slice(0,20).map(q=>q.id);
    durationSeconds=45*60;
    modeName='exam-part2';
  }else if(part==='topic'){
    const chosenTopic=topic||$('#exam-topic-select')?.value||'Financial Reporting';
    examTopicName=chosenTopic;
    pool=shuffle(bank.questions.filter(q=>inPractice(q)&&q.topic===chosenTopic)).slice(0,20).map(q=>q.id);
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
    order:shuffleOptions(q.options),
    mode:modeName,
    examTopic:examTopicName,
    attemptId:null,
    attemptIds:[],
    examInitialDuration:durationSeconds,
    examTimeRemaining:durationSeconds,
    examFlags:{}
  };
  if(source==='mock')state.session.examSource='mock';
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
  if(btn)btn.textContent=examTimerPaused?'Resume':'Pause';
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
  const examTitle=(s.examSource==='mock'?'AI mock exam · ':'')+(isPart1?'Part 1: Accounting & Auditing':isPart2?'Part 2: Controlling':isFull?(s.examSource==='mock'?'Both parts':'Whole Mock Exam'):(s.examTopic?`Topic: ${s.examTopic}`:'Topic Exam'));

  $('#main').innerHTML=`
    <div class="exam-banner">
      <div>
        <h2>Exam mode — ${h(examTitle)}</h2>
        <p>Exercise ${s.index+1} of ${s.queue.length} · Single choice · No deduction for wrong answers</p>
      </div>
      <div class="exam-banner-controls">
        <div class="exam-timer-box">
          <span class="exam-timer-display" id="exam-timer">${String(m).padStart(2,'0')}:${String(sec).padStart(2,'0')}</span>
          <button id="timer-toggle-btn" class="exam-timer-toggle" type="button" title="Pause or resume timer">${examTimerPaused?'Resume':'Pause'}</button>
          <button id="timer-reset-btn" class="exam-timer-toggle" type="button" title="Reset countdown timer">Reset timer</button>
        </div>
        <button type="button" id="btn-banner-cancel-exam" class="exam-cancel-btn" title="Cancel this exam sitting">Cancel exam</button>
      </div>
    </div>
    <div class="palette-card">
      <div class="palette-header">
        <span>Exercise matrix (${s.queue.length} exercises)</span>
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
            <span class="exam-marks">${q.marks?`(${q.marks} Mark${q.marks===1?'':'s'})`:'(1–2 Marks)'}</span>
            ${aiBadge(q)}
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
            <button type="button" id="btn-exam-prev" ${s.index===0?'disabled':''}>Previous</button>
            <button type="button" id="btn-exam-cancel" class="quiet danger">Cancel exam</button>
          </div>
          <div class="exam-nav-right">
            <button type="button" id="btn-exam-finish" class="danger">End and submit exam</button>
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
    s.order=shuffleOptions(question(s.queue[s.index]).options);
    save();render();focusQuestion();
  });

  $('#btn-exam-prev').onclick=()=>{
    if(s.index>0){s.index--;s.order=shuffleOptions(question(s.queue[s.index]).options);save();render();focusQuestion();}
  };

  $('#btn-exam-next').onclick=()=>{
    if(s.index+1<s.queue.length){s.index++;s.order=shuffleOptions(question(s.queue[s.index]).options);save();render();focusQuestion();}
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
  const byTopic=topicBreakdown(bank.questions,rows);
  const allMarked=rows.length&&rows.every(a=>question(a.questionId)?.marks);
  const marksTotal=allMarked?rows.reduce((sum,a)=>sum+question(a.questionId).marks,0):0;
  const marksEarned=allMarked?rows.reduce((sum,a)=>sum+(a.outcome==='correct'?question(a.questionId).marks:0),0):0;
  const wasMock=s.examSource==='mock';
  state.session=null;
  save();

  $('#main').innerHTML=`
    <section class="welcome">
      <h2>${wasMock?'AI mock exam score':'Exam score'}: ${correct} / ${rows.length} (${scorePct}%)</h2>
      ${allMarked?`<p><strong>Marks: ${marksEarned} / ${marksTotal}</strong> (${Math.round(100*marksEarned/marksTotal)}%)</p>`:''}
      <p>Passing benchmark is typically 50%. Wrong answers incurred zero deductions.</p>
      <div class="result-grid">
        <div><strong>${correct}</strong>Correct marks</div>
        <div><strong>${incorrect}</strong>Incorrect</div>
        <div><strong>${unanswered}</strong>Unanswered</div>
      </div>
      ${byTopic.length?`<h3>By topic</h3><div class="table-wrap exam-topics"><table class="topic-table"><caption class="visually-hidden">Exam score by topic, weakest first</caption><thead><tr><th scope="col">Topic</th><th scope="col">Correct</th><th scope="col">Share</th></tr></thead><tbody>${byTopic.map(t=>`<tr><th scope="row">${h(t.topic)}</th><td>${t.correct} / ${t.total}</td><td>${Math.round(100*t.correct/t.total)}%</td></tr>`).join('')}</tbody></table></div>`:''}
      <div class="actions">
        <button class="primary" id="btn-exam-again">Take another exam</button>
        <button id="btn-exam-history">View learning history</button>
      </div>
      ${recommendationCards(rows,freshScreen('exam-results'))}
    </section>
    <section class="dashboard-section">
      <h3>Review exam exercises</h3>
      ${rows.map(a=>{
        const q=question(a.questionId);
        const correctOpt=q.options.find(o=>o.id===q.correctOptionId);
        const chosenOpt=q.options.find(o=>o.id===a.optionId);
        return `
          <details class="history-item">
            <summary><strong class="outcome-${h(a.outcome)}">${label[a.outcome]}</strong> — ${h(q.topic)} · ${h(q.prompt.slice(0,90))}… ${aiBadge(q)}</summary>
            ${q.scenario?`<div class="scenario">${format(q.scenario)}</div>`:''}
            <div class="prompt">${format(q.prompt)}</div>
            <p><strong>Your answer:</strong> ${chosenOpt?h(optionText(chosenOpt)):'Unanswered'}</p>
            <p><strong>Correct answer:</strong> ${h(optionText(correctOpt))}</p>
            <div class="options" aria-label="Reviewed answer options">${q.options.map(o=>`<div class="option ${o.id===a.optionId?(o.id===q.correctOptionId?'correct-option':'wrong-option'):''}"><span>${h(optionText(o))}${o.id===a.optionId?' (your answer)':''}</span>${o.id===a.optionId?`<small class="answer-result">${o.id===q.correctOptionId?'Correct':'Incorrect'}</small>`:''}</div>`).join('')}</div>
            ${a.outcome==='incorrect'&&chosenOpt?`<p><strong>Why your answer is wrong:</strong> ${h(chosenOpt.explanation)}</p>`:''}
            <p>${h(q.explanation)}</p>
            ${q.workedCalculation?`<div class="calculation">${h(q.workedCalculation)}</div>`:''}
          </details>
        `;
      }).join('')}
    </section>
  `;
  $('#btn-exam-again').onclick=()=>setAppMode('exam');
  $('#btn-exam-history').onclick=()=>setView('history');
  bindRecommendations();
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
      <h2>Session results</h2>
      <p>${rows.length} submitted of ${session.queue.length} questions.</p>
      <div class="result-grid">
        <div><strong>${correct}</strong>Correct</div>
        <div><strong>${incorrect}</strong>Incorrect</div>
        <div><strong>${unknown}</strong>I don’t know</div>
      </div>
      <p>Accuracy among answered attempts: <strong>${correct+incorrect?Math.round(100*correct/(correct+incorrect))+'%':'No answered attempts'}</strong>.</p>
      <div class="actions">
        <button class="primary" id="again">Start another session</button>
        <button id="results-history">See learning history</button>
      </div>
      ${recommendationCards(rows,freshScreen('results'))}
    </section>
  `;
  $('#again').onclick=()=>$('#setup').requestSubmit();
  $('#results-history').onclick=()=>setView('history');
  bindRecommendations();
  $('#main').focus();
  updateAvailable();
}

function renderHistory(){
  stopExamTimer();
  const rows=topicProgress(bank.questions,state.attempts);

  $('#main').innerHTML=`
    <div class="section-heading"><h2>Learning history</h2><p class="muted">Share of each topic you have answered, and how many questions you last got wrong.</p></div>
    ${rows.length?`<div class="table-wrap">
      <table class="topic-table">
        <caption class="visually-hidden">Progress by topic</caption>
        <thead>
          <tr><th scope="col">Topic</th><th scope="col">Answered</th><th scope="col">Questions missed</th></tr>
        </thead>
        <tbody>
          ${rows.map(r=>`<tr><th scope="row">${h(r.topic)}</th><td>${r.percentAnswered}%</td><td>${r.wrongQuestions}</td></tr>`).join('')}
        </tbody>
      </table>
    </div>`:'<p class="muted">No validated questions yet.</p>'}
  `;
}

function download(text,name){
  const url=URL.createObjectURL(new Blob([text],{type:'application/json'}));
  const a=document.createElement('a');a.href=url;a.download=name;a.click();
  setTimeout(()=>URL.revokeObjectURL(url),1000);
}

// Options menu: a list of sections, one open at a time. The name attribute
// does this natively; the listener covers browsers without it. Closing the
// menu folds it back to the list.
// The header can be hidden completely; a small tab at the top brings it back.
function setHeaderCollapsed(collapsed,focus=false){
  root.classList.toggle('header-collapsed',collapsed);
  $('#header-show').hidden=!collapsed;
  if(collapsed)closeOptionsMenu(true);
  root.classList.toggle('header-swap',focus); // icon swap animates only on user toggles, not on load
  try{localStorage.setItem('aca_header',collapsed?'collapsed':'open');}catch{}
  if(focus)(collapsed?$('#header-show'):$('#header-hide')).focus();
}
function bindHeaderToggle(){
  let collapsed=false;try{collapsed=localStorage.getItem('aca_header')==='collapsed';}catch{}
  setHeaderCollapsed(collapsed);
  $('#header-hide').onclick=()=>setHeaderCollapsed(true,true);
  $('#header-show').onclick=()=>setHeaderCollapsed(false,true);
}

function bindOptionsMenu(){
  const menu=$('.options-menu'),sections=$$('.options-section');
  sections.forEach(el=>el.addEventListener('toggle',()=>{
    if(el.open)sections.forEach(other=>{if(other!==el)other.open=false;});
  }));
  menu.addEventListener('toggle',()=>{if(!menu.open)sections.forEach(el=>el.open=false);});
  // <details> closes instantly, so the summary click is intercepted to play the exit first.
  menu.querySelector('summary').addEventListener('click',e=>{
    if(menu.classList.contains('closing')){e.preventDefault();menu.classList.remove('closing');}
    else if(menu.open){e.preventDefault();closeOptionsMenu();}
  });
  menu.querySelector('.options-panel').addEventListener('animationend',e=>{if(e.target===e.currentTarget&&menu.classList.contains('closing'))closeOptionsMenu(true);});
  // Dialogs opened from the menu (reset, import) handle their own clicks and Escape.
  document.addEventListener('click',e=>{if(menu.open&&!menu.contains(e.target)&&!e.target.closest('dialog'))closeOptionsMenu();});
  document.addEventListener('keydown',e=>{if(e.key==='Escape'&&menu.open&&!document.querySelector('dialog[open]')){closeOptionsMenu();menu.querySelector('summary').focus();}});
}
// Popover exit: shrinks back toward the trigger (.closing, 150ms), then closes.
// instant skips the animation (reduced motion, hidden header, animation end).
function closeOptionsMenu(instant=false){
  const menu=$('.options-menu');
  if(!menu.open)return;
  if(instant||reduceMotion()||!menu.offsetParent){menu.classList.remove('closing');menu.open=false;return;}
  if(menu.classList.contains('closing'))return;
  menu.classList.add('closing');
  setTimeout(()=>{if(menu.classList.contains('closing'))closeOptionsMenu(true);},250); // fallback if animationend is missed
}

async function init(){
  try{
    bindOptionsMenu();bindHeaderToggle();
    initTheme();
    $('#theme-toggle').onclick=toggleTheme;

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
    const topics=[...new Set(bank.questions.filter(inPractice).map(q=>q.topic))].sort();
    topics.forEach(t=>{
      for(const select of [$('#topic'),$('#exam-topic-select')]){
        if(![...select.options].some(o=>o.value===t))select.add(new Option(t,t));
      }
      if(!preciseSubtopics[t])preciseSubtopics[t]=[
        {val:'',text:`All ${t} areas`},
        ...[...new Set(bank.questions.filter(q=>inPractice(q)&&q.topic===t).map(q=>q.subtopic))].sort().map(s=>({val:s,text:s}))
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
      const pool=unexploredFirst(shuffle(available(bank.questions,prefs,'mixed',state.attempts)).map(q=>q.id),state.attempts);
      if(!pool.length){notify('No questions match these filters. Try selecting All topics.');return;}
      const length=Number($('#length-slider')?.value||$('#length')?.value||15);
      startSession(pool.slice(0,length),'mixed',prefs);
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
  if(!button||reduceMotion())return;
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
