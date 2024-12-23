from dataclasses import dataclass, asdict
from typing import List


@dataclass
class PublicKey:
    sequence: List[int]

    @staticmethod
    def from_dict(data: dict):
        return PublicKey(data["sequence"])

    def dict(self):
        return {k: v for k, v in asdict(self).items()}
