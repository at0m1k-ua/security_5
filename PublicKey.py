from dataclasses import dataclass
from typing import List


@dataclass
class PublicKey:
    sequence: List[int]
