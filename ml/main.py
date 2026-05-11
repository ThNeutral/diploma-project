import argparse
import pathlib

from training.loop import train_model
from dto.training import ModelName

def main():
    parser = argparse.ArgumentParser(description="Train model")
    parser.add_argument("--out_file", default="./1.onnx", help="File to save model into")
    parser.add_argument("--train_data_dir", default="./data/PlantVillage", help="Directory to load data from")
    parser.add_argument("--val_data_dir", default="./data/PlantDoc/train", help="Directory to load data from")
    parser.add_argument("--epochs", default=10, help="Directory to load data from")
    parser.add_argument("--batch_size", default=32, help="Directory to load data from")
    args = parser.parse_args()

    out_file = pathlib.Path(args.out_file)
    out_file.parent.mkdir(parents=True, exist_ok=True)

    train_data_dir = pathlib.Path(args.train_data_dir)
    val_data_dir = pathlib.Path(args.val_data_dir)

    train_model(
        base_model_name=ModelName.EfficientNetV2_S,
        model_output_file=out_file,
        train_data_dir=train_data_dir,
        val_data_dir=val_data_dir,
        epochs=args.epochs,
        batch_size=args.batch_size
    )


if __name__ == "__main__":
    main()
