#!/usr/bin/python3
"""
Asyncio - ArjanCodes.
Transform a sync function into an async one.
Gather performs concurrency
"""
import asyncio
from random import randint
from typing import Any
from async_utils import async_timed

import requests

# The highest Pokemon id
MAX_POKEMON = 898


def http_get_sync(url: str) -> Any:
    """Synchronous function"""

    response = requests.get(url)
    return response.json()


async def http_get(url: str) -> Any:
    """Transform a not async function into one"""

    return await asyncio.to_thread(http_get_sync, url)


async def get_random_pokemon_name() -> str:
    """Get a pokemon name between the range"""

    pokemon_id = randint(1, MAX_POKEMON)
    pokemon_url = f"https://pokeapi.co/api/v2/pokemon/{pokemon_id}"
    pokemon = await http_get(pokemon_url)
    return str(pokemon["name"])


@async_timed()
async def main() -> None:

    # asynchronous call
    pokemon = await asyncio.gather(
        *[get_random_pokemon_name() for _ in range(20)])
    print(pokemon)


asyncio.run(main())
