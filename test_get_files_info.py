from threading import currentThread

from functions.get_files_info import get_files_info


def run_test(working_dir, dir) -> None:
    dir_text: str
    if dir == ".":
        dir_text = "current"
    else:
        dir_text = f"'{dir}'"
    print(f"Result for {dir_text} directory:")
    print(get_files_info(working_dir, dir))


run_test("calculator", ".")
run_test("calculator", "pkg")
run_test("calculator", "/bin")
run_test("calculator", "../")
