const DEFAULT_CATEGORIES = ["Electronics", "Home & Garden", "Kitchenware", "Toys", "Apparel"];
const REMOTE_DATA_URL = "./site-data.json";
const DEFAULT_PRODUCTS = [
    { id: 1, image: "https://cdn.jsdelivr.net/gh/Yeatru/Image@main/Images/YSCL001A.jpg", category: "Apparel", name: "Quick Dry Activewear Set", sku: "YS-CL-001A", material: "Polyester", size: "L/XL/XXL/XXXL/XXXXL", moq: 100, priceMin: 6.49, priceMax: 6.99, description: "Men's 2-piece quick-dry athletic set with short-sleeve tee and 2-in-1 double-layer running shorts. Moisture-wicking lightweight fabric rapidly dissipates sweat for cool, breathable comfort during gym, jogging, swimming and training. Built-in compression liner avoids chafing, elastic drawstring waist secures fit. Minimalist branded black design. Sizes L–XXXXL fit men weighing 42.5–90.5kg, flexible stretch material enables full unrestricted sports movement.,【L】42.5–52.5kgs,【XL】52.5–62.5kgs,【XXL】62.5–72.5kgs,【XXXL】72.5–82.5kgs,【XXXXL】82.5–90.5kgs" },
    { id: 2, image: "https://cdn.jsdelivr.net/gh/Yeatru/Image@main/Images/YSCL002WS.jpg", category: "Apparel", name: "Islamic/Muslim Women Swimsuit", sku: "YS-CL-002WS", material: "Polyester", size: "S/M/L/XL", moq: 200, priceMin: 7.69, priceMax: 7.99, description: "Women's 2-piece modest long sleeve swimsuit with tropical floral printed sleeves, available in black and navy blue. UPF 50+ quick-dry fabric blocks UV rays, ideal for surfing, diving, beach volleyball and Muslim modest swimwear. Soft elastic material ensures unrestricted movement, combining sun protection, coverage and stylish tropical print for all water activities." },
    { id: 3, image: "https://picsum.photos/id/292/600/400", category: "Kitchenware", name: "Stainless Steel Kitchen Knife", sku: "YS-K001", material: "High Carbon Stainless Steel", size: "8 inch blade", moq: 150, priceMin: 19.99, priceMax: 29.99, description: "Professional kitchen knife made of high carbon stainless steel, sharp and durable." },
    { id: 4, image: "https://picsum.photos/id/160/600/400", category: "Toys", name: "Wooden Building Blocks", sku: "YS-T001", material: "Natural Wood", size: "Various sizes", moq: 300, priceMin: 14.99, priceMax: 24.99, description: "Eco-friendly wooden building blocks set for kids, safe and educational." }
];

