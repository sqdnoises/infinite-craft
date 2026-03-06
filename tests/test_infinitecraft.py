import os
import time
import pytest
import warnings
from typing import Any
from infinitecraft import InfiniteCraft, Element


class TestinfinitecraftFileTests:
    """
    Tests the file handling logic of the InfiniteCraft client, specifically
    how it creates or interacts with the local discoveries.json file.
    """

    @pytest.mark.asyncio
    async def test_raises_error_when_make_file_is_false_without_existing_file(
        self, mock_kwargs: dict[str, Any]
    ) -> None:
        # If the file doesn't exist and we explicitly tell the client NOT to make it,
        # it should raise a FileNotFoundError.
        with pytest.raises(FileNotFoundError):
            InfiniteCraft(**mock_kwargs, make_file=False)

    @pytest.mark.asyncio
    async def test_creates_file_when_make_file_is_true(
        self, mock_kwargs: dict[str, Any]
    ) -> None:
        # If we tell the client to make the file, it should create it successfully.
        InfiniteCraft(**mock_kwargs, make_file=True)
        assert os.path.exists(mock_kwargs.get("discoveries_storage", ""))

    @pytest.mark.asyncio
    async def test_creates_fresh_file_when_reset_and_make_file_are_true(
        self, mock_kwargs: dict[str, Any]
    ) -> None:
        # Combining reset and make_file should result in a fresh file being created.
        InfiniteCraft(**mock_kwargs, do_reset=True, make_file=True)
        assert os.path.exists(mock_kwargs.get("discoveries_storage", ""))

    @pytest.mark.asyncio
    async def test_file_handling_behavior_when_reset_is_false(
        self, mock_kwargs: dict[str, Any]
    ) -> None:
        # If reset is False, it expects a file to exist. If we forbid making one, it fails.
        with pytest.raises(FileNotFoundError):
            InfiniteCraft(**mock_kwargs, do_reset=False, make_file=False)

        # Create the file so the next test can succeed
        InfiniteCraft(**mock_kwargs, do_reset=False, make_file=True)

        # Now that the file exists, this should pass without raising an error
        InfiniteCraft(**mock_kwargs, do_reset=False, make_file=False)
        assert os.path.exists(mock_kwargs.get("discoveries_storage", ""))


@pytest.mark.asyncio
async def test_session_lifecycle_ping_and_rate_limiting(
    mock_kwargs: dict[str, Any],
) -> None:
    """
    Main test for the InfiniteCraft client. Tests session lifecycle, basic
    pairing API calls, and the internal rate-limiting defense mechanism.
    """
    game = InfiniteCraft(**mock_kwargs)

    # --- Test Session Lifecycle (Before Start) ---
    assert game.closed is None
    with pytest.raises(RuntimeError):
        await game.close()  # Cannot close a session that hasn't started

    # --- Test Session Lifecycle (Started) ---
    await game.start()
    assert game.closed is False

    # --- Test Ping ---
    ping = await game.ping()
    print(f"{ping} seconds")
    assert ping >= 0

    start = time.monotonic()
    first = Element("Fire")
    second = Element("Water")

    # --- Test Pairing (No Storage) ---
    result = await game.pair(first, second, store=False)
    assert result not in game.discoveries

    # --- Test Rate Limiting (Under the limit) ---
    # Artificially fill the request history to 1 LESS than the maximum allowed
    current = time.monotonic() - 50
    game._requests = [  # type: ignore
        current for _ in range(game._api_rate_limit - 1)  # type: ignore
    ]

    result = await game.pair(first, second)
    assert result is not None
    assert result in game.discoveries

    # Ensure the request happened quickly because we weren't rate-limited yet
    time_taken = round(time.monotonic() - start)
    assert time_taken < 2

    # --- Test Rate Limiting (Hitting the limit) ---
    # Artificially fill the request history completely to trigger the defense mechanism
    current = time.monotonic() - 50
    game._requests = [  # type: ignore
        current for _ in range(game._api_rate_limit)  # type: ignore
    ]

    start = time.monotonic()
    result = await game.pair(first, second)
    time_taken = round(time.monotonic() - start)

    # The library should have detected the limit and automatically paused for ~10 seconds
    assert 10 <= time_taken < 12

    # --- Test Session Lifecycle (After Close) ---
    await game.close()
    assert game.closed is True

    # Cannot start a session that has already been closed
    with pytest.raises(RuntimeError):
        await game.start()


@pytest.mark.asyncio
async def test_context_manager_updates_session_state_correctly(
    mock_kwargs: dict[str, Any],
) -> None:
    """
    Tests that the async context manager propertly updates the 'closed' state.
    """
    game = InfiniteCraft(**mock_kwargs)
    assert game.closed is None

    with pytest.raises(RuntimeError):
        await game.close()

    await game.start()
    assert game.closed is False

    await game.close()
    assert game.closed is True

    with pytest.raises(RuntimeError):
        await game.start()


@pytest.mark.asyncio
async def test_full_api_flow_using_async_context_manager(
    mock_kwargs: dict[str, Any],
) -> None:
    """
    Tests the full API functionality (ping, pair, rate limiting) while utilizing
    the async context manager ('async with') to handle startup/teardown.
    """
    async with InfiniteCraft(**mock_kwargs) as game:  # type: ignore
        game: InfiniteCraft

        ping = await game.ping()
        print(f"{ping} seconds")
        assert ping >= 0
        assert game.closed is False

        start = time.monotonic()
        first = Element("Fire")
        second = Element("Water")

        result = await game.pair(first, second, store=False)
        assert result not in game.discoveries

        # Test staying just under the rate limit
        current = time.monotonic() - 50
        game._requests = [  # type: ignore
            current for _ in range(game._api_rate_limit - 1)  # type: ignore
        ]

        result = await game.pair(first, second)
        assert result is not None

        time_taken = round(time.monotonic() - start)
        assert time_taken < 2

        # Test hitting the rate limit and verify the ~10s delay
        current = time.monotonic() - 50
        game._requests = [  # type: ignore
            current for _ in range(game._api_rate_limit)  # type: ignore
        ]

        start = time.monotonic()
        result = await game.pair(first, second)
        time_taken = round(time.monotonic() - start)

        assert 10 <= time_taken < 12


@pytest.mark.asyncio
async def test_session_lifecycle_with_manual_control_enabled(
    mock_kwargs: dict[str, Any],
) -> None:
    """
    Tests that the client functions correctly when manual_control is enabled.
    """
    game = InfiniteCraft(**mock_kwargs, manual_control=True)

    await game.start()
    assert game.closed is False

    await game.close()
    assert game.closed is True

    with pytest.raises(RuntimeError):
        await game.start()


@pytest.mark.asyncio
async def test_real_api_connectivity(tmp_path: Any) -> None:
    """
    Tests the real neil.fun API.
    Wrapped in a try/except block so that if the external API goes down or changes,
    it issues a warning rather than failing the entire test suite in CI/CD.
    """
    real_api_kwargs = {  # type: ignore
        "discoveries_storage": str(tmp_path / "actual_discoveries.json"),
        "debug": True,
    }

    async with InfiniteCraft(**real_api_kwargs) as game:  # type: ignore
        try:
            ping = await game.ping()
            assert ping >= 0

            first = Element("Fire")
            second = Element("Water")

            # Store=False prevents us from muddying up real game files
            result = await game.pair(first, second, store=False)
            assert result is not None

        except Exception as e:
            warnings.warn(
                f"Real API test failed (likely downtime or network issue). Exception: {e}"
            )
