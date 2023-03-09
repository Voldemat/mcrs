import os
import signal
import types
from typing import Any, Callable


SIGNAL_TRANSLATION_MAP: dict[int, str] = {
    signal.SIGINT: "SIGINT",
    signal.SIGTERM: "SIGTERM",
}


class DelayedInterrupt:
    _pid: int
    _propagate_to_forked_processes: bool | None
    _sig: int | None
    _frame: types.FrameType | None
    _old_signal_handler_map: dict[
        int, Callable[[int, types.FrameType | None], None] | int | None
    ]

    def __init__(self, propagate_to_forked_processes: bool | None = None):
        self._pid = os.getpid()
        self._propagate_to_forked_processes = propagate_to_forked_processes
        self._sig = None
        self._frame = None
        self._old_signal_handler_map = {}

    def __enter__(self) -> None:
        self._old_signal_handler_map = {
            sig: signal.signal(sig, self._handler)
            for sig, _ in SIGNAL_TRANSLATION_MAP.items()
        }

    def __exit__(self, *args: Any, **kwargs: Any) -> None:
        for sig, handler in self._old_signal_handler_map.items():
            signal.signal(sig, handler)

        if self._sig is None:
            return

        signal_handler = self._old_signal_handler_map[self._sig]
        if callable(signal_handler):
            signal_handler(self._sig, self._frame)

    def _handler(self, sig: int, frame: types.FrameType | None) -> None:
        self._sig = sig
        self._frame = frame

        if os.getpid() != self._pid:
            if self._propagate_to_forked_processes is False:
                print(
                    "!!! DelayedKeyboardInterrupt._handler: "
                    f"{SIGNAL_TRANSLATION_MAP[sig]} received; "
                    f"PID mismatch: {os.getpid()=}, {self._pid=}, "
                    "calling original handler"
                )
                signal_handler = self._old_signal_handler_map[self._sig]
                if callable(signal_handler):
                    signal_handler(self._sig, self._frame)
            elif self._propagate_to_forked_processes is None:
                print(
                    "!!! DelayedKeyboardInterrupt._handler: "
                    f"{SIGNAL_TRANSLATION_MAP[sig]} received; "
                    f"PID mismatch: {os.getpid()=}, ignoring the signal"
                )
                return

        print(
            "!!! DelayedKeyboardInterrupt._handler: "
            f"{SIGNAL_TRANSLATION_MAP[sig]} received; "
            "delaying KeyboardInterrupt"
        )
