import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {emptyState,makeAttempt,validateBackup} from '../core.mjs';
const bank=JSON.parse(readFileSync(new URL('../content/questions.json',import.meta.url)));
const live=bank.questions.find(q=>q.status==='validated'),gone=bank.questions.find(q=>q.status!=='validated');

const st=emptyState(bank.bankVersion);
const a1=makeAttempt(live,live.correctOptionId,'','2026-11-01T10:00:00.000Z','a1',bank.bankVersion);
const a2={...a1,id:'a2',questionId:gone.id,optionId:gone.correctOptionId,outcome:'correct',misconception:null,bankVersion:'2026-10-01.1'};
st.attempts=[a1,a2];st.drafts[gone.id]={notes:'x',selected:null,updatedAt:'2026-11-01T10:00:00.000Z'};
st.session={queue:[live.id,gone.id],index:0,order:live.options.map(o=>o.id),mode:'mixed',attemptId:null,attemptIds:['a1','a2']};
const out=validateBackup(JSON.parse(JSON.stringify(st)),bank);
assert.deepEqual(out.attempts.map(a=>a.id),['a1']);assert.equal(out.drafts[gone.id],undefined);assert.equal(out.session,null);
console.log('PASS: records for retired questions are dropped; the rest of the saved data loads.');
