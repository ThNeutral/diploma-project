import argparse
import pathlib
import datetime

from training.matrix import train_variations
from dto.training import ModelName

def main():
    parser = argparse.ArgumentParser(description="Train model")
    parser.add_argument("--out_dir", default="./models", help="Dir to save models into")
    parser.add_argument("--data_dir", default="./data/PlantVillage", help="Directory to load data from")
    parser.add_argument("--val_data_dir", default="./data/PlantDoc", help="Directory to load validation data from")
    args = parser.parse_args()

    time_format = "%Y-%m-%dT%H-%M-%S"
    now = datetime.datetime.now() 

    out_dir = pathlib.Path(args.out_dir)
    out_dir = out_dir / f"{now.strftime(time_format)}"
    out_dir.parent.mkdir(parents=True, exist_ok=True)

    data_dir = pathlib.Path(args.data_dir)
    val_data_dir = pathlib.Path(args.val_data_dir)

    train_variations(
        output_dir=out_dir,
        data_dir=data_dir,
        val_data_dir=val_data_dir,
    )


if __name__ == "__main__":
    main()
