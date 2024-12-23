from dataclasses import dataclass, asdict
from typing import List


@dataclass
class PrivateKey:
    sequence: List[int]
    m: int
    n: int

    @staticmethod
    def from_dict(data: dict):
        return PrivateKey(data["sequence"],
                          data["m"],
                          data["n"])

    def dict(self):
        return {k: v for k, v in asdict(self).items()}

