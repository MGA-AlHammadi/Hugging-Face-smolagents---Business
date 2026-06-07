import logging
from fpdf import FPDF
import os
from datetime import datetime

# Setup für das Ereignis-Logging (gut für Debugging)
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def create_pdf_report(analysis_text: str, image_path: str = None) -> str:
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
        pdf.cell(0, 10, "Business Data Analyse Bericht", ln=True, align="C")
        
        # Untertitel mit Datum
        pdf.set_font("Arial", "I", 10)
        pdf.cell(0, 10, f"Erstellt am: {datetime.now().strftime('%d.%m.%Y %H:%M')}", ln=True, align="C")
        pdf.ln(10)
        
        # Den Analyse-Text einfügen (UTF-8 Workaround für FPDF)
        pdf.set_font("Arial", "", 12)
        pdf.multi_cell(0, 10, analysis_text.encode('latin-1', 'replace').decode('latin-1'))
        
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

