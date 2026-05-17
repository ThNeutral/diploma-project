import json
from pathlib import Path

from .config import JSONConfig

def load_config_from_json_file(file_path: Path) -> JSONConfig:
	with open(file_path, 'r') as file:
		content = file.read()
	
	json_content = json.loads(content)

	json_config = JSONConfig(**json_content)

	return json_config	  