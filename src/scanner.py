from pathlib import Path
from src.file_entry import FileEntry

def scan_directory(path):
    directory = Path(path)

    if not directory.is_dir():
        raise ValueError(f"The path '{path}' is not a valid directory.")
    
    results = []

    for child in directory.iterdir():
        try:
            size_bytes = child.stat().st_size

            file_entry_child = FileEntry(
                name=child.name,
                path=str(child),
                entry_type="directory" if child.is_dir() else "file",
                size=size_bytes
            )
            results.append(file_entry_child)

        except FileNotFoundError:
            continue
    
    return results