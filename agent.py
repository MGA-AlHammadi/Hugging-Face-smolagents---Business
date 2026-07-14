import os
from dotenv import load_dotenv
from smolagents import CodeAgent, LiteLLMModel

# Zentrale Konfiguration
CHART_FILENAME = "chart.png"
MODEL_ID = "gemini/gemini-2.5-flash"

# API-Keys aus .env laden
load_dotenv()

def run_business_analysis(user_query, hf_token=None, mode="📊 Business Analysis Mode"):
    """
    Kernfunktion: Initialisiert die KI und führt den Python-Code zur Analyse aus.
    """
    # Sicherheit: Gemini API-Key aus Umgebungsvariablen bevorzugen
    gemini_key = os.getenv("GEMINI_API_KEY")
    
    if not gemini_key:
        return "❌ Fehler: Kein GEMINI_API_KEY in der .env gefunden.", None
    
    # Pfad zur Datenbasis bestimmen
    data_file = "crm_master_data.csv" if mode == "👤 CRM Analytics Mode" else "business_data.csv"
    
    # Sicherstellen, dass die Datei existiert, bevor der Agent startet
    if not os.path.exists(data_file):
        return f"❌ Fehler: Datenbasis ({data_file}) fehlt. Bitte Datei hochladen.", None

    try:
        # Modell-Anbindung konfiguriert für Gemini via LiteLLM (smolagents Standard für Gemini)
        model = LiteLLMModel(
            model_id=MODEL_ID,
            api_key=gemini_key
        )
        
        # Der CodeAgent nutzt nun das Gemini-Modell
        agent = CodeAgent(
            tools=[], 
            model=model,
            additional_authorized_imports=["pandas", "matplotlib", "matplotlib.pyplot", "seaborn", "numpy"],
            add_base_tools=True
        )
        
        # System-Anweisung: Definiert Rolle und Regeln für die KI
        validation_instruction = """
        Egal welche Frage der Nutzer stellt oder welcher Modus aktiv ist: Berechne nicht nur die nackten Zahlen, sondern füge im PDF-Bericht immer einen Abschnitt 'Mathematische & Logische Validierung' hinzu. Erkläre dort kurz und präzise auf Deutsch, warum dieses Ergebnis korrekt ist und über welche Code-/Formel-Logik es berechnet wurde (z.B. Erkläre den Rechenweg oder die gefilterten Kriterien), damit der Nutzer die Korrektheit zu 100% nachvollziehen kann.
        """
        
        if mode == "👤 CRM Analytics Mode":
            instruction = f"""
            Du bist der Chief CRM & Sales Analytics Officer. Nutze die Daten in '{data_file}'.
            Die Daten enthalten Kunden-Zusammenführungen (Customers, Deals, Interactions).
            Felder umfassen: customer_id, Standortinformationen (z.B. country, region, branch, location), deal_value, stage (Lead, Negotiation, Won, Lost), und Interaktionsdaten.
            
            Anfrage: "{user_query}"
            
            Regeln:
            1. Antworte immer auf Deutsch.
            2. Visualisierungen MÜSSEN als '{CHART_FILENAME}' gespeichert werden.
            3. CRM-Kernmetriken (Standardanalysen):
               - Identifiziere die Top 5 Kunden nach Umsatzpotenzial.
               - Analysiere die Conversion Rate zwischen den Phasen Lead, Negotiation und Won.
               - Hebe Kunden mit hohem Risiko für Abwanderung (Churn Risk aufgrund mangelnder Interaktionen) hervor.
            4. Geografische Analyse & Management-Warnungen:
               - Falls Spalten wie 'country', 'region', 'branch', 'location' oder ähnliche vorhanden sind, führe eine Standort-Performance-Analyse durch.
               - Falls die Daten auf eine qualitative und quantitative Unterperformance hinweisen (unter Berücksichtigung des Gesamtwerts der Won-Deals vs. Lost-Deals), formuliere eine Management-Warnung.
               - Begründe Warnungen streng mit den vorliegenden Kennzahlen (Umsatz, Margen, Quoten), um Halluzinationen zu vermeiden.
            5. Erstelle klare Handlungsempfehlungen für das Management.
            {validation_instruction}
            """
        else:
            instruction = f"""
            Du bist ein Business Analyst. Nutze die Daten in '{data_file}'.
            Anfrage: "{user_query}"
            
            Regeln:
            1. Antworte immer auf Deutsch.
            2. Visualisierungen MÜSSEN als '{CHART_FILENAME}' gespeichert werden.
            3. Nutze saubere Diagramm-Beschriftungen.
            {validation_instruction}
            """
        
        # Bereinigung: Altes Bild löschen, falls vorhanden
        if os.path.exists(CHART_FILENAME):
            os.remove(CHART_FILENAME)
            
        # Agent führt den generierten Python-Code aus
        response = agent.run(instruction)
        
        # Rückgabe von Text und (falls erstellt) Bildpfad
        image_path = CHART_FILENAME if os.path.exists(CHART_FILENAME) else None
        
        return response, image_path

    except Exception as e:
        error_msg = f"❌ Analysefehler: {str(e)}"
        return error_msg, None