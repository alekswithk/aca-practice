import assert from 'node:assert/strict';
import {readFileSync,mkdirSync} from 'node:fs';
import {createRequire} from 'node:module';
import {homedir,tmpdir} from 'node:os';
import {join} from 'node:path';
import {emptyState,makeAttempt,STORAGE_KEY,validateBackup} from '../core.mjs';
const require=createRequire(import.meta.url);
let playwright;
try{playwright=require(process.env.PLAYWRIGHT_MODULE||'playwright');}catch{playwright=require(join(homedir(),'.codex/skills/deck-design-pdf/node_modules/playwright'));}
const bank=JSON.parse(readFileSync(new URL('../content/questions.json',import.meta.url)));
const q=bank.questions.find(q=>q.status==='validated'),remote=emptyState(bank.bankVersion);
remote.drafts[q.id]={selected:q.correctOptionId,notes:'Saved on another device',updatedAt:'2026-10-28T12:00:00Z'};
remote.attempts=[makeAttempt(q,q.correctOptionId,'Saved on another device','2026-10-28T12:00:00Z','cloud-attempt',bank.bankVersion)];
const mock=`export function createClient(){
  let user=null,listener;const rows=window.testRows={a:${JSON.stringify({state:remote,revision:1})}};
  window.testAuth={signIn(id){user={id,email:id+'@example.invalid'};listener('SIGNED_IN',{user});}};
  return {auth:{
    onAuthStateChange(fn){listener=fn;return {data:{subscription:{unsubscribe(){}}}};},
    async getSession(){return {data:{session:user?{user}:null},error:null};},
    async signInWithOAuth(args){window.testOAuth=args;return {error:window.failOAuth?{message:'Google sign-in unavailable'}:null};},
    async signOut(){user=null;listener('SIGNED_OUT',null);return {error:null};}
  },from(){let id;return {select(){return this},eq(k,value){id=value;return this},async maybeSingle(){return {data:structuredClone(rows[id]??null),error:window.failCloud?{message:'Offline'}:null}}}},
  async rpc(name,args){const row=rows[user.id];if((row?.revision??0)!==args.p_expected_revision)return {data:null,error:null};rows[user.id]={state:structuredClone(args.p_state),revision:(row?.revision??0)+1};return {data:rows[user.id].revision,error:null}}};
}`;
const browser=await playwright.chromium.launch({headless:true,executablePath:process.env.PLAYWRIGHT_EXECUTABLE_PATH});
const output=process.env.ACA_TEST_OUTPUT||join(tmpdir(),'aca-cloud');mkdirSync(output,{recursive:true});
try{
  const context=await browser.newContext({viewport:{width:1440,height:1000},colorScheme:'light',reducedMotion:'reduce'});
  await context.route('https://cdn.jsdelivr.net/**',route=>route.fulfill({contentType:'text/javascript',body:mock}));
  const page=await context.newPage(),errors=[];page.on('pageerror',error=>errors.push(error.message));
  const saved=key=>page.evaluate(key=>JSON.parse(localStorage.getItem(key)),key);
  const load=async()=>{await page.goto(process.env.ACA_TEST_URL||'http://127.0.0.1:8011/');await page.locator('#google-login:not([disabled])').waitFor({state:'attached'});};
  await load();
  const announcement=page.locator('#account-announcement');
  await announcement.waitFor({state:'visible'});
  assert.equal(await page.locator('#announcement-dismiss').evaluate(el=>el===document.activeElement),true);
  for(const width of [1440,768,390]){
    await page.setViewportSize({width,height:900});
    assert.equal(await announcement.evaluate(el=>el.scrollWidth>el.clientWidth),false);
    assert.ok(await page.locator('#announcement-title').evaluate(el=>el.getBoundingClientRect().height<=2*parseFloat(getComputedStyle(el).lineHeight)+1));
    await page.screenshot({path:join(output,`announcement-${width}.png`)});
  }
  await page.locator('#announcement-login').click();
  assert.equal(await page.evaluate(()=>window.testOAuth.provider),'google');
  await page.evaluate(()=>window.failOAuth=true);await page.locator('#announcement-login').click();
  await page.locator('#announcement-status').filter({hasText:'Sign-in failed'}).waitFor();
  await page.locator('#announcement-dismiss').click();
  await load();assert.equal(await announcement.isVisible(),false,'The announcement must not repeat after reload');
  await page.setViewportSize({width:1440,height:1000});
  await page.locator('#account-panel > summary').click();
  await page.locator('#google-login').click();
  assert.equal(await page.evaluate(()=>window.testOAuth.provider),'google');
  assert.match(await page.evaluate(()=>window.testOAuth.options.redirectTo),/127\.0\.0\.1/);
  await page.evaluate(()=>window.failOAuth=true);await page.locator('#google-login').click();
  await page.locator('#cloud-status').filter({hasText:'Sign-in failed. Google sign-in unavailable'}).waitFor();
  if(!await page.locator('#session-settings').evaluate(el=>el.open))await page.locator('#session-settings > summary').click();
  await page.locator('#start').click();await page.locator('#notebook > summary').click();
  await page.locator('textarea[data-notes]').fill('Guest note');
  const guest=await saved(STORAGE_KEY);
  await page.evaluate(()=>window.testAuth.signIn('a'));
  await page.getByText('Saved to your account',{exact:true}).waitFor();
  const keyA=STORAGE_KEY+':user:a';
  assert.equal((await saved(keyA)).attempts.length,1);
  assert.equal((await saved(keyA)).drafts[q.id].notes,'Saved on another device');
  assert.equal(await page.locator('#google-login').isVisible(),false);
  assert.equal(await page.locator('#reset').isDisabled(),true);
  assert.deepEqual(await saved(STORAGE_KEY),guest,'Sign-in must preserve guest data');
  await page.locator('#merge-guest').click();
  await page.getByText('Saved to your account',{exact:true}).waitFor();
  const merged=await saved(keyA);
  for(const id of Object.keys(guest.drafts))assert.ok(merged.drafts[id]);
  await page.evaluate(()=>scrollTo(0,0));await page.screenshot({path:join(output,'account-desktop.png'),fullPage:true});
  await page.evaluate(()=>window.failCloud=true);await page.locator('#sync-now').click();
  await page.locator('#cloud-status').filter({hasText:'Cloud save failed'}).waitFor();
  assert.deepEqual(await saved(keyA),merged);
  await page.evaluate(()=>window.failCloud=false);await page.locator('#sync-now').click();
  await page.getByText('Saved to your account',{exact:true}).waitFor();
  await page.locator('#sign-out').click();
  await page.getByText('Guest progress is saved in this browser.',{exact:true}).waitFor();
  assert.equal(await page.locator('#google-login').isVisible(),true);
  assert.deepEqual(await saved(STORAGE_KEY),validateBackup(guest,bank));
  await page.evaluate(()=>window.testAuth.signIn('b'));
  await page.getByText('Saved to your account',{exact:true}).waitFor();
  assert.equal((await saved(STORAGE_KEY+':user:b')).attempts.length,0);
  assert.deepEqual((await saved(STORAGE_KEY+':user:b')).drafts,{},'Another account must not inherit notes');
  await page.setViewportSize({width:390,height:844});
  await page.evaluate(()=>scrollTo(0,0));await page.screenshot({path:join(output,'account-mobile.png'),fullPage:true});
  assert.equal(await page.evaluate(()=>document.documentElement.scrollWidth>innerWidth),false);
  await page.locator('#theme-toggle').click();
  assert.equal(await page.locator('html').evaluate(el=>el.classList.contains('dark')),true);
  await page.evaluate(()=>scrollTo(0,0));
  await page.screenshot({path:join(output,'account-mobile-dark.png'),fullPage:true});
  await page.evaluate(()=>localStorage.removeItem('aca-account-announcement-v1'));
  await load();await announcement.waitFor({state:'visible'});
  await page.screenshot({path:join(output,'announcement-dark.png')});
  await page.keyboard.press('Escape');
  await load();assert.equal(await announcement.isVisible(),false,'Escape must also dismiss the announcement permanently');
  assert.deepEqual(errors,[]);
  console.log('PASS: one-time announcement, Google login, error feedback, guest migration, cloud restore, sign-out, account isolation, mobile layout and dark mode.');
}finally{await browser.close();}
