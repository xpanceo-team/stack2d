from typing import Any, Dict, Union
from omegaconf import DictConfig
import ase


def process_config(conf: Union[DictConfig, Dict]) -> Dict[str, Any]:
    """
    Process the configuration dictionary to ensure all required keys are present and have valid values.
    """
    config: Dict[str, Any] = {}
    for key, value in conf.items():
        if key == "base_layers":
            config[key] = {layer["name"]: ase.io.read(layer["path"]) for layer in value}
        elif key == "heterostructure":
            heterostructure = []
            for layer in value:
                name = list(layer.keys())[0]
                num_layers = layer[name]
                heterostructure.append((name, num_layers))
            config[key] = heterostructure
        else:
            config[key] = value
    return config
