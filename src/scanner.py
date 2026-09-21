from pathlib import Path
from src.file_entry import FileEntry

def get_size(path: Path | str) -> int:
    # recursively finding the size and returning 0 if it dissapears during scanning
    target = Path(path)

    if target.is_file():
        try:
            return target.stat().st_size
        except FileNotFoundError:
            return 0
        
    if target.is_dir():
        total_size = 0
        try:
            items = list(target.iterdir())
        except FileNotFoundError:
            return 0
        
        for item in items:
            try:
                total_size += get_size(item)
            except FileNotFoundError:
                continue
        return total_size
    
    return 0

def scan_directory(path):
    directory = Path(path)

    if not directory.is_dir():
        raise ValueError(f"The path '{path}' is not a valid directory.")
    
    results = []

    for child in directory.iterdir():
        try:
            size_bytes = get_size(child)

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