const puppeteer = require('puppeteer');
const path = require('path');

const targets = [
  { html: 'olivar-del-sur-logo.html',  png: 'olivar-del-sur-logo.png',  width: 800, height: 240 },
  { html: 'zelle-fake-01-maria.html',  png: 'zelle-fake-01-maria.png',  width: 414, height: 896 },
  { html: 'zelle-fake-02-carlos.html', png: 'zelle-fake-02-carlos.png', width: 414, height: 896 },
  { html: 'zelle-fake-03-lucia.html',  png: 'zelle-fake-03-lucia.png',  width: 414, height: 896 },
  { html: 'wire-fake-04-andes.html',   png: 'wire-fake-04-andes.png',   width: 414, height: 896 },
];

(async () => {
  const browser = await puppeteer.launch({ headless: 'new', args: ['--no-sandbox'] });
  const page = await browser.newPage();

  for (const t of targets) {
    await page.setViewport({ width: t.width, height: t.height, deviceScaleFactor: 2 });
    const file = path.resolve(__dirname, '..', 'posts', t.html);
    await page.goto('file://' + file.replace(/\\/g, '/'), { waitUntil: 'networkidle0' });
    const out = path.resolve(__dirname, '..', 'posts', t.png);
    await page.screenshot({ path: out, fullPage: false, omitBackground: false });
    console.log('Saved:', out);
  }

  await browser.close();
})();
