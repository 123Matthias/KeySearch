from textwrap import fill

import tkinter as tk
import ttkbootstrap as ttk
import threading
from Service.explorer_service import ExplorerService


class MainPage:
    def __init__(self, controller):
        self.controller = controller
        self.controller.set_view(self)

        self.root = ttk.Window(themename="darkly")
        self.root.title("OSWalk")

        # Service-Instanz für spätere Nutzung
        self.explorer_service = ExplorerService()

        # Header
        self.header = ttk.Frame(self.root)
        self.header.pack(padx=(50, 50), pady=(40, 10), fill="x")

        self.title_os = ttk.Label(self.header, text="OS", font=("", 32, "bold"), bootstyle="info")
        self.title_os.pack(side="left", padx=(0, 2))

        self.title_walk = ttk.Label(self.header, text="Walk", font=("", 32, "bold"), bootstyle="warning")
        self.title_walk.pack(side="left", padx=(0, 12))

        self.keywords = ttk.Entry(self.header, bootstyle="light", font=("", 16))
        self.keywords.pack(side="left", fill="x", expand=True)
        self.keywords.bind("<Return>", lambda e: self.controller.search())


        # default striped progressbar style
        self.progress_state = tk.DoubleVar(master=self.root, value=0)  # Der Wert
        progress_bar = ttk.Progressbar(bootstyle="light-striped", orient="horizontal", variable=self.progress_state)
        progress_bar.pack(fill="x", padx=10, pady=10)

        # Pfad-Label
        self.pfad_label = ttk.Label(self.root, text="Kein Pfad gewählt", bootstyle="light")
        self.pfad_label.pack(pady=(10, 5))


        self.btn = ttk.Button(self.root, text="choose-path", bootstyle="darkly", command=self.controller.choose_path)
        self.btn.pack(pady=(0, 10))
        # Button Hover-Effekte
        self.btn.bind("<Enter>", self._on_btn_enter)
        self.btn.bind("<Leave>", self._on_btn_leave)

        # ===== Results (Scroll-Container) mit Canvas =====
        self.results_wrap = ttk.Frame(self.root)
        self.results_wrap.pack(fill="both", expand=True, padx=50, pady=(10, 20))

        # Canvas für Scrolling
        self.canvas = ttk.Canvas(self.results_wrap, highlightthickness=0)
        # Scrollbar
        self.scrollbar = ttk.Scrollbar(self.results_wrap, orient="vertical", command=self.canvas.yview)

        # Frame für Snippets (wird in Canvas eingebettet)
        self.scrollable_frame = ttk.Frame(self.canvas)

        # Canvas und Scrollbar verbinden
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        # Scrollable Frame in Canvas einbetten
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")

        # Bei Größenänderung des Frames den Scrollbereich anpassen
        self.scrollable_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))

        # Packen
        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        self._enable_mousewheel()
        self.root.mainloop()

    def _enable_mousewheel(self):
        """Mausrad-Scrolling für normale Mäuse (Windows/Linux/macOS mit Rad)"""

        def on_mousewheel(event):
            if event.delta:
                steps = int(-1 * (event.delta / 60))
                self.canvas.yview_scroll(steps, "units")
            elif event.num == 4:
                self.canvas.yview_scroll(-1, "units")
            elif event.num == 5:
                self.canvas.yview_scroll(1, "units")
            return "break"

        self.root.bind_all("<MouseWheel>", on_mousewheel)
        self.root.bind_all("<Button-4>", on_mousewheel)
        self.root.bind_all("<Button-5>", on_mousewheel)

        print("🖱️ Mausrad-Scrolling für normale Mäuse aktiviert")

    def add_result(self, title, body, treffer_typ):
        """
        Fügt ein neues Suchergebnis zur GUI hinzu.
        Wird aus dem Thread aufgerufen.
        """

        def _add():
            snipped = ttk.Frame(self.scrollable_frame, padding=10)
            snipped.pack(fill="x", pady=6)

            # Emoji je nach Treffer-Typ
            emoji = "📁" if treffer_typ == "filename" else "🔍"

            title_label = ttk.Label(snipped, text=f"{emoji} {title}",
                                    wraplength=650, font=("", 14, "bold"),
                                    bootstyle="info", anchor="w", justify="left")
            title_label.pack(fill="x", anchor="w")
            title_label.visited = False

            body_label = ttk.Label(snipped, text=body, wraplength=650,
                                   anchor="w", justify="left")
            body_label.pack(fill="x", pady=(4, 0))

            def on_enter(e):
                title_label.configure(font=("", 14, "bold underline"))

            def on_leave(e):
                if title_label.visited:
                    title_label.configure(font=("", 14, "bold"))
                else:
                    title_label.configure(bootstyle="info", font=("", 14, "bold"))

            def on_click(e):
                title_label.visited = True
                title_label.configure(bootstyle="danger", font=("", 14, "bold"))

            title_label.bind("<Enter>", on_enter)
            title_label.bind("<Leave>", on_leave)
            title_label.bind("<Button-1>", on_click)
            title_label.configure(cursor="hand2")

            for e in [snipped, body_label]:
                e.bind("<Enter>", lambda e: e.widget.configure(cursor="hand2"))
                e.bind("<Leave>", lambda e: e.widget.configure(cursor=""))

        # GUI-Updates müssen im Haupt-Thread erfolgen
        self.root.after(0, _add)

    def clear_results(self):
        """Alle Ergebnisse im Scrollbereich löschen"""

        def _clear():
            for w in self.scrollable_frame.winfo_children():
                w.destroy()

        self.root.after(0, _clear)

    def show_status(self, message, typ="info"):
        """Zeigt Statusmeldungen an (optional)"""

        def _show():
            if hasattr(self, 'status_label'):
                self.status_label.configure(text=message, bootstyle=typ)

        self.root.after(0, _show)

    def _on_btn_enter(self, e):
        """Mouse Enter - Light Mode"""
        self.btn.configure(bootstyle="light")

    def _on_btn_leave(self, e):
        """Mouse Leave - Zurück zu Dark"""
        self.btn.configure(bootstyle="secondary")