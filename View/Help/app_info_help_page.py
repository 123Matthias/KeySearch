from PySide6.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QFrame
from PySide6.QtCore import Qt, QUrl
from PySide6.QtGui import QPixmap, QDesktopServices

from View.theme_manager import ThemeManager
from language import Language


class AppInfoHelpPage(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("App Info")
        self.setMinimumWidth(500)

        # ThemeManager initialisieren
        self.theme = ThemeManager()
        colors = self.theme.get_colors()

        # Hauptlayout
        layout = QVBoxLayout(self)
        layout.setSpacing(15)

        # Hintergrundfarbe setzen
        self.setStyleSheet(f"""
            QDialog {{
                background-color: {colors.UI.CONTAINER_BG.name()};
            }}
        """)

        # App Name
        title = QLabel("FileSearch")
        title.setStyleSheet(f"""
            font-size: 24px; 
            font-weight: bold; 
            color: {colors.Primary.MAIN.name()};
        """)
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        # Version
        version = QLabel("0.0.0 alpha")
        version.setStyleSheet(f"""
            font-size: 11px; 
            color: {colors.Text.SECONDARY.name()};
        """)
        version.setAlignment(Qt.AlignCenter)
        layout.addWidget(version)

        # Trennlinie
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setStyleSheet(f"""
            background-color: {colors.Text.DISABLED.name()}; 
            max-width: 300px;
        """)
        layout.addWidget(line)
        layout.setAlignment(line, Qt.AlignCenter)

        # Beschreibung
        desc_text = QLabel(
            Language.get_language("AppInfoHelpPage", "description")
        )
        desc_text.setWordWrap(True)
        desc_text.setAlignment(Qt.AlignCenter)
        desc_text.setStyleSheet(f"""
            font-size: 12px; 
            line-height: 1.4; 
            margin: 10px 20px;
            color: {colors.Text.SECONDARY.name()};
        """)
        layout.addWidget(desc_text)

        # GitHub Bereich mit Bild und Text
        github_layout = QHBoxLayout()
        github_layout.setAlignment(Qt.AlignCenter)

        # GitHub Logo (klein)
        github_logo = QLabel()
        github_pixmap = QPixmap("assets/img/LogoM-simple.png")  # Pfad anpassen
        if not github_pixmap.isNull():
            github_scaled = github_pixmap.scaled(20, 20, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            github_logo.setPixmap(github_scaled)
        else:
            github_logo.setText("🐙")  # Fallback Octopus
            github_logo.setStyleSheet(f"font-size: 16px; color: {colors.Text.SECONDARY.name()};")

        # GitHub Text
        github_text = "https://github.com/123Matthias/FileSearch"
        github_link = QLabel(f"{github_text}")
        github_link.setStyleSheet(f"""
            font-size: 11px;
            color: {colors.Primary.MAIN.name()};
        """)

        # Alles in einen Container, der klickbar ist
        github_container = QFrame()
        github_container.setCursor(Qt.PointingHandCursor)
        github_container.setStyleSheet("QFrame { background-color: transparent; }")

        container_layout = QHBoxLayout(github_container)
        container_layout.setContentsMargins(5, 2, 5, 2)
        container_layout.setSpacing(5)
        container_layout.addWidget(github_logo)
        container_layout.addWidget(github_link)

        # Klick-Event für den ganzen Container
        github_container.mousePressEvent = lambda e: QDesktopServices.openUrl(
            QUrl("https://github.com/123Matthias/selfSearch"))

        github_layout.addWidget(github_container)
        layout.addLayout(github_layout)

        # Open Source Hinweis
        open_source = QLabel("Open Source Licence")
        open_source.setStyleSheet(f"""
            font-size: 10px; 
            color: {colors.Text.DISABLED.name()}; 
            font-style: italic;
        """)
        open_source.setAlignment(Qt.AlignCenter)
        layout.addWidget(open_source)

        layout.addStretch()

        # OK-Button
        button_layout = QHBoxLayout()
        button_layout.addStretch()

        ok_button = QPushButton("OK")
        ok_button.setFixedWidth(120)
        ok_button.setFixedHeight(30)
        ok_button.setStyleSheet(f"""
            QPushButton {{
                background-color: {colors.Primary.MAIN.name()};
                color: {colors.Text.ON_PRIMARY.name()};
                border: none;
                border-radius: 5px;
                font-weight: bold;
                font-size: 12px;
            }}
            QPushButton:hover {{
                background-color: {colors.Primary.DARK.name()};
            }}
        """)
        ok_button.clicked.connect(self.accept)

        button_layout.addWidget(ok_button)
        button_layout.addStretch()

        layout.addLayout(button_layout)