const translationResources = {
    en: { translation: {
        nav: { home: "Home", products: "Products", services: "Services", sourcingProcess: "Sourcing Process", testimonials: "Testimonials", aboutUs: "About Us", contactUs: "Contact Us", login: "Login", logout: "Logout" },
        hero: { title: "Professional China Sourcing Agent Yiwu & Global Supply Chain", desc: "One-stop sourcing solution from China: product sourcing, supplier audit, quality control, logistics shipping. Help global buyers source from China easily.", contactBtn: "Contact Us Now", productsBtn: "View Products" },
        products: { title: "Hot Products", subtitle: "Explore our featured products sourced from China", categoryManagement: "Category Management", enterCategory: "Enter new category name", addCategory: "Add Category", addProduct: "Add New Product", imageUrl: "Image URL", enterImageUrl: "Enter product image URL", category: "Category", selectCategory: "Select Category", name: "Product Name", enterName: "Enter product name", sku: "SKU", enterSKU: "Enter product SKU", material: "Material", enterMaterial: "Enter material", size: "Size", enterSize: "Enter size", moq: "MOQ", enterMOQ: "Enter MOQ", priceMin: "Minimum Price ($)", enterMinPrice: "Enter minimum price", priceMax: "Maximum Price ($)", enterMaxPrice: "Enter maximum price", description: "Description", enterDescription: "Enter product description", cancel: "Cancel", save: "Save Product", edit: "Edit", delete: "Delete", quote: "Get a Quote", price: "Price: $", viewDetails: "View Details" },
        filter: { title: "Filter by Category", all: "All", reset: "Reset Filter", showing: "Showing", of: "of", products: "products", noResult: "No products in this category" },
        services: { title: "Our Comprehensive Sourcing Services", subtitle: "We offer end-to-end sourcing solutions tailored to your business needs", supplierVerification: "Supplier Verification", supplierVerificationDesc: "We thoroughly vet and verify suppliers to ensure they meet international quality standards and business ethics.", productSourcing: "Product Sourcing", productSourcingDesc: "Find the right products at competitive prices with our extensive network of reliable manufacturers and suppliers.", qualityControl: "Quality Control", qualityControlDesc: "Comprehensive quality inspection at every stage of production to ensure products meet your specifications.", logistics: "Logistics & Shipping", logisticsDesc: "Hassle-free shipping solutions including sea, air and express delivery with competitive rates.", priceNegotiation: "Price Negotiation", priceNegotiationDesc: "Leverage our local expertise to negotiate the best prices and payment terms with suppliers.", riskManagement: "Risk Management", riskManagementDesc: "Mitigate risks associated with international trade including payment security and delivery guarantees." },
        process: { title: "Our Simple Sourcing Process", subtitle: "We make sourcing from China straightforward and transparent", step1: "Your Requirements", step1Desc: "Share your product specifications, quantity, budget and timeline with our team.", step2: "Supplier Matching", step2Desc: "We identify and verify the best suppliers that match your specific requirements.", step3: "Sample & Pricing", step3Desc: "Obtain samples and competitive pricing quotes from pre-vetted suppliers.", step4: "Delivery & Support", step4Desc: "We handle production oversight, quality control and shipping to your doorstep." },
        testimonials: { title: "What Clients Say", subtitle: "Feedback from our global buyers", review1: "\"Yeatru Sourcing helped me source 5000+ storage boxes from Yiwu, great quality and fast shipping. Highly recommended!\"", review2: "\"Professional team, strict quality control, and excellent after-sales service. Best China sourcing partner I ever worked with.\"", review3: "\"The price negotiation service saved me over 20% on my order. The logistics team ensured on-time delivery to the US. Very satisfied!\"" },
        about: { title: "About Yeatru Sourcing", profile: "Company Profile", profileDesc: "Yeatru Sourcing is a professional one-stop sourcing agent located in Yiwu City, the world's largest small commodity distribution center. We specialize in providing global clients with reliable procurement services, supplier development, strict quality inspection, supplier management and integrated logistics solutions." },
        contact: { getInTouch: "Get In Touch With Us", desc: "Ready to start your sourcing journey? Fill out the form or contact us directly using the information below.", requestQuote: "Request a Free Quote", yourName: "Your Name", enterName: "Enter your name", email: "Email Address", enterEmail: "Enter your email", phone: "Phone Number", product: "Product You Need (e.g. Plastic storage boxes)", message: "Please describe your requirements in detail", enterMessage: "Enter your message", sendRequest: "Send Request" },
        footer: { desc: "Professional China sourcing agent helping businesses worldwide find reliable suppliers and quality products at competitive prices.", quickLinks: "Quick Links", services: "Our Services", contact: "Contact Us" },
        login: { title: "Admin Login", username: "Username", enterUsername: "Enter username", password: "Password", enterPassword: "Enter password", error: "Incorrect username or password!", cancel: "Cancel", submit: "Login" },
        quote: { title: "Get a Quote", quantity: "Required Quantity", enterQuantity: "Enter quantity", cancel: "Cancel", send: "Send Quote Request" },
        detail: { back: "Back to Products", edit: "Edit", preview: "Preview", saving: "Saving...", saved: "Saved", error: "Save failed" },
        aplus: { title: "A+ Content", addBlock: "Add a content block:", blockHero: "Hero Banner", blockText: "Text", blockTextImage: "Text + Image", blockImageText: "Image + Text", blockFeatures: "Feature Grid", placeholderHeading: "Click to edit heading", placeholderText: "Click to edit text content...", placeholderFeature: "Feature point", confirmDelete: "Delete this block?" },
        logo: { title: "Update Brand Logo", tip: "Logo is displayed in a 50x50 pixel container. Upload a square image (PNG/JPG/SVG) or paste an image URL for best results.", uploadFile: "Upload Image", imageUrl: "Or Image URL", reset: "Reset to Default", cancel: "Cancel", save: "Save Logo" }
    }},
    es: { translation: {
        nav: { home: "Inicio", products: "Productos", services: "Servicios", sourcingProcess: "Proceso de Suministro", testimonials: "Testimonios", aboutUs: "Sobre Nosotros", contactUs: "Contáctenos", login: "Iniciar Sesión", logout: "Cerrar Sesión" },
        hero: { title: "Agente Profesional de Suministro en China Yiwu & Cadena de Suministro Global", desc: "Solución integral de suministro desde China: búsqueda de productos, auditoría de proveedores, control de calidad, envío logístico. Ayudamos a compradores globales a abastecerse de China fácilmente.", contactBtn: "Contáctenos Ahora", productsBtn: "Ver Productos" },
        products: { title: "Productos Populares", subtitle: "Explora nuestros productos destacados suministrados desde China", categoryManagement: "Gestión de Categorías", enterCategory: "Ingrese el nombre de la nueva categoría", addCategory: "Agregar Categoría", addProduct: "Agregar Nuevo Producto", imageUrl: "URL de la Imagen", enterImageUrl: "Ingrese la URL de la imagen del producto", category: "Categoría", selectCategory: "Seleccionar Categoría", name: "Nombre del Producto", enterName: "Ingrese el nombre del producto", sku: "SKU", enterSKU: "Ingrese el SKU del producto", material: "Material", enterMaterial: "Ingrese el material", size: "Tamaño", enterSize: "Ingrese el tamaño", moq: "MOQ", enterMOQ: "Ingrese la MOQ", priceMin: "Precio Mínimo ($)", enterMinPrice: "Ingrese el precio mínimo", priceMax: "Precio Máximo ($)", enterMaxPrice: "Ingrese el precio máximo", description: "Descripción", enterDescription: "Ingrese la descripción del producto", cancel: "Cancelar", save: "Guardar Producto", edit: "Editar", delete: "Eliminar", quote: "Solicitar Presupuesto", price: "Precio: $", viewDetails: "Ver Detalles" },
        filter: { title: "Filtrar por Categoría", all: "Todos", reset: "Restablecer Filtro", showing: "Mostrando", of: "de", products: "productos", noResult: "No hay productos en esta categoría" },
        services: { title: "Nuestros Servicios Integrales de Suministro", subtitle: "Ofrecemos soluciones de suministro de extremo a extremo adaptadas a las necesidades de su negocio", supplierVerification: "Verificación de Proveedores", supplierVerificationDesc: "Revisamos y verificamos a fondo a los proveedores para garantizar que cumplen con los estándares de calidad internacionales y la ética empresarial.", productSourcing: "Búsqueda de Productos", productSourcingDesc: "Encuentra los productos adecuados a precios competitivos con nuestra extensa red de fabricantes y proveedores confiables.", qualityControl: "Control de Calidad", qualityControlDesc: "Inspección de calidad integral en cada etapa de la producción para garantizar que los productos cumplen con sus especificaciones.", logistics: "Logística y Envío", logisticsDesc: "Soluciones de envío sin complicaciones que incluyen envío marítimo, aéreo y exprés con tarifas competitivas.", priceNegotiation: "Negociación de Precios", priceNegotiationDesc: "Aproveche nuestra experiencia local para negociar los mejores precios y condiciones de pago con los proveedores.", riskManagement: "Gestión de Riesgos", riskManagementDesc: "Mitigar los riesgos asociados con el comercio internacional, incluida la seguridad de pagos y garantías de entrega." },
        process: { title: "Nuestro Simple Proceso de Suministro", subtitle: "Hacemos que el aprovisionamiento desde China sea sencillo y transparente", step1: "Sus Requisitos", step1Desc: "Comuníquese con nuestro equipo sobre las especificaciones del producto, cantidad, presupuesto y cronograma.", step2: "Coincidencia de Proveedores", step2Desc: "Identificamos y verificamos a los mejores proveedores que se adaptan a sus requisitos específicos.", step3: "Muestras y Precios", step3Desc: "Obtenga muestras y cotizaciones de precios competitivos de proveedores previamente verificados.", step4: "Entrega y Soporte", step4Desc: "Nos encargamos de la supervisión de la producción, el control de calidad y el envío hasta su puerta." },
        testimonials: { title: "Lo Que Dicen Nuestros Clientes", subtitle: "Comentarios de nuestros compradores globales", review1: "\"Yeatru Sourcing me ayudó a suministrar más de 5000 cajas de almacenamiento desde Yiwu, excelente calidad y envío rápido. ¡Muy recomendado!\"", review2: "\"Equipo profesional, control de calidad estricto y excelente servicio postventa. El mejor socio de suministro chino con el que he trabajado.\"", review3: "\"El servicio de negociación de precios me ahorró más del 20% en mi pedido. El equipo logístico garantizó la entrega a tiempo a EE. UU. ¡Muy satisfecho!\"" },
        about: { title: "Sobre Yeatru Sourcing", profile: "Perfil de la Empresa", profileDesc: "Yeatru Sourcing es un agente profesional de suministro integral ubicado en la ciudad de Yiwu, el mayor centro de distribución de pequeñas mercancías del mundo. Nos especializamos en brindar a clientes globales servicios de adquisición confiables, desarrollo de proveedores, inspección de calidad estricta, gestión de proveedores y soluciones logísticas integradas." },
        contact: { getInTouch: "Póngase en Contacto Con Nosotros", desc: "¿Listo para comenzar su viaje de suministro? Complete el formulario o contáctenos directamente con la información a continuación.", requestQuote: "Solicitar un Presupuesto Gratuito", yourName: "Su Nombre", enterName: "Ingrese su nombre", email: "Dirección de Correo Electrónico", enterEmail: "Ingrese su correo electrónico", phone: "Número de Teléfono", product: "Producto que Necesita", message: "Describa sus requisitos en detalle", enterMessage: "Ingrese su mensaje", sendRequest: "Enviar Solicitud" },
        footer: { desc: "Agente profesional de suministro chino que ayuda a empresas de todo el mundo a encontrar proveedores confiables y productos de calidad a precios competitivos.", quickLinks: "Enlaces Rápidos", services: "Nuestros Servicios", contact: "Contáctenos" },
        login: { title: "Inicio de Sesión de Administrador", username: "Nombre de Usuario", enterUsername: "Ingrese el nombre de usuario", password: "Contraseña", enterPassword: "Ingrese la contraseña", error: "¡Nombre de usuario o contraseña incorrectos!", cancel: "Cancelar", submit: "Iniciar Sesión" },
        quote: { title: "Solicitar Presupuesto", quantity: "Cantidad Requerida", enterQuantity: "Ingrese la cantidad", cancel: "Cancelar", send: "Enviar Solicitud de Presupuesto" },
        detail: { back: "Volver a Productos", edit: "Editar", preview: "Vista previa", saving: "Guardando...", saved: "Guardado", error: "Error al guardar" },
        aplus: { title: "Contenido A+", addBlock: "Agregar un bloque de contenido:", blockHero: "Banner Principal", blockText: "Texto", blockTextImage: "Texto + Imagen", blockImageText: "Imagen + Texto", blockFeatures: "Cuadrícula de Características", placeholderHeading: "Haz clic para editar título", placeholderText: "Haz clic para editar contenido...", placeholderFeature: "Punto destacado", confirmDelete: "¿Eliminar este bloque?" },
        logo: { title: "Actualizar Logotipo", tip: "El logotipo se muestra en un contenedor de 50x50 píxeles. Cargue una imagen cuadrada o pegue una URL.", uploadFile: "Cargar Imagen", imageUrl: "O URL de Imagen", reset: "Restablecer", cancel: "Cancelar", save: "Guardar Logotipo" }
    }},
    fr: { translation: {
        nav: { home: "Accueil", products: "Produits", services: "Services", sourcingProcess: "Processus d'Approvisionnement", testimonials: "Témoignages", aboutUs: "À Propos de Nous", contactUs: "Nous Contacter", login: "Connexion", logout: "Déconnexion" },
        hero: { title: "Agent Professionnel d'Approvisionnement en Chine Yiwu & Chaîne d'Approvisionnement Mondiale", desc: "Solution d'approvisionnement tout-en-un depuis la Chine: recherche de produits, audit de fournisseurs, contrôle de qualité, expédition logistique. Aidons les acheteurs mondiaux à s'approvisionner facilement depuis la Chine.", contactBtn: "Nous Contacter Maintenant", productsBtn: "Voir les Produits" },
        products: { title: "Produits Populaires", subtitle: "Découvrez nos produits phares approvisionnés depuis la Chine", categoryManagement: "Gestion des Catégories", enterCategory: "Entrez le nom de la nouvelle catégorie", addCategory: "Ajouter une Catégorie", addProduct: "Ajouter un Nouveau Produit", imageUrl: "URL de l'Image", enterImageUrl: "Entrez l'URL de l'image du produit", category: "Catégorie", selectCategory: "Sélectionner une Catégorie", name: "Nom du Produit", enterName: "Entrez le nom du produit", sku: "SKU", enterSKU: "Entrez le SKU du produit", material: "Matériau", enterMaterial: "Entrez le matériau", size: "Taille", enterSize: "Entrez la taille", moq: "MOQ", enterMOQ: "Entrez la MOQ", priceMin: "Prix Minimum ($)", enterMinPrice: "Entrez le prix minimum", priceMax: "Prix Maximum ($)", enterMaxPrice: "Entrez le prix maximum", description: "Description", enterDescription: "Entrez la description du produit", cancel: "Annuler", save: "Enregistrer", edit: "Modifier", delete: "Supprimer", quote: "Demander un Devis", price: "Prix: $", viewDetails: "Voir les Détails" },
        filter: { title: "Filtrer par Catégorie", all: "Tous", reset: "Réinitialiser le Filtre", showing: "Affichage de", of: "sur", products: "produits", noResult: "Aucun produit dans cette catégorie" },
        services: { title: "Nos Services Complets d'Approvisionnement", subtitle: "Nous offrons des solutions d'approvisionnement de bout en bout adaptées aux besoins de votre entreprise", supplierVerification: "Vérification des Fournisseurs", supplierVerificationDesc: "Nous examinons et vérifions en profondeur les fournisseurs pour garantir qu'ils respectent les normes de qualité internationales et l'éthique professionnelle.", productSourcing: "Recherche de Produits", productSourcingDesc: "Trouvez les bons produits à des prix compétitifs grâce à notre vaste réseau de fabricants et fournisseurs fiables.", qualityControl: "Contrôle de Qualité", qualityControlDesc: "Inspection de qualité complète à chaque étape de la production pour garantir que les produits répondent à vos spécifications.", logistics: "Logistique et Expédition", logisticsDesc: "Solutions d'expédition sans tracas incluant la livraison maritime, aérienne et express à des tarifs compétitifs.", priceNegotiation: "Négociation de Prix", priceNegotiationDesc: "Profitez de notre expertise locale pour négocier les meilleurs prix et conditions de paiement avec les fournisseurs.", riskManagement: "Gestion des Risques", riskManagementDesc: "Atténuer les risques liés au commerce international, y compris la sécurité des paiements et les garanties de livraison." },
        process: { title: "Notre Simple Processus d'Approvisionnement", subtitle: "Nous rendons l'approvisionnement depuis la Chine simple et transparent", step1: "Vos Exigences", step1Desc: "Partagez vos spécifications de produit, quantité, budget et calendrier avec notre équipe.", step2: "Appariement des Fournisseurs", step2Desc: "Nous identifions et vérifions les meilleurs fournisseurs correspondant à vos exigences spécifiques.", step3: "Échantillons et Prix", step3Desc: "Obtenez des échantillons et des devis de prix compétitifs de fournisseurs pré-vérifiés.", step4: "Livraison et Support", step4Desc: "Nous nous occupons de la supervision de la production, du contrôle de qualité et de l'expédition jusqu'à votre porte." },
        testimonials: { title: "Ce Que Disent Nos Clients", subtitle: "Avis de nos acheteurs mondiaux", review1: "\"Yeatru Sourcing m'a aidé à approvisionner plus de 5000 boîtes de rangement depuis Yiwu, excellente qualité et expédition rapide. Très recommandé!\"", review2: "\"Équipe professionnelle, contrôle de qualité strict et excellent service après-vente. Le meilleur partenaire d'approvisionnement chinois avec lequel j'ai travaillé.\"", review3: "\"Le service de négociation de prix m'a fait économiser plus de 20% sur ma commande. L'équipe logistique a assuré la livraison à temps aux États-Unis. Très satisfait!\"" },
        about: { title: "À Propos de Yeatru Sourcing", profile: "Profil de l'Entreprise", profileDesc: "Yeatru Sourcing est un agent d'approvisionnement tout-en-un professionnel situé dans la ville de Yiwu, le plus grand centre de distribution de petits articles au monde. Nous nous spécialisons dans la fourniture de services d'approvisionnement fiables, de développement de fournisseurs, d'inspection de qualité stricte, de gestion de fournisseurs et de solutions logistiques intégrées aux clients du monde entier." },
        contact: { getInTouch: "Prenez Contact Avec Nous", desc: "Prêt à commencer votre voyage d'approvisionnement? Remplissez le formulaire ou contactez-nous directement.", requestQuote: "Demander un Devis Gratuit", yourName: "Votre Nom", enterName: "Entrez votre nom", email: "Adresse E-mail", enterEmail: "Entrez votre e-mail", phone: "Numéro de Téléphone", product: "Produit dont vous avez besoin", message: "Décrivez vos exigences en détail", enterMessage: "Entrez votre message", sendRequest: "Envoyer la Demande" },
        footer: { desc: "Agent professionnel d'approvisionnement chinois aidant les entreprises du monde entier à trouver des fournisseurs fiables et des produits de qualité à des prix compétitifs.", quickLinks: "Liens Rapides", services: "Nos Services", contact: "Nous Contacter" },
        login: { title: "Connexion Administrateur", username: "Nom d'Utilisateur", enterUsername: "Entrez le nom d'utilisateur", password: "Mot de Passe", enterPassword: "Entrez le mot de passe", error: "Nom d'utilisateur ou mot de passe incorrect!", cancel: "Annuler", submit: "Se Connecter" },
        quote: { title: "Demander un Devis", quantity: "Quantité Requise", enterQuantity: "Entrez la quantité", cancel: "Annuler", send: "Envoyer la Demande de Devis" },
        detail: { back: "Retour aux Produits", edit: "Modifier", preview: "Aperçu", saving: "Enregistrement...", saved: "Enregistré", error: "Échec d'enregistrement" },
        aplus: { title: "Contenu A+", addBlock: "Ajouter un bloc :", blockHero: "Bannière", blockText: "Texte", blockTextImage: "Texte + Image", blockImageText: "Image + Texte", blockFeatures: "Grille de fonctionnalités", placeholderHeading: "Cliquez pour modifier le titre", placeholderText: "Cliquez pour modifier...", placeholderFeature: "Caractéristique", confirmDelete: "Supprimer ce bloc?" },
        logo: { title: "Mettre à jour le logo", tip: "Le logo s'affiche dans un conteneur 50x50. Téléchargez une image carrée ou collez une URL.", uploadFile: "Télécharger", imageUrl: "Ou URL d'image", reset: "Réinitialiser", cancel: "Annuler", save: "Enregistrer" }
    }},
    ru: { translation: {
        nav: { home: "Главная", products: "Продукты", services: "Услуги", sourcingProcess: "Процесс Поставок", testimonials: "Отзывы", aboutUs: "О Нас", contactUs: "Связаться", login: "Войти", logout: "Выйти" },
        hero: { title: "Профессиональный Агент По Поставкам Из Китая Ивю", desc: "Комплексное решение по поставкам из Китая.", contactBtn: "Связаться Сейчас", productsBtn: "Посмотреть Продукты" },
        products: { title: "Популярные Продукты", subtitle: "Изучите наши рекомендуемые продукты из Китая", categoryManagement: "Управление Категориями", enterCategory: "Введите название", addCategory: "Добавить", addProduct: "Добавить Продукт", imageUrl: "URL Изображения", enterImageUrl: "Введите URL", category: "Категория", selectCategory: "Выберите", name: "Название", enterName: "Введите название", sku: "Артикул", enterSKU: "Введите артикул", material: "Материал", enterMaterial: "Введите материал", size: "Размер", enterSize: "Введите размер", moq: "MOQ", enterMOQ: "Введите MOQ", priceMin: "Мин. Цена ($)", enterMinPrice: "Введите мин. цену", priceMax: "Макс. Цена ($)", enterMaxPrice: "Введите макс. цену", description: "Описание", enterDescription: "Введите описание", cancel: "Отмена", save: "Сохранить", edit: "Редактировать", delete: "Удалить", quote: "Получить Котировку", price: "Цена: $", viewDetails: "Подробнее" },
        filter: { title: "Фильтр по Категории", all: "Все", reset: "Сбросить", showing: "Показано", of: "из", products: "продуктов", noResult: "Нет продуктов в этой категории" },
        services: { title: "Наши Услуги По Поставкам", subtitle: "Комплексные решения по поставкам", supplierVerification: "Проверка Поставщиков", supplierVerificationDesc: "Тщательная проверка поставщиков.", productSourcing: "Поиск Продуктов", productSourcingDesc: "Найдите нужные продукты.", qualityControl: "Контроль Качества", qualityControlDesc: "Контроль качества на каждом этапе.", logistics: "Логистика и Доставка", logisticsDesc: "Беспроблемная доставка.", priceNegotiation: "Переговоры По Ценам", priceNegotiationDesc: "Лучшие цены.", riskManagement: "Управление Рисками", riskManagementDesc: "Снижение рисков." },
        process: { title: "Наш Процесс Поставок", subtitle: "Простой и прозрачный процесс", step1: "Ваши Требования", step1Desc: "Поделитесь спецификациями.", step2: "Подбор Поставщиков", step2Desc: "Подбираем лучших поставщиков.", step3: "Образцы и Цены", step3Desc: "Образцы и цены.", step4: "Доставка и Поддержка", step4Desc: "Контроль производства и доставка." },
        testimonials: { title: "Отзывы Клиентов", subtitle: "Отзывы наших покупателей", review1: "\"Отличное качество и быстрая доставка!\"", review2: "\"Профессиональная команда.\"", review3: "\"Сэкономил 20%!\"" },
        about: { title: "О Yeatru Sourcing", profile: "Профиль Компании", profileDesc: "Yeatru Sourcing — профессиональный агент по поставкам в Ивю." },
        contact: { getInTouch: "Свяжитесь С Нами", desc: "Готовы начать?", requestQuote: "Запросить Котировку", yourName: "Ваше Имя", enterName: "Введите имя", email: "Email", enterEmail: "Введите email", phone: "Телефон", product: "Нужный продукт", message: "Опишите требования", enterMessage: "Введите сообщение", sendRequest: "Отправить" },
        footer: { desc: "Профессиональный агент по поставкам из Китая.", quickLinks: "Ссылки", services: "Услуги", contact: "Контакты" },
        login: { title: "Вход", username: "Логин", enterUsername: "Введите логин", password: "Пароль", enterPassword: "Введите пароль", error: "Неверные данные!", cancel: "Отмена", submit: "Войти" },
        quote: { title: "Котировка", quantity: "Количество", enterQuantity: "Введите кол-во", cancel: "Отмена", send: "Отправить" },
        detail: { back: "Назад", edit: "Редактировать", preview: "Просмотр", saving: "Сохранение...", saved: "Сохранено", error: "Ошибка" },
        aplus: { title: "Контент A+", addBlock: "Добавить блок:", blockHero: "Баннер", blockText: "Текст", blockTextImage: "Текст + Изображение", blockImageText: "Изображение + Текст", blockFeatures: "Сетка функций", placeholderHeading: "Заголовок", placeholderText: "Текст...", placeholderFeature: "Особенность", confirmDelete: "Удалить блок?" },
        logo: { title: "Обновить логотип", tip: "50x50.", uploadFile: "Загрузить", imageUrl: "URL", reset: "Сброс", cancel: "Отмена", save: "Сохранить" }
    }}
};

