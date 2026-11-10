import os

schema_write_file = {
    "type": "function",
    "function": {
        "name": "write_file",
        "description": "Writes to the contents of a file, creating the file and directory if it doesn't exist yet. Please note this will replace the contents of the file, not append to it.",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "path to the file, relative to the working directory",
                },
                "content": {
                    "type": "string",
                    "description": "the text to write the contents of the file with (default is an empty string)",
                },
            },
            "required": ["file_path"],
        },
    },
}


def write_file(working_directory: str, file_path: str, content: str = "") -> str:
    try:
        work_dir_abs = os.path.abspath(working_directory)
        target_file = os.path.join(work_dir_abs, file_path)
        target_file = os.path.normpath(target_file)

        if os.path.commonpath([work_dir_abs, target_file]) != work_dir_abs:
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'

        if os.path.isdir(target_file):
            return f'Error: Cannot write to "{file_path}" as it is a directory'

        # creates missing directories. the exist_ok flag ensures it runs even if the path already exists
        os.makedirs(os.path.dirname(target_file), exist_ok=True)

        with open(target_file, mode="w") as file:
            file.write(content)

        return (
            f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
        )

    except Exception as e:
        return f"Error: {e}"
