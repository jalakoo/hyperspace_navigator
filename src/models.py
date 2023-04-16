from dataclasses import dataclass

@dataclass
class System:
    name: str
    x: float
    y: float
    region: str
    type: str = 'System'
