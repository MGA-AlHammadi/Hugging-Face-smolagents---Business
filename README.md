# 📊 AI Business Analyst Pro

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![Hugging Face](https://img.shields.io/badge/%F0%9F%A4%97%20Hugging%20Face-smolagents-orange)
![Google Gemini](https://img.shields.io/badge/AI-Google%20Gemini-red)
![Gradio](https://img.shields.io/badge/UI-Gradio-green)

Dieses Projekt bietet eine hochmoderne, automatisierte Lösung für die Analyse komplexer Geschäfts- und CRM-Daten. Durch den Einsatz von autonomen KI-Agenten werden Rohdaten in sekundenschnelle in strategische Erkenntnisse, visuelle Berichte und Management-Warnungen verwandelt.

## 1. Projektübersicht & Zielsetzung

### Die Herausforderung
In modernen CRM-Systemen sammeln sich riesige Mengen an Daten über Kunden, Deals und Interaktionen an. Für das Management ist es oft komplex und zeitaufwendig, aus diesen fragmentierten Daten (oft über mehrere Excel-Sheets verteilt) zeitnah fundierte Entscheidungen zu treffen. Manuelle Analysen sind fehleranfällig und hinken der Marktentwicklung oft hinterher.

### Unsere Lösung
Der **AI Business Analyst Pro** adressiert dieses Problem durch einen dualen, KI-gestützten Analyse-Ansatz. Basierend auf Hugging Face `smolagents` und Google Gemini (`LiteLLMModel`) agiert das System als autonomer Datenwissenschaftler, der Code in Echtzeit schreibt, ausführt und interpretiert.

**Zwei spezialisierte Modi stehen zur Verfügung:**
1.  **Business Analysis Mode:** Für schnelle Ad-hoc-Auswertungen einzelner Datensätze.
2.  **CRM Analytics Mode:** Ein tiefgreifendes Analyse-Tool für komplexe CRM-Strukturen, das Datenkorrelationen über mehrere Dimensionen hinweg erkennt.

---

## 2. Hauptfunktionen (Features)

Das System bietet eine breite Palette an Analyse-Werkzeugen, die speziell auf die Bedürfnisse des Managements zugeschnitten sind:

*   **Duale Analyse-Modi:**
    *   **Business Analysis:** Fokus auf allgemeine Trends, Umsatzverteilung und statistische Ausreißer.
    *   **CRM Analytics:** Spezialisiert auf Kundenlebenszyklen und Sales-Pipelines.
*   **Multi-Sheet-Excel-Merge:** Automatische Zusammenführung und Korrelation von Daten aus den Bereichen *Customers*, *Deals* und *Interactions*.
*   **Geografische Filialanalyse:** Analyse der Performance nach Standorten, Regionen und Ländern zur Identifikation lokaler Marktbesonderheiten.
*   **Automatisierte Management-Warnungen:** Das System erkennt eigenständig Unterperformance (z.B. sinkende Won-Quoten oder Margendruck) und generiert datenbasierte Warnmeldungen.
*   **Conversion Rate & Churn-Risk:**
    *   Präzise Berechnung der Conversion Rates zwischen den Phasen (Lead → Negotiation → Won).
    *   KI-basierte Identifikation von Kunden mit hohem Abwanderungsrisiko basierend auf Interaktionsfrequenzen.
*   **Automatisierter PDF-Export:** Generierung professioneller Analyse-Berichte inklusive dynamisch erstellter Diagramme.

---

## 3. Technische Architektur

Die Anwendung nutzt einen spezialisierten Tech-Stack für maximale Effizienz und Präzision:

*   **Frontend:** [Gradio](https://gradio.app/) – Ermöglicht eine intuitive, webbasierte Benutzeroberfläche.
*   **Orchestrierung:** [smolagents](https://github.com/huggingface/smolagents) – Framework für autonome Code-Agenten.
*   **LLM-Integration:** [LiteLLM](https://github.com/BerriAI/litellm) – Nahtlose Anbindung an Google Gemini für hochperformante Code-Generierung.
*   **Datenverarbeitung:** [Pandas](https://pandas.pydata.org/) & [Openpyxl](https://openpyxl.readthedocs.io/) – Robuste Handhabung komplexer Excel- und CSV-Strukturen.
*   **Visualisierung:** [Matplotlib](https://matplotlib.org/) & [Seaborn](https://seaborn.pydata.org/) – Dynamische Erstellung aussagekräftiger Management-Diagramme.

---

## 4. Installations- und Setup-Anleitung

Folgen Sie diesen Schritten, um die Analyse-Umgebung lokal einzurichten:

### Schritt 1: Virtuelle Umgebung erstellen
Es wird empfohlen, eine isolierte Umgebung zu nutzen:
```bash
# Umgebung erstellen
python -m venv .venv

# Aktivierung unter Windows
.venv\Scripts\activate

# Aktivierung unter macOS/Linux
source .venv/bin/activate
```

### Schritt 2: Abhängigkeiten installieren
Installieren Sie alle benötigten Bibliotheken mit einem Befehl:
```bash
pip install -r requirements.txt
```
*Alternativ können die Hauptpakete einzeln installiert werden:*
`pip install smolagents litellm gradio pandas openpyxl matplotlib seaborn python-dotenv`

### Schritt 3: Konfiguration der Umgebungsvariablen
Erstellen Sie eine Datei namens `.env` im Hauptverzeichnis des Projekts und hinterlegen Sie Ihren Google Gemini API-Key:
```env
GEMINI_API_KEY=Ihr_Google_Gemini_API_Key_Hier
```

---

## 5. Starten der Anwendung

Nachdem das Setup abgeschlossen ist, können Sie den Agenten starten:

```bash
python app.py
```

Sobald die Anwendung läuft, öffnet sich die Gradio-Oberfläche standardmäßig unter:
`http://127.0.0.1:7860`

**Hinweis für den Reviewer:** Für den CRM-Modus laden Sie bitte eine Excel-Datei hoch, die die Registerkarten "Customers", "Deals" und "Interactions" enthält, um das volle Potenzial des Multi-Sheet-Merges zu testen.

