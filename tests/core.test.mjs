import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {emptyState,shuffle,grade,makeAttempt,available,followup,topicStats,validateBackup,mergeBackups} from '../core.mjs';
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
