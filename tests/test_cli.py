from pathlib import Path
import subprocess
import pytest
from . import OPTIONS_PATH, RESOURCES_PATH
import os
import shutil


@pytest.mark.parametrize("output", [None, "output.xyz"])
def test_cli(monkeypatch, tmp_path, output):
    monkeypatch.chdir(tmp_path)
    command = ["stack2d", "options.yaml"]
    if output is not None:
        command += ["-o", output]
    else:
        output = "output.xyz"
    shutil.copy(OPTIONS_PATH, "options.yaml")
    for item in os.listdir(RESOURCES_PATH):
        if Path(item).suffix == ".xyz":
            shutil.copy(RESOURCES_PATH / item, item)
    subprocess.check_call(command)
    assert Path(output).is_file()
