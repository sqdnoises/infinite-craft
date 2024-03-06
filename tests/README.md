# Testing `infinite-craft`
This folder includes all the tests of [`infinitecraft`](/infinitecraft/) library.

To install the local version of the library, use `pip install -e .` at the directory where the [`pyproject.toml`](/pyproject.toml) is located.

To test, make sure the requirements from [`requirements.txt`](/requirements.txt) are installed and make sure `pytest` is on PATH. Then use `pytest` for the standard output, `pytest -q` for a smaller output or `pytest -v` for a verbose output of the tests. You can use the `-s` switch to view the stdout outputs.