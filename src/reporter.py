from src.candidate import Candidate

def format_size(size_bytes: int) -> str:
    if size_bytes < 0:
        raise ValueError("Size cannot be negative")
    
    units = ["B", "KB", "MB", "GB", "TB"]
    size = float(size_bytes)
    unit_index = 0

    while size >= 1024.0 and unit_index < len(units) - 1:
        size /= 1024.0
        unit_index += 1

    if unit_index == 0:
        return f"{int(size)} B"
    
    return f"{size:.2f} {units[unit_index]}"

def generate_report(candidates: list[Candidate], scanned_path: str = "") -> str:
    lines = []
    lines.append("Project: Mac - Cleaner Scan Report")
    if scanned_path:
        lines.append(f"Scanned: {scanned_path}")
        lines.append("")

    if not candidates:
        lines.append("No cleanup candidates found.")
        lines.append("")
        lines.append("Summary:")
        lines.append("Total Candidates: 0")
        lines.append("Candidate Space: 0 B")
        return "\n".join(lines)
    
    total_bytes = sum(candidate.size for candidate in candidates)
    suffix = "s" if len(candidates) > 1 else ""
    lines.append(f"Found {len(candidates)} candidate{suffix}:")

    lines.append("")

    for idx, candidate in enumerate(candidates, start=1):
        formatted_size = format_size(candidate.size)
        lines.append(f"[{idx}] {candidate.name}")
        lines.append(f"    Path:     {candidate.path}")
        lines.append(f"    Category: {candidate.category}")
        lines.append(f"    Size:     {formatted_size} ({candidate.size:,} bytes)")
        lines.append(f"    Safety:   {candidate.safety_classification}")
        lines.append(f"    Reason:   {candidate.reason}")
        lines.append("")
    
    lines.append("Summary:")
    lines.append(f"Total Candidates: {len(candidates)}")
    lines.append(f"Candidate Space: {format_size(total_bytes)}")

    return "\n".join(lines)