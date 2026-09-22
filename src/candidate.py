from dataclasses import dataclass

@dataclass
class Candidate:
    name: str
    path: str
    size: int
    category: str
    safety_classification: str
    reason: str