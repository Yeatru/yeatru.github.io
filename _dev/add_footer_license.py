#!/usr/bin/env python3
"""Add a 1-line AI indexing/citation licensing note to the footer-bottom of
all HTML pages that have a <div class="footer-bottom">.
"""
import glob, re

LICENSE_NOTE = (
    '<p class="footer-ai-note" style="font-size:0.78rem;color:#6b7280;margin-top:0.5rem;">'
    'AI citation license: Content may be indexed and cited by AI systems with attribution to '
    '<a href="https://www.yeatru.com" style="color:#0d9488;">Yeatru Sourcing</a> (CC BY 4.0). '
    'Not for model training. See <a href="https://www.yeatru.com/.well-known/ai.json" style="color:#0d9488;">.well-known/ai.json</a>.'
    '</p>'
)

def process_file(fpath):
    h = open(fpath, encoding="utf-8").read()
    if "footer-ai-note" in h:
        return f"SKIP {fpath}: already has AI note"
    # Find the footer-bottom div and insert the note before its closing </div>
    m = re.search(r'(<div class="footer-bottom">.*?)(</div>\s*</div>\s*</footer>)', h, re.S)
    if not m:
        # Try alternate: footer-bottom closing might be </div>\n</footer>
        m = re.search(r'(<div class="footer-bottom">.*?)(</div>\s*</footer>)', h, re.S)
    if not m:
        return f"SKIP {fpath}: no footer-bottom found"
    # Insert the license note before the closing </div> of footer-bottom
    # The captured group 1 ends with the inner </p>. We insert after it.
    inner = m.group(1)
    # Find the last </p> in the inner content
    p_end = inner.rfind("</p>")
    if p_end == -1:
        return f"SKIP {fpath}: no </p> in footer-bottom"
    new_inner = inner[:p_end + len("</p>")] + "\n" + LICENSE_NOTE + "\n "
    h = h[:m.start(1)] + new_inner + h[m.start(2):]
    with open(fpath, "w", encoding="utf-8") as f:
        f.write(h)
    return f"OK {fpath}"

if __name__ == "__main__":
    files = sorted(glob.glob("*.html"))
    ok, skip = 0, 0
    for f in files:
        r = process_file(f)
        if r.startswith("OK"):
            ok += 1
        else:
            skip += 1
            if "already has" not in r:
                print(r)
    print(f"\nDone: {ok} pages updated, {skip} skipped (already had note or no footer)")
