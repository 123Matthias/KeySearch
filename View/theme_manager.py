from PySide6.QtWidgets import QApplication
from PySide6.QtCore import Qt
from PySide6.QtGui import QGuiApplication

from stylesheet.dark_theme_style import DarkTheme
from stylesheet.light_theme_style import LightTheme


class ThemeManager:
    _instance = None
    _current_theme = "dark"
    _app = None
    _observers = []

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def initialize(self, app: QApplication):
        self._app = app
        # Signal verbinden
        QGuiApplication.styleHints().colorSchemeChanged.connect(
            self._on_system_theme_changed
        )
        # Initial erkennen
        self._detect_initial_theme()
        self._notify_observers()

    def _detect_initial_theme(self):
        color_scheme = QGuiApplication.styleHints().colorScheme()
        self._current_theme = "dark" if color_scheme == Qt.ColorScheme.Dark else "light"
        print(f"✅ Initiales Theme: {self._current_theme}")

    def _on_system_theme_changed(self, color_scheme):
        new_theme = "dark" if color_scheme == Qt.ColorScheme.Dark else "light"
        if new_theme != self._current_theme:
            self._current_theme = new_theme
            self._notify_observers()

    def _notify_observers(self):
        for observer in self._observers[:]:
            try:
                observer.on_theme_changed()
            except Exception as e:
                if observer in self._observers:
                    self._observers.remove(observer)

    def get_colors(self):
        return DarkTheme.get_colors() if self._current_theme == "dark" else LightTheme.get_colors()

    def register_observer(self, observer):
        if observer not in self._observers:
            self._observers.append(observer)

    def unregister_observer(self, observer):
        if observer in self._observers:
            self._observers.remove(observer)