import sys
import os
import subprocess
import importlib.util
from pathlib import Path

def check_and_install(package_name):
    """Check if package is installed, if not install it"""
    if importlib.util.find_spec(package_name) is None:
        print(f"📦 Installing missing package: {package_name}...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", package_name])
            print(f"✅ Installed {package_name}")
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to install {package_name}: {e}")

def main():
    # 1. Ensure Critical Dependencies
    print("🔍 Checking dependencies...")
    check_and_install("aiohttp")
    check_and_install("rumps")
    check_and_install("SpeechRecognition")
    check_and_install("pyaudio")
    check_and_install("psutil")
    check_and_install("openai")
    check_and_install("google.generativeai")

    # 2. Setup Environment
    project_root = Path(__file__).parent
    env = os.environ.copy()
    env["PYTHONPATH"] = str(project_root) + os.pathsep + env.get("PYTHONPATH", "")
    
    # 3. Launch App
    app_script = project_root / "haitham_voice_agent" / "hva_menubar.py"
    
    print(f"🚀 Launching HVA from: {app_script}")
    print(f"🐍 Using Python: {sys.executable}")
    
    try:
        subprocess.run([sys.executable, str(app_script)], env=env, check=True)
    except subprocess.CalledProcessError as e:
        print(f"❌ App crashed with exit code {e.returncode}")
    except KeyboardInterrupt:
        print("\n🛑 App stopped by user")

if __name__ == "__main__":
    main()
