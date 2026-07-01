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
        nav: { home: "Home", products: "Products", services: "Sourcing Service", sourcingProcess: "Sourcing Process", testimonials: "Testimonials", aboutUs: "About Us", contactUs: "Contact", login: "Login", logout: "Logout", servicePlans: "Service Plans", payment: "Payment", blog: "Blog", oem: "OEM Customization", sampleOrder: "Sample Order", factoryAudit: "Factory Audit" },
        hero: { title: "Professional China Sourcing Agent Yiwu & Global Supply Chain", desc: "One-stop sourcing solution from China: product sourcing, supplier audit, quality control, logistics shipping. Help global buyers source from China easily.", contactBtn: "Contact Us Now", productsBtn: "View Products" },
        products: { title: "Hot Products", subtitle: "Explore our featured products sourced from China", categoryManagement: "Category Management", enterCategory: "Enter new category name", addCategory: "Add Category", addProduct: "Add New Product", imageUrl: "Image URL", enterImageUrl: "Enter product image URL", category: "Category", selectCategory: "Select Category", name: "Product Name", enterName: "Enter product name", sku: "SKU", enterSKU: "Enter product SKU", material: "Material", enterMaterial: "Enter material", size: "Size", enterSize: "Enter size", moq: "MOQ", enterMOQ: "Enter MOQ", priceMin: "Minimum Price ($)", enterMinPrice: "Enter minimum price", priceMax: "Maximum Price ($)", enterMaxPrice: "Enter maximum price", description: "Description", enterDescription: "Enter product description", cancel: "Cancel", save: "Save Product", edit: "Edit", delete: "Delete", quote: "Get a Quote", price: "Price: $", viewDetails: "View Details" },
        filter: { title: "Filter by Category", all: "All", reset: "Reset Filter", showing: "Showing", of: "of", products: "products", noResult: "No products in this category" },
        services: { title: "Our Comprehensive Sourcing Services", subtitle: "We offer end-to-end sourcing solutions tailored to your business needs", supplierVerification: "Supplier Verification", supplierVerificationDesc: "We thoroughly vet and verify suppliers to ensure they meet international quality standards and business ethics.", productSourcing: "Product Sourcing", productSourcingDesc: "Find the right products at competitive prices with our extensive network of reliable manufacturers and suppliers.", qualityControl: "Quality Control", qualityControlDesc: "Comprehensive quality inspection at every stage of production to ensure products meet your specifications.", logistics: "Logistics & Warehousing", logisticsDesc: "Complete logistics and warehousing solutions including free storage, goods consolidation, and competitive shipping rates.", priceNegotiation: "Price Negotiation", priceNegotiationDesc: "Leverage our local expertise to negotiate the best prices and payment terms with suppliers.", designPhotography: "Design & Photography", designPhotographyDesc: "Professional product photography and graphic design to make your products stand out and boost sales." },
        process: { title: "Our Simple Sourcing Process", subtitle: "We make sourcing from China straightforward and transparent", step1: "Your Requirements", step1Desc: "Share your product specifications, quantity, budget and timeline with our team.", step2: "Supplier Matching", step2Desc: "We identify and verify the best suppliers that match your specific requirements.", step3: "Sample & Pricing", step3Desc: "Obtain samples and competitive pricing quotes from pre-vetted suppliers.", step4: "Delivery & Support", step4Desc: "We handle production oversight, quality control and shipping to your doorstep." },
        testimonials: { title: "What Clients Say", subtitle: "Feedback from our global buyers", review1: "\"Yeatru Sourcing helped me source 5000+ storage boxes from Yiwu, great quality and fast shipping. Highly recommended!\"", review2: "\"Professional team, strict quality control, and excellent after-sales service. Best China sourcing partner I ever worked with.\"", review3: "\"The price negotiation service saved me over 20% on my order. The logistics team ensured on-time delivery to the US. Very satisfied!\"" },
        about: { title: "About Yeatru Sourcing", profile: "Company Profile", profileDesc: "Yeatru Sourcing is a professional one-stop sourcing agent located in Yiwu City, the world's largest small commodity distribution center. We specialize in providing global clients with reliable procurement services, supplier development, strict quality inspection, supplier management and integrated logistics solutions." },
        contact: { getInTouch: "Get In Touch With Us", desc: "Ready to start your sourcing journey? Fill out the form or contact us directly using the information below.", requestQuote: "Request a Free Quote", yourName: "Your Name", enterName: "Enter your name", email: "Email Address", enterEmail: "Enter your email", phone: "Phone Number", product: "Product You Need (e.g. Plastic storage boxes)", message: "Please describe your requirements in detail", enterMessage: "Enter your message", sendRequest: "Send Request" },
        footer: { desc: "Professional China sourcing agent helping businesses worldwide find reliable suppliers and quality products at competitive prices.", quickLinks: "Quick Links", services: "Our Services", contact: "Contact Us" },
        login: { title: "Admin Login", username: "Username", enterUsername: "Enter username", password: "Password", enterPassword: "Enter password", error: "Incorrect username or password!", cancel: "Cancel", submit: "Login" },
        quote: { title: "Get a Quote", quantity: "Required Quantity", enterQuantity: "Enter quantity", cancel: "Cancel", send: "Send Quote Request" },
        detail: { back: "Back to Products", edit: "Edit", preview: "Preview", saving: "Saving...", saved: "Saved", error: "Save failed" },
        aplus: { title: "A+ Content", addBlock: "Add a content block:", blockHero: "Hero Banner", blockText: "Text", blockTextImage: "Text + Image", blockImageText: "Image + Text", blockFeatures: "Feature Grid", placeholderHeading: "Click to edit heading", placeholderText: "Click to edit text content...", placeholderFeature: "Feature point", confirmDelete: "Delete this block?" },
        logo: { title: "Update Brand Logo", tip: "Logo is displayed in a 50x50 pixel container. Upload a square image (PNG/JPG/SVG) or paste an image URL for best results.", uploadFile: "Upload Image", imageUrl: "Or Image URL", reset: "Reset to Default", cancel: "Cancel", save: "Save Logo" },
        advantages: { eyebrow: "Why Choose Us", title: "Our Core Advantages", subtitle: "What makes Yeatru your best China sourcing partner", lowMOQ: "Low MOQ Support", lowMOQDesc: "Start with small orders. We connect you with suppliers offering flexible MOQ suitable for startups and small businesses.", oneStop: "One-Stop China Sourcing", oneStopDesc: "From supplier matching to quality control and shipping — we handle the entire procurement process for you.", oem: "OEM & Private Label", oemDesc: "Customize products with your brand logo, packaging, and design. Professional samples in 3-7 days.", fastSample: "Fast Sample Production", fastSampleDesc: "Get professional samples quickly to verify quality before mass production. Sample fee refundable with bulk orders.", strictQC: "Strict QC Inspection", strictQCDesc: "AQL 2.5 quality inspections at every stage. We ensure products meet your specifications before shipping.", global: "Global Door-to-Door", globalDesc: "Free warehousing, goods consolidation, and competitive shipping rates to anywhere in the world." },
        banner: { slide1Tag: "14+ Years Experience · 200+ Clients Worldwide", slide1Title: "Start Sourcing from China Today — As Low as 50 Pieces MOQ", slide1Subtitle: "Join 200+ global sellers who've cut sourcing costs by 30%+. We handle supplier vetting, quality control, and shipping — you focus on growing your sales.", slide1Feat1: "50 Pieces MOQ", slide1Feat2: "24hr Quote", slide1Feat3: "Zero Risk", slide1Btn1: "Get Free Quote Now", slide1Btn2: "View Products", slide2Tag: "Build Your Brand Identity", slide2Title: "Custom Logo, Packaging & Design — Ship in 7 Days", slide2Subtitle: "Stand out from competitors with custom-branded products. Free design consultation included — no hidden fees, transparent pricing from day one.", slide2Feat1: "Free Design Support", slide2Feat2: "7-Day Sample", slide2Feat3: "Low MOQ 200pcs", slide2Btn1: "Start Custom Design", slide2Btn2: "View OEM Services", slide3Tag: "Global Logistics", slide3Title: "Drop Shipping & Global Warehouse Consolidation", slide3Subtitle: "Ship directly to your customers worldwide. We offer free warehousing, goods consolidation, and competitive door-to-door shipping rates.", slide3Feat1: "Free Warehousing", slide3Feat2: "Door-to-Door Delivery", slide3Feat3: "Global Coverage", slide3Btn1: "Get Free Quote", slide3Btn2: "Learn More" },
        common: { getQuote: "Get Quote", getFreeQuote: "Get Free Quote", contactUs: "Contact Us", viewProducts: "View Products", viewAll: "View All", learnMore: "Learn More", browseAll: "Browse All Products", startSourcing: "Start Your Sourcing", chatWithUs: "Chat With Us", sendRequest: "Send Request", viewAllArticles: "View All Articles", readArticle: "Read article", popularCategories: "Popular Categories", hotProducts: "Hot Selling Products", hotProductsSubtitle: "Browse our most popular product categories sourced from trusted suppliers", whatWeOffer: "What We Offer", oneStopServices: "One-Stop Sourcing Services", howItWorks: "How It Works", simpleProcess: "Simple 4-Step Sourcing Process", simpleProcessSubtitle: "From inquiry to delivery, we make sourcing from China easy", sendRequirements: "Send Requirements", sendRequirementsDesc: "Tell us your product needs, quantity, budget, and timeline. We'll find the best suppliers for you.", sourceQuote: "Source & Quote", sourceQuoteDesc: "We identify verified suppliers, negotiate prices, and send you detailed quotes with samples.", sampleConfirm: "Sample Confirm", sampleConfirmDesc: "Review samples, confirm quality, and finalize your order details before mass production.", productionShip: "Production & Ship", productionShipDesc: "We oversee production, QC inspection, consolidation, and ship directly to your door.", faq: "FAQ", faqSubtitle: "Quick answers to common questions about our sourcing services", all: "All", stillQuestions: "Still have questions?", clientStories: "Client Stories", trustedBy: "Trusted by Global Buyers", trustedBySubtitle: "Real feedback from Amazon sellers, local retailers, and wholesalers worldwide", sourcingKnowledge: "Sourcing Knowledge", sourcingInsights: "China Sourcing Insights & Tips", sourcingInsightsSubtitle: "Practical guides to help you source smarter and grow your business", globalClients: "Global Clients", countriesServed: "Countries Served", clientSatisfaction: "Client Satisfaction", supportAvailable: "Support Available", minRead: "min read", aboutUs: "About Us", contactUsTitle: "Contact Us", searchPlaceholder: "Search products, services, guides...", inquirySub: "Choose your preferred channel" },
        footer: { desc: "Professional China sourcing agent helping businesses worldwide find reliable suppliers and quality products at competitive prices.", quickLinks: "Quick Links", services: "Our Services", contact: "Contact Us", paymentMethods: "Payment Methods", privacyPolicy: "Privacy Policy", termsOfService: "Terms of Service", allRightsReserved: "All rights reserved." },
        aboutPage: { heroTag: "About Us", heroTitle: "Your Trusted China Sourcing Partner", heroSubtitle: "Founded in Yiwu — the world's largest small commodity market — we connect global buyers with reliable Chinese manufacturers.", feat1: "14+ Years Combined Experience", feat2: "200+ Global Clients", feat3: "50+ Countries Served", btnContact: "Contact Us", btnLearnMore: "Learn More", storyEyebrow: "Our Story", storyTitle: "From Yiwu to the World", storySubtitle: "Founded Where the World's Best Products Are Made", storyPara1: "Yeatru Sourcing was founded in Yiwu, Zhejiang Province — home to the Yiwu International Trade City, the world's largest small commodity wholesale market with over 75,000 booths and products in 26 categories.", storyPara2: "Our founding team brings over 14 years of combined experience in China manufacturing, supplier management, quality control, and international logistics. We've helped Amazon FBA sellers launch private-label products, local retailers source cost-competitive inventory, and wholesale buyers build long-term supplier partnerships.", storyPara3: "Our mission is simple: make sourcing from China transparent, affordable, and risk-free — one order at a time.", valuesEyebrow: "Our Values", valuesTitle: "What We Stand For", transparency: "Transparency", transparencyDesc: "Full cost breakdowns, no hidden fees, and honest communication at every step. You'll always know where your money goes.", integrity: "Integrity", integrityDesc: "We act in your best interest — not the factory's. NDA-signed confidentiality, no commissions from suppliers on your order.", verification: "Verification First", verificationDesc: "We don't take risks with your business. Every supplier we recommend has been vetted, visited, or audited by our team.", results: "Results-Driven", resultsDesc: "We measure success by your results: lower costs, better quality, faster delivery. Your growth is our growth.", whyEyebrow: "Why Yeatru", whyTitle: "What Makes Us Different", statClients: "Global Clients", statCountries: "Countries Served", statYears: "Years Combined Experience", statFactories: "Factory Network", whyHeading: "Local Expertise, Global Standards", whyPara1: "We combine deep local market knowledge with international business standards. Our team speaks English, Mandarin, and Spanish. We bridge the gap between Chinese factories and global buyers.", whyPara2: "Unlike trading companies, we don't mark up product prices. Our fee structure is transparent — and our incentive is aligned with yours: better outcomes mean more repeat business.", servicesEyebrow: "What We Do", servicesTitle: "End-to-End Sourcing Services", faqEyebrow: "Common Questions", faqTitle: "About Working with Yeatru", faq1Q: "What types of buyers do you work with?", faq1A: "We serve Amazon FBA sellers, TikTok Shop sellers, local retailers, wholesale distributors, and e-commerce entrepreneurs. From first-time importers to established brands expanding their China supply chain.", faq2Q: "How is Yeatru different from a trading company?", faq2A: "Trading companies mark up product prices 15-30% above factory cost. We charge a transparent flat fee or percentage — and our fee is disclosed upfront. You always get the factory-direct price.", faq3Q: "Do you work with small orders?", faq3A: "Yes. We're built for small-to-medium buyers. Many of our suppliers accept MOQs as low as 50-100 pieces. We help you start small and scale up.", faq4Q: "What happens if a supplier fails to deliver?", faq4A: "We mediate between you and the supplier. If the supplier is at fault, we negotiate compensation, source alternative factories, and cover the difference in costs if applicable under our service guarantee.", faq5Q: "How do I get started?", faq5A: "The easiest way: send us your product requirements via our contact form or WhatsApp. We'll reply within 4 hours with initial quotes and a sourcing plan.", ctaEyebrow: "Let's Work Together", ctaTitle: "Start Your Sourcing Journey Today", ctaSubtitle: "No commitment required. Get a free consultation and initial quote within 24 hours.", ctaBtn: "Contact Us Now" },
        contactPage: { heroTag: "Contact Us", heroTitle: "Get in Touch With Us", heroSubtitle: "Have a question or ready to start your sourcing project? We're here to help 24/7.", heroFeat1: "24/7 Support", heroFeat2: "Reply Within 4 Hours", heroFeat3: "Free Consultation", infoEyebrow: "Contact Information", infoTitle: "Multiple Ways to Reach Us", infoSubtitle: "Choose your preferred channel -- we respond fast", instantMsg: "Instant Messaging", officialEmail: "Official Email", phoneSupport: "Phone Support", ourOffice: "Our Office", quoteEyebrow: "Request a Quote", quoteTitle: "Tell Us What You Need", quoteSubtitle: "Fill in the form below and we'll get back to you within 4 hours", statYears: "Years Experience", statClients: "Global Clients", statCountries: "Countries Served", statSatisfaction: "Satisfaction" }
    }},
    es: { translation: {
        nav: { home: "Inicio", products: "Productos", services: "Servicio de Suministro", sourcingProcess: "Proceso de Suministro", testimonials: "Testimonios", aboutUs: "Sobre Nosotros", contactUs: "Contacto", login: "Iniciar Sesión", logout: "Cerrar Sesión", servicePlans: "Planes de Servicio", payment: "Pago", blog: "Blog", oem: "Personalización OEM", sampleOrder: "Pedido de Muestra", factoryAudit: "Auditoría de Fábrica" },
        hero: { title: "Agente Profesional de Suministro en China Yiwu & Cadena de Suministro Global", desc: "Solución integral de suministro desde China: búsqueda de productos, auditoría de proveedores, control de calidad, envío logístico. Ayudamos a compradores globales a abastecerse de China fácilmente.", contactBtn: "Contáctenos Ahora", productsBtn: "Ver Productos" },
        products: { title: "Productos Populares", subtitle: "Explora nuestros productos destacados suministrados desde China", categoryManagement: "Gestión de Categorías", enterCategory: "Ingrese el nombre de la nueva categoría", addCategory: "Agregar Categoría", addProduct: "Agregar Nuevo Producto", imageUrl: "URL de la Imagen", enterImageUrl: "Ingrese la URL de la imagen del producto", category: "Categoría", selectCategory: "Seleccionar Categoría", name: "Nombre del Producto", enterName: "Ingrese el nombre del producto", sku: "SKU", enterSKU: "Ingrese el SKU del producto", material: "Material", enterMaterial: "Ingrese el material", size: "Tamaño", enterSize: "Ingrese el tamaño", moq: "MOQ", enterMOQ: "Ingrese la MOQ", priceMin: "Precio Mínimo ($)", enterMinPrice: "Ingrese el precio mínimo", priceMax: "Precio Máximo ($)", enterMaxPrice: "Ingrese el precio máximo", description: "Descripción", enterDescription: "Ingrese la descripción del producto", cancel: "Cancelar", save: "Guardar Producto", edit: "Editar", delete: "Eliminar", quote: "Solicitar Presupuesto", price: "Precio: $", viewDetails: "Ver Detalles" },
        filter: { title: "Filtrar por Categoría", all: "Todos", reset: "Restablecer Filtro", showing: "Mostrando", of: "de", products: "productos", noResult: "No hay productos en esta categoría" },
        services: { title: "Nuestros Servicios Integrales de Suministro", subtitle: "Ofrecemos soluciones de suministro de extremo a extremo adaptadas a las necesidades de su negocio", supplierVerification: "Verificación de Proveedores", supplierVerificationDesc: "Revisamos y verificamos a fondo a los proveedores para garantizar que cumplen con los estándares de calidad internacionales y la ética empresarial.", productSourcing: "Búsqueda de Productos", productSourcingDesc: "Encuentra los productos adecuados a precios competitivos con nuestra extensa red de fabricantes y proveedores confiables.", qualityControl: "Control de Calidad", qualityControlDesc: "Inspección de calidad integral en cada etapa de la producción para garantizar que los productos cumplen con sus especificaciones.", logistics: "Logística y Almacenamiento", logisticsDesc: "Soluciones completas de logística y almacenamiento con almacenamiento gratuito, consolidación de mercancías y tarifas de envío competitivas.", priceNegotiation: "Negociación de Precios", priceNegotiationDesc: "Aproveche nuestra experiencia local para negociar los mejores precios y condiciones de pago con los proveedores.", designPhotography: "Diseño y Fotografía", designPhotographyDesc: "Fotografía profesional de productos y diseño gráfico para que sus productos destaquen y aumenten las ventas." },
        process: { title: "Nuestro Simple Proceso de Suministro", subtitle: "Hacemos que el aprovisionamiento desde China sea sencillo y transparente", step1: "Sus Requisitos", step1Desc: "Comuníquese con nuestro equipo sobre las especificaciones del producto, cantidad, presupuesto y cronograma.", step2: "Coincidencia de Proveedores", step2Desc: "Identificamos y verificamos a los mejores proveedores que se adaptan a sus requisitos específicos.", step3: "Muestras y Precios", step3Desc: "Obtenga muestras y cotizaciones de precios competitivos de proveedores previamente verificados.", step4: "Entrega y Soporte", step4Desc: "Nos encargamos de la supervisión de la producción, el control de calidad y el envío hasta su puerta." },
        testimonials: { title: "Lo Que Dicen Nuestros Clientes", subtitle: "Comentarios de nuestros compradores globales", review1: "\"Yeatru Sourcing me ayudó a suministrar más de 5000 cajas de almacenamiento desde Yiwu, excelente calidad y envío rápido. ¡Muy recomendado!\"", review2: "\"Equipo profesional, control de calidad estricto y excelente servicio postventa. El mejor socio de suministro chino con el que he trabajado.\"", review3: "\"El servicio de negociación de precios me ahorró más del 20% en mi pedido. El equipo logístico garantizó la entrega a tiempo a EE. UU. ¡Muy satisfecho!\"" },
        about: { title: "Sobre Yeatru Sourcing", profile: "Perfil de la Empresa", profileDesc: "Yeatru Sourcing es un agente profesional de suministro integral ubicado en la ciudad de Yiwu, el mayor centro de distribución de pequeñas mercancías del mundo. Nos especializamos en brindar a clientes globales servicios de adquisición confiables, desarrollo de proveedores, inspección de calidad estricta, gestión de proveedores y soluciones logísticas integradas." },
        contact: { getInTouch: "Póngase en Contacto Con Nosotros", desc: "¿Listo para comenzar su viaje de suministro? Complete el formulario o contáctenos directamente con la información a continuación.", requestQuote: "Solicitar un Presupuesto Gratuito", yourName: "Su Nombre", enterName: "Ingrese su nombre", email: "Dirección de Correo Electrónico", enterEmail: "Ingrese su correo electrónico", phone: "Número de Teléfono", product: "Producto que Necesita", message: "Describa sus requisitos en detalle", enterMessage: "Ingrese su mensaje", sendRequest: "Enviar Solicitud" },
        footer: { desc: "Agente profesional de suministro chino que ayuda a empresas de todo el mundo a encontrar proveedores confiables y productos de calidad a precios competitivos.", quickLinks: "Enlaces Rápidos", services: "Nuestros Servicios", contact: "Contáctenos" },
        login: { title: "Inicio de Sesión de Administrador", username: "Nombre de Usuario", enterUsername: "Ingrese el nombre de usuario", password: "Contraseña", enterPassword: "Ingrese la contraseña", error: "¡Nombre de usuario o contraseña incorrectos!", cancel: "Cancelar", submit: "Iniciar Sesión" },
        quote: { title: "Solicitar Presupuesto", quantity: "Cantidad Requerida", enterQuantity: "Ingrese la cantidad", cancel: "Cancelar", send: "Enviar Solicitud de Presupuesto" },
        detail: { back: "Volver a Productos", edit: "Editar", preview: "Vista previa", saving: "Guardando...", saved: "Guardado", error: "Error al guardar" },
        aplus: { title: "Contenido A+", addBlock: "Agregar un bloque de contenido:", blockHero: "Banner Principal", blockText: "Texto", blockTextImage: "Texto + Imagen", blockImageText: "Imagen + Texto", blockFeatures: "Cuadrícula de Características", placeholderHeading: "Haz clic para editar título", placeholderText: "Haz clic para editar contenido...", placeholderFeature: "Punto destacado", confirmDelete: "¿Eliminar este bloque?" },
        logo: { title: "Actualizar Logotipo", tip: "El logotipo se muestra en un contenedor de 50x50 píxeles. Cargue una imagen cuadrada o pegue una URL.", uploadFile: "Cargar Imagen", imageUrl: "O URL de Imagen", reset: "Restablecer", cancel: "Cancelar", save: "Guardar Logotipo" },
        advantages: { eyebrow: "Por Qué Elegirnos", title: "Nuestras Ventajas Principales", subtitle: "Qué hace de Yeatru su mejor socio de suministro en China", lowMOQ: "Soporte de MOQ Bajo", lowMOQDesc: "Comience con pedidos pequeños. Le conectamos con proveedores que ofrecen MOQ flexible, ideal para startups y pequeñas empresas.", oneStop: "Suministro Integral en China", oneStopDesc: "Desde la búsqueda de proveedores hasta el control de calidad y el envío — gestionamos todo el proceso de adquisición para usted.", oem: "OEM y Marca Privada", oemDesc: "Personalice productos con el logotipo, empaque y diseño de su marca. Muestras profesionales en 3-7 días.", fastSample: "Producción Rápida de Muestras", fastSampleDesc: "Obtenga muestras profesionales rápidamente para verificar la calidad antes de la producción en masa. La tarifa de muestra es reembolsable con pedidos al por mayor.", strictQC: "Inspección de Calidad Estricta", strictQCDesc: "Inspecciones de calidad AQL 2.5 en cada etapa. Aseguramos que los productos cumplan con sus especificaciones antes del envío.", global: "Entrega Puerta a Puerta Global", globalDesc: "Almacenamiento gratuito, consolidación de mercancías y tarifas de envío competitivas a cualquier parte del mundo." },
        banner: { slide1Tag: "14+ Años de Experiencia · 200+ Clientes Globales", slide1Title: "Comience a Abastecer desde China Hoy — Desde Solo 50 Piezas MOQ", slide1Subtitle: "Únase a más de 200 vendedores globales que han reducido sus costos de abastecimiento en un 30%+. Nosotros manejamos la verificación de proveedores, control de calidad y envío — usted enfocarse en crecer sus ventas.", slide1Feat1: "MOQ 50 Piezas", slide1Feat2: "Cotización en 24h", slide1Feat3: "Sin Riesgo", slide1Btn1: "Obtener Cotización Gratis Ahora", slide1Btn2: "Ver Productos", slide2Tag: "Construya Su Identidad de Marca", slide2Title: "Logo Personalizado, Empaque y Diseño — Envío en 7 Días", slide2Subtitle: "Destaque de la competencia con productos de marca personalizada. Consulta de diseño gratuita incluida — sin tarifas ocultas, precios transparentes desde el primer día.", slide2Feat1: "Soporte de Diseño Gratis", slide2Feat2: "Muestra en 7 Días", slide2Feat3: "MOQ Bajo 200pcs", slide2Btn1: "Comenzar Diseño Personalizado", slide2Btn2: "Ver Servicios OEM", slide3Tag: "Logística Global", slide3Title: "Drop Shipping y Consolidación de Almacenes Globales", slide3Subtitle: "Envíe directamente a sus clientes en todo el mundo. Ofrecemos almacenamiento gratuito, consolidación de mercancías y tarifas de envío puerta a puerta competitivas.", slide3Feat1: "Almacenamiento Gratuito", slide3Feat2: "Entrega Puerta a Puerta", slide3Feat3: "Cobertura Global", slide3Btn1: "Obtener Cotización Gratis", slide3Btn2: "Saber Más" },
        common: { getQuote: "Obtener Presupuesto", getFreeQuote: "Obtener Presupuesto Gratuito", contactUs: "Contáctenos", viewProducts: "Ver Productos", viewAll: "Ver Todo", learnMore: "Saber Más", browseAll: "Explorar Todos los Productos", startSourcing: "Inicie su Suministro", chatWithUs: "Chatee Con Nosotros", sendRequest: "Enviar Solicitud", viewAllArticles: "Ver Todos los Artículos", readArticle: "Leer artículo", popularCategories: "Categorías Populares", hotProducts: "Productos Más Vendidos", hotProductsSubtitle: "Explore nuestras categorías de productos más populares de proveedores confiables", whatWeOffer: "Qué Ofrecemos", oneStopServices: "Servicios de Suministro Integral", howItWorks: "Cómo Funciona", simpleProcess: "Proceso de Suministro Simple en 4 Pasos", simpleProcessSubtitle: "Desde la consulta hasta la entrega, facilitamos el suministro desde China", sendRequirements: "Enviar Requisitos", sendRequirementsDesc: "Cuéntenos sus necesidades de producto, cantidad, presupuesto y plazo. Encontraremos los mejores proveedores para usted.", sourceQuote: "Buscar y Presupuestar", sourceQuoteDesc: "Identificamos proveedores verificados, negociamos precios y le enviamos presupuestos detallados con muestras.", sampleConfirm: "Confirmación de Muestra", sampleConfirmDesc: "Revise muestras, confirme la calidad y finalice los detalles de su pedido antes de la producción en masa.", productionShip: "Producción y Envío", productionShipDesc: "Supervisamos la producción, inspección de calidad, consolidación y enviamos directamente a su puerta.", faq: "Preguntas Frecuentes", faqSubtitle: "Respuestas rápidas a preguntas comunes sobre nuestros servicios de suministro", all: "Todo", stillQuestions: "¿Aún tiene preguntas?", clientStories: "Historias de Clientes", trustedBy: "Confianza de Compradores Globales", trustedBySubtitle: "Comentarios reales de vendedores de Amazon, minoristas locales y mayoristas de todo el mundo", sourcingKnowledge: "Conocimiento de Suministro", sourcingInsights: "Consejos e Ideas sobre Suministro en China", sourcingInsightsSubtitle: "Guías prácticas para ayudarle a suministrar de forma más inteligente y hacer crecer su negocio", globalClients: "Clientes Globales", countriesServed: "Países Atendidos", clientSatisfaction: "Satisfacción del Cliente", supportAvailable: "Soporte Disponible", minRead: "min de lectura", aboutUs: "Sobre Nosotros", contactUsTitle: "Contáctenos", searchPlaceholder: "Buscar productos, servicios, guías...", inquirySub: "Elija su canal preferido" },
        footer: { desc: "Agente profesional de suministro chino que ayuda a empresas de todo el mundo a encontrar proveedores confiables y productos de calidad a precios competitivos.", quickLinks: "Enlaces Rápidos", services: "Nuestros Servicios", contact: "Contáctenos", paymentMethods: "Métodos de Pago", privacyPolicy: "Política de Privacidad", termsOfService: "Términos de Servicio", allRightsReserved: "Todos los derechos reservados." },
        aboutPage: { heroTag: "Sobre Nosotros", heroTitle: "Su Socio de Confianza en Suministro en China", heroSubtitle: "Fundados en Yiwu — el mercado de pequeñas mercancías más grande del mundo — conectamos a compradores globales con fabricantes chinos confiables.", feat1: "Más de 14 Años de Experiencia Combinada", feat2: "Más de 200 Clientes Globales", feat3: "Más de 50 Países Atendidos", btnContact: "Contáctenos", btnLearnMore: "Saber Más", storyEyebrow: "Nuestra Historia", storyTitle: "Desde Yiwu al Mundo", storySubtitle: "Fundados Donde Se Fabrican los Mejores Productos del Mundo", storyPara1: "Yeatru Sourcing fue fundada en Yiwu, provincia de Zhejiang — sede de la Ciudad Comercial Internacional de Yiwu, el mercado mayorista de pequeñas mercancías más grande del mundo con más de 75.000 puestos y productos en 26 categorías.", storyPara2: "Nuestro equipo fundador aporta más de 14 años de experiencia combinada en fabricación en China, gestión de proveedores, control de calidad y logística internacional. Hemos ayudado a vendedores de Amazon FBA a lanzar productos de marca privada, a minoristas locales a obtener inventario competitivo en costos y a compradores mayoristas a construir asociaciones a largo plazo con proveedores.", storyPara3: "Nuestra misión es simple: hacer que el suministro desde China sea transparente, asequible y sin riesgos — un pedido a la vez.", valuesEyebrow: "Nuestros Valores", valuesTitle: "En Qué Creemos", transparency: "Transparencia", transparencyDesc: "Desgloses completos de costos, sin tarifas ocultas y comunicación honesta en cada paso. Siempre sabrá dónde va su dinero.", integrity: "Integridad", integrityDesc: "Actuamos en su mejor interés — no en el de la fábrica. Confidencialidad con firma de NDA, sin comisiones de proveedores en su pedido.", verification: "Verificación Primero", verificationDesc: "No tomamos riesgos con su negocio. Cada proveedor que recomendamos ha sido examinado, visitado o auditado por nuestro equipo.", results: "Orientado a Resultados", resultsDesc: "Medimos el éxito por sus resultados: menores costos, mejor calidad, entrega más rápida. Su crecimiento es nuestro crecimiento.", whyEyebrow: "Por Qué Yeatru", whyTitle: "Qué Nos Hace Diferentes", statClients: "Clientes Globales", statCountries: "Países Atendidos", statYears: "Años de Experiencia Combinada", statFactories: "Red de Fábricas", whyHeading: "Experiencia Local, Estándares Globales", whyPara1: "Combinamos un profundo conocimiento del mercado local con estándares comerciales internacionales. Nuestro equipo habla inglés, mandarín y español. Salvamos la brecha entre las fábricas chinas y los compradores globales.", whyPara2: "A diferencia de las empresas comerciales, no aumentamos los precios de los productos. Nuestra estructura de tarifas es transparente — y nuestro incentivo está alineado con el suyo: mejores resultados significan más negocios repetidos.", servicesEyebrow: "Qué Hacemos", servicesTitle: "Servicios de Suministro de Extremo a Extremo", faqEyebrow: "Preguntas Comunes", faqTitle: "Sobre Trabajar con Yeatru", faq1Q: "¿Con qué tipos de compradores trabajan?", faq1A: "Atendemos a vendedores de Amazon FBA, vendedores de TikTok Shop, minoristas locales, distribuidores mayoristas y emprendedores de comercio electrónico. Desde importadores novatos hasta marcas establecidas que amplían su cadena de suministro en China.", faq2Q: "¿En qué se diferencia Yeatru de una empresa comercial?", faq2A: "Las empresas comerciales aumentan los precios de los productos un 15-30% sobre el costo de fábrica. Cobramos una tarifa fija o porcentaje transparente — y nuestra tarifa se revela por adelantado. Siempre obtiene el precio directo de fábrica.", faq3Q: "¿Trabajan con pedidos pequeños?", faq3A: "Sí. Estamos hechos para compradores pequeños y medianos. Muchos de nuestros proveedores aceptan MOQ tan bajas como 50-100 piezas. Le ayudamos a empezar poco a poco y escalar.", faq4Q: "¿Qué pasa si un proveedor no cumple con la entrega?", faq4A: "Mediamos entre usted y el proveedor. Si el proveedor tiene la culpa, negociamos compensación, buscamos fábricas alternativas y cubrimos la diferencia en costos si corresponde bajo nuestra garantía de servicio.", faq5Q: "¿Cómo empiezo?", faq5A: "La forma más fácil: envíenos sus requisitos de producto a través de nuestro formulario de contacto o WhatsApp. Le responderemos en 4 horas con presupuestos iniciales y un plan de suministro.", ctaEyebrow: "Trabajemos Juntos", ctaTitle: "Inicie Su Viaje de Suministro Hoy", ctaSubtitle: "Sin compromiso. Obtenga una consulta gratuita y presupuesto inicial en 24 horas.", ctaBtn: "Contáctenos Ahora" },
        contactPage: { heroTag: "Contáctenos", heroTitle: "Póngase en Contacto Con Nosotros", heroSubtitle: "¿Tiene una pregunta o está listo para comenzar su proyecto de suministro? Estamos aquí para ayudarle 24/7.", heroFeat1: "Soporte 24/7", heroFeat2: "Respuesta en 4 Horas", heroFeat3: "Consulta Gratuita", infoEyebrow: "Información de Contacto", infoTitle: "Múltiples Formas de Contactarnos", infoSubtitle: "Elija su canal preferido — respondemos rápido", instantMsg: "Mensajería Instantánea", officialEmail: "Correo Electrónico Oficial", phoneSupport: "Soporte Telefónico", ourOffice: "Nuestra Oficina", quoteEyebrow: "Solicitar Presupuesto", quoteTitle: "Cuéntenos Lo Que Necesita", quoteSubtitle: "Complete el formulario a continuación y le responderemos en 4 horas", statYears: "Años de Experiencia", statClients: "Clientes Globales", statCountries: "Países Atendidos", statSatisfaction: "Satisfacción" }
    }},
    fr: { translation: {
        nav: { home: "Accueil", products: "Produits", services: "Services", sourcingProcess: "Processus d'Approvisionnement", testimonials: "Témoignages", aboutUs: "À Propos de Nous", contactUs: "Nous Contacter", login: "Connexion", logout: "Déconnexion", servicePlans: "Plans de Service", payment: "Paiement", blog: "Blog", oem: "Personnalisation OEM", sampleOrder: "Commande d'Échantillon", factoryAudit: "Audit d'Usine" },
        hero: { title: "Agent Professionnel d'Approvisionnement en Chine Yiwu & Chaîne d'Approvisionnement Mondiale", desc: "Solution d'approvisionnement tout-en-un depuis la Chine: recherche de produits, audit de fournisseurs, contrôle de qualité, expédition logistique. Aidons les acheteurs mondiaux à s'approvisionner facilement depuis la Chine.", contactBtn: "Nous Contacter Maintenant", productsBtn: "Voir les Produits" },
        products: { title: "Produits Populaires", subtitle: "Découvrez nos produits phares approvisionnés depuis la Chine", categoryManagement: "Gestion des Catégories", enterCategory: "Entrez le nom de la nouvelle catégorie", addCategory: "Ajouter une Catégorie", addProduct: "Ajouter un Nouveau Produit", imageUrl: "URL de l'Image", enterImageUrl: "Entrez l'URL de l'image du produit", category: "Catégorie", selectCategory: "Sélectionner une Catégorie", name: "Nom du Produit", enterName: "Entrez le nom du produit", sku: "SKU", enterSKU: "Entrez le SKU du produit", material: "Matériau", enterMaterial: "Entrez le matériau", size: "Taille", enterSize: "Entrez la taille", moq: "MOQ", enterMOQ: "Entrez la MOQ", priceMin: "Prix Minimum ($)", enterMinPrice: "Entrez le prix minimum", priceMax: "Prix Maximum ($)", enterMaxPrice: "Entrez le prix maximum", description: "Description", enterDescription: "Entrez la description du produit", cancel: "Annuler", save: "Enregistrer", edit: "Modifier", delete: "Supprimer", quote: "Demander un Devis", price: "Prix: $", viewDetails: "Voir les Détails" },
        filter: { title: "Filtrer par Catégorie", all: "Tous", reset: "Réinitialiser le Filtre", showing: "Affichage de", of: "sur", products: "produits", noResult: "Aucun produit dans cette catégorie" },
        services: { title: "Nos Services Complets d'Approvisionnement", subtitle: "Nous offrons des solutions d'approvisionnement de bout en bout adaptées aux besoins de votre entreprise", supplierVerification: "Vérification des Fournisseurs", supplierVerificationDesc: "Nous examinons et vérifions en profondeur les fournisseurs pour garantir qu'ils respectent les normes de qualité internationales et l'éthique professionnelle.", productSourcing: "Recherche de Produits", productSourcingDesc: "Trouvez les bons produits à des prix compétitifs grâce à notre vaste réseau de fabricants et fournisseurs fiables.", qualityControl: "Contrôle de Qualité", qualityControlDesc: "Inspection de qualité complète à chaque étape de la production pour garantir que les produits répondent à vos spécifications.", logistics: "Logistique et Entrepôt", logisticsDesc: "Solutions complètes de logistique et d'entreposage avec stockage gratuit, consolidation des marchandises et tarifs d'expédition compétitifs.", priceNegotiation: "Négociation de Prix", priceNegotiationDesc: "Profitez de notre expertise locale pour négocier les meilleurs prix et conditions de paiement avec les fournisseurs.", designPhotography: "Design et Photographie", designPhotographyDesc: "Photographie professionnelle de produits et design graphique pour que vos produits se démarquent et augmentent les ventes." },
        process: { title: "Notre Simple Processus d'Approvisionnement", subtitle: "Nous rendons l'approvisionnement depuis la Chine simple et transparent", step1: "Vos Exigences", step1Desc: "Partagez vos spécifications de produit, quantité, budget et calendrier avec notre équipe.", step2: "Appariement des Fournisseurs", step2Desc: "Nous identifions et vérifions les meilleurs fournisseurs correspondant à vos exigences spécifiques.", step3: "Échantillons et Prix", step3Desc: "Obtenez des échantillons et des devis de prix compétitifs de fournisseurs pré-vérifiés.", step4: "Livraison et Support", step4Desc: "Nous nous occupons de la supervision de la production, du contrôle de qualité et de l'expédition jusqu'à votre porte." },
        testimonials: { title: "Ce Que Disent Nos Clients", subtitle: "Avis de nos acheteurs mondiaux", review1: "\"Yeatru Sourcing m'a aidé à approvisionner plus de 5000 boîtes de rangement depuis Yiwu, excellente qualité et expédition rapide. Très recommandé!\"", review2: "\"Équipe professionnelle, contrôle de qualité strict et excellent service après-vente. Le meilleur partenaire d'approvisionnement chinois avec lequel j'ai travaillé.\"", review3: "\"Le service de négociation de prix m'a fait économiser plus de 20% sur ma commande. L'équipe logistique a assuré la livraison à temps aux États-Unis. Très satisfait!\"" },
        about: { title: "À Propos de Yeatru Sourcing", profile: "Profil de l'Entreprise", profileDesc: "Yeatru Sourcing est un agent d'approvisionnement tout-en-un professionnel situé dans la ville de Yiwu, le plus grand centre de distribution de petits articles au monde. Nous nous spécialisons dans la fourniture de services d'approvisionnement fiables, de développement de fournisseurs, d'inspection de qualité stricte, de gestion de fournisseurs et de solutions logistiques intégrées aux clients du monde entier." },
        contact: { getInTouch: "Prenez Contact Avec Nous", desc: "Prêt à commencer votre voyage d'approvisionnement? Remplissez le formulaire ou contactez-nous directement.", requestQuote: "Demander un Devis Gratuit", yourName: "Votre Nom", enterName: "Entrez votre nom", email: "Adresse E-mail", enterEmail: "Entrez votre e-mail", phone: "Numéro de Téléphone", product: "Produit dont vous avez besoin", message: "Décrivez vos exigences en détail", enterMessage: "Entrez votre message", sendRequest: "Envoyer la Demande" },
        footer: { desc: "Agent professionnel d'approvisionnement chinois aidant les entreprises du monde entier à trouver des fournisseurs fiables et des produits de qualité à des prix compétitifs.", quickLinks: "Liens Rapides", services: "Nos Services", contact: "Nous Contacter" },
        login: { title: "Connexion Administrateur", username: "Nom d'Utilisateur", enterUsername: "Entrez le nom d'utilisateur", password: "Mot de Passe", enterPassword: "Entrez le mot de passe", error: "Nom d'utilisateur ou mot de passe incorrect!", cancel: "Annuler", submit: "Se Connecter" },
        quote: { title: "Demander un Devis", quantity: "Quantité Requise", enterQuantity: "Entrez la quantité", cancel: "Annuler", send: "Envoyer la Demande de Devis" },
        detail: { back: "Retour aux Produits", edit: "Modifier", preview: "Aperçu", saving: "Enregistrement...", saved: "Enregistré", error: "Échec d'enregistrement" },
        aplus: { title: "Contenu A+", addBlock: "Ajouter un bloc :", blockHero: "Bannière", blockText: "Texte", blockTextImage: "Texte + Image", blockImageText: "Image + Texte", blockFeatures: "Grille de fonctionnalités", placeholderHeading: "Cliquez pour modifier le titre", placeholderText: "Cliquez pour modifier...", placeholderFeature: "Caractéristique", confirmDelete: "Supprimer ce bloc?" },
        logo: { title: "Mettre à jour le logo", tip: "Le logo s'affiche dans un conteneur 50x50. Téléchargez une image carrée ou collez une URL.", uploadFile: "Télécharger", imageUrl: "Ou URL d'image", reset: "Réinitialiser", cancel: "Annuler", save: "Enregistrer" },
        advantages: { eyebrow: "Pourquoi Nous Choisir", title: "Nos Avantages Clés", subtitle: "Ce qui fait de Yeatru votre meilleur partenaire d'approvisionnement en Chine", lowMOQ: "Support MOQ Faible", lowMOQDesc: "Commencez par de petites commandes. Nous vous mettons en relation avec des fournisseurs offrant une MOQ flexible, idéale pour les startups et les petites entreprises.", oneStop: "Approvisionnement Intégré en Chine", oneStopDesc: "De la recherche de fournisseurs au contrôle qualité et à l'expédition — nous gérons l'ensemble du processus d'approvisionnement pour vous.", oem: "OEM et Marque Privée", oemDesc: "Personnalisez les produits avec le logo, l'emballage et le design de votre marque. Échantillons professionnels en 3-7 jours.", fastSample: "Production Rapide d'Échantillons", fastSampleDesc: "Obtenez rapidement des échantillons professionnels pour vérifier la qualité avant la production de masse. Les frais d'échantillon sont remboursables avec les commandes en gros.", strictQC: "Inspection QC Stricte", strictQCDesc: "Inspections de qualité AQL 2.5 à chaque étape. Nous nous assurons que les produits répondent à vos spécifications avant expédition.", global: "Livraison Porte à Porte Mondiale", globalDesc: "Stockage gratuit, consolidation des marchandises et tarifs d'expédition compétitifs partout dans le monde." },
        banner: { slide1Tag: "14+ Ans d'Expérience · 200+ Clients Mondiaux", slide1Title: "Commencez à Vous Approvisionner en Chine Aujourd'hui — À Partir de 50 Pièces MOQ", slide1Subtitle: "Rejoignez plus de 200 vendeurs mondiaux qui ont réduit leurs coûts d'approvisionnement de 30%+. Nous gérons la vérification des fournisseurs, le contrôle qualité et l'expédition — vous concentrez sur la croissance de vos ventes.", slide1Feat1: "MOQ 50 Pièces", slide1Feat2: "Devis en 24h", slide1Feat3: "Zéro Risque", slide1Btn1: "Obtenir un Devis Gratuit Maintenant", slide1Btn2: "Voir les Produits", slide2Tag: "Construisez Votre Identité de Marque", slide2Title: "Logo Personnalisé, Emballage & Design — Expédition en 7 Jours", slide2Subtitle: "Distinguez-vous de la concurrence avec des produits de marque personnalisée. Consultation design gratuite incluse — pas de frais cachés, tarification transparente dès le premier jour.", slide2Feat1: "Support Design Gratuit", slide2Feat2: "Échantillon en 7 Jours", slide2Feat3: "MOQ Bas 200pcs", slide2Btn1: "Commencer le Design Personnalisé", slide2Btn2: "Voir Services OEM", slide3Tag: "Logistique Mondiale", slide3Title: "Drop Shipping & Consolidation d'Entrepôts Mondiaux", slide3Subtitle: "Expédiez directement à vos clients du monde entier. Nous offrons un stockage gratuit, une consolidation des marchandises et des tarifs d'expédition porte à porte compétitifs.", slide3Feat1: "Stockage Gratuit", slide3Feat2: "Livraison Porte à Porte", slide3Feat3: "Couverture Mondiale", slide3Btn1: "Obtenir un Devis Gratuit", slide3Btn2: "En Savoir Plus" },
        common: { getQuote: "Obtenir un Devis", getFreeQuote: "Obtenir un Devis Gratuit", contactUs: "Nous Contacter", viewProducts: "Voir les Produits", viewAll: "Voir Tout", learnMore: "En Savoir Plus", browseAll: "Parcourir Tous les Produits", startSourcing: "Commencez Votre Approvisionnement", chatWithUs: "Discutez Avec Nous", sendRequest: "Envoyer la Demande", viewAllArticles: "Voir Tous les Articles", readArticle: "Lire l'article", popularCategories: "Catégories Populaires", hotProducts: "Produits les Plus Vendus", hotProductsSubtitle: "Découvrez nos catégories de produits les plus populaires auprès de fournisseurs fiables", whatWeOffer: "Ce Que Nous Offrons", oneStopServices: "Services d'Approvisionnement Intégrés", howItWorks: "Comment Ça Marche", simpleProcess: "Processus d'Approvisionnement Simple en 4 Étapes", simpleProcessSubtitle: "De la demande à la livraison, nous simplifions l'approvisionnement depuis la Chine", sendRequirements: "Envoyer les Exigences", sendRequirementsDesc: "Dites-nous vos besoins en produits, quantité, budget et délai. Nous trouverons les meilleurs fournisseurs pour vous.", sourceQuote: "Recherche et Devis", sourceQuoteDesc: "Nous identifions des fournisseurs vérifiés, négocions les prix et vous envoyons des devis détaillés avec échantillons.", sampleConfirm: "Confirmation d'Échantillon", sampleConfirmDesc: "Revoyez les échantillons, confirmez la qualité et finalisez les détails de votre commande avant la production de masse.", productionShip: "Production et Expédition", productionShipDesc: "Nous supervisons la production, l'inspection QC, la consolidation et expédions directement à votre porte.", faq: "FAQ", faqSubtitle: "Réponses rapides aux questions courantes sur nos services d'approvisionnement", all: "Tout", stillQuestions: "Vous avez encore des questions?", clientStories: "Histoires de Clients", trustedBy: "La Confiance des Acheteurs Mondiaux", trustedBySubtitle: "Retours d'expérience réels de vendeurs Amazon, détaillants locaux et grossistes du monde entier", sourcingKnowledge: "Connaissance en Approvisionnement", sourcingInsights: "Conseils et Idées sur l'Approvisionnement en Chine", sourcingInsightsSubtitle: "Guides pratiques pour vous aider à vous approvisionner plus intelligemment et à développer votre entreprise", globalClients: "Clients Mondiaux", countriesServed: "Pays Desservis", clientSatisfaction: "Satisfaction Client", supportAvailable: "Support Disponible", minRead: "min de lecture", aboutUs: "À Propos de Nous", contactUsTitle: "Nous Contacter", searchPlaceholder: "Rechercher produits, services, guides...", inquirySub: "Choisissez votre canal préféré" },
        footer: { desc: "Agent professionnel d'approvisionnement chinois aidant les entreprises du monde entier à trouver des fournisseurs fiables et des produits de qualité à des prix compétitifs.", quickLinks: "Liens Rapides", services: "Nos Services", contact: "Nous Contacter", paymentMethods: "Méthodes de Paiement", privacyPolicy: "Politique de Confidentialité", termsOfService: "Conditions d'Utilisation", allRightsReserved: "Tous droits réservés." },
        aboutPage: { heroTag: "À Propos de Nous", heroTitle: "Votre Partenaire de Confiance en Approvisionnement en Chine", heroSubtitle: "Fondés à Yiwu — le plus grand marché de petites marchandises du monde — nous mettons en relation les acheteurs mondiaux avec des fabricants chinois fiables.", feat1: "Plus de 14 Ans d'Expérience Combinée", feat2: "Plus de 200 Clients Mondiaux", feat3: "Plus de 50 Pays Desservis", btnContact: "Nous Contacter", btnLearnMore: "En Savoir Plus", storyEyebrow: "Notre Histoire", storyTitle: "De Yiwu au Monde", storySubtitle: "Fondés Là Où Sont Fabriqués les Meilleurs Produits du Monde", storyPara1: "Yeatru Sourcing a été fondée à Yiwu, dans la province du Zhejiang — siège de la Ville Commerciale Internationale de Yiwu, le plus grand marché de gros de petites marchandises du monde avec plus de 75 000 stands et des produits dans 26 catégories.", storyPara2: "Notre équipe fondatrice apporte plus de 14 ans d'expérience combinée dans la fabrication en Chine, la gestion de fournisseurs, le contrôle qualité et la logistique internationale. Nous avons aidé des vendeurs Amazon FBA à lancer des produits de marque privée, des détaillants locaux à s'approvisionner en inventaire compétitif et des acheteurs grossistes à établir des partenariats à long terme avec des fournisseurs.", storyPara3: "Notre mission est simple : rendre l'approvisionnement depuis la Chine transparent, abordable et sans risque — une commande à la fois.", valuesEyebrow: "Nos Valeurs", valuesTitle: "Ce Qui Nous Anime", transparency: "Transparence", transparencyDesc: "Détails complets des coûts, pas de frais cachés et communication honnête à chaque étape. Vous saurez toujours où va votre argent.", integrity: "Intégrité", integrityDesc: "Nous agissons dans votre intérêt — pas dans celui de l'usine. Confidentialité signée NDA, pas de commissions des fournisseurs sur votre commande.", verification: "Vérification d'Abord", verificationDesc: "Nous ne prenons pas de risques avec votre entreprise. Chaque fournisseur que nous recommandons a été examiné, visité ou audité par notre équipe.", results: "Axé sur les Résultats", resultsDesc: "Nous mesurons le succès par vos résultats : coûts réduits, meilleure qualité, livraison plus rapide. Votre croissance est notre croissance.", whyEyebrow: "Pourquoi Yeatru", whyTitle: "Ce Qui Nous Rend Différents", statClients: "Clients Mondiaux", statCountries: "Pays Desservis", statYears: "Années d'Expérience Combinée", statFactories: "Réseau d'Usines", whyHeading: "Expertise Locale, Normes Mondiales", whyPara1: "Nous combinons une connaissance approfondie du marché local avec des normes commerciales internationales. Notre équipe parle anglais, mandarin et espagnol. Nous comblons le fossé entre les usines chinoises et les acheteurs mondiaux.", whyPara2: "Contrairement aux sociétés commerciales, nous ne majorons pas les prix des produits. Notre structure tarifaire est transparente — et notre motivation est alignée sur la vôtre : de meilleurs résultats signifient plus d'affaires récurrentes.", servicesEyebrow: "Ce Que Nous Faisons", servicesTitle: "Services d'Approvisionnement de Bout en Bout", faqEyebrow: "Questions Courantes", faqTitle: "Travailler avec Yeatru", faq1Q: "Avec quels types d'acheteurs travaillez-vous?", faq1A: "Nous servons les vendeurs Amazon FBA, les vendeurs TikTok Shop, les détaillants locaux, les distributeurs grossistes et les entrepreneurs e-commerce. Des importateurs débutants aux marques établies qui développent leur chaîne d'approvisionnement en Chine.", faq2Q: "En quoi Yeatru est-il différent d'une société commerciale?", faq2A: "Les sociétés commerciales majorent les prix des produits de 15 à 30% au-dessus du coût d'usine. Nous facturons des frais forfaitaires ou un pourcentage transparent — et nos frais sont divulgués à l'avance. Vous obtenez toujours le prix direct usine.", faq3Q: "Travaillez-vous avec de petites commandes?", faq3A: "Oui. Nous sommes conçus pour les acheteurs petits et moyens. Beaucoup de nos fournisseurs acceptent des MOQ aussi basses que 50-100 pièces. Nous vous aidons à commencer petit et à évoluer.", faq4Q: "Que se passe-t-il si un fournisseur ne livre pas?", faq4A: "Nous médions entre vous et le fournisseur. Si le fournisseur est en faute, nous négocions une compensation, cherchons des usines alternatives et couvrons la différence de coûts le cas échéant dans le cadre de notre garantie de service.", faq5Q: "Comment commencer?", faq5A: "Le moyen le plus simple : envoyez-nous vos exigences en produits via notre formulaire de contact ou WhatsApp. Nous vous répondrons en 4 heures avec des devis initiaux et un plan d'approvisionnement.", ctaEyebrow: "Travaillons Ensemble", ctaTitle: "Commencez Votre Parcours d'Approvisionnement Aujourd'hui", ctaSubtitle: "Aucun engagement. Obtenez une consultation gratuite et un devis initial en 24 heures.", ctaBtn: "Nous Contacter Maintenant" },
        contactPage: { heroTag: "Nous Contacter", heroTitle: "Prenez Contact Avec Nous", heroSubtitle: "Vous avez une question ou êtes prêt à démarrer votre projet d'approvisionnement? Nous sommes là pour vous aider 24h/24 et 7j/7.", heroFeat1: "Support 24h/24 et 7j/7", heroFeat2: "Réponse en 4 Heures", heroFeat3: "Consultation Gratuite", infoEyebrow: "Informations de Contact", infoTitle: "Plusieurs Façons de Nous Contacter", infoSubtitle: "Choisissez votre canal préféré — nous répondons rapidement", instantMsg: "Messagerie Instantanée", officialEmail: "E-mail Officiel", phoneSupport: "Support Téléphonique", ourOffice: "Notre Bureau", quoteEyebrow: "Demander un Devis", quoteTitle: "Dites-Nous Ce Dont Vous Avez Besoin", quoteSubtitle: "Remplissez le formulaire ci-dessous et nous vous répondrons en 4 heures", statYears: "Années d'Expérience", statClients: "Clients Mondiaux", statCountries: "Pays Desservis", statSatisfaction: "Satisfaction" }
    }},
    ru: { translation: {
        nav: { home: "Главная", products: "Продукты", services: "Услуги", sourcingProcess: "Процесс Поставок", testimonials: "Отзывы", aboutUs: "О Нас", contactUs: "Связаться", login: "Войти", logout: "Выйти", servicePlans: "Тарифы", payment: "Оплата", blog: "Блог", oem: "OEM Кастомизация", sampleOrder: "Заказ Образца", factoryAudit: "Аудит Фабрики" },
        hero: { title: "Профессиональный Агент По Поставкам Из Китая Ивю", desc: "Комплексное решение по поставкам из Китая.", contactBtn: "Связаться Сейчас", productsBtn: "Посмотреть Продукты" },
        products: { title: "Популярные Продукты", subtitle: "Изучите наши рекомендуемые продукты из Китая", categoryManagement: "Управление Категориями", enterCategory: "Введите название", addCategory: "Добавить", addProduct: "Добавить Продукт", imageUrl: "URL Изображения", enterImageUrl: "Введите URL", category: "Категория", selectCategory: "Выберите", name: "Название", enterName: "Введите название", sku: "Артикул", enterSKU: "Введите артикул", material: "Материал", enterMaterial: "Введите материал", size: "Размер", enterSize: "Введите размер", moq: "MOQ", enterMOQ: "Введите MOQ", priceMin: "Мин. Цена ($)", enterMinPrice: "Введите мин. цену", priceMax: "Макс. Цена ($)", enterMaxPrice: "Введите макс. цену", description: "Описание", enterDescription: "Введите описание", cancel: "Отмена", save: "Сохранить", edit: "Редактировать", delete: "Удалить", quote: "Получить Котировку", price: "Цена: $", viewDetails: "Подробнее" },
        filter: { title: "Фильтр по Категории", all: "Все", reset: "Сбросить", showing: "Показано", of: "из", products: "продуктов", noResult: "Нет продуктов в этой категории" },
        services: { title: "Наши Услуги По Поставкам", subtitle: "Комплексные решения по поставкам", supplierVerification: "Проверка Поставщиков", supplierVerificationDesc: "Тщательная проверка поставщиков.", productSourcing: "Поиск Продуктов", productSourcingDesc: "Найдите нужные продукты.", qualityControl: "Контроль Качества", qualityControlDesc: "Контроль качества на каждом этапе.", logistics: "Логистика и Склад", logisticsDesc: "Комплексные решения логистики и хранения с бесплатным хранением.", priceNegotiation: "Переговоры По Ценам", priceNegotiationDesc: "Лучшие цены.", designPhotography: "Дизайн и Фотография", designPhotographyDesc: "Профессиональная фотография и дизайн для продаж." },
        process: { title: "Наш Процесс Поставок", subtitle: "Простой и прозрачный процесс", step1: "Ваши Требования", step1Desc: "Поделитесь спецификациями.", step2: "Подбор Поставщиков", step2Desc: "Подбираем лучших поставщиков.", step3: "Образцы и Цены", step3Desc: "Образцы и цены.", step4: "Доставка и Поддержка", step4Desc: "Контроль производства и доставка." },
        testimonials: { title: "Отзывы Клиентов", subtitle: "Отзывы наших покупателей", review1: "\"Отличное качество и быстрая доставка!\"", review2: "\"Профессиональная команда.\"", review3: "\"Сэкономил 20%!\"" },
        about: { title: "О Yeatru Sourcing", profile: "Профиль Компании", profileDesc: "Yeatru Sourcing — профессиональный агент по поставкам в Ивю." },
        contact: { getInTouch: "Свяжитесь С Нами", desc: "Готовы начать?", requestQuote: "Запросить Котировку", yourName: "Ваше Имя", enterName: "Введите имя", email: "Email", enterEmail: "Введите email", phone: "Телефон", product: "Нужный продукт", message: "Опишите требования", enterMessage: "Введите сообщение", sendRequest: "Отправить" },
        footer: { desc: "Профессиональный агент по поставкам из Китая.", quickLinks: "Ссылки", services: "Услуги", contact: "Контакты" },
        login: { title: "Вход", username: "Логин", enterUsername: "Введите логин", password: "Пароль", enterPassword: "Введите пароль", error: "Неверные данные!", cancel: "Отмена", submit: "Войти" },
        quote: { title: "Котировка", quantity: "Количество", enterQuantity: "Введите кол-во", cancel: "Отмена", send: "Отправить" },
        detail: { back: "Назад", edit: "Редактировать", preview: "Просмотр", saving: "Сохранение...", saved: "Сохранено", error: "Ошибка" },
        aplus: { title: "Контент A+", addBlock: "Добавить блок:", blockHero: "Баннер", blockText: "Текст", blockTextImage: "Текст + Изображение", blockImageText: "Изображение + Текст", blockFeatures: "Сетка функций", placeholderHeading: "Заголовок", placeholderText: "Текст...", placeholderFeature: "Особенность", confirmDelete: "Удалить блок?" },
        logo: { title: "Обновить логотип", tip: "50x50.", uploadFile: "Загрузить", imageUrl: "URL", reset: "Сброс", cancel: "Отмена", save: "Сохранить" },
        advantages: { eyebrow: "Почему Мы", title: "Наши Преимущества", subtitle: "Почему Yeatru — лучший партнёр по поставкам из Китая", lowMOQ: "Низкая MOQ", lowMOQDesc: "Начните с небольших заказов. Поставщики с гибкой MOQ для стартапов и малого бизнеса.", oneStop: "Комплексные Поставки", oneStopDesc: "От подбора поставщиков до контроля качества и доставки — ведём весь процесс.", oem: "OEM и Частная Марка", oemDesc: "Кастомизация продукции с вашим логотипом, упаковкой и дизайном. Образцы за 3-7 дней.", fastSample: "Быстрые Образцы", fastSampleDesc: "Профессиональные образцы для проверки качества. Стоимость возвращается при оптовом заказе.", strictQC: "Строгий Контроль Качества", strictQCDesc: "Инспекции AQL 2.5 на всех этапах. Гарантия соответствия спецификациям.", global: "Международная Доставка", globalDesc: "Бесплатное хранение, консолидация грузов и выгодные тарифы по всему миру." },
        banner: { slide1Tag: "14+ лет опыта · 200+ клиентов в мире", slide1Title: "Начните поставки из Китая сегодня — от 50 штук MOQ", slide1Subtitle: "Присоединяйтесь к 200+ продавцам, сократившим расходы на 30%+. Мы проверяем поставщиков, контролируем качество и доставляем — вы растите продажи.", slide1Feat1: "MOQ от 50 шт", slide1Feat2: "Расчёт за 24ч", slide1Feat3: "Без риска", slide1Btn1: "Бесплатный расчёт сейчас", slide1Btn2: "Смотреть товары", slide2Tag: "Создайте свой бренд", slide2Title: "Логотип, упаковка и дизайн — отправка за 7 дней", slide2Subtitle: "Выделитесь среди конкурентов с продукцией под вашей маркой. Бесплатная консультация по дизайну — без скрытых платежей.", slide2Feat1: "Бесплатный дизайн", slide2Feat2: "Образец за 7 дней", slide2Feat3: "MOQ от 200 шт", slide2Btn1: "Начать кастомизацию", slide2Btn2: "Услуги OEM", slide3Tag: "Глобальная Логистика", slide3Title: "Дропшиппинг и консолидация грузов", slide3Subtitle: "Доставка напрямую вашим клиентам по всему миру. Бесплатное хранение и выгодные тарифы.", slide3Feat1: "Бесплатное хранение", slide3Feat2: "Доставка до двери", slide3Feat3: "Глобальное покрытие", slide3Btn1: "Бесплатный расчёт", slide3Btn2: "Подробнее" },
        common: { getQuote: "Рассчитать", getFreeQuote: "Бесплатный расчёт", contactUs: "Связаться", viewProducts: "Смотреть товары", viewAll: "Смотреть все", learnMore: "Подробнее", browseAll: "Все товары", startSourcing: "Начать поставки", chatWithUs: "Написать нам", sendRequest: "Отправить заявку", viewAllArticles: "Все статьи", readArticle: "Читать статью", popularCategories: "Популярные категории", hotProducts: "Хиты продаж", hotProductsSubtitle: "Наши самые популярные категории товаров от проверенных поставщиков", whatWeOffer: "Что мы предлагаем", oneStopServices: "Комплексные услуги", howItWorks: "Как это работает", simpleProcess: "Простой 4-шаговый процесс", simpleProcessSubtitle: "От запроса до доставки — делаем поставки из Китая простыми", sendRequirements: "Отправить требования", sendRequirementsDesc: "Расскажите о нужных товарах, количестве, бюджете и сроках. Подберём лучших поставщиков.", sourceQuote: "Подбор и расчёт", sourceQuoteDesc: "Находим проверенных поставщиков, договариваемся о ценах, отправляем детальные расчёты с образцами.", sampleConfirm: "Подтверждение образцов", sampleConfirmDesc: "Проверка образцов, подтверждение качества и согласование деталей перед массовым производством.", productionShip: "Производство и доставка", productionShipDesc: "Контролируем производство, проводим инспекции, консолидируем грузы и доставляем до двери.", faq: "FAQ", faqSubtitle: "Ответы на часто задаваемые вопросы о наших услугах", all: "Все", stillQuestions: "Остались вопросы?", clientStories: "Истории клиентов", trustedBy: "Нам доверяют покупатели", trustedBySubtitle: "Реальные отзывы продавцов Amazon, розничных продавцов и оптовиков", sourcingKnowledge: "Знания о поставках", sourcingInsights: "Советы по поставкам из Китая", sourcingInsightsSubtitle: "Практические руководства для умных закупок и роста бизнеса", globalClients: "Клиенты по всему миру", countriesServed: "Стран обслуживания", clientSatisfaction: "Удовлетворённость клиентов", supportAvailable: "Поддержка 24/7", minRead: "мин чтения", aboutUs: "О нас", contactUsTitle: "Контакты", searchPlaceholder: "Поиск продуктов, услуг, руководств...", inquirySub: "Выберите предпочтительный канал" },
        footer: { desc: "Профессиональный агент по поставкам из Китая. Помогаем бизнесу находить надёжных поставщиков и качественные товары по выгодным ценам.", quickLinks: "Быстрые ссылки", services: "Услуги", contact: "Контакты", paymentMethods: "Способы оплаты", privacyPolicy: "Политика конфиденциальности", termsOfService: "Условия обслуживания", allRightsReserved: "Все права защищены." },
        aboutPage: { heroTag: "О нас", heroTitle: "Ваш надёжный партнёр по поставкам из Китая", heroSubtitle: "Основаны в Ивю — крупнейшем рынке мелких товаров мира. Связываем покупателей с надёжными китайскими производителями.", feat1: "Более 14 лет опыта", feat2: "Более 200 клиентов", feat3: "Более 50 стран", btnContact: "Связаться", btnLearnMore: "Подробнее", storyEyebrow: "Наша история", storyTitle: "Из Ивю в мир", storySubtitle: "Основаны там, где производят лучшие товары мира", storyPara1: "Yeatru Sourcing основана в Ивю, провинция Чжэцзян — городе с крупнейшим в мире оптовым рынком мелких товаров: более 75 000 торговых точек, 26 категорий продукции.", storyPara2: "Наша команда имеет более 14 лет совокупного опыта в производстве, управлении поставщиками, контроле качества и международной логистике. Мы помогали продавцам Amazon FBA запускать частные марки, розничным продавцам — выгодно закупать товары, оптовикам — строить долгосрочные партнёрства.", storyPara3: "Наша миссия проста: сделать поставки из Китая прозрачными, доступными и безопасными — один заказ за раз.", valuesEyebrow: "Наши ценности", valuesTitle: "Во что мы верим", transparency: "Прозрачность", transparencyDesc: "Полная детализация расходов, без скрытых комиссий, честная связь на каждом этапе. Вы всегда знаете, куда уходят деньги.", integrity: "Честность", integrityDesc: "Мы действуем в ваших интересах, а не в интересах фабрики. Конфиденциальность по NDA, без комиссий от поставщиков.", verification: "Проверка прежде всего", verificationDesc: "Мы не рискуем вашим бизнесом. Каждый рекомендуемый поставщик прошёл проверку нашей командой.", results: "Результативность", resultsDesc: "Мы измеряем успех вашими результатами: снижение затрат, улучшение качества, ускорение доставки. Ваш рост — наш рост.", whyEyebrow: "Почему Yeatru", whyTitle: "Чем мы отличаемся", statClients: "Клиентов в мире", statCountries: "Стран обслуживания", statYears: "Лет опыта", statFactories: "Сеть фабрик", whyHeading: "Местная экспертиза, мировые стандарты", whyPara1: "Мы сочетаем глубокое знание местного рынка с международными стандартами бизнеса. Наша команда говорит по-английски, по-китайски и по-испански. Мы мост между китайскими фабриками и покупателями со всего мира.", whyPara2: "В отличие от торговых компаний, мы не накручиваем цены на товары. Наша тарифная структура прозрачна — и наши стимулы совпадают с вашими: лучшие результаты = больше повторных заказов.", servicesEyebrow: "Что мы делаем", servicesTitle: "Комплексные услуги поставок", faqEyebrow: "Частые вопросы", faqTitle: "О работе с Yeatru", faq1Q: "С какими покупателями вы работаете?", faq1A: "Мы работаем с продавцами Amazon FBA и TikTok Shop, розничными продавцами, оптовыми дистрибьюторами и предпринимателями e-commerce. От новичков до развитых брендов, расширяющих цепочку поставок в Китае.", faq2Q: "Чем Yeatru отличается от торговой компании?", faq2A: "Торговые компании накручивают цены на 15-30% сверх фабричной стоимости. Мы берём прозрачный фиксированный сбор или процент — и сразу озвучиваем его. Вы всегда получаете прямую фабричную цену.", faq3Q: "Работаете ли вы с мелкими заказами?", faq3A: "Да. Мы ориентированы на малых и средних покупателей. Многие наши поставщики принимают MOQ от 50-100 штук. Помогаем начинать с малого и масштабироваться.", faq4Q: "Что если поставщик не выполнит доставку?", faq4A: "Мы выступаем посредником между вами и поставщиком. Если виноват поставщик — договариваемся о компенсации, ищем альтернативные фабрики и покрываем разницу в расходах при наличии гарантийного случая.", faq5Q: "Как начать работу?", faq5A: "Проще всего: отправьте требования к товарам через форму контактов или WhatsApp. Ответим в течение 4 часов с начальными расчётами и планом поставок.", ctaEyebrow: "Давайте работать вместе", ctaTitle: "Начните путь поставок сегодня", ctaSubtitle: "Без обязательств. Получите бесплатную консультацию и начальный расчёт за 24 часа.", ctaBtn: "Связаться сейчас" },
        contactPage: { heroTag: "Контакты", heroTitle: "Свяжитесь с нами", heroSubtitle: "Есть вопросы или готовы начать проект? Мы на связи 24/7.", heroFeat1: "Поддержка 24/7", heroFeat2: "Ответ за 4 часа", heroFeat3: "Бесплатная консультация", infoEyebrow: "Контактная информация", infoTitle: "Способы связи", infoSubtitle: "Выберите удобный канал — отвечаем быстро", instantMsg: "Мессенджеры", officialEmail: "Официальная почта", phoneSupport: "Телефонная поддержка", ourOffice: "Наш офис", quoteEyebrow: "Запросить расчёт", quoteTitle: "Расскажите, что вам нужно", quoteSubtitle: "Заполните форму — ответим в течение 4 часов", statYears: "Лет опыта", statClients: "Клиентов в мире", statCountries: "Стран обслуживания", statSatisfaction: "Удовлетворённость" }
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

const EXCHANGE_RATES = {
    USD: { rate: 1, symbol: '$', name: 'USD' },
    EUR: { rate: 0.92, symbol: '€', name: 'EUR' },
    GBP: { rate: 0.79, symbol: '£', name: 'GBP' },
    RUB: { rate: 92.5, symbol: '₽', name: 'RUB' },
    CNY: { rate: 7.25, symbol: '¥', name: 'CNY' }
};

let currentCurrency = 'USD';

function getCurrentCurrency() {
    return localStorage.getItem('yeatru_currency') || 'USD';
}

function formatPrice(usdPrice) {
    const currency = getCurrentCurrency();
    const cfg = EXCHANGE_RATES[currency] || EXCHANGE_RATES.USD;
    const converted = (usdPrice * cfg.rate).toFixed(2);
    return cfg.symbol + converted;
}

function initCurrencySelector() {
    const currencyItems = document.querySelectorAll('[data-currency]');
    const currentCurrencyEl = document.getElementById('current-currency');
    const saved = getCurrentCurrency();
    currentCurrency = saved;

    if (currentCurrencyEl) {
        currentCurrencyEl.textContent = saved;
    }

    currencyItems.forEach(item => {
        item.addEventListener('click', function(e) {
            e.preventDefault();
            const currency = this.dataset.currency;
            localStorage.setItem('yeatru_currency', currency);
            currentCurrency = currency;
            if (currentCurrencyEl) {
                currentCurrencyEl.textContent = currency;
            }
            document.dispatchEvent(new CustomEvent('currencyChanged', { detail: { currency } }));
            renderProducts();
            renderIndexHotProducts();
        });
    });
}

function safeAddEventListener(id, event, handler) {
    const el = document.getElementById(id);
    if (el) el.addEventListener(event, handler);
}

document.addEventListener('DOMContentLoaded', function () {
    console.log('[i18n] DOMContentLoaded fired, starting i18next init...');
    
    try {
        i18next
            .use(i18nextBrowserLanguageDetector)
            .init({
                fallbackLng: 'en',
                resources: translationResources,
                supportedLngs: ['en', 'es', 'fr', 'ru'],
                nonExplicitSupportedLngs: false,
                detection: {
                    order: ['querystring', 'cookie', 'localStorage', 'navigator', 'htmlTag'],
                    caches: ['localStorage', 'cookie']
                },
                interpolation: { escapeValue: false }
            }).then(function () {
                console.log('[i18n] i18next initialized successfully');
                console.log('[i18n] Current language:', i18next.language);
                updateContent();
                bindLanguageEvents();
                loadRemoteSiteData();
                updateLoginUI(isAdmin());
            }).catch(function (err) {
                console.error('[i18n] i18next init error:', err);
                updateLoginUI(isAdmin());
            });
    } catch (e) {
        console.error('[i18n] Exception during i18next setup:', e);
    }

    try {
        initCurrencySelector();
        renderBrandLogo();
        renderProductsDropdown();
        renderIndexCategories();
        renderIndexHotProducts();
        renderCategories();
        renderProducts();
    } catch (e) {
        console.error('[init] Error during initial render:', e);
    }

    safeAddEventListener('submitLogin', 'click', function () {
        const username = document.getElementById('adminUsername').value.trim();
        const password = document.getElementById('adminPassword').value.trim();
        const errorEl = document.getElementById('loginError');
        if (username === 'Yeatru' && password === 'Ldz52385109') {
            localStorage.setItem('yeatruAdminLoggedIn', 'true');
            updateLoginUI(true);
            const loginModal = document.getElementById('loginModal');
            if (loginModal) {
                const modalInstance = bootstrap.Modal.getInstance(loginModal) || new bootstrap.Modal(loginModal);
                modalInstance.hide();
            }
            if (errorEl) errorEl.classList.add('d-none');
            const adminUser = document.getElementById('adminUsername');
            const adminPass = document.getElementById('adminPassword');
            if (adminUser) adminUser.value = '';
            if (adminPass) adminPass.value = '';
        } else {
            if (errorEl) errorEl.classList.remove('d-none');
        }
    });

    safeAddEventListener('authBtn', 'click', function () {
        if (this.classList.contains('logged-in')) {
            localStorage.removeItem('yeatruAdminLoggedIn');
            updateLoginUI(false);
            const detailPage = document.getElementById('productDetailPage');
            if (detailPage && detailPage.classList.contains('active') && currentDetailMode === 'edit') {
                setDetailMode('preview');
            }
        }
    });

    safeAddEventListener('closeExportPanel', 'click', function () {
        const panel = document.getElementById('adminExportPanel');
        if (panel) panel.classList.add('d-none');
    });

    safeAddEventListener('addCategoryBtn', 'click', function () {
        const newCatInput = document.getElementById('newCategory');
        if (!newCatInput) return;
        const newCategory = newCatInput.value.trim();
        if (newCategory && !getCategories().includes(newCategory)) {
            saveCategories([...getCategories(), newCategory]);
            newCatInput.value = '';
        }
    });

    safeAddEventListener('addVariationBtn', 'click', function () {
        addVariationItem();
    });

    safeAddEventListener('addDetailVariationBtn', 'click', function () {
        addDetailVariationItem();
    });

    safeAddEventListener('saveProduct', 'click', function () {
        const productIdEl = document.getElementById('productId');
        if (!productIdEl) return;
        const productId = productIdEl.value;
        const variations = collectVariations();
        let priceMin = null;
        let priceMax = null;
        const pricedVariations = variations.filter(v => v.price !== null && v.price !== undefined && !isNaN(v.price));
        if (pricedVariations.length > 0) {
            const prices = pricedVariations.map(v => v.price);
            priceMin = Math.min(...prices);
            priceMax = Math.max(...prices);
        } else {
            priceMin = 1;
            priceMax = 1;
        }
        const product = {
            id: productId ? parseInt(productId) : Date.now(),
            image: document.getElementById('productImage') ? document.getElementById('productImage').value : '',
            category: document.getElementById('productCategory') ? document.getElementById('productCategory').value : '',
            name: document.getElementById('productName') ? document.getElementById('productName').value : '',
            sku: document.getElementById('productSKU') ? document.getElementById('productSKU').value : '',
            material: document.getElementById('productMaterial') ? document.getElementById('productMaterial').value : '',
            size: document.getElementById('productSize') ? document.getElementById('productSize').value : '',
            moq: document.getElementById('productMOQ') ? parseInt(document.getElementById('productMOQ').value) : 0,
            priceMin: priceMin,
            priceMax: priceMax,
            description: document.getElementById('productDescription') ? document.getElementById('productDescription').value : '',
            variations: variations
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
        if (productModal) {
            bootstrap.Modal.getInstance(productModal).hide();
        }
        const productForm = document.getElementById('productForm');
        if (productForm) productForm.reset();
        const variationsContainer = document.getElementById('variationsContainer');
        if (variationsContainer) variationsContainer.innerHTML = '';
        if (productIdEl) productIdEl.value = '';
        const modalLabel = document.getElementById('productModalLabel');
        if (modalLabel) modalLabel.textContent = tt('products.addProduct', 'Add New Product');
    });

    safeAddEventListener('addProductBtn', 'click', function () {
        const productForm = document.getElementById('productForm');
        if (productForm) productForm.reset();
        const productIdEl = document.getElementById('productId');
        if (productIdEl) productIdEl.value = '';
        const variationsContainer = document.getElementById('variationsContainer');
        if (variationsContainer) variationsContainer.innerHTML = '';
        const modalLabel = document.getElementById('productModalLabel');
        if (modalLabel) modalLabel.textContent = tt('products.addProduct', 'Add New Product');
    });

    safeAddEventListener('exportDataBtn', 'click', exportSiteData);
    safeAddEventListener('importDataBtn', 'click', function () {
        const importFile = document.getElementById('importDataFile');
        if (importFile) importFile.click();
    });
    safeAddEventListener('importDataFile', 'change', importSiteDataFromFile);

    safeAddEventListener('detailBackBtn', 'click', function () {
        hideDetailPage();
    });

    document.querySelectorAll('#detailModeToggle button').forEach(b => {
        b.addEventListener('click', function () {
            setDetailMode(this.getAttribute('data-mode'));
        });
    });

    safeAddEventListener('detailQuoteBtn', 'click', function () {
        if (!currentDetailProductId) return;
        const p = getProducts().find(x => x.id === currentDetailProductId);
        if (!p) return;
        const quoteProductName = document.getElementById('quoteProductName');
        if (quoteProductName) quoteProductName.value = p.name;
        const quoteModal = document.getElementById('quoteModal');
        if (quoteModal) new bootstrap.Modal(quoteModal).show();
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

    safeAddEventListener('brandLogoEdit', 'click', function (e) {
        e.preventDefault();
        e.stopPropagation();
        if (!isAdmin()) return;
        const logoUrlInput = document.getElementById('logoUrlInput');
        if (logoUrlInput) logoUrlInput.value = localStorage.getItem('yeatruBrandLogo') || '';
        const logoModal = document.getElementById('logoModal');
        if (logoModal) new bootstrap.Modal(logoModal).show();
    });
    safeAddEventListener('logoSaveBtn', 'click', saveLogoFromModal);
    safeAddEventListener('logoResetBtn', 'click', function () {
        localStorage.removeItem('yeatruBrandLogo');
        renderBrandLogo();
        const logoModal = document.getElementById('logoModal');
        if (logoModal) bootstrap.Modal.getInstance(logoModal).hide();
    });

    window.addEventListener('hashchange', handleHashRoute);
    handleHashRoute();

    document.querySelectorAll('.nav-item.dropdown > .nav-link').forEach(function(link) {
        link.addEventListener('click', function(e) {
            if (window.innerWidth <= 991) {
                e.preventDefault();
                e.stopPropagation();
                const parent = this.parentElement;
                parent.classList.toggle('show');
            }
        });
    });

    document.addEventListener('click', function(e) {
        if (window.innerWidth <= 991) {
            if (!e.target.closest('.nav-item.dropdown')) {
                document.querySelectorAll('.nav-item.dropdown.show').forEach(function(item) {
                    item.classList.remove('show');
                });
            }
        }
    });
});

function updateContent() {
    console.log('[i18n] Updating content for language:', i18next.language);
    const elements = document.querySelectorAll('[data-i18n]');
    console.log('[i18n] Found', elements.length, 'elements with data-i18n attribute');
    let updatedCount = 0;
    let failedCount = 0;
    elements.forEach((el, index) => {
        const key = el.getAttribute('data-i18n');
        try {
            const v = i18next.t(key);
            if (v && v !== key) {
                el.textContent = v;
                updatedCount++;
            } else {
                if (index < 20) {
                    console.warn('[i18n] No translation for key:', key, 'element:', el.tagName, el.className);
                }
                failedCount++;
            }
        } catch (e) {
            console.error('[i18n] Error translating key:', key, e);
            failedCount++;
        }
    });
    console.log('[i18n] Updated:', updatedCount, 'Failed:', failedCount);
    
    document.querySelectorAll('[data-i18n-placeholder]').forEach(el => {
        const key = el.getAttribute('data-i18n-placeholder');
        try {
            const v = i18next.t(key);
            if (v && v !== key) el.placeholder = v;
        } catch (e) {
            console.error('[i18n] Error translating placeholder key:', key, e);
        }
    });
    const langNames = { en: 'English', es: 'Español', fr: 'Français', ru: 'Русский' };
    const cur = document.getElementById('current-lang');
    if (cur) {
        try {
            cur.textContent = langNames[i18next.language] || 'English';
        } catch (e) {
            console.error('[i18n] Error updating lang indicator:', e);
            cur.textContent = 'English';
        }
    }

    renderCategoryFilter();
    renderProducts();
    renderProductsDropdown();
    const detailPage = document.getElementById('productDetailPage');
    if (detailPage && detailPage.classList.contains('active') && currentDetailProductId) {
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
    const authBtn = document.getElementById('authBtn');
    const addProductBtn = document.getElementById('addProductBtn');
    const categoryManagement = document.getElementById('categoryManagement');
    const brandLogoEdit = document.getElementById('brandLogoEdit');
    const adminExportPanel = document.getElementById('adminExportPanel');
    if (authBtn) {
        authBtn.classList.toggle('logged-in', loggedIn);
        const icon = authBtn.querySelector('i');
        if (loggedIn) {
            if (icon) icon.className = 'fas fa-sign-out-alt';
            authBtn.title = 'Admin Logout';
            authBtn.setAttribute('data-bs-toggle', '');
            authBtn.setAttribute('data-bs-target', '');
        } else {
            if (icon) icon.className = 'fas fa-user-shield';
            authBtn.title = 'Admin Login';
            authBtn.setAttribute('data-bs-toggle', 'modal');
            authBtn.setAttribute('data-bs-target', '#loginModal');
        }
    }
    if (addProductBtn) addProductBtn.classList.toggle('d-none', !loggedIn);
    if (categoryManagement) categoryManagement.style.display = loggedIn ? 'block' : 'none';
    if (brandLogoEdit) brandLogoEdit.classList.toggle('admin-visible', loggedIn);
    if (adminExportPanel) adminExportPanel.classList.toggle('d-none', !loggedIn);
    renderCategories();
    renderProducts();
    renderIndexHotProducts();
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
    renderIndexCategories();
    renderProductsDropdown();
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

function renderProductsDropdown() {
    const dropdown = document.getElementById('productsDropdownMenu');
    if (!dropdown) return;
    const categories = getCategories();
    dropdown.innerHTML = '';
    const allItem = document.createElement('li');
    allItem.innerHTML = '<a class="dropdown-item" href="products.html">All Products</a>';
    dropdown.appendChild(allItem);
    const divider = document.createElement('li');
    divider.innerHTML = '<hr class="dropdown-divider">';
    dropdown.appendChild(divider);
    categories.forEach(cat => {
        const li = document.createElement('li');
        li.innerHTML = '<a class="dropdown-item" href="products.html?category=' + encodeURIComponent(cat) + '">' + escapeHtml(cat) + '</a>';
        dropdown.appendChild(li);
    });
}

function getCategoryIcon(category) {
    const icons = {
        'Kitchenware': 'fa-utensils',
        'Toys': 'fa-puzzle-piece',
        'Apparel': 'fa-shirt',
        'Hand Bag': 'fa-bag-shopping',
        'Electronics': 'fa-mobile-screen-button',
        'Home': 'fa-house',
        'Garden': 'fa-leaf',
        'Material': 'fa-layer-group'
    };
    return icons[category] || 'fa-box';
}

function renderIndexCategories() {
    const list = document.getElementById('indexCategoryList');
    if (!list) return;
    const categories = getCategories();
    list.innerHTML = '';
    categories.forEach(cat => {
        const col = document.createElement('div');
        col.className = 'col-auto';
        col.innerHTML = `
            <a href="products.html?category=${encodeURIComponent(cat)}" class="category-text-card">
                <span class="category-text">${escapeHtml(cat)}</span>
            </a>
        `;
        list.appendChild(col);
    });
}

function renderIndexHotProducts() {
    const list = document.getElementById('indexHotProducts');
    if (!list) return;
    const products = getProducts();
    list.innerHTML = '';
    const displayCount = Math.min(products.length, 8);
    for (let i = 0; i < displayCount; i++) {
        const product = products[i];
        const priceText = formatPrice(product.priceMin) + ' - ' + formatPrice(product.priceMax);
        const col = document.createElement('div');
        col.className = 'col-lg-3 col-md-6';
        col.innerHTML = `
            <div class="product-card">
                <img src="${escapeHtml(product.image)}" class="card-img-top product-img-clickable" alt="${escapeHtml(product.name)}" data-id="${product.id}" style="cursor:pointer;" onerror="this.src='https://picsum.photos/600/400'; this.alt='${escapeHtml(product.name)}'">
                <div class="card-body">
                    <div class="product-category">${escapeHtml(product.category)}</div>
                    <h5 class="product-title product-title-clickable" data-id="${product.id}" style="cursor:pointer;">${escapeHtml(product.name)}</h5>
                    <div class="product-meta">
                        ${product.sku ? `<span class="product-sku"><i class="fas fa-barcode me-1"></i>${escapeHtml(product.sku)}</span>` : ''}
                        ${product.moq ? `<span class="product-moq"><i class="fas fa-box me-1"></i>MOQ: ${escapeHtml(product.moq)}</span>` : ''}
                    </div>
                    <p class="product-desc">${escapeHtml(product.description)}</p>
                    <p class="product-price">${escapeHtml(priceText)}</p>
                    <div class="d-flex flex-wrap gap-2 align-items-center">
                        <a href="products.html#product/${product.id}" class="product-action-btn view-detail-link" data-id="${product.id}"><i class="fas fa-circle-info me-1"></i>${tt('products.viewDetails', 'View Details')}</a>
                        <span class="text-muted">|</span>
                        <a href="#" class="product-action-btn quote-product" data-product="${escapeHtml(product.name)}"><i class="fas fa-file-invoice-dollar me-1"></i>${tt('products.quote', 'Get a Quote')}</a>
                    </div>
                </div>
            </div>
        `;
        list.appendChild(col);
    }
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
    renderIndexHotProducts();
}

function buildSiteDataObject() {
    const products = getProducts().map(p => {
        if (p.variations && Array.isArray(p.variations) && p.variations.length > 0) {
            const pricedVariations = p.variations.filter(v => v.price !== undefined && v.price !== null && v.price !== '' && !isNaN(parseFloat(v.price)));
            if (pricedVariations.length > 0) {
                const prices = pricedVariations.map(v => parseFloat(v.price));
                return { ...p, priceMin: Math.min(...prices), priceMax: Math.max(...prices) };
            }
        }
        return p;
    });
    return {
        version: 1,
        updatedAt: new Date().toISOString(),
        logo: localStorage.getItem('yeatruBrandLogo') || '',
        categories: getCategories(),
        products: products
    };
}

function applySiteData(data, options = {}) {
    if (!data || typeof data !== 'object') return false;

    if (Array.isArray(data.categories)) {
        localStorage.setItem('yeatruCategories', JSON.stringify(data.categories));
    }
    if (Array.isArray(data.products)) {
        data.products.forEach(p => {
            if (p.variations && Array.isArray(p.variations)) {
                const pricedVariations = p.variations.filter(v => v.price !== undefined && v.price !== null && v.price !== '' && !isNaN(parseFloat(v.price)));
                if (pricedVariations.length > 0) {
                    const prices = pricedVariations.map(v => parseFloat(v.price));
                    p.priceMin = Math.min(...prices);
                    p.priceMax = Math.max(...prices);
                }
            }
        });
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
    renderIndexCategories();
    renderIndexHotProducts();

    const detailPage = document.getElementById('productDetailPage');
    const mainContent = document.getElementById('mainContent');
    if (detailPage && mainContent) {
        if (currentDetailProductId) {
            const exists = getProducts().some(p => p.id === currentDetailProductId);
            if (exists) renderDetailPage(currentDetailProductId);
            else hideDetailPage();
        } else {
            const hash = location.hash || '';
            const m = hash.match(/^#product\/(\d+)/);
            if (m) {
                const id = parseInt(m[1]);
                const exists = getProducts().some(p => p.id === id);
                if (exists) showDetailPage(id);
            }
        }
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
        try {
            localStorage.setItem('yeatruSiteDataCache', JSON.stringify(data));
        } catch (e) {}
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
        const priceText = formatPrice(product.priceMin) + ' - ' + formatPrice(product.priceMax);
        const card = document.createElement('div');
        card.className = 'col-lg-3 col-md-6';
        card.innerHTML = `
            <div class="product-card">
                <img src="${escapeHtml(product.image)}" class="card-img-top product-img-clickable" alt="${escapeHtml(product.name)}" data-id="${product.id}" style="cursor:pointer;" onerror="this.src='https://picsum.photos/600/400'; this.alt='${escapeHtml(product.name)}'">
                <div class="card-body">
                    <div class="product-category">${escapeHtml(product.category)}</div>
                    <h5 class="product-title product-title-clickable" data-id="${product.id}" style="cursor:pointer;">${escapeHtml(product.name)}</h5>
                    <div class="product-meta">
                        ${product.sku ? `<span class="product-sku"><i class="fas fa-barcode me-1"></i>${escapeHtml(product.sku)}</span>` : ''}
                        ${product.moq ? `<span class="product-moq"><i class="fas fa-box me-1"></i>MOQ: ${escapeHtml(product.moq)}</span>` : ''}
                    </div>
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
    const detailPage = document.getElementById('productDetailPage');
    const mainContent = document.getElementById('mainContent');
    if (!detailPage || !mainContent) return;
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
    const v = data || { color: '', size: '', image: '', price: '' };
    const item = document.createElement('div');
    item.className = 'variation-item';
    item.innerHTML = `
        <input type="text" class="form-control variation-color" placeholder="Color (e.g. Red)" value="${escapeHtml(v.color || '')}">
        <input type="text" class="form-control variation-size" placeholder="Size (e.g. L)" value="${escapeHtml(v.size || '')}">
        <input type="number" step="0.01" class="form-control variation-price" placeholder="Price ($)" value="${escapeHtml(v.price !== undefined && v.price !== null ? v.price : '')}">
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
        const priceVal = item.querySelector('.variation-price').value.trim();
        const price = priceVal ? parseFloat(priceVal) : null;
        if (color || size) variations.push({ color, size, image, price });
    });
    return variations;
}
function renderDetailVariationsEditor(variations) {
    const container = document.getElementById('detailVariationsContainer');
    if (!container) return;
    container.innerHTML = '';
    if (variations && variations.length > 0) {
        variations.forEach(v => addDetailVariationItem(v));
    } else {
        addDetailVariationItem();
    }
}
function addDetailVariationItem(data) {
    const container = document.getElementById('detailVariationsContainer');
    if (!container) return;
    const v = data || { color: '', size: '', price: '', image: '' };
    const item = document.createElement('div');
    item.className = 'variation-item';
    item.innerHTML = `
        <input type="text" class="form-control variation-color" placeholder="Color (e.g. Red)" value="${escapeHtml(v.color || '')}">
        <input type="text" class="form-control variation-size" placeholder="Size (e.g. L)" value="${escapeHtml(v.size || '')}">
        <input type="number" step="0.01" class="form-control variation-price" placeholder="Price ($)" value="${escapeHtml(v.price !== undefined && v.price !== null ? v.price : '')}">
        <input type="url" class="form-control variation-image" placeholder="Image URL (optional)" value="${escapeHtml(v.image || '')}">
        <button type="button" class="variation-remove"><i class="fas fa-trash"></i></button>
    `;
    item.querySelector('.variation-remove').addEventListener('click', function () { item.remove(); });
    container.appendChild(item);
}
function collectDetailVariations() {
    const variations = [];
    document.querySelectorAll('#detailVariationsContainer .variation-item').forEach(item => {
        const color = item.querySelector('.variation-color').value.trim();
        const size = item.querySelector('.variation-size').value.trim();
        const image = item.querySelector('.variation-image').value.trim();
        const priceVal = item.querySelector('.variation-price').value.trim();
        const price = priceVal ? parseFloat(priceVal) : null;
        if (color || size) variations.push({ color, size, image, price });
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
                ${v.price !== undefined && v.price !== null && v.price !== '' ? `<span class="variation-price">${formatPrice(parseFloat(v.price))}</span>` : ''}
            </div>
        `;
        card.addEventListener('click', function () {
            document.querySelectorAll('.variation-card').forEach(c => c.classList.remove('selected'));
            card.classList.add('selected');
            const priceBig = document.getElementById('detailPriceBig');
            if (priceBig) {
                if (v.price !== undefined && v.price !== null && v.price !== '') {
                    priceBig.textContent = formatPrice(parseFloat(v.price));
                } else {
                    const product = getProducts().find(p => p.id === currentDetailProductId);
                    if (product) {
                        priceBig.textContent = formatPrice(product.priceMin || 0) + ' - ' + formatPrice(product.priceMax || 0);
                    }
                }
            }
        });
        
        list.appendChild(card);
    });
}

function showDetailPage(productId) {
    const mainContent = document.getElementById('mainContent');
    const page = document.getElementById('productDetailPage');
    if (!mainContent || !page) return;
    const product = getProducts().find(p => p.id === productId);
    if (!product) {
        hideDetailPage();
        return;
    }
    currentDetailProductId = productId;
    mainContent.style.display = 'none';
    page.style.display = 'block';
    page.classList.add('active');
    setDetailMode('preview');
    renderDetailPage(productId);
    setProductMeta(product);
    window.scrollTo({ top: 0, behavior: 'smooth' });
}

function hideDetailPage() {
    currentDetailProductId = null;
    const mainContent = document.getElementById('mainContent');
    const page = document.getElementById('productDetailPage');
    if (mainContent) mainContent.style.display = '';
    if (page) {
        page.classList.remove('active');
        page.style.display = 'none';
    }
    resetDefaultMeta();
    if (location.hash.startsWith('#product/')) {
        history.replaceState(null, '', '#products');
    }
}

function renderDetailPage(productId) {
    const product = getProducts().find(p => p.id === productId);
    if (!product) return;
    const detailImage = document.getElementById('detailImage');
    const detailName = document.getElementById('detailName');
    const detailCategory = document.getElementById('detailCategory');
    const detailSKU = document.getElementById('detailSKU');
    const detailMaterial = document.getElementById('detailMaterial');
    const detailSize = document.getElementById('detailSize');
    const detailMOQ = document.getElementById('detailMOQ');
    const detailPriceMin = document.getElementById('detailPriceMin');
    const detailPriceMax = document.getElementById('detailPriceMax');
    const detailDesc = document.getElementById('detailDesc');
    const detailPriceBig = document.getElementById('detailPriceBig');
    const detailNameInput = document.getElementById('detailNameInput');
    const detailImageInput = document.getElementById('detailImageInput');
    const detailMaterialInput = document.getElementById('detailMaterialInput');
    const detailSizeInput = document.getElementById('detailSizeInput');
    const detailMOQInput = document.getElementById('detailMOQInput');
    const detailPriceMinInput = document.getElementById('detailPriceMinInput');
    const detailPriceMaxInput = document.getElementById('detailPriceMaxInput');
    const detailDescInput = document.getElementById('detailDescInput');

    if (detailImage) { detailImage.src = product.image || 'https://picsum.photos/600/400'; detailImage.alt = product.name || ''; }
    if (detailName) detailName.textContent = product.name || '';
    if (detailCategory) detailCategory.textContent = product.category || '';
    if (detailSKU) detailSKU.textContent = product.sku || '';
    if (detailMaterial) detailMaterial.textContent = product.material || '';
    if (detailSize) detailSize.textContent = product.size || '';
    if (detailMOQ) detailMOQ.textContent = product.moq || '';
    if (detailPriceMin) detailPriceMin.textContent = (product.priceMin !== undefined && product.priceMin !== null) ? formatPrice(product.priceMin) : '';
    if (detailPriceMax) detailPriceMax.textContent = (product.priceMax !== undefined && product.priceMax !== null) ? formatPrice(product.priceMax) : '';
    if (detailDesc) detailDesc.textContent = product.description || '';

    let defaultPriceText;
    if (product.variations && product.variations.length > 0) {
        const pricedVariations = product.variations.filter(v => v.price !== undefined && v.price !== null && v.price !== '');
        if (pricedVariations.length > 0) {
            const prices = pricedVariations.map(v => parseFloat(v.price));
            const vMin = Math.min(...prices);
            const vMax = Math.max(...prices);
            if (vMin === vMax) {
                defaultPriceText = formatPrice(vMin);
            } else {
                defaultPriceText = formatPrice(vMin) + ' - ' + formatPrice(vMax);
            }
        } else {
            defaultPriceText = formatPrice(product.priceMin || 0) + ' - ' + formatPrice(product.priceMax || 0);
        }
    } else {
        defaultPriceText = formatPrice(product.priceMin || 0) + ' - ' + formatPrice(product.priceMax || 0);
    }
    if (detailPriceBig) detailPriceBig.textContent = defaultPriceText;

    if (detailNameInput) detailNameInput.value = product.name || '';
    if (detailImageInput) detailImageInput.value = product.image || '';
    if (detailMaterialInput) detailMaterialInput.value = product.material || '';
    if (detailSizeInput) detailSizeInput.value = product.size || '';
    if (detailMOQInput) detailMOQInput.value = product.moq || '';
    if (detailPriceMinInput) detailPriceMinInput.value = product.priceMin || '';
    if (detailPriceMaxInput) detailPriceMaxInput.value = product.priceMax || '';
    if (detailDescInput) detailDescInput.value = product.description || '';

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
    const aplusAddBar = document.getElementById('aplusAddBar');
    if (aplusAddBar) aplusAddBar.classList.toggle('visible', isEdit);

    // 变体编辑区域切换
    const variationsList = document.getElementById('variationsList');
    const detailVariationsContainer = document.getElementById('detailVariationsContainer');
    if (variationsList) variationsList.style.display = isEdit ? 'none' : '';
    if (detailVariationsContainer) {
        if (isEdit && currentDetailProductId) {
            const product = getProducts().find(p => p.id === currentDetailProductId);
            if (product && product.variations) {
                renderDetailVariationsEditor(product.variations);
            } else {
                renderDetailVariationsEditor([]);
            }
        }
    }

    const badge = document.getElementById('saveStatusBadge');
    badge.style.display = isEdit ? 'inline-flex' : 'none';
    if (isEdit) setSaveStatus('saved');
}

function setSaveStatus(state) {
    const badge = document.getElementById('saveStatusBadge');
    if (!badge) return;
    const span = badge.querySelector('span');
    badge.classList.remove('saving', 'saved', 'error');
    if (state === 'saving') {
        badge.classList.add('saving');
        if (span) span.textContent = tt('detail.saving', 'Saving...');
    } else if (state === 'saved') {
        badge.classList.add('saved');
        if (span) span.textContent = tt('detail.saved', 'Saved');
    } else if (state === 'error') {
        badge.classList.add('error');
        if (span) span.textContent = tt('detail.error', 'Save failed');
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
        p.description = document.getElementById('detailDescInput').value || p.description;

        p.aplus = collectAplusBlocks();
        p.variations = collectDetailVariations();

        if (p.variations && Array.isArray(p.variations) && p.variations.length > 0) {
            const pricedVariations = p.variations.filter(v => v.price !== undefined && v.price !== null && v.price !== '' && !isNaN(parseFloat(v.price)));
            if (pricedVariations.length > 0) {
                const prices = pricedVariations.map(v => parseFloat(v.price));
                p.priceMin = Math.min(...prices);
                p.priceMax = Math.max(...prices);
            }
        } else {
            const minV = document.getElementById('detailPriceMinInput').value;
            if (minV) p.priceMin = parseFloat(minV);
            const maxV = document.getElementById('detailPriceMaxInput').value;
            if (maxV) p.priceMax = parseFloat(maxV);
        }
        products[idx] = p;
        localStorage.setItem('yeatruProducts', JSON.stringify(products));
        document.getElementById('detailName').textContent = p.name;
        document.getElementById('detailImage').src = p.image;
        document.getElementById('detailMaterial').textContent = p.material;
        document.getElementById('detailSize').textContent = p.size;
        document.getElementById('detailMOQ').textContent = p.moq;
        document.getElementById('detailPriceMin').textContent = formatPrice(p.priceMin);
        document.getElementById('detailPriceMax').textContent = formatPrice(p.priceMax);
        document.getElementById('detailDesc').textContent = p.description;

        let savedPriceText;
        if (p.variations && p.variations.length > 0) {
            const pricedVariations = p.variations.filter(v => v.price !== undefined && v.price !== null && v.price !== '');
            if (pricedVariations.length > 0) {
                const prices = pricedVariations.map(v => parseFloat(v.price));
                const vMin = Math.min(...prices);
                const vMax = Math.max(...prices);
                if (vMin === vMax) {
                    savedPriceText = formatPrice(vMin);
                } else {
                    savedPriceText = formatPrice(vMin) + ' - ' + formatPrice(vMax);
                }
            } else {
                savedPriceText = formatPrice(p.priceMin || 0) + ' - ' + formatPrice(p.priceMax || 0);
            }
        } else {
            savedPriceText = formatPrice(p.priceMin || 0) + ' - ' + formatPrice(p.priceMax || 0);
        }
        document.getElementById('detailPriceBig').textContent = savedPriceText;
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

    const textToolbar = document.createElement('div');
    textToolbar.className = 'aplus-text-toolbar';
    textToolbar.innerHTML = `
        <button type="button" data-format="bold" title="Bold"><i class="fas fa-bold"></i></button>
        <button type="button" data-format="italic" title="Italic"><i class="fas fa-italic"></i></button>
        <button type="button" data-format="underline" title="Underline"><i class="fas fa-underline"></i></button>
        <button type="button" data-format="insertUnorderedList" title="Unordered List"><i class="fas fa-list-ul"></i></button>
        <button type="button" data-format="insertOrderedList" title="Ordered List"><i class="fas fa-list-ol"></i></button>
        <button type="button" data-format="insertTable" title="Insert Table"><i class="fas fa-table"></i></button>
        <button type="button" data-format="insertRow" title="Insert Row"><i class="fas fa-plus"></i></button>
        <button type="button" data-format="deleteRow" title="Delete Row"><i class="fas fa-minus"></i></button>
        <button type="button" data-format="deleteTable" title="Delete Table"><i class="fas fa-trash-alt"></i></button>
    `;
    wrap.appendChild(textToolbar);

    const content = document.createElement('div');
    content.className = 'aplus-block-content';
    if (b.type === 'hero') {
        content.innerHTML = `
            <h2 class="aplus-block-heading" data-editable="heading">${escapeHtml(b.heading || '')}</h2>
            <div class="aplus-block-text" data-editable="text">${b.text || ''}</div>
            <img src="${escapeHtml(b.image || '')}" alt="hero" style="width:100%;height:auto;border-radius:8px;" onerror="this.src='https://picsum.photos/1200/420'">
            <input type="url" class="form-control aplus-image-input" placeholder="Image URL" data-editable-img value="${escapeHtml(b.image || '')}">
        `;
    } else if (b.type === 'text') {
        content.innerHTML = `
            <h3 class="aplus-block-heading" data-editable="heading">${escapeHtml(b.heading || '')}</h3>
            <div class="aplus-block-text" data-editable="text">${b.text || ''}</div>
        `;
    } else if (b.type === 'textImage' || b.type === 'imageText') {
        const layoutClass = b.type === 'textImage' ? 'layout-text-image' : 'layout-image-text';
        content.innerHTML = `
            <div class="aplus-block-image-wrap ${layoutClass}">
                <div class="aplus-block-text-side">
                    <h3 class="aplus-block-heading" data-editable="heading">${escapeHtml(b.heading || '')}</h3>
                    <div class="aplus-block-text" data-editable="text">${b.text || ''}</div>
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
                    ${items.map(it => '<li data-editable="feature">' + it + '</li>').join('')}
                </ul>
            </div>
        `;
    } else if (b.type === 'twoColumns') {
        content.innerHTML = `
            <div class="aplus-block-two-columns">
                <div class="aplus-block-column" data-editable="column">${b.column1 || ''}</div>
                <div class="aplus-block-column" data-editable="column">${b.column2 || ''}</div>
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
    wrap.querySelectorAll('[data-format]').forEach(btn => {
        btn.addEventListener('mousedown', function (e) {
            e.preventDefault();
            const format = this.dataset.format;
            const textEl = wrap.querySelector('[data-editable="text"]');
            if (textEl) {
                textEl.focus();
                if (format === 'insertTable') {
                    const rows = prompt('Enter number of rows (1-10):', '3');
                    const cols = prompt('Enter number of columns (1-10):', '2');
                    const numRows = Math.min(10, Math.max(1, parseInt(rows) || 3));
                    const numCols = Math.min(10, Math.max(1, parseInt(cols) || 2));
                    let tableHtml = '<table border="1" style="border-collapse:collapse;margin:10px 0;width:100%;">';
                    // Header row
                    tableHtml += '<tr>';
                    for (let c = 0; c < numCols; c++) {
                        tableHtml += `<th style="padding:8px;border:1px solid #ccc;background:#0b7b94;color:#fff;">Header ${c + 1}</th>`;
                    }
                    tableHtml += '</tr>';
                    // Data rows
                    for (let r = 1; r < numRows; r++) {
                        tableHtml += '<tr>';
                        for (let c = 0; c < numCols; c++) {
                            tableHtml += `<td style="padding:8px;border:1px solid #ccc;">Cell ${r}-${c + 1}</td>`;
                        }
                        tableHtml += '</tr>';
                    }
                    tableHtml += '</table>';
                    document.execCommand('insertHTML', false, tableHtml);
                } else if (format === 'deleteTable') {
                    const selection = window.getSelection();
                    if (selection.rangeCount > 0) {
                        const range = selection.getRangeAt(0);
                        let node = range.commonAncestorContainer;
                        while (node && node !== textEl) {
                            if (node.tagName === 'TABLE') {
                                node.remove();
                                break;
                            }
                            node = node.parentNode;
                        }
                    }
                } else if (format === 'insertRow') {
                    const selection = window.getSelection();
                    if (selection.rangeCount > 0) {
                        let node = selection.anchorNode;
                        while (node && node !== textEl) {
                            if (node.tagName === 'TR') {
                                const newRow = node.cloneNode(true);
                                newRow.querySelectorAll('th, td').forEach(cell => {
                                    if (cell.tagName === 'TH') {
                                        cell.tagName = 'TD';
                                    }
                                    cell.textContent = 'New Cell';
                                });
                                node.parentNode.insertBefore(newRow, node.nextSibling);
                                break;
                            }
                            node = node.parentNode;
                        }
                    }
                } else if (format === 'deleteRow') {
                    const selection = window.getSelection();
                    if (selection.rangeCount > 0) {
                        let node = selection.anchorNode;
                        while (node && node !== textEl) {
                            if (node.tagName === 'TR') {
                                const table = node.closest('table');
                                if (table && table.rows.length > 1) {
                                    node.remove();
                                }
                                break;
                            }
                            node = node.parentNode;
                        }
                    }
                } else if (format === 'insertUnorderedList') {
                    document.execCommand('insertUnorderedList', false, null);
                } else if (format === 'insertOrderedList') {
                    document.execCommand('insertOrderedList', false, null);
                } else {
                    document.execCommand(format, false, null);
                }
                scheduleAutoSave();
            }
        });
    });
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
        const imgInput = blockEl.querySelector('[data-editable-img]');
        if (imgInput) item.image = imgInput.value;
        else {
            const img = blockEl.querySelector('img');
            if (img) item.image = img.src;
        }
        if (type === 'features') {
            item.items = [];
            blockEl.querySelectorAll('[data-editable="feature"]').forEach(li => {
                const v = li.innerHTML.trim();
                if (v) item.items.push(v);
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
        if (type === 'twoColumns') {
            const columns = blockEl.querySelectorAll('[data-editable="column"]');
            if (columns.length >= 1) item.column1 = columns[0].innerHTML;
            if (columns.length >= 2) item.column2 = columns[1].innerHTML;
        }
        out.push(item);
    });
    return out;
}

function renderBrandLogo() {
    let url = localStorage.getItem('yeatruBrandLogo');
    const img = document.getElementById('brandLogoImg');
    const fallback = document.getElementById('brandLogoFallback');
    const footerImg = document.getElementById('footerLogoImg');
    const footerFallback = document.getElementById('footerLogoFallback');
    
    if (!img || !fallback) return;
    
    if (!url) {
        try {
            const data = localStorage.getItem('yeatruSiteDataCache');
            if (data) {
                const parsed = JSON.parse(data);
                if (parsed.logo) url = parsed.logo;
            }
        } catch (e) {}
    }
    
    if (url) {
        img.src = url;
        img.style.display = 'block';
        fallback.style.display = 'none';
        if (footerImg && footerFallback) {
            footerImg.src = url;
            footerImg.style.display = 'block';
            footerFallback.style.display = 'none';
        }
    } else {
        img.src = '';
        img.style.display = 'none';
        fallback.style.display = '';
        if (footerImg && footerFallback) {
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

let defaultMeta = {};

function saveDefaultMeta() {
    const titleEl = document.querySelector('title');
    const descEl = document.querySelector('meta[name="description"]');
    const ogTitleEl = document.querySelector('meta[property="og:title"]');
    const ogDescEl = document.querySelector('meta[property="og:description"]');
    const ogImageEl = document.querySelector('meta[property="og:image"]');
    const ogUrlEl = document.querySelector('meta[property="og:url"]');
    const ogTypeEl = document.querySelector('meta[property="og:type"]');
    const twitterTitleEl = document.querySelector('meta[name="twitter:title"]');
    const twitterDescEl = document.querySelector('meta[name="twitter:description"]');
    const twitterImageEl = document.querySelector('meta[name="twitter:image"]');
    const twitterUrlEl = document.querySelector('meta[name="twitter:url"]');
    const canonicalEl = document.querySelector('link[rel="canonical"]');

    defaultMeta = {
        title: titleEl ? titleEl.textContent : '',
        description: descEl ? descEl.content : '',
        ogTitle: ogTitleEl ? ogTitleEl.content : '',
        ogDescription: ogDescEl ? ogDescEl.content : '',
        ogImage: ogImageEl ? ogImageEl.content : '',
        ogUrl: ogUrlEl ? ogUrlEl.content : '',
        ogType: ogTypeEl ? ogTypeEl.content : '',
        twitterTitle: twitterTitleEl ? twitterTitleEl.content : '',
        twitterDescription: twitterDescEl ? twitterDescEl.content : '',
        twitterImage: twitterImageEl ? twitterImageEl.content : '',
        twitterUrl: twitterUrlEl ? twitterUrlEl.content : '',
        canonical: canonicalEl ? canonicalEl.href : ''
    };
}

function updateMetaTag(selector, attribute, value) {
    let el = document.querySelector(selector);
    if (!el) {
        if (selector.startsWith('meta[property=')) {
            const prop = selector.match(/meta\[property="([^"]+)"\]/);
            if (prop) {
                el = document.createElement('meta');
                el.setAttribute('property', prop[1]);
                document.head.appendChild(el);
            }
        } else if (selector.startsWith('meta[name=')) {
            const name = selector.match(/meta\[name="([^"]+)"\]/);
            if (name) {
                el = document.createElement('meta');
                el.setAttribute('name', name[1]);
                document.head.appendChild(el);
            }
        } else if (selector.startsWith('link[rel=')) {
            const rel = selector.match(/link\[rel="([^"]+)"\]/);
            if (rel) {
                el = document.createElement('link');
                el.setAttribute('rel', rel[1]);
                document.head.appendChild(el);
            }
        }
    }
    if (el) {
        el.setAttribute(attribute, value);
    }
}

function setProductMeta(product) {
    if (!product) return;
    if (Object.keys(defaultMeta).length === 0) saveDefaultMeta();

    const productUrl = window.location.origin + window.location.pathname + '#product/' + product.id;
    const productImage = product.image || 'https://www.yeatru.com/og-image.svg';
    const productDesc = product.description ? product.description.substring(0, 160) : defaultMeta.description;
    const productTitle = product.name + ' | Yeatru Sourcing - China Wholesale Products';

    document.title = productTitle;
    updateMetaTag('meta[name="description"]', 'content', productDesc);
    updateMetaTag('link[rel="canonical"]', 'href', productUrl);
    updateMetaTag('meta[property="og:title"]', 'content', productTitle);
    updateMetaTag('meta[property="og:description"]', 'content', productDesc);
    updateMetaTag('meta[property="og:image"]', 'content', productImage);
    updateMetaTag('meta[property="og:url"]', 'content', productUrl);
    updateMetaTag('meta[property="og:type"]', 'content', 'product');
    updateMetaTag('meta[name="twitter:title"]', 'content', productTitle);
    updateMetaTag('meta[name="twitter:description"]', 'content', productDesc);
    updateMetaTag('meta[name="twitter:image"]', 'content', productImage);
    updateMetaTag('meta[name="twitter:url"]', 'content', productUrl);

    let existingLd = document.getElementById('product-jsonld');
    if (!existingLd) {
        existingLd = document.createElement('script');
        existingLd.type = 'application/ld+json';
        existingLd.id = 'product-jsonld';
        document.head.appendChild(existingLd);
    }
    existingLd.textContent = JSON.stringify({
        "@context": "https://schema.org",
        "@type": "Product",
        "name": product.name,
        "image": productImage,
        "description": product.description || '',
        "sku": product.sku || '',
        "brand": {
            "@type": "Brand",
            "name": "Yeatru Sourcing"
        },
        "offers": {
            "@type": "AggregateOffer",
            "priceCurrency": "USD",
            "lowPrice": product.priceMin || 0,
            "highPrice": product.priceMax || 0,
            "availability": "https://schema.org/InStock",
            "seller": {
                "@type": "Organization",
                "name": "Yeatru Sourcing"
            }
        }
    });
}

function resetDefaultMeta() {
    if (Object.keys(defaultMeta).length === 0) return;

    document.title = defaultMeta.title;
    updateMetaTag('meta[name="description"]', 'content', defaultMeta.description);
    updateMetaTag('link[rel="canonical"]', 'href', defaultMeta.canonical);
    updateMetaTag('meta[property="og:title"]', 'content', defaultMeta.ogTitle);
    updateMetaTag('meta[property="og:description"]', 'content', defaultMeta.ogDescription);
    updateMetaTag('meta[property="og:image"]', 'content', defaultMeta.ogImage);
    updateMetaTag('meta[property="og:url"]', 'content', defaultMeta.ogUrl);
    updateMetaTag('meta[property="og:type"]', 'content', defaultMeta.ogType);
    updateMetaTag('meta[name="twitter:title"]', 'content', defaultMeta.twitterTitle);
    updateMetaTag('meta[name="twitter:description"]', 'content', defaultMeta.twitterDescription);
    updateMetaTag('meta[name="twitter:image"]', 'content', defaultMeta.twitterImage);
    updateMetaTag('meta[name="twitter:url"]', 'content', defaultMeta.twitterUrl);

    const existingLd = document.getElementById('product-jsonld');
    if (existingLd) existingLd.remove();
}

function initBlogCardImages() {
    document.querySelectorAll('.blog-card-image').forEach(function (wrapper) {
        const img = wrapper.querySelector('img');
        if (!img) return;
        if (img.complete && img.naturalWidth > 0) {
            wrapper.classList.add('image-loaded');
        } else {
            img.addEventListener('load', function () {
                wrapper.classList.add('image-loaded');
            });
            img.addEventListener('error', function () {
                wrapper.classList.add('image-error');
                img.style.display = 'none';
            });
        }
    });
}

document.addEventListener('DOMContentLoaded', initBlogCardImages);