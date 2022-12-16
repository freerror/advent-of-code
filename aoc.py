from html import unescape
import os
from pathlib import Path
import re
import sys
from typing import Any, Callable
import requests


def get_file_contents(filepath: str | Path):
    """Open the file, read the contents to a string and return"""
    file = Path(filepath)
    with open(file) as f:
        return f.read()


def make_file(filepath: str | Path, content: str):
    """Write file with contents"""
    with open(filepath, "w", newline="\n") as f:
        f.write(content)


# CONSTANTS
YEAR_FILE = Path("year")
if not YEAR_FILE.exists():
    print("Enter year: ", end="")
    YEAR = int(input())
    make_file(YEAR_FILE, str(YEAR))
else:
    YEAR = int(get_file_contents(YEAR_FILE))
SESSION_FILE = Path("session")
if not SESSION_FILE.exists():
    print("Enter session cookie: ", end="")
    SESSION = input()
    make_file(SESSION_FILE, SESSION)
else:
    SESSION = get_file_contents(SESSION_FILE)


def extract_first_example(html: str):
    # Focus on text after "example" case insensitively
    html = re.split("example", html, flags=re.IGNORECASE)[1]
    # Get the first match of the pattern (code block)
    pattern = re.compile(r"(?:code>)((.|\n)*?)(?:<\/code>)")
    match = pattern.search(html)
    if match:
        return unescape(match.groups()[0])
    return ""


def download_input(day: int, year: int):
    """Download input from AOC website"""

    def request_site(url: str):
        res = requests.get(
            url,
            cookies={"session": SESSION},
        )
        if not res.ok:
            if res.status_code == 404:
                raise FileNotFoundError(res.text)
            raise RuntimeError(
                f"Request failed: {res.status_code}, content: {res.content}"
            )
        return res.text

    input_text = request_site(
        f"https://adventofcode.com/{year}/day/{day}/input"
    )[:-1]
    page_text = request_site(f"https://adventofcode.com/{year}/day/{day}")
    return page_text, input_text


def get_inputs(day: int, year: int = YEAR):
    """Get input from file or download from AOC website.
    Returns file contents as a string
    """
    input_dest = Path.joinpath(Path(sys.argv[0]).parent, "input")
    page_dest = Path.joinpath(Path(sys.argv[0]).parent, "page.html")
    example_dest = Path.joinpath(Path(sys.argv[0]).parent, "example")
    page_file = Path(page_dest)
    input_file = Path(input_dest)
    example_file = Path(example_dest)
    if not (
        input_file.exists() and page_file.exists() and example_dest.exists()
    ):
        page_text, input_text = download_input(day, year)
        example_text = extract_first_example(page_text)
        make_file(example_file, example_text)
        make_file(input_file, input_text)
        make_file(page_file, page_text)
    example_text = get_file_contents(example_file)
    input_text = get_file_contents(input_file)
    return {
        "Page Example Input": example_text,
        "Final Puzzle Input": input_text,
    }


def solve_day(
    day: int, solver_fn: Callable[[str], None | tuple[Any, Any]]
) -> None:
    """Runs the puzzle solver for example and main input"""
    for name, input in get_inputs(day=day).items():
        print(name)
        result = solver_fn(input)
        if result:
            print(f"Part 1 Result: \n{result[0]}")
            print(f"Part 2 Result: \n{result[1]}\n")


def main():
    """Create a new individual day folders with a template"""
    with open("template.txt") as f:
        template = f.read()
    for day in range(1, 26):
        day_dir = Path(f"day {day}")
        if day_dir.exists():
            continue
        os.mkdir(day_dir)
        with open(Path.joinpath(day_dir, "code.py"), "w", newline="\n") as f:
            f.write(
                template.replace("DAY", str(day)).replace("YEAR", str(YEAR))
            )
        # Stop after the first folder.
        break


if __name__ == "__main__":
    main()
