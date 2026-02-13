# mesh_processing.py
import trimesh
import numpy as np

def load_and_prepare_mesh(path: str) -> trimesh.Trimesh:
    """
    Завантажує OBJ-модель, очищає та нормалізує її для вокселізації.
    Підтримує сучасний trimesh 4.x (без remove_degenerate_faces)
    """
    # 1️⃣ Завантажуємо mesh
    mesh = trimesh.load(path, force='mesh', skip_materials=False)

    if mesh.is_empty:
        raise ValueError("Loaded mesh is empty")

    # 2️⃣ Очистка: видаляємо нульові грані
    face_areas = mesh.area_faces
    valid_faces = face_areas > 1e-12  # поріг для нульових граней
    mesh.update_faces(valid_faces)

    # 3️⃣ Видаляємо непотрібні вершини
    mesh.remove_unreferenced_vertices()

    # 4️⃣ Merge вершин без помилок
    try:
        mesh.merge_vertices()
    except Exception as e:
        print(f"[Warning] merge_vertices failed: {e}")

    # 5️⃣ Виправлення орієнтації та manifold
    try:
        trimesh.repair.fix_inversion(mesh)
        trimesh.repair.fix_winding(mesh)
        trimesh.repair.fill_holes(mesh)
    except Exception:
        pass

    # 6️⃣ Центрування та нормалізація
    mesh.apply_translation(-mesh.centroid)
    scale = 1.0 / max(mesh.extents)
    mesh.apply_scale(scale)

    return mesh