let currentFilterCategory = 'all';
let currentDetailMode = 'preview';
let saveTimer = null;
let currentDetailProductId = null;

function isAdmin() {
    return localStorage.getItem('yeatruAdminLoggedIn') === 'true';
}

function escapeHtml(str) {
    if (str === null || str === undefined) return '';
    return String(str).replace(/[&<>"']/g, function (s) {
        return ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[s]);
    });
}

function tt(key, fallback) {
    try {
        const v = i18next.t(key);
        if (v && v !== key) return v;
    } catch (e) {}
    return fallback || key;
}

document.addEventListener('DOMContentLoaded', function () {
    i18next
        .use(i18nextBrowserLanguageDetector)
        .init({
            fallbackLng: 'en',
            resources: translationResources,
            detection: {
                order: ['querystring', 'cookie', 'localStorage', 'navigator', 'htmlTag'],
                caches: ['localStorage', 'cookie']
            },
            interpolation: { escapeValue: false }
        }).then(function () {
            updateContent();
            bindLanguageEvents();
            loadRemoteSiteData();
            renderCategoryFilter();
            renderProducts();
        });

    window.addEventListener('beforeunload', function () {
        localStorage.removeItem('yeatruAdminLoggedIn');
    });

    updateLoginUI(isAdmin());
    renderCategories();
    renderProducts();
    renderBrandLogo();

    document.getElementById('submitLogin').addEventListener('click', function () {
        const username = document.getElementById('adminUsername').value.trim();
        const password = document.getElementById('adminPassword').value.trim();
        const errorEl = document.getElementById('loginError');
        if (username === 'Yeatru' && password === 'Ldz52385109') {
            localStorage.setItem('yeatruAdminLoggedIn', 'true');
            updateLoginUI(true);
            const loginModal = document.getElementById('loginModal');
            const modalInstance = bootstrap.Modal.getInstance(loginModal) || new bootstrap.Modal(loginModal);
            modalInstance.hide();
            errorEl.classList.add('d-none');
            document.getElementById('adminUsername').value = '';
            document.getElementById('adminPassword').value = '';
        } else {
            errorEl.classList.remove('d-none');
        }
    });

    document.getElementById('logoutBtn').addEventListener('click', function () {
        localStorage.removeItem('yeatruAdminLoggedIn');
        updateLoginUI(false);
        if (document.getElementById('productDetailPage').classList.contains('active') && currentDetailMode === 'edit') {
            setDetailMode('preview');
        }
    });

    document.getElementById('addCategoryBtn').addEventListener('click', function () {
        const newCategory = document.getElementById('newCategory').value.trim();
        if (newCategory && !getCategories().includes(newCategory)) {
            saveCategories([...getCategories(), newCategory]);
            document.getElementById('newCategory').value = '';
        }
    });

    document.getElementById('addVariationBtn').addEventListener('click', function () {
        addVariationItem();
    });

    document.getElementById('saveProduct').addEventListener('click', function () {
        const productId = document.getElementById('productId').value;
        const product = {
            id: productId ? parseInt(productId) : Date.now(),
            image: document.getElementById('productImage').value,
            category: document.getElementById('productCategory').value,
            name: document.getElementById('productName').value,
            sku: document.getElementById('productSKU').value,
            material: document.getElementById('productMaterial').value,
            size: document.getElementById('productSize').value,
            moq: parseInt(document.getElementById('productMOQ').value),
            priceMin: parseFloat(document.getElementById('productPriceMin').value),
            priceMax: parseFloat(document.getElementById('productPriceMax').value),
            description: document.getElementById('productDescription').value,
            variations: collectVariations()
        };
        const products = getProducts();
        if (productId) {
            const index = products.findIndex(p => p.id === parseInt(productId));
            if (index >= 0) {
                product.aplus = products[index].aplus || null;
                products[index] = product;
            }
        } else {
            products.push(product);
        }
        saveProducts(products);
        const productModal = document.getElementById('productModal');
        bootstrap.Modal.getInstance(productModal).hide();
        document.getElementById('productForm').reset();
        document.getElementById('variationsContainer').innerHTML = '';
        document.getElementById('productId').value = '';
        document.getElementById('productModalLabel').textContent = tt('products.addProduct', 'Add New Product');
    });

    document.getElementById('addProductBtn').addEventListener('click', function () {
        document.getElementById('productForm').reset();
        document.getElementById('productId').value = '';
        document.getElementById('variationsContainer').innerHTML = '';
        document.getElementById('productModalLabel').textContent = tt('products.addProduct', 'Add New Product');
    });

    document.getElementById('exportDataBtn').addEventListener('click', exportSiteData);
    document.getElementById('importDataBtn').addEventListener('click', function () {
        document.getElementById('importDataFile').click();
    });
    document.getElementById('importDataFile').addEventListener('change', importSiteDataFromFile);

    document.getElementById('detailBackBtn').addEventListener('click', function () {
        hideDetailPage();
    });

    document.querySelectorAll('#detailModeToggle button').forEach(b => {
        b.addEventListener('click', function () {
            setDetailMode(this.getAttribute('data-mode'));
        });
    });

    document.getElementById('detailQuoteBtn').addEventListener('click', function () {
        if (!currentDetailProductId) return;
        const p = getProducts().find(x => x.id === currentDetailProductId);
        if (!p) return;
        document.getElementById('quoteProductName').value = p.name;
        new bootstrap.Modal(document.getElementById('quoteModal')).show();
    });

    document.querySelectorAll('#aplusAddBar button').forEach(btn => {
        btn.addEventListener('click', function () {
            addAplusBlock(this.getAttribute('data-add-type'));
        });
    });

    ['detailNameInput', 'detailImageInput', 'detailMaterialInput', 'detailSizeInput', 'detailMOQInput', 'detailPriceMinInput', 'detailPriceMaxInput', 'detailDescInput'].forEach(id => {
        const el = document.getElementById(id);
        if (el) el.addEventListener('input', scheduleAutoSave);
    });

    document.getElementById('brandLogoEdit').addEventListener('click', function (e) {
        e.preventDefault();
        e.stopPropagation();
        if (!isAdmin()) return;
        document.getElementById('logoUrlInput').value = localStorage.getItem('yeatruBrandLogo') || '';
        new bootstrap.Modal(document.getElementById('logoModal')).show();
    });
    document.getElementById('logoSaveBtn').addEventListener('click', saveLogoFromModal);
    document.getElementById('logoResetBtn').addEventListener('click', function () {
        localStorage.removeItem('yeatruBrandLogo');
        renderBrandLogo();
        bootstrap.Modal.getInstance(document.getElementById('logoModal')).hide();
    });

    window.addEventListener('hashchange', handleHashRoute);
    handleHashRoute();
});

