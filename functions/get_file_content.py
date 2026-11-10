import os

from config import *

schema_get_file_content = {
    "type": "function",
    "function": {
        "name": "get_file_content",
        "description": "Returns the contents of a file",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "path to the file, relative to the working directory",
                },
            },
            "required": ["file_path"],
        },
    },
}


def get_file_content(working_directory: str, file_path: str) -> str:
    try:
        # get path to file
        work_dir_abs: str = os.path.abspath(working_directory)
        target_dir: str = os.path.join(work_dir_abs, file_path)
        target_dir = os.path.normpath(target_dir)

        # Error checking
        if not os.path.isfile(target_dir):
            return f'Error: File not found or is not a regular file: "{file_path}"'
        if os.path.commonpath([target_dir, work_dir_abs]) != work_dir_abs:
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'

        # read the file
        content = ""
        with open(target_dir, "r") as stream:
            content = stream.read(MAX_CHARS)
            if stream.read(1):
                content += (
                    f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'
                )
        return content
    except Exception as e:
        return f"Error: {e}"
