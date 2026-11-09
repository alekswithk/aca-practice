import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {topicProgress,recommendTopics} from '../core.mjs';
const bank=JSON.parse(readFileSync(new URL('../content/questions.json',import.meta.url)));
const questions=bank.questions;
const scored=topic=>questions.filter(q=>q.status==='validated'&&q.set!=='mock-exam'&&q.topic===topic);
const attempt=(questionId,outcome,n=0)=>({id:`${questionId}-${outcome}-${n}`,questionId,optionId:null,outcome,misconception:null,notesSnapshot:'',timestamp:`2026-11-09T10:00:${String(n).padStart(2,'0')}.000Z`,bankVersion:bank.bankVersion});
const synthetic=spec=>Object.entries(spec).flatMap(([topic,count])=>Array.from({length:count},(_,i)=>({id:`${topic}-${i}`,topic,status:'validated'})));

// Distinct questions: retrying the same question does not add to answered or wrong counts.
const auditing=scored('Auditing');
const [first,second]=auditing;
const retried=[attempt(first.id,'incorrect',1),attempt(first.id,'incorrect',2),attempt(first.id,'incorrect',3)];
let row=topicProgress(questions,retried).find(t=>t.topic==='Auditing');
assert.deepEqual(row,{topic:'Auditing',scored:auditing.length,answered:1,percentAnswered:Math.round(100/auditing.length),wrongQuestions:1});
const mixed=[attempt(first.id,'correct',1),attempt(first.id,'incorrect',2),attempt(second.id,'unknown',3)];
row=topicProgress(questions,mixed).find(t=>t.topic==='Auditing');
assert.equal(row.answered,2,'unknown responses still count as answered');
assert.equal(row.wrongQuestions,1,'a question answered correctly and later wrong counts once as wrong');
console.log('PASS: topicProgress counts distinct questions, not attempts.');

// Unscored questions and their attempts are ignored; topics without scored questions are omitted.
const review=questions.find(q=>q.status==='review');
const progressNoise=topicProgress(questions,[attempt(review.id,'incorrect',1)]);
assert.equal(progressNoise.find(t=>t.topic===review.topic)?.wrongQuestions??0,0);
assert.equal(progressNoise.find(t=>t.topic===review.topic)?.answered??0,0);
assert.deepEqual(topicProgress(synthetic({Empty:0,Real:1}),[]).map(t=>t.topic),['Real']);
assert.deepEqual(topicProgress([{id:'r',topic:'Only review',status:'review'}],[]),[]);
const order=topicProgress(questions,[]).map(t=>t.topic);
assert.deepEqual(order,[...new Set(questions.filter(q=>q.status==='validated'&&q.set!=='mock-exam').map(q=>q.topic))],'first-seen order');
console.log('PASS: topicProgress ignores unscored questions and keeps first-seen order.');

// Null cases.
assert.deepEqual(recommendTopics(questions,[]),{mostMistakes:null,leastCovered:'Auditing'},'no attempts: all topics tie at 0%, alphabetical first');
const correctOnly=[attempt(first.id,'correct',1)];
assert.equal(recommendTopics(questions,correctOnly).mostMistakes,null,'no incorrect session attempts gives null');
const single=synthetic({Solo:3});
assert.deepEqual(recommendTopics(single,[]),{mostMistakes:null,leastCovered:null},'one topic gives null leastCovered');
assert.deepEqual(recommendTopics(single,[{questionId:'Solo-0',outcome:'incorrect'}]),{mostMistakes:'Solo',leastCovered:null});
console.log('PASS: recommendTopics returns null for no mistakes and for a single topic.');

// Ties: most incorrect attempts, then higher wrong share, then alphabetical.
const tied=synthetic({Alpha:4,Beta:4,Gamma:4});
const sessionShare=[
  {questionId:'Alpha-0',outcome:'incorrect'},{questionId:'Alpha-1',outcome:'incorrect'},{questionId:'Alpha-2',outcome:'correct'},{questionId:'Alpha-3',outcome:'correct'},
  {questionId:'Beta-0',outcome:'incorrect'},{questionId:'Beta-1',outcome:'incorrect'},
];
assert.equal(recommendTopics(tied,sessionShare).mostMistakes,'Beta','equal counts: higher wrong share wins (Beta 2/2 over Alpha 2/4)');
const sessionAlpha=[
  {questionId:'Beta-0',outcome:'incorrect'},{questionId:'Alpha-0',outcome:'incorrect'},
];
assert.equal(recommendTopics(tied,sessionAlpha).mostMistakes,'Alpha','equal counts and shares: alphabetical wins');
console.log('PASS: mostMistakes tie-breaks by wrong share, then alphabetically.');

// leastCovered ties: lowest percent, then fewer answered, then alphabetical.
const coverage=synthetic({Bee:4,Cee:2,Dee:2});
const covered=[{questionId:'Bee-0',outcome:'correct'},{questionId:'Bee-1',outcome:'correct'},{questionId:'Cee-0',outcome:'correct'},{questionId:'Dee-0',outcome:'correct'},{questionId:'Dee-1',outcome:'correct'}];
// Bee 2/4 = 50%, Cee 1/2 = 50%, Dee 2/2 = 100%. Tie at 50%: fewer answered (Cee 1 vs Bee 2) wins.
assert.equal(recommendTopics(coverage,[],covered).leastCovered,'Cee');
const evenCoverage=[{questionId:'Bee-0',outcome:'correct'},{questionId:'Bee-1',outcome:'correct'},{questionId:'Cee-0',outcome:'correct'},{questionId:'Cee-1',outcome:'correct'}];
// Bee 2/4 = 50%, Cee 2/2 = 100%, Dee 0/2 = 0%: lowest percent is Dee.
assert.equal(recommendTopics(coverage,[],evenCoverage).leastCovered,'Dee');
const alphaCoverage=synthetic({Zed:2,Amy:2});
assert.equal(recommendTopics(alphaCoverage,[],[]).leastCovered,'Amy','full tie: alphabetical');
console.log('PASS: leastCovered tie-breaks by percent, then answered count, then alphabetical.');

// leastCovered must differ from mostMistakes, and uses all attempts rather than session attempts.
const sessionOnAuditing=[attempt(first.id,'incorrect',1),attempt(second.id,'incorrect',2),attempt(second.id,'incorrect',3)];
const allNone=recommendTopics(questions,sessionOnAuditing,[]);
assert.equal(allNone.mostMistakes,'Auditing');
assert.notEqual(allNone.leastCovered,'Auditing','leastCovered must not repeat mostMistakes');
assert.equal(allNone.leastCovered,'Budgeting','next-lowest after Auditing when every topic is 0%, alphabetical');
const withHistory=[...sessionOnAuditing,attempt(scored('Capital Budgeting')[0].id,'correct',9)];
const realRec=recommendTopics(questions,sessionOnAuditing,withHistory);
assert.equal(realRec.mostMistakes,'Auditing');
assert.notEqual(realRec.leastCovered,'Auditing');
assert.equal(realRec.leastCovered,'Budgeting','lowest coverage excluding Auditing: several topics at 0%, alphabetical first');
console.log('PASS: leastCovered differs from mostMistakes and is computed from all attempts.');

// Real bank: exact percent values for a topic with one answered question.
const progress=topicProgress(questions,withHistory);
assert.equal(progress.find(t=>t.topic==='Capital Budgeting').answered,1);
assert.equal(progress.find(t=>t.topic==='Capital Budgeting').percentAnswered,Math.round(100/scored('Capital Budgeting').length));
console.log('PASS: real bank percentages and recommendations.');
