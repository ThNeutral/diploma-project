import argparse
from pathlib import Path

from training.matrix import train_variations_from_config

from datasets.human_readable_classes import PLANT_VILLAGE_HUMAN_READABLE_LABELS

from config import load_config_from_json_file

def main():
    print(PLANT_VILLAGE_HUMAN_READABLE_LABELS)
    return

    parser = argparse.ArgumentParser(description="Train model")
    parser.add_argument("--config_file", default="./config.json", help="Config file location")
    args = parser.parse_args()

    config_file = Path(args.config_file) 

    config = load_config_from_json_file(config_file)

    train_variations_from_config(
        config=config,
    )

if __name__ == "__main__":
    main()
