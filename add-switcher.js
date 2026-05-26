#!/usr/bin/env node

const fs = require('fs');
const path = require('path');

// Список всіх варіантів
const variants = [
  { num: '00', label: 'Оригінал', url: '/index.html' },
  { num: '01', label: 'Dark Luxury', url: '/variants/v1-dark-luxury.html' },
  { num: '02', label: 'Full-bleed відео', url: '/variants/v2-fullbleed-video.html' },
  { num: '03', label: 'Split ліво/право', url: '/variants/v3-split-layout.html' },
  { num: '04', label: 'Ultra Minimal', url: '/variants/v4-ultra-minimal.html' },
  { num: '05', label: 'Відео зверху', url: '/variants/v5-video-top.html' },
  { num: '06', label: 'Sage зелений', url: '/variants/v6-sage-natural.html' },
  { num: '07', label: 'Corporate Blue', url: '/variants/v7-corporate-blue.html' },
  { num: '08', label: 'Centered відео', url: '/variants/v8-centered-video.html' },
  { num: '09', label: 'Terracotta', url: '/variants/v9-terracotta.html' },
  { num: '10', label: 'Bands смуги', url: '/variants/v10-bands.html' },
  { num: '11', label: 'Editorial', url: '/variants/v11-editorial.html' },
  { num: '12', label: 'Brutalist', url: '/variants/v12-brutalist.html' },
  { num: '13', label: 'Glassmorphism', url: '/variants/v13-glassmorphism.html' },
  { num: '14', label: 'Ink Paper', url: '/variants/v14-ink-paper.html' },
  { num: '15', label: 'Bento Grid', url: '/variants/v15-bento.html' },
  { num: '16', label: 'Framed рамка', url: '/variants/v16-framed.html' },
  { num: '17', label: 'Neon Dark', url: '/variants/v17-neon-dark.html' },
  { num: '18', label: 'Two-tone', url: '/variants/v18-twotone.html' },
  { num: '19', label: 'Poster', url: '/variants/v19-poster.html' },
  { num: '20', label: 'Rotating Slides', url: '/variants/v20-rotating-slides.html' },
];

// HTML код для switcher
const switcherHTML = `
<!-- Variant Switcher -->
<button id="vswBtn" aria-label="Switcher">⊞</button>
<div id="vswPanel">
  <div style="padding:16px 20px;border-bottom:1px solid rgba(200,180,140,.2);font-size:11px;letter-spacing:0.2em;text-transform:uppercase;color:rgba(200,180,140,.6)">Варіанти дизайну</div>
  <div style="overflow-y:auto;max-height:calc(70vh - 60px)">
    ${variants.map(v => `<a href="${v.url}" data-path="${v.url}"><span>${v.num}</span>${v.label}</a>`).join('\n    ')}
  </div>
</div>
<style>
#vswBtn{position:fixed;bottom:72px;right:16px;width:44px;height:44px;border-radius:50%;border:none;background:rgba(28,22,14,.8);backdrop-filter:blur(8px);color:#C7A66B;font-size:22px;cursor:pointer;z-index:99999;display:flex;align-items:center;justify-content:center;transition:all .2s ease;box-shadow:0 2px 12px rgba(0,0,0,.3)}
#vswBtn:hover{background:rgba(28,22,14,.95);transform:scale(1.05)}
#vswPanel{position:fixed;bottom:124px;right:16px;width:260px;background:rgba(28,22,14,.95);backdrop-filter:blur(16px);border-radius:6px;z-index:99998;display:none;box-shadow:0 4px 24px rgba(0,0,0,.5)}
#vswPanel.show{display:block}
#vswPanel a{display:flex;align-items:center;gap:14px;padding:12px 20px;color:#E5DCC8;text-decoration:none;font-size:14px;transition:background .2s ease;border-bottom:1px solid rgba(200,180,140,.08)}
#vswPanel a:hover{background:rgba(199,166,107,.15)}
#vswPanel a.active{background:rgba(199,166,107,.25);color:#C7A66B}
#vswPanel a span{display:inline-block;min-width:24px;font-size:11px;color:rgba(200,180,140,.5);font-variant-numeric:tabular-nums}
#vswPanel a.active span{color:#C7A66B;font-weight:600}
</style>
<script>
(function(){
const btn=document.getElementById('vswBtn');
const panel=document.getElementById('vswPanel');
if(!btn||!panel)return;
btn.addEventListener('click',function(e){
  e.stopPropagation();
  panel.classList.toggle('show');
});
document.addEventListener('click',function(e){
  if(!panel.contains(e.target)&&e.target!==btn){
    panel.classList.remove('show');
  }
});
const path=location.pathname;
document.querySelectorAll('#vswPanel a').forEach(function(a){
  const href=a.getAttribute('data-path');
  if(path===href||(path==='/'&&href==='/index.html')){
    a.classList.add('active');
  }
});
})();
</script>
`;

// Функція для обробки одного файлу
function processFile(filePath) {
  try {
    let content = fs.readFileSync(filePath, 'utf8');

    // Перевіряємо, чи вже є switcher
    if (content.includes('id="vswBtn"')) {
      console.log(`⏭  ${filePath} - вже має switcher, пропускаю`);
      return false;
    }

    // Шукаємо закриваючий тег </body>
    const bodyCloseIndex = content.lastIndexOf('</body>');
    if (bodyCloseIndex === -1) {
      console.log(`⚠  ${filePath} - не знайдено </body>`);
      return false;
    }

    // Вставляємо switcher перед </body>
    content = content.slice(0, bodyCloseIndex) + switcherHTML + '\n' + content.slice(bodyCloseIndex);

    // Записуємо файл
    fs.writeFileSync(filePath, content, 'utf8');
    console.log(`✓  ${filePath} - switcher додано`);
    return true;
  } catch (error) {
    console.error(`✗  ${filePath} - помилка: ${error.message}`);
    return false;
  }
}

// Головна функція
function main() {
  console.log('🚀 Починаю додавати switcher до HTML файлів...\n');

  const files = [];

  // Додаємо index.html
  files.push(path.join(__dirname, 'index.html'));

  // Додаємо всі файли з variants/
  const variantsDir = path.join(__dirname, 'variants');
  if (fs.existsSync(variantsDir)) {
    const variantFiles = fs.readdirSync(variantsDir)
      .filter(f => f.endsWith('.html'))
      .map(f => path.join(variantsDir, f));
    files.push(...variantFiles);
  }

  let processed = 0;
  let skipped = 0;

  files.forEach(file => {
    if (fs.existsSync(file)) {
      const result = processFile(file);
      if (result) processed++;
      else skipped++;
    } else {
      console.log(`⚠  ${file} - файл не знайдено`);
    }
  });

  console.log(`\n✅ Готово! Оброблено: ${processed}, Пропущено: ${skipped}`);
}

main();
