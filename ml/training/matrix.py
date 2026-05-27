from pathlib import Path
import torch
from torch.utils.data import DataLoader
from torchvision.datasets import ImageFolder
from torchvision import transforms
from torch.utils.tensorboard import SummaryWriter
from torchmetrics import ConfusionMatrix

from .loop import train_model_
from .save_model import save_model

from tracking import ExperimentTracker

from datasets.human_readable_classes import PLANT_VILLAGE_HUMAN_READABLE_LABELS

from .model import get_model_input_size_1d, get_model_input_size_4d, build_model, get_eval_transform
from datasets.data import get_dataset_from_folder
from dto.training import StepName, ModelMetadata

from utils.types import Transform

from dto.training import ModelName

from config import JSONConfig

def train_variations_from_config(
	config: JSONConfig
):
	sources = {
		StepName.Train: config.train_data_dir,
		StepName.Test: config.test_data_dir,
		StepName.Validation: config.val_data_dir
	}

	device = config.device
	if not device:
		device = torch.accelerator.current_accelerator() if torch.accelerator.is_available() else 'cpu'

	print(f"Using device: {device}")

	run_settings = config.run_settings

	for run_config in config.to_product():
		_train_from_config(
			output_model_name=run_config.get_run_name(),
			base_model_name=run_config.model_name,
			should_augment=run_config.should_augment,
			device=device,
			sources=sources,
			epochs=run_settings.epochs,
			batch_size=run_settings.batch_size,
			output_dir=config.output_dir,
			num_workers=run_settings.num_workers,
			unfrozen_blocks=run_config.unfrozen_blocks
		)	

def _train_from_config(
	*,
	base_model_name: ModelName,
	output_model_name: str,
	should_augment: bool,
	device: torch.device,
	sources: dict[StepName, Path],
	output_dir: Path,
	epochs: int,
	batch_size: int,
	num_workers: int,
	unfrozen_blocks: int
):
	output_dir = output_dir / output_model_name
	output_dir.mkdir(parents=True, exist_ok=True)
	
	tracker = ExperimentTracker(
		log_dir=output_dir / "logs"
	) 

	input_size = get_model_input_size_1d(base_model_name)
	
	eval_transform = get_eval_transform(base_model_name)
	train_transform = _build_train_transform(input_size, should_augment)

	transforms = {
		StepName.Train: train_transform,
		StepName.Test: eval_transform,
		StepName.Validation: eval_transform
	}

	datasources = _get_datasources(
		sources=sources,
		transforms=transforms
	)

	classes = datasources[StepName.Train].classes
	num_of_classes = len(classes)

	cm_fn = ConfusionMatrix(
		task="multiclass",
		num_classes=num_of_classes
	).to(device)

	dataloaders = _get_dataloaders(
		datasources=datasources,
		batch_size=batch_size,
		num_workers=num_workers
	)

	model = build_model(
		num_of_classes=num_of_classes, 
		model_name=base_model_name, 
		device=device,
		unfrozen_blocks=unfrozen_blocks
	)

	train_model_(
		model=model,
		cm_fn=cm_fn,
		dataloaders=dataloaders,
		epochs=epochs,
		device=device,
		tracker=tracker
	)	

	metadata = ModelMetadata(
		input_size=get_model_input_size_4d(base_model_name),
		classes=PLANT_VILLAGE_HUMAN_READABLE_LABELS
	)

	save_model(
		model=model,
		output_folder=output_dir,
		model_metadata=metadata,
		model_name=output_model_name,
		device=device
	)

	tracker.close()


def _build_train_transform(input_size: int, should_augment: bool):
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

	return transforms.Compose(transforms_stack)


def _get_datasources(
	sources: dict[StepName, Path],
	transforms: dict[StepName, Transform]
) -> dict[StepName, ImageFolder]:
	datasources: dict[StepName, ImageFolder] = {}

	for (name, source) in sources.items():
		transform = transforms[name]

		datasource = get_dataset_from_folder(
			source=source,
			transform=transform
		)

		datasources[name] = datasource

	return datasources

def _get_dataloaders(
	datasources: dict[StepName, ImageFolder],
	batch_size: int,
	num_workers: int
) -> dict[StepName, DataLoader]:
	dataloaders: dict[StepName, DataLoader] = {}

	for (name, datasource) in datasources.items():
		dataloader = DataLoader(
			dataset=datasource,
			batch_size=batch_size,
			num_workers=num_workers,
			persistent_workers=True,
			prefetch_factor=2,
			shuffle=name == "train"
		)

		dataloaders[name] = dataloader

	return dataloaders