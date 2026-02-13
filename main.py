from mesh_processing import load_and_prepare_mesh
from voxelization import voxelize_surface, solid_fill, remove_inner_voxels
from export_voxel_obj import export_voxel_obj
from voxel_texture import sample_voxel_colors

input_path = r"C:\Users\user\Downloads\Test\blade.obj"

mesh = load_and_prepare_mesh(input_path)

surface = voxelize_surface(mesh, pitch=0.05)
solid = solid_fill(surface)

solid_surface = remove_inner_voxels(solid)
print("Surface voxels only:", solid_surface.sum())

# Optional: sample voxel colors (skip if mesh has no texture)
colors = sample_voxel_colors(mesh, solid_surface, voxel_size=0.05)

# Export voxel OBJ (with colors if available)
export_voxel_obj(solid_surface, voxel_size=0.05, output_path="Monkey_voxel.obj",
                 voxel_colors=colors)
