from dataclasses import dataclass
from typing import List


@dataclass
class PrivateKey:
    sequence: List[int]
    m: int
    n: int
