import torch
from torch import nn
from torch.utils import data
from torch import optim
from torchmetrics import ConfusionMatrix

from tqdm.auto import tqdm

from dto.training import StepResult 

from datasets.mapper import map_plant_doc_to_plant_village

def step(
	*,
	model: nn.Module,
	cm_fn: ConfusionMatrix,
	dataloader: data.DataLoader,
	optimizer: optim.Optimizer | None = None,
	loss_fn: nn.Module,
	device: torch.device,
	should_transform_data: bool = False
) -> StepResult:
	if optimizer is not None:
		model.train()
	else:
		model.eval()

	total_loss = 0.0
	confusion_matrix = None

	context = torch.enable_grad() if optimizer is not None else torch.no_grad()

	with context:
		for i, (X_data, y_data) in enumerate(tqdm(dataloader)):
			X_data = X_data.to(device)
			y_data = y_data.to(device)
		
			if should_transform_data:
				y_data = map_plant_doc_to_plant_village(y_data, device=device)
			
			y_pred = model(X_data)

			if optimizer is not None:
				optimizer.zero_grad()

			loss = loss_fn(y_pred, y_data)
			
			if optimizer is not None:
				loss.backward()
				optimizer.step()

			total_loss += loss.item() * len(X_data)

			cm = cm_fn(
				y_pred,
				y_data
			)
			confusion_matrix = cm if confusion_matrix is None else confusion_matrix + cm

	avg_loss = total_loss / len(dataloader.dataset)

	return StepResult(
		avg_loss=avg_loss,
		confusion_matrix=confusion_matrix
	)
