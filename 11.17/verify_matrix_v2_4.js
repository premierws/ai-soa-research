const {chromium}=require('/home/shaun/browser/node_modules/playwright');
const fs=require('fs');
const path=require('path');
const root=__dirname;
(async()=>{
 const browser=await chromium.launch({headless:true,executablePath:'/opt/microsoft/msedge/msedge',args:['--no-sandbox']});
 const report={slides:24,checks:[],errors:[]};
 const target=process.argv[2]||'file://'+path.join(root,'matrix_planning_v2_4.html');
 for(const [w,h] of [[1920,1080],[1366,768],[1280,720]]){
  const page=await browser.newPage({viewport:{width:w,height:h}});
  page.on('pageerror',err=>report.errors.push(err.message));
  const response=await page.goto(target); await page.evaluate(()=>document.fonts.ready);
  const issues=await page.evaluate(()=>{
   const issues=[];
   if(document.querySelectorAll('.slide').length!==24)issues.push('slide count');
   if(document.querySelectorAll('table').length!==1)issues.push('table count');
   for(const s of document.querySelectorAll('.slide')){
    const r=s.getBoundingClientRect(),body=s.querySelector('.body');
    for(const el of body.children){const b=el.getBoundingClientRect();if(b.bottom>r.bottom-innerHeight*.062-5)issues.push({slide:s.id,type:'vertical overflow',bottom:b.bottom-r.top,limit:r.height-innerHeight*.062-5});if(b.right>r.right-25||b.left<r.left-1)issues.push({slide:s.id,type:'horizontal overflow'});}
    for(const g of s.querySelectorAll('.diagram-node')){
     const b=g.querySelector('rect').getBBox();
     for(const t of g.querySelectorAll('text')){const a=t.getBBox();if(a.x<b.x-1||a.y<b.y-1||a.x+a.width>b.x+b.width+1||a.y+a.height>b.y+b.height+1)issues.push({slide:s.id,type:'SVG text overflow',text:t.textContent});}
    }
   }
   const titles=[...document.querySelectorAll('h1,h2')].map(x=>x.textContent);
   if(titles.some(x=>/附录|参考材料|目标型车控/.test(x)))issues.push('removed headings present');
   return issues;
  });
  await page.keyboard.press('Home');await page.waitForTimeout(80);
  await page.keyboard.press('ArrowDown');await page.waitForTimeout(80);
  if(!page.url().endsWith('#s2'))issues.push('next keyboard');
  await page.click('#overview-toggle');
  if(await page.locator('#overview-grid button').count()!==24)issues.push('overview count');
  await page.locator('#overview-grid button').nth(4).click();await page.waitForTimeout(80);
  if(!page.url().endsWith('#s5'))issues.push('overview jump');
  await page.click('#notes-toggle');if(await page.locator('#notes-panel').isHidden())issues.push('notes');await page.click('#notes-toggle');
  if(w===1366){for(const n of [2,4,5,8,11,13,16,18,20,22]){await page.evaluate(n=>document.querySelector('#rail').children[n-1].click(),n);await page.waitForTimeout(60);await page.screenshot({path:'/tmp/matrix-v24-'+n+'.png'});}}
  report.checks.push({w,h,status:response?.status(),issues});await page.close();
 }
 const mobile=await browser.newPage({viewport:{width:390,height:844}});await mobile.goto(target);
 report.mobile={horizontalOverflow:await mobile.evaluate(()=>document.documentElement.scrollWidth>innerWidth)};
 await mobile.close();
 report.passed=report.checks.every(x=>!x.issues.length)&&!report.errors.length&&!report.mobile.horizontalOverflow;
 fs.writeFileSync(path.join(root,'matrix_v2_4_verification.json'),JSON.stringify(report,null,2)+'\n');
 console.log(JSON.stringify(report,null,2));await browser.close();if(!report.passed)process.exit(1);
})().catch(e=>{console.error(e);process.exit(1)});
