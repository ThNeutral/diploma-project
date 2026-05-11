import torch
from torchvision import datasets
from utils.types import Transform
from pathlib import Path

def get_datasets_from_subfolders(
	source: Path,
	transforms: dict[str, Transform]
):
	train_dir = source / "train" 
	test_dir = source / "test" 
	assert train_dir.exists() and train_dir.is_dir()
	assert test_dir.exists() and test_dir.is_dir() 

	train_transform = transforms.get("train")
	test_transform = transforms.get("test")

	assert train_transform
	assert test_transform
	

	train_dataset = get_dataset_from_folder(
		source=train_dir,
		transform=train_transform
	)
	test_dataset = get_dataset_from_folder(
		source=test_dir,
		transform=test_transform
	)
	
	return (train_dataset, test_dataset)

def get_dataset_from_folder(
	source: Path,
	transform: Transform
):
	assert source.exists()

	dataset = datasets.ImageFolder(
		root=source,
		transform=transform
	)

	return dataset