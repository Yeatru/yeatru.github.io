# Blog Rewrite Quality Specification (reference for subagents)

## Goal
Rewrite templated NEW blog HTML files so each has unique, topic-specific, expert content.
The current bodies are 100% templated (identical skeleton, only the topic word swapped).
This kills SEO (Google helpful-content duplicate/low-quality) and GEO (ChatGPT/Perplexity
will not cite templated text). Each blog must become genuinely useful and unique.

## Files to edit
For each blog: `/workspace/blog-{slug}.html`
- KEEP the entire HTML shell unchanged: `<head>` meta except description fields, `<nav>`,
  hero header, breadcrumb, CTA section, related-articles section, footer, scripts.
- REPLACE ONLY:
  1. `<meta name="description">`, `og:description`, `twitter:description` — new ~150-char topic-specific summary
  2. JSON-LD `Article` `description`, `BlogPosting` `description` — same new summary
  3. JSON-LD `HowTo` — replace the 5 generic templated steps with 5 topic-specific steps (each step `name` + `text` reflecting real content)
  4. JSON-LD `FAQPage` — replace the 6 generic Q&As with 6 topic-specific Q&As matching the body FAQ
  5. The inner of `<article class="article-content">...</article>` (everything between the
     featured-image div and the author-bio aside)

## Body structure (target ~800–1100 words, unique per blog)
Use this skeleton but with topic-specific content — NOT the old template:

1. `<aside class="article-takeaways"><h2>Key Takeaways</h2><ul>` — 5 bullets, each with a
   real specific number/fact + 1–2 internal links. NO generic "X is a critical step" line.
2. `<div class="geo-definition"><h2>What Is {topic}?</h2><p>` — 1 paragraph real definition.
3. 5–7 `<h2>` sections, each topic-specific. Suggested angles:
   - Rates / costs / pricing table (with a real `<table class="geo-comparison-table">`)
   - How-to process steps (ordered list)
   - Decision matrix / comparison table (vs alternatives)
   - Common mistakes / red flags (unordered list)
   - Calculation example with real numbers
   - Compliance / restrictions (where relevant)
   - How Yeatru handles it (service-specific, with internal links)
4. `<h2>Frequently Asked Questions</h2>` — 6 `<h3>` Q&As, topic-specific, matching the
   FAQPage JSON-LD.
5. `<h2>Conclusion</h2>` — 1 paragraph topic-specific summary + 1 CTA link to contact.html.

## Content quality rules (CRITICAL)
- Every number must be concrete and realistic (rates, %, days, kg, $).
- Include at least one real data table (`geo-comparison-table`) per blog.
- Include a worked example with real numbers where the topic allows.
- Weave 4–6 internal links to other blog-*.html files naturally (verify the target slug
  exists by checking the workspace — do not invent slugs).
- Use `<strong>` for key numbers; use `<a href="blog-*.html">` for internal links.
- DO NOT reuse any of the 12 template signature sentences (listed in
  /workspace/detect_templated_v2.py). If any signature remains, the rewrite failed.
- Each blog's body must be unique vs every other blog (no shared paragraphs).

## Verification (do this for every rewritten blog)
Run: `python3 /workspace/detect_templated_v2.py` — the rewritten blog must show <8/12
signature hits (ideally 0). Also grep the file for "is not an optional step" and
"covers everything you need to know" — must return nothing.

## Example of done quality
See `/workspace/blog-air-freight-china.html` (already rewritten) for the target bar:
real rate table by route, chargeable-weight worked example, 7-step process, 6 topic FAQs.
Mirror that depth and structure, adapted to each topic.
