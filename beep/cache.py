from typing import Dict

from beep.beep import BeepInstance

_cache: Dict[int, BeepInstance] = {}


def get_beep_instance(guild_id: int) -> BeepInstance:
    if guild_id not in _cache:
        _cache[guild_id] = BeepInstance(guild_id)

    return _cache[guild_id]
