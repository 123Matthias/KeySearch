import os
import threading
from tkinter import filedialog


from Service.explorer_service import ExplorerService
from Service.reader_service import ReaderService


class MainPageController:
    def __init__(self):
        self.view = None
        self.reader_service = ReaderService()
        self.explorer_service = ExplorerService()
        self.search_thread = None
        self.cancel_search = False

        self.progress_inkrement = 0.0

    def set_view(self, view):
        """Setzt die View-Referenz nach der Erstellung"""
        self.view = view

    def choose_path(self):
        """Pfad auswählen und in der View aktualisieren"""
        pfad = filedialog.askdirectory(initialdir=os.path.expanduser("~/Downloads"))
        if pfad:
            self.view.pfad_label.configure(text=pfad)
            self.view.basis_pfad = pfad

    def search(self, event=None):
        """Startet die Suche in einem separaten Thread"""
        keywords = self.view.keywords.get()

        # Prüfen ob ein Pfad ausgewählt wurde
        if not hasattr(self.view, "basis_pfad") or not self.view.basis_pfad:
            print("Kein Pfad ausgewählt")
            return

        if not keywords:
            print("Kein Suchbegriff eingegeben")
            return

        # Prüfen ob bereits ein Suchlauf läuft
        if self.search_thread and self.search_thread.is_alive():
            print("Suche läuft bereits, wird abgebrochen...")
            self.cancel_search = True
            self.search_thread.join(timeout=1.0)

        # Alte Ergebnisse löschen
        self.view.clear_results()

        # Neuen Such-Thread starten
        self.cancel_search = False
        self.search_thread = threading.Thread(target=self._run_search_thread, args=(keywords,))
        self.search_thread.daemon = True  # Thread wird beendet wenn Hauptprogramm endet
        self.search_thread.start()

        print(f"🔍 Suche nach '{keywords}' gestartet...")

    def _run_search_thread(self, keywords):
        """
        Die eigentliche Suchlogik in einem separaten Thread.
        Ergebnisse werden sofort an die GUI gesendet.
        """

        self.reset_progress_bar()
        #Inkrement 10 datei ein Progress fortschritt
        self.progress_inkrement = 100.0 / self.explorer_service.count_files(self.view.basis_pfad)

        try:
            # ===== 1️⃣ ZUERST: Suche nach Dateinamen =====
            dateinamen_treffer = self.explorer_service.list_files(
                self.view.basis_pfad,
                keywords,
                recursive=True
            )

            namen_treffer_count = 0
            for dateipfad in dateinamen_treffer:
                if self.cancel_search:
                    self.reset_progress_bar()
                    print("Suche abgebrochen")
                    return

                dateiname = os.path.basename(dateipfad)
                # Relativen Pfad für die Anzeige
                rel_pfad = os.path.relpath(dateipfad, self.view.basis_pfad)
                snippet_text = f"Fundort: {rel_pfad}"

                # Ergebnis sofort an GUI senden
                self.view.add_result(dateiname, snippet_text, "filename")
                self.update_progress_bar(1 * self.progress_inkrement)
                namen_treffer_count += 1

            # ===== 2️⃣ DANN: Suche im Dateiinhalt =====
            # Alle Dateien im Verzeichnis (ohne Namensfilter)
            alle_dateien = self.explorer_service.list_files(
                self.view.basis_pfad,
                recursive=True
            )

            # Keywords für die Inhaltssuche aufbereiten
            keyword_list = [k.strip().lower() for k in keywords.replace(',', ' ').split() if k.strip()]

            inhalt_treffer_count = 0

            for dateipfad in alle_dateien:
                if self.cancel_search:
                    print("Suche abgebrochen")
                    return

                # Überspringe Dateien, die schon als Namens-Treffer angezeigt wurden
                if dateipfad in dateinamen_treffer:
                    continue

                dateiname = os.path.basename(dateipfad)
                rel_pfad = os.path.relpath(dateipfad, self.view.basis_pfad)
                self.update_progress_bar(1 * self.progress_inkrement)
                try:
                    # ReaderService für Text-Extraktion nutzen
                    text = self.reader_service.extract_text(dateipfad, max_chars=2000)

                    if text:
                        text_lower = text.lower()

                        for keyword in keyword_list:
                            if keyword in text_lower:
                                # Treffer! Snippet mit Kontext erstellen
                                kontext = self._make_body_text(text, keyword, ctx=200)
                                if kontext:
                                    snippet_text = f"'{keyword}' gefunden in: {rel_pfad}\n...{kontext}..."
                                else:
                                    snippet_text = f"Treffer im Inhalt\nFundort: {rel_pfad}"

                                # Ergebnis sofort an GUI senden
                                self.view.add_result(dateiname, snippet_text, "content")
                                break  # Ein Treffer pro Datei reicht

                except Exception as e:
                    # Falls Datei nicht lesbar, einfach überspringen
                    print(f"⚠️ Konnte {dateipfad} nicht lesen: {e}")
                    continue

            print(f"✅ Suche abgeschlossen: {namen_treffer_count} Treffer im Namen, "
                  f"{inhalt_treffer_count} Treffer im Inhalt")

        except Exception as e:
            print(f"❌ Fehler bei der Suche: {e}")

    def _make_body_text(self, text, keyword, ctx=100):
        """
        Erstellt ein Snippet mit Keyword im Kontext.

        Args:
            text: Der Text, in dem gesucht wird
            keyword: Das Suchwort
            ctx: Anzahl Zeichen vor und nach dem Treffer

        Returns:
            String mit dem Kontext oder None
        """
        if not text or not keyword:
            return None

        idx = text.lower().find(keyword.lower())
        if idx == -1:
            return None

        start = max(0, idx - ctx)
        end = min(len(text), idx + len(keyword) + ctx)

        # Bereinige den Text
        kontext = text[start:end].replace("\n", " ").replace("\r", " ")
        # Entferne mehrfache Leerzeichen
        kontext = ' '.join(kontext.split())

        return kontext

    def suche_abbrechen(self):
        """Bricht die laufende Suche ab"""
        self.cancel_search = True
        print("Suche wird abgebrochen...")

    # Hier können Sie jetzt Methoden hinzufügen, die den Progress aktualisieren
    def update_progress_bar(self, value):
        """Progress-Wert aktualisieren"""
        self.view.progress_state.set(self.view.progress_state.get() + value)

    def reset_progress_bar(self):
        """Progress zurücksetzen"""
        self.view.progress_state.set(0)