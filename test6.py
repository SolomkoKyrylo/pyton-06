import sys
from pathlib import Path

CATEGORIES = {
    "images": [".jpeg", ".jpg", ".png", ".svg"],
    "video": [".avi", ".mp4", ".mov", ".mkv"],
    "documents": [".doc", ".docx", ".txt", ".pdf", ".xlsx", ".pptx"],
    "audio": [".mp3", ".ogg", ".wav", ".amr"],
    "archives": [".zip", ".gz", ".tar"],
}

def normalize(filename):
    
    normalized = filename.encode('ascii', 'ignore').decode('ascii')
    normalized = ''.join([c if c.isalnum() or c.isspace() else '_' for c in normalized])
    return normalized

def get_categories(file):
    ext = file.suffix.lower()
    for cat, extensions in CATEGORIES.items():
        if ext in extensions:
            return cat
    return "unknown"

def move_file(file, category, root_dir):
    target_dir = root_dir.joinpath(category)
    if not target_dir.exists():
        target_dir.mkdir()
    new_name = normalize(file.name)
    file.replace(target_dir.joinpath(new_name))

def sort_folder(path):
    for element in path.glob("**/*"):
        if element.is_file():
            category = get_categories(element)
            move_file(element, category, path)
        elif element.is_dir() and element.name not in CATEGORIES:
            sort_folder(element)
        elif element.is_dir() and element.name in CATEGORIES:
            
            element.rmdir()

def main():
    try:
        path = Path(sys.argv[1])
    except IndexError:
        return "No path to folder"

    if not path.exists():
        return "Folder does not exist"

    sort_folder(path)
    return "Folder sorted successfully"

if __name__ == "__main__":
    print(main())
