from dataclasses import dataclass
from enum import Enum
from pathlib import Path
import shutil
from src.candidate import Candidate
from src.safety import SafetyError, validate_candidate_for_deletion

class DeletionStatus(Enum):
    DELETED = "deleted"
    SKIPPED = "skipped"
    FAILED = "failed"

@dataclass
class DeletionResult:
    candidate: Candidate
    status: DeletionStatus
    message: str = ""

def delete_candidate(candidate: Candidate, scanned_path: str | Path, approved: bool = False) -> DeletionResult:
    if not approved:
        return DeletionResult(
            candidate=candidate,
            status=DeletionStatus.SKIPPED,
            message="User declined deletion"
        )
    
    try:
        validate_candidate_for_deletion(
            candidate=candidate,
            scanned_path=scanned_path,
            approved=approved
        )
    except SafetyError as e:
        return DeletionResult(
            candidate=candidate,
            status=DeletionStatus.FAILED,
            message=f"Safety check failed: {e}"
        )
    
    resolved_path = Path(candidate.path).resolve()

    if not resolved_path.exists():
        return DeletionResult(
            candidate=candidate,
            status=DeletionStatus.FAILED,
            message="File or directory vanished before deletion could take place"
        )
    
    try:
        if resolved_path.is_dir() and not resolved_path.is_symlink():
            shutil.rmtree(resolved_path)
        else:
            resolved_path.unlink()

        return DeletionResult(
            candidate=candidate,
            status=DeletionStatus.DELETED,
            message="Successfully removed"
        )
    except OSError as e:
        return DeletionResult(
            candidate=candidate,
            status=DeletionStatus.FAILED,
            message=f"OS/Permission error: {e.strerror or e}",
        )