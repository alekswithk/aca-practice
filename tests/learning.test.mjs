import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {emptyState,makeAttempt,isGuess,validateBackup,mergeBackups,reviewQueue,topicBreakdown,flaggedIds} from '../core.mjs';
const bank=JSON.parse(readFileSync(new URL('../content/questions.json',import.meta.url)));
const scored=bank.questions.filter(q=>q.status==='validated');
const [q1,q2,q3]=scored;
const wrongOption=q=>q.options.find(o=>o.id!==q.correctOptionId).id;
const at=(day,hour=10)=>new Date(Date.UTC(2026,10,day,hour)).toISOString();
let n=0;
const attempt=(q,kind,time,confidence)=>makeAttempt(q,kind==='correct'?q.correctOptionId:kind==='unknown'?null:wrongOption(q),'',time,`a${++n}`,bank.bankVersion,confidence);

// Confidence: stored only on answered attempts, validated, round-tripped and tolerated by merges.
{
  const guess=attempt(q1,'correct',at(1),'guess'),sure=attempt(q2,'incorrect',at(1),'sure'),skip=attempt(q3,'unknown',at(1),'guess'),plain=attempt(q3,'correct',at(2));
  assert.equal(guess.confidence,'guess');assert.equal(sure.confidence,'sure');
  assert.equal('confidence' in skip,false,'a skip has no confidence');assert.equal('confidence' in plain,false,'exam attempts carry no confidence');
  assert.equal(isGuess(guess),true);assert.equal(isGuess(sure),false);assert.equal(isGuess(plain),false);
  assert.equal(isGuess({...sure,confidence:'guess'}),false,'a wrong guess is just wrong');
  const state=emptyState(bank.bankVersion);state.attempts=[guess,sure,skip,plain];
  const restored=validateBackup(structuredClone(state),bank);
  assert.deepEqual(restored.attempts,state.attempts,'confidence survives a backup; old attempts stay without it');
  const bad=structuredClone(state);bad.attempts[0].confidence='maybe';assert.throws(()=>validateBackup(bad,bank));
  // A copy written by an older version drops confidence. Merging keeps the copy that has it, in either direction.
  const old=structuredClone(restored);delete old.attempts[0].confidence;
  assert.equal(mergeBackups(restored,old).attempts.find(a=>a.id===guess.id).confidence,'guess');
  assert.equal(mergeBackups(old,restored).attempts.find(a=>a.id===guess.id).confidence,'guess');
  const conflict=structuredClone(restored);conflict.attempts[0].notesSnapshot='changed';assert.throws(()=>mergeBackups(restored,conflict));
  console.log('PASS: confidence is optional, validated, survives backups and merges with copies that lack it.');
}

// Spaced review from attempt history.
{
  const R=(attempts,now)=>reviewQueue(bank.questions,attempts,now);
  assert.deepEqual(R([],at(5)),{due:[],pending:0,nextAt:null});
  assert.deepEqual(R([attempt(q1,'correct',at(1))],at(9)),{due:[],pending:0,nextAt:null},'a sure correct answer never needs review');
  for(const kind of ['incorrect','unknown']){
    const a=[attempt(q1,kind,at(1))];
    assert.deepEqual(R(a,at(1,12)),{due:[],pending:1,nextAt:at(2)},`${kind}: not due before a day has passed`);
    assert.deepEqual(R(a,at(2)).due,[q1.id],`${kind}: due exactly one day later`);
  }
  assert.deepEqual(R([attempt(q1,'correct',at(1),'guess')],at(2)).due,[q1.id],'a correct guess is due a day later');
  assert.deepEqual(R([attempt(q1,'correct',at(1),'sure')],at(2)).due,[],'a correct sure answer is not');
  // Wrong, then right once when due: a final check 3 days later. Right again then: cleared.
  const wrong=attempt(q1,'incorrect',at(1)),first=attempt(q1,'correct',at(2,12),'sure'),second=attempt(q1,'correct',at(5,12),'sure');
  assert.deepEqual(R([wrong,first],at(3)),{due:[],pending:1,nextAt:at(5,12)});
  assert.deepEqual(R([wrong,first],at(5,12)).due,[q1.id]);
  assert.deepEqual(R([wrong,first,second],at(9)),{due:[],pending:0,nextAt:null},'cleared after the final check');
  // Order of the attempt list does not matter; history is sorted by time.
  assert.deepEqual(R([second,wrong,first],at(9)).due,[]);
  // Correct answers before the due time do not count.
  const early=attempt(q1,'correct',at(1,11),'sure');
  assert.deepEqual(R([wrong,early],at(2)).due,[q1.id],'answering right an hour later does not clear it');
  assert.deepEqual(R([wrong,first,attempt(q1,'correct',at(3),'sure')],at(5,12)).due,[q1.id],'nor does an early answer during the 3-day wait');
  // A guess or a miss at any stage starts over at one day.
  assert.deepEqual(R([wrong,first,attempt(q1,'correct',at(5,12),'guess')],at(6)),{due:[],pending:1,nextAt:at(6,12)});
  assert.deepEqual(R([wrong,first,attempt(q1,'incorrect',at(3))],at(4)).due,[q1.id]);
  // Several questions: oldest due first; nextAt is the soonest upcoming one; retired questions are ignored.
  const retired=bank.questions.find(q=>q.status!=='validated');
  const many=[attempt(q2,'incorrect',at(2)),attempt(q1,'incorrect',at(1)),attempt(q3,'incorrect',at(4)),{...attempt(q1,'incorrect',at(1)),questionId:retired.id}];
  assert.deepEqual(R(many,at(3,12)),{due:[q1.id,q2.id],pending:1,nextAt:at(5)});
  assert.deepEqual(R(many,new Date(at(3,12)).getTime()).due,[q1.id,q2.id],'now may be a timestamp in ms');
  // Review sessions survive a backup.
  const state=emptyState(bank.bankVersion);state.attempts=[wrong];
  state.session={queue:[q1.id],index:0,order:q1.options.map(o=>o.id),mode:'review',attemptId:null,attemptIds:[]};
  assert.deepEqual(validateBackup(structuredClone(state),bank),state);
  console.log('PASS: due-for-review rules (1 day, 3-day final check, early answers ignored, restarts) and review sessions.');
}

