from pathlib import Path
from src.scanner import get_size, scan_directory

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

def test_recursively_scan_directory_return_files_correctly(tmp_path: Path):
    file1 = tmp_path / "file1.txt"
    file1.write_text("abcd") # 4 bytes

    file2 = tmp_path / "file2.txt"
    file2.write_text("abcdef") # 6 bytes

    subfolder = tmp_path / "folder"
    subfolder.mkdir()

    file3 = subfolder / "file3.txt"
    file3.write_text("abcde") # 5 bytes

    file4 = subfolder / "file4.txt"
    file4.write_text("abcdefg") # 7 bytes

    assert get_size(subfolder) == 12
    assert get_size(tmp_path) == 22

    entries = scan_directory(tmp_path)
    entry_map = {entry.name: entry for entry in entries}

    # verifying file1.txt details
    assert "file1.txt" in entry_map
    assert entry_map["file1.txt"].entry_type == "file"
    assert entry_map["file1.txt"].size == 4

    # verifying file2.txt details
    assert "file2.txt" in entry_map
    assert entry_map["file2.txt"].entry_type == "file"
    assert entry_map["file2.txt"].size == 6

    # verifying subfolder details
    assert "folder" in entry_map
    assert entry_map["folder"].entry_type == "directory"
    assert entry_map["folder"].size == 12

def test_get_size_handles_dissapearing_files_correctly(tmp_path: Path):
    folder = tmp_path / "folder"
    folder.mkdir()

    a = folder / "a.txt"
    a.write_text("abcdef") # 6 bytes

    b = folder / "b.txt"
    b.write_text("ab") # 2 bytes

    c = folder / "c.txt"
    c.write_text("abc") # 3 bytes

    c.unlink()

    assert get_size(folder) == 8