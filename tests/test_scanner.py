from pathlib import Path
from src.scanner import scan_directory

def test_scan_directory_return_files_correctly(tmp_path: Path):
    file1 = tmp_path / "file1.txt"
    file1.write_text("abcd") # 4 bytes

    file2 = tmp_path / "file2.txt"
    file2.write_text("abcdef") # 6 bytes

    entries = scan_directory(tmp_path)

    assert len(entries) == 2

    entry_map = {entry.name: entry for entry in entries}

    # verifying file1.txt details
    assert "file1.txt" in entry_map
    assert entry_map["file1.txt"].entry_type == "file"
    assert entry_map["file1.txt"].size == 4

    # verifying file2.txt details
    assert "file2.txt" in entry_map
    assert entry_map["file2.txt"].entry_type == "file"
    assert entry_map["file2.txt"].size == 6