"""Internationalization — EN / PT / ES / EL translations."""

TRANSLATIONS = {
    "EN": {
        "title": "☀️ RenewView",
        "subtitle": "Find out what your land could earn from solar.",
        "intro": "Free assessment in under 2 minutes for landowners in Portugal, Spain & Greece.",
        "location": "📍 Property Location",
        "details": "🏗️ Property Details",
        "country": "Country",
        "latitude": "Latitude",
        "longitude": "Longitude",
        "site_type": "Site Type",
        "ground_parcel": "Ground Parcel",
        "commercial_rooftop": "Commercial Rooftop",
        "parking_structure": "Parking Structure",
        "parcel_size": "Parcel Size (hectares)",
        "usable_area": "Usable Area (m²)",
        "grid_distance": "Distance to Grid (km)",
        "terrain": "Terrain Type",
        "land_status": "Land Status",
        "run_assessment": "🔍 Run Viability Assessment",
        "start_assessment": "🚀 Start New Assessment",
        "back_to_home": "Back to Home",
        "back_to_inputs": "Back to Inputs",
        "new_assessment": "🔄 New Assessment",
        "results": "📊 Assessment Results",
        "viability": "Viability",
        "score": "Score",
        "annual_kwh": "Est. Annual kWh",
        "annual_revenue": "Est. Annual Revenue",
        "connect_installer": "🔗 Connect with a regional installer for a detailed survey",
        "not_viable_msg": "This site did not pass pre-screening.",
        "disclaimer": "⚠️ Preliminary assessment only. Consult a qualified professional.",
        "map_preview": "Selected location preview",
        "about": "About RenewView",
        "ethics_title": "Ethics & Limitations",
        "model_not_ready": "⚠️ Model not yet trained. Run `crewai flow kickoff` first. Showing heuristic results.",
        "eliminated_by": "Eliminated by Gate",
        "reason": "Reason",
        "redirect": "Recommendation",
        "flags": "Flags",
        # Sidebar
        "sidebar_about_text": (
            "**RenewView** uses multi-agent AI to assess solar viability.\n\n"
            "**Pipeline:**\n"
            "1. Elimination gates (protected land, grid distance, irradiance)\n"
            "2. ML classification (Random Forest / Gradient Boosting)\n"
            "3. Energy & revenue estimation\n\n"
            "**Data:** NASA POWER API + OpenStreetMap\n\n"
            "**Regions:** Portugal, Spain, Greece, Italy"
        ),
        "sidebar_ethics_text": (
            "- Bias toward data-rich regions (Spain, Italy have more data)\n"
            "- False positive risk on marginal sites\n"
            "- Agricultural land conversion trade-offs\n"
            "- Always consult a professional before investing"
        ),
        # Tabs
        "tab_assessment": "🔍 Assessment",
        "tab_about": "ℹ️ About",
        # NASA POWER fetch
        "fetch_solar_data": "☀️ Fetch Solar Data from NASA",
        "fetching_data": "Fetching solar data from NASA POWER...",
        "solar_data_loaded": "Solar data loaded from NASA POWER API",
        "solar_data_error": "Could not fetch solar data. Using estimates.",
        "ghi_label": "GHI (kWh/m²/day)",
        "dni_label": "DNI (kWh/m²/day)",
        "temperature_label": "Temperature (°C)",
        "humidity_label": "Humidity (%)",
        "wind_speed_label": "Wind Speed (m/s)",
        "precipitation_label": "Precipitation (mm/day)",
        "cloud_cover_label": "Cloud Cover (%)",
        "climate_data": "🌤️ Climate Data",
        "climate_manual_note": "Adjust values or click Fetch to get real data",
        # Results extras
        "gates_passed": "Pre-screening gates passed",
        "gate_detail_g1": "G1 — Land status: not protected/wetland",
        "gate_detail_g2": "G2 — Grid distance within 8 km",
        "gate_detail_g3": "G3 — Solar irradiance above 3.5 kWh/m²/day",
        "gate_detail_g4": "G4 — Parcel size adequate",
        # Address search & polygon drawing
        "search_address": "Search address",
        "search_address_placeholder": "e.g. Faro, Portugal",
        "search_button": "Search",
        "searching_address": "Searching address...",
        "address_not_found": "Address not found. Try a different search.",
        "address_found": "Location updated from address search.",
        "draw_parcel": "Draw your parcel boundary on the map (polygon tool)",
        "polygon_area_detected": "Parcel area detected from drawing",
        "map_instructions": "Use the polygon tool on the left to outline your parcel. Click vertices, then close the shape.",
        # Auto-detect site properties
        "auto_detect_btn": "Auto-detect Site Properties",
        "detecting_properties": "Detecting grid distance and terrain...",
        "detection_success": "Auto-detected",
        "detection_grid_fail": "Could not detect grid distance (no substations found nearby).",
        "detection_terrain_fail": "Elevation API unavailable — terrain estimated from country.",
        # About page
        "about_problem": "## Problem",
        "about_problem_text": (
            "The EU targets 700 GW solar by 2030, but landowners in Southern Europe "
            "have no data-driven way to assess land viability before hiring consultants."
        ),
        "about_solution": "## Solution",
        "about_solution_text": (
            "A CrewAI-powered pre-screening decision gate that predicts solar feasibility, "
            "classifies risk tiers, estimates energy output, and connects viable sites to "
            "regional installers."
        ),
        "about_architecture": "## Architecture",
        "about_architecture_text": (
            "- **Crew 1 — Land Intelligence:** 4 agents (ingestion, cleaning, EDA, contract)\n"
            "- **Validation Gate:** Schema check before ML\n"
            "- **Crew 2 — Prediction:** 4 agents (validator, features, training, evaluation)\n"
            "- **Elimination Gates:** G1–G4 hard filters before classification\n"
            "- **Frontend:** Multi-language Streamlit (EN/PT/ES/EL)"
        ),
        "about_ethics": "## Ethics & Limitations",
        "about_ethics_text": (
            "- **Regional bias:** More training data available for Spain and Italy\n"
            "- **False positives:** Marginal sites may receive optimistic assessments\n"
            "- **Land conversion:** Solar development on agricultural land has trade-offs\n"
            "- **Preliminary only:** Always consult a qualified professional"
        ),
        "about_stack": "## Stack",
        "about_stack_text": "CrewAI Flow, Python, Pandas, Scikit-Learn, Matplotlib, Seaborn, Streamlit",
        "about_course": "## Course",
        "about_course_text": "AI Development & Collaboration — Hebrew University 2026 — Dr. Zvi Ben Ami",
        # Pre-qualification (Step 1)
        "prequalify_heading": "Quick Pre-Check",
        "land_size_question": "How large is your site?",
        "land_size_option_small": "Less than 1 hectare",
        "land_size_option_medium": "1–5 hectares",
        "land_size_option_large": "5–50 hectares",
        "land_size_option_xlarge": "50+ hectares",
        "land_size_rooftop_hint": "For parcels under 2 ha, consider a rooftop assessment instead.",
        "lead_name": "Your name",
        "lead_email": "Email address",
        "lead_optional_note": "Optional — we'll send your report here",
        # Step 2 advanced toggle
        "advanced_coords": "Advanced: Manual coordinates",
        # Step 3 paid report CTA
        "cta_headline": "Your full personalized subsidy + installer report, delivered by email within 24 hours.",
        "cta_button": "Get my €29 detailed report →",
        "cta_trust": "Secure checkout by Lemon Squeezy. EU VAT included.",
        "cta_not_viable_note": (
            "Based on these inputs, solar doesn't look viable here. "
            "The detailed report is offered only for viable properties — "
            "adjust your inputs if you think the assessment is off."
        ),
    },
    "PT": {
        "title": "☀️ RenewView",
        "subtitle": "Descubra quanto o seu terreno pode render com energia solar.",
        "intro": "Avaliação gratuita em menos de 2 minutos para proprietários em Portugal, Espanha e Grécia.",
        "location": "📍 Localização",
        "details": "🏗️ Detalhes da Propriedade",
        "country": "País",
        "latitude": "Latitude",
        "longitude": "Longitude",
        "site_type": "Tipo de Local",
        "ground_parcel": "Terreno",
        "commercial_rooftop": "Telhado Comercial",
        "parking_structure": "Estacionamento",
        "parcel_size": "Tamanho (hectares)",
        "usable_area": "Área Útil (m²)",
        "grid_distance": "Distância à Rede (km)",
        "terrain": "Tipo de Terreno",
        "land_status": "Estado do Terreno",
        "run_assessment": "🔍 Avaliar Viabilidade",
        "start_assessment": "🚀 Iniciar Nova Avaliação",
        "back_to_home": "Voltar ao Início",
        "back_to_inputs": "Voltar aos Dados",
        "new_assessment": "🔄 Nova Avaliação",
        "results": "📊 Resultados",
        "viability": "Viabilidade",
        "score": "Pontuação",
        "annual_kwh": "kWh Anual Est.",
        "annual_revenue": "Receita Anual Est.",
        "connect_installer": "🔗 Contacte um instalador regional para uma avaliação detalhada",
        "not_viable_msg": "Este local não passou na triagem.",
        "disclaimer": "⚠️ Avaliação preliminar. Consulte um profissional qualificado.",
        "map_preview": "Pré-visualização da localização selecionada",
        "about": "Sobre o RenewView",
        "ethics_title": "Ética e Limitações",
        "model_not_ready": "⚠️ Modelo ainda não treinado. Execute `crewai flow kickoff`. Mostrando resultados heurísticos.",
        "eliminated_by": "Eliminado pelo Portão",
        "reason": "Motivo",
        "redirect": "Recomendação",
        "flags": "Sinalizações",
        "sidebar_about_text": (
            "**RenewView** utiliza IA multi-agente para avaliar a viabilidade solar.\n\n"
            "**Pipeline:**\n"
            "1. Portões de eliminação (terreno protegido, distância da rede, irradiação)\n"
            "2. Classificação ML (Random Forest / Gradient Boosting)\n"
            "3. Estimativa de energia e receita\n\n"
            "**Dados:** NASA POWER API + OpenStreetMap\n\n"
            "**Regiões:** Portugal, Espanha, Grécia, Itália"
        ),
        "sidebar_ethics_text": (
            "- Viés para regiões com mais dados (Espanha, Itália)\n"
            "- Risco de falsos positivos em locais marginais\n"
            "- Compensações na conversão de terras agrícolas\n"
            "- Consulte sempre um profissional antes de investir"
        ),
        "tab_assessment": "🔍 Avaliação",
        "tab_about": "ℹ️ Sobre",
        "fetch_solar_data": "☀️ Obter Dados Solares da NASA",
        "fetching_data": "A obter dados solares da NASA POWER...",
        "solar_data_loaded": "Dados solares carregados da NASA POWER API",
        "solar_data_error": "Não foi possível obter dados solares. A usar estimativas.",
        "ghi_label": "GHI (kWh/m²/dia)",
        "dni_label": "DNI (kWh/m²/dia)",
        "temperature_label": "Temperatura (°C)",
        "humidity_label": "Humidade (%)",
        "wind_speed_label": "Velocidade do Vento (m/s)",
        "precipitation_label": "Precipitação (mm/dia)",
        "cloud_cover_label": "Cobertura de Nuvens (%)",
        "climate_data": "🌤️ Dados Climáticos",
        "climate_manual_note": "Ajuste os valores ou clique Obter para dados reais",
        "gates_passed": "Portões de pré-triagem aprovados",
        "gate_detail_g1": "G1 — Estado do terreno: não protegido/pantanal",
        "gate_detail_g2": "G2 — Distância da rede dentro de 8 km",
        "gate_detail_g3": "G3 — Irradiação solar acima de 3,5 kWh/m²/dia",
        "gate_detail_g4": "G4 — Tamanho da parcela adequado",
        "search_address": "Pesquisar endereço",
        "search_address_placeholder": "ex. Faro, Portugal",
        "search_button": "Pesquisar",
        "searching_address": "A pesquisar endereço...",
        "address_not_found": "Endereço não encontrado. Tente outra pesquisa.",
        "address_found": "Localização atualizada a partir da pesquisa.",
        "draw_parcel": "Desenhe o limite da parcela no mapa (ferramenta polígono)",
        "polygon_area_detected": "Área da parcela detetada a partir do desenho",
        "map_instructions": "Use a ferramenta de polígono à esquerda para delinear a sua parcela.",
        "auto_detect_btn": "Detetar Propriedades do Local",
        "detecting_properties": "A detetar distância à rede e terreno...",
        "detection_success": "Detetado automaticamente",
        "detection_grid_fail": "Não foi possível detetar a distância à rede (sem subestações próximas).",
        "detection_terrain_fail": "API de elevação indisponível — terreno estimado pelo país.",
        "about_problem": "## Problema",
        "about_problem_text": (
            "A UE pretende 700 GW de solar até 2030, mas os proprietários no Sul da Europa "
            "não têm ferramentas baseadas em dados para avaliar a viabilidade antes de contratar consultores."
        ),
        "about_solution": "## Solução",
        "about_solution_text": (
            "Um sistema de pré-triagem baseado em CrewAI que prevê a viabilidade solar, "
            "classifica níveis de risco, estima a produção de energia e conecta locais viáveis "
            "a instaladores regionais."
        ),
        "about_architecture": "## Arquitetura",
        "about_architecture_text": (
            "- **Crew 1 — Inteligência Territorial:** 4 agentes (ingestão, limpeza, EDA, contrato)\n"
            "- **Portão de Validação:** Verificação de esquema antes do ML\n"
            "- **Crew 2 — Previsão:** 4 agentes (validador, features, treino, avaliação)\n"
            "- **Portões de Eliminação:** G1–G4 filtros antes da classificação\n"
            "- **Frontend:** Streamlit multilingue (EN/PT/ES/EL)"
        ),
        "about_ethics": "## Ética e Limitações",
        "about_ethics_text": (
            "- **Viés regional:** Mais dados de treino para Espanha e Itália\n"
            "- **Falsos positivos:** Locais marginais podem receber avaliações otimistas\n"
            "- **Conversão de terrenos:** Desenvolvimento solar em terras agrícolas tem compensações\n"
            "- **Apenas preliminar:** Consulte sempre um profissional qualificado"
        ),
        "about_stack": "## Tecnologias",
        "about_stack_text": "CrewAI Flow, Python, Pandas, Scikit-Learn, Matplotlib, Seaborn, Streamlit",
        "about_course": "## Curso",
        "about_course_text": "Desenvolvimento de IA e Colaboração — Universidade Hebraica 2026 — Dr. Zvi Ben Ami",
        # Pre-qualification (Step 1)
        "prequalify_heading": "Pré-verificação Rápida",
        "land_size_question": "Qual é o tamanho do seu terreno?",
        "land_size_option_small": "Menos de 1 hectare",
        "land_size_option_medium": "1–5 hectares",
        "land_size_option_large": "5–50 hectares",
        "land_size_option_xlarge": "50+ hectares",
        "land_size_rooftop_hint": "Para parcelas com menos de 2 ha, considere uma avaliação de telhado.",
        "lead_name": "O seu nome",
        "lead_email": "Endereço de e-mail",
        "lead_optional_note": "Opcional — enviaremos o seu relatório aqui",
        # Step 2 advanced toggle
        "advanced_coords": "Avançado: Coordenadas manuais",
        # Step 3 paid report CTA
        "cta_headline": "O seu relatório completo e personalizado de subsídios + instaladores, entregue por email em 24 horas.",
        "cta_button": "Obter o meu relatório detalhado €29 →",
        "cta_trust": "Checkout seguro via Lemon Squeezy. IVA da UE incluído.",
        "cta_not_viable_note": (
            "Com base nestes dados, a energia solar não parece viável aqui. "
            "O relatório detalhado é oferecido apenas para propriedades viáveis — "
            "ajuste os seus dados se achar que a avaliação está incorreta."
        ),
    },
    "ES": {
        "title": "☀️ RenewView",
        "subtitle": "Descubra cuánto podría rentar su terreno con energía solar.",
        "intro": "Evaluación gratuita en menos de 2 minutos para propietarios en Portugal, España y Grecia.",
        "location": "📍 Ubicación",
        "details": "🏗️ Detalles de la Propiedad",
        "country": "País",
        "latitude": "Latitud",
        "longitude": "Longitud",
        "site_type": "Tipo de Sitio",
        "ground_parcel": "Parcela de Terreno",
        "commercial_rooftop": "Techo Comercial",
        "parking_structure": "Estacionamiento",
        "parcel_size": "Tamaño (hectáreas)",
        "usable_area": "Área Útil (m²)",
        "grid_distance": "Distancia a la Red (km)",
        "terrain": "Tipo de Terreno",
        "land_status": "Estado del Terreno",
        "run_assessment": "🔍 Evaluar Viabilidad",
        "start_assessment": "🚀 Iniciar Nueva Evaluación",
        "back_to_home": "Volver al Inicio",
        "back_to_inputs": "Volver a los Datos",
        "new_assessment": "🔄 Nueva Evaluación",
        "results": "📊 Resultados",
        "viability": "Viabilidad",
        "score": "Puntuación",
        "annual_kwh": "kWh Anual Est.",
        "annual_revenue": "Ingreso Anual Est.",
        "connect_installer": "🔗 Conecte con un instalador regional para una evaluación detallada",
        "not_viable_msg": "Este sitio no pasó la evaluación previa.",
        "disclaimer": "⚠️ Evaluación preliminar. Consulte a un profesional calificado.",
        "map_preview": "Vista previa de la ubicación seleccionada",
        "about": "Acerca de RenewView",
        "ethics_title": "Ética y Limitaciones",
        "model_not_ready": "⚠️ Modelo no entrenado. Ejecute `crewai flow kickoff`. Mostrando resultados heurísticos.",
        "eliminated_by": "Eliminado por Puerta",
        "reason": "Razón",
        "redirect": "Recomendación",
        "flags": "Señalizaciones",
        "sidebar_about_text": (
            "**RenewView** utiliza IA multi-agente para evaluar la viabilidad solar.\n\n"
            "**Pipeline:**\n"
            "1. Puertas de eliminación (terreno protegido, distancia a red, irradiación)\n"
            "2. Clasificación ML (Random Forest / Gradient Boosting)\n"
            "3. Estimación de energía e ingresos\n\n"
            "**Datos:** NASA POWER API + OpenStreetMap\n\n"
            "**Regiones:** Portugal, España, Grecia, Italia"
        ),
        "sidebar_ethics_text": (
            "- Sesgo hacia regiones con más datos (España, Italia)\n"
            "- Riesgo de falsos positivos en sitios marginales\n"
            "- Compensaciones en la conversión de tierras agrícolas\n"
            "- Consulte siempre a un profesional antes de invertir"
        ),
        "tab_assessment": "🔍 Evaluación",
        "tab_about": "ℹ️ Acerca de",
        "fetch_solar_data": "☀️ Obtener Datos Solares de NASA",
        "fetching_data": "Obteniendo datos solares de NASA POWER...",
        "solar_data_loaded": "Datos solares cargados de NASA POWER API",
        "solar_data_error": "No se pudieron obtener datos solares. Usando estimaciones.",
        "ghi_label": "GHI (kWh/m²/día)",
        "dni_label": "DNI (kWh/m²/día)",
        "temperature_label": "Temperatura (°C)",
        "humidity_label": "Humedad (%)",
        "wind_speed_label": "Velocidad del Viento (m/s)",
        "precipitation_label": "Precipitación (mm/día)",
        "cloud_cover_label": "Cobertura de Nubes (%)",
        "climate_data": "🌤️ Datos Climáticos",
        "climate_manual_note": "Ajuste valores o haga clic en Obtener para datos reales",
        "gates_passed": "Puertas de pre-evaluación aprobadas",
        "gate_detail_g1": "G1 — Estado del terreno: no protegido/humedal",
        "gate_detail_g2": "G2 — Distancia a la red dentro de 8 km",
        "gate_detail_g3": "G3 — Irradiación solar superior a 3,5 kWh/m²/día",
        "gate_detail_g4": "G4 — Tamaño de parcela adecuado",
        "search_address": "Buscar dirección",
        "search_address_placeholder": "ej. Sevilla, España",
        "search_button": "Buscar",
        "searching_address": "Buscando dirección...",
        "address_not_found": "Dirección no encontrada. Intente otra búsqueda.",
        "address_found": "Ubicación actualizada desde la búsqueda.",
        "draw_parcel": "Dibuje el límite de la parcela en el mapa (herramienta polígono)",
        "polygon_area_detected": "Área de parcela detectada desde el dibujo",
        "map_instructions": "Use la herramienta de polígono a la izquierda para delinear su parcela.",
        "auto_detect_btn": "Detectar Propiedades del Sitio",
        "detecting_properties": "Detectando distancia a la red y terreno...",
        "detection_success": "Detectado automáticamente",
        "detection_grid_fail": "No se pudo detectar la distancia a la red (sin subestaciones cercanas).",
        "detection_terrain_fail": "API de elevación no disponible — terreno estimado por país.",
        "about_problem": "## Problema",
        "about_problem_text": (
            "La UE apunta a 700 GW de solar para 2030, pero los propietarios en el sur de Europa "
            "no tienen herramientas basadas en datos para evaluar la viabilidad antes de contratar consultores."
        ),
        "about_solution": "## Solución",
        "about_solution_text": (
            "Un sistema de pre-evaluación basado en CrewAI que predice la viabilidad solar, "
            "clasifica niveles de riesgo, estima la producción de energía y conecta sitios viables "
            "con instaladores regionales."
        ),
        "about_architecture": "## Arquitectura",
        "about_architecture_text": (
            "- **Crew 1 — Inteligencia Territorial:** 4 agentes (ingestión, limpieza, EDA, contrato)\n"
            "- **Puerta de Validación:** Verificación de esquema antes del ML\n"
            "- **Crew 2 — Predicción:** 4 agentes (validador, features, entrenamiento, evaluación)\n"
            "- **Puertas de Eliminación:** G1–G4 filtros antes de la clasificación\n"
            "- **Frontend:** Streamlit multilingüe (EN/PT/ES/EL)"
        ),
        "about_ethics": "## Ética y Limitaciones",
        "about_ethics_text": (
            "- **Sesgo regional:** Más datos de entrenamiento para España e Italia\n"
            "- **Falsos positivos:** Sitios marginales pueden recibir evaluaciones optimistas\n"
            "- **Conversión de tierras:** Desarrollo solar en tierras agrícolas tiene compensaciones\n"
            "- **Solo preliminar:** Consulte siempre a un profesional calificado"
        ),
        "about_stack": "## Tecnologías",
        "about_stack_text": "CrewAI Flow, Python, Pandas, Scikit-Learn, Matplotlib, Seaborn, Streamlit",
        "about_course": "## Curso",
        "about_course_text": "Desarrollo de IA y Colaboración — Universidad Hebrea 2026 — Dr. Zvi Ben Ami",
        # Pre-qualification (Step 1)
        "prequalify_heading": "Pre-verificación Rápida",
        "land_size_question": "¿Qué tamaño tiene su terreno?",
        "land_size_option_small": "Menos de 1 hectárea",
        "land_size_option_medium": "1–5 hectáreas",
        "land_size_option_large": "5–50 hectáreas",
        "land_size_option_xlarge": "50+ hectáreas",
        "land_size_rooftop_hint": "Para parcelas de menos de 2 ha, considere una evaluación de techo.",
        "lead_name": "Su nombre",
        "lead_email": "Correo electrónico",
        "lead_optional_note": "Opcional — le enviaremos su informe aquí",
        # Step 2 advanced toggle
        "advanced_coords": "Avanzado: Coordenadas manuales",
        # Step 3 paid report CTA
        "cta_headline": "Su informe completo y personalizado de subvenciones + instaladores, entregado por email en 24 horas.",
        "cta_button": "Obtener mi informe detallado €29 →",
        "cta_trust": "Pago seguro con Lemon Squeezy. IVA de la UE incluido.",
        "cta_not_viable_note": (
            "Según estos datos, la energía solar no parece viable aquí. "
            "El informe detallado solo se ofrece para propiedades viables — "
            "ajuste sus datos si cree que la evaluación es incorrecta."
        ),
    },
    "EL": {
        "title": "☀️ RenewView",
        "subtitle": "Μάθετε πόσα μπορεί να αποδώσει η γη σας από την ηλιακή ενέργεια.",
        "intro": "Δωρεάν αξιολόγηση σε λιγότερο από 2 λεπτά για ιδιοκτήτες γης σε Πορτογαλία, Ισπανία και Ελλάδα.",
        "location": "📍 Τοποθεσία",
        "details": "🏗️ Στοιχεία Ακινήτου",
        "country": "Χώρα",
        "latitude": "Γεωγραφικό Πλάτος",
        "longitude": "Γεωγραφικό Μήκος",
        "site_type": "Τύπος Χώρου",
        "ground_parcel": "Οικόπεδο",
        "commercial_rooftop": "Εμπορική Στέγη",
        "parking_structure": "Χώρος Στάθμευσης",
        "parcel_size": "Μέγεθος (εκτάρια)",
        "usable_area": "Χρήσιμη Επιφάνεια (m²)",
        "grid_distance": "Απόσταση από Δίκτυο (km)",
        "terrain": "Τύπος Εδάφους",
        "land_status": "Κατάσταση Γης",
        "run_assessment": "🔍 Εκτέλεση Αξιολόγησης",
        "start_assessment": "🚀 Νέα Αξιολόγηση",
        "back_to_home": "Επιστροφή",
        "back_to_inputs": "Πίσω στα Δεδομένα",
        "new_assessment": "🔄 Νέα Αξιολόγηση",
        "results": "📊 Αποτελέσματα",
        "viability": "Βιωσιμότητα",
        "score": "Βαθμολογία",
        "annual_kwh": "Ετήσιες kWh (εκτ.)",
        "annual_revenue": "Ετήσια Έσοδα (εκτ.)",
        "connect_installer": "🔗 Συνδεθείτε με τοπικό εγκαταστάτη για λεπτομερή αξιολόγηση",
        "not_viable_msg": "Αυτός ο χώρος δεν πέρασε τον προέλεγχο.",
        "disclaimer": "⚠️ Προκαταρκτική αξιολόγηση. Συμβουλευτείτε ειδικό.",
        "map_preview": "Προεπισκόπηση επιλεγμένης τοποθεσίας",
        "about": "Σχετικά με το RenewView",
        "ethics_title": "Ηθική & Περιορισμοί",
        "model_not_ready": "⚠️ Μοντέλο μη εκπαιδευμένο. Εκτελέστε `crewai flow kickoff`. Ευρετικά αποτελέσματα.",
        "eliminated_by": "Αποκλείστηκε από Πύλη",
        "reason": "Αιτία",
        "redirect": "Σύσταση",
        "flags": "Σημειώσεις",
        "sidebar_about_text": (
            "**RenewView** χρησιμοποιεί AI πολλαπλών πρακτόρων για αξιολόγηση ηλιακής βιωσιμότητας.\n\n"
            "**Διαδικασία:**\n"
            "1. Πύλες αποκλεισμού (προστατευόμενη γη, απόσταση δικτύου, ακτινοβολία)\n"
            "2. Ταξινόμηση ML (Random Forest / Gradient Boosting)\n"
            "3. Εκτίμηση ενέργειας και εσόδων\n\n"
            "**Δεδομένα:** NASA POWER API + OpenStreetMap\n\n"
            "**Περιοχές:** Πορτογαλία, Ισπανία, Ελλάδα, Ιταλία"
        ),
        "sidebar_ethics_text": (
            "- Προκατάληψη σε περιοχές με πλούσια δεδομένα (Ισπανία, Ιταλία)\n"
            "- Κίνδυνος ψευδών θετικών σε οριακές τοποθεσίες\n"
            "- Ανταλλαγές στη μετατροπή γεωργικής γης\n"
            "- Συμβουλευτείτε πάντα ειδικό πριν επενδύσετε"
        ),
        "tab_assessment": "🔍 Αξιολόγηση",
        "tab_about": "ℹ️ Σχετικά",
        "fetch_solar_data": "☀️ Λήψη Ηλιακών Δεδομένων από NASA",
        "fetching_data": "Λήψη ηλιακών δεδομένων από NASA POWER...",
        "solar_data_loaded": "Ηλιακά δεδομένα φορτώθηκαν από NASA POWER API",
        "solar_data_error": "Αδυναμία λήψης ηλιακών δεδομένων. Χρήση εκτιμήσεων.",
        "ghi_label": "GHI (kWh/m²/ημέρα)",
        "dni_label": "DNI (kWh/m²/ημέρα)",
        "temperature_label": "Θερμοκρασία (°C)",
        "humidity_label": "Υγρασία (%)",
        "wind_speed_label": "Ταχύτητα Ανέμου (m/s)",
        "precipitation_label": "Βροχόπτωση (mm/ημέρα)",
        "cloud_cover_label": "Νεφοκάλυψη (%)",
        "climate_data": "🌤️ Κλιματικά Δεδομένα",
        "climate_manual_note": "Ρυθμίστε τιμές ή κάντε κλικ Λήψη για πραγματικά δεδομένα",
        "gates_passed": "Πύλες προελέγχου εγκρίθηκαν",
        "gate_detail_g1": "G1 — Κατάσταση γης: μη προστατευόμενη/υγρότοπος",
        "gate_detail_g2": "G2 — Απόσταση δικτύου εντός 8 km",
        "gate_detail_g3": "G3 — Ηλιακή ακτινοβολία πάνω από 3,5 kWh/m²/ημέρα",
        "gate_detail_g4": "G4 — Μέγεθος αγροτεμαχίου επαρκές",
        "search_address": "Αναζήτηση διεύθυνσης",
        "search_address_placeholder": "π.χ. Αθήνα, Ελλάδα",
        "search_button": "Αναζήτηση",
        "searching_address": "Αναζήτηση διεύθυνσης...",
        "address_not_found": "Η διεύθυνση δεν βρέθηκε. Δοκιμάστε άλλη αναζήτηση.",
        "address_found": "Η τοποθεσία ενημερώθηκε από την αναζήτηση.",
        "draw_parcel": "Σχεδιάστε το όριο του αγροτεμαχίου στον χάρτη (εργαλείο πολυγώνου)",
        "polygon_area_detected": "Εντοπίστηκε εμβαδόν αγροτεμαχίου από το σχέδιο",
        "map_instructions": "Χρησιμοποιήστε το εργαλείο πολυγώνου αριστερά για να σκιαγραφήσετε το αγροτεμάχιό σας.",
        "auto_detect_btn": "Αυτόματη Ανίχνευση Ιδιοτήτων",
        "detecting_properties": "Ανίχνευση απόστασης δικτύου και εδάφους...",
        "detection_success": "Αυτόματη ανίχνευση",
        "detection_grid_fail": "Δεν ήταν δυνατή η ανίχνευση απόστασης δικτύου (χωρίς κοντινούς υποσταθμούς).",
        "detection_terrain_fail": "API υψομέτρου μη διαθέσιμο — έδαφος εκτιμήθηκε από τη χώρα.",
        "about_problem": "## Πρόβλημα",
        "about_problem_text": (
            "Η ΕΕ στοχεύει σε 700 GW ηλιακής ενέργειας μέχρι το 2030, αλλά οι ιδιοκτήτες "
            "στη Νότια Ευρώπη δεν έχουν εργαλεία βασισμένα σε δεδομένα για αξιολόγηση βιωσιμότητας."
        ),
        "about_solution": "## Λύση",
        "about_solution_text": (
            "Ένα σύστημα προελέγχου βασισμένο σε CrewAI που προβλέπει ηλιακή βιωσιμότητα, "
            "ταξινομεί επίπεδα κινδύνου, εκτιμά παραγωγή ενέργειας και συνδέει βιώσιμες "
            "τοποθεσίες με περιφερειακούς εγκαταστάτες."
        ),
        "about_architecture": "## Αρχιτεκτονική",
        "about_architecture_text": (
            "- **Crew 1 — Εδαφική Νοημοσύνη:** 4 πράκτορες (εισαγωγή, καθαρισμός, EDA, συμβόλαιο)\n"
            "- **Πύλη Επικύρωσης:** Έλεγχος σχήματος πριν το ML\n"
            "- **Crew 2 — Πρόβλεψη:** 4 πράκτορες (επικυρωτής, features, εκπαίδευση, αξιολόγηση)\n"
            "- **Πύλες Αποκλεισμού:** G1–G4 φίλτρα πριν την ταξινόμηση\n"
            "- **Frontend:** Πολυγλωσσικό Streamlit (EN/PT/ES/EL)"
        ),
        "about_ethics": "## Ηθική & Περιορισμοί",
        "about_ethics_text": (
            "- **Περιφερειακή προκατάληψη:** Περισσότερα δεδομένα εκπαίδευσης για Ισπανία και Ιταλία\n"
            "- **Ψευδή θετικά:** Οριακές τοποθεσίες μπορεί να λάβουν αισιόδοξες αξιολογήσεις\n"
            "- **Μετατροπή γης:** Ηλιακή ανάπτυξη σε γεωργική γη έχει ανταλλαγές\n"
            "- **Μόνο προκαταρκτική:** Συμβουλευτείτε πάντα ειδικό"
        ),
        "about_stack": "## Τεχνολογίες",
        "about_stack_text": "CrewAI Flow, Python, Pandas, Scikit-Learn, Matplotlib, Seaborn, Streamlit",
        "about_course": "## Μάθημα",
        "about_course_text": "Ανάπτυξη AI & Συνεργασία — Εβραϊκό Πανεπιστήμιο 2026 — Dr. Zvi Ben Ami",
        # Pre-qualification (Step 1)
        "prequalify_heading": "Γρήγορος Προέλεγχος",
        "land_size_question": "Πόσο μεγάλο είναι το οικόπεδό σας;",
        "land_size_option_small": "Λιγότερο από 1 εκτάριο",
        "land_size_option_medium": "1–5 εκτάρια",
        "land_size_option_large": "5–50 εκτάρια",
        "land_size_option_xlarge": "50+ εκτάρια",
        "land_size_rooftop_hint": "Για αγροτεμάχια κάτω από 2 ha, εξετάστε αξιολόγηση στέγης.",
        "lead_name": "Το όνομά σας",
        "lead_email": "Διεύθυνση email",
        "lead_optional_note": "Προαιρετικό — θα στείλουμε την αναφορά σας εδώ",
        # Step 2 advanced toggle
        "advanced_coords": "Για προχωρημένους: Χειροκίνητες συντεταγμένες",
        # Step 3 paid report CTA
        "cta_headline": "Η πλήρης εξατομικευμένη αναφορά σας για επιδοτήσεις + εγκαταστάτες, παραδίδεται μέσω email εντός 24 ωρών.",
        "cta_button": "Λάβετε την αναλυτική μου αναφορά €29 →",
        "cta_trust": "Ασφαλής πληρωμή μέσω Lemon Squeezy. Συμπεριλαμβάνεται ΦΠΑ ΕΕ.",
        "cta_not_viable_note": (
            "Με βάση αυτά τα δεδομένα, η ηλιακή ενέργεια δεν φαίνεται βιώσιμη εδώ. "
            "Η αναλυτική αναφορά προσφέρεται μόνο για βιώσιμα ακίνητα — "
            "προσαρμόστε τα δεδομένα σας αν πιστεύετε ότι η αξιολόγηση είναι λανθασμένη."
        ),
    },
}


def t(key: str, lang: str = "EN") -> str:
    """Get translation for key in given language. Falls back to EN."""
    return TRANSLATIONS.get(lang, TRANSLATIONS["EN"]).get(
        key, TRANSLATIONS["EN"].get(key, key)
    )
