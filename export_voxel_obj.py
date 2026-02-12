import numpy as np

def export_voxel_obj(voxels: np.ndarray, voxel_size: float = 1.0,
                     output_path: str = "voxel_model.obj",
                     voxel_colors: np.ndarray = None):
    """
    Export a voxel grid as OBJ.

    Parameters
    ----------
    voxels : np.ndarray
        3D boolean array representing surface voxels (True = voxel exists).
    voxel_size : float
        Size of each voxel cube.
    output_path : str
        File path to save the OBJ.
    voxel_colors : np.ndarray, optional
        Nx3 RGB values for each voxel; if None, colors are skipped.
    """
    voxel_coords = np.argwhere(voxels)
    vertex_lines = []
    face_lines = []
    vertex_index = 1

    cube_offsets = np.array([
        [0,0,0],
        [1,0,0],
        [1,1,0],
        [0,1,0],
        [0,0,1],
        [1,0,1],
        [1,1,1],
        [0,1,1]
    ], dtype=float) * voxel_size

    cube_faces = [
        [0,1,2,3],
        [4,5,6,7],
        [0,1,5,4],
        [2,3,7,6],
        [0,3,7,4],
        [1,2,6,5]
    ]

    for i, c in enumerate(voxel_coords):
        verts = cube_offsets + c.astype(float) * voxel_size
        color = None
        if voxel_colors is not None:
            color = voxel_colors[i]

        for v in verts:
            if color is not None:
                # OBJ vertex with RGB (normalized 0-1)
                vertex_lines.append(f"v {v[0]} {v[1]} {v[2]} {color[0]/255:.3f} {color[1]/255:.3f} {color[2]/255:.3f}\n")
            else:
                vertex_lines.append(f"v {v[0]} {v[1]} {v[2]}\n")

        for f in cube_faces:
            face_lines.append(f"f {f[0]+vertex_index} {f[1]+vertex_index} "
                              f"{f[2]+vertex_index} {f[3]+vertex_index}\n")

        vertex_index += 8

    with open(output_path, "w") as f:
        f.writelines(vertex_lines)
        f.writelines(face_lines)

    print(f"Voxel OBJ exported: {output_path}, voxels: {len(voxel_coords)}, colored: {voxel_colors is not None}")
