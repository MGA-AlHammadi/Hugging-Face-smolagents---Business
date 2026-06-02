# 📊 KI-gestützter Business Data Analyst (smolagents)

Dieses Projekt nutzt Hugging Face `smolagents`, um eine autonome Datenanalyse auf CSV-Dateien durchzuführen. Die Benutzeroberfläche wird mit Gradio bereitgestellt.

## Features
- Autonome Code-Generierung für Datenanalyse.
- Erstellung von Diagrammen (Matplotlib/Seaborn).
- Deutschsprachige Interaktion.

## Installation

1. Repository klonen:
   ```bash
   git clone <dein-repo-url>
   cd "Hugging Face smolagents - Business"
   ```

2. Abhängigkeiten installieren:
   ```bash
   pip install -r requirements.txt
   ```

3. `.env` Datei erstellen:
   Erstelle eine Datei namens `.env` im Hauptverzeichnis und füge deinen Hugging Face Token hinzu:
   ```env
   HF_TOKEN=dein_hf_token_hier
   ```

## Starten
```bash
python app.py
```
