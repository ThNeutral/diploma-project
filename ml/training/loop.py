import torch
from torch.utils.data import DataLoader
from utils import logging
from torch import optim
from torch import nn

from tracking import ExperimentTracker

from dto.training import StepName

from .train_step import train_step
from .test_step import test_step
from .val_step import val_step

def train_model_(
		*,
		tracker: ExperimentTracker,
		model: nn.Module,
		dataloaders: dict[StepName, DataLoader],
		epochs: int,
		device: torch.device
):
	optimizer = optim.SGD(
		params=model.classifier.parameters()
	)

	loss_fn = nn.CrossEntropyLoss()

	for epoch in range(epochs):
		logging.info(f"Epoch: {epoch}")
		
		logging.info(f"{StepName.Train}")
		train_result = train_step(
			model=model,
			dataloader=dataloaders[StepName.Train],
			optimizer=optimizer,
			loss_fn=loss_fn,
			device=device
		)
		logging.info(f"Loss {train_result.avg_loss}")

		logging.info(f"{StepName.Test}")
		test_result = test_step(
			model=model,
			dataloader=dataloaders[StepName.Test],
			loss_fn=loss_fn,
			device=device
		)
		logging.info(f"Loss {test_result.avg_loss}")

		logging.info(f"{StepName.Validation}")
		val_result = val_step(
			model=model,
			dataloader=dataloaders[StepName.Validation],
			loss_fn=loss_fn,
			device=device
		)
		logging.info(f"Loss {val_result.avg_loss}")

		tracker.track_step({
			StepName.Train: train_result,
			StepName.Test: test_result,
			StepName.Validation: val_result
		}, epoch)

	tracker.flush()
	