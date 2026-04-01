#!/bin/bash

build_app() {
    local APP_NAME="FileSearch"
    local ICON="assets/img/logo.icns"
    
    # Alle Verzeichnisse (rekursiv)
    local DIRS="assets Controller Process Service stylesheet View"
    
    # Python-Dateien im Hauptverzeichnis
    local PY_FILES="main.py settings.py language.py project_data.py"
    
    # Spezielle Asset-Dateien
    local ASSETS="assets/fa-7-Free-Solid-900.otf assets/PythonSelf.otf"
    
    # Hidden Imports
    local IMPORTS="fitz docx openpyxl pptx psutil PyPDF2 PySide6 PySide6.QtCore PySide6.QtGui PySide6.QtWidgets"
    
    # Basis-Befehl
    local CMD="pyinstaller --onedir --windowed --name \"$APP_NAME\" --icon=\"$ICON\""
    
    # Füge Verzeichnisse hinzu
    for dir in $DIRS; do
        CMD="$CMD --add-data \"$dir:$dir\""
    done
    
    # Füge Python-Dateien hinzu
    for file in $PY_FILES; do
        CMD="$CMD --add-data \"$file:.\""
    done
    
    # Füge Assets hinzu  
    for asset in $ASSETS; do
        CMD="$CMD --add-data \"$asset:assets\""
    done
    
    # Füge Imports hinzu
    for imp in $IMPORTS; do
        CMD="$CMD --hidden-import=$imp"
    done
    
    # Ausführen
    CMD="$CMD --clean main.py"
    echo "📦 Baue $APP_NAME..."
    eval $CMD
}

# Build starten
build_app