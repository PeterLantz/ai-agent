import json
from collections.abc import Callable

from functions.get_file_content import get_file_content, schema_get_file_content
from functions.get_files_info import get_files_info, schema_get_files_info
from functions.run_python_file import run_python_file, schema_run_python_file
from functions.write_file import schema_write_file, write_file

available_functions = [
    schema_get_files_info,
    schema_get_file_content,
    schema_run_python_file,
    schema_write_file,
]

function_map: dict[str, Callable[..., str]] = {
    "get_files_info": get_files_info,
    "get_file_content": get_file_content,
    "run_python_file": run_python_file,
    "write_file": write_file,
}


def call_function(tool_call, verbose: bool = False) -> dict:
    function_name = tool_call.function.name
    function_args = json.loads(tool_call.function.arguments or "{}")
    function_args["working_directory"] = "./calculator"

    if verbose:
        print(f" - Calling function: {function_name}({function_args})")
    else:
        print(f" - Calling function: {function_name}")

    # call the function
    result = ""
    if function_map[function_name] is not None:
        result = function_map[function_name](**function_args)
    else:
        result = f"Error: Unknown function: {function_name}"

    # return the results
    message = {
        "role": "tool",  # a special role just for tools in the chat history passed into the ai
        "tool_call_id": tool_call.id,  # how a model matches a result to the request it made
        "content": result,
    }
    return message
