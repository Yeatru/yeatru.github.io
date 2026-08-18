// Cloudflare Pages Function v5 — SEO Fix Bundle (Bing 308 redirecting + GSC 集成)
// -----------------------------------------------------------------------------
// Google Search Console 报错修复:
//   (0) products.html?product=SKU  → 301 → /product-SKU.html
//       (取代客户端 JS window.location.replace(), 避免 "Page with redirect")
//   (1) /product-<旧数字ID>.html   → 301 → /product-<新SKU>.html
//       (解决 "Not found (404)" 中 product-274.html?lang=fr 等 41 页)
//   (2) .html URL → env.ASSETS.fetch() 直读文件, 不再走 subrequest fetch()
//       (解决 "Redirect error" china-sourcing-agent-europe / blog-1688-*.html)
//       (v3 的 subrequest fetch() 会触发 _redirects 域名301!规则, 造成多跳)
//   (3) /images/* 代理 (CF CDN缓存24h, 解决wsrv.nl失效)
// -----------------------------------------------------------------------------

const GITHUB_IMAGE_REPO = 'https://raw.githubusercontent.com/Yeatru/Image/main/Images';

const IMAGE_MIME = {
  '.png':  'image/png',
  '.jpg':  'image/jpeg',
  '.jpeg': 'image/jpeg',
  '.webp': 'image/webp',
  '.gif':  'image/gif',
  '.svg':  'image/svg+xml',
  '.ico':  'image/x-icon',
};

// --- (a) 永久301: 固定URL别名迁移 ---
const PERMANENT_301 = {
  '/shipping-and-logistics.html':   '/logistics-shipping.html',
  '/shipping-and-logistics':        '/logistics-shipping.html',
  '/how-it-works.html':             '/index.html#sourcing-process',
  '/how-it-works':                  '/index.html#sourcing-process',
  '/yiwu-market.html':              '/blog-yiwu-market-agent-for-foreigners.html',
  '/yiwu-market':                   '/blog-yiwu-market-agent-for-foreigners.html',
  '/blog-index.html':               '/blog.html',
  '/blog-index':                    '/blog.html',
  '/process.html':                  '/index.html#sourcing-process',
  '/process':                       '/index.html#sourcing-process',
  '/term.html':                     '/terms.html',
  '/term':                          '/terms.html',
  '/services.html':                 '/supplier-verification.html',
  '/services':                      '/supplier-verification.html',
};

