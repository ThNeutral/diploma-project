from pathlib import Path

import torch
from torchvision import transforms

from .loop import train_model
from .save_model import save_model

from .model import get_model_input_size_1d

from utils.types import Transform

from dto.training import ModelName

MODELS = [
	ModelName.EfficientNetV2_S,
	ModelName.EfficientNetV2_M
]

SHOULD_AUGMENT = [
	False,
	True
]

def train_variations(
	data_dir: Path,
	val_data_dir: Path,
	output_dir: Path,
	epochs: int,
	batch_size: int
):
	device = torch.accelerator.current_accelerator() if torch.accelerator.is_available() else 'cpu'
	for model in MODELS:
		for should_augment in SHOULD_AUGMENT:
			_train_from_config(
				output_model_name=f"{model}_{should_augment}",
				base_model_name=model,
				should_augment=should_augment,
				device=device,
				data_dir=data_dir,
				val_data_dir=val_data_dir,
				epochs=epochs,
				batch_size=batch_size,
				output_dir=output_dir
			)	
	pass

def _train_from_config(
	*,
	base_model_name: ModelName,
	output_model_name: str,
	should_augment: bool,
	device: torch.device,
	data_dir: Path,
	val_data_dir: Path,
	output_dir: Path,
	epochs: int,
	batch_size: int
):
	input_size = get_model_input_size_1d(base_model_name)

	transforms_stack: list[Transform] = [transforms.Resize(input_size)]
	if should_augment:
		transforms_stack.append(
			transforms.TrivialAugmentWide()
		)
	transforms_stack.append(
		transforms.ToTensor()
	)
	transforms_stack.append(
		transforms.Normalize(
			mean=[0.485, 0.456, 0.406],
			std=[0.229, 0.224, 0.225]
		)
	)

	train_transform = transforms.Compose(transforms_stack)

	model, metadata = train_model(
		base_model_name=base_model_name,
		data_dir=data_dir,
		val_data_dir=val_data_dir,
		epochs=epochs,
		batch_size=batch_size,
		train_transform=train_transform,
		device=device
	)	

	output_dir = output_dir / output_model_name
	output_dir.mkdir(parents=True, exist_ok=True)

	save_model(
		model=model,
		output_folder=output_dir,
		model_metadata=metadata,
		model_name=output_model_name,
		device=device
	)