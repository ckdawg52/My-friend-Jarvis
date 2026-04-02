import os
import subprocess
from google.genai import types

def run_python_file(working_directory, file_path, args=None):
    try:
        working_directory_abs = os.path.abspath(working_directory)
        file_path_abs = os.path.normpath(os.path.join(working_directory_abs, file_path))
        if working_directory_abs != os.path.commonpath([working_directory_abs, file_path_abs]):
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        if not os.path.isfile(file_path_abs):
            return f'Error: "{file_path}" does not exist or is not a regular file'
        if not file_path.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file'
        command = ["python", file_path_abs]
        if args is not None:
            command.extend(args)
        run_file = subprocess.run(command, cwd=working_directory_abs, capture_output=True, text=True, timeout=30)
        parts = []
        if run_file.returncode != 0:
            returncode = f"Process exited with code {run_file.returncode}"
            parts.append(returncode)
        if run_file.stdout != "":
            parts.append(f"STDOUT: {run_file.stdout}")
        if run_file.stderr != "":
            parts.append(f"STDERR: {run_file.stderr}")
        if run_file.stdout == "" and run_file.stderr == "":
            parts.append("No output produced")
        return "\n".join(parts)
    except Exception as e:
        return f"Error: executing Python file: {e}"


schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Executes the chosen python file",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="File path to python file, relative to the working directory",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                items=types.Schema(type=types.Type.STRING),
                description="Optional list of arguments to pass to the python file",
            ),
        },
    ),
)