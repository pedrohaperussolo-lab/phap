const { chromium } = require('playwright');
(async () => {
  const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium' });
  const p = await b.newPage({ viewport: { width: 1236, height: 888 } });
  await p.goto('file:///tmp/cover2/wrap.html');
  await p.waitForTimeout(1200);
  await p.pdf({ path: '/tmp/cover2/base.pdf', width: '12.875in', height: '9.25in', printBackground: true, pageRanges: '1' });
  await p.screenshot({ path: '/tmp/cover2/wrap.png' });
  await b.close();
})();
