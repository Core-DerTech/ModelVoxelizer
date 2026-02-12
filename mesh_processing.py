# mesh_processing.py
import trimesh
import numpy as np

def load_and_prepare_mesh(path: str) -> trimesh.Trimesh:
    """
    Load an OBJ mesh, clean it, center it, and normalize scale.
    """
    mesh = trimesh.load(path, force='mesh', skip_materials=False)

    if mesh.is_empty:
        raise ValueError("Loaded mesh is empty")

    # Remove degenerate faces (faces with zero area)
    mesh.update_faces(mesh.faces[mesh.area_faces > 1e-12])

    # Remove vertices not used by any faces
    mesh.remove_unreferenced_vertices()

    # Merge duplicate vertices
    mesh.merge_vertices()

    # Center mesh at origin
    mesh.apply_translation(-mesh.centroid)

    # Normalize scale so largest dimension = 1
    scale = 1.0 / max(mesh.extents)
    mesh.apply_scale(scale)

    return mesh
