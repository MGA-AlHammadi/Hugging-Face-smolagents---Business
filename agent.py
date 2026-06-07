import os
from dotenv import load_dotenv
from smolagents import CodeAgent, InferenceClientModel

# Zentrale Konfiguration
CHART_FILENAME = "chart.png"
MODEL_ID = "Qwen/Qwen2.5-Coder-32B-Instruct"

# API-Keys aus .env laden
load_dotenv()

def run_business_analysis(user_query, hf_token=None):
    """
    Kernfunktion: Initialisiert die KI und führt den Python-Code zur Analyse aus.
    """
    # Sicherheit: Token aus UI bevorzugen, sonst aus Umgebungsvariablen
    active_token = hf_token.strip() if hf_token and hf_token.strip() else os.getenv("HF_TOKEN")
    
    if not active_token:
        return "❌ Fehler: Kein API-Token gefunden.", None
    
    # Sicherstellen, dass die Datei existiert, bevor der Agent startet
    if not os.path.exists("business_data.csv"):
        return "❌ Fehler: Datenbasis fehlt. Bitte Datei hochladen.", None

    try:
        # Modell-Anbindung konfigurieren
        model = InferenceClientModel(model_id=MODEL_ID, token=active_token)
        
        # Der CodeAgent darf Python-Bibliotheken zur Analyse nutzen
        agent = CodeAgent(
            tools=[], 
            model=model,
            additional_authorized_imports=["pandas", "matplotlib", "matplotlib.pyplot", "seaborn", "numpy"],
            add_base_tools=True
        )
        
        # System-Anweisung: Definiert Rolle und Regeln für die KI
        instruction = f"""
        Du bist ein Business Analyst. Nutze die Daten in 'business_data.csv'.
        Anfrage: "{user_query}"
        
        Regeln:
        1. Antworte immer auf Deutsch.
        2. Visualisierungen MÜSSEN als '{CHART_FILENAME}' gespeichert werden.
        3. Nutze saubere Diagramm-Beschriftungen.
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