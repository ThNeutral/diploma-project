import datetime
from pathlib import Path
from itertools import product
from dataclasses import dataclass

from dto.training import ModelName

@dataclass
class RunConfig:
	unfrozen_blocks: int
	should_augment: bool
	model_name: ModelName

	def __post_init__(self):
		self.model_name = ModelName(self.model_name)

	def get_run_name(self):
		return f"{self.model_name}_{self.should_augment}_{self.unfrozen_blocks}"

@dataclass
class RunSettings:
	epochs: int
	batch_size: int
	num_workers: int

@dataclass
class _RunConfigRaw:
	unfrozen_blocks: list[int]
	should_augment: list[bool]
	model_name: list[ModelName]
	
	def to_product(self) -> list[RunConfig]:
		prod = product(
			self.unfrozen_blocks,
			self.should_augment,
			self.model_name
		)

		configs = map(lambda config: RunConfig(
			unfrozen_blocks=config[0],
			should_augment=config[1],
			model_name=config[2]
		), prod)

		return list(configs)

@dataclass
class JSONConfig:
	run_config: _RunConfigRaw
	run_settings: RunSettings
	
	train_data_dir: Path
	test_data_dir: Path
	val_data_dir: Path
	
	output_dir: Path

	device: str | None = None

	def __post_init__(self):
		self.run_config = _RunConfigRaw(**self.run_config)
		self.run_settings = RunSettings(**self.run_settings)

		self.train_data_dir = Path(self.train_data_dir)
		self.test_data_dir = Path(self.test_data_dir)
		self.val_data_dir = Path(self.val_data_dir)

		time_format = "%Y-%m-%dT%H-%M-%S"
		now = datetime.datetime.now() 
		self.output_dir = Path(self.output_dir) / now.strftime(time_format)

	def to_product(self) -> list[RunConfig]:
		return self.run_config.to_product()