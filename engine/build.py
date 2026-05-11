#!/usr/bin/env python3
import argparse
import subprocess
import shutil
import pathlib
import logging
import sys

logger = logging.getLogger(__name__)

DEST_DIR = pathlib.Path("../webapi/PlantDiseaseRecognition.WebApi.Engine.Rust")
DLL_NAME = "engine.dll"

def build_cargo(profile: str) -> pathlib.Path:
    cargo_args = ["cargo", "build"]

    if profile == "prod":
        cargo_args.append("--release")
        output_dir = pathlib.Path("target/release")
    else:
        output_dir = pathlib.Path("target/debug")

    logger.info("Building cargo lib (profile: %s)...", profile)
    result = subprocess.run(cargo_args, capture_output=True, text=True)

    if result.returncode != 0:
        logger.error("cargo build failed:\n%s", result.stderr)
        sys.exit(1)

    logger.debug("cargo build stdout:\n%s", result.stdout)
    logger.debug("cargo build stderr:\n%s", result.stderr)

    dll_path = output_dir / DLL_NAME
    if not dll_path.exists():
        logger.error("Expected DLL not found at %s", dll_path)
        sys.exit(1)

    return dll_path


def copy_dll(dll_path: pathlib.Path, dest_dir: pathlib.Path, profile: str) -> pathlib.Path:
    dest_dir.mkdir(parents=True, exist_ok=True)
    dest_name = dll_path.name
    dest = dest_dir / dest_name
    shutil.copy2(dll_path, dest)
    logger.info("Copied %s -> %s", dll_path, dest)
    return dest


def main() -> None:
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s [%(levelname)s] %(message)s",
    )

    parser = argparse.ArgumentParser(description="Build Rust engine DLL and deploy it")
    parser.add_argument(
        "env",
        nargs="?",
        default="dev",
        choices=["dev", "prod"],
        help="Build environment: dev (default) or prod",
    )
    args = parser.parse_args()

    dll_path = build_cargo(args.env)
    dest = copy_dll(dll_path, DEST_DIR, args.env)

    logger.info("Done. DLL deployed to %s", dest)


if __name__ == "__main__":
    main()