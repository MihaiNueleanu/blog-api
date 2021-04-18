import asyncio

loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)


def fire_and_forget(function):
    """
    Use this decorator to create an in-process async call
    """
    def wrapped(*args, **kwargs):
        return loop.run_in_executor(None, function, *args, *kwargs)

    return wrapped
