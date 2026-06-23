import logging
from fpdf import FPDF
import os
from datetime import datetime

# Setup für das Ereignis-Logging (gut für Debugging)
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def create_pdf_report(analysis_text: str, image_path: str = None, mode="📊 Business Analysis Mode") -> str:
    """
    Exportiert die KI-Analyse in ein formatiertes PDF-Dokument.
    """
    # Eindeutiger Zeitstempel für den Dateinamen
    pdf_filename = f"Analysebericht_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
    
    try:
        pdf = FPDF()
        pdf.add_page()
        
        # Titel des Berichts
        pdf.set_font("Arial", "B", 16)
        title = "CRM Analytics Management Bericht" if mode == "👤 CRM Analytics Mode" else "Business Data Analyse Bericht"
        pdf.cell(0, 10, title, ln=True, align="C")
        
        # Untertitel mit Datum
        pdf.set_font("Arial", "I", 10)
        pdf.cell(0, 10, f"Erstellt am: {datetime.now().strftime('%d.%m.%Y %H:%M')}", ln=True, align="C")
        pdf.ln(10)
        
        # Spezieller CRM Abschnitt
        if mode == "👤 CRM Analytics Mode":
            pdf.set_font("Arial", "B", 12)
            pdf.cell(0, 10, "Bericht zur Filialoptimierung und geografischen Analyse", ln=True)
            pdf.set_font("Arial", "", 10)
            pdf.multi_cell(0, 8, "Dieser Abschnitt enthält strategische Empfehlungen zur geografischen Performance.")
            pdf.ln(5)

        # Den Analyse-Text einfügen (UTF-8 Workaround für FPDF)
        pdf.set_font("Arial", "", 12)
        # Text in latin-1 kodieren, um Probleme mit Sonderzeichen zu vermeiden
        safe_text = str(analysis_text).encode('latin-1', 'replace').decode('latin-1')
        pdf.multi_cell(0, 10, safe_text)
        
        # Diagramm einfügen, falls die KI eines generiert hat
        if image_path and os.path.exists(image_path):
            pdf.ln(10)
            # Zentriert das Bild auf der Seite
            pdf.image(image_path, x=10, w=180)
            
        pdf.output(pdf_filename)
        logger.info(f"Bericht generiert: {pdf_filename}")
        return pdf_filename
    except Exception as e:
        logger.error(f"PDF-Fehler: {e}")
        return None

