import torch
from torchmetrics import Metric
from torch.utils.data import DataLoader
from utils import logging
from torch import optim
from torch import nn

from tracking import ExperimentTracker

from dto.training import StepName

from .step import step

def train_model_(
		*,
		tracker: ExperimentTracker,
		cm_fn: Metric,
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
		train_result = step(
			model=model,
			cm_fn=cm_fn,
			dataloader=dataloaders[StepName.Train],
			optimizer=optimizer,
			loss_fn=loss_fn,
			device=device
		)
		logging.info(f"{train_result}")

		logging.info(f"{StepName.Test}")
		test_result = step(
			model=model,
			cm_fn=cm_fn,
			dataloader=dataloaders[StepName.Test],
			loss_fn=loss_fn,
			device=device
		)
		logging.info(f"{test_result}")

		logging.info(f"{StepName.Validation}")
		val_result = step(
			model=model,
			cm_fn=cm_fn,
			dataloader=dataloaders[StepName.Validation],
			loss_fn=loss_fn,
			device=device
		)
		logging.info(f"{val_result}")

		tracker.track_epoch({
			StepName.Train: train_result,
			StepName.Test: test_result,
			StepName.Validation: val_result
		}, epoch)

	tracker.flush()
	