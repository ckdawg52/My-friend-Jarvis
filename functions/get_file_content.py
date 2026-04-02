import os
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