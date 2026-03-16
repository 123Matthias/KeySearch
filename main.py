import multiprocessing
import os
import sys
from PySide6.QtWidgets import QApplication
from Controller.main_page_controller import MainPageController
from View.main_page import MainPage
from Service.font_awesome_service import FontAwesomeService
from View.theme_manager import ThemeManager
from project_data import ProjectData
from language import Language
from settings import Settings
import os
import sys
import platform


def get_base_path():
    """Ermittelt den korrekten Basis-Pfad für die jeweilige Plattform"""
    if getattr(sys, 'frozen', False):
        # Wir sind in einer PyInstaller-Binary
        if platform.system() == 'Darwin':  # macOS
            # MacOS: app/Contents/MacOS/executable -> app/Contents/Resources/
            base_path = os.path.dirname(sys.executable)
            resources_path = os.path.join(base_path, '..', 'Resources')
            return os.path.abspath(resources_path)

        elif platform.system() == 'Windows':
            # Windows: EXE liegt in dist/selfSearch/, Daten in dist/selfSearch/_internal/
            exe_path = os.path.dirname(sys.executable)
            internal_path = os.path.join(exe_path, '_internal')
            return os.path.abspath(internal_path)

        else:  # Linux
            return os.path.dirname(sys.executable)
    else:
        # Entwicklungsmodus - Verzeichnis der Python-Datei
        return os.path.dirname(os.path.abspath(__file__))

# Arbeitsverzeichnis setzen
base_path = get_base_path()
os.chdir(base_path)
print(f"✅ Arbeitsverzeichnis: {base_path}")
print(f"✅ Plattform: {platform.system()}")


class Main:
    def __init__(self, my_app):
        self.app = my_app

        # Load Settings and save them into Project_Data class
        Settings.load_settings()

        # Load Languages from Project Data
        Language.load(ProjectData.language)

        # Fonts
        self.font_awesome_7 = FontAwesomeService.load_font_awesome_free()

        # Theme Manager start
        ThemeManager().initialize(self.app)

        # Controller instance
        self.main_page_controller = MainPageController()

        # MainPage instance and show
        self.main_page = MainPage(self.main_page_controller)
        self.main_page.show()


        print("✅ Main App initialized. Starting...")

    def run(self):
        return self.app.exec()



if __name__ == "__main__":
    # PyInstaller startet sonst startet er mehrere Instanzen der App!
    multiprocessing.freeze_support()

    app = QApplication(sys.argv)
    app.setApplicationName("FileSearch")
    app.setApplicationDisplayName("FileSearch")

    main_app = Main(app)
    sys.exit(main_app.run())