// Exam score by topic, weakest share first.
{
  const topic=t=>scored.filter(q=>q.topic===t);
  const [fr1,fr2]=topic('Financial Reporting'),[au1,au2]=topic('Auditing'),[cs1]=topic('Consolidated Statements'),[bu1]=topic('Budgeting');
  const retired=bank.questions.find(q=>q.status!=='validated');
  const rows=[attempt(fr1,'correct',at(1)),attempt(fr2,'incorrect',at(1)),attempt(au1,'unknown',at(1)),attempt(au2,'incorrect',at(1)),attempt(cs1,'correct',at(1)),attempt(bu1,'incorrect',at(1)),{...attempt(fr1,'correct',at(1)),questionId:retired.id}];
  assert.deepEqual(topicBreakdown(bank.questions,rows),[
    {topic:'Auditing',correct:0,total:2},{topic:'Budgeting',correct:0,total:1},
    {topic:'Financial Reporting',correct:1,total:2},{topic:'Consolidated Statements',correct:1,total:1},
  ],'worst share first; ties put the larger topic first, then by name; unscored questions are left out');
  assert.deepEqual(topicBreakdown(bank.questions,[]),[]);
  console.log('PASS: exam topic breakdown.');
}

// Practice flags: optional in backups, newest choice wins on merge, so unflagging sticks.
{
  const base=emptyState(bank.bankVersion);
  assert.deepEqual(base.flags,{});
  const legacy=structuredClone(base);delete legacy.flags;
  assert.deepEqual(validateBackup(legacy,bank).flags,{},'backups from before flags still load');
  const retired=bank.questions.find(q=>q.status!=='validated');
  const state={...structuredClone(base),flags:{[q1.id]:{flagged:true,updatedAt:at(1)},[q2.id]:{flagged:false,updatedAt:at(1)},[retired.id]:{flagged:true,updatedAt:at(1)}}};
  const restored=validateBackup(structuredClone(state),bank);
  assert.deepEqual(restored.flags,{[q1.id]:state.flags[q1.id],[q2.id]:state.flags[q2.id]},'flags round trip; retired questions are dropped');
  assert.deepEqual(flaggedIds(bank.questions,restored.flags),[q1.id]);
  assert.deepEqual(flaggedIds(bank.questions,undefined),[]);
  for(const flags of [[],'x',{missing:{flagged:true,updatedAt:at(1)}},{[q1.id]:true},{[q1.id]:{flagged:'yes',updatedAt:at(1)}},{[q1.id]:{flagged:true,updatedAt:'never'}}]){
    assert.throws(()=>validateBackup({...structuredClone(base),flags},bank),undefined,JSON.stringify(flags));
  }
  // Flags set on either side are kept; for the same question the newer change wins.
  const a={...structuredClone(restored),flags:{[q1.id]:{flagged:false,updatedAt:at(3)},[q3.id]:{flagged:true,updatedAt:at(2)}}};
  const merged=mergeBackups(a,restored);
  assert.deepEqual(merged.flags,{[q1.id]:{flagged:false,updatedAt:at(3)},[q2.id]:{flagged:false,updatedAt:at(1)},[q3.id]:{flagged:true,updatedAt:at(2)}});
  assert.deepEqual(mergeBackups(restored,a).flags,merged.flags,'merge order does not matter');
  assert.deepEqual(flaggedIds(bank.questions,merged.flags),[q3.id]);
  assert.deepEqual(mergeBackups(legacy,restored).flags,restored.flags,'a local copy without flags takes the incoming ones');
  // Flagged sessions survive a backup.
  const session={...structuredClone(restored),session:{queue:[q1.id],index:0,order:q1.options.map(o=>o.id),mode:'flagged',attemptId:null,attemptIds:[]}};
  assert.deepEqual(validateBackup(structuredClone(session),bank),session);
  console.log('PASS: practice flags validate, round trip, merge by newest change and start flagged sessions.');
}
