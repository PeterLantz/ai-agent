import os

schema_get_files_info = {
    "type": "function",
    "function": {
        "name": "get_files_info",
        "description": "Lists files in a specified directory relative to the working directory, providing file size and directory status",
        "parameters": {
            "type": "object",
            "properties": {
                "directory": {
                    "type": "string",
                    "description": "Directory path to list files from, relative to the working directory (default is the working directory itself)",
                },
            },
        },
    },
}


def get_files_info(working_directory: str, directory: str = ".") -> str:
    try:
        work_dir_abs: str = os.path.abspath(working_directory)
        target_dir: str = os.path.join(work_dir_abs, directory)
        target_dir = os.path.normpath(target_dir)

        if not os.path.isdir(target_dir):
            return f'Error: "{directory}" is not a directory'
        if os.path.commonpath([target_dir, work_dir_abs]) != work_dir_abs:
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

        target_dir_contents = os.listdir(target_dir)

        entries = []
        for name in target_dir_contents:
            path = os.path.join(target_dir, name)
            file_size = os.path.getsize(path)
            is_dir = os.path.isdir(path)
            entries.append(f"- {name}: file_size={file_size} bytes, is_dir={is_dir}")

        return "\n".join(entries)

        # return f'Success: "{directory}" is within the working directory'
    except Exception as e:
        return f"Error: {e}"
