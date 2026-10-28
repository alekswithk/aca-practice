import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {createRequire} from 'node:module';
import {homedir} from 'node:os';
import {join} from 'node:path';
import {STORAGE_KEY} from '../core.mjs';

const require=createRequire(import.meta.url);
let playwright;
try{playwright=require(process.env.PLAYWRIGHT_MODULE||'playwright');}catch{playwright=require(join(homedir(),'.codex/skills/deck-design-pdf/node_modules/playwright'));}
const bank=JSON.parse(readFileSync(new URL('../content/questions.json',import.meta.url)));
const base=process.env.ACA_TEST_URL||'http://127.0.0.1:8011';
const count=topic=>bank.questions.filter(q=>q.status==='validated'&&(!topic||q.topic===topic)).length;
const browser=await playwright.chromium.launch({headless:true,executablePath:process.env.PLAYWRIGHT_EXECUTABLE_PATH});

try{
  const page=await browser.newPage();
  await page.addInitScript(()=>localStorage.setItem('aca-account-announcement-v1','seen'));
  await page.goto(base);
  await page.locator('#start:not([disabled])').waitFor();
  await page.evaluate(key=>{
    const saved=JSON.parse(localStorage.getItem(key));
    saved.preferences.origin='generated';
    localStorage.setItem(key,JSON.stringify(saved));
  },STORAGE_KEY);
  await page.reload();
  await page.locator('#start:not([disabled])').waitFor();
  assert.equal(await page.locator('#origin').inputValue(),'');
  assert.equal(Number((await page.locator('#available').textContent()).split(' ')[0]),count(''));
  await page.selectOption('#topic','Budgeting');
  assert.equal(Number((await page.locator('#available').textContent()).split(' ')[0]),count('Budgeting'));
  await page.selectOption('#topic','Variances');
  assert.equal(Number((await page.locator('#available').textContent()).split(' ')[0]),count('Variances'));
  console.log(`PASS: stale hidden source filter cleared; ${count('')} total, ${count('Budgeting')} Budgeting and ${count('Variances')} Variances questions available.`);
}finally{
  await browser.close();
}
