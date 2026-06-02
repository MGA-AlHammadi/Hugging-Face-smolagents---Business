import os
from dotenv import load_dotenv
from smolagents import CodeAgent, InferenceClientModel

# Konstanten für den Agenten
CHART_FILENAME = "chart.png"
MODEL_ID = "Qwen/Qwen2.5-Coder-32B-Instruct"

# Umgebungsvariablen laden
load_dotenv()

def run_business_analysis(user_query, hf_token=None):
    """
    Initialisiert den CodeAgent und führt die Analyse basierend auf 
    der 'business_data.csv' aus.
    """
    # Token-Priorisierung: UI-Eingabe > .env Datei
    active_token = hf_token.strip() if hf_token and hf_token.strip() else os.getenv("HF_TOKEN")
    
    if not active_token:
        return "❌ Fehler: Kein Hugging Face Token gefunden.", None
    
    if not os.path.exists("business_data.csv"):
        return "❌ Fehler: Keine Datendatei gefunden. Bitte zuerst hochladen.", None

    try:
        # KI-Modell initialisieren
        model = InferenceClientModel(model_id=MODEL_ID, token=active_token)
        
        # Agent konfigurieren
        agent = CodeAgent(
            tools=[], 
            model=model,
            additional_authorized_imports=["pandas", "matplotlib", "matplotlib.pyplot", "seaborn", "numpy"],
            add_base_tools=True
        )
        
        # System-Prompt für professionelle Ergebnisse
        instruction = f"""
        Du bist ein Business Data Analyst. Analysiere die Datei 'business_data.csv'.
        Anfrage: "{user_query}"
        
        WICHTIG:
        - Antworte auf Deutsch.
        - Diagramme IMMER als '{CHART_FILENAME}' speichern.
        - Achte auf saubere Beschriftungen im Plot.
        """
        
        # Vorheriges Diagramm löschen, um Verwechslungen zu vermeiden
        if os.path.exists(CHART_FILENAME):
            os.remove(CHART_FILENAME)
            
        # Agenten-Ausführung
        response = agent.run(instruction)
        
        # Prüfen, ob ein neues Bild erstellt wurde
        image_path = CHART_FILENAME if os.path.exists(CHART_FILENAME) else None
        
        return response, image_path

    except Exception as e:
        error_msg = f"❌ Analysefehler: {str(e)}"
        if "401" in str(e):
            error_msg += "\n\nHinweis: Der API-Token ist ungültig."
        return error_msg, None