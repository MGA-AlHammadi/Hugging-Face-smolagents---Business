import subprocess
import sys

def ensure_dependencies():
    """
    Überprüft die Verfügbarkeit notwendiger Bibliotheken und installiert diese bei Bedarf automatisch.
    Dies gewährleistet die Portabilität des Skripts auf verschiedenen Systemen.
    """
    REQUIRED_PACKAGES = {
        "smolagents": "smolagents",
        "gradio": "gradio",
        "pandas": "pandas",
        "matplotlib": "matplotlib",
        "seaborn": "seaborn",
        "huggingface_hub": "huggingface_hub",
        "python-dotenv": "python-dotenv",
        "openpyxl": "openpyxl"
    }

    for module_name, package_name in REQUIRED_PACKAGES.items():
        try:
            # Versuche das Modul zu importieren (manche Namen unterscheiden sich vom Paketnamen)
            if module_name == "python-dotenv":
                import dotenv
            else:
                __import__(module_name.replace("-", "_"))
        except ImportError:
            print(f"[System] Bibliothek '{package_name}' fehlt. Installation läuft...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", package_name])

# Sofortige Ausführung beim Import, falls gewünscht, 
# oder expliziter Aufruf in der app.py