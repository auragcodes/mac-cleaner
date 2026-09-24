from pathlib import Path
from src.classifier import classify_entry, find_candidates, scan_and_find_candidates
from src.file_entry import FileEntry

def test_find_candidates_filter_mixed_entries_correctly():
    matching_dir = FileEntry(
        name="__pycache__",
        path="/app/__pycache__",
        entry_type="directory",
        size=4096,
    )
    matching_log = FileEntry(
        name="server.log",
        path="/app/server.log",
        entry_type="file",
        size=1024,
    )
    ordinary_file = FileEntry(
        name="main.py",
        path="/app/main.py",
        entry_type="file",
        size=500,
    )
    ordinary_dir = FileEntry(
        name="src",
        path="/app/src",
        entry_type="directory",
        size=2048,
    )

    entries = [matching_dir, matching_log, ordinary_file, ordinary_dir]

    candidates = find_candidates(entries)

    assert len(candidates) == 2

    candidates_names = {candidate.name for candidate in candidates}
    assert "__pycache__" in candidates_names
    assert "server.log" in candidates_names
    assert "main.py" not in candidates_names
    assert "src" not in candidates_names

def test_classify_entry_matches_pycache_directory():
    entry = FileEntry(
        name="__pycache__",
        path="/some/path/__pycache__",
        entry_type="directory",
        size=4096,
    )

    candidate = classify_entry(entry)

    assert candidate is not None
    assert candidate.name == "__pycache__"
    assert candidate.path == "/some/path/__pycache__"
    assert candidate.size == 4096
    assert candidate.category == "cache"
    assert candidate.safety_classification == "investigate"
    assert candidate.reason == "Python compiled bytecode directory"

def test_classify_entry_matches_log_file():
    entry = FileEntry(
        name="app.log",
        path="/some/path/app.log",
        entry_type="file",
        size=1024,
    )

    candidate = classify_entry(entry)

    assert candidate is not None
    assert candidate.name == "app.log"
    assert candidate.path == "/some/path/app.log"
    assert candidate.size == 1024
    assert candidate.category == "log"
    assert candidate.safety_classification == "investigate"
    assert candidate.reason == "Application or runtime log file"

def test_classify_entry_ignores_unmatched_file_or_directory():
    regular_file = FileEntry(
        name="script.py",
        path="/some/path/script.py",
        entry_type="file",
        size=200,
    )
    regular_dir = FileEntry(
        name="src",
        path="/some/path/src",
        entry_type="directory",
        size=8192
    )

    candidate_file = classify_entry(regular_file)
    candidate_dir = classify_entry(regular_dir)

    assert candidate_file is None
    assert candidate_dir is None

def test_classify_entry_does_not_match_pycache_file():
    # if pycache is a file name and not directory name, it should not match
    entry = FileEntry(
        name="__pycache__",
        path="/some/path/__pycache__",
        entry_type="file",
        size=50
    )

    candidate = classify_entry(entry)

    assert candidate is None

def test_scan_and_find_candidates_end_to_end(tmp_path: Path):
    normal_file = tmp_path / "normal.txt"
    normal_file.write_text("regular python source code or text")

    log_file = tmp_path / "app.log"
    log_file.write_text("2026-09-22 ERROR Something crashed")

    pycache_dir = tmp_path / "__pycache__"
    pycache_dir.mkdir()

    compiled_file = pycache_dir / "module.cpython-314.pyc"
    compiled_file.write_text("bytecode")

    candidates = scan_and_find_candidates(tmp_path)

    assert len(candidates) == 2

    candidate_map = {candidate.name: candidate for candidate in candidates}

    assert "app.log" in candidate_map
    assert candidate_map["app.log"].category == "log"

    assert "__pycache__" in candidate_map
    assert candidate_map["__pycache__"].category == "cache"

    assert "normal.txt" not in candidate_map

def test_classify_entry_matches_tmp_file():
    entry = FileEntry(
        name="cache.tmp",
        path="/some/path/cache.tmp",
        entry_type="file",
        size=2048,
    )

    candidate = classify_entry(entry)

    assert candidate is not None
    assert candidate.name == "cache.tmp"
    assert candidate.category == "temp_file"
    assert candidate.safety_classification == "investigate"
    assert candidate.reason == "Temporary operational file"


def test_classify_entry_matches_temp_file():
    entry = FileEntry(
        name="data.temp",
        path="/some/path/data.temp",
        entry_type="file",
        size=1024,
    )

    candidate = classify_entry(entry)

    assert candidate is not None
    assert candidate.name == "data.temp"
    assert candidate.category == "temp_file"


def test_classify_entry_matches_ds_store():
    entry = FileEntry(
        name=".DS_Store",
        path="/some/path/.DS_Store",
        entry_type="file",
        size=6148,
    )

    candidate = classify_entry(entry)

    assert candidate is not None
    assert candidate.name == ".DS_Store"
    assert candidate.category == "system_metadata"
    assert candidate.safety_classification == "investigate"
    assert candidate.reason == "macOS Finder folder metadata file"


def test_classify_entry_does_not_match_ds_store_directory():
    # A directory named .DS_Store should NOT match file_name rule
    entry = FileEntry(
        name=".DS_Store",
        path="/some/path/.DS_Store",
        entry_type="directory",
        size=4096,
    )

    assert classify_entry(entry) is None


def test_find_candidates_all_four_rules():
    entries = [
        FileEntry(name="__pycache__", path="/app/__pycache__", entry_type="directory", size=4096),
        FileEntry(name="error.log", path="/app/error.log", entry_type="file", size=512),
        FileEntry(name="buffer.tmp", path="/app/buffer.tmp", entry_type="file", size=128),
        FileEntry(name=".DS_Store", path="/app/.DS_Store", entry_type="file", size=6148),
        FileEntry(name="main.py", path="/app/main.py", entry_type="file", size=1024),
    ]

    candidates = find_candidates(entries)

    assert len(candidates) == 4
    candidates_categories = {candidate.category for candidate in candidates}
    assert candidates_categories == {"cache", "log", "temp_file", "system_metadata"}