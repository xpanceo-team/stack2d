from omegaconf import OmegaConf
from . import OPTIONS_PATH, RESOURCES_PATH
from stack2d.utils.config import process_config
from stack2d import HeterostructureGenerator
import os


def test_generator():
    os.chdir(RESOURCES_PATH)
    config = process_config(OmegaConf.load(OPTIONS_PATH))
    generator = HeterostructureGenerator(
        base_layers=config["base_layers"],
        gap=config["gap"],
        max_misfit=config["max_misfit"],
        max_area=config["max_area"],
        vacuum_size=config["vacuum_size"],
    )
    generator(layers=config["heterostructure"])
