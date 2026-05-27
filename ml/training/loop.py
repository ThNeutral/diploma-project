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
		model.classifier.parameters(),
		lr=0.1,
		momentum=0.9,
		weight_decay=1e-4
	)

	warmup_epochs = 5

	warmup = optim.lr_scheduler.LinearLR(
    optimizer, start_factor=0.1, end_factor=1.0, total_iters=warmup_epochs
	)
	cosine = optim.lr_scheduler.CosineAnnealingLR(
    optimizer, T_max=epochs - warmup_epochs, eta_min=1e-6
	)
	scheduler = optim.lr_scheduler.SequentialLR(
    optimizer, schedulers=[warmup, cosine], milestones=[warmup_epochs]
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

		scheduler.step()

	tracker.flush()
	