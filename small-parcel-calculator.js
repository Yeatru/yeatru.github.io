/*!
 * Yeatru Sourcing — Small-Parcel Shipping Calculator
 * ------------------------------------------------------------------
 * Auto-injects a "Shipping Calculator" card on every product detail page
 * (pages containing .detail-spec-cards and a [data-sku] anchor). Computes
 * small-parcel freight from small-parcel-rates.js (CNY → USD @ 6.6).
 *
 * Wires up:
 *   - country <select> (90 destinations grouped by continent)
 *   - qty <input> synced with the page's existing #detailQty (bidirectional)
 *   - "Estimate weight" hint (unit kg × qty = total kg, N parcels)
 *   - live result panel: billable weight, freight, per-pkg fee, total USD,
 *     ETA, customs notes
 *   - JSON-LD OfferShippingDetails.shippingRate.value update for SEO
 *
 * Depends on: window.YEATRU_SP (small-parcel-rates.js).
 */
(function (global) {
  'use strict';
  if (!global.YEATRU_SP) {
    if (typeof console !== 'undefined' && console.warn) {
      console.warn('[small-parcel-calculator] YEATRU_SP missing — small-parcel-rates.js must load first.');
    }
    return;
  }
  var SP = global.YEATRU_SP;

  function init() {
    var host = document.querySelector('.detail-spec-cards');
    if (!host) return; // not a product detail page

    // Pull SKU + mainCategory from the JSON-LD Product payload
    var sku = '';
    var mainCategory = '';
    var ld = document.querySelectorAll('script[type="application/ld+json"]');
    for (var i = 0; i < ld.length; i++) {
      try {
        var parsed = JSON.parse(ld[i].textContent);
        var node = Array.isArray(parsed) ? parsed[0] : parsed;
        if (node && (node['@type'] === 'Product' || node.sku)) {
          sku = node.sku || sku;
          if (node.category) mainCategory = typeof node.category === 'string' ? node.category : (node.category.name || '');
          break;
        }
      } catch (e) { /* try next */ }
    }
    if (!sku) {
      // Fallback: read from the quote/WhatsApp link data-sku attribute
      var q = document.querySelector('[data-sku]');
      if (q) sku = q.getAttribute('data-sku') || '';
    }
    if (!sku) return;

    var card = buildCard(sku, mainCategory);
    host.parentNode.insertBefore(card, host.nextSibling);

    wireEvents(card, sku, mainCategory);
    recalc(card, sku, mainCategory);
  }

  function buildCard(sku, mainCategory) {
    var card = document.createElement('div');
    card.className = 'sp-calc-card card border-0 bg-light mt-3';
    card.setAttribute('data-sp-sku', sku);
    card.innerHTML =
      '<div class="card-body p-3">' +
        '<div class="d-flex align-items-center mb-2">' +
          '<i class="fas fa-truck-fast text-indigo me-2"></i>' +
          '<h3 class="h6 mb-0">Small-Parcel Shipping Calculator</h3>' +
        '</div>' +
        '<p class="small text-muted mb-3">Live small-parcel freight to 90+ countries. Rate card CNY→USD @ 6.6. Billable weight = ceil to 0.5 kg. Heavy consignments auto-split into multiple parcels per destination weight limit.</p>' +
        '<div class="row g-2 mb-3">' +
          '<div class="col-7">' +
            '<label class="form-label small mb-1" for="spCountry">Destination</label>' +
            '<select id="spCountry" class="form-select form-select-sm"></select>' +
          '</div>' +
          '<div class="col-5">' +
            '<label class="form-label small mb-1" for="spQty">Quantity</label>' +
            '<input type="number" id="spQty" class="form-control form-control-sm" min="1" value="100" inputmode="numeric">' +
          '</div>' +
        '</div>' +
        '<div class="sp-result" id="spResult"></div>' +
        '<p class="small text-muted mt-2 mb-0">Indicative only — final DDP quote (duties, insurance, last-mile) returns within 24 h via <a href="contact.html">request a quote</a>.</p>' +
      '</div>';

    // Populate country dropdown grouped by continent
    var sel = card.querySelector('#spCountry');
    var lastContinent = null;
    SP.COUNTRY_LIST.forEach(function (r) {
      if (r.continent !== lastContinent) {
        var og = document.createElement('optgroup');
        og.label = r.continent;
        sel.appendChild(og);
        lastContinent = r.continent;
      }
      var o = document.createElement('option');
      o.value = r.code;
      o.textContent = r.name_cn + ' (' + r.code + ')';
      sel.appendChild(o);
    });
    // Default destination: try geolocale, else US
    sel.value = (navigator.language && navigator.language.indexOf('zh') === 0) ? 'CN' : 'US';
    // CN isn't in the table — so reset to US if it failed
    if (!sel.value || !SP.RATES_BY_COUNTRY[sel.value]) sel.value = 'US';

    // Sync initial qty from the page's main #detailQty if present
    var detailQty = document.getElementById('detailQty');
    if (detailQty) {
      var v = parseInt(detailQty.value, 10);
      if (isFinite(v) && v > 0) card.querySelector('#spQty').value = v;
    }
    return card;
  }

  function wireEvents(card, sku, mainCategory) {
    var sel = card.querySelector('#spCountry');
    var qty = card.querySelector('#spQty');
    var result = card.querySelector('#spResult');

    function onChange() { recalc(card, sku, mainCategory); }
    sel.addEventListener('change', onChange);
    qty.addEventListener('input', onChange);

    // Bidirectional sync with the main page qty input (#detailQty)
    var detailQty = document.getElementById('detailQty');
    if (detailQty) {
      detailQty.addEventListener('input', function () {
        var v = parseInt(detailQty.value, 10);
        if (isFinite(v) && v > 0 && parseInt(qty.value, 10) !== v) {
          qty.value = v;
          recalc(card, sku, mainCategory);
        }
      });
      qty.addEventListener('input', function () {
        var v = parseInt(qty.value, 10);
        if (isFinite(v) && v > 0 && parseInt(detailQty.value, 10) !== v) {
          detailQty.value = v;
          // Don't trigger detailQty's input handler recursively
          // (the guard above prevents the loop)
        }
      });
    }
  }

  function recalc(card, sku, mainCategory) {
    var sel = card.querySelector('#spCountry');
    var qty = card.querySelector('#spQty');
    var result = card.querySelector('#spResult');
    var countryCode = sel.value;
    var q = parseInt(qty.value, 10);
    if (!isFinite(q) || q < 1) q = 1;

    var r = SP.calc({ sku: sku, mainCategory: mainCategory, qty: q, countryCode: countryCode });
    if (!r) {
      result.innerHTML = '<div class="alert alert-warning small mb-0 py-2">No rate for this destination — request a custom quote.</div>';
      return;
    }

    var estNote = '';
    if (!hasProductWeight(sku, mainCategory)) {
      estNote = '<div class="sp-est-note small text-muted">Weight estimated from category (' + mainCategory + ' ≈ ' + r.unitKg.toFixed(2) + ' kg/unit). Final quote uses actual weighed parcel.</div>';
    }

    result.innerHTML =
      '<table class="table table-sm mb-0 sp-result-table">' +
        '<tbody>' +
          '<tr><td class="small text-muted">Estimated unit weight</td><td class="text-end fw-medium">' + r.unitKg.toFixed(2) + ' kg</td></tr>' +
          '<tr><td class="small text-muted">Total actual weight (' + r.qty + ' pcs)</td><td class="text-end fw-medium">' + r.actualKg.toFixed(2) + ' kg</td></tr>' +
          '<tr><td class="small text-muted">Parcels (max ' + r.maxPerPkg + ' kg each)</td><td class="text-end fw-medium">' + r.numPackages + '</td></tr>' +
          '<tr><td class="small text-muted">Billable weight</td><td class="text-end fw-medium">' + r.totalBillableKg.toFixed(2) + ' kg</td></tr>' +
          '<tr><td class="small text-muted">Freight</td><td class="text-end">' + SP.formatUsd(r.freightUsd) + '</td></tr>' +
          '<tr><td class="small text-muted">Per-parcel fee (' + r.numPackages + '×)</td><td class="text-end">' + SP.formatUsd(r.perPackageFeeUsd) + '</td></tr>' +
          '<tr class="sp-total-row"><td class="fw-semibold">Estimated shipping</td><td class="text-end fw-bold fs-5">' + SP.formatUsd(r.totalUsd) + '</td></tr>' +
        '</tbody>' +
      '</table>' +
      '<div class="sp-meta small text-muted mt-2"><i class="fas fa-clock me-1"></i> ' + escapeHtml(r.eta) + ' · ' + escapeHtml(r.countryCn) + ' (' + r.countryCode + ')</div>' +
      (r.notes ? '<div class="sp-notes small text-muted"><i class="fas fa-circle-info me-1"></i> ' + escapeHtml(r.notes) + '</div>' : '') +
      estNote;

    // Update JSON-LD OfferShippingDetails.shippingRate to the computed total (SEO)
    updateJsonLdShipping(r, countryCode);
  }

  function hasProductWeight(sku, mainCategory) {
    if (global.YEATRU_SP_WEIGHTS && global.YEATRU_SP_WEIGHTS[sku]) return true;
    return false; // using category default
  }

  function updateJsonLdShipping(r, countryCode) {
    var ld = document.querySelectorAll('script[type="application/ld+json"]');
    for (var i = 0; i < ld.length; i++) {
      try {
        var raw = ld[i].textContent;
        var parsed = JSON.parse(raw);
        var node = Array.isArray(parsed) ? parsed[0] : parsed;
        if (!node) continue;
        var updated = false;
        if (node.offers && node.offers.shippingDetails) {
          node.offers.shippingDetails.shippingRate.value = Math.round(r.totalUsd * 100) / 100;
          // Make sure destination includes the user's selection (best-effort)
          var dest = node.offers.shippingDetails.shippingDestination;
          if (dest && Array.isArray(dest.addressCountry) && dest.addressCountry.indexOf(countryCode) === -1) {
            dest.addressCountry.push(countryCode);
          }
          updated = true;
        }
        if (updated) {
          ld[i].textContent = JSON.stringify(parsed);
        }
      } catch (e) { /* skip */ }
    }
  }

  function escapeHtml(s) {
    return String(s == null ? '' : s)
      .replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;').replace(/'/g, '&#39;');
  }

  // Bootstrap on DOM ready
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})(typeof window !== 'undefined' ? window : this);
