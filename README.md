# Timeout Decorator

A versatile timeout decorator for both synchronous and asynchronous functions in Python.

## Features

- Works with both synchronous and asynchronous functions
- Customizable timeout duration
- Optional callback function on timeout
- Support for custom exception on timeout
- Colored logging

## Installation

```bash
pip install timeout-decorator
```
## Parameters
`timeout`: The maximum execution time in seconds.
`callback (optional)`: A function to be called if the timeout occurs.
`custom_error (optional)`: A custom exception class to be raised on timeout.

## Usage
#### Basic Usage
```python
from timeout_decorator import timeout_decorator

@timeout_decorator(5)  # 5 seconds timeout
def my_function():
    # Your code here
    pass

@timeout_decorator(10)  # 10 seconds timeout
async def my_async_function():
    # Your async code here
    pass
```
### Advanced Usage
```python 
from timeout_decorator import timeout_decorator

def on_timeout(func_name, *args, **kwargs):
    print(f"Function {func_name} timed out!")

class MyTimeoutError(Exception):
    pass

@timeout_decorator(5, callback=on_timeout, custom_error=MyTimeoutError)
def my_function():
    # Your code here
    pass

# Usage with synchronous function
try:
    result = my_function()
except MyTimeoutError:
    print("Caught custom timeout error")

# Usage with asynchronous function
@timeout_decorator(5, callback=on_timeout, custom_error=MyTimeoutError)
async def my_async_function():
    # Your async code here
    pass

import asyncio

async def main():
    try:
        result = await my_async_function()
    except MyTimeoutError:
        print("Caught custom timeout error")

asyncio.run(main())
``` 
## Tests
 run 
 ```python 
    pytest tests/test_timeout_decorator.py -v
```


## Notes
For synchronous functions, the decorator uses a `ThreadPoolExecutor` to implement the timeout.

For asynchronous functions, it uses `asyncio.wait_for()`.

The decorator automatically detects whether the decorated function is synchronous or asynchronous.

## Licence
This project is licensed under the MIT License
