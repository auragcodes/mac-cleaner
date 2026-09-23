from dataclasses import dataclass
from src.candidate import Candidate
from src.file_entry import FileEntry
from src.scanner import scan_directory

@dataclass
class Rule:
    rule_name: str
    match_type: str # dir name or file(.extension)
    pattern: str
    category: str
    safety_classification: str
    reason: str

    def matches(self, entry: FileEntry) -> bool:
        if self.match_type == "dir_name":
            return entry.entry_type == "directory" and entry.name == self.pattern
        
        if self.match_type == "file_extension":
            return entry.entry_type == "file" and entry.name.endswith(self.pattern)
        
        return False
    
DEFAULT_RULES = [
    Rule(
        rule_name="Python Bytecode Cache",
        match_type="dir_name",
        pattern="__pycache__",
        category="cache",
        safety_classification="investigate",
        reason="Python compiled bytecode directory",
    ),
    Rule(
        rule_name="Log File",
        match_type="file_extension",
        pattern=".log",
        category="log",
        safety_classification="investigate",
        reason="Application log file",
    ),
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