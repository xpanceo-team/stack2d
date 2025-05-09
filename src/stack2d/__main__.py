from argparse import ArgumentParser, RawTextHelpFormatter
from omegaconf import OmegaConf
from . import PACKAGE_ROOT
from .utils.jsonschema import validate
from .utils.config import process_config
from .generator import HeterostructureGenerator

import json


def main():
    parser = ArgumentParser(
        description=__doc__,
        formatter_class=RawTextHelpFormatter,
    )
    parser.add_argument(
        "options",
        type=str,
        help="Options YAML file for running Stack2D",
    )

    parser.add_argument(
        "-o",
        "--output",
        dest="output",
        type=str,
        required=False,
        default="output.xyz",
        help="Path to save the final heterostructure (default: %(default)s).",
    )

    args = parser.parse_args()

    options = OmegaConf.load(args.options)
    with open(PACKAGE_ROOT / "share/schema-base.json", "r") as f:
        schema_base = json.load(f)
    validate(instance=OmegaConf.to_container(options), schema=schema_base)
    config = process_config(options)

    generator = HeterostructureGenerator(
        base_layers=config["base_layers"],
        gap=config["gap"],
        max_misfit=config["max_misfit"],
        max_area=config["max_area"],
        vacuum_size=config["vacuum_size"],
    )
    heterostructure = generator(
        layers=config["heterostructure"],
    )
    heterostructure.write(args.output)


if __name__ == "__main__":
    main()
