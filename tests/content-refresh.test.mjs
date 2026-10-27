import assert from 'node:assert/strict';
import {readFileSync,mkdirSync} from 'node:fs';
import {createRequire} from 'node:module';
import {homedir,tmpdir} from 'node:os';
import {join} from 'node:path';
import {emptyState,STORAGE_KEY} from '../core.mjs';
const require=createRequire(import.meta.url);
let playwright;
try{playwright=require(process.env.PLAYWRIGHT_MODULE||'playwright');}catch{playwright=require(join(homedir(),'.codex/skills/deck-design-pdf/node_modules/playwright'));}
const bank=JSON.parse(readFileSync(new URL('../content/questions.json',import.meta.url)));
const base=process.env.ACA_TEST_URL||'http://127.0.0.1:8011';
const output=process.env.ACA_TEST_OUTPUT||join(tmpdir(),'aca-content-refresh');mkdirSync(output,{recursive:true});
const browser=await playwright.chromium.launch({headless:true,executablePath:process.env.PLAYWRIGHT_EXECUTABLE_PATH});
try{
  const page=await browser.newPage({viewport:{width:1440,height:1000}});
  const errors=[];page.on('pageerror',e=>errors.push(e.message));
  page.on('dialog',dialog=>dialog.accept());
  await page.addInitScript(()=>{Math.random=()=>.5;});
  const load=async()=>{await page.goto(base);await page.locator('#start:not([disabled])').waitFor({state:'attached'});};
  const openSetup=async()=>{if(!await page.locator('#session-settings').evaluate(el=>el.open))await page.locator('#session-settings > summary').click();};
  const saved=()=>page.evaluate(key=>JSON.parse(localStorage.getItem(key)),STORAGE_KEY);
  await load();
  for(const [topic,count] of [['Capital Budgeting',14],['Cost and Performance Management',16]]){
    assert.equal(bank.questions.filter(q=>q.topic===topic&&q.status==='validated').length,count);
    await page.selectOption('#topic',topic);
    assert.match(await page.locator('#available').textContent(),new RegExp(`^${count} matching`));
    assert.ok(await page.locator('#subtopic option').count()>1);
    assert.equal(await page.locator(`#exam-topic-select option[value="${topic}"]`).count(),1);
    await page.locator('[data-topic="'+topic+'"]').click();
    assert.ok((await saved()).session.queue.every(id=>bank.questions.find(q=>q.id===id).topic===topic));
    await page.evaluate(key=>localStorage.removeItem(key),STORAGE_KEY);
    await load();
  }

  // Every exercise table must stay available with its question, including after a reload.
  const tableQuestions=bank.questions.filter(q=>/^(cap-|cpm-)/.test(q.id)&&q.scenario.includes('|'));
  assert.equal(tableQuestions.length,7);
  for(const q of tableQuestions){
    const state=emptyState(bank.bankVersion);
    state.session={queue:[q.id],index:0,order:q.options.map(o=>o.id),mode:'retry',attemptId:null,attemptIds:[]};
    await page.evaluate(({key,state})=>localStorage.setItem(key,JSON.stringify(state)),{key:STORAGE_KEY,state});
    await load();
    const expectedRows=q.scenario.split('\n').filter(line=>line.startsWith('|')).length-2;
    assert.equal(await page.locator('.question .exercise-table tbody tr').count(),expectedRows);
    assert.equal(await page.locator('.question .exercise-table th[scope="row"]').count(),expectedRows);
    assert.equal(await page.locator('.feedback').count(),0);
    assert.equal(await page.locator('.exercise-table td.numeric').first().evaluate(el=>getComputedStyle(el).textAlign),'right');
    for(const width of [375,768,1440]){
      await page.setViewportSize({width,height:1000});
      assert.ok(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth),`${q.id} page overflow at ${width}px`);
    }
  }
  // The two source variants retain their distinct Bali assets.
  assert.ok(bank.questions.find(q=>q.id==='cpm-fritz-9.1').scenario.includes('CHF 6,000,000'));
  assert.ok(bank.questions.find(q=>q.id==='cpm-fritz-9.2').scenario.includes('CHF 5,000,000'));
  await page.screenshot({path:join(output,'eva-desktop.png'),fullPage:true});
  await page.setViewportSize({width:375,height:900});
  const table=page.locator('.exercise-table');
  await table.focus();await page.keyboard.press('End');
  assert.ok(await table.evaluate(el=>el.scrollWidth>el.clientWidth),'Wide phone table should scroll inside its container');
  await table.evaluate(el=>{el.scrollLeft=el.scrollWidth;});
  assert.ok(await table.evaluate(el=>el.scrollLeft>0));
  await page.screenshot({path:join(output,'eva-mobile.png'),fullPage:true});
  await page.locator('#notebook > summary').click();
  await page.locator('textarea[data-notes]').fill('NOPAT less the capital charge.');
  await page.locator('input[name=answer][value="a"]').check();
  await page.locator('#answer-form button[type=submit]').click();
  await page.locator('.feedback[data-outcome=correct]').waitFor();
  await page.locator('#nav-history').click();
  assert.equal(await page.locator('.history-item .exercise-table').count(),1);

  await page.setViewportSize({width:1440,height:1000});
  await page.locator('#nav-study').click();
  await openSetup();
  await page.locator('#tab-mode-exam').click();
  for(const topic of ['Capital Budgeting','Cost and Performance Management']){
    await openSetup();
    await page.locator('input[name=exam-part][value=topic]').check();
    await page.selectOption('#exam-topic-select',topic);
    await page.locator('#start-exam').click();
    assert.ok((await saved()).session.queue.every(id=>bank.questions.find(q=>q.id===id).topic===topic));
    if(topic==='Cost and Performance Management'){
      const index=(await saved()).session.queue.indexOf('cpm-fritz-9.1');
      await page.locator(`[data-jump="${index}"]`).click();
      assert.equal(await page.locator('.question .exercise-table tbody tr').count(),3);
      await page.locator('input[name=exam-answer][value=a]').check();
      await page.locator('#btn-exam-finish').click();
      assert.equal(await page.locator('.history-item .exercise-table').count(),2);
      await page.locator('#btn-exam-again').click();
    }else await page.locator('#btn-exam-cancel').click();
  }
  for(const part of ['part2','full']){
    await openSetup();
    await page.locator(`input[name=exam-part][value=${part}]`).check();
    await page.locator('#start-exam').click();
    const topics=(await saved()).session.queue.map(id=>bank.questions.find(q=>q.id===id).topic);
    assert.ok(topics.includes('Capital Budgeting'),part);
    assert.ok(topics.includes('Cost and Performance Management'),part);
    await page.locator('#btn-exam-cancel').click();
  }
  assert.deepEqual(errors,[]);
  console.log('PASS: 30 additions available in practice, focus filters and exams; seven tables retain their data, align numbers, scroll on phones and appear in history.');
  console.log('Screenshots: '+output);
}finally{await browser.close();}
