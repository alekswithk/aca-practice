// Optional browser regression check. The study app itself has no dependencies.
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
const output=process.env.ACA_TEST_OUTPUT||join(tmpdir(),'aca-practice-check');mkdirSync(output,{recursive:true});
const browser=await playwright.chromium.launch({headless:true});
try{
 const context=await browser.newContext({viewport:{width:1440,height:1000},acceptDownloads:true});const page=await context.newPage();
 const errors=[];page.on('pageerror',e=>errors.push(e.message));
 const load=async()=>{await page.goto(base);await page.locator('#start:not([disabled])').waitFor();};
 const data=()=>page.evaluate(key=>JSON.parse(localStorage.getItem(key)),STORAGE_KEY);
 await load();assert.equal(await page.locator('#review-count').textContent(),`(${bank.questions.filter(q=>q.status==='review').length})`);
 await page.selectOption('#topic','Financial Reporting');await page.selectOption('#difficulty','Hard');await page.selectOption('#origin','original');
 assert.equal(Number((await page.locator('#available').textContent()).split(' ')[0]),bank.questions.filter(q=>q.status==='validated'&&q.topic==='Financial Reporting'&&q.difficulty==='Hard'&&q.origin==='original').length);
 await page.locator('#tax-focus').hover();await page.mouse.down();await page.waitForFunction(()=>new DOMMatrix(getComputedStyle(document.querySelector('#tax-focus')).transform).a<.999);assert.equal((await data()).session,null,'Press feedback must happen before committing the action');await page.mouse.up();let state=await data();const firstId=state.session.queue[0],q=bank.questions.find(q=>q.id===firstId);assert.equal(q.subtopic,'Deferred taxes');assert.equal(q.origin,'generated');assert.equal(await page.locator('.question').evaluate(el=>el.getAnimations().length),0,'Frequently used questions must appear immediately');
 assert.equal(await page.locator('.feedback').count(),0);assert.equal(await page.getByText('Preserved original question',{exact:false}).count(),0);
 const draft='Difference first, then multiply by the rate.';await page.locator('textarea[data-notes]').fill(draft);
 const wrong=q.options.find(o=>o.misconception==='tax-rate-omitted');assert.ok(wrong);
 await page.locator(`input[name=answer][value="${wrong.id}"]`).check();
 const initialOrder=(await data()).session.order;assert.deepEqual(await page.locator('.option span').allTextContents().then(rows=>rows.map(x=>x.slice(0,3))),initialOrder.map((_,i)=>String.fromCharCode(65+i)+'. '),'Displayed labels must follow shuffled order');
 await page.reload();await page.locator('textarea[data-notes]').waitFor();assert.equal(await page.locator('textarea[data-notes]').inputValue(),draft);
 assert.equal(await page.locator(`input[value="${wrong.id}"]`).isChecked(),true);assert.deepEqual((await data()).session.order,initialOrder);
 await page.getByRole('button',{name:'Submit answer',exact:true}).click();await page.locator('.feedback[data-outcome=incorrect]').waitFor();
 assert.match(await page.locator('.feedback').textContent(),new RegExp('Correct answer: '+String.fromCharCode(65+initialOrder.indexOf(q.correctOptionId))+'\\.'));
 assert.equal((await data()).attempts[0].notesSnapshot,draft);assert.equal(await page.locator('.feedback').evaluate(el=>getComputedStyle(el).transitionDuration),'0.16s, 0.16s');
 assert.match(await page.locator('#feedback').textContent(),/Misconception/);
 await page.locator('textarea[data-notes]').fill('Revised after feedback: apply the tax rate.');
 await page.reload();await page.locator('.feedback').waitFor();state=await data();assert.equal(state.attempts.length,1);assert.equal(state.attempts[0].notesSnapshot,draft);assert.equal(state.drafts[firstId].notes,'Revised after feedback: apply the tax rate.');
 await page.getByRole('button',{name:'Try a relevant follow-up'}).click();state=await data();assert.notEqual(state.session.queue[state.session.index],firstId);
 const follow=bank.questions.find(q=>q.id===state.session.queue[state.session.index]);assert.ok(follow.targets.includes('tax-rate-omitted'));
 await page.getByRole('button',{name:'I don’t know',exact:true}).click();await page.locator('.feedback[data-outcome=unknown]').waitFor();assert.equal((await data()).attempts[1].outcome,'unknown');
 await page.getByRole('button',{name:'Learning history',exact:true}).click();assert.match(await page.locator('tbody').textContent(),/50|0/);
 await page.locator(`[data-retry="${firstId}"]`).first().click();assert.equal(await page.locator('.feedback').count(),0);
 await page.locator(`input[name=answer][value="${q.correctOptionId}"]`).check();await page.getByRole('button',{name:'Submit answer',exact:true}).click();await page.locator('.feedback[data-outcome=correct]').waitFor();
 state=await data();assert.equal(state.attempts.length,3);assert.deepEqual(state.attempts.map(a=>a.outcome),['incorrect','unknown','correct']);assert.equal(state.attempts[0].notesSnapshot,draft);
 await page.getByRole('button',{name:'Learning history',exact:true}).click();const row=page.locator('tbody tr').filter({hasText:'Financial Reporting'});assert.match(await row.textContent(),/50%/);
 await page.getByRole('button',{name:/Source review/}).click();assert.equal(await page.locator('.review-item').count(),bank.questions.filter(q=>q.status==='review').length);const review=page.locator('.review-item').first();await review.locator('summary').first().click();await review.locator('textarea').fill('Ask why this has two correct options.');
 await page.reload();await page.locator('.review-item').first().waitFor();assert.equal(await page.locator('.review-item').first().locator('textarea').inputValue(),'Ask why this has two correct options.');
 const downloadPromise=page.waitForEvent('download');await page.click('#export');const exported=await downloadPromise;const exportPath=await exported.path();const backup=JSON.parse(readFileSync(exportPath,'utf8'));assert.equal(backup.attempts.length,3);assert.equal(backup.attempts[0].notesSnapshot,draft);
 await page.click('#reset');await page.locator('#reset-dialog[open]').waitFor();await page.keyboard.press('Escape');assert.equal((await data()).attempts.length,3);
 await page.click('#reset');await page.locator('#reset-dialog button[value=confirm]').click();await page.waitForFunction(key=>JSON.parse(localStorage.getItem(key)).attempts.length===0,STORAGE_KEY);assert.equal((await data()).attempts.length,0);
 const upload=()=>page.locator('#import').setInputFiles({name:'backup.json',mimeType:'application/json',buffer:Buffer.from(JSON.stringify(backup))});
 await upload();await page.locator('#import-dialog[open]').waitFor();await page.locator('#import-dialog button[value=cancel]').click();assert.equal((await data()).attempts.length,0);
 await upload();await page.locator('#import-dialog button[value=confirm]').click();await page.waitForFunction(key=>JSON.parse(localStorage.getItem(key)).attempts.length===3,STORAGE_KEY);assert.equal((await data()).attempts.length,3);assert.deepEqual((await data()).drafts,backup.drafts);
 await upload();await page.locator('#import-dialog button[value=confirm]').click();await page.waitForFunction(key=>JSON.parse(localStorage.getItem(key)).attempts.length===3,STORAGE_KEY);assert.equal((await data()).attempts.length,3);
 await page.click('#reset');await page.locator('#reset-dialog[open]').waitFor();await page.keyboard.press('Escape');await page.locator('#reset-dialog').waitFor({state:'hidden'});assert.equal((await data()).attempts.length,3);
 const cancelledBackup=structuredClone(backup);cancelledBackup.drafts[firstId].notes='Never merge this cancelled draft';cancelledBackup.drafts[firstId].updatedAt='2050-01-01T00:00:00.000Z';
 await page.locator('#import').setInputFiles({name:'cancelled.json',mimeType:'application/json',buffer:Buffer.from(JSON.stringify(cancelledBackup))});await page.locator('#import-dialog[open]').waitFor();await page.keyboard.press('Escape');await page.locator('#import-dialog').waitFor({state:'hidden'});assert.equal((await data()).drafts[firstId].notes,backup.drafts[firstId].notes);
 await page.locator('#import').setInputFiles({name:'bad.json',mimeType:'application/json',buffer:Buffer.from('{"app":"bad"}')});await page.waitForFunction(()=>document.querySelector('#notice').textContent.includes('Invalid'));assert.equal((await data()).attempts.length,3);assert.match(await page.locator('#notice').textContent(),/Invalid/);
 await page.getByRole('button',{name:'Practice',exact:true}).click();await page.screenshot({path:output+'/desktop.png',fullPage:true,animations:'disabled'});
 for(const width of [375,768,1024,1440]){await page.setViewportSize({width,height:900});assert.ok(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth),`overflow at ${width}`);}
 await page.setViewportSize({width:375,height:900});await page.waitForFunction(()=>document.querySelector('#notebook').parentElement.id==='notebook-slot');assert.ok(await page.evaluate(()=>!!(document.querySelector('#notebook').compareDocumentPosition(document.querySelector('#feedback'))&Node.DOCUMENT_POSITION_FOLLOWING)),'Mobile notebook must precede feedback');await page.emulateMedia({reducedMotion:'reduce'});assert.equal(await page.locator('.question').evaluate(el=>getComputedStyle(el).animationName),'none');await page.screenshot({path:output+'/mobile.png',fullPage:true,animations:'disabled'});
 await page.evaluate(()=>document.documentElement.style.fontSize='24px');assert.ok(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth),'overflow with large text');await page.evaluate(()=>document.documentElement.style.fontSize='16px');
 // Close and reopen a page in the same browser profile: storage survives the closure.
 await page.close();const reopened=await context.newPage();await reopened.goto(base);await reopened.locator('textarea[data-notes]').waitFor();assert.equal(await reopened.locator('textarea[data-notes]').inputValue(),backup.drafts[firstId].notes);
 // A separate fresh context tests keyboard selection and submission.
 const keyboardContext=await browser.newContext();const keyboardPage=await keyboardContext.newPage();await keyboardPage.goto(base);await keyboardPage.locator('#start:not([disabled])').waitFor();
 await keyboardPage.keyboard.press('Tab');assert.equal(await keyboardPage.locator('.skip').evaluate(el=>el===document.activeElement),true);await keyboardPage.keyboard.press('Enter');assert.equal(await keyboardPage.locator('#main').evaluate(el=>el===document.activeElement),true);
 await keyboardPage.setViewportSize({width:375,height:900});await keyboardPage.locator('#tax-focus').focus();await keyboardPage.keyboard.press('Enter');assert.ok(await keyboardPage.evaluate(()=>!!(document.querySelector('#notebook').compareDocumentPosition(document.querySelector('#answer-form button[type=submit]'))&Node.DOCUMENT_POSITION_FOLLOWING)),'Mobile notes must precede submission');await keyboardPage.locator('input[name=answer]').first().focus();await keyboardPage.keyboard.press('Space');await keyboardPage.keyboard.press('ArrowDown');assert.equal(await keyboardPage.locator('input[name=answer]:checked').count(),1);
 assert.equal(await keyboardPage.locator('input[name=answer]:checked').evaluate(el=>getComputedStyle(el).outlineStyle),'solid');
 await keyboardPage.getByRole('button',{name:'Submit answer',exact:true}).focus();await keyboardPage.keyboard.press('Enter');await keyboardPage.locator('.feedback').waitFor();assert.equal(await keyboardPage.locator('#feedback-heading').evaluate(el=>el===document.activeElement),true);assert.equal(await keyboardPage.evaluate(()=>document.documentElement.dataset.input),'keyboard');assert.equal(await keyboardPage.locator('.feedback').evaluate(el=>getComputedStyle(el).transitionDuration),'0s');assert.equal(await keyboardPage.locator('.feedback').evaluate(el=>el.getAnimations().length),0);
 // New topic cards route to validated Management Accounting questions, including five-option questions.
 const maContext=await browser.newContext({viewport:{width:1440,height:1000}});const maPage=await maContext.newPage();await maPage.goto(base);await maPage.locator('[data-topic="Management Accounting"]').waitFor();
 await maPage.screenshot({path:output+'/welcome.png',fullPage:true,animations:'disabled'});await maPage.setViewportSize({width:375,height:900});await maPage.reload();await maPage.locator('.study-hero').waitFor();assert.equal(await maPage.locator('#session-settings').getAttribute('open'),null);assert.ok(await maPage.evaluate(()=>document.documentElement.scrollWidth<=innerWidth));await maPage.screenshot({path:output+'/welcome-mobile.png',fullPage:true,animations:'disabled'});await maPage.setViewportSize({width:1440,height:1000});
 await maPage.locator('[data-topic="Management Accounting"]').click();
 const maState=await maPage.evaluate(key=>JSON.parse(localStorage.getItem(key)),STORAGE_KEY);
 assert.ok(maState.session.queue.every(id=>bank.questions.some(q=>q.id===id&&q.topic==='Management Accounting'&&q.status==='validated')));
 const maQuestion=bank.questions.find(q=>q.id===maState.session.queue[0]);assert.equal(await maPage.locator('input[name=answer]').count(),maQuestion.options.length);
 await maPage.locator('textarea[data-notes]').fill('Management accounting: record the contribution and units.');
 await maPage.locator(`input[name=answer][value="${maQuestion.correctOptionId}"]`).check();await maPage.getByRole('button',{name:'Submit answer',exact:true}).click();await maPage.locator('.feedback[data-outcome=correct]').waitFor();
 await maPage.screenshot({path:output+'/management-accounting.png',fullPage:true,animations:'disabled'});
 await maPage.setViewportSize({width:375,height:900});assert.ok(await maPage.evaluate(()=>document.documentElement.scrollWidth<=innerWidth),'MA question overflow');
 await maPage.getByRole('button',{name:'Learning history',exact:true}).click();assert.match(await maPage.locator('tbody tr').filter({hasText:'Management Accounting'}).textContent(),/100%/);
 await maPage.getByRole('button',{name:/Source review/}).click();assert.equal(await maPage.locator('.review-item').filter({hasText:'ma-'}).count(),5);
 // Apple design: touch capabilities, readable controls, floating navigation and accessibility preferences.
 const touchContext=await browser.newContext({viewport:{width:375,height:900},isMobile:true,hasTouch:true});const touchPage=await touchContext.newPage();await touchPage.goto(base);await touchPage.locator('.study-hero').waitFor();
 assert.equal(await touchPage.evaluate(()=>matchMedia('(hover: hover) and (pointer: fine)').matches),false);
 const card=touchPage.locator('[data-topic="Management Accounting"]');const cardColor=await card.evaluate(el=>getComputedStyle(el).backgroundColor);await card.hover();assert.equal(await card.evaluate(el=>getComputedStyle(el).backgroundColor),cardColor);
 await touchPage.locator('#session-settings > summary').tap();assert.ok(await touchPage.locator('select').evaluateAll(elements=>elements.every(el=>parseFloat(getComputedStyle(el).fontSize)>=16)));
 await touchPage.locator('#tax-focus').tap();await touchPage.locator('textarea[data-notes]').waitFor();assert.equal(await touchPage.evaluate(()=>document.documentElement.dataset.input),'pointer');assert.ok(await touchPage.locator('textarea[data-notes]').evaluate(el=>parseFloat(getComputedStyle(el).fontSize)>=16));
 await touchPage.evaluate(()=>window.scrollTo(0,500));assert.ok(await touchPage.locator('.masthead').evaluate(el=>Math.abs(el.getBoundingClientRect().top)<1),'Study navigation must remain available while scrolling');
 await touchPage.locator('textarea[data-notes]').fill('Readable on a phone; notes remain selectable.');assert.notEqual(await touchPage.locator('textarea[data-notes]').evaluate(el=>getComputedStyle(el).userSelect),'none');
 const cdp=await touchContext.newCDPSession(touchPage);await cdp.send('Emulation.setEmulatedMedia',{features:[{name:'prefers-reduced-transparency',value:'reduce'},{name:'prefers-contrast',value:'more'},{name:'prefers-reduced-motion',value:'reduce'}]});
 assert.equal(await touchPage.locator('.masthead').evaluate(el=>getComputedStyle(el).backdropFilter),'none');assert.equal(await touchPage.evaluate(()=>getComputedStyle(document.documentElement).getPropertyValue('--line').trim()),'#586575');assert.equal(await touchPage.locator('button').first().evaluate(el=>getComputedStyle(el).transitionDuration),'0s');
 assert.ok(await touchPage.evaluate(()=>document.documentElement.scrollWidth<=innerWidth),'Touch layout must not overflow');await touchPage.screenshot({path:output+'/apple-touch.png',fullPage:false,animations:'disabled'});
 // Corrupt data must survive initialization; no blank state may overwrite it.
 const corruptContext=await browser.newContext();await corruptContext.addInitScript(key=>localStorage.setItem(key,'unreadable-json'),STORAGE_KEY);const corruptPage=await corruptContext.newPage();await corruptPage.goto(base);await corruptPage.getByRole('button',{name:'Download unreadable data'}).waitFor();assert.equal(await corruptPage.evaluate(key=>localStorage.getItem(key),STORAGE_KEY),'unreadable-json');
 // Restart a persistent browser profile, not just a page, to verify durable drafts/history.
 const profile=output+'/profile-'+Date.now();
 let persistent=await playwright.chromium.launchPersistentContext(profile,{headless:true});let durable=await persistent.newPage();await durable.goto(base);await durable.locator('#start:not([disabled])').waitFor();await durable.click('#tax-focus');await durable.locator('textarea[data-notes]').fill('Saved across a complete browser restart.');await durable.getByRole('button',{name:'I don’t know',exact:true}).click();await durable.locator('.feedback[data-outcome=unknown]').waitFor();await persistent.close();
 persistent=await playwright.chromium.launchPersistentContext(profile,{headless:true});durable=await persistent.newPage();await durable.goto(base);await durable.locator('.feedback[data-outcome=unknown]').waitFor();assert.equal(await durable.locator('textarea[data-notes]').inputValue(),'Saved across a complete browser restart.');assert.equal(await durable.evaluate(key=>JSON.parse(localStorage.getItem(key)).attempts[0].notesSnapshot,STORAGE_KEY),'Saved across a complete browser restart.');await persistent.close();
 // Failed browser writes must be visible and the in-memory work must remain exportable.
 const fullContext=await browser.newContext({acceptDownloads:true});await fullContext.addInitScript(()=>{Storage.prototype.setItem=function(){throw new DOMException('Quota exceeded','QuotaExceededError');};});const fullPage=await fullContext.newPage();await fullPage.goto(base);await fullPage.locator('#start:not([disabled])').waitFor();await fullPage.click('#tax-focus');await fullPage.locator('textarea[data-notes]').fill('Export this even though browser saving failed.');assert.match(await fullPage.locator('.save-status').textContent(),/Not saved/);const failureDownload=fullPage.waitForEvent('download');await fullPage.click('#export');const failureFile=await failureDownload;const failedBackup=JSON.parse(readFileSync(await failureFile.path(),'utf8'));assert.ok(Object.values(failedBackup.drafts).some(d=>d.notes==='Export this even though browser saving failed.'));
 assert.deepEqual(errors,[]);
 console.log('PASS: browser grading, hidden feedback, autosave/reload/browser restart, immutable snapshots, history/retries, targeted follow-up, filters, JSON export/import/cancel/deduplication, reset confirmation, keyboard flow, 375–1440px layouts, large text, failed-save export and recovery protection.');
 console.log('PASS: pointer-down feedback before release, immediate question and keyboard updates, touch hover gating, 16px phone inputs, floating navigation, reduced transparency and increased contrast.');
 console.log('Screenshots: '+output+'/desktop.png and mobile.png');
}finally{await browser.close();}
