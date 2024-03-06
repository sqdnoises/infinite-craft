import os
import pytest
from typing import Any as Ignore
from infinitecraft import InfiniteCraft, Element, Logger

d = "tests/discoveries.json"
e = "tests/emoji_cache.json"


def remove():
    if os.path.exists(d):
        os.remove(d)

    if os.path.exists(e):
        os.remove(e)


kwargs: Ignore = dict(
    discoveries_storage=d,
    emoji_cache=e,
    logger=Logger(log_level=5)
)


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

        assert os.path.exists(d)
        assert os.path.exists(e)
    
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
        assert os.path.exists(d)
        assert os.path.exists(e)


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
    first = Element("ThisElementDoesNotExist.OrDoesIt?No")
    second = Element("ThisElementDoesNotExist.OrDoesIt?Yes")
    
    result = await game.pair(first, second)
    assert result == None
    
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
    
    # --- test_check_pairing ---
    async with game: # test_start_session is handled
        assert game.closed == False # test_session_started
        
        first = Element("Fire")
        second = Element("Water")
        
        result = await game.pair(first, second)
        assert result is not None
    # --------------------------
    
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
        
        first = Element("ThisElementDoesNotExist.OrDoesIt?No")
        second = Element("ThisElementDoesNotExist.OrDoesIt?Yes")
        
        result = await game.pair(first, second)
        assert result == None
        
        first = Element("Fire")
        second = Element("Water")
        
        result = await game.pair(first, second)
        assert result is not None
    # --------------------------


@pytest.mark.asyncio
async def test_InfiniteCraft_manual_control():
    remove()
    game = InfiniteCraft(**kwargs, manual_control=True)
    
    await game.start() # test_start_session
    
    assert game.closed == False # test_session_started
    
    # --- test_check_ping ---
    ping = await game.ping()
    print(ping, "seconds")
    assert ping >= 0
    # -----------------------
    
    # --- test_check_pairing ---
    async with game:
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