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
    parser.add_argument("--epochs", default="10", help="Epochs to train model for")
    parser.add_argument("--batch_size", default="32", help="Batch size for DataLoader")
    parser.add_argument("--num_workers", default="4", help="Number of workers for DataLoader")
    args = parser.parse_args()

    epochs = int(args.epochs)
    batch_size = int(args.batch_size)
    num_workers = int(args.num_workers)

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
        epochs=epochs,
        batch_size=batch_size,
        num_workers=num_workers
    )


if __name__ == "__main__":
    main()
