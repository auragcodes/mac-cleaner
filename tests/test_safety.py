from pathlib import Path
import pytest
from src.candidate import Candidate
from src.safety import SafetyError, validate_candidate_for_deletion


def test_validate_candidate_valid_inside_scanned_path(tmp_path: Path):
    candidate_file = tmp_path / "app.log"
    candidate_file.write_text("log data")

    candidate = Candidate(
        name="app.log",
        path=str(candidate_file),
        size=8,
        category="log",
        safety_classification="investigate",
        reason="Log file",
    )

    validate_candidate_for_deletion(candidate, scanned_path=tmp_path, approved=True)


def test_validate_candidate_unapproved_raises_error(tmp_path: Path):
    candidate_file = tmp_path / "app.log"
    candidate_file.write_text("log data")

    candidate = Candidate(
        name="app.log",
        path=str(candidate_file),
        size=8,
        category="log",
        safety_classification="investigate",
        reason="Log file",
    )

    with pytest.raises(SafetyError, match="not explicitly approved"):
        validate_candidate_for_deletion(candidate, scanned_path=tmp_path, approved=False)


def test_validate_candidate_missing_path_raises_error(tmp_path: Path):
    missing_file = tmp_path / "nonexistent.tmp" # we didnt write_text or touch the file, therefore, its nonexistent

    candidate = Candidate(
        name="nonexistent.tmp",
        path=str(missing_file),
        size=0,
        category="temp_file",
        safety_classification="investigate",
        reason="Temporary file",
    )

    with pytest.raises(SafetyError, match="does not exist"):
        validate_candidate_for_deletion(candidate, scanned_path=tmp_path, approved=True)


def test_validate_candidate_outside_scanned_path_raises_error(tmp_path: Path):
    scanned_dir = tmp_path / "project"
    scanned_dir.mkdir()

    outside_dir = tmp_path / "outside" # "project" and "outside" has a sibling relationship and not a parent-child relationship
    outside_dir.mkdir()
    outside_file = outside_dir / "secret.log"
    outside_file.write_text("secret")

    candidate = Candidate(
        name="secret.log",
        path=str(outside_file),
        size=6,
        category="log",
        safety_classification="investigate",
        reason="Log file",
    )

    with pytest.raises(SafetyError, match="is outside the scanned directory"):
        validate_candidate_for_deletion(candidate, scanned_path=scanned_dir, approved=True)


def test_validate_candidate_is_scanned_root_raises_error(tmp_path: Path):
    candidate = Candidate(
        name=tmp_path.name,
        path=str(tmp_path),
        size=4096,
        category="cache",
        safety_classification="investigate",
        reason="Root directory",
    )

    with pytest.raises(SafetyError, match="identical to the scanned root directory"):
        validate_candidate_for_deletion(candidate, scanned_path=tmp_path, approved=True)


def test_validate_candidate_protected_system_path_raises_error():
    candidate = Candidate(
        name="System",
        path="/System",
        size=0,
        category="system_metadata",
        safety_classification="investigate",
        reason="Protected path",
    )

    with pytest.raises(SafetyError, match="is a protected system path"):
        validate_candidate_for_deletion(candidate, scanned_path="/", approved=True)

def test_validate_candidate_symlink_pointing_outside_scanned_path_raises_error(tmp_path: Path):
    scanned_dir = tmp_path / "project"
    scanned_dir.mkdir()

    outside_dir = tmp_path / "outside"
    outside_dir.mkdir()
    target_file = outside_dir / "secret.log"
    target_file.write_text("critical data")

    # 2. symlink inside scanned_dir pointing the the outside file
    symlink_path = scanned_dir / "outside_link.log"
    symlink_path.symlink_to(target_file)

    candidate = Candidate(
        name="outside_link.log",
        path=str(symlink_path),
        size=13,
        category="log",
        safety_classification="investigate",
        reason="Symlink to log file",
    )

    with pytest.raises(SafetyError, match="is outside the scanned directory"):
        validate_candidate_for_deletion(candidate, scanned_path=scanned_dir, approved=True)