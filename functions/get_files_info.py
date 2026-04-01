import os

def get_files_info(working_directory, directory="."):
    try:    
        working_directory_abs = os.path.abspath(working_directory)
        target_dir = os.path.normpath(os.path.join(working_directory_abs, directory))
        if working_directory_abs != os.path.commonpath([target_dir, working_directory_abs]):
            raise Exception(f'Cannot list "{directory}" as it is outside the permitted working directory')
        if os.path.isdir(target_dir) == False:
            raise Exception(f'"{directory}" is not a directory')
        all_item_info = []
        for item in os.listdir(target_dir):
            item_path = os.path.abspath(f"{target_dir}/{item}")
            item_name = f"- {item}:"
            item_size = f"size={os.path.getsize(item_path)} bytes,"
            if os.path.isfile(item_path):
                is_dir = "is_dir=False"
            if os.path.isdir(item_path):
                is_dir = "is_dir=True"
            item_info = " ".join([item_name, item_size, is_dir])
            all_item_info.append(item_info)
        return f"Results for current directory:\n{"\n".join(all_item_info)}"
    except Exception as e:
        return(f"Error: {e}")
