from pathlib import Path
inbox = Path.home() / "HVA_Workspace/inbox/tasks/tasks.json"
print(f"Checking: {inbox}")
if inbox.exists():
    print("--- CONTENT START ---")
    print(inbox.read_text())
    print("--- CONTENT END ---")
else:
    print(f"File not found: {inbox}")
