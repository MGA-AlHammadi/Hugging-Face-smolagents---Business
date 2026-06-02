import subprocess
import sys
import os

CHART_FILENAME = "chart.png"

# 1. Automatische Installation fehlender Bibliotheken
# (Wichtig: Das Dictionary ordnet dem Modulnamen den Paketnamen für pip zu)
REQUIRED_PACKAGES = {
    "smolagents": "smolagents",
    "gradio": "gradio",
    "pandas": "pandas",
    "matplotlib": "matplotlib",
    "seaborn": "seaborn",
    "huggingface_hub": "huggingface_hub",
    "duckduckgo_search": "duckduckgo-search",
    "ddgs": "ddgs",
    "dotenv": "python-dotenv"
}

for module_name, package_name in REQUIRED_PACKAGES.items():
    try:
        __import__(module_name)
    except ImportError:
        print(f"Bibliothek '{package_name}' fehlt. Installiere automatisch...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", package_name])

# Erst nach Überprüfung die Bibliotheken importieren
import gradio as gr
import pandas as pd
from smolagents import CodeAgent, InferenceClientModel
from dotenv import load_dotenv

# .env Datei laden
load_dotenv()

# 2. Funktion für die Datenanalyse (Backend)
def analyze_business_data(hf_token, file, user_query):
    # Nutze den eingegebenen Token oder, falls leer, den aus der .env Datei
    active_token = hf_token.strip() if hf_token and hf_token.strip() else os.getenv("HF_TOKEN")
    
    # Validierung
    if not active_token or not active_token.startswith("hf_"):
        return "Kein gültiger API-Token gefunden! Bitte gib einen Token ein oder setze ihn in der .env Datei.", None
    
    if file is None:
        return "Bitte laden Sie zuerst eine CSV-Datei hoch!", None
    
    try:
        # KI-Modell mit dem gewählten Token initialisieren
        model = InferenceClientModel(model_id="Qwen/Qwen2.5-Coder-32B-Instruct", token=active_token)
        
        # Agent erstellen
        agent = CodeAgent(
            tools=[], 
            model=model,
            additional_authorized_imports=["pandas", "matplotlib", "matplotlib.pyplot", "seaborn"],
            add_base_tools=True
        )
        
        # Datei speichern
        df = pd.read_csv(file.name)
        df.to_csv("business_data.csv", index=False)
        
        # System-Anweisung für den Agenten
        full_instruction = f"""
        Du bist ein professioneller Datenanalyst für ein Unternehmen.
        Du hast eine Datendatei namens 'business_data.csv'.
        Die Anfrage des Nutzers lautet: "{user_query}"
        
        WICHTIGE ANWEISUNGEN:
        1. Antworte komplett auf Deutsch.
        2. Wenn der Nutzer ein Diagramm (Plot/Chart) anfordert, speichere es IMMER als '{CHART_FILENAME}'.
        3. Nutze deutsche Beschriftungen (Labels und Titel) im Diagramm.
        """
        
        # Agent startet die Analyse
        agent_response = agent.run(full_instruction)
        
        # Prüfen, ob ein Diagramm erstellt wurde
        image_path = CHART_FILENAME if os.path.exists(CHART_FILENAME) else None
        return agent_response, image_path
        
    except Exception as e:
        return f"Ein Fehler ist aufgetreten: {str(e)}\nBitte überprüfen Sie Ihren API-Token.", None

# 3. Benutzeroberfläche erstellen (Frontend mit Gradio)
with gr.Blocks() as demo:
    gr.Markdown("# 📊 KI-gestützter Business Data Analyst (smolagents)")
    gr.Markdown("Richten Sie Ihren API-Zugang ein, laden Sie Ihre CSV-Datei hoch und starten Sie die autonome Analyse.")
    
    with gr.Row():
        with gr.Column():
            # Feld für den API-Token (Bleibt leer für maximale Sicherheit)
            token_input = gr.Textbox(
                label="1. Hugging Face Access Token (Optional, falls .env genutzt wird)", 
                placeholder="hf_...",
                type="password"
            )
            file_input = gr.File(label="2. CSV-Datei hochladen", file_types=[".csv"])
            query_input = gr.Textbox(
                label="3. Was möchten Sie wissen?", 
                placeholder="z.B.: Zeige mir den Umsatz pro Produkt als Balkendiagramm.",
                lines=3
            )
            submit_btn = gr.Button("Analyse starten 🚀", variant="primary")
            
        with gr.Column():
            output_text = gr.Textbox(label="KI-Analysenbericht", lines=10)
            output_image = gr.Image(label="Generiertes Diagramm")
            
    # Button-Klick verknüpfen
    submit_btn.click(
        fn=analyze_business_data, 
        inputs=[token_input, file_input, query_input], 
        outputs=[output_text, output_image]
    )

if __name__ == "__main__":
    if os.path.exists(CHART_FILENAME):
        os.remove(CHART_FILENAME)
    demo.launch(theme=gr.themes.Soft())