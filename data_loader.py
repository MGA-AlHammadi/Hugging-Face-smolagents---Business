import pandas as pd
import os

INTERNAL_DATA_PATH = "business_data.csv"

def load_and_prepare_data(file_obj):
    """
    Liest eine hochgeladene Datei (CSV oder Excel) ein und speichert sie 
    für den Agenten als standardisierte CSV-Datei zwischen.
    """
    if file_obj is None:
        return None
    
    try:
        # Dateiformat anhand der Endung prüfen
        if file_obj.name.endswith(".xlsx"):
            df = pd.read_excel(file_obj.name)
        else:
            # Robustes Einlesen für verschiedene CSV-Trenner
            try:
                df = pd.read_csv(file_obj.name)
            except Exception:
                df = pd.read_csv(file_obj.name, sep=None, engine='python')
        
        # Zwischenspeichern für den Zugriff durch den CodeAgent
        df.to_csv(INTERNAL_DATA_PATH, index=False)
        return df
    except Exception as e:
        raise Exception(f"Fehler beim Laden der Datei: {str(e)}")

def generate_data_overview(df):
    """
    Extrahiert Metadaten aus dem DataFrame für eine schnelle Nutzerübersicht.
    """
    if df is None:
        return "Keine Daten verfügbar."
    
    num_rows = len(df)
    num_cols = len(df.columns)
    col_names = ", ".join(df.columns.tolist())
    
    overview_md = f"""### ✅ Daten erfolgreich geladen
- **Datensätze (Zeilen):** {num_rows}
- **Dimensionen (Spalten):** {num_cols}
- **Spaltennamen:** `{col_names}`
"""
    return overview_md