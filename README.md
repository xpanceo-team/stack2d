
# Stack2D

**Stack2D** is a minimalistic Python package for constructing heterostructures from 2D materials. It provides a simple interface for stacking atomic structures, adjusting interlayer distances, and managing layer alignments using ASE (Atomic Simulation Environment).

## Features

- Stack multiple 2D materials with precise control over interlayer distances
- Simple interface built on top of ASE for compatibility with existing workflows
- Lightweight and easy to integrate

## Installation

To install the package, use pip:

```bash
pip install git+https://github.com/xpanceo-team/stack2d.git
```

## Usage

Stack2D is designed to be used from the command line. The basic usage is as follows:

```bash
stack2d options.yaml -o heterostructure.xyz
```

The `options.yaml` file should contain the configuration for the heterostructure you
want to create. The output will be saved in the specified file format (e.g., `.xyz`).

Base building 2D blocks are defined in the `base_layers` section, where for each 2D
layer is defined by its name and path to the file containing the atomic structure.
The `heterostructure` section specifies the stacking order and number of layers for
each base layer. The `gap` parameter defines the interlayer distance, and the
`max_misfit` and `max_area` parameters control the maximum allowed lattice mismatch
and are of the heterostructure, respectively. The `vacuum_size` parameter defines the
size of the vacuum region in the z-direction.


### Example YAML Configuration

```yaml
base_layers:
  - name: graphene
    path: path/to/graphene.xyz
  - name: MoS2
    path: path/to/MoS2.xyz
  - name: hBN
    path: path/to/hBN.xyz
heterostructure:
  - graphene: 2
  - hBN: 1
  - MoS2: 1
  - graphene: 2
gap: 3.0
max_misfit: 5e-3
max_area: 400
vacuum_size: 10.0
```

## Documentation

Documantation is not available yet. For now, please refer to the code and examples in the repository.

## Examples

Example of a basic usage is provided in the `examples` directory.