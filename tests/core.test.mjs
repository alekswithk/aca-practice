import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {emptyState,shuffle,grade,makeAttempt,available,followup,topicStats,validateBackup,mergeBackups,mockExam,inPractice} from '../core.mjs';
const bank=JSON.parse(readFileSync(new URL('../content/questions.json',import.meta.url)));
const questions=bank.questions,q=questions.find(q=>q.id==='tax-01');
for(const original of questions.filter(q=>q.status==='validated')){
  for(let seed=0;seed<5;seed++){
    const order=shuffle(original.options,()=>seed/5);
    assert.deepEqual(new Set(order.map(o=>o.id)),new Set(original.options.map(o=>o.id)));
    assert.equal(order.filter(o=>grade(original,o.id)==='correct').length,1);
  }
}
assert.throws(()=>grade(questions.find(q=>q.status==='review'),'a'));
assert.throws(()=>grade(q,'missing'));
const state=emptyState(bank.bankVersion);
state.drafts[q.id]={notes:'24,000 × 20%',selected:'a',updatedAt:'2026-09-30T12:00:00.000Z'};
const wrong=makeAttempt(q,'a',state.drafts[q.id].notes,'2026-09-30T12:01:00.000Z','attempt-1',bank.bankVersion);
state.attempts.push(wrong);state.drafts[q.id].notes='Corrected: 4,800 DTL';
assert.equal(wrong.notesSnapshot,'24,000 × 20%');
const unknown=makeAttempt(q,null,'unsure','2026-09-30T12:02:00.000Z','attempt-2',bank.bankVersion);state.attempts.push(unknown);
assert.equal(unknown.outcome,'unknown');assert.equal(unknown.misconception,null);
assert.equal(available(questions,{topic:'Financial Reporting',subtopic:'Deferred taxes',origin:'generated',difficulty:''},'missed',state.attempts).length,1);
const next=followup(q,wrong,questions,state.attempts);assert.notEqual(next.id,q.id);assert.ok(next.targets.includes('tax-rate-omitted'));
state.session={queue:[q.id],index:0,order:shuffle(q.options.map(o=>o.id)),mode:'retry',attemptId:unknown.id,attemptIds:[unknown.id]};
const restored=validateBackup(JSON.parse(JSON.stringify(state)),bank);assert.deepEqual(restored,state);
assert.deepEqual(validateBackup({...structuredClone(state),view:'home'},bank),{...state,view:'home'},'Home backups must preserve the current session and learning data');
assert.deepEqual(mergeBackups(state,restored),state);
const fresh=mergeBackups(emptyState(bank.bankVersion),restored);assert.deepEqual(fresh.attempts,state.attempts);assert.deepEqual(fresh.drafts,state.drafts);assert.deepEqual(fresh.session,state.session);
const correct=makeAttempt(q,q.correctOptionId,'4,800 liability','2026-09-30T12:03:00.000Z','attempt-3',bank.bankVersion);state.attempts.push(correct);
assert.equal(available(questions,{},'missed',state.attempts).length,0);assert.equal(state.attempts.length,3);
const stats=topicStats(questions,state.attempts).find(s=>s.topic===q.topic);assert.deepEqual([stats.total,stats.correct,stats.incorrect,stats.unknown,stats.accuracy],[3,1,1,1,50]);
for(const mutate of [s=>s.attempts[0].optionId='missing',s=>s.attempts[0].outcome='correct',s=>s.drafts['not-a-question']={},s=>s.session.order=['a','a','b','c'],s=>s.attempts.push(s.attempts[0]),s=>s.app='different-app']){
 const bad=JSON.parse(JSON.stringify(restored));mutate(bad);assert.throws(()=>validateBackup(bad,bank));
}
const conflict=JSON.parse(JSON.stringify(restored));conflict.attempts[0].notesSnapshot='different';assert.throws(()=>mergeBackups(restored,conflict));
const newer=JSON.parse(JSON.stringify(restored));newer.drafts[q.id].updatedAt='2026-10-01T12:00:00.000Z';newer.drafts[q.id].notes='Newest draft';assert.equal(mergeBackups(restored,newer).drafts[q.id].notes,'Newest draft');
console.log('PASS: shuffled grading for every scored question, snapshots, unknown responses, filters, retries, follow-ups, statistics, backup round trips and invalid/conflicting imports.');

// An existing browser profile upgrades the bank without losing drafts, attempts or option order.
const legacy=structuredClone(restored);legacy.bankVersion='2026-09-30.1';legacy.attempts.forEach(a=>a.bankVersion=legacy.bankVersion);
const upgraded=validateBackup(legacy,bank);assert.equal(upgraded.bankVersion,bank.bankVersion);assert.deepEqual(upgraded.attempts,legacy.attempts);assert.deepEqual(upgraded.drafts,legacy.drafts);assert.deepEqual(upgraded.session,legacy.session);
const sourceMA=questions.filter(q=>q.topic==='Management Accounting'&&!q.aiGenerated);
assert.equal(available(sourceMA,{topic:'Management Accounting'},'mixed',[]).length,43);
assert.equal(sourceMA.filter(q=>q.status==='review').length,8);
assert.equal(sourceMA.length,51);
assert.equal(available(questions,{topic:'Management Accounting'},'mixed',[]).length,43+20+14,'20 AI practice questions and 14 practice-exam questions join the Management Accounting pool');
console.log('PASS: legacy bank upgrade preserves learning data; all 51 management questions imported, 43 scored and 8 excluded; 20 AI questions added.');

