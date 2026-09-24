from dataclasses import dataclass
from src.candidate import Candidate
from src.file_entry import FileEntry
from src.scanner import scan_directory

@dataclass
class Rule:
    rule_name: str
    match_type: str # "dir_name" or "file_extension" or "file_name"
    pattern: str
    category: str
    safety_classification: str
    reason: str

    def matches(self, entry: FileEntry) -> bool:
        if self.match_type == "dir_name":
            return entry.entry_type == "directory" and entry.name == self.pattern
        
        if self.match_type == "file_extension":
            return entry.entry_type == "file" and entry.name.endswith(self.pattern)
        
        if self.match_type == "file_name":
            return entry.entry_type == "file" and entry.name == self.pattern
        
        return False
    
DEFAULT_RULES = [
    # 1. Caches
    Rule(
        rule_name="Python Bytecode Cache",
        match_type="dir_name",
        pattern="__pycache__",
        category="cache",
        safety_classification="investigate",
        reason="Python compiled bytecode directory",
    ),
    # 2. Logs
    Rule(
        rule_name="Log File",
        match_type="file_extension",
        pattern=".log",
        category="log",
        safety_classification="investigate",
        reason="Application or runtime log file",
    ),
    # 3. Temporary Files
    Rule(
        rule_name="Temporary File (.tmp)",
        match_type="file_extension",
        pattern=".tmp",
        category="temp_file",
        safety_classification="investigate",
        reason="Temporary operational file",
    ),
    Rule(
        rule_name="Temporary File (.temp)",
        match_type="file_extension",
        pattern=".temp",
        category="temp_file",
        safety_classification="investigate",
        reason="Temporary operational file",
    ),
    # 4. System Metadata
    Rule(
        rule_name="macOS Finder Metadata",
        match_type="file_name",
        pattern=".DS_Store",
        category="system_metadata",
        safety_classification="investigate",
        reason="macOS Finder folder metadata file",
    )
]

def classify_entry(entry: FileEntry, rules: list[Rule] = DEFAULT_RULES) -> Candidate | None:
    # candidate returned if rule matches, else none returned
    for rule in rules:
        if rule.matches(entry):
            return Candidate(
                name=entry.name,
                path=entry.path,
                size=entry.size,
                category=rule.category,
                safety_classification=rule.safety_classification,
                reason=rule.reason,
            )
    return None

def find_candidates(entries: list[FileEntry], rules: list[Rule] = DEFAULT_RULES) -> list[Candidate]:
    candidates = []

    for entry in entries:
        candidate = classify_entry(entry, rules)
        if candidate is not None:
            candidates.append(candidate)

    return candidates

def scan_and_find_candidates(path: str, rules: list[Rule] = DEFAULT_RULES) -> list[Candidate]:
    entries = scan_directory(path)
    return find_candidates(entries, rules)