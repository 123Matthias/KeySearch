from PySide6.QtGui import QColor


class DarkColors:
    """Dunkles Farbschema - NUR Farben"""

    class Primary:
        MAIN = QColor("#00bc8c")  # Hauptakzentfarbe - Hellgrün
        LIGHT = QColor("#4eedb8")  # Helle Variante - Mintgrün
        DARK = QColor("#008c64")  # Dunkle Variante - Waldgrün

    class Secondary:
        MAIN = QColor("#f39c12")  # Sekundäre Akzentfarbe - Orange
        LIGHT = QColor("#ffcd4a")  # Helle Variante - Hellorange/Gelb
        DARK = QColor("#bb6e00")  # Dunkle Variante - Dunkelorange/Braun

    class UI:
        INPUT_BG = QColor("#2c2c2c")  # Input Hintergrund - Dunkelgrau
        INPUT_BORDER = QColor("#3c3c3c")  # Input Rahmen - Helleres Dunkelgrau
        INPUT_HIGHLIGHT = QColor("#00bc8c")  # Input Hervorhebung - Grün

        CONTAINER_BG = QColor("#1e1e1e")  # Hauptcontainer - Sehr dunkles Grau
        CARD_BG = QColor("#2d2d2d")  # Karten/Widgets - Dunkelgrau
        CARD_BG_GRADIENT_START = QColor("#1c1c1c")  # Card Gradient Start - Fast Schwarz
        CARD_BG_GRADIENT_END = QColor("#1a1a1a")  # Card Gradient End - Noch dunkler
        TOOLBAR_BG = QColor("#252525")  # Toolbar - Dunkelgrau
        SPLITTER_HANDLE = QColor("#2c2c2c")  # Splitter - Dunkelgrau
        SPLITTER_HANDLE_HOVER = QColor("#3c3c3c")  # Splitter Hover - Hellgrau

    class Text:
        PRIMARY = QColor("#ffffff")  # Weiß - Primärtext
        SECONDARY = QColor("#b0b0b0")  # Hellgrau - Sekundärtext
        DISABLED = QColor("#606060")  # Dunkelgrau - Deaktivierter Text
        ON_PRIMARY = QColor("#000000")  # Schwarz - Text auf primärer Farbe
        ON_SECONDARY = QColor("#000000")  # Schwarz - Text auf sekundärer Farbe


class LightColors:
    """Helles Farbschema - NUR Farben"""

    class Primary:
        MAIN = QColor("#006650")  # Hauptakzentfarbe - Dunkelgrün (vorher #00bc8c)
        LIGHT = QColor("#4eedb8")  # Helle Variante - Mintgrün
        DARK = QColor("#006644")  # Noch dunkler - Tannengrün

    class Secondary:
        MAIN = QColor("#c45c00")  # Sekundäre Akzentfarbe - Rostorange (vorher #f39c12)
        LIGHT = QColor("#ffcd4a")  # Helle Variante - Hellgelb
        DARK = QColor("#bb6e00")  # Dunkle Variante - Goldbraun

    class UI:
        INPUT_BG = QColor("#ffffff")  # Weiß - Input Hintergrund
        INPUT_BORDER = QColor("#d0d0d0")  # Hellgrau - Input Rahmen
        INPUT_HIGHLIGHT = QColor("#006650")  # Input Hervorhebung - Dunkelgrün

        CONTAINER_BG = QColor("#f5f5f5")  # Sehr helles Grau - Hauptcontainer
        CARD_BG = QColor("#ffffff")  # Reinweiß - Kartenhintergrund
        CARD_BG_GRADIENT_START = QColor("#f0f0f0")  # Card Gradient Start - Hellgrau (vorher #fafafa)
        CARD_BG_GRADIENT_END = QColor("#e8e8e8")    # Card Gradient End - Mittelgrau (vorher #f0f0f0)
        TOOLBAR_BG = QColor("#e0e0e0")  # Toolbar - Mittelgrau (vorher #e8e8e8)
        SPLITTER_HANDLE = QColor("#b0b0b0")  # Splitter - Grau (vorher #cccccc)
        SPLITTER_HANDLE_HOVER = QColor("#808080")  # Splitter Hover - Dunkelgrau (vorher #999999)

    class Text:
        PRIMARY = QColor("#000000")  # Schwarz - Primärtext
        SECONDARY = QColor("#444444")  # Dunkelgrau - Sekundärtext (vorher #666666)
        DISABLED = QColor("#888888")  # Mittelgrau - Deaktivierter Text (vorher #999999)
        ON_PRIMARY = QColor("#ffffff")  # Weiß - Text auf primärer Farbe
        ON_SECONDARY = QColor("#000000")  # Schwarz - Text auf sekundärer Farbe