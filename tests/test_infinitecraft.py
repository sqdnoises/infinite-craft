import os
import pytest
import asyncio
import uvicorn
from typing import Any as Ignore
from fastapi import FastAPI
from uvicorn import Config
from threading import Thread
from infinitecraft import InfiniteCraft, Element, Logger


kwargs: Ignore = dict(
    api_url = "http://127.0.0.1:8080",
    discoveries_storage="tests/discoveries.json",
    logger=Logger(log_level=5)
)

def remove():
    file = kwargs.get("discoveries_storage")
    if os.path.exists(file):
        os.remove(file)


class ThreadedUvicorn:
    def __init__(self, *args: Ignore, config: Config | None = None, **kwargs: Ignore):
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
app = FastAPI() 
server = ThreadedUvicorn(app, host="127.0.0.1", port=8080)

@app.get("/api/infinite-craft/pair")
async def pair(first: str, second: str):
    print(f"[MOCK API] PAIR: {first} + {second}")
    print(f"[MOCK API] RESULT: 🌌 ???")
    
    if len(first) == 0 or len(second) == 0:
        return {
            "result": "???",
            "emoji": "🌌",
            "isNew": False
        }
    return {
        "result": "???",
        "emoji": "🌌",
        "isNew": False
    }

print("Starting MOCK API server")
server.start()
print("MOCK API server started")

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
    
    # --- test_check_pairing ---
    first = Element("Fire")
    second = Element("Water")
    
    result = await game.pair(first, second)
    assert result is not None
    # --------------------------
    
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
        
        # --- test_check_pairing ---
        first = Element("Fire")
        second = Element("Water")
        
        result = await game.pair(first, second)
        assert result is not None
        # --------------------------
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

def pytest_sessionfinish(session: Ignore, exitstatus: Ignore):
    print("Clean files")
    remove()
    print("Stopping MOCK API server")
    server.stop()
    print("MOCK API server stopped")
    print("Test finished")