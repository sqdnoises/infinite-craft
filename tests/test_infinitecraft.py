import os
import time
import pytest
import asyncio
import uvicorn
from typing import Any
from uvicorn import Config
from threading import Thread

from infinitecraft       import (
    InfiniteCraft,
    Element
)
from infinitecraft.utils import mock_server

HOST = "127.0.0.1"
PORT = 15575

kwargs: Any = dict(
    api_url = f"http://{HOST}:{PORT}",
    discoveries_storage = "tests/discoveries.json",
    debug = True
)

def remove():
    file = kwargs.get("discoveries_storage")
    if os.path.exists(file):
        os.remove(file)

class ThreadedUvicorn:
    def __init__(self, *args: Any, config: Config | None = None, **kwargs: Any):
        if config is None:
            self.server = uvicorn.Server(Config(*args, **kwargs))
        else:
            self.server = uvicorn.Server(config)
        self.thread = Thread(daemon=True, target=self.server.run)

    def start(self):
        self.thread.start()
        asyncio.run(self.wait_for_started())

    async def wait_for_started(self):
        while not self.server.started:
            await asyncio.sleep(0.1)

    def stop(self):
        if self.thread.is_alive():
            self.server.should_exit = True
            while self.thread.is_alive():
                continue

# mock server
app = mock_server()
server = ThreadedUvicorn(app, host=HOST, port=PORT)

print("Starting MOCK API server")
server.start()
print("MOCK API server started")

remove()

class TestInfiniteCraftFiles:
    @pytest.mark.asyncio
    async def test_make_file_False(self):
        remove()
        with pytest.raises(FileNotFoundError):
            InfiniteCraft(**kwargs, make_file=False)
    
    @pytest.mark.asyncio
    async def test_make_file_True(self):
        remove()
        InfiniteCraft(**kwargs, make_file=True)
        assert os.path.exists(kwargs.get("discoveries_storage"))
    
    @pytest.mark.asyncio
    async def test_make_file_and_do_reset_True(self):
        remove()
        InfiniteCraft(**kwargs, do_reset=True, make_file=True)
    
    @pytest.mark.asyncio
    async def test_make_file_and_do_reset_False(self):
        remove()
        with pytest.raises(FileNotFoundError):
            InfiniteCraft(**kwargs, do_reset=False, make_file=False)
        
        InfiniteCraft(**kwargs, do_reset=False, make_file=True)
        
        InfiniteCraft(**kwargs, do_reset=False, make_file=False)
        assert os.path.exists(kwargs.get("discoveries_storage"))

@pytest.mark.asyncio
async def test_InfiniteCraft():
    remove()
    game = InfiniteCraft(**kwargs)
    
    # --- test_check_session_before ---
    assert game.closed == None
    
    with pytest.raises(RuntimeError):
        await game.close()
    # ---------------------------------
    
    await game.start() # test_start_session
    
    assert game.closed == False # test_session_started
    
    # --- test_check_ping ---
    ping = await game.ping()
    print(ping, "seconds")
    assert ping >= 0
    # -----------------------
    
    # --- test_check_requests ---
    
    start = time.monotonic()
    
    # --- test_check_pairing ---
    first = Element("Fire")
    second = Element("Water")
    
    # --- test_check_store_False ---
    result = await game.pair(first, second, store=False)
    assert result not in game.discoveries
    # ------------------------------
    
    current = time.monotonic() - 50
    game._requests = [current for i in range(game._api_rate_limit - 1)] # adding 1 less than ratelimit amount of dummy requests # type: ignore
    
    result = await game.pair(first, second)
    assert result is not None
    assert result in game.discoveries
    # --------------------------
    
    time_taken = round(time.monotonic() - start)
    
    assert time_taken < 2 # 2 seconds for good measure
    
    current = time.monotonic() - 50
    game._requests = [current for i in range(game._api_rate_limit)] # adding ratelimit amount of dummy requests # type: ignore
    
    start = time.monotonic()
    result = await game.pair(first, second)
    time_taken = round(time.monotonic() - start)
    
    assert time_taken >= 10 and time_taken < 12 # 10 seconds for "rate limit" and +2 seconds for good measure
    
    # ---------------------------
    
    await game.close() # test_end_session
    
    # --- test_check_session_after ---
    assert game.closed == True
    
    with pytest.raises(RuntimeError):
        await game.start()
    # --------------------------------

@pytest.mark.asyncio
async def test_InfiniteCraft_async_with():
    remove()
    game = InfiniteCraft(**kwargs)
    
    # --- test_check_session_before ---
    assert game.closed == None
    
    with pytest.raises(RuntimeError):
        await game.close()
    # ---------------------------------
    
    await game.start() # test_start_session
    
    assert game.closed == False # test_session_started
    
    await game.close() # test_end_session
    
    # --- test_check_session_after ---
    assert game.closed == True
    
    with pytest.raises(RuntimeError):
        await game.start()
    # --------------------------------

@pytest.mark.asyncio
async def test_InfiniteCraft_async_with2():
    remove()
    
    # --- test_session ---
    async with InfiniteCraft(**kwargs) as game: # test_start_session  # type: ignore
        game: InfiniteCraft

        # --- test_check_ping ---
        ping = await game.ping()
        print(ping, "seconds")
        assert ping >= 0
        # -----------------------
        
        assert game.closed == False # test_session_started
        
        # --- test_check_requests ---
        
        start = time.monotonic()
        
        # --- test_check_pairing ---
        first = Element("Fire")
        second = Element("Water")
        
        # --- test_check_store_False ---
        result = await game.pair(first, second, store=False)
        assert result not in game.discoveries
        # ------------------------------
        
        current = time.monotonic() - 50
        game._requests = [current for i in range(game._api_rate_limit - 1)] # adding 1 less than ratelimit amount of dummy requests # type: ignore
        
        result = await game.pair(first, second)
        assert result is not None
        # --------------------------
        
        time_taken = round(time.monotonic() - start)
        
        assert time_taken < 2 # 2 seconds for good measure
        
        current = time.monotonic() - 50
        game._requests = [current for i in range(game._api_rate_limit)] # adding ratelimit amount of dummy requests # type: ignore
        
        start = time.monotonic()
        result = await game.pair(first, second)
        time_taken = round(time.monotonic() - start)
        
        assert time_taken >= 10 and time_taken < 12 # 10 seconds for "rate limit" and +2 seconds for good measure
        
        # ---------------------------
    # --------------------------

@pytest.mark.asyncio
async def test_InfiniteCraft_manual_control():
    remove()
    game = InfiniteCraft(**kwargs, manual_control=True)
    
    await game.start() # test_start_session
    
    assert game.closed == False # test_session_started
    
    await game.close() # test_end_session
    
    # --- test_check_session_after ---
    assert game.closed == True
    
    with pytest.raises(RuntimeError):
        await game.start()
    # --------------------------------

def pytest_sessionfinish(session: Any, exitstatus: Any):
    print("Clean files")
    remove()
    print("Stopping MOCK API server")
    server.stop()
    print("MOCK API server stopped")
    print("Test finished")