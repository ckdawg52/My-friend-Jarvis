import os
from google.genai import types

def get_file_content(working_directory, file_path):
    try:
        working_directory_abs = os.path.abspath(working_directory)
        file_path_abs = os.path.normpath(os.path.join(working_directory_abs, file_path))
        if working_directory_abs != os.path.commonpath([working_directory_abs, file_path_abs]):
            raise Exception(f'Cannot read "{file_path}" as it is outside the permitted working directory')
        if os.path.isfile(file_path_abs) == False:
            raise Exception(f'File not found or is not a regular file: "{file_path}"')
        MAX_CHARS = 10000
        with open(file_path_abs) as f:
            file_content_string = f.read(MAX_CHARS)
            if f.read(1):
                file_content_string += f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'
            return file_content_string
    except Exception as e:
        return(f"Error: {e}")


schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Reads the contents of a chosen file",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="File path to get contents from, relative to the working directory",
            ),
        },
    ),
)