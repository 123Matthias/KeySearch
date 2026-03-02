import os
import unicodedata


class ExplorerService:
    def __init__(self):
        pass

    def list_files(self, directory, keywords=None, recursive=False):
        """
        Listet alle Dateien in einem Verzeichnis auf, optional gefiltert nach Keywords.
        """
        files = []

        # Keywords aufbereiten
        keyword_list = []
        if keywords:
            cleaned = keywords.replace(',', ' ')
            keyword_list = [k.strip().lower() for k in cleaned.split() if k.strip()]

        if recursive:
            # Rekursive Suche mit os.walk
            for root, dirs, filenames in os.walk(directory):

                for filename in filenames:
                    filepath = os.path.join(root, filename)

                    if not keyword_list:
                        files.append(filepath)
                        self.progress_hits = len(files)
                    else:
                        # Prüfen ob eines der Keywords im Dateinamen vorkommt
                        file_lower = filename.lower()
                        file_normalized = unicodedata.normalize('NFC', file_lower)

                        for keyword in keyword_list:
                            keyword_normalized = unicodedata.normalize('NFC', keyword.lower())

                            if keyword_normalized in file_normalized:
                                files.append(filepath)
                                break
        else:
            # Nur aktuelles Verzeichnis
            for item in os.listdir(directory):
                full_path = os.path.join(directory, item)
                if os.path.isfile(full_path):
                    if not keyword_list:
                        files.append(full_path)
                    else:
                        item_lower = item.lower()
                        for keyword in keyword_list:
                            if keyword in item_lower:
                                files.append(full_path)
                                break

        return files

    def normalize_text(self, text):
        """Wandle in NFC-Form um (ü als ein Zeichen)"""
        return unicodedata.normalize('NFC', text)


    def count_files(self, path):
        count = 0
        for root, dirs, files in os.walk(path):
            count += len(files)
        return count
