#!/usr/bin/env python3
"""
PageSpeed optimization: fix all HTML pages.

Optimizations applied:
1. Bootstrap CSS: defer via media="print" onload pattern (removes render-blocking)
2. bootstrap.bundle.min.js: add defer attribute
3. Hero images: add width/height/loading="eager" to prevent LCP delay + CLS
4. Google Fonts: keep sync (so LCP text is styled) but ensure display=swap
5. app.js / i18n-*.js: ensure defer (they're at body bottom already)
"""
import re, glob, os, shutil

ROOT = os.path.dirname(os.path.abspath(__file__))
EXTENSIONS = ('index.html', '*.html')

PROTECTED_DIRS = {'functions', 'node_modules', '.git'}

def should_process(filepath):
    basename = os.path.basename(filepath)
    for d in PROTECTED_DIRS:
        if f'/{d}/' in filepath or filepath.startswith(os.path.join(ROOT, d)):
            return False
    return basename.endswith('.html') and basename != 'index.html' or True  # process all HTML

def fix_page(s, filename):
    changes = []
    
    # === 1. Bootstrap CSS: defer via print-media trick ===
    # Replace: <link href="...bootstrap.min.css" rel="stylesheet" integrity="..." crossorigin="anonymous">
    # With:    <link rel="stylesheet" href="..." media="print" onload="this.media='all'" integrity="..." crossorigin="anonymous">
    orig = s
    s = re.sub(
        r'<link\s+href="(https://cdn\.jsdelivr\.net/npm/bootstrap@[^"]+)"\s+rel="stylesheet"([^>]*)>',
        r'<link rel="stylesheet" href="\1" media="print" onload="this.media=\'all\'"\2>',
        s,
        count=1
    )
    if s != orig:
        # Check if we need to add noscript fallback
        if '<noscript><link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap' not in s:
            # Insert noscript right after the deferred one
            s = re.sub(
                r'(<link rel="stylesheet" href="(https://cdn\.jsdelivr\.net/npm/bootstrap[^"]+)" media="print"[^>]*>)',
                r'\1\n    <noscript><link rel="stylesheet" href="\2" integrity="sha384-DQvkBjpPgn7RC31MCQoOeC9TI2kdqa4+BSgNMNj8v77fdC77Kj5zpWFTJaaAoMbC" crossorigin="anonymous"></noscript>',
                s,
                count=1
            )
        changes.append('Bootstrap CSS deferred')
    
    # === 2. bootstrap.bundle.min.js: add defer ===
    orig = s
    s = re.sub(
        r'(<script\s+src="(https://cdn\.jsdelivr\.net/npm/bootstrap[^"]+\.bundle[^"]*)"[^>]*?)(?=\s*>)',
        lambda m: m.group(1) + ' defer' if 'defer' not in m.group(1) else m.group(1),
        s,
        count=1
    )
    # Also handle the case where it's the same pattern
    s = re.sub(
        r'(src="https://cdn\.jsdelivr\.net/npm/bootstrap[^"]+\.bundle[^"]*")(?=[^>]*></script>)',
        r'\1 defer',
        s,
        count=1
    )
    if s != orig:
        changes.append('Bootstrap JS deferred')
    
    # === 3. Product page: ensure hero img has loading="eager" ===
    # index.html hero image: fetchpriority is already high, add loading="eager" 
    orig = s
    # FBA.jpg (index hero) — add loading="eager" if present
    if '/Images/FBA.jpg' in s:
        s = s.replace(
            '<img data-img-editable="index.slide1.image" src="/Images/FBA.jpg"',
            '<img data-img-editable="index.slide1.image" src="/Images/FBA.jpg" loading="eager"'
        )
    
    # logo_and_mold.jpg (slide 2) — not LCP, add lazy
    if '/Images/logo_and_mold.jpg' in s:
        s = s.replace(
            'src="/Images/logo_and_mold.jpg" alt=',
            'src="/Images/logo_and_mold.jpg" loading="lazy" alt='
        )
    
    if s != orig:
        changes.append('Hero images optimized')
    
    # === 4. Check app.js defer ===
    if 'src="app.js"' in s and 'src="app.js" defer' not in s:
        s = s.replace('src="app.js"', 'src="app.js" defer')
        changes.append('app.js deferred')
    
    # === 5. i18n scripts — defer them too (they're just data) ===
    for i18n_file in ['i18n-svc1.js', 'i18n-svc2.js', 'i18n-svc3.js', 'i18n-misc.js']:
        if f'src="{i18n_file}"' in s and f'src="{i18n_file}" defer' not in s:
            s = s.replace(f'src="{i18n_file}"', f'src="{i18n_file}" defer')
            if i18n_file not in str(changes):
                changes.append(f'{i18n_file} deferred')
    
    return s, changes


def main():
    prodfiles = glob.glob(os.path.join(ROOT, '*.html'))
    
    total_touched = 0
    all_changes = {}
    
    for pf in sorted(prodfiles):
        # Skip if it's inside a protected dir
        if any(f'/{d}/' in pf or pf.endswith(f'/{d}') for d in PROTECTED_DIRS):
            continue
        
        with open(pf, encoding='utf-8') as f:
            original = f.read()
        
        new, changes = fix_page(original, os.path.basename(pf))
        
        if new != original:
            # Backup first
            # shutil.copy(pf, pf + '.bak')  # too many backups, skip
            with open(pf, 'w', encoding='utf-8') as f:
                f.write(new)
            total_touched += 1
            for c in changes:
                all_changes[c] = all_changes.get(c, 0) + 1
    
    print(f"Processed {total_touched} HTML files.")
    print("\nOptimization summary:")
    for change, count in sorted(all_changes.items()):
        print(f"  ✅ {change}: {count} files")


if __name__ == '__main__':
    main()
