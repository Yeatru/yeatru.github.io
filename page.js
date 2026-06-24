const PAGE_DATA_KEY = 'yeatruPageData';
const PAGE_DATA_VERSION_KEY = 'yeatruPageDataVersion';
const CURRENT_DATA_VERSION = 3;
const PAGE_DATA_URL = 'page-data.json';
const GITHUB_OWNER = 'Yeatru';
const GITHUB_REPO = 'yeatru.github.io';
const GITHUB_BRANCH = 'main';
const GITHUB_TOKEN_KEY = 'yeatruGithubToken';

let currentPageId = '';
let currentPageMode = 'preview';

const i18n = {
    en: {
        nav: { home: 'Home', products: 'Products', services: 'Services', sourcingProcess: 'Sourcing Process', testimonials: 'Testimonials', aboutUs: 'About Us', contactUs: 'Contact Us', login: 'Login', logout: 'Logout', servicePlans: 'Service Plans' },
        login: { title: 'Admin Login', username: 'Username', enterUsername: 'Enter username', password: 'Password', enterPassword: 'Enter password', error: 'Incorrect username or password!', cancel: 'Cancel', submit: 'Login' },
        page: { edit: 'Edit Page', save: 'Save', export: 'Export Data', import: 'Import', preview: 'Preview', syncToGithub: 'Sync to GitHub', githubToken: 'GitHub Token', tokenPlaceholder: 'Enter your GitHub personal access token', syncSuccess: 'Successfully synced to GitHub!', syncError: 'Sync failed: ', syncConfirm: 'This will update the live site data. Continue?' }
    },
    es: {
        nav: { home: 'Inicio', products: 'Productos', services: 'Servicios', sourcingProcess: 'Proceso de Suministro', testimonials: 'Testimonios', aboutUs: 'Sobre Nosotros', contactUs: 'Contáctenos', login: 'Iniciar Sesión', logout: 'Cerrar Sesión', servicePlans: 'Planes de Servicio' },
        login: { title: 'Inicio de Sesión de Administrador', username: 'Nombre de Usuario', enterUsername: 'Ingrese el nombre de usuario', password: 'Contraseña', enterPassword: 'Ingrese la contraseña', error: '¡Nombre de usuario o contraseña incorrectos!', cancel: 'Cancelar', submit: 'Iniciar Sesión' },
        page: { edit: 'Editar Página', save: 'Guardar', export: 'Exportar Datos', import: 'Importar', preview: 'Vista Previa', syncToGithub: 'Sincronizar con GitHub', githubToken: 'Token de GitHub', tokenPlaceholder: 'Ingrese su token de acceso personal de GitHub', syncSuccess: '¡Sincronizado con GitHub exitosamente!', syncError: 'Error de sincronización: ', syncConfirm: 'Esto actualizará los datos del sitio en vivo. ¿Continuar?' }
    },
    fr: {
        nav: { home: 'Accueil', products: 'Produits', services: 'Services', sourcingProcess: 'Processus d\'Approvisionnement', testimonials: 'Témoignages', aboutUs: 'À Propos de Nous', contactUs: 'Nous Contacter', login: 'Connexion', logout: 'Déconnexion', servicePlans: 'Plans de Service' },
        login: { title: 'Connexion Administrateur', username: 'Nom d\'Utilisateur', enterUsername: 'Entrez le nom d\'utilisateur', password: 'Mot de Passe', enterPassword: 'Entrez le mot de passe', error: 'Nom d\'utilisateur ou mot de passe incorrect!', cancel: 'Annuler', submit: 'Se Connecter' },
        page: { edit: 'Modifier la Page', save: 'Enregistrer', export: 'Exporter les Données', import: 'Importer', preview: 'Aperçu', syncToGithub: 'Synchroniser sur GitHub', githubToken: 'Token GitHub', tokenPlaceholder: 'Entrez votre token d\'accès personnel GitHub', syncSuccess: 'Synchronisé sur GitHub avec succès!', syncError: 'Échec de la synchronisation: ', syncConfirm: 'Cela mettra à jour les données du site en direct. Continuer?' }
    },
    ru: {
        nav: { home: 'Главная', products: 'Продукты', services: 'Услуги', sourcingProcess: 'Процесс Поставок', testimonials: 'Отзывы', aboutUs: 'О Нас', contactUs: 'Связаться', login: 'Войти', logout: 'Выйти', servicePlans: 'Тарифы' },
        login: { title: 'Вход', username: 'Логин', enterUsername: 'Введите логин', password: 'Пароль', enterPassword: 'Введите пароль', error: 'Неверные данные!', cancel: 'Отмена', submit: 'Войти' },
        page: { edit: 'Редактировать', save: 'Сохранить', export: 'Экспорт Данных', import: 'Импорт', preview: 'Просмотр', syncToGithub: 'Синхр. с GitHub', githubToken: 'GitHub Токен', tokenPlaceholder: 'Введите ваш персональный токен доступа GitHub', syncSuccess: 'Успешно синхронизировано с GitHub!', syncError: 'Ошибка синхронизации: ', syncConfirm: 'Это обновит данные живого сайта. Продолжить?' }
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
        const cachedVersion = parseInt(localStorage.getItem(PAGE_DATA_VERSION_KEY) || '0');
        if (cachedVersion < CURRENT_DATA_VERSION) {
            localStorage.removeItem(PAGE_DATA_KEY);
            const defaultData = getDefaultPageData();
            savePageData(defaultData);
            return defaultData;
        }
        const s = localStorage.getItem(PAGE_DATA_KEY);
        if (s) return JSON.parse(s);
    } catch (e) {}
    return getDefaultPageData();
}

