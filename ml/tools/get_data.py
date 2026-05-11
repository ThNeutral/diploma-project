import argparse
import logging
import os
import shutil
import pathlib
import subprocess
import tempfile
from sklearn.model_selection import train_test_split

logger = logging.getLogger(__name__)


def download_github_subfolder(repo_url: str, subfolder: str, out_dir: pathlib.Path) -> None:
    """Sparse-clone a subfolder from a GitHub repo into out_dir."""
    out_dir.mkdir(parents=True, exist_ok=True)

    with tempfile.TemporaryDirectory(prefix="git_sparse_") as tmp:
        tmp_path = pathlib.Path(tmp)
        cmds = [
            ["git", "clone", "--no-checkout", "--depth=1", "--filter=blob:none", repo_url, str(tmp_path)],
            ["git", "-C", str(tmp_path), "sparse-checkout", "init", "--cone"],
            ["git", "-C", str(tmp_path), "sparse-checkout", "set", subfolder],
            ["git", "-C", str(tmp_path), "checkout"],
        ]
        for cmd in cmds:
            result = subprocess.run(cmd, capture_output=True, text=True)
            if result.returncode != 0:
                raise RuntimeError(
                    f"Command failed: {' '.join(cmd)}\n"
                    f"  stdout: {result.stdout.strip()}\n"
                    f"  stderr: {result.stderr.strip()}"
                )
            logger.debug("OK: %s\n  %s", " ".join(cmd), result.stdout.strip())

        src = tmp_path / subfolder
        if not src.exists():
            raise FileNotFoundError(f"Expected subfolder not found after checkout: {src}")

        dest = out_dir / pathlib.Path(subfolder).name
        if dest.exists():
            shutil.rmtree(dest)
        shutil.copytree(src, dest)


def split_data(
    src: pathlib.Path,
    subfolder_name: str,
    test_size: float,
    seed: int,
) -> None:
    """Split a flat class-directory dataset into train/ and test/."""
    color_path = src / subfolder_name
    train_path = src / "train"
    test_path = src / "test"

    if not color_path.is_dir():
        raise FileNotFoundError(f"Source class directory not found: {color_path}")

    train_path.mkdir(exist_ok=True)
    test_path.mkdir(exist_ok=True)

    for class_dir in sorted(color_path.iterdir()):
        if not class_dir.is_dir():
            continue

        images = list(class_dir.glob("*"))
        if not images:
            logger.warning("No images found in %s, skipping", class_dir)
            continue

        logger.info("%d images in class '%s'", len(images), class_dir.name)
        images_train, images_test = train_test_split(
            images, test_size=test_size, random_state=seed
        )

        (train_path / class_dir.name).mkdir(exist_ok=True)
        (test_path / class_dir.name).mkdir(exist_ok=True)

        for image in images_train:
            shutil.move(str(image), train_path / class_dir.name / image.name)
        for image in images_test:
            shutil.move(str(image), test_path / class_dir.name / image.name)


def main() -> None:
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s [%(levelname)s] %(name)s — %(message)s",
    )

    parser = argparse.ArgumentParser(description="Download and split PlantVillage dataset")
    parser.add_argument("out_dir", help="Directory to download data into")
    parser.add_argument("--test-size", type=float, default=0.2, help="Fraction for test split (default: 0.2)")
    parser.add_argument("--seed", type=int, default=1337, help="Random seed (default: 1337)")
    args = parser.parse_args()

    out_dir = pathlib.Path(args.out_dir)
    subfolder = "raw/color"

    logger.info("Downloading '%s' from GitHub", subfolder)
    download_github_subfolder(
        "https://github.com/spMohanty/PlantVillage-Dataset.git",
        subfolder,
        out_dir,
    )

    logger.info("Splitting data %.0f/%.0f (seed=%d)", (1 - args.test_size) * 100, args.test_size * 100, args.seed)
    split_data(
        src=out_dir,
        subfolder_name=pathlib.Path(subfolder).name,  # "color"
        test_size=args.test_size,
        seed=args.seed,
    )

    logger.info("Done preparing data in %s", out_dir)


if __name__ == "__main__":
    main()