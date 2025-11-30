#!/bin/bash

# HVA Text Mode - No Terminal, No Voice, Just Text File
cd "/Users/haitham/development/Haitham Voice Agent (HVA)"
source .venv/bin/activate

# Run in background, no terminal output
python3 hva_text_mode.py > /dev/null 2>&1

# Exit immediately so terminal closes
exit 0
