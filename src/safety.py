from pathlib import Path
from src.candidate import Candidate

class SafetyError(Exception):
    pass

PROTECTED_SYSTEM_PATHS = {
    Path("/"),
    Path("/System"),
    Path("/Library"),
    Path("/Users"),
    Path("/Applications"),
    Path("/bin"),
    Path("/sbin"),
    Path("/usr"),
    Path("/var"),
    Path("/etc"),
    Path("/private"),
}

def validate_candidate_for_deletion(candidate: Candidate, scanned_path: str | Path, approved: bool = False) -> None:
    if not approved:
        raise SafetyError(f"Candidate '{candidate.name}' was not explicitly approved for deletion.")
    
    resolved_scanned_path = Path(scanned_path).resolve()
    resolved_candidate_path = Path(candidate.path).resolve()

    if not resolved_candidate_path.exists():
        raise SafetyError(f"Candidate path does not exist: {resolved_candidate_path}")
    
    if resolved_candidate_path == resolved_scanned_path:
        raise SafetyError(f"Candidate path '{resolved_candidate_path}' is identical to the scanned root directory")
    
    if not resolved_candidate_path.is_relative_to(resolved_scanned_path):
        raise SafetyError(f"Candidate path '{resolved_candidate_path}' is outside the scanned directory '{resolved_scanned_path}'")
    
    if resolved_candidate_path in PROTECTED_SYSTEM_PATHS:
        raise SafetyError(f"Candidate path '{resolved_candidate_path}' is a protected system path")