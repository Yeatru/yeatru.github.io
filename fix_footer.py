#!/usr/bin/env python3
"""
Replace all footer sections in HTML files with the standard footer from index.html.
The standard footer is extracted from index.html and used as the universal footer.
"""
import re
import os
import glob

# The standard footer from index.html
STANDARD_FOOTER = '''<footer class="footer">
 <div class="container">
 <div class="row">
 <div class="col-lg-3 col-md-6">
 <a href="/" class="footer-brand">
 <span class="brand-logo-box"><img src="logo.svg" alt="Yeatru Sourcing Logo" width="38" height="38"></span></a>
 <p class="footer-desc" data-i18n="footer.desc">Professional China sourcing agent helping businesses worldwide find reliable suppliers and quality products at competitive prices.</p>
 <div class="footer-social">
 <a href="https://facebook.com/NeilLaw" target="_blank" class="footer-social-icon" rel="noopener noreferrer" aria-label="Facebook Yeatru Sourcing"><i class="fab fa-facebook-f"></i></a>
 <a href="https://www.linkedin.com/in/neil-liu-398983257" target="_blank" class="footer-social-icon" rel="noopener noreferrer" aria-label="LinkedIn Yeatru Sourcing"><i class="fab fa-linkedin-in"></i></a>
 <a href="https://wa.me/8615988516408" target="_blank" class="footer-social-icon" rel="noopener noreferrer" aria-label="WhatsApp Yeatru Sourcing"><i class="fab fa-whatsapp"></i></a>
 <a href="https://t.me/YeatruSourcing" target="_blank" class="footer-social-icon" rel="noopener noreferrer" aria-label="Telegram Yeatru Sourcing"><i class="fab fa-telegram"></i></a>
 <a href="https://instagram.com/yeatru_sourcing" target="_blank" class="footer-social-icon" rel="noopener noreferrer" aria-label="Instagram Yeatru Sourcing"><i class="fab fa-instagram"></i></a>
 </div>
 </div>
 <div class="col-lg-3 col-md-6">
 <h3 class="footer-title" data-i18n="footer.quickLinks">Quick Links</h3>
 <a href="/" class="footer-link">Home</a>
 <a href="products.html" class="footer-link">Products</a>
 <a href="supplier-verification.html" class="footer-link">Services</a>
 <a href="payment.html" class="footer-link">Payment</a>
 <a href="about.html" class="footer-link">About Us</a>
 <a href="blog.html" class="footer-link">Blog</a>
 <a href="contact.html" class="footer-link">Contact Us</a>
 <a href="data.html" class="footer-link">Our Data</a>
 <a href="testimonials.html" class="footer-link">Testimonials</a>
 <a href="faq.html" class="footer-link">FAQ</a>
 </div>
 <div class="col-lg-3 col-md-6">
 <h3 class="footer-title" data-i18n="footer.services">Our Services</h3>
 <a href="supplier-verification.html" class="footer-link">Supplier Verification</a>
 <a href="product-sourcing.html" class="footer-link">Product Sourcing</a>
 <a href="quality-control.html" class="footer-link">Quality Control</a>
 <a href="logistics-shipping.html" class="footer-link">Logistics &amp; Warehousing</a>
 <a href="price-negotiation.html" class="footer-link">Price Negotiation</a>
 <a href="factory-audit.html" class="footer-link">Factory Audit</a>
 <a href="sample-order.html" class="footer-link">Sample Order</a>
 <a href="oem.html" class="footer-link">OEM Customization</a>
 </div>
 <div class="col-lg-3 col-md-6">
 <h3 class="footer-title" data-i18n="footer.contact">Contact Us</h3>
 <a href="https://maps.google.com/?q=NO.188+Shangcheng+Avenue+Yiwu+Zhejiang+322000+China" target="_blank" rel="noopener noreferrer" class="footer-link"><i class="fas fa-map-marker-alt me-2"></i> NO.188 Shangcheng Ave Yiwu Zhejiang China</a>
 <a href="tel:+8615988516408" class="footer-link"><i class="fas fa-phone me-2"></i> +86 15988516408</a>
 <a href="mailto:info@yeatru.com" class="footer-link"><i class="fas fa-envelope me-2"></i> info@yeatru.com</a>
 <a href="contact.html#opening-hours" class="footer-link"><i class="fas fa-clock me-2"></i> Open: Mo-Sa 09:00–18:00 · 24/7 Online</a>
 <div class="footer-payment-section mt-3">
 <h4 class="footer-payment-label" data-i18n="footer.paymentMethods">Payment Methods</h4>
 <div class="footer-payment-icons-vertical">
 <span class="payment-icon"><i class="fab fa-cc-visa"></i><span>Visa</span></span>
 <span class="payment-icon"><i class="fab fa-cc-mastercard"></i><span>MasterCard</span></span>
 <span class="payment-icon"><i class="fab fa-paypal"></i><span>PayPal</span></span>
 <span class="payment-icon"><i class="fas fa-university"></i><span>Bank Transfer</span></span>
 </div>
 </div>
 </div>
 </div>

 <div class="footer-bottom">
 <p>&copy; 2022–2026 · Yeatru Sourcing (YIWU ETRUE TRADING CO. LTD.). <span data-i18n="footer.allRightsReserved">All rights reserved.</span> |
 <a href="privacy.html" class="footer-link d-inline" data-i18n="footer.privacyPolicy">Privacy Policy</a> |
 <a href="terms.html" class="footer-link d-inline" data-i18n="footer.termsOfService">Terms of Service</a>
 |
 <a href="refund.html" class="footer-link d-inline">Refund Policy</a> |
 <a href="nda.html" class="footer-link d-inline">NDA & Confidentiality</a></p>
 </div>
 </div>
 </footer>'''

# Regex to match <footer ...>...</footer> (non-greedy, DOTALL)
FOOTER_PATTERN = re.compile(
    r'<footer\s+[^>]*>.*?</footer>',
    re.DOTALL | re.IGNORECASE
)

def process_file(filepath):
    """Replace footer in a single HTML file."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        return False, f"Read error: {e}"

    # Check if file has a footer
    match = FOOTER_PATTERN.search(content)
    if not match:
        return False, "No footer found"

    old_footer = match.group(0)

    # Skip if already matches (quick check)
    if old_footer.strip() == STANDARD_FOOTER.strip():
        return True, "Already standard"

    # Replace the footer
    new_content = content[:match.start()] + STANDARD_FOOTER + content[match.end():]

    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        return True, "Replaced"
    except Exception as e:
        return False, f"Write error: {e}"

def main():
    # Find all HTML files in the workspace
    html_files = sorted(glob.glob('/workspace/*.html'))
    print(f"Found {len(html_files)} HTML files")

    replaced = 0
    skipped = 0
    errors = 0
    no_footer = 0

    for filepath in html_files:
        filename = os.path.basename(filepath)
        success, msg = process_file(filepath)

        if success:
            if msg == "Replaced":
                replaced += 1
            else:
                skipped += 1
        else:
            if msg == "No footer found":
                no_footer += 1
            else:
                errors += 1
                print(f"  ERROR: {filename}: {msg}")

    print(f"\nResults:")
    print(f"  Replaced: {replaced}")
    print(f"  Already standard: {skipped}")
    print(f"  No footer: {no_footer}")
    print(f"  Errors: {errors}")

if __name__ == '__main__':
    main()
