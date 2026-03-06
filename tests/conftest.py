import pytest
import asyncio
import uvicorn
from typing import Any, Generator
from fastapi import FastAPI
from uvicorn import Config
from threading import Thread

# Define the host and port for our mock testing server
HOST = "127.0.0.1"
PORT = 15575


class ThreadedUvicorn:
    """
    A helper class to run a Uvicorn server in a background thread.
    This is necessary because if we ran it in the main thread, it would block
    the execution of our pytest suite.
    """

    def __init__(self, *args: Any, config: Config | None = None, **kwargs: Any) -> None:
        # Initialize the Uvicorn server with the provided configuration
        if config is None:
            self.server = uvicorn.Server(Config(*args, **kwargs))
        else:
            self.server = uvicorn.Server(config)

        # Set up a daemon thread so it automatically dies if the main program crashes
        self.thread = Thread(daemon=True, target=self.server.run)

    def start(self) -> None:
        # Start the background thread running the server
        self.thread.start()
        # Block the main thread just long enough to ensure the server is actually ready to accept requests
        asyncio.run(self.wait_for_started())

    async def wait_for_started(self) -> None:
        # Poll the server's internal state every 0.1 seconds until it's fully booted
        while not self.server.started:
            await asyncio.sleep(0.1)

    def stop(self) -> None:
        # Gracefully shut down the server if it's currently running
        if self.thread.is_alive():
            self.server.should_exit = True
            # Wait for the background thread to finish its shutdown process
            while self.thread.is_alive():
                continue


@pytest.fixture(scope="session")
def mock_api_server() -> Generator[str, None, None]:
    """
    Pytest fixture that spins up a mock FastAPI server for the entire test session.
    scope="session" means this server only starts up once when pytest begins,
    and shuts down once all tests are completely finished, saving time.
    """
    # Disable automatic docs generation to speed up the mock server slightly
    app = FastAPI(openapi_url=None, docs_url=None, redoc_url=None)

    # Define the mock endpoint that mimics the real Infinite Craft API
    @app.get("/api/infinite-craft/pair")
    async def pair(first: str, second: str) -> dict[str, str | bool]:  # type: ignore
        print(f"[MOCK API] PAIR: {first} + {second}")
        print("[MOCK API] RESULT: 🌌 ???")
        # Always return a static dummy response for testing purposes
        return {"result": "???", "emoji": "🌌", "isNew": False}

    # Initialize and start our custom threaded server
    server = ThreadedUvicorn(app, host=HOST, port=PORT)
    print("\nStarting MOCK API server")
    server.start()

    # Yield control back to pytest.
    # Tests will receive the URL string, and execution pauses here.
    yield f"http://{HOST}:{PORT}"

    # Once all tests are done, execution resumes here to tear down the server
    print("\nStopping MOCK API server")
    server.stop()


@pytest.fixture
def mock_kwargs(mock_api_server: str, tmp_path: Any) -> dict[str, Any]:
    """
    Provides standard initialization arguments for the InfiniteCraft client.
    Because this fixture does not have scope="session", it runs fresh for EVERY test.
    """
    return {
        "api_url": mock_api_server,
        # tmp_path creates a unique, isolated temporary directory for every single test.
        # This prevents tests from overwriting each other's discoveries.json files.
        "discoveries_storage": str(tmp_path / "discoveries.json"),
        "debug": True,
    }
