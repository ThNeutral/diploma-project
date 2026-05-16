import argparse
import pathlib

from training.matrix import train_variations
from dto.training import ModelName

def main():
    parser = argparse.ArgumentParser(description="Train model")
    parser.add_argument("--out_dir", default="./models", help="Dir to save models into")
    parser.add_argument("--data_dir", default="./data/PlantVillage", help="Directory to load data from")
    parser.add_argument("--val_data_dir", default="./data/PlantDoc/train", help="Directory to load validation data from")
    parser.add_argument("--epochs", default="10", help="Directory to load data from")
    parser.add_argument("--batch_size", default="32", help="Directory to load data from")
    args = parser.parse_args()

    epochs = int(args.epochs)
    batch_size = int(args.batch_size)

    out_dir = pathlib.Path(args.out_dir)
    out_dir.parent.mkdir(parents=True, exist_ok=True)

    data_dir = pathlib.Path(args.data_dir)
    val_data_dir = pathlib.Path(args.val_data_dir)

    train_variations(
        output_dir=out_dir,
        data_dir=data_dir,
        val_data_dir=val_data_dir,
        epochs=epochs,
        batch_size=batch_size
    )


if __name__ == "__main__":
    main()
