#!/bin/zsh

# If HVA is already running → stop it
if pgrep -f "haitham_voice_agent.main" >/dev/null 2>&1; then
  echo "🔴 Stopping HVA..."
  pkill -f "haitham_voice_agent.main"
  
  # UX Improvement: Close the terminal window after killing to avoid clutter
  osascript -e 'tell application "Terminal" to close first window' & exit
fi

# If we reach here, HVA is not running → start it
echo "🟢 Starting HVA..."
cd "/Users/haitham/development/Haitham Voice Agent (HVA)"

# Use the virtual environment python directly
VENV_PYTHON="/Users/haitham/development/Haitham Voice Agent (HVA)/.venv/bin/python"

if [ -f "$VENV_PYTHON" ]; then
  "$VENV_PYTHON" -m haitham_voice_agent.main
else
  echo "⚠️ Virtual environment not found. Falling back to system python3..."
  python3 -m haitham_voice_agent.main
fi
