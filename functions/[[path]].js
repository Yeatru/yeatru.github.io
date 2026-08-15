// Cloudflare Pages Function — intercepts *.html URLs and serves them as 200
// instead of letting Cloudflare's auto-strip-.html return a 308 Permanent Redirect.
// This is the ONLY reliable way to make Bing (and Google) index .html pages that
// currently land on "redirect, cannot be indexed" in URL Inspection.
export async function onRequest(context) {
  const { request, next } = context;
  const url = new URL(request.url);

  // Only intercept when the path ends with .html (and not .html/... subpaths)
  if (/\.html$/.test(url.pathname)) {
    const cleanUrl = url.origin + url.pathname.replace(/\.html$/, '') + url.search;
    const response = await fetch(cleanUrl);

    if (response && response.status === 200) {
      const headers = new Headers(response.headers);
      // Ensure proper content type for HTML
      if (!headers.has('Content-Type')) {
        headers.set('Content-Type', 'text/html; charset=utf-8');
      }
      // Remove any redirect-related headers that might confuse crawlers
      headers.delete('Location');
      headers.delete('Refresh');
      return new Response(response.body, { status: 200, headers });
    }
  }

  return next();
}
