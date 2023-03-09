import time
from multiprocessing import Event, Process
from multiprocessing.synchronize import Event as EventClass

from .delayed_interrupt import DelayedInterrupt


def process_main(
    terminate_event: EventClass, result_event: EventClass
) -> None:
    with DelayedInterrupt():
        terminate_event.set()
        time.sleep(1)
        result_event.set()


def test_delayed_interrupt() -> None:
    terminate_event = Event()
    result_event = Event()
    process = Process(
        target=process_main, args=(terminate_event, result_event)
    )
    process.start()
    terminate_event.wait(timeout=10)
    process.terminate()
    process.join()
    assert result_event.is_set()