// --- (0) 产品详情页合法SKU白名单 → 服务端301替代客户端JS redirect ---
const VALID_PRODUCT_SKUS = new Set([
'YS-CL-201A','YS-CL-102WS','YCS-MSF-001','YCS-BAC-007','YCS-SHO-022','YCS-SHO-023','YCS-CLO-001','YCS-KBM-001','YCS-CLO-002','YCS-CLO-003','YCS-CLO-004','YCS-CLN-001','YCS-STA-001','YCS-MSS-001','YCS-MSS-002','YCS-PCR-001','YCS-STA-005','YCS-STA-006','YCS-STA-007','YCS-MOT-001','YCS-MSK-001','YCS-MCH-001','YCS-AUT-001','YCS-MCS-001','YCS-MCS-002','YCS-MSS-003','YCS-MSK-002','YCS-MHD-001','YCS-FIT-001','YCS-OTH-001','YCS-OTH-006','YCS-OTH-007','YCS-OTH-008','YCS-OTH-009','YCS-CLO-005','YCS-CLO-006','YCS-SOC-003','YCS-SOC-004','YCS-OTH-002','YCS-OTH-010','YCS-OTH-011','YCS-ACC-001','YCS-SKN-001','YCS-HOM-001','YCS-OTH-003','YCS-OTH-004','YCS-MCH-002','YCS-STO-001','YCS-BAC-002','YCS-STO-003','YCS-STO-004','YCS-MOT-003','YCS-MHD-002','YCS-MHD-003','YCS-MHD-004','YCS-AUS-001','YCS-AUS-002','YCS-AUS-003','YCS-AUS-004','YCS-AUS-005','YCS-AUS-006','YCS-AUS-007','YCS-PHO-001','YCS-MHD-005','YCS-PHO-002','YCS-MOT-005','YCS-MOT-006','YCS-MOT-007','YCS-MOT-008','YCS-STO-005','YCS-STO-006','YCS-STO-007','YCS-STO-009','YCS-KST-001','YCS-STO-010','YCS-DGO-001','YCS-STO-011','YCS-KST-002','YCS-MOT-009','YCS-SHO-024','YCS-SHO-001','YCS-PCR-003','YCS-STO-012','YCS-SMA-001','YCS-SMA-002','YCS-SMA-003','YCS-AVD-001','YCS-KBM-002','YCS-MOT-004','YCS-KID-001','YCS-AUS-008','YCS-ACC-004','YCS-CLO-007','YCS-HOM-002','YCS-STO-015','YCS-OUT-001','YCS-SHO-002','YCS-OUT-002','YCS-LED-002','YCS-OUT-003','YCS-TOY-001','YCS-BBC-002','YCS-TOY-002','YCS-TOY-003','YCS-TOY-004','YCS-CLO-008','YCS-LED-003','YCS-TOY-005','YCS-BBC-003','YCS-TOY-006','YCS-CLN-003','YCS-KST-004','YCS-STO-017','YCS-STO-018','YCS-STO-019','YCS-STO-020','YCS-TAB-001','YCS-STO-021','YCS-KST-005','YCS-MHD-007','YCS-DGO-002','YCS-STO-022','YCS-STO-023','YCS-STO-024','YCS-STO-025','YCS-STO-026','YCS-STO-028','YCS-BBC-004','YCS-SKN-003','YCS-HAB-002','YCS-HAB-008','YCS-STO-031','YCS-TOY-007','YCS-HAB-009','YCS-HAB-010','YCS-TOY-071','YCS-SMA-004','YCS-SMA-005','YCS-SMA-006','YCS-SMA-007','YCS-BTY-002','YCS-BTY-003','YCS-LAP-001','YCS-PCR-004','YCS-PCR-005','YCS-PCR-006','YCS-PCR-007','YCS-AUT-002','YCS-DGO-003','YCS-KST-006','YCS-HOM-003','YCS-KUT-001','YCS-KST-007','YCS-KST-008','YCS-PHO-004','YCS-STO-032','YCS-TOY-008','YCS-CLO-036','YCS-MHD-008','YCS-MHD-009','YCS-AVD-002','YCS-SMA-008','YCS-AVD-003','YCS-MOT-011','YCS-MOT-012','YCS-STO-035','YCS-KST-028','YCS-STO-036','YCS-MHD-010','YCS-MSS-011','YCS-STO-037','YCS-TOY-009','YCS-HOM-024','YCS-KST-009','YCS-STO-038','YCS-BAG-002','YCS-STO-039','YCS-AUT-003','YCS-HAB-003','YCS-BAG-003','YCS-HAB-005','YCS-CLN-004','YCS-MCH-003','YCS-MCH-004','YCS-MCH-005','YCS-KBM-003','YCS-STO-040','YCS-STO-041','YCS-STO-042','YCS-CLO-009','YCS-CLO-010','YCS-CLO-011','YCS-CLO-012','YCS-CLO-013','YCS-SHO-025','YCS-SHO-003','YCS-SHO-004','YCS-SHO-005','YCS-BBC-005','YCS-BBC-008','YCS-BBC-009','YCS-BBC-010','YCS-KID-002','YCS-LED-004','YCS-TOY-010','YCS-TOY-011','YCS-TOY-012','YCS-TOY-013','YCS-TOY-014','YCS-TOY-015','YCS-TOY-016','YCS-TOY-017','YCS-TOY-018','YCS-MUS-001','YCS-TOY-019','YCS-CLN-005','YCS-CLN-006','YCS-CLN-008','YCS-STO-043','YCS-HOM-004','YCS-CLN-009','YCS-PCR-009','YCS-KST-011','YCS-KST-012','YCS-LAP-002','YCS-KUT-002','YCS-KUT-003','YCS-LED-005','YCS-CUP-003','YCS-AUT-004','YCS-LED-006','YCS-CUP-016','YCS-CLO-014','YCS-SHO-026','YCS-KAP-001','YCS-STO-044','YCS-STO-045','YCS-MSS-007','YCS-OTH-005','YCS-BTY-004','YCS-SKN-009','YCS-CUP-017','YCS-SKN-005','YCS-BTY-005','YCS-FIT-002','YCS-BTY-006','YCS-KID-003','YCS-KID-004','YCS-CUP-004','YCS-HWR-003','YCS-ACC-005','YCS-CLO-015','YCS-CLO-016','YCS-BAG-005','YCS-AUS-009','YCS-CLO-017','YCS-FIT-003','YCS-FIT-004','YCS-TOY-072','YCS-TOY-020','YCS-TOY-021','YCS-TOY-022','YCS-HWR-004','YCS-HWR-005','YCS-CLN-010','YCS-SKN-006','YCS-SMA-009','YCS-SMA-010','YCS-KAP-002','YCS-SMA-013','YCS-CUP-005','YCS-SKN-010','YCS-MCH-006','YCS-SMA-011','YCS-SMA-012','YCS-PHO-005','YCS-HAB-006','YCS-HAB-011','YCS-HAB-012','YCS-FIT-005','YCS-DGO-005','YCS-TOY-024','YCS-MOT-014','YCS-CUP-006','YCS-CUP-007','YCS-TOY-026','YCS-MSS-009','YCS-KUT-004','YCS-KUT-005','YCS-KUT-006','YCS-KUT-007','YCS-KST-013','YCS-TOY-027','YCS-TOY-028','YCS-TOY-029','YCS-CLO-018','YCS-CLO-019','YCS-TOY-030','YCS-TOY-031','YCS-TOY-032','YCS-DGO-006','YCS-DGO-007','YCS-PHO-006','YCS-KST-015','YCS-CUP-009','YCS-CUP-010','YCS-LED-007','YCS-KUT-008','YCS-KUT-009','YCS-HWR-006','YCS-KUT-010','YCS-CUP-011','YCS-AVD-004','YCS-MHD-011','YCS-HOM-005','YCS-STO-048','YCS-TOY-033','YCS-TOY-034','YCS-TOY-035','YCS-TOY-036','YCS-HOM-006','YCS-CLO-020','YCS-CLO-021','YCS-CLO-022','YCS-ACC-006','YCS-ACC-002','YCS-HOM-007','YCS-TOY-037','YCS-STA-008','YCS-CLN-011','YCS-CLN-012','YCS-CLN-013','YCS-FIT-006','YCS-FIT-007','YCS-FIT-008','YCS-FIT-009','YCS-MCH-007','YCS-MCH-008','YCS-MCH-009','YCS-MCH-010','YCS-LAP-003','YCS-LED-008','YCS-LAP-004','YCS-MCH-011','YCS-AVD-005','YCS-TOY-038','YCS-STA-002','YCS-STA-003','YCS-KID-006','YCS-AUT-005','YCS-TOY-039','YCS-TOY-040','YCS-TOY-041','YCS-TOY-042','YCS-KAP-003','YCS-HOM-008','YCS-TOY-043','YCS-TOY-044','YCS-TOY-045','YCS-TOY-046','YCS-TOY-047','YCS-TOY-048','YCS-TOY-049','YCS-FIT-011','YCS-HWR-007','YCS-HWR-008','YCS-HWR-009','YCS-TOY-051','YCS-TOY-052','YCS-CLO-024','YCS-DGO-008','YCS-AVD-006','YCS-DGO-009','YCS-MHD-012','YCS-MOT-015','YCS-AUS-010','YCS-BAG-009','YCS-AUT-006','YCS-MHD-013','YCS-CLO-025','YCS-CLO-026','YCS-LED-009','YCS-LED-010','YCS-LED-011','YCS-LED-013','YCS-LED-014','YCS-LED-015','YCS-LAP-005','YCS-STO-049','YCS-KST-016','YCS-KST-017','YCS-SKN-007','YCS-TOY-053','YCS-TOY-054','YCS-TOY-055','YCS-TOY-056','YCS-TOY-057','YCS-TOY-058','YCS-TOY-059','YCS-TOY-060','YCS-HWR-010','YCS-CLN-014','YCS-SHO-008','YCS-MSK-003','YCS-TAB-002','YCS-KID-008','YCS-KID-009','YCS-KID-010','YCS-KID-011','YCS-KID-012','YCS-KID-013','YCS-HOM-009','YCS-AUT-007','YCS-AUS-011','YCS-CUP-018','YCS-MUS-003','YCS-LAP-007','YCS-SHO-027','YCS-TOY-063','YCS-TOY-065','YCS-KID-014','YCS-TOY-066','YCS-TOY-067','YCS-KID-015','YCS-FAN-001','YCS-SHO-010','YCS-DGO-010','YCS-MCS-005','YCS-DGO-011','YCS-SHO-011','YCS-LED-016','YCS-HAB-007','YCS-SHO-012','YCS-SHO-013','YCS-SHO-028','YCS-SHO-014','YCS-HOM-010','YCS-PET-001','YCS-FIT-012','YCS-FIT-013','YCS-OFC-003','YCS-ACC-003','YCS-MHD-014','YCS-KID-016','YCS-MHD-017','YCS-DGO-012','YCS-MHD-018','YCS-LED-017','YCS-LAP-008','YCS-SKN-008','YCS-MHD-019','YCS-MHD-020','YCS-PHO-007','YCS-PHO-008','YCS-MHD-021','YCS-CLN-015','YCS-LAP-009','YCS-SWI-001','YCS-SWI-002','YCS-CLO-027','YCS-CLO-029','YCS-CLO-031','YCS-CLO-032','YCS-SHO-029','YCS-CLN-016','YCS-SHO-030','YCS-SHO-017','YCS-SHO-031','YCS-FAN-002','YCS-HOM-012','YCS-HOM-013','YCS-HOM-014','YCS-CLN-017','YCS-STA-009','YCS-STA-010','YCS-TOY-068','YCS-KUT-012','YCS-KID-017','YCS-TOY-069','YCS-OTH-012','YCS-OTH-013','YCS-OTH-014','YCS-OTH-015','YCS-OTH-016','YCS-KST-021','YCS-TOY-070','YCS-STA-011','YCS-FAN-003','YCS-SHO-032','YCS-SHO-033','YCS-FAN-004','YCS-HOM-016','YCS-HOM-017','YCS-HOM-018','YCS-HOM-019','YCS-HOM-020','YCS-HOM-021','YCS-HAB-013','YCS-FTB-002','YCS-KUT-013','YCS-STO-051','YCS-HAB-014','YCS-AUS-014','YCS-CLN-020','YCS-HOM-022','YCS-MOT-019','YCS-DGO-013','YCS-DGO-014','YCS-DGO-015','YCS-MUS-002','YCS-BAC-003','YCS-BAC-004','YCS-BAG-010','YCS-BAC-005','YCS-BAC-008','YCS-BAC-006','YCS-MOT-020','YCS-CLO-035','YCS-FTB-003','YCS-SHO-034','YCS-MHD-022','YCS-ART-001','YCS-ART-002','YCS-ART-003','YCS-ART-004','YCS-ART-005','YCS-ART-006','YCS-ART-007','YCS-ART-008','YCS-CLN-018','YCS-LED-018','YCS-ART-009','YCS-SWI-010','YCS-SWI-006','YCS-SWI-007','YCS-STO-052','YCS-BAC-009','YCS-STO-053','YCS-STO-054','YCS-KID-018','YCS-KST-022','YCS-LOC-001','YCS-KST-023','YCS-LOC-002','YCS-LOC-003','YCS-KST-026','YCS-LOC-004','YCS-LOC-005','YCS-KUT-014','YCS-CUP-013','YCS-CUP-014','YCS-CUP-015','YCS-MHD-023','YCS-KID-019','YCS-STO-055','YCS-KUT-015','YCS-KST-027','YCS-FIT-014','YCS-CLN-019','YCS-CLO-038','YCS-CLO-041','YCS-CLO-043','YCS-OFC-004','YCS-AUS-012','YCS-AUS-013','YCS-BAC-001','YCS-BAG-001','YCS-BAG-006','YCS-BAG-007','YCS-BBC-001','YCS-BBC-006','YCS-BBC-007','YCS-BBC-011','YCS-BTY-001','YCS-CLN-002','YCS-CLN-007','YCS-CLO-023','YCS-CLO-028','YCS-CLO-030','YCS-CLO-037','YCS-CLO-039','YCS-CLO-040','YCS-CLO-042','YCS-CLO-044','YCS-CLO-045','YCS-CUP-001','YCS-CUP-002','YCS-CUP-012','YCS-DGO-004','YCS-DRY-001','YCS-FIT-010','YCS-FTB-001','YCS-HAB-001','YCS-HAB-004','YCS-HOM-011','YCS-HOM-015','YCS-HOM-023','YCS-HWR-001','YCS-KID-005','YCS-KID-007','YCS-KST-003','YCS-KST-010','YCS-KST-018','YCS-KST-019','YCS-KST-020','YCS-KUT-011','YCS-KUT-016','YCS-LAP-006','YCS-LED-001','YCS-LED-012','YCS-MCS-003','YCS-MHD-015','YCS-MOT-002','YCS-MOT-010','YCS-MOT-013','YCS-MOT-017','YCS-MSS-004','YCS-MSS-005','YCS-MSS-006','YCS-OFC-001','YCS-PCR-002','YCS-PCR-008','YCS-PHO-003','YCS-SHO-006','YCS-SHO-007','YCS-SHO-009','YCS-SHO-015','YCS-SHO-016','YCS-SHO-035','YCS-SHO-036','YCS-SHO-037','YCS-SHO-038','YCS-SHO-039','YCS-SHO-040','YCS-SHO-041','YCS-SHO-042','YCS-SHO-043','YCS-SKN-002','YCS-SKN-004','YCS-SOC-001','YCS-STA-004','YCS-STO-002','YCS-STO-008','YCS-STO-013','YCS-STO-014','YCS-STO-016','YCS-STO-027','YCS-STO-029','YCS-STO-030','YCS-STO-033','YCS-STO-034','YCS-SWI-003','YCS-SWI-005','YCS-TOY-023','YCS-TOY-025','YCS-TOY-061','YCS-TOY-062'
]);

