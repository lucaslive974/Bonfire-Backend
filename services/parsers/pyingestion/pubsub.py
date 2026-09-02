import time
from typing import Any, Callable, List

from utils.logger import logger


class DeadLetterQueue:
    def __init__(self):
        self._dlq = []

    def route(self, item: Any, error: str):
        logger.error(f"Routing item to DLQ due to error: {error}. Item: {item}")
        self._dlq.append((item, error))


class SyncBatchProcessor:
    def __init__(
        self, processor_func: Callable[[List[Any]], int], batch_size: int = 100
    ):
        self.processor_func = processor_func
        self.batch_size = batch_size
        self._buffer = []

        self.inserted_count = 0
        self.ignored_count = 0
        self.total_processed = 0

        self.dlq = DeadLetterQueue()

    def start(self):
        # Manteve para compatibilidade de interface
        pass

    def publish(self, item: Any):
        self._buffer.append(item)
        if len(self._buffer) >= self.batch_size:
            self._flush()

    def _flush(self):
        if not self._buffer:
            return

        batch_len = len(self._buffer)
        try:
            inserted = self.processor_func(self._buffer)

            if inserted is None:
                inserted = 0

            self.inserted_count += inserted
            self.ignored_count += batch_len - inserted
            self.total_processed += batch_len
            self._buffer.clear()
        except Exception as e:
            logger.warn(
                f"Batch processing failed. Triggering backoff/retry. Error: {e}"
            )
            time.sleep(2)
            try:
                inserted = self.processor_func(self._buffer)
                if inserted is None:
                    inserted = 0
                self.inserted_count += inserted
                self.ignored_count += batch_len - inserted
                self.total_processed += batch_len
                self._buffer.clear()
                logger.info("Batch processed and ACKed successfully on retry.")
            except Exception as retry_err:
                logger.error(f"Retry failed. Routing batch to DLQ. Error: {retry_err}")
                self.total_processed += batch_len
                self.ignored_count += batch_len
                for item in self._buffer:
                    self.dlq.route(item, str(retry_err))
                self._buffer.clear()

    def stop(self):
        self._flush()
