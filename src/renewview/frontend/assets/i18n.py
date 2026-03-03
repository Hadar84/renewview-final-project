"""Internationalization — EN / PT / ES / EL translations."""

TRANSLATIONS = {
    "EN": {
        "title": "☀️ RenewView",
        "subtitle": "Solar Energy Land Viability Assessment — Southern Europe",
        "intro": "Enter your property details to receive an AI-powered viability assessment.",
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
        "sidebar_built_with": "Built with CrewAI, Scikit-Learn & Streamlit",
        "sidebar_course": "Final Project — AI Development Course 2026",
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
    },
    "PT": {
        "title": "☀️ RenewView",
        "subtitle": "Avaliação de Viabilidade de Energia Solar — Sul da Europa",
        "intro": "Insira os dados da sua propriedade para receber uma avaliação de viabilidade.",
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
        "sidebar_built_with": "Desenvolvido com CrewAI, Scikit-Learn e Streamlit",
        "sidebar_course": "Projeto Final — Curso de IA 2026",
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
    },
    "ES": {
        "title": "☀️ RenewView",
        "subtitle": "Evaluación de Viabilidad Solar — Sur de Europa",
        "intro": "Ingrese los datos de su propiedad para una evaluación de viabilidad.",
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
        "sidebar_built_with": "Desarrollado con CrewAI, Scikit-Learn y Streamlit",
        "sidebar_course": "Proyecto Final — Curso de IA 2026",
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
    },
    "EL": {
        "title": "☀️ RenewView",
        "subtitle": "Αξιολόγηση Βιωσιμότητας Ηλιακής Ενέργειας — Νότια Ευρώπη",
        "intro": "Εισάγετε τα στοιχεία του ακινήτου σας για αξιολόγηση βιωσιμότητας.",
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
        "sidebar_built_with": "Αναπτύχθηκε με CrewAI, Scikit-Learn & Streamlit",
        "sidebar_course": "Τελικό Πρόγραμμα — Μάθημα AI 2026",
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
    },
}


def t(key: str, lang: str = "EN") -> str:
    """Get translation for key in given language. Falls back to EN."""
    return TRANSLATIONS.get(lang, TRANSLATIONS["EN"]).get(
        key, TRANSLATIONS["EN"].get(key, key)
    )
