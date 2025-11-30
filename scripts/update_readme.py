#!/usr/bin/env python3
"""
Auto-update README.md based on codebase changes
Uses GPT to intelligently update relevant sections
"""

import os
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

def get_project_structure():
    """Get current project structure"""
    structure = []
    
    # Scan haitham_voice_agent directory
    hva_dir = project_root / "haitham_voice_agent"
    
    for root, dirs, files in os.walk(hva_dir):
        # Skip __pycache__ and .pyc files
        dirs[:] = [d for d in dirs if d != '__pycache__']
        files = [f for f in files if f.endswith('.py') and not f.startswith('__')]
        
        if files:
            rel_path = Path(root).relative_to(project_root)
            structure.append({
                'path': str(rel_path),
                'files': files
            })
    
    return structure

def get_recent_changes():
    """Get recent git changes"""
    import subprocess
    
    try:
        # Get last commit message
        result = subprocess.run(
            ['git', 'log', '-1', '--pretty=%B'],
            capture_output=True,
            text=True,
            cwd=project_root
        )
        last_commit = result.stdout.strip()
        
        # Get changed files
        result = subprocess.run(
            ['git', 'diff', '--name-only', 'HEAD~1', 'HEAD'],
            capture_output=True,
            text=True,
            cwd=project_root
        )
        changed_files = result.stdout.strip().split('\n')
        
        return {
            'last_commit': last_commit,
            'changed_files': [f for f in changed_files if f]
        }
    except Exception as e:
        print(f"Error getting git changes: {e}")
        return None

def update_readme_with_gpt(changes):
    """Use GPT to intelligently update README based on code changes"""
    try:
        import openai
        import re
        
        client = openai.OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        
        # Read current README
        readme_path = project_root / 'README.md'
        current_readme = readme_path.read_text(encoding='utf-8')
        
        # Get project structure for context
        structure = get_project_structure()
        structure_summary = "\n".join([f"- {s['path']}: {', '.join(s['files'][:3])}" for s in structure[:10]])
        
        prompt = f"""You are updating README.md for the Haitham Voice Agent (HVA) project.

RECENT CHANGES:
Commit: {changes['last_commit']}
Changed files: {', '.join(changes['changed_files'][:10])}

CURRENT PROJECT STRUCTURE (sample):
{structure_summary}

TASK:
Analyze if the Project Structure section (🗂️ هيكل المشروع | Project Structure) needs updating.
This section shows the file tree under haitham_voice_agent/.

RULES:
1. Only update if NEW Python files were added or REMOVED
2. Keep the existing format and emojis
3. Maintain bilingual comments (Arabic | English)
4. If no significant changes, return "NO_UPDATE"

OUTPUT FORMAT:
If update needed, return ONLY the updated file tree section between the ``` markers.
If no update needed, return exactly: NO_UPDATE
"""
        
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a technical documentation expert. Be conservative - only update if truly necessary."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.2,
            max_tokens=1500
        )
        
        suggestion = response.choices[0].message.content.strip()
        
        if suggestion == "NO_UPDATE" or "NO_UPDATE" in suggestion:
            print("✅ No README updates needed")
            return False
        
        # Check if we got a valid structure update
        if "haitham_voice_agent/" not in suggestion:
            print("⚠️  GPT response doesn't contain valid structure, skipping update")
            return False
        
        print(f"📝 GPT suggested structure update")
        
        # Find and replace the project structure section
        # Pattern: from "```" after "هيكل المشروع" to the closing "```"
        pattern = r'(### 🗂️ هيكل المشروع \| Project Structure\s*\n\s*```\s*\n)(.*?)(\n```)'
        
        match = re.search(pattern, current_readme, re.DOTALL)
        
        if not match:
            print("⚠️  Could not find project structure section in README")
            return False
        
        # Extract the new structure (remove markdown code fence if GPT included it)
        new_structure = suggestion
        new_structure = re.sub(r'^```\s*\n', '', new_structure)
        new_structure = re.sub(r'\n```\s*$', '', new_structure)
        
        # Replace the structure
        updated_readme = re.sub(
            pattern,
            r'\1' + new_structure + r'\3',
            current_readme,
            flags=re.DOTALL
        )
        
        # Verify the update didn't break the file
        if len(updated_readme) < len(current_readme) * 0.8:
            print("⚠️  Update seems to have removed too much content, aborting")
            return False
        
        # Write the updated README
        readme_path.write_text(updated_readme, encoding='utf-8')
        print("✅ README updated successfully")
        return True
        
    except Exception as e:
        print(f"❌ Error updating README: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    print("=" * 60)
    print("README Auto-Update Script")
    print("=" * 60)
    
    # Get recent changes
    changes = get_recent_changes()
    
    if not changes:
        print("⚠️  Could not get git changes")
        return
    
    print(f"\n📝 Last commit: {changes['last_commit']}")
    print(f"📁 Changed files: {len(changes['changed_files'])}")
    
    # Check if README update is needed
    if 'README.md' in changes['changed_files']:
        print("✅ README was already updated in this commit")
        return
    
    # Check if any Python files changed
    py_changes = [f for f in changes['changed_files'] if f.endswith('.py')]
    
    if not py_changes:
        print("✅ No Python files changed, README likely up-to-date")
        return
    
    print(f"\n🔍 Analyzing {len(py_changes)} Python file changes...")
    
    # Use GPT to suggest updates
    updated = update_readme_with_gpt(changes)
    
    if updated:
        print("\n✅ README updated successfully")
    else:
        print("\n✅ No README updates needed")

if __name__ == "__main__":
    main()
