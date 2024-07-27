import asyncio
import time

import pytest

from timeout_decorator import timeout_decorator


def test_sync_function_timeout():
    @timeout_decorator(1)
    def slow_function():
        time.sleep(2)
        return "Done"

    assert slow_function() is None

def test_sync_function_success():
    @timeout_decorator(2)
    def fast_function():
        time.sleep(1)
        return "Done"

    assert fast_function() == "Done"

@pytest.mark.asyncio
async def test_async_function_timeout():
    @timeout_decorator(1)
    async def slow_async_function():
        await asyncio.sleep(2)
        return "Done"

    assert await slow_async_function() is None

@pytest.mark.asyncio
async def test_async_function_success():
    @timeout_decorator(2)
    async def fast_async_function():
        await asyncio.sleep(1)
        return "Done"

    assert await fast_async_function() == "Done"

def test_sync_function_with_callback():
    callback_called = False

    def callback(func_name, *args, **kwargs):
        nonlocal callback_called
        callback_called = True

    @timeout_decorator(1, callback=callback)
    def slow_function():
        time.sleep(2)
        return "Done"

    assert slow_function() is None
    assert callback_called

def test_sync_function_with_custom_error():
    class CustomTimeoutError(Exception):
        pass

    @timeout_decorator(1, custom_error=CustomTimeoutError)
    def slow_function():
        time.sleep(2)
        return "Done"

    with pytest.raises(CustomTimeoutError):
        slow_function()

@pytest.mark.asyncio
async def test_async_function_with_custom_error():
    class CustomTimeoutError(Exception):
        pass

    @timeout_decorator(1, custom_error=CustomTimeoutError)
    async def slow_async_function():
        await asyncio.sleep(2)
        return "Done"

    with pytest.raises(CustomTimeoutError):
        await slow_async_function()

def test_sync_function_exception():
    @timeout_decorator(1)
    def error_function():
        raise ValueError("Test error")

    with pytest.raises(ValueError, match="Test error"):
        error_function()

@pytest.mark.asyncio
async def test_async_function_exception():
    @timeout_decorator(1)
    async def error_async_function():
        raise ValueError("Test error")

    with pytest.raises(ValueError, match="Test error"):
        await error_async_function()