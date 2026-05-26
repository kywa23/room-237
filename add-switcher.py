#!/usr/bin/env python3

import os
import glob

# Список всіх варіантів
variants = [
    {'num': '00', 'label': 'Оригінал', 'url': '/index.html'},
    {'num': '01', 'label': 'Dark Luxury', 'url': '/variants/v1-dark-luxury.html'},
    {'num': '02', 'label': 'Full-bleed відео', 'url': '/variants/v2-fullbleed-video.html'},
    {'num': '03', 'label': 'Split ліво/право', 'url': '/variants/v3-split-layout.html'},
    {'num': '04', 'label': 'Ultra Minimal', 'url': '/variants/v4-ultra-minimal.html'},
    {'num': '05', 'label': 'Відео зверху', 'url': '/variants/v5-video-top.html'},
    {'num': '06', 'label': 'Sage зелений', 'url': '/variants/v6-sage-natural.html'},
    {'num': '07', 'label': 'Corporate Blue', 'url': '/variants/v7-corporate-blue.html'},
    {'num': '08', 'label': 'Centered відео', 'url': '/variants/v8-centered-video.html'},
    {'num': '09', 'label': 'Terracotta', 'url': '/variants/v9-terracotta.html'},
    {'num': '10', 'label': 'Bands смуги', 'url': '/variants/v10-bands.html'},
    {'num': '11', 'label': 'Editorial', 'url': '/variants/v11-editorial.html'},
    {'num': '12', 'label': 'Brutalist', 'url': '/variants/v12-brutalist.html'},
    {'num': '13', 'label': 'Glassmorphism', 'url': '/variants/v13-glassmorphism.html'},
    {'num': '14', 'label': 'Ink Paper', 'url': '/variants/v14-ink-paper.html'},
    {'num': '15', 'label': 'Bento Grid', 'url': '/variants/v15-bento.html'},
    {'num': '16', 'label': 'Framed рамка', 'url': '/variants/v16-framed.html'},
    {'num': '17', 'label': 'Neon Dark', 'url': '/variants/v17-neon-dark.html'},
    {'num': '18', 'label': 'Two-tone', 'url': '/variants/v18-twotone.html'},
    {'num': '19', 'label': 'Poster', 'url': '/variants/v19-poster.html'},
    {'num': '20', 'label': 'Rotating Slides', 'url': '/variants/v20-rotating-slides.html'},
]

# HTML код для switcher
links_html = '\n    '.join([
    f'<a href="{v["url"]}" data-path="{v["url"]}"><span>{v["num"]}</span>{v["label"]}</a>'
    for v in variants
])

switcher_html = f'''
<!-- Variant Switcher -->
<button id="vswBtn" aria-label="Switcher">⊞</button>
<div id="vswPanel">
  <div style="padding:16px 20px;border-bottom:1px solid rgba(200,180,140,.2);font-size:11px;letter-spacing:0.2em;text-transform:uppercase;color:rgba(200,180,140,.6)">Варіанти дизайну</div>
  <div style="overflow-y:auto;max-height:calc(70vh - 60px)">
    {links_html}
  </div>
</div>
<style>
#vswBtn{{position:fixed;bottom:72px;right:16px;width:44px;height:44px;border-radius:50%;border:none;background:rgba(28,22,14,.8);backdrop-filter:blur(8px);color:#C7A66B;font-size:22px;cursor:pointer;z-index:99999;display:flex;align-items:center;justify-content:center;transition:all .2s ease;box-shadow:0 2px 12px rgba(0,0,0,.3)}}
#vswBtn:hover{{background:rgba(28,22,14,.95);transform:scale(1.05)}}
#vswPanel{{position:fixed;bottom:124px;right:16px;width:260px;background:rgba(28,22,14,.95);backdrop-filter:blur(16px);border-radius:6px;z-index:99998;display:none;box-shadow:0 4px 24px rgba(0,0,0,.5)}}
#vswPanel.show{{display:block}}
#vswPanel a{{display:flex;align-items:center;gap:14px;padding:12px 20px;color:#E5DCC8;text-decoration:none;font-size:14px;transition:background .2s ease;border-bottom:1px solid rgba(200,180,140,.08)}}
#vswPanel a:hover{{background:rgba(199,166,107,.15)}}
#vswPanel a.active{{background:rgba(199,166,107,.25);color:#C7A66B}}
#vswPanel a span{{display:inline-block;min-width:24px;font-size:11px;color:rgba(200,180,140,.5);font-variant-numeric:tabular-nums}}
#vswPanel a.active span{{color:#C7A66B;font-weight:600}}
</style>
<script>
(function(){{
const btn=document.getElementById('vswBtn');
const panel=document.getElementById('vswPanel');
if(!btn||!panel)return;
btn.addEventListener('click',function(e){{
  e.stopPropagation();
  panel.classList.toggle('show');
}});
document.addEventListener('click',function(e){{
  if(!panel.contains(e.target)&&e.target!==btn){{
    panel.classList.remove('show');
  }}
}});
const path=location.pathname;
document.querySelectorAll('#vswPanel a').forEach(function(a){{
  const href=a.getAttribute('data-path');
  if(path===href||(path==='/'&&href==='/index.html')){{
    a.classList.add('active');
  }}
}});
}})();
</script>
'''

def process_file(file_path):
    """Обробляє один HTML файл"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Перевіряємо, чи вже є switcher
        if 'id="vswBtn"' in content:
            print(f'⏭  {file_path} - вже має switcher, пропускаю')
            return False

        # Шукаємо закриваючий тег </body>
        body_close_index = content.rfind('</body>')
        if body_close_index == -1:
            print(f'⚠  {file_path} - не знайдено </body>')
            return False

        # Вставляємо switcher перед </body>
        content = content[:body_close_index] + switcher_html + '\n' + content[body_close_index:]

        # Записуємо файл
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)

        print(f'✓  {file_path} - switcher додано')
        return True

    except Exception as e:
        print(f'✗  {file_path} - помилка: {e}')
        return False

def main():
    print('🚀 Починаю додавати switcher до HTML файлів...\n')

    files = []

    # Додаємо index.html
    index_path = 'index.html'
    if os.path.exists(index_path):
        files.append(index_path)

    # Додаємо всі файли з variants/
    variant_files = glob.glob('variants/*.html')
    files.extend(variant_files)

    processed = 0
    skipped = 0

    for file_path in files:
        if os.path.exists(file_path):
            result = process_file(file_path)
            if result:
                processed += 1
            else:
                skipped += 1
        else:
            print(f'⚠  {file_path} - файл не знайдено')

    print(f'\n✅ Готово! Оброблено: {processed}, Пропущено: {skipped}')

if __name__ == '__main__':
    main()
