from typing import Dict, List, Tuple
from pymatgen.analysis.interfaces.zsl import ZSLGenerator
import numpy as np
from pymatgen.analysis.interfaces.coherent_interfaces import (
    get_2d_transform,
    Deformation,
)
import ase
from pymatgen.io.ase import AseAtomsAdaptor
from ase import Atoms


class HeterostructureGenerator:
    def __init__(
        self,
        base_layers: Dict[str, ase.Atoms],
        gap: float = 3.0,
        max_misfit: float = 5e-3,
        max_area: float = 400.0,
        vacuum_size: float = 10.0,
    ):
        self.base_layers = base_layers
        self.gap = gap
        self.max_misfit = max_misfit
        self.max_area = max_area
        self.vacuum_size = vacuum_size

    def __call__(self, *args, **kwargs) -> ase.Atoms:
        return self.generate(*args, **kwargs)

    def generate(self, layers: List[Tuple[str, int]]) -> ase.Atoms:
        """
        Generate a heterostructure by stacking multiple 2D materials.
        """
        current_structure = None
        i = 0
        while i < len(layers):
            layer_name, num_layers = layers[i]
            if layer_name not in self.base_layers:
                raise ValueError(f"Layer {layer_name} not found in base layers.")
            if num_layers <= 0:
                raise ValueError(
                    f"Number of layers must be positive, got {num_layers}."
                )

            base_layer = self.base_layers[layer_name].copy()

            # Build up multiple layers of the same material if num_layers > 1
            for _ in range(num_layers):
                if current_structure is None:
                    current_structure = base_layer.copy()
                else:
                    current_structure = self.generate_single_unit(
                        substrate=current_structure, film=base_layer.copy()
                    )
            i += 1

        return current_structure

    def generate_single_unit(
        self,
        substrate: ase.Atoms,
        film: ase.Atoms,
    ) -> ase.Atoms:
        """
        Generate a heterostructure by stacking two 2D materials.
        """
        substrate_structure = AseAtomsAdaptor.get_structure(substrate)
        film_structure = AseAtomsAdaptor.get_structure(film)
        film_vectors = film_structure.lattice.matrix[:2]
        substrate_vectors = substrate_structure.lattice.matrix[:2]
        film_supercell_matrix, substrate_supercell_matrix = get_supercell_matrices(
            film_vectors, substrate_vectors, self.max_misfit, self.max_area
        )
        film_supercell = film_structure.make_supercell(
            film_supercell_matrix, in_place=False
        )
        substrate_supercell = substrate_structure.make_supercell(
            substrate_supercell_matrix, in_place=False
        )

        film_supercell_atoms = AseAtomsAdaptor.get_atoms(film_supercell)
        substrate_supercell_atoms = AseAtomsAdaptor.get_atoms(substrate_supercell)
        film_supercell_atoms.rotate(film_supercell_atoms.cell[0], "x", rotate_cell=True)
        substrate_supercell_atoms.rotate(
            substrate_supercell_atoms.cell[0], "x", rotate_cell=True
        )

        heterostructure = join_heterostructure(
            film_supercell_atoms,
            substrate_supercell_atoms,
            gap=self.gap,
            vacuum_size=self.vacuum_size,
        )
        return heterostructure


def get_supercell_matrices(film_vectors, substrate_vectors, max_mixfit, max_area):
    """
    Get the supercell matrices for the film and substrate.
    """
    generator = ZSLGenerator(max_area=max_area)
    matches = generator(film_vectors, substrate_vectors)
    for match in matches:
        strain = Deformation(match.match_transformation).green_lagrange_strain
        if np.max(strain) < max_mixfit:
            M1 = np.round(get_2d_transform(film_vectors, match.film_sl_vectors)).astype(
                int
            )
            M2 = np.round(
                get_2d_transform(substrate_vectors, match.substrate_sl_vectors)
            ).astype(int)
            if np.linalg.det(M1) * np.linalg.det(M2) > 0:
                break
    film_supercell_matrix = np.eye(3)
    film_supercell_matrix[:2, :2] = M1
    substrate_supercell_matrix = np.eye(3)
    substrate_supercell_matrix[:2, :2] = M2
    return film_supercell_matrix, substrate_supercell_matrix


def join_heterostructure(film, substrate, gap, vacuum_size=10.0):
    """
    Join two structures with a gap between them.
    """
    film = film.copy()
    substrate = substrate.copy()
    cell = substrate.cell
    film_positions = film.get_positions()
    substrate_positions = substrate.get_positions()
    substrate_positions[:, 2] -= substrate_positions[:, 2].min()
    film_positions[:, 2] -= film_positions[:, 2].min()
    film_positions[:, 2] += substrate_positions[:, 2].max() + gap
    symbols = substrate.get_chemical_symbols() + film.get_chemical_symbols()
    positions = np.vstack((substrate_positions, film_positions))
    heterostructure = Atoms(
        symbols=symbols,
        positions=positions,
        cell=cell,
        pbc=[True, True, False],
    )
    heterostructure.wrap(pbc=[True, True, False])
    heterostructure.center(vacuum=vacuum_size, axis=2)
    return heterostructure
