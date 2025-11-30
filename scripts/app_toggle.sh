#!/bin/bash

# ═══════════════════════════════════════════════════════════
#  🎤 HVA App Toggle Logic
#  Starts HVA if stopped, Stops HVA if running.
# ═══════════════════════════════════════════════════════════

PROJECT_DIR="/Users/haitham/development/Haitham Voice Agent (HVA)"
SCRIPT_PATH="$PROJECT_DIR/scripts/launch_silent.sh"

# Check if HVA is running
if pgrep -f "haitham_voice_agent.hva_menubar" > /dev/null 2>&1; then
  # --- STOPPING ---
  pkill -f "haitham_voice_agent.hva_menubar"
  
  # Send notification
  osascript -e 'display notification "Goodbye! 👋" with title "HVA Stopped"'
  
else
  # --- STARTING ---
  if [ -f "$SCRIPT_PATH" ]; then
    "$SCRIPT_PATH"
    # Notification is handled by launch_silent.sh, but we can add one here too if needed
  else
    osascript -e 'display alert "Error: Launch script not found at '"$SCRIPT_PATH"'"'
  fi
fi
