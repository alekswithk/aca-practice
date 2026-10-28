import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {emptyState,makeAttempt,validateBackup} from '../core.mjs';
import {createProgressSync,progressKey} from '../cloud.mjs';
const bank=JSON.parse(readFileSync(new URL('../content/questions.json',import.meta.url)));
const q=bank.questions.find(q=>q.status==='validated');
const fresh=()=>emptyState(bank.bankVersion);
const attempt=id=>makeAttempt(q,q.correctOptionId,id,'2026-10-28T12:00:00Z',id,bank.bankVersion);
let local=fresh(),remote=null,status='',writes=0,readHook=null,writeHook=null,failure=null;
const client={
  from(){return {select(){return this;},eq(_column,id){assert.equal(id,'user-a');return this;},async maybeSingle(){
    if(readHook)await readHook();
    return {data:structuredClone(remote),error:failure};
  }};},
  async rpc(name,args){
    assert.equal(name,'save_progress');writes++;
    if(writeHook)await writeHook();
    if(args.p_expected_revision!==(remote?.revision??0))return {data:null,error:null};
    remote={state:structuredClone(args.p_state),revision:(remote?.revision??0)+1};
    return {data:remote.revision,error:null};
  },
};
const sync=createProgressSync({client,getState:()=>local,applyState:s=>{local=s;},validate:s=>validateBackup(s,bank),onStatus:s=>{status=s;}});
assert.notEqual(progressKey('progress','a'),progressKey('progress','b'));
assert.equal(progressKey('progress',null),'progress');
sync.setUser('user-a',true);
local.attempts=[attempt('local')];
assert.equal(await sync.flush(),true);assert.equal(remote.state.attempts.length,1);
remote.state.attempts.push(attempt('other-device'));remote.revision++;
local.attempts.push(attempt('offline'));
assert.equal(await sync.flush(),true);
assert.deepEqual(new Set(remote.state.attempts.map(a=>a.id)),new Set(['local','other-device','offline']));
// A concurrent cloud write between read and save forces a fresh merge.
writeHook=()=>{writeHook=null;remote.state.attempts.push(attempt('racing-device'));remote.revision++;};
assert.equal(await sync.flush(),true);assert.ok(remote.state.attempts.some(a=>a.id==='racing-device'));
// Edits made while a request is running must also reach the database.
writeHook=()=>{writeHook=null;local.attempts.push(attempt('typed-during-save'));sync.schedule();};
assert.equal(await sync.flush(),true);assert.ok(remote.state.attempts.some(a=>a.id==='typed-during-save'));
assert.equal(status,'Saved to your account');
const session={queue:[q.id],index:0,order:q.options.map(o=>o.id),mode:'mixed',attemptId:null,attemptIds:[]};
remote.state.session=structuredClone(session);
local.session=null;
assert.equal(await sync.flush(),true);assert.equal(local.session,null,'A finished session must not be resurrected');
remote.state.session=structuredClone(session);remote.state.view='home';local=fresh();
sync.setUser('user-a',true);assert.equal(await sync.flush(),true);
assert.deepEqual(local.session,session);assert.equal(local.view,'home','A new device restores cloud session and view');
// Invalid remote data and transport failures leave local progress untouched.
const before=structuredClone(local),beforeWrites=writes;
remote.state={bad:true};assert.equal(await sync.flush(),false);assert.deepEqual(local,before);assert.equal(writes,beforeWrites);
failure={message:'Offline'};assert.equal(await sync.flush(),false);assert.match(status,/Cloud save failed/);assert.deepEqual(local,before);failure=null;
// An old account's pending request cannot update the next account or guest UI.
let release;
readHook=()=>new Promise(resolve=>{release=resolve;});
const pending=sync.flush();sync.setUser(null);local=fresh();status='Guest';release();
assert.equal(await pending,false);assert.deepEqual(local,fresh());assert.equal(status,'Guest');assert.equal(writes,beforeWrites);
readHook=null;
console.log('PASS: cloud merge, revision conflicts, in-flight edits, session restore, failures, validation and account isolation.');
