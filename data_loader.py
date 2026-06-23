import pandas as pd
import os
from typing import Optional, Tuple

INTERNAL_DATA_PATH = "business_data.csv"
CRM_DATA_PATH = "crm_master_data.csv"

def load_and_prepare_data(file_obj, mode="📊 Business Analysis Mode") -> Optional[pd.DataFrame]:
    """
    Lädt eine hochgeladene Datei (CSV oder Excel) und bereitet sie für den Agenten vor.
    
    Args:
        file_obj: Das von Gradio hochgeladene Dateiobjekt.
        mode: Der gewählte Analyse-Modus.
        
    Returns:
        pd.DataFrame: Der geladenäre DataFrame oder None bei Fehler.
    """
    if file_obj is None:
        return None
    
    try:
        # Dateiendung prüfen
        file_ext = os.path.splitext(file_obj.name)[1].lower()
        
        if mode == "👤 CRM Analytics Mode":
            if file_ext != ".xlsx":
                raise ValueError("CRM Mode erfordert eine .xlsx Datei.")
            
            # Multi-Sheet Handling
            xl = pd.ExcelFile(file_obj.name)
            required_sheets = ['Customers', 'Deals', 'Interactions']
            if not all(sheet in xl.sheet_names for sheet in required_sheets):
                raise ValueError(f"Excel-Datei muss folgende Sheets enthalten: {required_sheets}")
            
            df_customers = pd.read_excel(xl, sheet_name='Customers')
            df_deals = pd.read_excel(xl, sheet_name='Deals')
            df_interactions = pd.read_excel(xl, sheet_name='Interactions')
            
            # Aggregation der Interaktionen, um Duplikate beim Merge zu vermeiden
            df_inter_agg = df_interactions.groupby('customer_id').agg({
                'interaction_id': 'count',
                'date': 'max'
            }).rename(columns={'interaction_id': 'total_interactions', 'date': 'last_interaction'}).reset_index()
            
            # Sauberer Merge: Deals als Basis
            df = df_deals.merge(df_customers, on='customer_id', how='left')
            df = df.merge(df_inter_agg, on='customer_id', how='left')
            
            # Fehlende Interaktionen mit 0/None füllen
            df['total_interactions'] = df['total_interactions'].fillna(0)
            
            # Speichern als CRM Master
            df.to_csv(CRM_DATA_PATH, index=False)
            return df
        else:
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