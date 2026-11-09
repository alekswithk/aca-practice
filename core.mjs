export const STORAGE_KEY = 'aca-practice-v1';
export const emptyState = bankVersion => ({app:'aca-practice',schemaVersion:1,bankVersion,drafts:{},attempts:[],session:null,preferences:{topic:'',subtopic:'',difficulty:'',origin:''},view:'practice'});
export function shuffle(items, random=Math.random) {
  const result=[...items];
  for(let i=result.length-1;i>0;i--){const j=Math.floor(random()*(i+1));[result[i],result[j]]=[result[j],result[i]];}
  return result;
}
// "None of the others" style options always sit last, after shuffling.
export const isNoneOption=o=>/^\s*none of\b/i.test(o.text);
export function pinNoneLast(orderIds, options) {
  const byId=new Map(options.map(o=>[o.id,o]));
  const normal=orderIds.filter(id=>!isNoneOption(byId.get(id)));
  const none=orderIds.filter(id=>isNoneOption(byId.get(id)));
  return [...normal,...none];
}
export function shuffleOptions(options, random=Math.random) {
  return pinNoneLast(shuffle(options.map(o=>o.id), random), options);
}
export function grade(q, optionId) {
  if(q.status!=='validated') throw new Error('This question is excluded from scoring.');
  if(optionId===null) return 'unknown';
  if(!q.options.some(o=>o.id===optionId)) throw new Error('Choose a valid answer.');
  return optionId===q.correctOptionId?'correct':'incorrect';
}
// confidence ('sure'|'guess') is only recorded for answered practice questions.
// Attempts without it (older ones, exams, skips) count as sure.
export function makeAttempt(q,optionId,notes,timestamp,id,bankVersion,confidence){
  const outcome=grade(q,optionId);
  const attempt={id,questionId:q.id,optionId,outcome,misconception:outcome==='incorrect'?q.options.find(o=>o.id===optionId).misconception:null,notesSnapshot:notes,timestamp,bankVersion};
  if(confidence&&optionId!==null)attempt.confidence=confidence;
  return attempt;
}
export const isGuess=a=>a.outcome==='correct'&&a.confidence==='guess';
export function latestAttempts(attempts){return new Map([...attempts].sort((a,b)=>Date.parse(a.timestamp)-Date.parse(b.timestamp)).map(a=>[a.questionId,a]));}
// Questions never attempted come first (each group keeps its shuffled order),
// so a topic's unexplored questions are all asked before any repeats.
export function unexploredFirst(ids,attempts){
  const seen=new Set(attempts.map(a=>a.questionId));
  return [...ids.filter(id=>!seen.has(id)),...ids.filter(id=>seen.has(id))];
}
export function available(questions,filters,mode,attempts){
  const latest=latestAttempts(attempts);
  return questions.filter(q=>q.status==='validated' && Object.entries(filters).every(([k,v])=>!v||q[k]===v) && (mode!=='missed'||(latest.has(q.id)&&latest.get(q.id).outcome!=='correct')));
}
export function followup(q,attempt,questions,attempts){
  const candidates=questions.filter(x=>x.status==='validated' && x.origin==='generated' && x.id!==q.id && (attempt.misconception?x.targets.includes(attempt.misconception):x.subtopic===q.subtopic));
  const pool=candidates.length?candidates:questions.filter(x=>x.status==='validated' && x.id!==q.id && x.subtopic===q.subtopic);
  const latest=latestAttempts(attempts);
  return pool.sort((a,b)=>(Date.parse(latest.get(a.id)?.timestamp)||0)-(Date.parse(latest.get(b.id)?.timestamp)||0))[0]||null;
}
export function topicStats(questions,attempts){
  return [...new Set(questions.map(q=>q.topic))].map(topic=>{
    const ids=new Set(questions.filter(q=>q.topic===topic).map(q=>q.id));const rows=attempts.filter(a=>ids.has(a.questionId));
    const correct=rows.filter(a=>a.outcome==='correct').length,incorrect=rows.filter(a=>a.outcome==='incorrect').length,unknown=rows.filter(a=>a.outcome==='unknown').length;
    return {topic,total:rows.length,correct,incorrect,unknown,accuracy:correct+incorrect?Math.round(100*correct/(correct+incorrect)):null};
  });
}
// Attempts on questions that are not scored are ignored throughout.
const scoredById=questions=>new Map(questions.filter(q=>q.status==='validated').map(q=>[q.id,q]));
const byText=(x,y)=>x<y?-1:x>y?1:0;
// One entry per topic with scored questions, in first-seen order. Counts questions, not attempts.
export function topicProgress(questions, attempts){
  const scored=scoredById(questions);
  const topics=new Map();
  for(const q of scored.values()){
    if(!topics.has(q.topic)) topics.set(q.topic,{topic:q.topic,ids:new Set(),answeredIds:new Set(),wrongIds:new Set()});
    topics.get(q.topic).ids.add(q.id);
  }
  for(const a of attempts){
    const q=scored.get(a.questionId);
    if(!q) continue;
    const t=topics.get(q.topic);
    t.answeredIds.add(q.id);
    if(a.outcome==='incorrect') t.wrongIds.add(q.id);
  }
  return [...topics.values()].map(({topic,ids,answeredIds,wrongIds})=>{
    const scoredCount=ids.size, answered=answeredIds.size;
    return {topic,scored:scoredCount,answered,percentAnswered:scoredCount?Math.round(100*answered/scoredCount):0,wrongQuestions:wrongIds.size};
  });
}
// sessionAttempts drives mostMistakes; allAttempts (defaults to sessionAttempts) drives leastCovered.
export function recommendTopics(questions, sessionAttempts, allAttempts=sessionAttempts){
  const scored=scoredById(questions);
  const session=new Map();
  for(const a of sessionAttempts){
    const q=scored.get(a.questionId);
    if(!q) continue;
    const s=session.get(q.topic)??{total:0,incorrect:0};
    s.total++;
    if(a.outcome==='incorrect') s.incorrect++;
    session.set(q.topic,s);
  }
  const mistaken=[...session].filter(([,s])=>s.incorrect>0).sort(([ta,a],[tb,b])=>
    (b.incorrect-a.incorrect)||(b.incorrect/b.total-a.incorrect/a.total)||byText(ta,tb));
  const mostMistakes=mistaken.length?mistaken[0][0]:null;
  const ranked=topicProgress(questions,allAttempts).sort((a,b)=>
    (a.percentAnswered-b.percentAnswered)||(a.answered-b.answered)||byText(a.topic,b.topic));
  const leastCovered=ranked.find(t=>t.topic!==mostMistakes)?.topic??null;
  return {mostMistakes,leastCovered:ranked.length>1?leastCovered:null};
}
export function validateBackup(value,bank){
  const fail=()=>{throw new Error('Invalid or incompatible backup. Your current data has not been changed.');};
  const object=x=>x && typeof x==='object' && !Array.isArray(x);
  const str=x=>typeof x==='string';const date=x=>str(x)&&Number.isFinite(Date.parse(x));
  const qs=new Map(bank.questions.map(q=>[q.id,q]));
  const option=(id,v)=>v===null||qs.get(id)?.options.some(o=>o.id===v);
  if(!object(value)||value.app!=='aca-practice'||value.schemaVersion!==1||!str(value.bankVersion)||!object(value.drafts)||!Array.isArray(value.attempts)||!object(value.preferences))fail();
  const drafts={};
  // Questions retired from scoring (e.g. duplicates) are still in the bank.
  // Records that point at them are dropped instead of rejecting the whole backup.
  const retired=id=>qs.has(id)&&qs.get(id).status!=='validated';
  for(const [id,d] of Object.entries(value.drafts)){
    if(retired(id))continue;
    if(!qs.has(id)||!object(d)||!str(d.notes)||d.notes.length>1000000||!option(id,d.selected)||!date(d.updatedAt))fail();
    drafts[id]={notes:d.notes,selected:d.selected,updatedAt:d.updatedAt};
  }
  const ids=new Set(),dropped=new Set();const attempts=value.attempts.filter(a=>{
    if(object(a)&&retired(a.questionId)){if(str(a.id))dropped.add(a.id);return false;}
    return true;
  }).map(a=>{
    const q=qs.get(a?.questionId);
    if(!object(a)||!q||q.status!=='validated'||!str(a.id)||!a.id||ids.has(a.id)||!date(a.timestamp)||!str(a.notesSnapshot)||a.notesSnapshot.length>1000000||!str(a.bankVersion)||!option(q.id,a.optionId)||!['correct','incorrect','unknown'].includes(a.outcome))fail();
    if((a.optionId===null)!==(a.outcome==='unknown')||!(a.misconception===null||str(a.misconception))||(a.confidence!==undefined&&!['sure','guess'].includes(a.confidence)))fail();
    if(a.bankVersion===bank.bankVersion && (grade(q,a.optionId)!==a.outcome || (a.outcome==='incorrect'?q.options.find(o=>o.id===a.optionId).misconception:null)!==a.misconception))fail();
    ids.add(a.id);const out={id:a.id,questionId:q.id,optionId:a.optionId,outcome:a.outcome,misconception:a.misconception,notesSnapshot:a.notesSnapshot,timestamp:a.timestamp,bankVersion:a.bankVersion};
    if(a.confidence!==undefined)out.confidence=a.confidence;
    return out;
  });
  const preferences={};for(const k of ['topic','subtopic','difficulty','origin']){
    const v=value.preferences[k];if(!str(v)||(v&&!bank.questions.some(q=>q[k]===v)))fail();preferences[k]=v;
  }
  let session=null;
  const staleSession=s=>object(s)&&((Array.isArray(s.queue)&&s.queue.some(retired))||(Array.isArray(s.attemptIds)&&s.attemptIds.some(id=>dropped.has(id))));
  if(value.session!==null&&!staleSession(value.session)){
    const s=value.session;
    if(!object(s)||!Array.isArray(s.queue)||!s.queue.length||new Set(s.queue).size!==s.queue.length||!s.queue.every(id=>qs.get(id)?.status==='validated')||!Number.isInteger(s.index)||s.index<0||s.index>=s.queue.length||!Array.isArray(s.order)||!str(s.mode)||!['mixed','topic','missed','retry','followup','exam','exam-part1','exam-part2','exam-full','exam-topic'].includes(s.mode))fail();
    const q=qs.get(s.queue[s.index]);
    if(s.order.length!==q.options.length||new Set(s.order).size!==s.order.length||!s.order.every(id=>q.options.some(o=>o.id===id))||!Array.isArray(s.attemptIds)||!s.attemptIds.every(id=>ids.has(id)))fail();
    if(s.attemptId!==null&&!attempts.some(a=>a.id===s.attemptId&&a.questionId===q.id))fail();
    session={queue:[...s.queue],index:s.index,order:pinNoneLast(s.order,q.options),mode:s.mode,attemptId:s.attemptId,attemptIds:[...s.attemptIds]};
    if(s.scope!==undefined){
      if(!object(s.scope)||!['topic','subtopic','difficulty'].every(k=>str(s.scope[k]??'')))fail();
      session.scope={topic:s.scope.topic??'',subtopic:s.scope.subtopic??'',difficulty:s.scope.difficulty??''};
    }
    if(s.questionOrders!==undefined){
      if(!object(s.questionOrders))fail();
      for(const [id,order] of Object.entries(s.questionOrders)){
        if(!s.queue.includes(id)||!Array.isArray(order)||order.length!==qs.get(id).options.length||new Set(order).size!==order.length||!order.every(option=>qs.get(id).options.some(o=>o.id===option)))fail();
      }
      session.questionOrders=Object.fromEntries(Object.entries(s.questionOrders).map(([id,order])=>[id,pinNoneLast(order,qs.get(id).options)]));
    }
    if(s.mode.startsWith('exam')){
      const flags=s.examFlags??{};
      if(!object(flags)||Object.entries(flags).some(([id,flag])=>!s.queue.includes(id)||typeof flag!=='boolean'))fail();
      const initial=s.examInitialDuration??(s.mode==='exam-full'?5400:2700),remaining=s.examTimeRemaining??initial;
      if(!Number.isInteger(initial)||initial<=0||!Number.isInteger(remaining)||remaining<0||remaining>initial)fail();
      if(s.examTopic!=null&&(!str(s.examTopic)||!bank.questions.some(q=>q.topic===s.examTopic)))fail();
      Object.assign(session,{examFlags:{...flags},examInitialDuration:initial,examTimeRemaining:remaining,examTopic:s.examTopic??null});
    }
  }
  if(!['home','practice','history','review'].includes(value.view))fail();
  return {...emptyState(bank.bankVersion),drafts,attempts,preferences,session,view:value.view};
}
export function mergeBackups(local,incoming){
  const attempts=new Map(local.attempts.map(a=>[a.id,a]));
  // A copy saved by an older version lacks confidence; that is not a conflict, and the copy that has it is kept.
  const bare=({confidence,...rest})=>JSON.stringify(rest);
  for(const a of incoming.attempts){
    const prev=attempts.get(a.id);
    if(prev&&bare(prev)!==bare(a)) throw new Error('Conflicting attempt IDs in this backup. No data was changed.');
    if(prev?.confidence!==undefined)continue;
    attempts.set(a.id,a);
  }
  const drafts={...local.drafts};
  for(const [id,d] of Object.entries(incoming.drafts))if(!drafts[id]||Date.parse(d.updatedAt)>Date.parse(drafts[id].updatedAt))drafts[id]=d;
  return {...local,drafts,attempts:[...attempts.values()].sort((a,b)=>Date.parse(a.timestamp)-Date.parse(b.timestamp)),session:local.session||incoming.session};
}
