from src.classifier import classify_entry, find_candidates
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
    assert candidate.reason == "Application log file"

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