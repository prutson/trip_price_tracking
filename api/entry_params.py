from dataclasses import dataclass
from typing import Optional

@dataclass
class EntryParams:
    origem: str
    destino: str
    data: str
    passageiros: list