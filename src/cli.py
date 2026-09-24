import argparse
import sys
from pathlib import Path

from src.classifier import scan_and_find_candidates
from src.reporter import generate_report

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
    
    candidates = scan_and_find_candidates(str(target_path))
    report_text = generate_report(candidates, scanned_path=str(target_path.resolve()))
    print(report_text)
    return 0
