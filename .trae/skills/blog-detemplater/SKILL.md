---
name: "blog-detemplater"
description: "Detects and rewrites templated/boilerplate blog HTML into unique, topic-specific SEO content. Invoke when blog pages share identical filler phrases, need SEO de-duplication, or a batch of generated articles reads generic."
---

# Blog Detemplater

Rewrites templated blog HTML files so each article has unique, expert, topic-specific content — replacing boilerplate filler with concrete data tables, worked examples, and real numbers. Then validates uniqueness, word count, internal-link integrity, and JSON-LD validity.

## When to Invoke

- A batch of blog HTML files was generated from a shared template and reads identically.
- Signature boilerplate phrases (e.g. "X is not an optional step", "covers everything you need to know", generic 5/6/7-stage process blocks) appear across multiple articles.
- User asks to "de-duplicate", "de-template", "rewrite", or "make unique" blog/SEO articles.
- SEO content audit flags thin or duplicate blog pages.

## Pre-requisites in the Workspace

The skill expects (and reads first):

1. **`REWRITE_SPEC.md`** at the workspace root — the canonical rewrite spec: structure, word count, table format, HowTo/FAQ JSON-LD rules, internal-link policy, CTA convention. Always read it before editing.
2. **A reference blog** (e.g. `blog-air-freight-china.html`) that already follows the spec — read it as the quality baseline.
3. **`detect_templated_v2.py`** at the workspace root — the detector that scores each file against a signature-phrase list. Threshold: ≥8/12 signatures = templated.
4. A list of "new blogs" (slug names, one per line) at `/tmp/new_blogs.txt` (or regenerate from the workspace glob).

If any of these are missing, create them first before rewriting.

## Workflow

### Step 1 — Detect templated files

Run the detector to get the candidate list and each file's hit count:

```bash
python3 detect_templated_v2.py
```

Only rewrite files with **≥8/12** signature hits. Files below the threshold already have unique content — leave them alone.

### Step 2 — Read spec + reference

Read `REWRITE_SPEC.md` and the reference blog (`blog-air-freight-china.html`) to lock in:

- Editable zones only: `meta description`, `og:description`, `twitter:description`; JSON-LD `Article`/`BlogPosting` `description`; `HowTo` (5 steps); `FAQPage` (6 Q&As); the `<article>` inner block.
- Everything else (HTML shell, nav, CTA, footer, styles) stays untouched.

### Step 3 — Rewrite per file

For each templated file, produce unique content covering:

- **Meta / JSON-LD description**: ~150 chars, topic-specific, with one concrete number.
- **HowTo JSON-LD**: 5 topic-specific steps (name + text), not generic.
- **FAQPage JSON-LD**: 6 topic-specific Q&As that match the body FAQ.
- **Article body** (≥800 words):
  - Key Takeaways (5 bullets, each with a concrete number and ≥1 internal link).
  - Definition / intro section.
  - 5–7 H2 sections with at least one `geo-comparison-table` data table (real numbers).
  - At least one worked example with a numeric calculation.
  - 6 FAQ entries matching the JSON-LD.
  - Conclusion + CTA linking to `contact.html`.
- **Internal links**: point only to slugs that exist as files in the workspace.

### Step 4 — Validate

After each batch, run all four checks. All must pass:

```bash
# 1. Template signatures — every rewritten file must be <8 hits (0 ideal)
python3 detect_templated_v2.py

# 2. Residual boilerplate phrases — must be 0
grep -rl --include="blog-*.html" "is not an optional step" . ; \
grep -rl --include="blog-*.html" "covers everything you need to know" .

# 3. Word count — no article body under 700 words
python3 -c "
import os,re
for f in sorted(os.listdir('.')):
    if not (f.startswith('blog-') and f.endswith('.html')): continue
    c=open(f,encoding='utf-8',errors='replace').read()
    m=re.search(r'<article[^>]*>(.*?)</article>',c,re.S)
    body=m.group(1) if m else ''
    text=re.sub(r'<[^>]+>',' ',body); text=re.sub(r'\s+',' ',text)
    if len(text.split())<700: print(f, len(text.split()))
"

# 4. Internal links — zero broken
python3 -c "
import os,re
files=set(f for f in os.listdir('.') if f.startswith('blog-') and f.endswith('.html'))
broken=0
for f in sorted(files):
    c=open(f,encoding='utf-8',errors='replace').read()
    for l in set(re.findall(r'href=\"(blog-[a-z0-9-]+\.html)\"',c)):
        if l not in files:
            broken+=1; print('BROKEN:',f,'->',l)
print('broken:',broken)
"
```

### Step 5 — Batching

- For large batches (20+ files), split into parallel `general_purpose_task` invocations of 5–10 files each. Each task must read `REWRITE_SPEC.md` + the reference blog first.
- After all tasks complete, re-run the detector to find any stragglers, then do a final single-batch rewrite pass on the remainder.

## Rules

- **Never edit outside** the editable zones listed in Step 2.
- **Never invent internal links** — only link to slugs that have a corresponding `blog-*.html` file.
- **Never reuse** generic process text ("First… Second… Third…", "Most first-time buyers make the same mistakes", "Understanding the real cost structure", "Focusing only on the lowest unit price", "Skipping supplier verification", "Yeatru Sourcing specializes in", "5-15 days from RFQ", "off-the-shelf Yiwu goods", "AQL 2.5 pre-shipment inspection", "50% deposit to start production") verbatim across articles. Industry terms (AQL, MOQ, 50/50 deposit) may appear naturally but not as copy-pasted boilerplate.
- **Concrete numbers only** — no vague "a few days", "low cost". Use real ranges (5–15 days, $4–9/kg).
- **Do not git push** unless the user explicitly asks.
