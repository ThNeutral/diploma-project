import torch
from torch import nn
from torch.utils import data
from torch import optim
from torch.utils.tensorboard import SummaryWriter

from tqdm.auto import tqdm

from dto.training import StepResult 

def train_step(
	*,
	model: nn.Module,
	dataloader: data.DataLoader,
	optimizer: optim.Optimizer,
	loss_fn: nn.Module,
	device: torch.device
) -> StepResult:
	model.train()

	total_loss = 0.0

	for X_train, y_train in tqdm(dataloader):
		X_train = X_train.to(device)
		y_train = y_train.to(device)
		
		y_pred = model(X_train)

		optimizer.zero_grad()

		loss = loss_fn(y_pred, y_train)
		loss.backward()

		optimizer.step()

		total_loss = loss.item() * len(X_train)

	avg_loss = total_loss / len(dataloader.dataset)

	return StepResult(
		avg_loss=avg_loss
	)
	