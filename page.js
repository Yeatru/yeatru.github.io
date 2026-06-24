const PAGE_DATA_KEY = 'yeatruPageData';
const PAGE_DATA_URL = 'page-data.json';

let currentPageId = '';
let currentPageMode = 'preview';

const i18n = {
    en: {
        nav: { home: 'Home', products: 'Products', services: 'Services', sourcingProcess: 'Sourcing Process', testimonials: 'Testimonials', aboutUs: 'About Us', contactUs: 'Contact Us', login: 'Login', logout: 'Logout', servicePlans: 'Service Plans' },
        login: { title: 'Admin Login', username: 'Username', enterUsername: 'Enter username', password: 'Password', enterPassword: 'Enter password', error: 'Incorrect username or password!', cancel: 'Cancel', submit: 'Login' },
        page: { edit: 'Edit Page', save: 'Save', export: 'Export Data', import: 'Import', preview: 'Preview' }
    },
    es: {
        nav: { home: 'Inicio', products: 'Productos', services: 'Servicios', sourcingProcess: 'Proceso de Suministro', testimonials: 'Testimonios', aboutUs: 'Sobre Nosotros', contactUs: 'Contáctenos', login: 'Iniciar Sesión', logout: 'Cerrar Sesión', servicePlans: 'Planes de Servicio' },
        login: { title: 'Inicio de Sesión de Administrador', username: 'Nombre de Usuario', enterUsername: 'Ingrese el nombre de usuario', password: 'Contraseña', enterPassword: 'Ingrese la contraseña', error: '¡Nombre de usuario o contraseña incorrectos!', cancel: 'Cancelar', submit: 'Iniciar Sesión' },
        page: { edit: 'Editar Página', save: 'Guardar', export: 'Exportar Datos', import: 'Importar', preview: 'Vista Previa' }
    },
    fr: {
        nav: { home: 'Accueil', products: 'Produits', services: 'Services', sourcingProcess: 'Processus d\'Approvisionnement', testimonials: 'Témoignages', aboutUs: 'À Propos de Nous', contactUs: 'Nous Contacter', login: 'Connexion', logout: 'Déconnexion', servicePlans: 'Plans de Service' },
        login: { title: 'Connexion Administrateur', username: 'Nom d\'Utilisateur', enterUsername: 'Entrez le nom d\'utilisateur', password: 'Mot de Passe', enterPassword: 'Entrez le mot de passe', error: 'Nom d\'utilisateur ou mot de passe incorrect!', cancel: 'Annuler', submit: 'Se Connecter' },
        page: { edit: 'Modifier la Page', save: 'Enregistrer', export: 'Exporter les Données', import: 'Importer', preview: 'Aperçu' }
    },
    ru: {
        nav: { home: 'Главная', products: 'Продукты', services: 'Услуги', sourcingProcess: 'Процесс Поставок', testimonials: 'Отзывы', aboutUs: 'О Нас', contactUs: 'Связаться', login: 'Войти', logout: 'Выйти', servicePlans: 'Тарифы' },
        login: { title: 'Вход', username: 'Логин', enterUsername: 'Введите логин', password: 'Пароль', enterPassword: 'Введите пароль', error: 'Неверные данные!', cancel: 'Отмена', submit: 'Войти' },
        page: { edit: 'Редактировать', save: 'Сохранить', export: 'Экспорт Данных', import: 'Импорт', preview: 'Просмотр' }
    }
};

function getCurrentLang() {
    return localStorage.getItem('yeatruLang') || 'en';
}

function setCurrentLang(lang) {
    localStorage.setItem('yeatruLang', lang);
}

function t(key) {
    const lang = getCurrentLang();
    const keys = key.split('.');
    let obj = i18n[lang] || i18n.en;
    for (const k of keys) {
        if (obj && obj[k]) obj = obj[k];
        else return key;
    }
    return obj;
}

function applyI18n() {
    document.querySelectorAll('[data-i18n]').forEach(el => {
        const key = el.getAttribute('data-i18n');
        const val = t(key);
        if (val && val !== key) el.textContent = val;
    });
    document.querySelectorAll('[data-i18n-placeholder]').forEach(el => {
        const key = el.getAttribute('data-i18n-placeholder');
        const val = t(key);
        if (val && val !== key) el.placeholder = val;
    });
    const langNames = { en: 'English', es: 'Español', fr: 'Français', ru: 'Русский' };
    const cur = document.getElementById('current-lang');
    if (cur) cur.textContent = langNames[getCurrentLang()] || 'English';
}

