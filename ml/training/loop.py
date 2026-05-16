import torch
from torch.utils.data import DataLoader
from torchvision import transforms
from utils import logging
from pathlib import Path
import os
import json
from torch import optim
from torch import nn

from .model import get_eval_transform, build_model, ModelName, get_model_input_size_1d, get_model_input_size_4d
from datasets.data import get_datasets_from_subfolders, get_dataset_from_folder

from dto.training import ModelMetadata
from utils.types import Transform

from .train_step import train_step
from .test_step import test_step
from .val_step import val_step

def train_model(
		*,
		base_model_name: ModelName,
		data_dir: Path,
		val_data_dir: Path,
		epochs: int,
		batch_size: int,
		train_transform: Transform,
		device: torch.device
) -> tuple[nn.Module, ModelMetadata]:
	logging.info("Using device %s", device)

	logging.debug("Using base model %s", base_model_name)

	eval_transform = get_eval_transform(base_model_name) 

	train_dataset, test_dataset = get_datasets_from_subfolders(
		source=data_dir,
		transforms={
			"train": train_transform,			
			"test": eval_transform,			
		}
	)
	class_to_idx = train_dataset.class_to_idx
	classes = train_dataset.classes
	logging.debug("Classes: ")
	logging.debug(classes)

	validation_dataset = get_dataset_from_folder(
		source=val_data_dir,
		transform=eval_transform
	)

	train_dataloader = DataLoader(
		dataset=train_dataset,
		batch_size=batch_size,
		shuffle=True,
		num_workers=4
	)
	test_dataloader = DataLoader(
		dataset=test_dataset,
		batch_size=batch_size,
		shuffle=False, 
		num_workers=4
	)

	validation_dataloader = DataLoader(
		dataset=validation_dataset,
		batch_size=batch_size,
		shuffle=True,
		num_workers=4
	)

	num_of_classes = len(class_to_idx)

	model = build_model(
		num_of_classes=num_of_classes, 
		model_name=base_model_name, 
		device=device
	)
	
	X, y = next(iter(train_dataloader))
	logging.debug("Dataset size")
	logging.debug("\tX: %s", X.shape)
	logging.debug("\ty: %s", y.shape)

	model.train()
	y_pred = model(X.to(device))
	logging.debug("Model output size")
	logging.debug("\t%s", y_pred.shape)
	
	X, y = next(iter(validation_dataloader))
	logging.debug("Validation size")
	logging.debug("\tX: %s", X.shape)
	logging.debug("\ty: %s", y.shape)

	optimizer = optim.SGD(
		params=model.classifier.parameters()
	)

	loss_fn = nn.CrossEntropyLoss()

	for epoch in range(epochs):
		train_result = train_step(
			model=model,
			dataloader=train_dataloader,
			optimizer=optimizer,
			loss_fn=loss_fn,
			device=device
		)
		print(f"Epoch: {epoch}. Train. Loss {train_result.avg_loss}")

		test_result = test_step(
			model=model,
			dataloader=test_dataloader,
			loss_fn=loss_fn,
			device=device
		)
		print(f"Epoch: {epoch}. Test. Loss {test_result.avg_loss}")

		val_result = val_step(
			model=model,
			dataloader=validation_dataloader,
			loss_fn=loss_fn,
			device=device
		)
		print(f"Epoch: {epoch}. Test. Loss {val_result.avg_loss}")

	metadata = ModelMetadata(
		input_size=get_model_input_size_4d(base_model_name),
		classes=classes
	)
	return (model, metadata)
	