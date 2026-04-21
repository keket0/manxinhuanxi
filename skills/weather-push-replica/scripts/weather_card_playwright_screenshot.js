const { chromium } = require('playwright');
const path = require('path');
const fs = require('fs');

(async () => {
  const outputDir = process.env.WEATHER_OUTPUT_DIR || '/www/manmanai/openclaw/任务推送/天气';
  fs.mkdirSync(outputDir, { recursive: true });
  const htmlPath = path.resolve(outputDir, 'weather_card.html');
  const outPath = path.resolve(outputDir, 'weather_card_pw.png');

  const browser = await chromium.launch({ headless: true });
  const page = await browser.newPage({ viewport: { width: 1080, height: 1200 }, deviceScaleFactor: 2 });
  await page.goto('file://' + htmlPath, { waitUntil: 'load' });
  await page.evaluate(() => new Promise(r => requestAnimationFrame(() => requestAnimationFrame(r))));
  const size = await page.evaluate(() => {
    const card = document.querySelector('.card');
    const rect = card ? card.getBoundingClientRect() : { width: 1080, height: 1350 };
    return {
      width: Math.ceil(rect.width),
      height: Math.ceil(rect.height),
      bodyHeight: Math.ceil(document.body.scrollHeight),
      docHeight: Math.ceil(document.documentElement.scrollHeight)
    };
  });
  const clipHeight = Math.max(size.height, size.bodyHeight, size.docHeight, 1350);
  await page.setViewportSize({ width: Math.max(size.width, 1080), height: Math.min(clipHeight, 5000) });
  await page.screenshot({ path: outPath, fullPage: true, scale: 'device' });

  const history = fs.readdirSync(outputDir)
    .filter(name => /^weather_card_\d{8}_\d{6}\.png$/.test(name));
  for (const stale of history) {
    fs.unlinkSync(path.join(outputDir, stale));
  }

  console.log(JSON.stringify({ outPath, removedHistoryCount: history.length, size, clipHeight }, null, 2));
  await browser.close();
})().catch(err => { console.error(err); process.exit(1); });
