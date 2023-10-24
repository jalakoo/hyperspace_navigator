from dataclasses import dataclass

@dataclass
class System:
    name: str
    x: float
    y: float
    region: str
    type: str = 'System'
    importance: float = 0.0
    affiliation: str = "Neutral"