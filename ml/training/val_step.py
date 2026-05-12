import torch
from torch import nn
from torch.utils import data
from torch import optim

from tqdm.auto import tqdm

from dto.training import StepResult 

from datasets.mapper import map_plant_village_to_plant_doc

def val_step(
	*,
	model: nn.Module,
	dataloader: data.DataLoader,
	loss_fn: nn.Module,
	device: torch.device
) -> StepResult:
	total_loss = 0.0	

	for X_val, y_val in tqdm(dataloader):	
		X_val = X_val.to(device)
		y_val = y_val.to(device)

		y_pred = model(X_val)
		X_val = map_plant_village_to_plant_doc(y_val)

		loss = loss_fn(y_pred, y_val)

		total_loss = loss.item() * len(X_val)

	avg_loss = total_loss / len(dataloader)

	step_result = StepResult(
		avg_loss=avg_loss
	)
	return step_result