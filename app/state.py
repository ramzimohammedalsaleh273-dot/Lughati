from __future__ import annotations
from typing import Callable

_current_child_id: int | None = None
_listeners: list[Callable[[], None]] = []

def set_child(child_id: int | None):
    global _current_child_id
    _current_child_id = int(child_id) if child_id is not None else None
    for listener in list(_listeners):
        try: listener()
        except Exception: pass

def child_id() -> int | None:
    return _current_child_id

def subscribe(listener: Callable[[], None]):
    if listener not in _listeners: _listeners.append(listener)

def unsubscribe(listener: Callable[[], None]):
    if listener in _listeners: _listeners.remove(listener)