function updateContent() {
    document.querySelectorAll('[data-i18n]').forEach(el => {
        const key = el.getAttribute('data-i18n');
        const v = i18next.t(key);
        if (v && v !== key) el.textContent = v;
    });
    document.querySelectorAll('[data-i18n-placeholder]').forEach(el => {
        const key = el.getAttribute('data-i18n-placeholder');
        const v = i18next.t(key);
        if (v && v !== key) el.placeholder = v;
    });
    const langNames = { en: 'English', es: 'Español', fr: 'Français', ru: 'Русский' };
    const cur = document.getElementById('current-lang');
    if (cur) cur.textContent = langNames[i18next.language] || 'English';

    renderCategoryFilter();
    renderProducts();
    if (document.getElementById('productDetailPage').classList.contains('active') && currentDetailProductId) {
        renderDetailPage(currentDetailProductId);
    }
}

function bindLanguageEvents() {
    document.querySelectorAll('.dropdown-item[data-lang]').forEach(item => {
        item.addEventListener('click', function (e) {
            e.preventDefault();
            const lang = this.getAttribute('data-lang');
            i18next.changeLanguage(lang).then(updateContent);
        });
    });
}

function updateLoginUI(loggedIn) {
    const loginBtn = document.getElementById('loginBtn');
    const logoutBtn = document.getElementById('logoutBtn');
    const addProductBtn = document.getElementById('addProductBtn');
    const adminDataTools = document.getElementById('adminDataTools');
    const categoryManagement = document.getElementById('categoryManagement');
    const brandLogoEdit = document.getElementById('brandLogoEdit');
    if (loggedIn) {
        loginBtn.classList.add('d-none');
        logoutBtn.classList.remove('d-none');
        addProductBtn.classList.remove('d-none');
        adminDataTools.classList.remove('d-none');
        adminDataTools.classList.add('d-flex');
        categoryManagement.style.display = 'block';
        brandLogoEdit.classList.add('admin-visible');
    } else {
        loginBtn.classList.remove('d-none');
        logoutBtn.classList.add('d-none');
        addProductBtn.classList.add('d-none');
        adminDataTools.classList.add('d-none');
        adminDataTools.classList.remove('d-flex');
        categoryManagement.style.display = 'none';
        brandLogoEdit.classList.remove('admin-visible');
    }
    renderCategories();
    renderProducts();
    if (!loggedIn && currentDetailMode === 'edit') setDetailMode('preview');
    const toggle = document.getElementById('detailModeToggle');
    if (toggle) toggle.style.display = loggedIn ? 'inline-flex' : 'none';
}