function isAdmin() {
    return localStorage.getItem('yeatruAdminLoggedIn') === 'true';
}

function escapeHtml(str) {
    if (str === null || str === undefined) return '';
    return String(str).replace(/[&<>"']/g, function (s) {
        return ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[s]);
    });
}

function renderBrandLogo() {
    const url = localStorage.getItem('yeatruBrandLogo');
    const img = document.getElementById('brandLogoImg');
    const fallback = document.getElementById('brandLogoFallback');
    const footerImg = document.getElementById('footerLogoImg');
    const footerFallback = document.getElementById('footerLogoFallback');
    if (url) {
        if (img) {
            img.src = url;
            img.style.display = 'block';
        }
        if (fallback) fallback.style.display = 'none';
        if (footerImg) {
            footerImg.src = url;
            footerImg.style.display = 'block';
        }
        if (footerFallback) footerFallback.style.display = 'none';
    } else {
        if (img) {
            img.src = '';
            img.style.display = 'none';
        }
        if (fallback) fallback.style.display = '';
        if (footerImg) {
            footerImg.src = '';
            footerImg.style.display = 'none';
        }
        if (footerFallback) footerFallback.style.display = '';
    }
}

function getPageData() {
    try {
        const s = localStorage.getItem(PAGE_DATA_KEY);
        if (s) return JSON.parse(s);
    } catch (e) {}
    return getDefaultPageData();
}

function savePageData(data) {
    localStorage.setItem(PAGE_DATA_KEY, JSON.stringify(data));
}

function getDefaultPageData() {
    return {
        pages: {
            services: {
                title: 'Our Comprehensive Sourcing Services',
                subtitle: 'We offer end-to-end sourcing solutions tailored to your business needs',
                services: [
                    { icon: 'fa-user-check', title: 'Supplier Verification', desc: 'We thoroughly vet and verify suppliers to ensure they meet international quality standards and business ethics.' },
                    { icon: 'fa-search', title: 'Product Sourcing', desc: 'Find the right products at competitive prices with our extensive network of reliable manufacturers and suppliers.' },
                    { icon: 'fa-check-square', title: 'Quality Control', desc: 'Comprehensive quality inspection at every stage of production to ensure products meet your specifications.' },
                    { icon: 'fa-truck', title: 'Logistics & Shipping', desc: 'Hassle-free shipping solutions including sea, air and express delivery with competitive rates.' },
                    { icon: 'fa-handshake', title: 'Price Negotiation', desc: 'Leverage our local expertise to negotiate the best prices and payment terms with suppliers.' },
                    { icon: 'fa-shield-alt', title: 'Risk Management', desc: 'Mitigate risks associated with international trade including payment security and delivery guarantees.' }
                ]
            },
            process: {
                title: 'Our Simple Sourcing Process',
                subtitle: 'We make sourcing from China straightforward and transparent',
                steps: [
                    { number: 1, title: 'Your Requirements', desc: 'Share your product specifications, quantity, budget and timeline with our team.' },
                    { number: 2, title: 'Supplier Matching', desc: 'We identify and verify the best suppliers that match your specific requirements.' },
                    { number: 3, title: 'Sample & Pricing', desc: 'Obtain samples and competitive pricing quotes from pre-vetted suppliers.' },
                    { number: 4, title: 'Delivery & Support', desc: 'We handle production oversight, quality control and shipping to your doorstep.' }
                ]
            },
            plans: {
                title: 'Our Service Plans',
                subtitle: 'Choose the sourcing plan that fits your business needs',
                plans: [
                    { name: 'Plan A', title: 'On-Demand', subtitle: 'Flat fee per task', features: ['Payment Assistance', 'On-Demand QC Inspection', 'Factory On-site Audits', 'Lab Testing Coordination'], featured: false },
                    { name: 'Plan B', title: '0% Commission', subtitle: "Don't have suppliers yet", features: ['Manufacturing Sourcing', 'Quote Collection', 'Manufacturing Solution Support', 'Order Management', 'Mass Production Follow Up', 'Goods Consolidation', 'Free AQL 2.5 Quality Inspection', '2 Months Free Warehousing', 'Door-to-Door Logistics', 'Quality Guarantee & Compensation'], featured: true },
                    { name: 'Plan C', title: '3% Commission', subtitle: 'Have suppliers already', features: ['Supplier Coordination', 'Full Order Follow-up', 'Goods Consolidation', 'Free AQL 2.5 Quality Inspection', '1 Month Free Warehousing', 'Door-to-Door Logistics'], featured: false },
                    { name: 'Plan D', title: 'Prep', subtitle: '3PL Prep & Fulfillment', features: ['100% piece-by-piece Inspection', 'Compliance Labeling', 'Bundling & Kitting', 'Retail-Ready Re-pack', 'Sample Consolidation', 'Supplier Cargo Pick-up'], featured: false }
                ]
            },
            testimonials: {
                title: 'What Clients Say',
                subtitle: 'Feedback from our global buyers',
                testimonials: [
                    { text: 'Yeatru Sourcing helped me source 5000+ storage boxes from Yiwu, great quality and fast shipping. Highly recommended!', author: 'Marco', country: 'Italy', initial: 'M' },
                    { text: 'Professional team, strict quality control, and excellent after-sales service. Best China sourcing partner I ever worked with.', author: 'Anna', country: 'Germany', initial: 'A' },
                    { text: 'The price negotiation service saved me over 20% on my order. The logistics team ensured on-time delivery to the US. Very satisfied!', author: 'John', country: 'USA', initial: 'J' }
                ]
            },
            about: {
                title: 'About Yeatru Sourcing',
                profileTitle: 'Company Profile',
                profileDesc: 'Yeatru Sourcing is a professional one-stop sourcing agent located in Yiwu City, the world\'s largest small commodity distribution center. We specialize in providing global clients with reliable procurement services, supplier development, strict quality inspection, supplier management and integrated logistics solutions.',
                image: 'https://cdn.jsdelivr.net/gh/Yeatru/Image@main/Images/international%20trading%20city%20pic.jpg',
                stats: [
                    { number: '8+', label: 'Years in Business' },
                    { number: '500+', label: 'Global Clients' },
                    { number: '50+', label: 'Countries Served' },
                    { number: '24/7', label: 'Support Available' }
                ]
            },
            contact: {
                title: 'Get In Touch With Us',
                subtitle: 'Ready to start your sourcing journey? Fill out the form or contact us directly using the information below.',
                address: 'Yiwu City, Zhejiang Province, China',
                phone: '+86 15988516408 (WhatsApp)',
                email: 'info@yeatru.com'
            }
        }
    };
}