// --- (1) 旧数字产品ID → 新SKU: 301永久迁移 (解决GSC 404) ---
const LEGACY_ID_TO_SKU = {'1':'YS-CL-201A','2':'YS-CL-102WS','23':'YCS-MSF-001','24':'YCS-BAC-007','25':'YCS-SHO-022','26':'YCS-SHO-023','27':'YCS-CLO-001','28':'YCS-KBM-001','29':'YCS-CLO-002','30':'YCS-CLO-003','31':'YCS-CLO-004','32':'YCS-CLN-001','33':'YCS-STA-001','34':'YCS-MSS-001','35':'YCS-MSS-002','36':'YCS-PCR-001','37':'YCS-STA-005','38':'YCS-STA-006','39':'YCS-STA-007','40':'YCS-MOT-001','41':'YCS-MSK-001','42':'YCS-MCH-001','43':'YCS-AUT-001','44':'YCS-MCS-001','45':'YCS-MCS-002','46':'YCS-MSS-003','47':'YCS-MSK-002','48':'YCS-MHD-001','49':'YCS-FIT-001','50':'YCS-OTH-001','51':'YCS-OTH-006','52':'YCS-OTH-007','53':'YCS-OTH-008','54':'YCS-OTH-009','55':'YCS-CLO-005','56':'YCS-CLO-006','57':'YCS-SOC-003','58':'YCS-SOC-004','59':'YCS-OTH-002','60':'YCS-OTH-010','61':'YCS-OTH-011','62':'YCS-ACC-001','63':'YCS-SKN-001','64':'YCS-HOM-001','65':'YCS-OTH-003','66':'YCS-OTH-004','67':'YCS-MCH-002','68':'YCS-STO-001','69':'YCS-BAC-002','70':'YCS-STO-003','71':'YCS-STO-004','72':'YCS-MOT-003','73':'YCS-MHD-002','74':'YCS-MHD-003','75':'YCS-MHD-004','76':'YCS-AUS-001','77':'YCS-AUS-002','78':'YCS-AUS-003','79':'YCS-SMA-001','80':'YCS-SMA-002','81':'YCS-SMA-003','82':'YCS-AVD-001','83':'YCS-KBM-002','84':'YCS-MOT-004','85':'YCS-KID-001','86':'YCS-AUS-004','87':'YCS-AUS-005','88':'YCS-AUS-006','89':'YCS-AUS-007','90':'YCS-PHO-001','91':'YCS-MHD-005','92':'YCS-PHO-002','93':'YCS-MOT-005','94':'YCS-MOT-006','95':'YCS-MOT-007','96':'YCS-MOT-008','97':'YCS-STO-005','98':'YCS-STO-006','99':'YCS-STO-007','100':'YCS-STO-009','101':'YCS-KST-001','102':'YCS-STO-010','103':'YCS-DGO-001','104':'YCS-STO-011','105':'YCS-KST-002','106':'YCS-MOT-009','107':'YCS-SHO-024','108':'YCS-SHO-001','109':'YCS-PCR-003','110':'YCS-STO-012','111':'YCS-SMA-004','112':'YCS-KBM-003','113':'YCS-MHD-006','114':'YCS-MCH-003','115':'YCS-AUS-008','116':'YCS-ACC-004','117':'YCS-CLO-007','118':'YCS-HOM-002','119':'YCS-STO-015','120':'YCS-OUT-001','121':'YCS-SHO-002','122':'YCS-OUT-002','123':'YCS-LED-002','124':'YCS-OUT-003','125':'YCS-TOY-001','126':'YCS-BBC-002','127':'YCS-TOY-002','128':'YCS-TOY-003','129':'YCS-TOY-004','130':'YCS-CLO-008','131':'YCS-LED-003','132':'YCS-TOY-005','133':'YCS-BBC-003','134':'YCS-TOY-006','135':'YCS-CLN-003','136':'YCS-KST-004','137':'YCS-STO-017','138':'YCS-STO-018','139':'YCS-STO-019','140':'YCS-STO-020','141':'YCS-TAB-001','142':'YCS-STO-021','143':'YCS-KST-005','144':'YCS-MHD-007','145':'YCS-DGO-002','146':'YCS-STO-022','147':'YCS-STO-023','148':'YCS-STO-024','149':'YCS-STO-025','150':'YCS-STO-026','151':'YCS-STO-028','152':'YCS-BBC-004','153':'YCS-SKN-003','154':'YCS-HAB-002','155':'YCS-HAB-008','156':'YCS-STO-031','157':'YCS-TOY-007','158':'YCS-HAB-009','159':'YCS-HAB-010','160':'YCS-TOY-071','161':'YCS-SMA-005','162':'YCS-SMA-006','163':'YCS-SMA-007','164':'YCS-BTY-002','165':'YCS-BTY-003','166':'YCS-LAP-001','167':'YCS-PCR-004','168':'YCS-PCR-005','169':'YCS-PCR-006','170':'YCS-PCR-007','171':'YCS-AUT-002','172':'YCS-DGO-003','173':'YCS-KST-006','174':'YCS-HOM-003','175':'YCS-KUT-001','176':'YCS-KST-007','177':'YCS-KST-008','178':'YCS-PHO-004','179':'YCS-STO-032','180':'YCS-TOY-008','181':'YCS-CLO-036','182':'YCS-MHD-008','183':'YCS-MHD-009','184':'YCS-AVD-002','185':'YCS-SMA-008','186':'YCS-AVD-003','187':'YCS-MOT-011','188':'YCS-MOT-012','189':'YCS-STO-035','190':'YCS-KST-028','191':'YCS-STO-036','192':'YCS-MHD-010','193':'YCS-MSS-011','194':'YCS-STO-037','195':'YCS-TOY-009','196':'YCS-HOM-024','197':'YCS-KST-009','198':'YCS-STO-038','199':'YCS-BAG-002','200':'YCS-STO-039','201':'YCS-AUT-003','202':'YCS-HAB-003','203':'YCS-BAG-003','204':'YCS-HAB-005','205':'YCS-CLN-004','206':'YCS-MCH-004','207':'YCS-MCH-005','208':'YCS-KBM-003','209':'YCS-STO-040','210':'YCS-STO-041','211':'YCS-STO-042','212':'YCS-CLO-009','213':'YCS-CLO-010','214':'YCS-CLO-011','215':'YCS-CLO-012','216':'YCS-CLO-013','217':'YCS-SHO-025','218':'YCS-SHO-003','219':'YCS-SHO-004','220':'YCS-SHO-005','221':'YCS-BBC-005','222':'YCS-BBC-008','223':'YCS-BBC-009','224':'YCS-BBC-010','225':'YCS-KID-002','226':'YCS-LED-004','227':'YCS-TOY-010','228':'YCS-TOY-011','229':'YCS-TOY-012','230':'YCS-TOY-013','231':'YCS-TOY-014','232':'YCS-TOY-015','233':'YCS-TOY-016','234':'YCS-TOY-017','235':'YCS-TOY-018','236':'YCS-MUS-001','237':'YCS-TOY-019','238':'YCS-CLN-005','239':'YCS-CLN-006','240':'YCS-CLN-008','241':'YCS-STO-043','242':'YCS-HOM-004','243':'YCS-CLN-009','244':'YCS-PCR-009','245':'YCS-KST-011','246':'YCS-KST-012','247':'YCS-LAP-002','248':'YCS-KUT-002','249':'YCS-KUT-003','250':'YCS-LED-005','251':'YCS-CUP-003','252':'YCS-AUT-004','253':'YCS-LED-006','254':'YCS-CUP-016','255':'YCS-CLO-014','256':'YCS-SHO-026','257':'YCS-KAP-001','258':'YCS-STO-044','259':'YCS-STO-045','260':'YCS-MSS-007','261':'YCS-OTH-005','262':'YCS-BTY-004','263':'YCS-SKN-009','264':'YCS-CUP-017','265':'YCS-SKN-005','266':'YCS-BTY-005','267':'YCS-FIT-002','268':'YCS-BTY-006','269':'YCS-KID-003','270':'YCS-KID-004','271':'YCS-CUP-004','272':'YCS-HWR-003','273':'YCS-ACC-005','274':'YCS-CLO-015','275':'YCS-CLO-016','276':'YCS-BAG-005','277':'YCS-AUS-009','278':'YCS-CLO-017','279':'YCS-FIT-003','280':'YCS-FIT-004','281':'YCS-TOY-072','282':'YCS-TOY-020','283':'YCS-TOY-021','284':'YCS-TOY-022','285':'YCS-HWR-004','286':'YCS-HWR-005','287':'YCS-CLN-010','288':'YCS-SKN-006','289':'YCS-SMA-009','290':'YCS-SMA-010','291':'YCS-KAP-002','292':'YCS-SMA-013','293':'YCS-CUP-005','294':'YCS-SKN-010','295':'YCS-MCH-006','296':'YCS-SMA-011','297':'YCS-SMA-012','298':'YCS-PHO-005','299':'YCS-HAB-006','300':'YCS-HAB-011','301':'YCS-HAB-012','302':'YCS-FIT-005','303':'YCS-DGO-005','304':'YCS-TOY-024','305':'YCS-MOT-014','306':'YCS-CUP-006','307':'YCS-CUP-007','308':'YCS-TOY-026','309':'YCS-MSS-009','310':'YCS-KUT-004','311':'YCS-KUT-005','312':'YCS-KUT-006','313':'YCS-KUT-007','314':'YCS-KST-013','315':'YCS-TOY-027','316':'YCS-TOY-028','317':'YCS-TOY-029','318':'YCS-CLO-018','319':'YCS-CLO-019','320':'YCS-TOY-030','321':'YCS-TOY-031','322':'YCS-TOY-032','323':'YCS-DGO-006','324':'YCS-DGO-007','325':'YCS-PHO-006','326':'YCS-KST-015','327':'YCS-CUP-009','328':'YCS-CUP-010','329':'YCS-LED-007','330':'YCS-KUT-008','331':'YCS-KUT-009','332':'YCS-HWR-006','333':'YCS-KUT-010','334':'YCS-CUP-011','335':'YCS-AVD-004','336':'YCS-MHD-011','337':'YCS-HOM-005','338':'YCS-STO-048','339':'YCS-TOY-033','340':'YCS-TOY-034','341':'YCS-TOY-035','342':'YCS-TOY-036','343':'YCS-HOM-006','344':'YCS-CLO-020','345':'YCS-CLO-021','346':'YCS-CLO-022','347':'YCS-ACC-006','348':'YCS-ACC-002','349':'YCS-HOM-007','350':'YCS-TOY-037','351':'YCS-STA-008','352':'YCS-CLN-011','353':'YCS-CLN-012','354':'YCS-CLN-013','355':'YCS-FIT-006','356':'YCS-FIT-007','357':'YCS-FIT-008','358':'YCS-FIT-009','359':'YCS-MCH-007','360':'YCS-MCH-008','361':'YCS-MCH-009','362':'YCS-MCH-010','363':'YCS-LAP-003','364':'YCS-LED-008','365':'YCS-LAP-004','366':'YCS-MCH-011','367':'YCS-AVD-005','368':'YCS-TOY-038','369':'YCS-STA-002','370':'YCS-STA-003','371':'YCS-KID-006','372':'YCS-AUT-005','373':'YCS-TOY-039','374':'YCS-TOY-040','375':'YCS-TOY-041','376':'YCS-TOY-042','377':'YCS-KAP-003','378':'YCS-HOM-008','379':'YCS-TOY-043','380':'YCS-TOY-044','381':'YCS-TOY-045','382':'YCS-TOY-046','383':'YCS-TOY-047','384':'YCS-TOY-048','385':'YCS-TOY-049','386':'YCS-FIT-011','387':'YCS-HWR-007','388':'YCS-HWR-008','389':'YCS-HWR-009','390':'YCS-TOY-051','391':'YCS-TOY-052','392':'YCS-CLO-024','393':'YCS-DGO-008','394':'YCS-AVD-006','395':'YCS-DGO-009','396':'YCS-MHD-012','397':'YCS-MOT-015','398':'YCS-AUS-010','399':'YCS-BAG-009','400':'YCS-AUT-006','401':'YCS-MHD-013','402':'YCS-CLO-025','403':'YCS-CLO-026','404':'YCS-LED-009','405':'YCS-LED-010','406':'YCS-LED-011','407':'YCS-LED-013','408':'YCS-LED-014','409':'YCS-LED-015','410':'YCS-LAP-005','411':'YCS-STO-049','412':'YCS-KST-016','413':'YCS-KST-017','414':'YCS-SKN-007','415':'YCS-TOY-053','416':'YCS-TOY-054','417':'YCS-TOY-055','418':'YCS-TOY-056','419':'YCS-TOY-057','420':'YCS-TOY-058','421':'YCS-TOY-059','422':'YCS-TOY-060','423':'YCS-HWR-010','424':'YCS-CLN-014','425':'YCS-SHO-008','426':'YCS-MSK-003','427':'YCS-TAB-002','428':'YCS-KID-008','429':'YCS-KID-009','430':'YCS-KID-010','431':'YCS-KID-011','432':'YCS-KID-012','433':'YCS-KID-013','434':'YCS-HOM-009','435':'YCS-AUT-007','436':'YCS-AUS-011','437':'YCS-CUP-018','438':'YCS-MUS-003','439':'YCS-LAP-007','440':'YCS-SHO-027','441':'YCS-TOY-063','442':'YCS-TOY-065','443':'YCS-KID-014','444':'YCS-TOY-066','445':'YCS-TOY-067','446':'YCS-KID-015','447':'YCS-FAN-001','448':'YCS-SHO-010','449':'YCS-DGO-010','450':'YCS-MCS-005','451':'YCS-DGO-011','452':'YCS-SHO-011','453':'YCS-LED-016','454':'YCS-HAB-007','455':'YCS-SHO-012','456':'YCS-SHO-013','457':'YCS-SHO-028','458':'YCS-SHO-014','459':'YCS-HOM-010','460':'YCS-PET-001','461':'YCS-FIT-012','462':'YCS-FIT-013','463':'YCS-OFC-003','464':'YCS-ACC-003','465':'YCS-MHD-014','466':'YCS-KID-016','467':'YCS-MHD-017','468':'YCS-DGO-012','469':'YCS-MHD-018','470':'YCS-LED-017','471':'YCS-LAP-008','472':'YCS-SKN-008','473':'YCS-MHD-019','474':'YCS-MHD-020','475':'YCS-PHO-007','476':'YCS-PHO-008','477':'YCS-MHD-021','478':'YCS-CLN-015','479':'YCS-LAP-009','480':'YCS-SWI-001','481':'YCS-SWI-002','482':'YCS-CLO-027','483':'YCS-CLO-029','484':'YCS-CLO-031','485':'YCS-CLO-032','486':'YCS-SHO-029','487':'YCS-CLN-016','488':'YCS-SHO-030','489':'YCS-SHO-017','490':'YCS-SHO-031','491':'YCS-FAN-002','492':'YCS-HOM-012','493':'YCS-HOM-013','494':'YCS-HOM-014','495':'YCS-CLN-017','496':'YCS-STA-009','497':'YCS-STA-010','498':'YCS-TOY-068','499':'YCS-KUT-012','500':'YCS-KID-017','501':'YCS-TOY-069','502':'YCS-OTH-012','503':'YCS-OTH-013','504':'YCS-OTH-014','505':'YCS-OTH-015','506':'YCS-OTH-016','507':'YCS-KST-021','508':'YCS-TOY-070','509':'YCS-STA-011','510':'YCS-FAN-003','511':'YCS-SHO-032','512':'YCS-SHO-033','513':'YCS-FAN-004','514':'YCS-HOM-016','515':'YCS-HOM-017','516':'YCS-HOM-018','517':'YCS-HOM-019','518':'YCS-HOM-020','519':'YCS-HOM-021','520':'YCS-HAB-013','521':'YCS-FTB-002','522':'YCS-KUT-013','523':'YCS-STO-051','524':'YCS-HAB-014','525':'YCS-AUS-014','526':'YCS-CLN-020','527':'YCS-HOM-022','528':'YCS-MOT-019','529':'YCS-DGO-013','530':'YCS-DGO-014','531':'YCS-DGO-015','532':'YCS-MUS-002','533':'YCS-BAC-003','534':'YCS-BAC-004','535':'YCS-BAG-010','536':'YCS-BAC-005','537':'YCS-BAC-008','538':'YCS-BAC-006','539':'YCS-MOT-020','540':'YCS-CLO-035','541':'YCS-FTB-003','542':'YCS-SHO-034','543':'YCS-MHD-022','544':'YCS-ART-001','545':'YCS-ART-002','546':'YCS-ART-003','547':'YCS-ART-004','548':'YCS-ART-005','549':'YCS-ART-006','550':'YCS-ART-007','551':'YCS-ART-008','552':'YCS-CLN-018','553':'YCS-LED-018','554':'YCS-ART-009','555':'YCS-SWI-010','556':'YCS-SWI-006','557':'YCS-SWI-007','558':'YCS-STO-052','559':'YCS-BAC-009','560':'YCS-STO-053','561':'YCS-STO-054','562':'YCS-KID-018','563':'YCS-KST-022','564':'YCS-LOC-001','565':'YCS-KST-023','566':'YCS-LOC-002','567':'YCS-LOC-003','568':'YCS-KST-026','569':'YCS-LOC-004','570':'YCS-LOC-005','571':'YCS-KUT-014','572':'YCS-CUP-013','573':'YCS-CUP-014','574':'YCS-CUP-015','575':'YCS-MHD-023','576':'YCS-KID-019','577':'YCS-STO-055','578':'YCS-KUT-015','579':'YCS-KST-027','580':'YCS-FIT-014','581':'YCS-CLN-019','582':'YCS-CLO-038','583':'YCS-CLO-041','584':'YCS-CLO-043','585':'YCS-OFC-004','586':'YCS-AUS-012','587':'YCS-AUS-013','588':'YCS-BAC-001','589':'YCS-BAG-001','590':'YCS-BAG-006','591':'YCS-BAG-007','592':'YCS-BBC-001','593':'YCS-BBC-006','594':'YCS-BBC-007','595':'YCS-BBC-011','596':'YCS-BTY-001','597':'YCS-CLN-002','598':'YCS-CLN-007','599':'YCS-CLO-023','600':'YCS-CLO-028','601':'YCS-CLO-030','602':'YCS-CLO-037','603':'YCS-CLO-039','604':'YCS-CLO-040','605':'YCS-CLO-042','606':'YCS-CLO-044','607':'YCS-CLO-045','608':'YCS-CUP-001','609':'YCS-CUP-002','610':'YCS-CUP-012','611':'YCS-DGO-004','612':'YCS-DRY-001','613':'YCS-FIT-010','614':'YCS-FTB-001','615':'YCS-HAB-001','616':'YCS-HAB-004','617':'YCS-HOM-011','618':'YCS-HOM-015','619':'YCS-HOM-023','620':'YCS-HWR-001','621':'YCS-KID-005','622':'YCS-KID-007','623':'YCS-KST-003','624':'YCS-KST-010','625':'YCS-KST-018','626':'YCS-KST-019','627':'YCS-KST-020','628':'YCS-KUT-011','629':'YCS-KUT-016','630':'YCS-LAP-006','631':'YCS-LED-001','632':'YCS-LED-012','633':'YCS-MCS-003','634':'YCS-MHD-015','635':'YCS-MOT-002','636':'YCS-MOT-010','637':'YCS-MOT-013','638':'YCS-MOT-017','639':'YCS-MSS-004','640':'YCS-MSS-005','641':'YCS-MSS-006','642':'YCS-OFC-001','643':'YCS-PCR-002','644':'YCS-PCR-008','645':'YCS-PHO-003','646':'YCS-SHO-006','647':'YCS-SHO-007','648':'YCS-SHO-009','649':'YCS-SHO-015','650':'YCS-SHO-016','651':'YCS-SHO-035','652':'YCS-SHO-036','653':'YCS-SHO-037','654':'YCS-SHO-038','655':'YCS-SHO-039','656':'YCS-SHO-040','657':'YCS-SHO-041','658':'YCS-SHO-042','659':'YCS-SHO-043','660':'YCS-SKN-002','661':'YCS-SKN-004','662':'YCS-SOC-001','663':'YCS-STA-004','664':'YCS-STO-002','665':'YCS-STO-008','666':'YCS-STO-013','667':'YCS-STO-014','668':'YCS-STO-016','669':'YCS-STO-027','670':'YCS-STO-029','671':'YCS-STO-030','672':'YCS-STO-033','673':'YCS-STO-034','674':'YCS-SWI-003','675':'YCS-SWI-005','676':'YCS-TOY-023','677':'YCS-TOY-025','678':'YCS-TOY-061','679':'YCS-TOY-062'};

