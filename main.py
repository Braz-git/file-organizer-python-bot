import shutil
from pathlib import Path
import argparse

# ==================== SETTINGS ====================
FILE_CATEGORIES = {
    "Images": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".svg", ".webp"],
    "Documents": [".pdf", ".doc", ".docx", ".txt", ".md", ".odt", ".xlsx", ".xls", ".pptx", ".csv"],
    "Videos": [".mp4", ".mkv", ".avi", ".mov", ".wmv"],
    "Audio": [".mp3", ".wav", ".flac", ".m4a"],
    "Archives": [".zip", ".rar", ".7z", ".tar", ".gz"],
    "Code": [".py", ".js", ".html", ".css", ".java", ".cpp", ".c"],
    "Executables": [".exe", ".msi", ".app", ".dmg"],
    "Others": []
}

def get_category(ext: str) -> str:
    ext = ext.lower()
    for category, extensions in FILE_CATEGORIES.items():
        if ext in extensions:
            return category
    return "Others"

def organize_files(target_dir: str, dry_run: bool = False):
    target_path = Path(target_dir).resolve()
    
    # ==================== DEBUG INFO ====================
    print(f"🔍 DEBUG: Target path resolved to → {target_path}")
    print(f"🔍 DEBUG: Dry-run mode enabled? → {dry_run}")
    print(f"🔍 DEBUG: Directory exists? → {target_path.exists()}")
    
    if not target_path.exists() or not target_path.is_dir():
        print(f"❌ ERRO: Directory '{target_dir}' does not exist or is not a directory!")
        print("💡 TIP: Use double quotes if the path contains spaces.")
        return

    print(f"\n🚀 Starting organization of: {target_path}")
    print("Mode: DRY-RUN (simulation - no files will be moved)" if dry_run else "Mode: REAL (files WILL be moved!)")

    moved = 0
    for item in target_path.iterdir():
        if item.is_file():
            category = get_category(item.suffix)
            dest_folder = target_path / category
            dest_folder.mkdir(exist_ok=True)

            dest_path = dest_folder / item.name
            counter = 1
            while dest_path.exists():
                dest_path = dest_folder / f"{item.stem}_{counter}{item.suffix}"
                counter += 1

            if dry_run:
                print(f"   [DRY] {item.name} → {category}/")
            else:
                shutil.move(str(item), str(dest_path))
                print(f"   ✅ Moved: {item.name} → {category}/")
            moved += 1

    print(f"\n✅ Done! Files processed: {moved}")

# ==================== MAIN EXECUTION ====================
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="File Organizer Bot - Automatically sort files by type")
    parser.add_argument("directory", nargs="?", default=".", help="Directory to organize (use quotes if path has sapces)")
    parser.add_argument("--dry-run", action="store_true", help="Simulate without moving any files")
    
    args = parser.parse_args()
    organize_files(args.directory, args.dry_run)