import torch
import collections

from .classes import PLANT_DOC_CLASSES, PLANT_VILLAGE_CLASSES

_PLANT_DOC_TO_PLANT_VILLAGE: collections.OrderedDict[str, str] = collections.OrderedDict(
	sorted(
		{
			"Apple leaf": "Apple__healthy",
			"Apple rust leaf": "Apple__Cedar_apple_rust",
			"Apple Scab Leaf": "Apple__Apple_scab",
			"Bell_pepper leaf": "Pepper__bell__healthy",
			"Bell_pepper leaf spot": "Pepper__bell__Bacterial_spot",
			"Blueberry leaf": "Blueberry__healthy",
			"Cherry leaf": "Cherry_(including_sour)__healthy",
			"Corn Gray leaf spot": "Corn_(maize)__Cercospora_leaf_spot_Gray_leaf_spot",
			"Corn leaf blight": "Corn_(maize)__Northern_Leaf_Blight",
			"Corn rust leaf": "Corn_(maize)__Common_rust_",
			"grape leaf": "Grape__healthy",
			"grape leaf black rot": "Grape__Black_rot",
			"Peach leaf": "Peach__healthy",
			"Potato leaf early blight": "Potato__Early_blight",
			"Potato leaf late blight": "Potato__Late_blight",
			"Raspberry leaf": "Raspberry__healthy",
			"Soyabean leaf": "Soybean__healthy",
			"Squash Powdery mildew leaf": "Squash__Powdery_mildew",
			"Strawberry leaf": "Strawberry__healthy",
			"Tomato Early blight leaf": "Tomato__Early_blight",
			"Tomato leaf": "Tomato__healthy",
			"Tomato leaf bacterial spot": "Tomato__Bacterial_spot",
			"Tomato leaf late blight": "Tomato__Late_blight",
			"Tomato leaf mosaic virus": "Tomato__Tomato_mosaic_virus",
			"Tomato leaf yellow virus": "Tomato__Tomato_Yellow_Leaf_Curl_Virus",
			"Tomato mold leaf": "Tomato__Leaf_Mold",
			"Tomato Septoria leaf spot": "Tomato__Septoria_leaf_spot",
			"Tomato two spotted spider mites leaf": "Tomato__Spider_mites_Two-spotted_spider_mite"
		}.items()
	)
)

assert len(PLANT_DOC_CLASSES) == len(_PLANT_DOC_TO_PLANT_VILLAGE)

for (key, value) in _PLANT_DOC_TO_PLANT_VILLAGE.items():
	assert key in PLANT_DOC_CLASSES, key
	assert value in PLANT_VILLAGE_CLASSES, value


def map_plant_doc_to_plant_village(plant_doc_tensor: torch.Tensor, device: torch.device) -> torch.Tensor:
	assert len(plant_doc_tensor.shape) == 1

	mapped_tensor = torch.zeros(plant_doc_tensor.shape)
	for (tensor_index, entry) in enumerate(plant_doc_tensor):
		plant_doc_index = entry.item()
		assert type(plant_doc_index) is int

		plant_doc_class_str = PLANT_DOC_CLASSES[plant_doc_index]
		plant_village_class_str = _PLANT_DOC_TO_PLANT_VILLAGE.get(plant_doc_class_str)
		assert plant_village_class_str
		
		plant_doc_index = PLANT_VILLAGE_CLASSES.index(plant_village_class_str)
		mapped_tensor[tensor_index] = plant_doc_index

	return mapped_tensor.type(torch.long).to(device)

# Test mapper
if __name__ == "__main__":
	print("Running test for map_plant_doc_to_plant_village")

	import numpy

	device = "cpu"

	plant_doc_tensor = torch.from_numpy(
		numpy.array([
			PLANT_DOC_CLASSES.index(entry) 
			for entry in ["grape leaf black rot", "Tomato Early blight leaf", "Tomato leaf yellow virus"]])
	).to(device)

	actual_plant_village_tensor = map_plant_doc_to_plant_village(plant_doc_tensor, device=device)
	expected_plant_village_tensor = torch.from_numpy(
		numpy.array([
			11, 29, 35 
		])
	)

	assert torch.equal(actual_plant_village_tensor, expected_plant_village_tensor), (actual_plant_village_tensor, expected_plant_village_tensor)
	
	print("Success")