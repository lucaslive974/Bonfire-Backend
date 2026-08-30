import queue
import threading
import time
from typing import Any, Callable, List

from utils.logger import logger


class DeadLetterQueue:
    def __init__(self):
        self._dlq = []

    def route(self, item: Any, error: str):
        logger.error(f"Routing item to DLQ due to error: {error}. Item: {item}")
        self._dlq.append((item, error))


class AsyncMessageProcessor(threading.Thread):
    def __init__(
        self, processor_func: Callable[[List[Any]], None], batch_size: int = 100
    ):
        super().__init__(daemon=True)
        self.queue = queue.Queue()
        self.processor_func = processor_func
        self.batch_size = batch_size
        self._buffer = []
        self.inserted_count = 0
        self.dlq = DeadLetterQueue()
        self.running = True

    def publish(self, item: Any):
        self.queue.put(item)

    def run(self):
        while self.running:
            try:
                item = self.queue.get(timeout=0.5)
                if item == "STOP":
                    break

                self._buffer.append(item)

                if len(self._buffer) >= self.batch_size:
                    self._flush()
            except queue.Empty:
                self._flush()
            except Exception as e:
                logger.error(f"Unexpected error in AsyncMessageProcessor: {e}")

    def _flush(self):
        if not self._buffer:
            return

        try:
            # Try processing the whole batch
            self.processor_func(self._buffer)
            self.inserted_count += len(self._buffer)
            self._buffer.clear()
        except Exception as e:
            # NACK: Handle failure
            logger.warning(
                f"Batch processing failed. Triggering backoff/retry. Error: {e}"
            )
            time.sleep(2)  # Simple backoff
            try:
                self.processor_func(self._buffer)
                self._buffer.clear()
                logger.info("Batch processed and ACKed successfully on retry.")
            except Exception as retry_err:
                logger.error(f"Retry failed. Routing batch to DLQ. Error: {retry_err}")
                for item in self._buffer:
                    self.dlq.route(item, str(retry_err))
                self._buffer.clear()

    def stop(self):
        self.running = False
        self.queue.put("STOP")
        self.join()
        self._flush()
