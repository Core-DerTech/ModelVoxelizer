import numpy as np
import trimesh

def sample_voxel_colors(mesh: trimesh.Trimesh, voxels: np.ndarray, voxel_size: float):
    """
    Sample colors from the original mesh for each voxel.

    Returns:
        voxel_coords: Nx3 int positions of voxels
        colors: Nx3 uint8 RGB colors
    """
    voxel_coords = np.argwhere(voxels)
    colors = []

    # Check if mesh has vertex colors
    if hasattr(mesh.visual, "vertex_colors") and len(mesh.visual.vertex_colors) > 0:
        for c in voxel_coords:
            # Voxel center
            point = (c + 0.5) * voxel_size
            nearest, _, _ = mesh.nearest.on_surface([point])
            color = mesh.visual.vertex_colors[nearest[0]][:3]
            colors.append(color)
        colors = np.array(colors, dtype=np.uint8)
    else:
        # No colors → return None to indicate skipping
        colors = None

    return colors