async function loadRemotePageData() {
    try {
        const res = await fetch(PAGE_DATA_URL + '?t=' + Date.now(), { cache: 'no-store' });
        if (res.ok) {
            const data = await res.json();
            if (data && data.pages) {
                localStorage.setItem(PAGE_DATA_KEY, JSON.stringify(data));
                return data;
            }
        }
    } catch (e) {}
    return null;
}

function renderPage(pageId) {
    currentPageId = pageId;
    const data = getPageData();
    const pageData = data.pages[pageId];
    if (!pageData) return;

    const pageTitle = document.getElementById('pageTitle');
    if (pageTitle) pageTitle.textContent = pageData.title || '';

    const pageSubtitle = document.getElementById('pageSubtitle');
    if (pageSubtitle) pageSubtitle.textContent = pageData.subtitle || '';

    if (pageId === 'services') {
        renderServicesPage(pageData);
        const plansData = data.pages.plans;
        if (plansData && document.getElementById('plansGrid')) {
            renderPlansPage(plansData);
        }
    } else if (pageId === 'process') {
        renderProcessPage(pageData);
    } else if (pageId === 'plans') {
        renderPlansPage(pageData);
    } else if (pageId === 'testimonials') {
        renderTestimonialsPage(pageData);
    } else if (pageId === 'about') {
        renderAboutPage(pageData);
    } else if (pageId === 'contact') {
        renderContactPage(pageData);
    }

    applyPageEditState();
}

function renderServicesPage(data) {
    const container = document.getElementById('servicesGrid');
    if (!container) return;
    container.innerHTML = '';
    (data.services || []).forEach((svc, idx) => {
        const col = document.createElement('div');
        col.className = 'col-lg-2 col-md-4 col-sm-6';
        col.innerHTML = `
            <div class="service-card">
                <div class="service-icon"><i class="fas ${escapeHtml(svc.icon || '')}"></i></div>
                <h3 class="service-title" data-editable="service-title" data-idx="${idx}">${escapeHtml(svc.title || '')}</h3>
                <p class="service-desc" data-editable="service-desc" data-idx="${idx}">${escapeHtml(svc.desc || '')}</p>
            </div>
        `;
        container.appendChild(col);
    });
}

