"""Django caching wrapper and cache related capabilities."""
from collections.abc import Callable

from django.core.cache import cache
from huey.contrib.djhuey import db_task

from conreq.utils import log
from conreq.utils.generic import clean_string
from conreq.utils.threads import ReturnThread

# Globals
DEFAULT_CACHE_DURATION = 60 * 60  # Time in seconds

# Creating a logger (for log files)
_logger = log.get_logger(__name__)


def generate_cache_key(
    cache_name: str, cache_args: list, cache_kwargs: dict, key: str
) -> str:
    """Generates a key to be used with django caching"""
    return clean_string(
        (
            cache_name
            + "_args"
            + str(cache_args)
            + "_kwargs"
            + str(cache_kwargs)
            + "_key"
            + key
        )
    )


def obtain_key_from_cache_key(cache_key: str) -> str:
    """Parses the cache key and returns any values after the string '_key'"""
    return cache_key[cache_key.find("_key") + len("_key") :]


@db_task()
def __cache_set_many(missing_keys, cache_duration):
    cache.set_many(missing_keys, cache_duration)


@db_task()
def __cache_set(cache_key, function_results, cache_duration):
    cache.set(cache_key, function_results, cache_duration)


def handler(
    cache_name: str,
    page_key: str = "",
    function: Callable = None,
    force_update_cache: bool = False,
    cache_duration: int = DEFAULT_CACHE_DURATION,
    args: list = (),
    kwargs: dict = None,
) -> any:
    """Handles caching for results and data.

    Args:
        cache_name: Name prepended to cache get/set calls.
        page_key: A value to use as a page key.
        function: The function to be executed (if cached values are expired).
            If no function is provided, whatever was stored in cache is always returned.
        force_update_cache: Forces execution of function, regardless if value is expired or not. Does not work with multi execution.
        cache_duration: Duration in seconds that the cached value should be valid for.
        args: A list of arguements to pass into function.
        kwargs: A dictionary of keyworded arguements to pass into function.
    """

    if kwargs is None:
        kwargs = {}
    cached_results = None
    # Looks through cache and will perform a search if needed.
    try:
        log.handler(f"{cache_name} - Accessed.", log.DEBUG, _logger)

        # Get the cached value
        cache_key = generate_cache_key(cache_name, args, kwargs, page_key)
        cached_results = cache.get(cache_key)
        log.handler(
            f"{cache_name} - Generated cache key {cache_key}",
            log.DEBUG,
            _logger,
        )

        # No function was provided, just return a bare cache value
        if function is None:
            log.handler(f"{cache_name} - Requested raw cache values.", log.DEBUG, _logger)
            return cached_results

        # If the user wants to force update the cache, nothing
        # was in cache, or cache was expired, run function()
        if cached_results is None or force_update_cache:
            function_results = function(*args, **kwargs)
            if function_results:
                __cache_set(cache_key, function_results, cache_duration)
            log.handler(f"{cache_name} - {function.__name__}()", log.INFO, _logger)
            return function_results

        # If a value was in cache and not expired, return that value
        return cached_results

    except Exception:
        # If the function threw an exception, return none.
        if hasattr(function, "__name__"):
            log.handler(
                f"Function {function.__name__} failed to execute!",
                log.ERROR,
                _logger,
            )
        else:
            log.handler(
                f"Cache handler has failed! Function: {str(function)} Cache Name: {cache_name} Page Key: {page_key}",
                log.ERROR,
                _logger,
            )
    return None


def multi_handler(
    cache_name: str,
    functions: dict[dict],
    cache_duration: int = DEFAULT_CACHE_DURATION,
    timeout: int = 5,
) -> dict[dict]:
    """Retrieve, set, and potentially execute multiple cache functions at once.
    Functions must follow this format:

    {
      page_key : {
         "function": function_value,
         "args": [args_values],
         "kwargs": {kwargs_value},
      },
      ...
    }
    """
    try:
        log.handler(f"{cache_name} - Accessed.", log.DEBUG, _logger)

        requested_keys = []
        for key, value in functions.items():
            cache_key = generate_cache_key(
                cache_name, value["args"], value["kwargs"], key
            )
            log.handler(
                f"{cache_name} - Cache multi execution generated cache key {cache_key}",
                log.DEBUG,
                _logger,
            )
            requested_keys.append(cache_key)

        # Search cache for all keys
        cached_results = cache.get_many(requested_keys)
        log.handler(
            f"{cache_name} - Cache multi execution detected {len(cached_results)} available keys.",
            log.INFO,
            _logger,
        )

        # If nothing was in cache, or cache was expired, run function()
        thread_list = []
        for cache_key in requested_keys:
            if not cached_results.__contains__(cache_key):
                key = obtain_key_from_cache_key(cache_key)
                thread = ReturnThread(
                    target=functions[key]["function"],
                    args=functions[key]["args"],
                    kwargs=functions[key]["kwargs"],
                )
                thread.start()
                thread_list.append((cache_key, thread))

        missing_keys = {
            key: thread.join(timeout=timeout) for key, thread in thread_list
        }
        # Set values in cache for any newly executed functions
        if bool(missing_keys):
            log.handler(
                f"{cache_name} - Cache multi execution detected {len(missing_keys)} missing keys.",
                log.INFO,
                _logger,
            )
            __cache_set_many(missing_keys, cache_duration)

        # Return all results
        cached_results.update(missing_keys)

        # If results were none, log it.
        if cached_results is None:
            log.handler(
                f"{cache_name} - Cache multi execution generated no results!",
                log.WARNING,
                _logger,
            )

        return cached_results

    except Exception:
        log.handler(f"Functions {functions} failed to execute!", log.ERROR, _logger)
    return None