function savePageData(data) {
    localStorage.setItem(PAGE_DATA_KEY, JSON.stringify(data));
    localStorage.setItem(PAGE_DATA_VERSION_KEY, String(CURRENT_DATA_VERSION));
}

function getGithubToken() {
    return localStorage.getItem(GITHUB_TOKEN_KEY) || '';
}

function setGithubToken(token) {
    localStorage.setItem(GITHUB_TOKEN_KEY, token);
}

async function getGithubFileSha(filePath, token) {
    const url = `https://api.github.com/repos/${GITHUB_OWNER}/${GITHUB_REPO}/contents/${filePath}?ref=${GITHUB_BRANCH}`;
    const response = await fetch(url, {
        headers: {
            'Authorization': `token ${token}`,
            'Accept': 'application/vnd.github.v3+json'
        }
    });
    if (response.status === 404) return null;
    if (!response.ok) {
        const err = await response.json().catch(() => ({}));
        throw new Error(err.message || `HTTP ${response.status}`);
    }
    const data = await response.json();
    return data.sha;
}

async function uploadToGithub(filePath, content, message, token) {
    const sha = await getGithubFileSha(filePath, token);
    const url = `https://api.github.com/repos/${GITHUB_OWNER}/${GITHUB_REPO}/contents/${filePath}`;
    const body = {
        message: message,
        content: btoa(unescape(encodeURIComponent(content))),
        branch: GITHUB_BRANCH
    };
    if (sha) body.sha = sha;

    const response = await fetch(url, {
        method: 'PUT',
        headers: {
            'Authorization': `token ${token}`,
            'Accept': 'application/vnd.github.v3+json',
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(body)
    });
    if (!response.ok) {
        const err = await response.json().catch(() => ({}));
        throw new Error(err.message || `HTTP ${response.status}`);
    }
    return await response.json();
}

async function syncPageDataToGithub() {
    const token = getGithubToken();
    if (!token) {
        const input = prompt(t('page.githubToken') + '\n' + t('page.tokenPlaceholder'));
        if (!input) return false;
        setGithubToken(input.trim());
    }
    if (!confirm(t('page.syncConfirm'))) return false;

    try {
        const data = getPageData();
        const jsonStr = JSON.stringify(data, null, 2);
        await uploadToGithub(
            PAGE_DATA_URL,
            jsonStr,
            `Update page data via admin (${new Date().toISOString().slice(0, 10)})`,
            getGithubToken()
        );
        alert(t('page.syncSuccess'));
        return true;
    } catch (err) {
        alert(t('page.syncError') + err.message);
        return false;
    }
}

function getDefaultPageData() {
    return {
        pages: {
            services: {
                title: 'Our Comprehensive Sourcing Services',
                subtitle: 'We offer end-to-end sourcing solutions tailored to your business needs',
                services: [
                    { icon: 'fa-user-check', title: 'Supplier Verification', desc: 'We thoroughly vet and verify suppliers to ensure they meet international quality standards and business ethics.', image: 'https://cdn.jsdelivr.net/gh/Yeatru/Image@main/Images/QC%20Meeting%20on%20site.png' },
                    { icon: 'fa-search', title: 'Product Sourcing', desc: 'Find the right products at competitive prices with our extensive network of reliable manufacturers and suppliers.', image: 'https://cdn.jsdelivr.net/gh/Yeatru/Image@main/Images/products%20(3).jpg' },
                    { icon: 'fa-check-square', title: 'Quality Control', desc: 'Comprehensive quality inspection at every stage of production to ensure products meet your specifications.', image: 'https://cdn.jsdelivr.net/gh/Yeatru/Image@main/Images/sample%20checking.jpg' },
                    { icon: 'fa-truck', title: 'Logistics & Shipping', desc: 'Hassle-free shipping solutions including sea, air and express delivery with competitive rates.', image: 'https://cdn.jsdelivr.net/gh/Yeatru/Image@main/Images/loading%20containers.jpg' },
                    { icon: 'fa-handshake', title: 'Price Negotiation', desc: 'Leverage our local expertise to negotiate the best prices and payment terms with suppliers.', image: 'https://cdn.jsdelivr.net/gh/Yeatru/Image@main/Images/PP%20sample%20pending%20veridation.jpg' },
                    { icon: 'fa-shield-alt', title: 'Risk Management', desc: 'Mitigate risks associated with international trade including payment security and delivery guarantees.', image: 'https://cdn.jsdelivr.net/gh/Yeatru/Image@main/Images/QC%20Meeting%20on%20site.png' }
                ],
                blocks: [
                    { type: 'heading', heading: 'Why Choose Yeatru Sourcing?' },
                    { type: 'smallImageText', image: 'https://cdn.jsdelivr.net/gh/Yeatru/Image@main/Images/products%20(3).jpg', heading: 'Extensive Product Range', text: 'With access to thousands of suppliers across China, we help you find the perfect products for your business. From consumer electronics to home goods, we cover a wide range of categories.' },
                    { type: 'smallImageText', image: 'https://cdn.jsdelivr.net/gh/Yeatru/Image@main/Images/PP%20sample%20pending%20veridation.jpg', heading: 'Strict Quality Control', text: 'Every product goes through our rigorous quality control process. We inspect at every stage - from raw materials to final packaging - ensuring you receive only the highest quality products.' }
                ]
            },
            process: {
                title: 'Our Simple Sourcing Process',
                subtitle: 'We make sourcing from China straightforward and transparent',
                steps: [
                    { number: 1, title: 'Your Requirements', desc: 'Share your product specifications, quantity, budget and timeline with our team.', image: 'https://cdn.jsdelivr.net/gh/Yeatru/Image@main/Images/products%20(3).jpg' },
                    { number: 2, title: 'Supplier Matching', desc: 'We identify and verify the best suppliers that match your specific requirements.', image: 'https://cdn.jsdelivr.net/gh/Yeatru/Image@main/Images/QC%20Meeting%20on%20site.png' },
                    { number: 3, title: 'Sample & Pricing', desc: 'Obtain samples and competitive pricing quotes from pre-vetted suppliers.', image: 'https://cdn.jsdelivr.net/gh/Yeatru/Image@main/Images/PP%20sample%20pending%20veridation.jpg' },
                    { number: 4, title: 'Delivery & Support', desc: 'We handle production oversight, quality control and shipping to your doorstep.', image: 'https://cdn.jsdelivr.net/gh/Yeatru/Image@main/Images/loading%20containers.jpg' }
                ],
                blocks: [
                    { type: 'heading', heading: 'Quality You Can Trust' },
                    { type: 'twoImages', image1: 'https://cdn.jsdelivr.net/gh/Yeatru/Image@main/Images/sample%20checking.jpg', image2: 'https://cdn.jsdelivr.net/gh/Yeatru/Image@main/Images/QC%20Meeting%20on%20site.png' },
                    { type: 'text', text: 'Our quality control team works tirelessly to ensure every product meets your exact specifications. From initial sample verification to final pre-shipment inspections, we\'ve got you covered at every step of the way.' }
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
                savePageData(data);
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

    renderPageBlocks(pageData);
    applyPageEditState();
}

function renderPageBlocks(pageData) {
    const container = document.getElementById('pageBlocks');
    if (!container) return;
    container.innerHTML = '';
    const blocks = pageData.blocks || [];
    const isEdit = currentPageMode === 'edit' && isAdmin();

    blocks.forEach((block, idx) => {
        const blockDiv = document.createElement('div');
        blockDiv.className = 'page-block';
        blockDiv.setAttribute('data-block-idx', idx);

        let html = '';
        if (block.type === 'heading') {
            html = `<div class="section-title-wrap text-center">
                <h2 class="section-title" data-block-field="heading">${escapeHtml(block.heading || '')}</h2>
                <div class="section-divider mx-auto"></div>
            </div>`;
        } else if (block.type === 'text') {
            html = `<div class="page-block-text">
                <p data-block-field="text">${escapeHtml(block.text || '')}</p>
            </div>`;
        } else if (block.type === 'image') {
            html = `<div class="page-block-image">
                <img src="${escapeHtml(block.image || '')}" alt="" onerror="this.style.display='none';">
                <input type="url" class="form-control block-image-input" placeholder="Image URL" data-block-field="image" value="${escapeHtml(block.image || '')}">
            </div>`;
        } else if (block.type === 'textImage') {
            html = `<div class="row align-items-center">
                <div class="col-lg-6">
                    <h3 data-block-field="heading" class="mb-3">${escapeHtml(block.heading || '')}</h3>
                    <p data-block-field="text">${escapeHtml(block.text || '')}</p>
                </div>
                <div class="col-lg-6">
                    <div class="page-block-image">
                        <img src="${escapeHtml(block.image || '')}" alt="" onerror="this.style.display='none';">
                        <input type="url" class="form-control block-image-input" placeholder="Image URL" data-block-field="image" value="${escapeHtml(block.image || '')}">
                    </div>
                </div>
            </div>`;
        } else if (block.type === 'imageText') {
            html = `<div class="row align-items-center">
                <div class="col-lg-6">
                    <div class="page-block-image">
                        <img src="${escapeHtml(block.image || '')}" alt="" onerror="this.style.display='none';">
                        <input type="url" class="form-control block-image-input" placeholder="Image URL" data-block-field="image" value="${escapeHtml(block.image || '')}">
                    </div>
                </div>
                <div class="col-lg-6">
                    <h3 data-block-field="heading" class="mb-3">${escapeHtml(block.heading || '')}</h3>
                    <p data-block-field="text">${escapeHtml(block.text || '')}</p>
                </div>
            </div>`;
        } else if (block.type === 'smallImageText') {
            html = `<div class="row align-items-center">
                <div class="col-md-2 col-4">
                    <div class="page-block-image small-image">
                        <img src="${escapeHtml(block.image || '')}" alt="" onerror="this.style.display='none';">
                        <input type="url" class="form-control block-image-input" placeholder="Image URL" data-block-field="image" value="${escapeHtml(block.image || '')}">
                    </div>
                </div>
                <div class="col-md-10 col-8">
                    <h3 data-block-field="heading" class="mb-3">${escapeHtml(block.heading || '')}</h3>
                    <p data-block-field="text">${escapeHtml(block.text || '')}</p>
                </div>
            </div>`;
        } else if (block.type === 'smallTextImage') {
            html = `<div class="row align-items-center">
                <div class="col-md-10 col-8">
                    <h3 data-block-field="heading" class="mb-3">${escapeHtml(block.heading || '')}</h3>
                    <p data-block-field="text">${escapeHtml(block.text || '')}</p>
                </div>
                <div class="col-md-2 col-4">
                    <div class="page-block-image small-image">
                        <img src="${escapeHtml(block.image || '')}" alt="" onerror="this.style.display='none';">
                        <input type="url" class="form-control block-image-input" placeholder="Image URL" data-block-field="image" value="${escapeHtml(block.image || '')}">
                    </div>
                </div>
            </div>`;
        } else if (block.type === 'twoImages') {
            html = `<div class="aplus-multi-images aplus-two-images">
                <div class="aplus-multi-image-item">
                    <img src="${escapeHtml(block.image1 || '')}" alt="" onerror="this.src='https://picsum.photos/600/400'">
                    <input type="url" class="form-control block-image-input" placeholder="Image 1 URL" data-block-field="image1" value="${escapeHtml(block.image1 || '')}">
                </div>
                <div class="aplus-multi-image-item">
                    <img src="${escapeHtml(block.image2 || '')}" alt="" onerror="this.src='https://picsum.photos/600/400'">
                    <input type="url" class="form-control block-image-input" placeholder="Image 2 URL" data-block-field="image2" value="${escapeHtml(block.image2 || '')}">
                </div>
            </div>`;
        } else if (block.type === 'threeImages') {
            html = `<div class="aplus-multi-images aplus-three-images">
                <div class="aplus-multi-image-item">
                    <img src="${escapeHtml(block.image1 || '')}" alt="" onerror="this.src='https://picsum.photos/400/300'">
                    <input type="url" class="form-control block-image-input" placeholder="Image 1 URL" data-block-field="image1" value="${escapeHtml(block.image1 || '')}">
                </div>
                <div class="aplus-multi-image-item">
                    <img src="${escapeHtml(block.image2 || '')}" alt="" onerror="this.src='https://picsum.photos/400/300'">
                    <input type="url" class="form-control block-image-input" placeholder="Image 2 URL" data-block-field="image2" value="${escapeHtml(block.image2 || '')}">
                </div>
                <div class="aplus-multi-image-item">
                    <img src="${escapeHtml(block.image3 || '')}" alt="" onerror="this.src='https://picsum.photos/400/300'">
                    <input type="url" class="form-control block-image-input" placeholder="Image 3 URL" data-block-field="image3" value="${escapeHtml(block.image3 || '')}">
                </div>
            </div>`;
        }

        if (isEdit) {
            html = `<div style="position:relative; border: 1px dashed #dee2e6; border-radius: 8px; padding: 1rem; margin-bottom: 1rem;">
                <div class="block-toolbar" style="position:absolute;top:-12px;right:10px;display:flex;gap:4px;z-index:10;">
                    <button class="btn btn-sm btn-outline-secondary move-block-up" data-idx="${idx}" title="Move Up"><i class="fas fa-chevron-up"></i></button>
                    <button class="btn btn-sm btn-outline-secondary move-block-down" data-idx="${idx}" title="Move Down"><i class="fas fa-chevron-down"></i></button>
                    <button class="btn btn-sm btn-danger delete-block-btn" data-idx="${idx}" title="Delete"><i class="fas fa-trash"></i></button>
                    <span class="badge bg-secondary" style="align-self:center;">${block.type}</span>
                </div>
                ${html}
            </div>`;
        }

        blockDiv.innerHTML = html;
        container.appendChild(blockDiv);
    });
}

function addPageBlock(type) {
    const data = getPageData();
    const pageData = data.pages[currentPageId];
    if (!pageData) return;
    if (!pageData.blocks) pageData.blocks = [];

    const newBlock = { type: type };
    if (type === 'heading') newBlock.heading = 'New Heading';
    if (type === 'text') newBlock.text = 'Enter your text here...';
    if (type === 'image') newBlock.image = '';
    if (type === 'textImage' || type === 'imageText' || type === 'smallImageText' || type === 'smallTextImage') {
        newBlock.heading = 'Heading';
        newBlock.text = 'Enter your text here...';
        newBlock.image = '';
    }
    if (type === 'twoImages') {
        newBlock.image1 = '';
        newBlock.image2 = '';
    }
    if (type === 'threeImages') {
        newBlock.image1 = '';
        newBlock.image2 = '';
        newBlock.image3 = '';
    }

    pageData.blocks.push(newBlock);
    savePageData(data);
    renderPage(currentPageId);
}

function deletePageBlock(idx) {
    const data = getPageData();
    const pageData = data.pages[currentPageId];
    if (!pageData || !pageData.blocks) return;
    if (!confirm('Delete this block?')) return;
    pageData.blocks.splice(idx, 1);
    savePageData(data);
    renderPage(currentPageId);
}

function movePageBlock(idx, direction) {
    const data = getPageData();
    const pageData = data.pages[currentPageId];
    if (!pageData || !pageData.blocks) return;
    const blocks = pageData.blocks;
    const newIdx = direction === 'up' ? idx - 1 : idx + 1;
    if (newIdx < 0 || newIdx >= blocks.length) return;
    [blocks[idx], blocks[newIdx]] = [blocks[newIdx], blocks[idx]];
    savePageData(data);
    renderPage(currentPageId);
}

function getServicePageUrl(title) {
    const t = (title || '').toLowerCase().trim();
    const urlMap = {
        'supplier verification': 'supplier-verification.html',
        'product sourcing': 'product-sourcing.html',
        'quality control': 'quality-control.html',
        'logistics & warehousing': 'logistics-shipping.html',
        'logistics & shipping': 'logistics-shipping.html',
        'logistics and shipping': 'logistics-shipping.html',
        'price negotiation': 'price-negotiation.html',
        'design & photography': 'design-photography.html'
    };
    return urlMap[t] || '';
}

function renderServicesPage(data) {
    const container = document.getElementById('servicesGrid');
    if (!container) return;
    container.innerHTML = '';
    const isEdit = currentPageMode === 'edit' && isAdmin();
    (data.services || []).forEach((svc, idx) => {
        const col = document.createElement('div');
        col.className = 'col-lg-4 col-md-6';
        const serviceUrl = getServicePageUrl(svc.title);
        const isLinked = !isEdit && serviceUrl;
        const imgHtml = svc.image ? `
            <div class="service-card-image">
                <img src="${escapeHtml(svc.image)}" alt="${escapeHtml(svc.title)}" onerror="this.style.display='none';this.parentElement.querySelector('.no-image-placeholder')?.style.removeProperty('display');">
                <div class="no-image-placeholder" style="display:none;height:180px;background:#f8f9fa;display:none;align-items:center;justify-content:center;color:#adb5bd;border-radius:8px;">
                    <i class="fas fa-image me-2"></i> No Image
                </div>
                <input type="url" class="form-control service-image-input" placeholder="Image URL" data-idx="${idx}" value="${escapeHtml(svc.image || '')}">
            </div>
        ` : `
            <div class="service-card-image">
                <div class="no-image-placeholder" style="height:180px;background:#f8f9fa;display:flex;align-items:center;justify-content:center;color:#adb5bd;border-radius:8px;">
                    <i class="fas fa-image me-2"></i> No Image
                </div>
                <input type="url" class="form-control service-image-input" placeholder="Image URL" data-idx="${idx}" value="${escapeHtml(svc.image || '')}">
            </div>
        `;
        const deleteBtn = isEdit ? `
            <button class="btn btn-sm btn-danger delete-service-btn" data-idx="${idx}" style="position:absolute;top:10px;right:10px;z-index:10;">
                <i class="fas fa-trash"></i>
            </button>
        ` : '';
        const cardTag = isLinked ? 'a' : 'div';
        const cardHref = isLinked ? `href="${serviceUrl}"` : '';
        const cardStyle = isLinked ? 'position:relative;display:block;text-decoration:none;color:inherit;' : 'position:relative;';
        col.innerHTML = `
            <${cardTag} class="service-card" style="${cardStyle}" ${cardHref}>
                ${deleteBtn}
                ${imgHtml}
                <h3 class="service-title" data-editable="service-title" data-idx="${idx}">${escapeHtml(svc.title || '')}</h3>
                <p class="service-desc" data-editable="service-desc" data-idx="${idx}">${escapeHtml(svc.desc || '')}</p>
            </${cardTag}>
        `;
        container.appendChild(col);
    });

    if (isEdit) {
        const addCol = document.createElement('div');
        addCol.className = 'col-lg-4 col-md-6';
        addCol.innerHTML = `
            <div class="service-card add-service-card" id="addServiceBtn" style="cursor:pointer;border:2px dashed #dee2e6;display:flex;align-items:center;justify-content:center;min-height:280px;color:#adb5bd;flex-direction:column;gap:0.5rem;">
                <i class="fas fa-plus-circle" style="font-size:2rem;"></i>
                <span>Add Service</span>
            </div>
        `;
        container.appendChild(addCol);
    }
}

function addServiceItem() {
    const data = getPageData();
    if (!data.pages.services) return;
    data.pages.services.services.push({
        icon: 'fa-star',
        title: 'New Service',
        desc: 'Service description goes here.',
        image: ''
    });
    savePageData(data);
    renderPage('services');
}

function renderProcessPage(data) {
    const container = document.getElementById('processTimeline');
    if (!container) return;
    container.innerHTML = '';
    const isEdit = currentPageMode === 'edit' && isAdmin();
    (data.steps || []).forEach((step, idx) => {
        const div = document.createElement('div');
        div.className = 'process-step-alt';
        div.style.position = 'relative';
        const imgHtml = step.image ? `
            <div class="process-step-image">
                <img src="${escapeHtml(step.image)}" alt="Step ${step.number}" onerror="this.style.display='none';">
                <input type="url" class="form-control process-image-input" placeholder="Image URL" data-idx="${idx}" value="${escapeHtml(step.image || '')}">
            </div>
        ` : (isEdit ? `
            <div class="process-step-image">
                <div style="height:180px;background:#f8f9fa;display:flex;align-items:center;justify-content:center;color:#adb5bd;border-radius:8px;">
                    <i class="fas fa-image me-2"></i> No Image
                </div>
                <input type="url" class="form-control process-image-input" placeholder="Image URL" data-idx="${idx}" value="${escapeHtml(step.image || '')}">
            </div>
        ` : '');
        const deleteBtn = isEdit ? `
            <button class="btn btn-sm btn-danger delete-step-btn" data-idx="${idx}" style="position:absolute;top:10px;right:10px;z-index:10;">
                <i class="fas fa-trash"></i>
            </button>
        ` : '';
        div.innerHTML = `
            ${deleteBtn}
            ${imgHtml}
            <div class="process-number">${step.number || idx + 1}</div>
            <h3 class="process-title" data-editable="step-title" data-idx="${idx}">${escapeHtml(step.title || '')}</h3>
            <p class="process-desc" data-editable="step-desc" data-idx="${idx}">${escapeHtml(step.desc || '')}</p>
        `;
        container.appendChild(div);
    });

    if (isEdit) {
        const addDiv = document.createElement('div');
        addDiv.className = 'process-step-alt';
        addDiv.id = 'addStepBtn';
        addDiv.style.cursor = 'pointer';
        addDiv.style.border = '2px dashed #dee2e6';
        addDiv.style.display = 'flex';
        addDiv.style.alignItems = 'center';
        addDiv.style.justifyContent = 'center';
        addDiv.style.flexDirection = 'column';
        addDiv.style.color = '#adb5bd';
        addDiv.style.gap = '0.5rem';
        addDiv.innerHTML = `
            <i class="fas fa-plus-circle" style="font-size:2rem;"></i>
            <span>Add Step</span>
        `;
        container.appendChild(addDiv);
    }
}

function addProcessStep() {
    const data = getPageData();
    if (!data.pages.process) return;
    const steps = data.pages.process.steps || [];
    steps.push({
        number: steps.length + 1,
        title: 'New Step',
        desc: 'Step description goes here.',
        image: ''
    });
    data.pages.process.steps = steps;
    savePageData(data);
    renderPage('process');
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
    document.querySelectorAll('[data-block-field]').forEach(el => {
        if (el.tagName !== 'INPUT') {
            el.contentEditable = isEdit ? 'true' : 'false';
        }
    });
    document.body.classList.toggle('edit-mode', isEdit);

    const pageTitle = document.getElementById('pageTitle');
    const pageSubtitle = document.getElementById('pageSubtitle');
    if (pageTitle) pageTitle.contentEditable = isEdit ? 'true' : 'false';
    if (pageSubtitle) pageSubtitle.contentEditable = isEdit ? 'true' : 'false';

    const editBtn = document.getElementById('pageEditBtn');
    const saveBtn = document.getElementById('pageSaveBtn');
    const exportBtn = document.getElementById('pageExportBtn');
    const syncBtn = document.getElementById('pageSyncBtn');
    const addBlockToolbar = document.getElementById('addBlockToolbar');
    const importLabel = document.querySelector('label[for="pageImportBtn"], label:has(#pageImportBtn)');
    if (editBtn) editBtn.style.display = isAdmin() ? 'inline-block' : 'none';
    if (saveBtn) saveBtn.style.display = (isAdmin() && isEdit) ? 'inline-block' : 'none';
    if (exportBtn) exportBtn.style.display = (isAdmin() && isEdit) ? 'inline-block' : 'none';
    if (syncBtn) syncBtn.style.display = (isAdmin() && isEdit) ? 'inline-block' : 'none';
    if (addBlockToolbar) addBlockToolbar.style.display = (isAdmin() && isEdit) ? 'block' : 'none';
    if (importLabel) importLabel.style.display = (isAdmin() && isEdit) ? 'inline-block' : 'none';

    if (isEdit) {
        bindEditModeEvents();
    }
}

function bindEditModeEvents() {
    const addServiceBtn = document.getElementById('addServiceBtn');
    if (addServiceBtn) {
        addServiceBtn.onclick = function() { addServiceItem(); };
    }

    document.querySelectorAll('.delete-service-btn').forEach(btn => {
        btn.onclick = function(e) {
            e.stopPropagation();
            const idx = parseInt(this.getAttribute('data-idx'));
            if (confirm('Delete this service?')) {
                const data = getPageData();
                if (data.pages.services && data.pages.services.services) {
                    data.pages.services.services.splice(idx, 1);
                    savePageData(data);
                    renderPage('services');
                }
            }
        };
    });

    const addStepBtn = document.getElementById('addStepBtn');
    if (addStepBtn) {
        addStepBtn.onclick = function() { addProcessStep(); };
    }

    document.querySelectorAll('.delete-step-btn').forEach(btn => {
        btn.onclick = function(e) {
            e.stopPropagation();
            const idx = parseInt(this.getAttribute('data-idx'));
            if (confirm('Delete this step?')) {
                const data = getPageData();
                if (data.pages.process && data.pages.process.steps) {
                    data.pages.process.steps.splice(idx, 1);
                    data.pages.process.steps.forEach((s, i) => { s.number = i + 1; });
                    savePageData(data);
                    renderPage('process');
                }
            }
        };
    });

    document.querySelectorAll('.service-image-input, .process-image-input').forEach(input => {
        input.addEventListener('input', function() {
            const idx = this.getAttribute('data-idx');
            const img = this.parentElement.querySelector('img');
            if (img) {
                img.src = this.value;
                img.style.display = this.value ? 'block' : 'none';
            }
        });
    });

    document.querySelectorAll('.block-image-input').forEach(input => {
        input.addEventListener('input', function() {
            const img = this.parentElement.querySelector('img');
            if (img) {
                img.src = this.value;
                img.style.display = this.value ? 'block' : 'none';
                img.onerror = function() { this.style.display = 'none'; };
            }
        });
    });

    document.querySelectorAll('.delete-block-btn').forEach(btn => {
        btn.onclick = function(e) {
            e.stopPropagation();
            const idx = parseInt(this.getAttribute('data-idx'));
            deletePageBlock(idx);
        };
    });

    document.querySelectorAll('.move-block-up').forEach(btn => {
        btn.onclick = function(e) {
            e.stopPropagation();
            const idx = parseInt(this.getAttribute('data-idx'));
            movePageBlock(idx, 'up');
        };
    });

    document.querySelectorAll('.move-block-down').forEach(btn => {
        btn.onclick = function(e) {
            e.stopPropagation();
            const idx = parseInt(this.getAttribute('data-idx'));
            movePageBlock(idx, 'down');
        };
    });

    document.querySelectorAll('.add-block-btn').forEach(btn => {
        btn.onclick = function(e) {
            e.stopPropagation();
            const type = this.getAttribute('data-type');
            addPageBlock(type);
        };
    });
}

function setPageMode(mode) {
    currentPageMode = mode;
    applyPageEditState();
}

function saveCurrentPage() {
    const data = getPageData();
    const pageData = data.pages[currentPageId];
    if (!pageData) return;

    const pageTitle = document.getElementById('pageTitle')?.textContent?.trim();
    const pageSubtitle = document.getElementById('pageSubtitle')?.textContent?.trim();
    if (pageTitle) pageData.title = pageTitle;
    if (pageSubtitle) pageData.subtitle = pageSubtitle;

    if (currentPageId === 'services') {
        pageData.services = [];
        const serviceCards = document.querySelectorAll('.service-card:not(.add-service-card)');
        serviceCards.forEach((card, idx) => {
            const title = card.querySelector('[data-editable="service-title"]')?.textContent || '';
            const desc = card.querySelector('[data-editable="service-desc"]')?.textContent || '';
            const icon = card.querySelector('.service-icon i')?.className?.replace('fas ', '') || 'fa-check';
            const image = card.querySelector('.service-image-input')?.value || '';
            pageData.services.push({ icon, title, desc, image });
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
        const stepCards = document.querySelectorAll('.process-step-alt:not(#addStepBtn)');
        stepCards.forEach((step, idx) => {
            const number = step.querySelector('.process-number')?.textContent || (idx + 1);
            const title = step.querySelector('[data-editable="step-title"]')?.textContent || '';
            const desc = step.querySelector('[data-editable="step-desc"]')?.textContent || '';
            const image = step.querySelector('.process-image-input')?.value || '';
            pageData.steps.push({ number, title, desc, image });
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

    const blocksContainer = document.getElementById('pageBlocks');
    if (blocksContainer) {
        const blocks = [];
        blocksContainer.querySelectorAll('.page-block').forEach((blockDiv, idx) => {
            const blockData = {};
            const blockEl = blockDiv.querySelector('[data-block-field]')?.closest('.page-block > div') || blockDiv.firstElementChild;
            const typeBadge = blockDiv.querySelector('.block-toolbar .badge');
            let type = typeBadge ? typeBadge.textContent.trim() : null;
            
            if (!type) {
                if (blockDiv.querySelector('[data-block-field="heading"]') && blockDiv.querySelector('h2.section-title')) type = 'heading';
                else if (blockDiv.querySelector('[data-block-field="text"]') && !blockDiv.querySelector('[data-block-field="heading"]') && !blockDiv.querySelector('.aplus-multi-images')) type = 'text';
                else if (blockDiv.querySelector('[data-block-field="image"]') && !blockDiv.querySelector('[data-block-field="heading"]')) type = 'image';
                else if (blockDiv.querySelector('.aplus-three-images')) type = 'threeImages';
                else if (blockDiv.querySelector('.aplus-two-images')) type = 'twoImages';
                else if (blockDiv.querySelector('[data-block-field="image"]') && blockDiv.querySelector('[data-block-field="heading"]')) {
                    const firstCol = blockDiv.querySelector('.row > div:first-child');
                    if (firstCol && firstCol.querySelector('.page-block-image')) type = 'imageText';
                    else type = 'textImage';
                }
            }
            if (!type) return;

            blockData.type = type;
            blockDiv.querySelectorAll('[data-block-field]').forEach(fieldEl => {
                const field = fieldEl.getAttribute('data-block-field');
                if (fieldEl.tagName === 'INPUT') {
                    blockData[field] = fieldEl.value || '';
                } else {
                    blockData[field] = fieldEl.textContent || '';
                }
            });
            blocks.push(blockData);
        });
        pageData.blocks = blocks;
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

    const syncBtn = document.getElementById('pageSyncBtn');
    if (syncBtn) {
        syncBtn.addEventListener('click', function() {
            saveCurrentPage();
            setTimeout(syncPageDataToGithub, 100);
        });
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
