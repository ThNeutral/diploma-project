from typing import Any
from dataclasses import dataclass, asdict

@dataclass
class ModelMetadata:
	input_size: tuple
	classes: list[str]

	def to_dict(self) -> dict[str, Any]:
		return asdict(self)