from pathlib import Path
from src.candidate import Candidate
from src.cleaner import DeletionStatus, delete_candidate


def test_delete_candidate_approved_file_deleted(tmp_path: Path):
    file_to_delete = tmp_path / "app.log"
    file_to_delete.write_text("log data")

    candidate = Candidate(
        name="app.log",
        path=str(file_to_delete),
        size=8,
        category="log",
        safety_classification="investigate",
        reason="Log file",
    )

    result = delete_candidate(candidate, scanned_path=tmp_path, approved=True)

    assert result.status == DeletionStatus.DELETED
    assert not file_to_delete.exists()


def test_delete_candidate_approved_directory_deleted(tmp_path: Path):
    dir_to_delete = tmp_path / "__pycache__"
    dir_to_delete.mkdir()
    (dir_to_delete / "cache.pyc").write_text("bytecode")

    candidate = Candidate(
        name="__pycache__",
        path=str(dir_to_delete),
        size=8,
        category="cache",
        safety_classification="investigate",
        reason="Python cache",
    )

    result = delete_candidate(candidate, scanned_path=tmp_path, approved=True)

    assert result.status == DeletionStatus.DELETED
    assert not dir_to_delete.exists()


def test_delete_candidate_not_approved_skipped(tmp_path: Path):
    file_to_keep = tmp_path / "app.log"
    file_to_keep.write_text("log data")

    candidate = Candidate(
        name="app.log",
        path=str(file_to_keep),
        size=8,
        category="log",
        safety_classification="investigate",
        reason="Log file",
    )

    result = delete_candidate(candidate, scanned_path=tmp_path, approved=False)

    assert result.status == DeletionStatus.SKIPPED
    assert file_to_keep.exists()


def test_delete_candidate_outside_scan_root_failed(tmp_path: Path):
    scanned_dir = tmp_path / "project"
    scanned_dir.mkdir()

    outside_dir = tmp_path / "outside"
    outside_dir.mkdir()
    outside_file = outside_dir / "secret.log"
    outside_file.write_text("data")

    candidate = Candidate(
        name="secret.log",
        path=str(outside_file),
        size=4,
        category="log",
        safety_classification="investigate",
        reason="Log file",
    )

    result = delete_candidate(candidate, scanned_path=scanned_dir, approved=True)

    assert result.status == DeletionStatus.FAILED
    assert "Safety check failed" in result.message
    assert outside_file.exists()


def test_delete_candidate_disappears_before_deletion_failed(tmp_path: Path):
    missing_file = tmp_path / "phantom.tmp"

    candidate = Candidate(
        name="phantom.tmp",
        path=str(missing_file),
        size=0,
        category="temp_file",
        safety_classification="investigate",
        reason="Temporary file",
    )

    result = delete_candidate(candidate, scanned_path=tmp_path, approved=True)

    assert result.status == DeletionStatus.FAILED
    assert "Safety check failed" in result.message or "vanished" in result.message


def test_delete_candidate_permission_error_handled(tmp_path: Path, monkeypatch):
    file_path = tmp_path / "readonly.log"
    file_path.write_text("protected log")

    candidate = Candidate(
        name="readonly.log",
        path=str(file_path),
        size=13,
        category="log",
        safety_classification="investigate",
        reason="Log file",
    )

    def mock_unlink(self):
        raise PermissionError("Permission denied")

    monkeypatch.setattr(Path, "unlink", mock_unlink)
    # since unit tests run with full permisions inside tmp_path, its tricky to trigger GENUINE file system permission
    # errors, thus monkeypatch is used to temporarily replace Path.unlink with mock_unlink.
    # whenever cleaner.py calls .unlink() on a Path instance during this test run, it won't touch the disk,
    # and will instantly throw a PermissionError("Permission denied")

    result = delete_candidate(candidate, scanned_path=tmp_path, approved=True)

    assert result.status == DeletionStatus.FAILED
    assert "Permission denied" in result.message
    assert file_path.exists()