function renderProcessPage(data) {
    const container = document.getElementById('processTimeline');
    if (!container) return;
    container.innerHTML = '';
    (data.steps || []).forEach((step, idx) => {
        const div = document.createElement('div');
        div.className = 'process-step-alt';
        div.innerHTML = `
            <div class="process-number">${step.number || idx + 1}</div>
            <h3 class="process-title" data-editable="step-title" data-idx="${idx}">${escapeHtml(step.title || '')}</h3>
            <p class="process-desc" data-editable="step-desc" data-idx="${idx}">${escapeHtml(step.desc || '')}</p>
        `;
        container.appendChild(div);
    });
}

function renderPlansPage(data) {
    const container = document.getElementById('plansGrid');
    if (!container) return;
    container.innerHTML = '';
    (data.plans || []).forEach((plan, idx) => {
        const col = document.createElement('div');
        col.className = 'col-lg-3 col-md-6';
        const planClass = plan.featured ? 'featured' : '';
        const planHeaderClass = `plan-${String.fromCharCode(97 + idx)}`;
        let featuresHtml = '';
        (plan.features || []).forEach(f => {
            featuresHtml += `<li data-editable="plan-feature" data-plan-idx="${idx}">${escapeHtml(f)}</li>`;
        });
        let headerHtml = '';
        if (plan.title) {
            headerHtml += `<div class="plan-name" data-editable="plan-name" data-idx="${idx}">${escapeHtml(plan.name || '')}</div>`;
            if (plan.title === '0% Commission' || plan.title === '3% Commission') {
                headerHtml += `<div class="plan-percent" data-editable="plan-percent" data-idx="${idx}">${escapeHtml(plan.title || '')}</div>`;
            } else {
                headerHtml += `<div class="plan-title" data-editable="plan-title" data-idx="${idx}">${escapeHtml(plan.title || '')}</div>`;
            }
            headerHtml += `<div class="plan-subtitle" data-editable="plan-subtitle" data-idx="${idx}">${escapeHtml(plan.subtitle || '')}</div>`;
        }
        col.innerHTML = `
            <div class="plan-card ${planClass}">
                <div class="plan-card-header ${planHeaderClass}">
                    ${headerHtml}
                </div>
                <div class="plan-card-body">
                    <ul class="plan-feature-list">${featuresHtml}</ul>
                </div>
            </div>
        `;
        container.appendChild(col);
    });
}

function renderTestimonialsPage(data) {
    const container = document.getElementById('testimonialsGrid');
    if (!container) return;
    container.innerHTML = '';
    (data.testimonials || []).forEach((t, idx) => {
        const col = document.createElement('div');
        col.className = 'col-lg-4 col-md-6';
        col.innerHTML = `
            <div class="testimonial-card">
                <div class="testimonial-quote-icon"><i class="fas fa-quote-left"></i></div>
                <div class="testimonial-stars"><i class="fas fa-star"></i><i class="fas fa-star"></i><i class="fas fa-star"></i><i class="fas fa-star"></i><i class="fas fa-star"></i></div>
                <p class="testimonial-text" data-editable="testimonial-text" data-idx="${idx}">${escapeHtml(t.text || '')}</p>
                <div class="d-flex align-items-center gap-2">
                    <div class="testimonial-avatar" data-editable="testimonial-initial" data-idx="${idx}">${escapeHtml(t.initial || t.author?.charAt(0) || '?')}</div>
                    <p class="testimonial-author">— <span data-editable="testimonial-author" data-idx="${idx}">${escapeHtml(t.author || '')}</span>, <span data-editable="testimonial-country" data-idx="${idx}">${escapeHtml(t.country || '')}</span></p>
                </div>
            </div>
        `;
        container.appendChild(col);
    });
}

function renderAboutPage(data) {
    const img = document.getElementById('aboutImage');
    if (img && data.image) {
        img.src = data.image;
        img.onerror = function() { this.src = 'https://picsum.photos/1200/420'; };
    }

    const profileTitle = document.getElementById('aboutProfileTitle');
    if (profileTitle) profileTitle.textContent = data.profileTitle || '';

    const profileDesc = document.getElementById('aboutProfileDesc');
    if (profileDesc) profileDesc.textContent = data.profileDesc || '';

    const statsContainer = document.getElementById('aboutStats');
    if (statsContainer) {
        statsContainer.innerHTML = '';
        (data.stats || []).forEach((stat, idx) => {
            const div = document.createElement('div');
            div.className = 'about-stat-item';
            div.innerHTML = `
                <div class="about-stat-number" data-editable="stat-number" data-idx="${idx}">${escapeHtml(stat.number || '')}</div>
                <div class="about-stat-label" data-editable="stat-label" data-idx="${idx}">${escapeHtml(stat.label || '')}</div>
            `;
            statsContainer.appendChild(div);
        });
    }
}