// AI-generated questions: 20 practice questions per topic, plus a separate 50-question mock exam that never enters practice pools.
const topics=[...new Set(questions.filter(q=>!q.aiGenerated).map(q=>q.topic))];
for(const topic of topics)assert.equal(questions.filter(q=>q.aiGenerated&&q.set==='bank'&&q.topic===topic&&!q.id.startsWith('pe')).length,20,topic);
assert.equal(questions.filter(q=>q.aiGenerated&&q.set==='bank'&&q.id.startsWith('pe-')).length,51,'practice exam 1');
assert.equal(questions.filter(q=>q.aiGenerated&&q.set==='bank'&&q.id.startsWith('pe2-')).length,53,'practice exam 2');
const mock=mockExam(questions);
assert.equal(mock.length,50);assert.deepEqual(mock.map(q=>q.examOrder),Array.from({length:50},(_,i)=>i+1));
assert.equal(mockExam(questions,1).length,30);assert.equal(mockExam(questions,2).length,20);
assert.equal(mockExam(questions,1).reduce((s,q)=>s+q.marks,0),45);assert.equal(mockExam(questions,2).reduce((s,q)=>s+q.marks,0),45);
assert.ok(mock.every(q=>q.aiGenerated&&!inPractice(q)));
const practiceIds=new Set(available(questions,{},'mixed',[]).map(q=>q.id));
assert.ok(mock.every(q=>!practiceIds.has(q.id)),'mock questions never appear in practice');
for(const m of mock){const a=makeAttempt(m,m.options.find(o=>o.id!==m.correctOptionId).id,'','2026-11-09T12:00:00Z','x',bank.bankVersion);const f=followup(m,a,questions,[]);assert.ok(!f||f.set!=='mock-exam');}
const mockState=emptyState(bank.bankVersion);
mockState.session={queue:mock.map(q=>q.id),index:0,order:mock[0].options.map(o=>o.id),mode:'exam-full',attemptId:null,attemptIds:[],examFlags:{},examInitialDuration:5400,examTimeRemaining:5400,examTopic:null,examSource:'mock'};
assert.deepEqual(validateBackup(structuredClone(mockState),bank),mockState,'AI mock exam session survives a backup/reload');
const badSource=structuredClone(mockState);badSource.session.examSource='other';assert.throws(()=>validateBackup(badSource,bank));
console.log('PASS: 20 AI practice questions per topic; 50-question AI mock exam (45 + 45 marks) kept out of practice, mixed exams and follow-ups.');

const exam=emptyState(bank.bankVersion);
exam.session={queue:[q.id],index:0,order:q.options.map(o=>o.id),mode:'exam-topic',attemptId:null,attemptIds:[],examFlags:{[q.id]:true},examInitialDuration:2700,examTimeRemaining:1850,examTopic:q.topic};
assert.deepEqual(validateBackup(structuredClone(exam),bank),exam,'Exam flags, countdown and scope survive a backup/reload');
for(const mutate of [s=>s.examFlags.missing=true,s=>s.examFlags[q.id]='true',s=>s.examTimeRemaining=-1,s=>s.examTimeRemaining=2701,s=>s.examInitialDuration=0,s=>s.examTopic='Missing topic']){
 const bad=structuredClone(exam);mutate(bad.session);assert.throws(()=>validateBackup(bad,bank));
}
console.log('PASS: exam state round trip and invalid flag/timer/scope rejection.');

const navigation=structuredClone(restored);
navigation.session.questionOrders={[q.id]:q.options.map(o=>o.id)};
assert.deepEqual(validateBackup(navigation,bank),navigation,'Practice answer order survives navigation and backups');
for(const orders of [null,[],{missing:['a']},{[q.id]:['a','a','b','c']},{[q.id]:['missing']},{[q.id]:'abcd'}]){
 const bad=structuredClone(navigation);bad.session.questionOrders=orders;assert.throws(()=>validateBackup(bad,bank));
}
console.log('PASS: practice navigation order round trip and invalid cached-order rejection.');
{
 const {unexploredFirst}=await import('../core.mjs');
 const attempts=[{questionId:'b'},{questionId:'d'}];
 assert.deepEqual(unexploredFirst(['b','a','d','c'],attempts),['a','c','b','d'],'Unexplored questions come first, each group keeps its order');
 assert.deepEqual(unexploredFirst(['a','b'],[]),['a','b']);
 const scoped=structuredClone(navigation);scoped.session.scope={topic:'Financial Reporting',subtopic:'Deferred taxes',difficulty:''};
 assert.deepEqual(validateBackup(scoped,bank).session.scope,scoped.session.scope,'Session scope survives backups');
 const badScope=structuredClone(navigation);badScope.session.scope={topic:5};assert.throws(()=>validateBackup(badScope,bank));
 console.log('PASS: unexplored-first ordering and session scope round trip.');
}