function getCategories() {
    try {
        const s = localStorage.getItem('yeatruCategories');
        return s ? JSON.parse(s) : DEFAULT_CATEGORIES.slice();
    } catch (e) { return DEFAULT_CATEGORIES.slice(); }
}

function saveCategories(categories) {
    localStorage.setItem('yeatruCategories', JSON.stringify(categories));
    renderCategories();
    renderCategoryFilter();
}

function renderCategories() {
    const categories = getCategories();
    const categoryList = document.getElementById('categoryList');
    const productCategorySelect = document.getElementById('productCategory');
    if (!categoryList || !productCategorySelect) return;
    categoryList.innerHTML = '';
    categories.forEach(category => {
        const badge = document.createElement('div');
        badge.className = 'badge bg-primary d-flex align-items-center gap-2';
        badge.innerHTML = `${escapeHtml(category)}${isAdmin() ? '<button class="btn-close btn-close-white btn-sm delete-category" data-category="' + escapeHtml(category) + '"></button>' : ''}`;
        categoryList.appendChild(badge);
    });
    productCategorySelect.innerHTML = `<option value="">${tt('products.selectCategory', 'Select Category')}</option>`;
    categories.forEach(category => {
        const option = document.createElement('option');
        option.value = category;
        option.textContent = category;
        productCategorySelect.appendChild(option);
    });
    document.querySelectorAll('.delete-category').forEach(btn => {
        btn.addEventListener('click', function () {
            const category = this.getAttribute('data-category');
            saveCategories(getCategories().filter(c => c !== category));
            saveProducts(getProducts().filter(p => p.category !== category));
        });
    });
}

function renderCategoryFilter() {
    const list = document.getElementById('categoryFilterList');
    if (!list) return;
    const categories = getCategories();
    if (currentFilterCategory !== 'all' && !categories.includes(currentFilterCategory)) {
        currentFilterCategory = 'all';
    }
    list.innerHTML = '';
    const allBtn = document.createElement('button');
    allBtn.type = 'button';
    allBtn.className = 'category-filter-btn' + (currentFilterCategory === 'all' ? ' active' : '');
    allBtn.textContent = tt('filter.all', 'All');
    allBtn.addEventListener('click', function () {
        currentFilterCategory = 'all';
        renderCategoryFilter();
        renderProducts();
    });
    list.appendChild(allBtn);
    categories.forEach(cat => {
        const btn = document.createElement('button');
        btn.type = 'button';
        btn.className = 'category-filter-btn' + (currentFilterCategory === cat ? ' active' : '');
        btn.textContent = cat;
        btn.addEventListener('click', function () {
            currentFilterCategory = cat;
            renderCategoryFilter();
            renderProducts();
        });
        list.appendChild(btn);
    });
    const resetBtn = document.createElement('button');
    resetBtn.type = 'button';
    resetBtn.className = 'category-filter-reset';
    resetBtn.innerHTML = '<i class="fas fa-rotate-left me-1"></i>' + tt('filter.reset', 'Reset Filter');
    resetBtn.addEventListener('click', function () {
        currentFilterCategory = 'all';
        renderCategoryFilter();
        renderProducts();
    });
    list.appendChild(resetBtn);
}

function getProducts() {
    try {
        const s = localStorage.getItem('yeatruProducts');
        return s ? JSON.parse(s) : DEFAULT_PRODUCTS.slice();
    } catch (e) { return DEFAULT_PRODUCTS.slice(); }
}

function saveProducts(products) {
    localStorage.setItem('yeatruProducts', JSON.stringify(products));
    renderProducts();
}

function buildSiteDataObject() {
    return {
        version: 1,
        updatedAt: new Date().toISOString(),
        logo: localStorage.getItem('yeatruBrandLogo') || '',
        categories: getCategories(),
        products: getProducts()
    };
}

function applySiteData(data, options = {}) {
    if (!data || typeof data !== 'object') return false;

    if (Array.isArray(data.categories)) {
        localStorage.setItem('yeatruCategories', JSON.stringify(data.categories));
    }
    if (Array.isArray(data.products)) {
        localStorage.setItem('yeatruProducts', JSON.stringify(data.products));
    }
    if (Object.prototype.hasOwnProperty.call(data, 'logo')) {
        if (data.logo) {
            localStorage.setItem('yeatruBrandLogo', data.logo);
        } else {
            localStorage.removeItem('yeatruBrandLogo');
        }
    }

    renderBrandLogo();
    renderCategories();
    renderCategoryFilter();
    renderProducts();

    if (currentDetailProductId) {
        const exists = getProducts().some(p => p.id === currentDetailProductId);
        if (exists) renderDetailPage(currentDetailProductId);
        else hideDetailPage();
    }

    if (!options.silent) {
        alert('site-data.json 已导入，当前浏览器已更新。请记得把 JSON 文件上传到 GitHub，游客才能看到。');
    }
    return true;
}

async function loadRemoteSiteData() {
    try {
        const response = await fetch(REMOTE_DATA_URL + '?t=' + Date.now(), { cache: 'no-store' });
        if (!response.ok) throw new Error('site-data.json not found');
        const data = await response.json();
        applySiteData(data, { silent: true });
        console.info('已从 site-data.json 读取公开数据');
    } catch (error) {
        console.info('未读取到 site-data.json，使用本地缓存或默认数据。', error);
    }
}

