import json
from pathlib import Path

import torch
from torch import nn

from dto.training import ModelMetadata

def save_model(
	*,
	model_metadata: ModelMetadata,
	model: nn.Module,
	output_folder: Path,
	model_name: str,
	device: torch.device
):
	model_output_file = output_folder / f"{model_name}.onnx"
	metadata_output_file = output_folder / f"{model_name}_metadata.json"

	dummy_input = torch.randn(model_metadata.input_size).to(device)

	onnx_program = torch.onnx.export(model, (dummy_input, ), dynamo=True)
	assert onnx_program

	onnx_program.save(model_output_file)

	with open(metadata_output_file, "w") as f:
		json.dump(model_metadata.to_dict(), f)