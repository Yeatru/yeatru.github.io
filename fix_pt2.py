#!/usr/bin/env python3
"""Fix escaped quotes in onload and double-defer on all HTML pages."""
import re, glob

prodfiles = glob.glob('*.html')

fixed_onload = 0
fixed_defer = 0
remaining_double_defer = 0

BAD_ONLOAD = "onload=\"this.media=\\\\'all\\\\'\""  # The actually-written bad string
GOOD_ONLOAD = "onload=\"this.media='all'\""

for pf in prodfiles:
    with open(pf, encoding='utf-8') as f:
        s = f.read()
    orig = s
    
    # Fix 1: escaped quotes in onload
    if BAD_ONLOAD in s:
        s = s.replace(BAD_ONLOAD, GOOD_ONLOAD)
        fixed_onload += 1
    
    # Fix 2: any double defer in script tags
    # Strategy: find all <script ... defer ... defer ...> and reduce to single defer
    def dedupe_defer(m):
        full = m.group(0)
        # Replace first "defer defer" or " defer  defer " with single
        return re.sub(r'\bdefer\b\s+\bdefer\b', 'defer', full)
    
    s = re.sub(r'<script[^>]*>', dedupe_defer, s)
    
    if s != orig:
        with open(pf, 'w', encoding='utf-8') as f:
            f.write(s)
    
    # Count remaining issues
    with open(pf) as f:
        content = f.read()
    if re.search(r'<script[^>]*\bdefer\b[^>]*\bdefer\b', content):
        remaining_double_defer += 1

print(f"Fixed onload quotes: {fixed_onload}")
print(f"Fixed double defer in this pass: {fixed_defer}")
print(f"Files still with double defer: {remaining_double_defer}")

# Verify index.html
with open('index.html') as f:
    s = f.read()

m = re.search(r'<link[^>]*bootstrap\.min\.css[^>]*>', s)
print("\nBootstrap CSS:", m.group(0).strip())

m = re.search(r'<script[^>]*bootstrap.*bundle[^>]*>', s)
print("Bootstrap JS:", m.group(0).strip()[:180])

print("\n=== DONE ===")