function renderContactPage(data) {
    const title = document.getElementById('contactInfoTitle');
    if (title) title.textContent = data.title || '';

    const subtitle = document.getElementById('contactInfoDesc');
    if (subtitle) subtitle.textContent = data.subtitle || '';

    const address = document.getElementById('contactAddress');
    if (address) address.textContent = data.address || '';

    const phone = document.getElementById('contactPhone');
    if (phone) phone.textContent = data.phone || '';

    const email = document.getElementById('contactEmail');
    if (email) email.textContent = data.email || '';
}

function applyPageEditState() {
    const isEdit = currentPageMode === 'edit' && isAdmin();
    document.querySelectorAll('[data-editable]').forEach(el => {
        el.contentEditable = isEdit ? 'true' : 'false';
    });
    document.body.classList.toggle('edit-mode', isEdit);

    const editBtn = document.getElementById('pageEditBtn');
    const saveBtn = document.getElementById('pageSaveBtn');
    if (editBtn) editBtn.style.display = isAdmin() ? 'inline-block' : 'none';
    if (saveBtn) saveBtn.style.display = (isAdmin() && isEdit) ? 'inline-block' : 'none';
}

function setPageMode(mode) {
    currentPageMode = mode;
    applyPageEditState();
}

function saveCurrentPage() {
    const data = getPageData();
    const pageData = data.pages[currentPageId];
    if (!pageData) return;

    if (currentPageId === 'services') {
        pageData.services = [];
        document.querySelectorAll('.service-card').forEach((card, idx) => {
            const title = card.querySelector('[data-editable="service-title"]')?.textContent || '';
            const desc = card.querySelector('[data-editable="service-desc"]')?.textContent || '';
            const icon = card.querySelector('.service-icon i')?.className?.replace('fas ', '') || 'fa-check';
            pageData.services.push({ icon, title, desc });
        });
        if (document.getElementById('plansGrid') && data.pages.plans) {
            data.pages.plans.plans = [];
            document.querySelectorAll('.plan-card').forEach((card, idx) => {
                const name = card.querySelector('[data-editable="plan-name"]')?.textContent || '';
                const title = card.querySelector('[data-editable="plan-title"]')?.textContent || card.querySelector('[data-editable="plan-percent"]')?.textContent || '';
                const subtitle = card.querySelector('[data-editable="plan-subtitle"]')?.textContent || '';
                const features = [];
                card.querySelectorAll('[data-editable="plan-feature"]').forEach(li => {
                    features.push(li.textContent || '');
                });
                const featured = card.classList.contains('featured');
                data.pages.plans.plans.push({ name, title, subtitle, features, featured });
            });
        }
    } else if (currentPageId === 'process') {
        pageData.steps = [];
        document.querySelectorAll('.process-step-alt').forEach((step, idx) => {
            const number = step.querySelector('.process-number')?.textContent || (idx + 1);
            const title = step.querySelector('[data-editable="step-title"]')?.textContent || '';
            const desc = step.querySelector('[data-editable="step-desc"]')?.textContent || '';
            pageData.steps.push({ number, title, desc });
        });
    } else if (currentPageId === 'testimonials') {
        pageData.testimonials = [];
        document.querySelectorAll('.testimonial-card').forEach((card, idx) => {
            const text = card.querySelector('[data-editable="testimonial-text"]')?.textContent || '';
            const author = card.querySelector('[data-editable="testimonial-author"]')?.textContent || '';
            const country = card.querySelector('[data-editable="testimonial-country"]')?.textContent || '';
            const initial = card.querySelector('[data-editable="testimonial-initial"]')?.textContent || '';
            pageData.testimonials.push({ text, author, country, initial });
        });
    } else if (currentPageId === 'about') {
        const profileTitle = document.querySelector('[data-editable="profile-title"]')?.textContent || pageData.profileTitle;
        const profileDesc = document.querySelector('[data-editable="profile-desc"]')?.textContent || pageData.profileDesc;
        if (profileTitle) pageData.profileTitle = profileTitle;
        if (profileDesc) pageData.profileDesc = profileDesc;
    } else if (currentPageId === 'contact') {
        const title = document.querySelector('[data-editable="contact-title"]')?.textContent || pageData.title;
        const subtitle = document.querySelector('[data-editable="contact-subtitle"]')?.textContent || pageData.subtitle;
        if (title) pageData.title = title;
        if (subtitle) pageData.subtitle = subtitle;
    }

    savePageData(data);
    alert('Page saved! Remember to export and upload to GitHub.');
}

