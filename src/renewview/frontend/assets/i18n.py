"""Internationalization — EN / PT / ES / EL translations."""

TRANSLATIONS = {
    "EN": {
        "title": "☀️ RenewView",
        "subtitle": "Find out what your land could earn from solar.",
        "intro": "Portugal-focused solar viability preview for property owners.",
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
            "**RenewView** gives property owners in Portugal a quick first look at solar potential.\n\n"
            "**What it checks:**\n"
            "1. Property and roof/site basics\n"
            "2. Local solar conditions\n"
            "3. Estimated production and financial upside\n\n"
            "**Designed for:** Portuguese properties"
        ),
        "sidebar_ethics_text": (
            "- This is an early screening, not a final engineering survey\n"
            "- Marginal properties can be over- or under-estimated\n"
            "- Roof condition, permits, and installer review still matter\n"
            "- Consult a qualified professional before investing"
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
            "Many property owners in Portugal have no simple way to preview solar viability "
            "before speaking with installers or consultants."
        ),
        "about_solution": "## Solution",
        "about_solution_text": (
            "A Portugal-focused pre-screening tool that estimates solar feasibility, "
            "risk tier, energy output, and the next practical steps for viable properties."
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
            "- **Preliminary only:** This is not a final engineering survey\n"
            "- **False positives:** Marginal properties may receive optimistic assessments\n"
            "- **Local constraints:** Permits, roof condition, and installer review still matter\n"
            "- **Professional review:** Always consult a qualified professional"
        ),
        "about_stack": "## Stack",
        "about_stack_text": "CrewAI Flow, Python, Pandas, Scikit-Learn, Matplotlib, Seaborn, Streamlit",
        "about_course": "## Course",
        "about_course_text": "AI Development & Collaboration — Hebrew University 2026 — Dr. Zvi Ben Ami",
        # Pre-qualification (Step 1)
        "prequalify_heading": "Quick Pre-Check",
        "precheck_note": "Answer three quick details to start a Portugal-focused solar preview.",
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
        "cta_headline": "Your full personalized solar potential + installer report, delivered by email within 24 hours.",
        "cta_button": "Get my €29 detailed report →",
        "cta_trust": "Secure checkout by Lemon Squeezy. EU VAT included.",
        "cta_not_viable_note": (
            "Based on these inputs, solar doesn't look viable here. "
            "The detailed report is offered only for viable properties — "
            "adjust your inputs if you think the assessment is off."
        ),
        # Residential roof — site type + inputs
        "residential_roof": "Residential Roof",
        "roof_area": "Roof Area (m²)",
        "roof_orientation": "Roof Orientation",
        "roof_shading": "Shading Level",
        "orient_s": "South",
        "orient_se": "Southeast",
        "orient_sw": "Southwest",
        "orient_e": "East",
        "orient_w": "West",
        "orient_n": "North",
        "shading_none": "None",
        "shading_light": "Light",
        "shading_moderate": "Moderate",
        "shading_heavy": "Heavy",
        # Residential roof — result labels
        "est_annual_production": "Est. Annual Production",
        "annual_savings": "Est. Annual Savings",
        "system_size": "System Size",
        "payback_period": "Payback Period",
        "years_unit": "years",
        "net_savings_25yr": "25-Year Net Savings",
        "local_incentives_note": (
            "Many regions offer solar incentives or financing. "
            "Check with your local authority or energy provider for what's available where you live."
        ),
        # Residential roof — gate descriptions
        "roof_gate_g1": "G1 — Roof orientation usable for solar",
        "roof_gate_g2": "G2 — Shading level acceptable",
        "roof_gate_g3": "G3 — Solar irradiance above 3.5 kWh/m²/day",
        "roof_gate_g4": "G4 — System size in viable range (1.5–15 kWp)",
    },
    "PT": {
        "title": "☀️ RenewView",
        "subtitle": "Descubra quanto o seu terreno pode render com energia solar.",
        "intro": "Pré-visualização de viabilidade solar focada em propriedades em Portugal.",
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
            "**RenewView** dá aos proprietários em Portugal uma primeira leitura do potencial solar.\n\n"
            "**O que verifica:**\n"
            "1. Dados básicos da propriedade e do telhado/local\n"
            "2. Condições solares locais\n"
            "3. Produção estimada e potencial financeiro\n\n"
            "**Criado para:** propriedades em Portugal"
        ),
        "sidebar_ethics_text": (
            "- Esta é uma triagem inicial, não um estudo técnico final\n"
            "- Propriedades marginais podem ser sobre- ou subestimadas\n"
            "- Licenças, estado do telhado e revisão por instalador ainda importam\n"
            "- Consulte um profissional qualificado antes de investir"
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
            "Muitos proprietários em Portugal não têm uma forma simples de prever a "
            "viabilidade solar antes de falar com instaladores ou consultores."
        ),
        "about_solution": "## Solução",
        "about_solution_text": (
            "Uma ferramenta de pré-triagem focada em Portugal que estima a viabilidade "
            "solar, o nível de risco, a produção de energia e os próximos passos práticos."
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
            "- **Apenas preliminar:** Não substitui um estudo técnico final\n"
            "- **Falsos positivos:** Propriedades marginais podem receber avaliações otimistas\n"
            "- **Restrições locais:** Licenças, telhado e revisão por instalador ainda importam\n"
            "- **Revisão profissional:** Consulte sempre um profissional qualificado"
        ),
        "about_stack": "## Tecnologias",
        "about_stack_text": "CrewAI Flow, Python, Pandas, Scikit-Learn, Matplotlib, Seaborn, Streamlit",
        "about_course": "## Curso",
        "about_course_text": "Desenvolvimento de IA e Colaboração — Universidade Hebraica 2026 — Dr. Zvi Ben Ami",
        # Pre-qualification (Step 1)
        "prequalify_heading": "Pré-verificação Rápida",
        "precheck_note": "Responda a três detalhes rápidos para iniciar uma pré-visualização solar focada em Portugal.",
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
        "cta_headline": "O seu relatório completo e personalizado de potencial solar + instaladores, entregue por email em 24 horas.",
        "cta_button": "Obter o meu relatório detalhado €29 →",
        "cta_trust": "Checkout seguro via Lemon Squeezy. IVA da UE incluído.",
        "cta_not_viable_note": (
            "Com base nestes dados, a energia solar não parece viável aqui. "
            "O relatório detalhado é oferecido apenas para propriedades viáveis — "
            "ajuste os seus dados se achar que a avaliação está incorreta."
        ),
        # Residential roof — site type + inputs
        "residential_roof": "Telhado Residencial",
        "roof_area": "Área do Telhado (m²)",
        "roof_orientation": "Orientação do Telhado",
        "roof_shading": "Nível de Sombreamento",
        "orient_s": "Sul",
        "orient_se": "Sudeste",
        "orient_sw": "Sudoeste",
        "orient_e": "Leste",
        "orient_w": "Oeste",
        "orient_n": "Norte",
        "shading_none": "Nenhum",
        "shading_light": "Leve",
        "shading_moderate": "Moderado",
        "shading_heavy": "Intenso",
        # Residential roof — result labels
        "est_annual_production": "Produção Anual Est.",
        "annual_savings": "Poupança Anual Est.",
        "system_size": "Tamanho do Sistema",
        "payback_period": "Período de Retorno",
        "years_unit": "anos",
        "net_savings_25yr": "Poupança Líquida 25 Anos",
        "local_incentives_note": (
            "Muitas regiões oferecem incentivos ou financiamento para energia solar. "
            "Verifique junto da sua autarquia ou fornecedor de energia o que está disponível na sua zona."
        ),
        # Residential roof — gate descriptions
        "roof_gate_g1": "G1 — Orientação do telhado adequada para solar",
        "roof_gate_g2": "G2 — Nível de sombreamento aceitável",
        "roof_gate_g3": "G3 — Irradiação solar acima de 3,5 kWh/m²/dia",
        "roof_gate_g4": "G4 — Tamanho do sistema viável (1,5–15 kWp)",
    },
    "ES": {
        "title": "☀️ RenewView",
        "subtitle": "Descubra cuánto podría rentar su terreno con energía solar.",
        "intro": "Vista previa de viabilidad solar enfocada en propiedades en Portugal.",
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
            "**RenewView** ofrece a propietarios en Portugal una primera lectura del potencial solar.\n\n"
            "**Qué revisa:**\n"
            "1. Datos básicos de la propiedad y del tejado/sitio\n"
            "2. Condiciones solares locales\n"
            "3. Producción estimada y potencial financiero\n\n"
            "**Diseñado para:** propiedades en Portugal"
        ),
        "sidebar_ethics_text": (
            "- Es una evaluación inicial, no un estudio técnico final\n"
            "- Las propiedades marginales pueden sobre- o subestimarse\n"
            "- Permisos, estado del tejado y revisión del instalador siguen siendo importantes\n"
            "- Consulte a un profesional cualificado antes de invertir"
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
        "search_address_placeholder": "ej. Faro, Portugal",
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
            "Muchos propietarios en Portugal no tienen una forma sencilla de prever la "
            "viabilidad solar antes de hablar con instaladores o consultores."
        ),
        "about_solution": "## Solución",
        "about_solution_text": (
            "Una herramienta de pre-evaluación enfocada en Portugal que estima la "
            "viabilidad solar, el nivel de riesgo, la producción de energía y los próximos pasos."
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
            "- **Solo preliminar:** No sustituye un estudio técnico final\n"
            "- **Falsos positivos:** Propiedades marginales pueden recibir evaluaciones optimistas\n"
            "- **Restricciones locales:** Permisos, tejado y revisión del instalador siguen importando\n"
            "- **Revisión profesional:** Consulte siempre a un profesional calificado"
        ),
        "about_stack": "## Tecnologías",
        "about_stack_text": "CrewAI Flow, Python, Pandas, Scikit-Learn, Matplotlib, Seaborn, Streamlit",
        "about_course": "## Curso",
        "about_course_text": "Desarrollo de IA y Colaboración — Universidad Hebrea 2026 — Dr. Zvi Ben Ami",
        # Pre-qualification (Step 1)
        "prequalify_heading": "Pre-verificación Rápida",
        "precheck_note": "Responda tres datos rápidos para iniciar una vista previa solar enfocada en Portugal.",
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
        "cta_headline": "Su informe completo y personalizado de potencial solar + instaladores, entregado por email en 24 horas.",
        "cta_button": "Obtener mi informe detallado €29 →",
        "cta_trust": "Pago seguro con Lemon Squeezy. IVA de la UE incluido.",
        "cta_not_viable_note": (
            "Según estos datos, la energía solar no parece viable aquí. "
            "El informe detallado solo se ofrece para propiedades viables — "
            "ajuste sus datos si cree que la evaluación es incorrecta."
        ),
        # Residential roof — site type + inputs
        "residential_roof": "Tejado Residencial",
        "roof_area": "Área del Tejado (m²)",
        "roof_orientation": "Orientación del Tejado",
        "roof_shading": "Nivel de Sombra",
        "orient_s": "Sur",
        "orient_se": "Sureste",
        "orient_sw": "Suroeste",
        "orient_e": "Este",
        "orient_w": "Oeste",
        "orient_n": "Norte",
        "shading_none": "Ninguna",
        "shading_light": "Ligera",
        "shading_moderate": "Moderada",
        "shading_heavy": "Intensa",
        # Residential roof — result labels
        "est_annual_production": "Producción Anual Est.",
        "annual_savings": "Ahorro Anual Est.",
        "system_size": "Tamaño del Sistema",
        "payback_period": "Periodo de Amortización",
        "years_unit": "años",
        "net_savings_25yr": "Ahorro Neto 25 Años",
        "local_incentives_note": (
            "Muchas regiones ofrecen incentivos o financiación para energía solar. "
            "Consulte con su administración local o proveedor de energía qué opciones existen en su zona."
        ),
        # Residential roof — gate descriptions
        "roof_gate_g1": "G1 — Orientación del tejado adecuada para solar",
        "roof_gate_g2": "G2 — Nivel de sombra aceptable",
        "roof_gate_g3": "G3 — Irradiación solar superior a 3,5 kWh/m²/día",
        "roof_gate_g4": "G4 — Tamaño del sistema viable (1,5–15 kWp)",
    },
    "EL": {
        "title": "☀️ RenewView",
        "subtitle": "Μάθετε πόσα μπορεί να αποδώσει η γη σας από την ηλιακή ενέργεια.",
        "intro": "Προεπισκόπηση ηλιακής βιωσιμότητας για ακίνητα στην Πορτογαλία.",
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
            "**RenewView** δίνει στους ιδιοκτήτες στην Πορτογαλία μια πρώτη εικόνα του ηλιακού δυναμικού.\n\n"
            "**Τι ελέγχει:**\n"
            "1. Βασικά στοιχεία ακινήτου και στέγης/χώρου\n"
            "2. Τοπικές ηλιακές συνθήκες\n"
            "3. Εκτιμώμενη παραγωγή και οικονομική προοπτική\n\n"
            "**Σχεδιασμένο για:** ακίνητα στην Πορτογαλία"
        ),
        "sidebar_ethics_text": (
            "- Πρόκειται για αρχικό έλεγχο, όχι τελική τεχνική μελέτη\n"
            "- Οριακά ακίνητα μπορεί να υπερεκτιμηθούν ή να υποεκτιμηθούν\n"
            "- Άδειες, κατάσταση στέγης και έλεγχος εγκαταστάτη παραμένουν σημαντικά\n"
            "- Συμβουλευτείτε εξειδικευμένο επαγγελματία πριν επενδύσετε"
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
        "search_address_placeholder": "π.χ. Φάρο, Πορτογαλία",
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
            "Πολλοί ιδιοκτήτες στην Πορτογαλία δεν έχουν απλό τρόπο να εκτιμήσουν "
            "την ηλιακή βιωσιμότητα πριν μιλήσουν με εγκαταστάτες ή συμβούλους."
        ),
        "about_solution": "## Λύση",
        "about_solution_text": (
            "Ένα εργαλείο προελέγχου εστιασμένο στην Πορτογαλία που εκτιμά ηλιακή "
            "βιωσιμότητα, επίπεδο κινδύνου, παραγωγή ενέργειας και πρακτικά επόμενα βήματα."
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
            "- **Μόνο προκαταρκτική:** Δεν αντικαθιστά τελική τεχνική μελέτη\n"
            "- **Ψευδή θετικά:** Οριακά ακίνητα μπορεί να λάβουν αισιόδοξες αξιολογήσεις\n"
            "- **Τοπικοί περιορισμοί:** Άδειες, στέγη και έλεγχος εγκαταστάτη παραμένουν σημαντικά\n"
            "- **Επαγγελματικός έλεγχος:** Συμβουλευτείτε πάντα ειδικό"
        ),
        "about_stack": "## Τεχνολογίες",
        "about_stack_text": "CrewAI Flow, Python, Pandas, Scikit-Learn, Matplotlib, Seaborn, Streamlit",
        "about_course": "## Μάθημα",
        "about_course_text": "Ανάπτυξη AI & Συνεργασία — Εβραϊκό Πανεπιστήμιο 2026 — Dr. Zvi Ben Ami",
        # Pre-qualification (Step 1)
        "prequalify_heading": "Γρήγορος Προέλεγχος",
        "precheck_note": "Απαντήστε σε τρία σύντομα στοιχεία για προεπισκόπηση ηλιακής βιωσιμότητας στην Πορτογαλία.",
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
        "cta_headline": "Η πλήρης εξατομικευμένη αναφορά σας για ηλιακό δυναμικό + εγκαταστάτες, παραδίδεται μέσω email εντός 24 ωρών.",
        "cta_button": "Λάβετε την αναλυτική μου αναφορά €29 →",
        "cta_trust": "Ασφαλής πληρωμή μέσω Lemon Squeezy. Συμπεριλαμβάνεται ΦΠΑ ΕΕ.",
        "cta_not_viable_note": (
            "Με βάση αυτά τα δεδομένα, η ηλιακή ενέργεια δεν φαίνεται βιώσιμη εδώ. "
            "Η αναλυτική αναφορά προσφέρεται μόνο για βιώσιμα ακίνητα — "
            "προσαρμόστε τα δεδομένα σας αν πιστεύετε ότι η αξιολόγηση είναι λανθασμένη."
        ),
        # Residential roof — site type + inputs
        "residential_roof": "Στέγη Κατοικίας",
        "roof_area": "Επιφάνεια Στέγης (m²)",
        "roof_orientation": "Προσανατολισμός Στέγης",
        "roof_shading": "Επίπεδο Σκίασης",
        "orient_s": "Νότος",
        "orient_se": "Νοτιοανατολικά",
        "orient_sw": "Νοτιοδυτικά",
        "orient_e": "Ανατολικά",
        "orient_w": "Δυτικά",
        "orient_n": "Βορράς",
        "shading_none": "Καμία",
        "shading_light": "Ελαφριά",
        "shading_moderate": "Μέτρια",
        "shading_heavy": "Έντονη",
        # Residential roof — result labels
        "est_annual_production": "Εκτ. Ετήσια Παραγωγή",
        "annual_savings": "Εκτ. Ετήσια Εξοικονόμηση",
        "system_size": "Μέγεθος Συστήματος",
        "payback_period": "Περίοδος Απόσβεσης",
        "years_unit": "έτη",
        "net_savings_25yr": "Καθαρή Εξοικονόμηση 25 Ετών",
        "local_incentives_note": (
            "Πολλές περιοχές προσφέρουν κίνητρα ή χρηματοδότηση για ηλιακή ενέργεια. "
            "Επικοινωνήστε με την τοπική αρχή ή τον πάροχο ενέργειας σας για να μάθετε τι είναι διαθέσιμο στην περιοχή σας."
        ),
        # Residential roof — gate descriptions
        "roof_gate_g1": "G1 — Ο προσανατολισμός της στέγης είναι κατάλληλος",
        "roof_gate_g2": "G2 — Αποδεκτό επίπεδο σκίασης",
        "roof_gate_g3": "G3 — Ηλιακή ακτινοβολία πάνω από 3,5 kWh/m²/ημέρα",
        "roof_gate_g4": "G4 — Μέγεθος συστήματος σε βιώσιμο εύρος (1,5–15 kWp)",
    },
}


def t(key: str, lang: str = "EN") -> str:
    """Get translation for key in given language. Falls back to EN."""
    return TRANSLATIONS.get(lang, TRANSLATIONS["EN"]).get(
        key, TRANSLATIONS["EN"].get(key, key)
    )
