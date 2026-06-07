import pandas as pd
import os
from typing import Optional, Tuple

INTERNAL_DATA_PATH = "business_data.csv"

def load_and_prepare_data(file_obj) -> Optional[pd.DataFrame]:
    """
    Lädt eine hochgeladene Datei (CSV oder Excel) und bereitet sie für den Agenten vor.
    
    Args:
        file_obj: Das von Gradio hochgeladene Dateiobjekt.
        
    Returns:
        pd.DataFrame: Der geladene DataFrame oder None bei Fehler.
    """
    if file_obj is None:
        return None
    
    try:
        # Dateiendung prüfen
        file_ext = os.path.splitext(file_obj.name)[1].lower()
        
        if file_ext == ".xlsx":
            df = pd.read_excel(file_obj.name)
        elif file_ext == ".csv":
            try:
                df = pd.read_csv(file_obj.name)
            except Exception:
                df = pd.read_csv(file_obj.name, sep=None, engine='python')
        else:
            raise ValueError(f"Nicht unterstütztes Format: {file_ext}")
        
        # Speichern für den Agenten
        df.to_csv(INTERNAL_DATA_PATH, index=False)
        return df
    except Exception as e:
        print(f"DEBUG: Fehler beim Laden der Datei: {e}")
        return None

def generate_data_overview_md(df: pd.DataFrame) -> str:
    """
    Erstellt eine formatierte Markdown-Übersicht der Daten.
    """
    if df is None or df.empty:
        return "⚠️ Keine Daten verfügbar oder Datei konnte nicht gelesen werden."
    
    return (
        f"### 📊 Datenübersicht\n"
        f"- **Datensätze:** {len(df)}\n"
        f"- **Spalten:** {len(df.columns)}\n"
        f"- **Struktur:** `{', '.join(df.columns.tolist())}`"
    )