function exportPageData() {
    const data = getPageData();
    const jsonStr = JSON.stringify(data, null, 2);
    const blob = new Blob([jsonStr], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'page-data.json';
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
}

function importPageData(file) {
    const reader = new FileReader();
    reader.onload = function(e) {
        try {
            const data = JSON.parse(e.target.result);
            if (data && data.pages) {
                savePageData(data);
                renderPage(currentPageId);
                alert('page-data.json imported successfully!');
            } else {
                alert('Invalid file format');
            }
        } catch (err) {
            alert('Failed to parse JSON: ' + err.message);
        }
    };
    reader.readAsText(file);
}

function updateLoginUI(loggedIn) {
    const loginBtn = document.getElementById('loginBtn');
    const logoutBtn = document.getElementById('logoutBtn');
    const pageEditBtn = document.getElementById('pageEditBtn');
    if (loginBtn) loginBtn.classList.toggle('d-none', loggedIn);
    if (logoutBtn) logoutBtn.classList.toggle('d-none', !loggedIn);
    if (pageEditBtn) pageEditBtn.style.display = loggedIn ? 'inline-block' : 'none';
}

document.addEventListener('DOMContentLoaded', function() {
    loadRemotePageData().then(() => {
        if (currentPageId) renderPage(currentPageId);
    });

    const loginBtn = document.getElementById('submitLogin');
    if (loginBtn) {
        loginBtn.addEventListener('click', function () {
            const username = document.getElementById('adminUsername')?.value?.trim();
            const password = document.getElementById('adminPassword')?.value?.trim();
            const errorEl = document.getElementById('loginError');
            if (username === 'Yeatru' && password === 'Ldz52385109') {
                localStorage.setItem('yeatruAdminLoggedIn', 'true');
                updateLoginUI(true);
                applyPageEditState();
                const loginModal = document.getElementById('loginModal');
                if (loginModal) {
                    const modalInstance = bootstrap.Modal.getInstance(loginModal) || new bootstrap.Modal(loginModal);
                    modalInstance.hide();
                }
                if (errorEl) errorEl.classList.add('d-none');
            } else {
                if (errorEl) errorEl.classList.remove('d-none');
            }
        });
    }

    const logoutBtn = document.getElementById('logoutBtn');
    if (logoutBtn) {
        logoutBtn.addEventListener('click', function () {
            localStorage.removeItem('yeatruAdminLoggedIn');
            updateLoginUI(false);
            setPageMode('preview');
        });
    }

    const editBtn = document.getElementById('pageEditBtn');
    if (editBtn) {
        editBtn.addEventListener('click', function() {
            if (currentPageMode === 'edit') {
                setPageMode('preview');
                this.innerHTML = '<i class="fas fa-edit me-1"></i> ' + t('page.edit');
            } else {
                setPageMode('edit');
                this.innerHTML = '<i class="fas fa-eye me-1"></i> ' + t('page.preview');
            }
        });
    }

    const saveBtn = document.getElementById('pageSaveBtn');
    if (saveBtn) {
        saveBtn.addEventListener('click', saveCurrentPage);
    }

    const exportBtn = document.getElementById('pageExportBtn');
    if (exportBtn) {
        exportBtn.addEventListener('click', exportPageData);
    }

    const importBtn = document.getElementById('pageImportBtn');
    if (importBtn) {
        importBtn.addEventListener('change', function(e) {
            if (e.target.files && e.target.files[0]) {
                importPageData(e.target.files[0]);
            }
        });
    }

    document.querySelectorAll('.dropdown-item[data-lang]').forEach(item => {
        item.addEventListener('click', function (e) {
            e.preventDefault();
            const lang = this.getAttribute('data-lang');
            setCurrentLang(lang);
            applyI18n();
        });
    });

    applyI18n();
    renderBrandLogo();
    updateLoginUI(isAdmin());
});
