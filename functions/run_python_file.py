import os
import subprocess

schema_run_python_file = {
    "type": "function",
    "function": {
        "name": "run_python_file",
        "description": "Runs, or in other words, executes a python file",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "path to the python file to be run, relative to the working directory",
                },
                "args": {
                    "type": "array",
                    "items": {
                        "type": "string",
                    },
                    "description": "arguments to pass into the python file",
                },
            },
            "required": ["file_path"],
        },
    },
}


def run_python_file(
    working_directory: str, file_path: str, args: list[str] | None = None
) -> str:
    try:
        work_dir_abs = os.path.abspath(working_directory)
        target_file = os.path.join(work_dir_abs, file_path)
        target_file = os.path.normpath(target_file)

        if not os.path.isfile(target_file):
            return f'Error: "{file_path}" does not exist or is not a regular file'

        if os.path.commonpath([work_dir_abs, target_file]) != work_dir_abs:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

        if not file_path.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file'

        # run the file
        command = ["python", target_file]
        if args is None:
            args = []
        command.extend(args)
        completed_process = subprocess.run(
            command, check=False, timeout=30, text=True, capture_output=True
        )
        output = completed_process.stdout
        error = completed_process.stderr
        return_code = completed_process.returncode

        # build a string from the file
        result = ""
        if return_code != 0:
            result += f"Process exited with code {return_code} \n"
        if output is None and error is None:
            result += "No output produced \n"
        else:
            result += f"STDOUT: {output} \n"
            result += f"STDERR: {error}"
        return result

    except Exception as e:
        return f"Error: executing Python file: {e}"
