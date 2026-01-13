import os
from functions.config import MAX_CHARS

def get_file_content(working_directory, file_path):
    working_dir_abs = os.path.abspath(working_directory)
    target_file = os.path.abspath(os.path.join(working_dir_abs, file_path))
    if not os.path.isfile(target_file):
        return f'Error: File not found or is not a regular file: "{file_path}"'    
    # Will be True or False
    valid_target = os.path.commonpath(
        [
            working_dir_abs,
            target_file
        ]
    ) == working_dir_abs

    if not valid_target:
        return f'Error: Cannot list "{file_path}" as it is outside the permitted working directory'
    
    with open(target_file, "r", encoding="utf-8") as f:
        content = f.read(MAX_CHARS)
        # After reading the first MAX_CHARS...
        if f.read(1):
            content = content[:MAX_CHARS] + f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'
        return content
