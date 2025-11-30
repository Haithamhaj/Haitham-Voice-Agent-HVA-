import sys
import os
import subprocess
from pathlib import Path

def main():
    # Get the directory of the script
    project_root = Path(__file__).parent
    
    # Set PYTHONPATH to include project root
    env = os.environ.copy()
    env["PYTHONPATH"] = str(project_root) + os.pathsep + env.get("PYTHONPATH", "")
    
    # Path to hva_menubar.py
    app_script = project_root / "haitham_voice_agent" / "hva_menubar.py"
    
    print(f"🚀 Launching HVA from: {app_script}")
    print(f"🐍 Using Python: {sys.executable}")
    
    # Execute the app using the SAME python interpreter running this script
    try:
        subprocess.run([sys.executable, str(app_script)], env=env, check=True)
    except subprocess.CalledProcessError as e:
        print(f"❌ App crashed with exit code {e.returncode}")
    except KeyboardInterrupt:
        print("\n🛑 App stopped by user")

if __name__ == "__main__":
    main()
