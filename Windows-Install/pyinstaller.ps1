function Build-App {
    $AppName = "FileSearch"

    # Windows verwendet .ico
    $Icon = "assets\img\logo.ico"


    # Alle Verzeichnisse (rekursiv)
    $Dirs = @(
        "assets",
        "Controller",
        "Process",
        "Service",
        "stylesheet",
        "View"
    )

    # Python-Dateien im Hauptverzeichnis
    $PyFiles = "main.py","settings.py","language.py","project_data.py"

    # Hidden Imports
    $Imports = @(
        "fitz",
        "python-docx",
        "openpyxl",
        "pptx",
        "psutil",
        "PyPDF2",
        "PySide6",
        "PySide6.QtCore",
        "PySide6.QtGui",
        "PySide6.QtWidgets",
        "PySide6.QtNetwork",
        "json"
    )

    # Basis-Befehl als Array
    $Args = @(
        "--onedir"
        "--windowed"
        "--name", $AppName
    )


    $Args += "--icon"
    $Args += $Icon


    # Verzeichnisse hinzufuegen
    foreach ($dir in $Dirs) {
        if (Test-Path $dir) {
            $Args += "--add-data"
            $Args += "$dir;$dir"
            Write-Host "  + $dir"
        } else {
            Write-Warning "Warnung: $dir nicht gefunden"
        }
    }

    # Python-Dateien hinzufuegen
    foreach ($file in $PyFiles) {
        if (Test-Path $file) {
            $Args += "--add-data"
            $Args += "$file;."
            Write-Host "  + $file"
        }
    }

    # Hidden Imports hinzufuegen
    foreach ($imp in $Imports) {
        $Args += "--hidden-import"
        $Args += $imp
    }

    # Windows-spezifische Zusaetze
    $Args += "--collect-all", "PySide6"
    $Args += "--collect-all", "fitz"
    $Args += "--clean"
    $Args += "main.py"

    # Build starten
    Write-Host ""
    Write-Host "=== Build $AppName fuer Windows ==="
    Write-Host "Starte PyInstaller..."
    Write-Host ""

    pyinstaller @Args

    if ($LASTEXITCODE -eq 0) {
        Write-Host ""
        Write-Host "=== Build erfolgreich ==="
        Write-Host "Ausgabe: dist/$AppName"
    } else {
        Write-Host ""
        Write-Host "=== Build fehlgeschlagen ==="
    }
}

# Build starten
Build-App