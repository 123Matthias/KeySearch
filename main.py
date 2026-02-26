from Service.pdf_reader_service import PDFReader
from pathlib import Path
import os


print("Aktuelles Verzeichnis:", os.getcwd())
print("Dateien:", os.listdir('.'))
pdf_name = "testrechnung.pdf"
pdf_name_2 = "test.pdf"
pdf_path = Path(pdf_name)  # ← In Path umwandeln!

# Prüfe ob Datei existiert und lesbar ist
if pdf_path.exists():
    if os.access(pdf_path, os.R_OK):
        print(f"Datei gefunden und lesbar: {pdf_path}")
        reader = PDFReader(pdf_path)
        
        # Jetzt erst die Methoden aufrufen!
        print(f"Seitenanzahl: {reader.get_page_count()}")
        print("\n" + "="*50 + "\n")
        
        # Erste Seite lesen
        print("ERSTE SEITE:")
        print(reader.read_page(1))
        print("\n" + "="*50 + "\n")
        
        # Alles lesen
        print("KOMPLETTES PDF:")
        print(reader.read_all_pages())
        
    else:
        print(f"Keine Leserechte für: {pdf_path}")
else:
    print(f"Datei nicht gefunden: {pdf_path}")