/** 301 helper: 永久缓存, 附带任何原始 query (lang=xx 等) */
function redirect301(url, suffix) {
  const location = url.origin + suffix + (suffix.includes('#') ? '' : url.search);
  return new Response(null, {
    status: 301,
    headers: {
      Location: location,
      'Cache-Control': 'public, max-age=31536000, immutable',
    },
  });
}

export async function onRequest(context) {
  const { request, next, env } = context;
  const url = new URL(request.url);

  // 只处理 GET
  if (request.method !== 'GET') return next();

  // --- (a) 硬编码永久301 ---
  const permanentTarget = PERMANENT_301[url.pathname];
  if (permanentTarget) return redirect301(url, permanentTarget);

  // --- (0) products.html?product=SKU → /product-SKU.html (服务端301, 避免JS redirect) ---
  if (url.pathname === '/products.html' || url.pathname === '/products') {
    const productParam = url.searchParams.get('product');
    if (productParam) {
      // 优先SKU匹配: 合法SKU白名单
      if (VALID_PRODUCT_SKUS.has(productParam)) {
        return redirect301(url, `/product-${productParam}.html`);
      }
      // 否则尝试旧数字ID匹配
      const sku = LEGACY_ID_TO_SKU[productParam];
      if (sku) {
        return redirect301(url, `/product-${sku}.html`);
      }
    }
  }

  // --- (1) /product-<纯数字>.html 或 /product-<纯数字> → 新SKU 301 ---
  const legacyMatch = url.pathname.match(/^\/product-(\d+)(?:\.html)?$/i);
  if (legacyMatch) {
    const sku = LEGACY_ID_TO_SKU[legacyMatch[1]];
    if (sku) {
      return redirect301(url, `/product-${sku}.html`);
    }
    // 未知ID: 继续走默认处理器 (最终404, 但不再是"跳转+404"链)
  }

  // --- (3) Image proxy: /images/SKU.ext (仅小写路径) ---
  // 重要: 本地 /Images/ (大写I) 目录下的静态文件不走此代理，交给 CF Pages 静态处理器
  // 原因: 之前忽略大小写的正则会拦截 /Images/*.jpg，远程代理失败返回占位SVG，导致轮播图不显示
  const imageMatch = url.pathname.match(/^\/(images|img)\/([^/]+)$/);
  if (imageMatch) {
    const filename = decodeURIComponent(imageMatch[2]);
    const ext = (filename.match(/\.(\w+)$/) || [])[1];
    const mime = ext ? IMAGE_MIME['.' + ext.toLowerCase()] : null;

    // 先查本地构建产物 (ASSETS)，命中直接返回
    if (env && env.ASSETS && typeof env.ASSETS.fetch === 'function') {
      try {
        const cleanUrl = `${url.origin}${url.pathname}`;
        const localAsset = await env.ASSETS.fetch(new Request(cleanUrl, request));
        if (localAsset && localAsset.status === 200 && localAsset.body) {
          const headers = new Headers(localAsset.headers);
          if (mime && !headers.has('Content-Type')) headers.set('Content-Type', mime);
          headers.set('Cache-Control', 'public, max-age=2592000, s-maxage=2592000');
          headers.set('X-Yeatru-Img', 'local-assets');
          return new Response(localAsset.body, { status: 200, headers });
        }
      } catch (_) { /* 本地无此文件，继续远程 */ }
    }

    const upstreamUrl = `${GITHUB_IMAGE_REPO}/${filename}`;
    try {
      const imgResp = await fetch(upstreamUrl, {
        headers: { 'User-Agent': 'YeatruSourcing/1.0 (+https://www.yeatru.com)' },
        cf: { cacheTtl: 86400, polish: 'original' },
      });
      if (imgResp.status === 200) {
        const headers = new Headers(imgResp.headers);
        if (mime && !headers.has('Content-Type')) headers.set('Content-Type', mime);
        headers.set('Cache-Control', 'public, max-age=86400, s-maxage=86400');
        headers.set('Access-Control-Allow-Origin', '*');
        headers.set('X-Yeatru-Img', 'proxy-ok');
        return new Response(imgResp.body, { status: 200, headers });
      }
      const jsdelivrUrl = `https://cdn.jsdelivr.net/gh/Yeatru/Image@main/Images/${filename}`;
      const jdResp = await fetch(jsdelivrUrl, {
        headers: { 'User-Agent': 'YeatruSourcing/1.0' },
        cf: { cacheTtl: 86400, polish: 'original' },
      });
      if (jdResp.status === 200) {
        const headers = new Headers(jdResp.headers);
        if (mime && !headers.has('Content-Type')) headers.set('Content-Type', mime);
        headers.set('Cache-Control', 'public, max-age=86400, s-maxage=86400');
        headers.set('X-Yeatru-Img', 'jsdelivr-fallback');
        return new Response(jdResp.body, { status: 200, headers });
      }
      // 上游也找不到 → fallback 给 Pages 静态处理器 (可能命中本地文件或返回404)
      return next();
    } catch (e) {
      return next();
    }
  }

  // --- (2) HTML URL 服务 (v5 统一无后缀/.html双通道, 彻底解决 Bing 308 redirecting) ---
  // 根因: Cloudflare Pages 默认对无后缀路径如 /testimonials 返回 308 → /testimonials.html
  //      Bing Site Explorer 把这些核心服务页归入 "URLs redirecting" (不计入 Indexed)
  // 修复: 对 "无后缀路径 + /pathname.html" 都统一用 env.ASSETS.fetch 直读静态文件, HTTP 200 返回.
  //      这也让两种 URL 格式都能被搜索引擎当作"正确URL直接收录", 避免重定向丢权重.
  const isHtmlSuffix = /\.html$/i.test(url.pathname);
  const isRoot = url.pathname === '/';
  const isCleanPath = !isHtmlSuffix && !isRoot
    && !/\.[a-z0-9]{1,6}$/i.test(url.pathname)     // 排除 .jpg/.css/.svg 等静态资源
    && !/^\/(images?|img|assets?|css|js|fonts?|_)/i.test(url.pathname);

  if (isHtmlSuffix || isCleanPath || isRoot) {
    let clean;
    let htmlPath;
    if (isRoot) {
      clean = '/';
      htmlPath = '/index.html';
    } else if (isHtmlSuffix) {
      clean = url.pathname.replace(/\.html$/i, '');
      htmlPath = url.pathname;
    } else {
      // /testimonials → clean=/testimonials htmlPath=/testimonials.html
      clean = url.pathname.replace(/\/+$/, '') || '/';
      htmlPath = clean + '.html';
    }
    const pathsToTry = [clean, htmlPath];

    if (env && env.ASSETS && typeof env.ASSETS.fetch === 'function') {
      for (const p of pathsToTry) {
        try {
          const r = new Request(url.origin + p + url.search, request);
          const asset = await env.ASSETS.fetch(r);
          if (asset && asset.status === 200 && asset.body) {
            const h = new Headers(asset.headers);
            h.delete('Location');
            h.delete('Refresh');
            if (!h.has('Content-Type')) h.set('Content-Type', 'text/html; charset=utf-8');
            // 强制 X-Robots-Tag index (data.html 特殊加强版)
            if (/\/data(\.html)?$/i.test(url.pathname)) {
              h.set('X-Robots-Tag', 'index, follow, max-snippet:-1, max-image-preview:large, max-video-preview:-1');
            } else if (!h.has('X-Robots-Tag')) {
              h.set('X-Robots-Tag', 'index, follow, max-snippet:-1, max-image-preview:large');
            }
            return new Response(asset.body, { status: 200, headers: h });
          }
          // ASSETS.fetch 也可能返回 301/308 (CF 自动), 剥掉 Location 直接用其 body
          if (asset && (asset.status === 301 || asset.status === 308) && asset.body) {
            const h = new Headers(asset.headers);
            h.delete('Location');
            h.delete('Refresh');
            if (!h.has('Content-Type')) h.set('Content-Type', 'text/html; charset=utf-8');
            if (/\/data(\.html)?$/i.test(url.pathname)) {
              h.set('X-Robots-Tag', 'index, follow, max-snippet:-1, max-image-preview:large, max-video-preview:-1');
            } else if (!h.has('X-Robots-Tag')) {
              h.set('X-Robots-Tag', 'index, follow, max-snippet:-1, max-image-preview:large');
            }
            return new Response(asset.body, { status: 200, headers: h });
          }
        } catch (_) { /* try next path */ }
      }
    }

    // 兜底: 交给 Pages 默认处理器 (可能出现 308, 但这是无法匹配文件时的极端情况)
    return next();
  }

  // 其他 (静态资源 / /images /products带参数等): 透传
  return next();
}
