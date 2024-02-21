import os


def create_dir_structure(file_path, root_dir, output_dir):
    relative_path = os.path.relpath(file_path, root_dir)
    new_dir = os.path.join(output_dir, os.path.dirname(relative_path))
    os.makedirs(new_dir, exist_ok=True)
    return new_dir
