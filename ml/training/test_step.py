import torch
from torch import nn
from torch.utils import data

from tqdm.auto import tqdm

from dto.training import StepResult 

def test_step(
	model: nn.Module,
	dataloader: data.DataLoader,
	loss_fn: nn.Module,
	device: torch.device
) -> StepResult:
	model.eval()

	total_loss = 0.0

	for X_test, y_test in tqdm(dataloader):
		X_test = X_test.to(device)
		y_test = y_test.to(device)
		
		y_pred = model(y_test)

		loss = loss_fn(y_pred, y_test)

		total_loss = loss.item() * len(X_test)

	avg_loss = total_loss / len(dataloader.dataset)

	return StepResult(
		avg_loss=avg_loss
	)
	