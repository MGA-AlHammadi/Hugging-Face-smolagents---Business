import os
import logging
import gradio as gr
import pandas as pd
from typing import Tuple, Optional

# Import der logischen Module (Strukturierte Trennung)
from agent import run_business_analysis
from data_loader import load_and_prepare_data, generate_data_overview_md
from utils import create_pdf_report

# Globales Logging Setup
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def process_analysis(hf_token: str, file_obj, user_query: str, mode: str) -> Tuple[str, Optional[str], Optional[str]]:
    """
    Hauptfunktion, die Backend-Logik mit Frontend-Events verbindet.
    """
    # Validierung: Wurden alle nötigen Daten geliefert?
    if not file_obj:
        return "⚠️ Bitte laden Sie zuerst eine Datei hoch.", None, None
    
    if not user_query.strip():
        return "⚠️ Bitte geben Sie eine Frage zur Analyse ein.", None, None

    # 1. Daten vorbereiten (Einlesen & Konvertieren)
    df = load_and_prepare_data(file_obj, mode=mode)
    if df is None:
        return "❌ Datei konnte nicht verarbeitet werden oder falsches Format für den Modus.", None, None

    # 2. KI-Agenten starten (Ergebnisse abholen)
    response_text, image_path = run_business_analysis(user_query, hf_token, mode=mode)
    
    # 3. PDF aus den Ergebnissen erstellen
    pdf_path = create_pdf_report(response_text, image_path, mode=mode)
    
    return response_text, image_path, pdf_path

# Definition der Benutzeroberfläche (Gradio Layout)
with gr.Blocks() as demo:
    gr.Markdown("# 🏢 AI Business Analyst Pro")
    gr.Markdown("Laden Sie Ihre Geschäftsdaten hoch und lassen Sie die KI die strategische Auswertung übernehmen.")
    
    # Modus-Auswahl ganz oben
    mode_selector = gr.Dropdown(
        label="Analysemodus wählen / Select Analysis Mode",
        choices=["📊 Business Analysis Mode", "👤 CRM Analytics Mode"],
        value="📊 Business Analysis Mode",
        interactive=True
    )
    
    with gr.Row():
        # Bereich für Konfiguration und Datei-Upload
        with gr.Column(scale=1):
            token_input = gr.Textbox(
                label="Hugging Face API Token", 
                placeholder="hf_...", 
                type="password",
                info="Optional: Wird nur benötigt, wenn keine .env Datei existiert."
            )
            file_input = gr.File(
                label="Excel/CSV Quelldatei", 
                file_types=[".csv", ".xlsx"]
            )
            gr.Markdown("**Hinweis:** Im CRM-Modus wird eine .xlsx mit den Sheets 'Customers', 'Deals' und 'Interactions' erwartet.")
            data_overview = gr.Markdown("### Status\nWarte auf Datei...")
            
        # Bereich für Nutzeranfragen und Ergebnisse
        with gr.Column(scale=2):
            query_input = gr.Textbox(
                label="Analyse-Auftrag", 
                placeholder="z.B. Erstelle eine Trendanalyse der Verkäufe.", 
                lines=3
            )
            submit_btn = gr.Button("Analyse jetzt starten 🚀", variant="primary")
            
            # Beispiele für neue Nutzer
            gr.Examples(
                examples=[
                    "Fasse die wichtigsten Kennzahlen zusammen.", 
                    "Erstelle ein Diagramm über die Umsatzverteilung.",
                    "Welche Regionen sind am wenigsten profitabel?"
                ],
                inputs=query_input
            )

    # Anzeige-Bereiche für die Analyse-Ergebnisse
    with gr.Row():
        output_text = gr.Textbox(label="Bericht (Text)", lines=10)
        output_image = gr.Image(label="Grafik/Visualisierung")
        output_pdf = gr.File(label="Download PDF-Bericht")

    # Logik: Was passiert bei Interaktionen?
    # Update Status-Text bei Modus-Wechsel
    def update_mode_status(mode):
        if mode == "👤 CRM Analytics Mode":
            return "### Modus: CRM Analytics\nBitte Excel mit 3 Sheets hochladen."
        return "### Modus: Business Analysis\nBitte einzelne CSV/Excel hochladen."

    mode_selector.change(
        fn=update_mode_status,
        inputs=[mode_selector],
        outputs=[data_overview]
    )

    # Wenn eine Datei hochgeladen wird -> Zeige Übersicht
    file_input.change(
        fn=lambda f, m: generate_data_overview_md(load_and_prepare_data(f, mode=m)), 
        inputs=[file_input, mode_selector], 
        outputs=[data_overview]
    )
    
    # Wenn der Start-Button geklickt wird -> Starte Prozess
    submit_btn.click(
        fn=process_analysis, 
        inputs=[token_input, file_input, query_input, mode_selector], 
        outputs=[output_text, output_image, output_pdf]
    )

# App-Start
if __name__ == "__main__":
    logger.info("Anwendung wird gestartet...")
    demo.launch(theme=gr.themes.Soft())