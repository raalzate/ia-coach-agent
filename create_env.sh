#!/bin/bash

echo ">>> Creando ambiente virtual..."
python3 -m venv app-env

echo ">>> Activando ambiente..."
source app-env/bin/activate

echo ">>> Actualizando pip..."
pip install --upgrade pip

echo ">>> Instalando dependencias..."
pip install -r requirements.txt

echo ">>> Instalación completa."
echo ">>> Para activar el ambiente nuevamente:"
echo "source app-env/bin/activate"
