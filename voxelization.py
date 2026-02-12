# voxelization.py
import numpy as np
from scipy.ndimage import binary_fill_holes, binary_erosion
import trimesh

def voxelize_surface(mesh: trimesh.Trimesh, pitch: float) -> np.ndarray:
    """
    Convert mesh surface to voxel grid (bool numpy array).
    pitch: size of each voxel
    """
    vox = mesh.voxelized(pitch)
    return vox.matrix.astype(bool)


def solid_fill(voxels: np.ndarray) -> np.ndarray:
    """
    Fill interior of voxel grid to make it solid.
    """
    filled = binary_fill_holes(voxels)
    return filled


def remove_inner_voxels(voxels: np.ndarray) -> np.ndarray:
    """
    Remove interior voxels, keeping only surface voxels.
    """
    eroded = binary_erosion(voxels)
    surface = voxels ^ eroded  # XOR → only surface layer remains
    return surface
