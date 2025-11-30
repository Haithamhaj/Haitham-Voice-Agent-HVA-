#!/bin/bash

# Get the directory where the script is located
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_ROOT="$(dirname "$DIR")"

# Path to the virtual environment python
PYTHON_EXEC="$PROJECT_ROOT/.venv/bin/python"

# Check if python exists
if [ ! -f "$PYTHON_EXEC" ]; then
    osascript -e 'display notification "Virtual environment not found!" with title "HVA Error"'
    exit 1
fi

# Run the app wrapper (which checks dependencies) in the background
cd "$PROJECT_ROOT"
nohup "$PYTHON_EXEC" run_app.py > "$PROJECT_ROOT/hva.log" 2>&1 &

# Notify user
osascript -e 'display notification "HVA is running in the menu bar" with title "Haitham Voice Agent"'
