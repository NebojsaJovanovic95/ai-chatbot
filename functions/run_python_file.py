import os, subprocess
from google.genai import types


schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Runs specified python file with args relative to the working directory",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="file_path path to python file to run, relative to the working directory",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                items=types.Schema(
                    type=types.Type.STRING
                ),
                description="List of arguments to pass to the python file"
            )
        },
        required=["file_path"]
    ),
)

def run_python_file(working_directory, file_path, args=None):
    
    try:
        # f'Error: Cannot write to "{file_path}" as it is a directory'
        working_dir_abs = os.path.abspath(working_directory)
        target_path = os.path.abspath(os.path.join(working_dir_abs, file_path))
        # Will be True or False
        valid_target_dir = os.path.commonpath(
            [
                working_dir_abs,
                target_path
            ]
        ) == working_dir_abs

        if not valid_target_dir:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        if not os.path.isfile(target_path):
            return f'Error: "{file_path}" does not exist or is not a regular file'
        _, extension = os.path.splitext(target_path)
        if extension != ".py":
            return f'Error: "{file_path}" is not a Python file'

        command = ["python", target_path]
        if args:
            command.extend(args)
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            cwd=working_dir_abs,
            timeout=30
        )
        output = f""
        if result.returncode != 0:
            output += f"Process exited with code {result.returncode}"
        if not (result.stdout or result.stderr):
            output += f"No output produced"
        output += f"STDOUT: {result.stdout}\n"
        output += f"STDERR: {result.stderr}"
        return output

    except subprocess.TimeoutExpired as e:
        return f"Timed out! \nSTDOUT so far: {e.stdout}\n STDERR so far: {e.stderr}"
    except Exception as e:
        return f"Error: executing Python file: {e}"
