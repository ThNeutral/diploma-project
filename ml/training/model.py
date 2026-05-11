import torch
import logging
from torch import nn
import torchvision

from dto.training import ModelName

model_packages = {
	ModelName.EfficientNetV2_S: (
		torchvision.models.EfficientNet_V2_S_Weights,
		torchvision.models.efficientnet_v2_s,
	),
	ModelName.EfficientNetV2_M: (
		torchvision.models.EfficientNet_V2_M_Weights,
		torchvision.models.efficientnet_v2_m,
	)
}

def get_eval_transform(model_name: ModelName):
	weigths, _ = get_model_package(model_name)
	return weigths.transforms

def get_model_input_size_1d(model_name: ModelName):
	weights, _ = get_model_package(model_name)
	
	return weights.DEFAULT.transforms().crop_size[0]

def get_model_input_size_4d(model_name: ModelName):
	weights, _ = get_model_package(model_name)
	
	h = w = weights.DEFAULT.transforms().crop_size[0]
	return (1, 3, h, w)

def build_model(
	*,
	num_of_classes: int,
	model_name: ModelName,
	device: torch.device
):
	model_package = model_packages.get(model_name)
	assert model_package

	weights, model_factory = model_package
	model = model_factory(weights=weights.DEFAULT).to(device)

	for param in model.parameters():
		param.requires_grad = False

	model.classifier = nn.Sequential(
		nn.Dropout(0.2),
		nn.Linear(1280, num_of_classes)
	).to(device)

	return model

def get_model_package(model_name: ModelName):
	model_package = model_packages.get(model_name)
	assert model_package

	return model_package
