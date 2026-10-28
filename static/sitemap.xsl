<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:s="http://www.sitemaps.org/schemas/sitemap/0.9">
<xsl:output method="html" encoding="UTF-8"/>
<xsl:template match="/">
<html lang="en">
<head>
<meta charset="UTF-8"/>
<meta name="robots" content="noindex,follow"/>
<title>Yeatru Sitemap Index</title>
<style>
body{font-family:system-ui,-apple-system,sans-serif;max-width:800px;margin:2em auto;padding:0 1em;color:#333;background:#fafafa}
h1{color:#1a1a2e}
a{color:#2563eb;text-decoration:none}
a:hover{text-decoration:underline}
ul{list-style:none;padding:0}
li{padding:.5em 0;border-bottom:1px solid #eee}
.tag{display:inline-block;background:#e5e7eb;padding:.1em .4em;border-radius:3px;font-size:.85em;margin-right:.3em}
</style>
</head>
<body>
<h1>Yeatru Sitemap</h1>
<p>This is an XML sitemap generated for search engines. Human-readable index below:</p>
<xsl:choose>
  <xsl:when test="//s:sitemapindex">
    <ul>
      <xsl:for-each select="//s:sitemap">
        <li><span class="tag">sitemap</span><a><xsl:attribute name="href"><xsl:value-of select="s:loc"/></xsl:attribute><xsl:value-of select="s:loc"/></a> <small>(<xsl:value-of select="s:lastmod"/>)</small></li>
      </xsl:for-each>
    </ul>
  </xsl:when>
  <xsl:otherwise>
    <ul>
      <xsl:for-each select="//s:url">
        <li><a><xsl:attribute name="href"><xsl:value-of select="s:loc"/></xsl:attribute><xsl:value-of select="s:loc"/></a> <small>(<xsl:value-of select="s:lastmod"/>, <xsl:value-of select="s:priority"/>)</small></li>
      </xsl:for-each>
    </ul>
  </xsl:otherwise>
</xsl:choose>
</body>
</html>
</xsl:template>
</xsl:stylesheet>
