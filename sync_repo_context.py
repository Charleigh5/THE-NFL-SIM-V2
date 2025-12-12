import os
import subprocess
import sys

# ==========================================
# CONFIGURATION
# ==========================================
OUTPUT_FILE = "nfl_sim_context.txt"
BRANCH_NAME = "main"  # Ensure this matches your repo (main vs master)
IGNORE_DIRS = {
    ".git", "node_modules", "venv", "env", "__pycache__", 
    ".next", "dist", "build", "coverage", ".vscode", ".idea", 
    "playwright-report", "test-results", "target", "out"
}
IGNORE_FILES = {
    ".DS_Store", "package-lock.json", "yarn.lock", "Thumbs.db", 
    "pnpm-lock.yaml", "poetry.lock", "bun.lockb"
}
# ==========================================

def run_git_pull():
    """Runs git pull to update the repository."""
    print(f"🔄 Gridiron Architect: Pulling latest changes from GitHub ({BRANCH_NAME})...")
    try:
        if not os.path.exists(".git"):
            print("⚠️ Warning: Not a git repository root. Skipping pull.")
            return

        result = subprocess.run(
            ["git", "pull", "origin", BRANCH_NAME],
            capture_output=True,
            text=True
        )
        
        if result.returncode == 0:
            print("✅ Git Pull Successful.")
            if "Already up to date." in result.stdout:
                print("   (No new changes detected)")
            else:
                print(result.stdout)
        else:
            print("❌ Git Pull Failed:")
            print(result.stderr)
            # We don't exit here, as we might still want to generate context from local state
            
    except Exception as e:
        print(f"❌ Error running git: {e}")

def generate_tree(startpath, file_handle):
    """Recursively walks the directory and writes the structure."""
    for root, dirs, files in os.walk(startpath):
        # Filter directories in-place
        dirs[:] = [d for d in dirs if d not in IGNORE_DIRS]
        
        level = root.replace(startpath, '').count(os.sep)
        indent = '│   ' * level
        
        folder_name = os.path.basename(root)
        if root == startpath:
            file_handle.write(f"{folder_name}/\n")
        else:
            file_handle.write(f"{indent}├── {folder_name}/\n")
        
        subindent = '│   ' * (level + 1)
        files.sort()
        for f in files:
            if f not in IGNORE_FILES and not f.endswith(('.png', '.jpg', '.jpeg', '.svg', '.ico', '.woff', '.woff2')):
                file_handle.write(f"{subindent}├── {f}\n")

def main():
    current_dir = os.getcwd()
    
    # 1. Update Repo
    run_git_pull()
    
    # 2. Generate Context
    print(f"📦 Gridiron Architect: Scanning project structure at {current_dir}...")
    try:
        with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
            f.write(f"# REPOSITORY CONTEXT: THE-NFL-SIM-V2\n")
            f.write(f"# Generated: {os.path.basename(current_dir)}\n")
            f.write(f"# Role: Input this file to the Gridiron Architect Gem\n")
            f.write(f"# =========================================\n\n")
            
            generate_tree(current_dir, f)
            
        print(f"✅ Success! Context generated at: {OUTPUT_FILE}")
        print(f"👉 INSTRUCTION: Upload '{OUTPUT_FILE}' to the Gem to prime it.")
        
    except Exception as e:
        print(f"❌ Error generating context: {e}")

if __name__ == "__main__":
    main()