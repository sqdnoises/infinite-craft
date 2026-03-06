# 🔨 Testing infinite-craft

This folder includes the complete test suite for the [`infinitecraft`](../infinitecraft/) library. 

These tests spin up a local mock FastAPI server in the background, test the library and at the end connectivity to the Infinite Craft API is tested aswell.

## ⚙️ Setup Instructions

To install the local version of the library with all dev dependencies, run this in the directory where your [`pyproject.toml`](../pyproject.toml) is located:
```bash
pip install -e .[dev]
```


## 🚀 Running the Tests

Make sure `pytest` is on PATH. You can run the test suite from the root of the project using the following commands, depending on what kind of output you need:

* **The standard run:**
```bash
pytest
```

* **The silent run:**\
Produces minimal output, and at the end shows all warnings, pass & fail status and time taken.
```bash
pytest -q
```

* **The human-readable run (for local dev):**
```bash
pytest -v
```

* **The CI/CD run (e.g. GitHub Actions):**
```bash
pytest -v --log-cli-level=ERROR
```

* **Debugging:**
Add the `-s` flag to any of the commands above to prevent pytest from capturing stdout, to see everything being printed.