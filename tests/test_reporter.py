import pytest
from src.candidate import Candidate
from src.reporter import format_size, generate_report

def test_format_size_converts_bytes_correctly():
    assert format_size(0) == "0 B"
    assert format_size(500) == "500 B"
    assert format_size(1024) == "1.00 KB"
    assert format_size(348160) == "340.00 KB"
    assert format_size(1048576) == "1.00 MB"
    assert format_size(1073741824) == "1.00 GB"

def test_format_size_raises_error_on_negative_bytes():
    with pytest.raises(ValueError, match="cannot be negative"):
        format_size(-100)

def test_generate_report_with_candidates():
    candidates = [
        Candidate(
            name="app.log",
            path="/app/app.log",
            size=1048576,  # 1.00 MB
            category="log",
            safety_classification="investigate",
            reason="Application log file",
        ),
        Candidate(
            name="__pycache__",
            path="/app/__pycache__",
            size=512000,  # 500 KB
            category="cache",
            safety_classification="investigate",
            reason="Python compiled bytecode directory",
        ),
    ]

    report = generate_report(candidates, scanned_path="/app")

    assert "Project: Mac - Cleaner Scan Report" in report
    assert "Scanned: /app" in report
    assert "Found 2 candidates" in report
    assert "[1] app.log" in report
    assert "Size:     1.00 MB" in report
    assert "[2] __pycache__" in report
    assert "Total Candidates: 2" in report
    assert "Candidate Space: 1.49 MB" in report

def test_generate_report_without_candidates():
    report = generate_report([], scanned_path="/empty_dir")

    assert "No cleanup candidates found." in report
    assert "Total Candidates: 0" in report
    assert "Candidate Space: 0 B" in report