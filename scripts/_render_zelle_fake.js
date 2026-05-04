const puppeteer = require('puppeteer');
const path = require('path');

(async () => {
  const browser = await puppeteer.launch({
    headless: 'new',
    args: ['--no-sandbox']
  });
  const page = await browser.newPage();
  await page.setViewport({ width: 414, height: 896, deviceScaleFactor: 2 });

  const file = path.resolve(__dirname, '..', 'posts', 'zelle-fake-maria-gonzalez.html');
  await page.goto('file://' + file.replace(/\\/g, '/'), { waitUntil: 'networkidle0' });

  const out = path.resolve(__dirname, '..', 'posts', 'zelle-fake-maria-gonzalez.png');
  await page.screenshot({ path: out, fullPage: false, omitBackground: false });
  console.log('Saved:', out);

  await browser.close();
})();
