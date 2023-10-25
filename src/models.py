from dataclasses import dataclass

# Or Planet
@dataclass(frozen=True)
class System:
    name: str
    x: float
    y: float
    region: str
    type: str = 'System'
    importance: float = 0.0
    affiliation: str = "Neutral"