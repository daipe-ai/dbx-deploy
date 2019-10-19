#!/bin/bash
set -e

if [ "$(cut -c 1-10 <<< "$(uname -s)")" == "MINGW64_NT" ]; then
  IS_WINDOWS=1
else
  IS_WINDOWS=0
fi

CURRENT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

if [ $IS_WINDOWS == 1 ]; then
  CURRENT_DIR=$(sed "s|^/c/|c:/|" <<< $CURRENT_DIR)
fi

CONDA_ENV_PATH="$CURRENT_DIR/.venv"

echo "Creating Conda environment"
conda env create -f environment.yml -p "$CURRENT_DIR/.venv"

if [ $IS_WINDOWS == 1 ]; then
  PYTHON_EXECUTABLE_PATH="$CONDA_ENV_PATH/python.exe"
else
  PYTHON_EXECUTABLE_PATH="$CONDA_ENV_PATH/bin/python"
fi

eval "$(conda shell.bash hook)"
conda activate "$CONDA_ENV_PATH"

echo "Update pip"
$PYTHON_EXECUTABLE_PATH -m pip install --upgrade pip==19.3.1

echo "Update certifi"
$PYTHON_EXECUTABLE_PATH -m pip install --upgrade --ignore-installed certifi==2019.9.11

echo "Installing Poetry"
$PYTHON_EXECUTABLE_PATH -m pip install --user poetry==1.0.0b2

# Installing dependencies from pyproject.toml
$PYTHON_EXECUTABLE_PATH -m poetry install --no-root

if [ $IS_WINDOWS == 1 ]; then
  echo "Setting up Windows-specific stuff"

  CONDA_SCRIPTS_OS="windows"
  CONDA_SCRIPTS_FILE="env_vars.bat"
else
  echo "Setting up Linux/MacOS-specific stuff"

  CONDA_SCRIPTS_OS="unix"
  CONDA_SCRIPTS_FILE="env_vars.sh"
fi

echo "Setting up Conda activation & deactivation scripts"

CONDA_ACTIVATE_DIR="$CONDA_ENV_PATH/etc/conda/activate.d"
mkdir -p $CONDA_ACTIVATE_DIR
curl "https://raw.githubusercontent.com/DataSentics/dev-env-init/master/$CONDA_SCRIPTS_OS/conda/activate.d/$CONDA_SCRIPTS_FILE?$(date +%s)" --silent -o "$CONDA_ACTIVATE_DIR/$CONDA_SCRIPTS_FILE"
chmod +x "$CONDA_ACTIVATE_DIR/$CONDA_SCRIPTS_FILE"

CONDA_DEACTIVATE_DIR="$CONDA_ENV_PATH/etc/conda/deactivate.d"
mkdir -p $CONDA_DEACTIVATE_DIR
curl "https://raw.githubusercontent.com/DataSentics/dev-env-init/master/$CONDA_SCRIPTS_OS/conda/deactivate.d/$CONDA_SCRIPTS_FILE?$(date +%s)" --silent -o "$CONDA_DEACTIVATE_DIR/$CONDA_SCRIPTS_FILE"
chmod +x "$CONDA_DEACTIVATE_DIR/$CONDA_SCRIPTS_FILE"

echo "---------------"

echo "Setup completed. Active Conda environment now:"
echo ""
echo "conda activate $CONDA_ENV_PATH"
echo ""
