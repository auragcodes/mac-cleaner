import argparse
import sys
from pathlib import Path

from src.candidate import Candidate
from src.classifier import scan_and_find_candidates
from src.cleaner import DeletionStatus, delete_candidate
from src.reporter import generate_report

def prompt_and_cleanup_candidates(candidates: list[Candidate], scanned_path: Path) -> tuple[int, int, int]:
    print("\nInteractive Cleanup Session")

    deleted_count = 0
    skipped_count = 0
    failed_count = 0

    for idx, candidate in enumerate(candidates, 1):
        try:
            response = (
                input(f"Delete candidate [{idx}] '{candidate.name}'? (y/n): ")
                .strip()
                .lower()
            )
        except (KeyboardInterrupt, EOFError):
            print("\nCleanup interrupted by user. Exiting.")
            break

        approved = response == "y"

        result = delete_candidate(
            candidate=candidate,
            scanned_path=scanned_path,
            approved=approved
        )

        if result.status == DeletionStatus.DELETED:
            print(f"[DELETED] {candidate.name}")
            deleted_count += 1
        elif result.status == DeletionStatus.SKIPPED:
            print(f"[SKIPPED] {candidate.name}")
            skipped_count += 1
        else:
            print(f"[FAILED] {candidate.name}: {result.message}")
            failed_count += 1
    
    return deleted_count, skipped_count, failed_count


def run_cli(args: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Scans a directory and identifies potential cleanup candidates")
    parser.add_argument(
        "path",
        nargs="?",
        default=".",
        help="Directory path to scan (defaults to current directory '.')"
    )

    passed_args = parser.parse_args(args)
    target_path = Path(passed_args.path)

    if not target_path.exists():
        print(f"Error: Path '{target_path}' does not exist.", file=sys.stderr)
        return 1
    
    if not target_path.is_dir():
        print(f"Error: Path '{target_path}' is a file, not a directory.", file=sys.stderr)
        return 1
    
    resolved_target = target_path.resolve()

    candidates = scan_and_find_candidates(str(resolved_target))

    report_text = generate_report(candidates, scanned_path=str(resolved_target))
    print(report_text)

    if not candidates:
        return 0
    
    deleted, skipped, failed = prompt_and_cleanup_candidates(
        candidates=candidates,
        scanned_path=resolved_target
    )

    print("\nCleanup Summary:")
    print(f"Total Processed: {len(candidates)}")
    print(f"Deleted: {deleted}")
    print(f"Skipped: {skipped}")
    print(f"Failed:  {failed}")

    return 0