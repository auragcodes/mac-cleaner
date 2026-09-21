from dataclasses import dataclass

@dataclass
class FileEntry:
    name: str
    path: str
    entry_type: str
    size: int