function exportSiteData() {
    if (!isAdmin()) return;
    const data = buildSiteDataObject();
    const json = JSON.stringify(data, null, 2);
    const blob = new Blob([json], { type: 'application/json;charset=utf-8' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'site-data.json';
    document.body.appendChild(a);
    a.click();
    a.remove();
    URL.revokeObjectURL(url);
    alert('已导出 site-data.json。把这个文件上传并覆盖 GitHub 仓库同目录的 site-data.json，游客刷新网页后即可看到更新。');
}

function importSiteDataFromFile(event) {
    if (!isAdmin()) return;
    const file = event.target.files && event.target.files[0];
    if (!file) return;
    const reader = new FileReader();
    reader.onload = function (e) {
        try {
            const data = JSON.parse(e.target.result);
            applySiteData(data);
        } catch (error) {
            alert('导入失败：请选择格式正确的 site-data.json 文件。');
        } finally {
            event.target.value = '';
        }
    };
    reader.readAsText(file, 'utf-8');
}

function renderProducts() {
    const products = getProducts();
    const productList = document.getElementById('productList');
    const filterInfo = document.getElementById('filterResultInfo');
    if (!productList) return;

    const filtered = currentFilterCategory === 'all'
        ? products
        : products.filter(p => p.category === currentFilterCategory);

    if (filterInfo) {
        if (currentFilterCategory === 'all') {
            filterInfo.textContent = `${tt('filter.showing', 'Showing')} ${filtered.length} ${tt('filter.products', 'products')}`;
        } else {
            filterInfo.textContent = `${tt('filter.showing', 'Showing')} ${filtered.length} ${tt('filter.of', 'of')} ${products.length} ${tt('filter.products', 'products')} (${currentFilterCategory})`;
        }
    }

    productList.innerHTML = '';

    if (filtered.length === 0) {
        productList.innerHTML = `<div class="col-12 text-center py-5"><h5>${tt('filter.noResult', 'No products in this category')}</h5></div>`;
        return;
    }

    filtered.forEach(product => {
        const priceText = (tt('products.price', 'Price: $')) + product.priceMin + ' - ' + product.priceMax;
        const card = document.createElement('div');
        card.className = 'col-lg-3 col-md-6';
        card.innerHTML = `
            <div class="product-card">
                <img src="${escapeHtml(product.image)}" class="card-img-top product-img-clickable" alt="${escapeHtml(product.name)}" data-id="${product.id}" style="cursor:pointer;" onerror="this.src='https://picsum.photos/600/400'; this.alt='${escapeHtml(product.name)}'">
                <div class="card-body">
                    <div class="product-category">${escapeHtml(product.category)}</div>
                    <h5 class="product-title product-title-clickable" data-id="${product.id}" style="cursor:pointer;">${escapeHtml(product.name)}</h5>
                    <p class="product-desc">${escapeHtml(product.description)}</p>
                    <p class="product-price">${escapeHtml(priceText)}</p>
                    <div class="d-flex flex-wrap gap-2 align-items-center">
                        <a href="#product/${product.id}" class="product-action-btn view-detail-link" data-id="${product.id}"><i class="fas fa-circle-info me-1"></i>${tt('products.viewDetails', 'View Details')}</a>
                        <span class="text-muted">|</span>
                        <a href="#" class="product-action-btn quote-product" data-product="${escapeHtml(product.name)}"><i class="fas fa-file-invoice-dollar me-1"></i>${tt('products.quote', 'Get a Quote')}</a>
                    </div>
                    ${isAdmin() ? `
                        <div class="product-admin-actions">
                            <button class="btn btn-sm btn-primary product-admin-btn edit-product" data-id="${product.id}"><i class="fas fa-edit me-1"></i>${tt('products.edit', 'Edit')}</button>
                            <button class="btn btn-sm btn-danger product-admin-btn delete-product" data-id="${product.id}"><i class="fas fa-trash me-1"></i>${tt('products.delete', 'Delete')}</button>
                        </div>
                    ` : ''}
                </div>
            </div>
        `;
        productList.appendChild(card);
    });

    document.querySelectorAll('.edit-product').forEach(btn => {
        btn.addEventListener('click', function () {
            const productId = parseInt(this.getAttribute('data-id'));
            const product = getProducts().find(p => p.id === productId);
            if (product) {
                document.getElementById('productId').value = product.id;
                document.getElementById('productImage').value = product.image;
                document.getElementById('productCategory').value = product.category;
                document.getElementById('productName').value = product.name;
                document.getElementById('productSKU').value = product.sku;
                document.getElementById('productMaterial').value = product.material;
                document.getElementById('productSize').value = product.size;
                document.getElementById('productMOQ').value = product.moq;
                document.getElementById('productPriceMin').value = product.priceMin;
                document.getElementById('productPriceMax').value = product.priceMax;
                document.getElementById('productDescription').value = product.description;
                renderVariationsModal(product.variations || []);
                document.getElementById('productModalLabel').textContent = (tt('products.edit', 'Edit')) + ' ' + product.name;
                new bootstrap.Modal(document.getElementById('productModal')).show();
            }
        });
    });

    document.querySelectorAll('.delete-product').forEach(btn => {
        btn.addEventListener('click', function () {
            const productId = parseInt(this.getAttribute('data-id'));
            if (confirm((tt('products.delete', 'Delete')) + ' this product?')) {
                saveProducts(getProducts().filter(p => p.id !== productId));
            }
        });
    });

    document.querySelectorAll('.quote-product').forEach(btn => {
        btn.addEventListener('click', function (e) {
            e.preventDefault();
            e.stopPropagation();
            const productName = this.getAttribute('data-product');
            document.getElementById('quoteProductName').value = productName;
            new bootstrap.Modal(document.getElementById('quoteModal')).show();
        });
    });

    document.querySelectorAll('.product-img-clickable, .product-title-clickable, .view-detail-link').forEach(el => {
        el.addEventListener('click', function (e) {
            e.preventDefault();
            const id = parseInt(this.getAttribute('data-id'));
            if (!id) return;
            location.hash = '#product/' + id;
        });
    });
}

function handleHashRoute() {
    const hash = location.hash || '';
    const m = hash.match(/^#product\/(\d+)/);
    if (m) {
        const id = parseInt(m[1]);
        showDetailPage(id);
    } else {
        hideDetailPage();
    }
}

function renderVariationsModal(variations) {
    const container = document.getElementById('variationsContainer');
    if (!container) return;
    container.innerHTML = '';
    if (variations && variations.length > 0) {
        variations.forEach(v => addVariationItem(v));
    }
}
function addVariationItem(data) {
    const container = document.getElementById('variationsContainer');
    if (!container) return;
    const v = data || { color: '', size: '', image: '' };
    const item = document.createElement('div');
    item.className = 'variation-item';
    item.innerHTML = `
        <input type="text" class="form-control variation-color" placeholder="Color (e.g. Red)" value="${escapeHtml(v.color || '')}">
        <input type="text" class="form-control variation-size" placeholder="Size (e.g. L)" value="${escapeHtml(v.size || '')}">
        <input type="url" class="form-control variation-image" placeholder="Image URL (optional)" value="${escapeHtml(v.image || '')}">
        <button type="button" class="variation-remove"><i class="fas fa-trash"></i></button>
    `;
    item.querySelector('.variation-remove').addEventListener('click', function () { item.remove(); });
    container.appendChild(item);
}
function collectVariations() {
    const variations = [];
    document.querySelectorAll('#variationsContainer .variation-item').forEach(item => {
        const color = item.querySelector('.variation-color').value.trim();
        const size = item.querySelector('.variation-size').value.trim();
        const image = item.querySelector('.variation-image').value.trim();
        if (color || size) variations.push({ color, size, image });
    });
    return variations;
}
function getColorValue(colorName) {
    const colorMap = {
        'Black': '#1a1a1a', 'White': '#f5f5f5', 'Gray': '#808080', 'Blue': '#0b7b94',
        'Red': '#dc3545', 'Pink': '#e83e8c', 'Green': '#28a745', 'Yellow': '#ffc107',
        'Orange': '#fd7e14', 'Purple': '#6f42c1', 'Brown': '#8b4513', 'Light Blue': '#87ceeb',
        'Navy': '#001f3f', 'Cream': '#fffdd0', 'Natural': '#d4a574', 'Beige': '#f5f5dc',
        'Teal': '#20c997', 'Gold': '#ffd700', 'Silver': '#c0c0c0', 'Charcoal': '#36454f'
    };
    return colorMap[colorName] || '#ccc';
}

function renderVariationsDisplay(variations) {
    const display = document.getElementById('variationsDisplay');
    const list = document.getElementById('variationsList');
    if (!display || !list) return;
    if (!variations || variations.length === 0) {
        display.style.display = 'none';
        return;
    }
    display.style.display = 'block';
    list.innerHTML = '';
    variations.forEach(v => {
        const card = document.createElement('div');
        card.className = 'variation-card';
        card.innerHTML = `
            <div class="variation-info">
                <span class="variation-color-dot"${v.color ? ` style="background-color: ${getColorValue(v.color)}"` : ''}></span>
                <span class="variation-name">${escapeHtml(v.color || '-')}</span>
                <span class="variation-size">${escapeHtml(v.size || '')}</span>
                ${v.price !== undefined && v.price !== null && v.price !== '' ? `<span class="variation-price">$${escapeHtml(v.price)}</span>` : ''}
            </div>
        `;
        card.addEventListener('click', function () {
            document.querySelectorAll('.variation-card').forEach(c => c.classList.remove('selected'));
            card.classList.add('selected');
            if (v.price !== null && v.price !== undefined && !isNaN(v.price)) {
                document.getElementById('detailPriceBig').textContent = '$' + v.price;
            }
        });
        
        list.appendChild(card);
    });
}

function showDetailPage(productId) {
    const product = getProducts().find(p => p.id === productId);
    if (!product) {
        hideDetailPage();
        return;
    }
    currentDetailProductId = productId;
    document.getElementById('mainContent').style.display = 'none';
    const page = document.getElementById('productDetailPage');
    page.classList.add('active');
    setDetailMode('preview');
    renderDetailPage(productId);
    window.scrollTo({ top: 0, behavior: 'smooth' });
}

function hideDetailPage() {
    currentDetailProductId = null;
    document.getElementById('mainContent').style.display = '';
    document.getElementById('productDetailPage').classList.remove('active');
    if (location.hash.startsWith('#product/')) {
        history.replaceState(null, '', '#products');
    }
}

function renderDetailPage(productId) {
    const product = getProducts().find(p => p.id === productId);
    if (!product) return;
    document.getElementById('detailImage').src = product.image || 'https://picsum.photos/600/400';
    document.getElementById('detailImage').alt = product.name || '';
    document.getElementById('detailName').textContent = product.name || '';
    document.getElementById('detailCategory').textContent = product.category || '';
    document.getElementById('detailSKU').textContent = product.sku || '';
    document.getElementById('detailMaterial').textContent = product.material || '';
    document.getElementById('detailSize').textContent = product.size || '';
    document.getElementById('detailMOQ').textContent = product.moq || '';
    document.getElementById('detailPriceMin').textContent = (product.priceMin !== undefined && product.priceMin !== null) ? product.priceMin : '';
    document.getElementById('detailPriceMax').textContent = (product.priceMax !== undefined && product.priceMax !== null) ? product.priceMax : '';
    document.getElementById('detailDesc').textContent = product.description || '';

    // 计算默认价格显示：优先使用变体价格区间，其次使用产品 priceMin-priceMax
    let defaultPriceText;
    if (product.variations && product.variations.length > 0) {
        const pricedVariations = product.variations.filter(v => v.price !== undefined && v.price !== null && v.price !== '');
        if (pricedVariations.length > 0) {
            const prices = pricedVariations.map(v => parseFloat(v.price));
            const vMin = Math.min(...prices);
            const vMax = Math.max(...prices);
            if (vMin === vMax) {
                defaultPriceText = '$' + vMin;
            } else {
                defaultPriceText = '$' + vMin + ' - $' + vMax;
            }
        } else {
            defaultPriceText = '$' + (product.priceMin || 0) + ' - $' + (product.priceMax || 0);
        }
    } else {
        defaultPriceText = '$' + (product.priceMin || 0) + ' - $' + (product.priceMax || 0);
    }
    document.getElementById('detailPriceBig').textContent = defaultPriceText;

    document.getElementById('detailNameInput').value = product.name || '';
    document.getElementById('detailImageInput').value = product.image || '';
    document.getElementById('detailMaterialInput').value = product.material || '';
    document.getElementById('detailSizeInput').value = product.size || '';
    document.getElementById('detailMOQInput').value = product.moq || '';
    document.getElementById('detailPriceMinInput').value = product.priceMin || '';
    document.getElementById('detailPriceMaxInput').value = product.priceMax || '';
    document.getElementById('detailDescInput').value = product.description || '';

    renderVariationsDisplay(product.variations);
    renderAplusBlocks(product);
}

function setDetailMode(mode) {
    if (mode === 'edit' && !isAdmin()) mode = 'preview';
    currentDetailMode = mode;
    document.querySelectorAll('#detailModeToggle button').forEach(b => {
        b.classList.toggle('active', b.getAttribute('data-mode') === mode);
    });
    const editOnly = document.querySelectorAll('.detail-edit-only');
    const previewBtnsToHide = ['detailName', 'detailImage', 'detailMaterial', 'detailSize', 'detailMOQ', 'detailPriceMin', 'detailPriceMax', 'detailDesc'];
    const isEdit = mode === 'edit';
    editOnly.forEach(el => el.style.display = isEdit ? '' : 'none');
    previewBtnsToHide.forEach(id => {
        const el = document.getElementById(id);
        if (el) el.style.display = isEdit ? 'none' : '';
    });
    const priceBig = document.getElementById('detailPriceBig');
    if (priceBig) priceBig.style.display = isEdit ? 'none' : '';

    document.querySelectorAll('.aplus-block').forEach(b => {
        b.classList.toggle('edit-mode', isEdit);
        b.querySelectorAll('[data-editable]').forEach(el => el.contentEditable = isEdit ? 'true' : 'false');
    });
    document.getElementById('aplusAddBar').classList.toggle('visible', isEdit);
    const badge = document.getElementById('saveStatusBadge');
    badge.style.display = isEdit ? 'inline-flex' : 'none';
    if (isEdit) setSaveStatus('saved');
}

function setSaveStatus(state) {
    const badge = document.getElementById('saveStatusBadge');
    const span = badge.querySelector('span');
    badge.classList.remove('saving', 'saved', 'error');
    if (state === 'saving') {
        badge.classList.add('saving');
        span.textContent = tt('detail.saving', 'Saving...');
    } else if (state === 'saved') {
        badge.classList.add('saved');
        span.textContent = tt('detail.saved', 'Saved');
    } else if (state === 'error') {
        badge.classList.add('error');
        span.textContent = tt('detail.error', 'Save failed');
    }
}

function scheduleAutoSave() {
    if (!isAdmin() || currentDetailMode !== 'edit' || !currentDetailProductId) return;
    setSaveStatus('saving');
    if (saveTimer) clearTimeout(saveTimer);
    saveTimer = setTimeout(commitSave, 400);
}

function commitSave() {
    try {
        const products = getProducts();
        const idx = products.findIndex(p => p.id === currentDetailProductId);
        if (idx < 0) return;
        const p = products[idx];
        p.name = document.getElementById('detailNameInput').value || p.name;
        p.image = document.getElementById('detailImageInput').value || p.image;
        p.material = document.getElementById('detailMaterialInput').value || p.material;
        p.size = document.getElementById('detailSizeInput').value || p.size;
        const moqV = document.getElementById('detailMOQInput').value;
        if (moqV) p.moq = parseInt(moqV);
        const minV = document.getElementById('detailPriceMinInput').value;
        if (minV) p.priceMin = parseFloat(minV);
        const maxV = document.getElementById('detailPriceMaxInput').value;
        if (maxV) p.priceMax = parseFloat(maxV);
        p.description = document.getElementById('detailDescInput').value || p.description;

        p.aplus = collectAplusBlocks();
        products[idx] = p;
        localStorage.setItem('yeatruProducts', JSON.stringify(products));
        document.getElementById('detailName').textContent = p.name;
        document.getElementById('detailImage').src = p.image;
        document.getElementById('detailMaterial').textContent = p.material;
        document.getElementById('detailSize').textContent = p.size;
        document.getElementById('detailMOQ').textContent = p.moq;
        document.getElementById('detailPriceMin').textContent = p.priceMin;
        document.getElementById('detailPriceMax').textContent = p.priceMax;
        document.getElementById('detailDesc').textContent = p.description;
        document.getElementById('detailPriceBig').textContent = '$' + (p.priceMin || 0) + ' - $' + (p.priceMax || 0);
        setSaveStatus('saved');
        renderProducts();
    } catch (e) {
        console.error(e);
        setSaveStatus('error');
    }
}

function defaultAplus() {
    return [
        { type: 'hero', heading: 'Premium Quality, Trusted Worldwide', text: 'Manufactured under strict quality controls and shipped globally with care.', image: 'https://picsum.photos/1200/420' },
        { type: 'textImage', heading: 'About This Product', text: 'Crafted from selected materials and engineered for everyday use. Carefully inspected before shipping.', image: 'https://picsum.photos/600/400' },
        { type: 'features', heading: 'Key Features', items: ['High-quality material', 'Strict QC inspection', 'Custom logo / packaging', 'Fast worldwide shipping'] }
    ];
}

function renderAplusBlocks(product) {
    const container = document.getElementById('aplusBlocks');
    if (!container) return;
    const blocks = (product && product.aplus && product.aplus.length) ? product.aplus : defaultAplus();
    container.innerHTML = '';
    blocks.forEach((b, idx) => container.appendChild(buildAplusBlockEl(b, idx)));
    applyAplusEditState();
}

function applyAplusEditState() {
    const isEdit = currentDetailMode === 'edit' && isAdmin();
    document.querySelectorAll('.aplus-block').forEach(b => {
        b.classList.toggle('edit-mode', isEdit);
        b.querySelectorAll('[data-editable]').forEach(el => el.contentEditable = isEdit ? 'true' : 'false');
    });
}

function buildAplusBlockEl(b, idx) {
    const wrap = document.createElement('div');
    wrap.className = 'aplus-block';
    wrap.dataset.type = b.type;
    wrap.dataset.idx = idx;

    const toolbar = document.createElement('div');
    toolbar.className = 'aplus-block-toolbar';
    toolbar.innerHTML = `
        <button type="button" class="move-up" title="Move Up"><i class="fas fa-arrow-up"></i></button>
        <button type="button" class="move-down" title="Move Down"><i class="fas fa-arrow-down"></i></button>
        <button type="button" class="danger delete-block" title="Delete"><i class="fas fa-trash"></i></button>
    `;
    wrap.appendChild(toolbar);

    const content = document.createElement('div');
    content.className = 'aplus-block-content';
    if (b.type === 'hero') {
        content.innerHTML = `
            <h2 class="aplus-block-heading" data-editable="heading">${escapeHtml(b.heading || '')}</h2>
            <p class="aplus-block-text" data-editable="text">${escapeHtml(b.text || '')}</p>
            <img src="${escapeHtml(b.image || '')}" alt="hero" style="width:100%;height:auto;border-radius:8px;" onerror="this.src='https://picsum.photos/1200/420'">
            <input type="url" class="form-control aplus-image-input" placeholder="Image URL" data-editable-img value="${escapeHtml(b.image || '')}">
        `;
    } else if (b.type === 'text') {
        content.innerHTML = `
            <h3 class="aplus-block-heading" data-editable="heading">${escapeHtml(b.heading || '')}</h3>
            <div class="aplus-block-text" data-editable="text">${escapeHtml(b.text || '')}</div>
        `;
    } else if (b.type === 'textImage' || b.type === 'imageText') {
        const layoutClass = b.type === 'textImage' ? 'layout-text-image' : 'layout-image-text';
        content.innerHTML = `
            <div class="aplus-block-image-wrap ${layoutClass}">
                <div class="aplus-block-text-side">
                    <h3 class="aplus-block-heading" data-editable="heading">${escapeHtml(b.heading || '')}</h3>
                    <div class="aplus-block-text" data-editable="text">${escapeHtml(b.text || '')}</div>
                </div>
                <img src="${b.image || 'https://picsum.photos/600/400'}" alt="block" onerror="this.src='https://picsum.photos/600/400'">
            </div>
            <input type="url" class="form-control aplus-image-input" placeholder="Image URL" data-editable-img value="${escapeHtml(b.image || '')}">
        `;
    } else if (b.type === 'features') {
        const items = b.items || [];
        content.innerHTML = `
            <h3 class="aplus-block-heading" data-editable="heading">${escapeHtml(b.heading || 'Key Features')}</h3>
            <div class="aplus-block-features">
                <ul data-editable="features">
                    ${items.map(it => '<li data-editable="feature">' + escapeHtml(it) + '</li>').join('')}
                </ul>
            </div>
        `;
    } else if (b.type === 'twoColumns') {
        content.innerHTML = `
            <div class="aplus-block-two-columns">
                <div class="aplus-block-column">${b.column1 || ''}</div>
                <div class="aplus-block-column">${b.column2 || ''}</div>
            </div>
        `;
    }
    wrap.appendChild(content);

    wrap.querySelector('.delete-block').addEventListener('click', function () {
        if (confirm(tt('aplus.confirmDelete', 'Delete this block?'))) {
            wrap.remove();
            scheduleAutoSave();
        }
    });
    wrap.querySelector('.move-up').addEventListener('click', function () {
        if (wrap.previousElementSibling) {
            wrap.parentNode.insertBefore(wrap, wrap.previousElementSibling);
            scheduleAutoSave();
        }
    });
    wrap.querySelector('.move-down').addEventListener('click', function () {
        if (wrap.nextElementSibling) {
            wrap.parentNode.insertBefore(wrap.nextElementSibling, wrap);
            scheduleAutoSave();
        }
    });
    wrap.querySelectorAll('[data-editable]').forEach(el => {
        el.addEventListener('input', scheduleAutoSave);
        el.addEventListener('blur', scheduleAutoSave);
    });
    const imgInput = wrap.querySelector('[data-editable-img]');
    if (imgInput) {
        imgInput.addEventListener('input', function () {
            const img = wrap.querySelector('img');
            if (img && this.value) img.src = this.value;
            scheduleAutoSave();
        });
    }
    return wrap;
}

function addAplusBlock(type) {
    const presets = {
        hero: { type: 'hero', heading: tt('aplus.placeholderHeading', 'Click to edit heading'), text: tt('aplus.placeholderText', 'Click to edit text content...'), image: 'https://picsum.photos/1200/420' },
        text: { type: 'text', heading: tt('aplus.placeholderHeading', 'Click to edit heading'), text: tt('aplus.placeholderText', 'Click to edit text content...') },
        textImage: { type: 'textImage', heading: tt('aplus.placeholderHeading', 'Click to edit heading'), text: tt('aplus.placeholderText', 'Click to edit text content...'), image: 'https://picsum.photos/600/400' },
        imageText: { type: 'imageText', heading: tt('aplus.placeholderHeading', 'Click to edit heading'), text: tt('aplus.placeholderText', 'Click to edit text content...'), image: 'https://picsum.photos/600/400' },
        features: { type: 'features', heading: 'Key Features', items: [tt('aplus.placeholderFeature', 'Feature point') + ' 1', tt('aplus.placeholderFeature', 'Feature point') + ' 2', tt('aplus.placeholderFeature', 'Feature point') + ' 3'] },
        gallery: { type: 'gallery', heading: 'Gallery', images: ['https://picsum.photos/400/300', 'https://picsum.photos/400/300'] },
        multiText: { type: 'multiText', headings: ['Section 1', 'Section 2'], texts: ['Click to edit text...', 'Click to edit text...'] }
    };
    const preset = presets[type];
    if (!preset) return;
    const container = document.getElementById('aplusBlocks');
    const idx = container.children.length;
    const el = buildAplusBlockEl(preset, idx);
    container.appendChild(el);
    applyAplusEditState();
    scheduleAutoSave();
}

function collectAplusBlocks() {
    const out = [];
    document.querySelectorAll('#aplusBlocks .aplus-block').forEach(blockEl => {
        const type = blockEl.dataset.type;
        const item = { type: type };
        const heading = blockEl.querySelector('[data-editable="heading"]');
        if (heading) item.heading = heading.innerText.trim();
        const text = blockEl.querySelector('[data-editable="text"]');
        if (text) item.text = text.innerHTML;
        
        if (type === 'gallery') {
            item.images = [];
            blockEl.querySelectorAll('.gallery-item .aplus-image-input').forEach(input => {
                item.images.push(input.value || '');
            });
        } else if (type === 'multiText') {
            item.texts = [];
            item.headings = [];
            blockEl.querySelectorAll('.multi-text-item').forEach(itemEl => {
                const h = itemEl.querySelector('.multi-text-heading')?.textContent || '';
                const t = itemEl.querySelector('.multi-text-content')?.innerHTML || '';
                item.headings.push(h);
                item.texts.push(t);
            });
        } else {
            const imgInput = blockEl.querySelector('[data-editable-img]');
            if (imgInput) item.image = imgInput.value;
            else {
                const img = blockEl.querySelector('img');
                if (img) item.image = img.src;
            }
            if (type === 'features') {
                item.items = [];
                blockEl.querySelectorAll('[data-editable="feature"]').forEach(li => {
                    const v = li.innerHTML;
                    if (v) item.items.push(v);
                });
            }
        }
        out.push(item);
    });
    return out;
}

function renderBrandLogo() {
    const url = localStorage.getItem('yeatruBrandLogo');
    const img = document.getElementById('brandLogoImg');
    const fallback = document.getElementById('brandLogoFallback');
    const footerImg = document.getElementById('footerLogoImg');
    const footerFallback = document.getElementById('footerLogoFallback');
    if (url) {
        img.src = url;
        img.style.display = 'block';
        fallback.style.display = 'none';
        if (footerImg) {
            footerImg.src = url;
            footerImg.style.display = 'block';
            footerFallback.style.display = 'none';
        }
    } else {
        img.src = '';
        img.style.display = 'none';
        fallback.style.display = '';
        if (footerImg) {
            footerImg.src = '';
            footerImg.style.display = 'none';
            footerFallback.style.display = '';
        }
    }
}

function saveLogoFromModal() {
    const fileInput = document.getElementById('logoFileInput');
    const urlInput = document.getElementById('logoUrlInput');
    const finalize = function (data) {
        if (data) localStorage.setItem('yeatruBrandLogo', data);
        renderBrandLogo();
        bootstrap.Modal.getInstance(document.getElementById('logoModal')).hide();
        fileInput.value = '';
    };
    if (fileInput.files && fileInput.files[0]) {
        const file = fileInput.files[0];
        const reader = new FileReader();
        reader.onload = function (e) { finalize(e.target.result); };
        reader.readAsDataURL(file);
    } else if (urlInput.value) {
        finalize(urlInput.value);
    } else {
        finalize(null);
    }
}