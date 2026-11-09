import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {emptyState,makeAttempt,isGuess,validateBackup,mergeBackups} from '../core.mjs';
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
