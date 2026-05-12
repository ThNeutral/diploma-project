import torch

PLANT_VILLAGE_CLASSES: list[str] = [
	"Apple__Apple_scab",
	"Apple__Black_rot",
	"Apple__Cedar_apple_rust",
	"Apple__healthy",
	"Blueberry__healthy",
	"Cherry_(including_sour)__healthy",
	"Cherry_(including_sour)__Powdery_mildew",
	"Corn_(maize)__Cercospora_leaf_spot_Gray_leaf_spot",
	"Corn_(maize)__Common_rust_",
	"Corn_(maize)__Northern_Leaf_Blight",
	"Corn_(maize)__healthy",
	"Grape__Black_rot",
	"Grape__Esca_(Black_Measles)",
	"Grape__Leaf_blight_(Isariopsis_Leaf_Spot_)",
	"Grape__healthy",
	"Orange__Haunglongbing_(Citrus_greening)",
	"Peach__Bacterial_spot",
	"Peach__healthy",
	"Pepper__bell__Bacterial_spot",
	"Pepper__bell__healthy",
	"Potato__Early_blight",
	"Potato__Late_blight",
	"Potato__healthy",
	"Raspberry__healthy",
	"Soybean__healthy",
	"Squash__Powdery_mildew",
	"Strawberry__Leaf_scorch",
	"Strawberry__healthy",
	"Tomato__Bacterial_spot",
	"Tomato__Early_blight",
	"Tomato__Late_blight",
	"Tomato__Leaf_Mold",
	"Tomato__Septoria_leaf_spot",         
	"Tomato__Spider_mites_Two-spotted_spider_mite",
	"Tomato__Target_Spot",
	"Tomato__Tomato_Yellow_Leaf_Curl_Virus",
	"Tomato__Tomato_mosaic_virus",
	"Tomato__healthy",
]

_CLASS_TO_IDX: dict[str, int] = {cls: idx for idx, cls in enumerate(PLANT_VILLAGE_CLASSES)}

_PLANT_DOC_TO_PLANT_VILLAGE: dict[str, str] = {
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
	"Potato leaf": "Potato__healthy",
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
}

_PLANT_VILLAGE_TO_PLANT_DOC = {v: k for k, v in _PLANT_DOC_TO_PLANT_VILLAGE.items()}

def map_plant_village_to_plant_doc(plant_village_tensor: torch.Tensor) -> torch.Tensor:
	assert len(plant_village_tensor.shape) == 1

	plant_doc_classes = list(_PLANT_DOC_TO_PLANT_VILLAGE.keys())

	mapper_tensor = torch.zeros(plant_village_tensor.shape)
	for entry in plant_village_tensor:
		mapped_entry = _PLANT_VILLAGE_TO_PLANT_DOC.get(entry)
		mapper_tensor

	plant_doc_indices = [
		plant_doc_classes.index(_PLANT_VILLAGE_TO_PLANT_DOC.get(PLANT_VILLAGE_CLASSES[idx], 0))
		for idx in plant_village_tensor
	]
	return torch.tensor(plant_doc_indices, dtype=torch.long).reshape(plant_village_tensor.shape)