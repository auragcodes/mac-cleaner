from dataclasses import dataclass

@dataclass
class Candidate:
    path: str
    size: int
    category: str
    safety_classification: str
    reason: str