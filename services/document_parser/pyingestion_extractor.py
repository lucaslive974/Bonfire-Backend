from typing import Any, BinaryIO, Callable, Optional

from pyingestion import ExtractionObserver as PyIngestionObserver
from pyingestion import ExtractionSession, Gaia

from services.document_parser.core import DocumentExtractor, ExtractionObserver
from services.document_parser.exceptions import DocumentParsingError


class PyIngestionObserverAdapter(PyIngestionObserver):
    is_cancelled = False

    """Adapts PyIngestion's native observer events to Bonfire's ExtractionObserver"""

    def __init__(self, bonfire_observer: ExtractionObserver):
        self.bonfire_observer = bonfire_observer

    def on_start(self, *args, **kwargs):
        self.bonfire_observer.on_event("status_change", "started")

    def on_page_processed(self, *args, **kwargs):
        self.bonfire_observer.on_event("row_processed")

    def on_error(self, error: Exception, *args, **kwargs):
        self.bonfire_observer.on_event("warning", str(error))
        self.bonfire_observer.on_event("status_change", "error")

    def on_complete(self, *args, **kwargs):
        self.bonfire_observer.on_event("status_change", "completed")

    def on_file_start(self, *args, **kwargs):
        pass

    def on_file_complete(self, *args, **kwargs):
        pass

    def on_page_start(self, *args, **kwargs):
        pass


class PyIngestionDocumentExtractor(DocumentExtractor):
    """Concrete DocumentExtractor that orchestrates PyIngestion's ETL pipeline."""

    def __init__(
        self,
        input_stream_class: Any,
        transform_stream_class: Any,
        write_stream_factory: Callable[[], Any],
    ):
        self.input_stream_class = input_stream_class
        self.transform_stream_class = transform_stream_class
        self.write_stream_factory = write_stream_factory

    def clone(self) -> "PyIngestionDocumentExtractor":
        """Returns a fresh instance of the configured extractor"""
        return PyIngestionDocumentExtractor(
            input_stream_class=self.input_stream_class,
            transform_stream_class=self.transform_stream_class,
            write_stream_factory=self.write_stream_factory,
        )

    def extract(
        self, file_stream: BinaryIO, observer: Optional[ExtractionObserver] = None
    ) -> None:
        try:
            # 1. Instantiate the stream components
            input_stream = self.input_stream_class()
            transform_stream = self.transform_stream_class()
            output_stream = self.write_stream_factory()

            # 2. Setup the Observer and Session
            pyingestion_observer = None
            if observer:
                pyingestion_observer = PyIngestionObserverAdapter(observer)

            session = ExtractionSession(observer=pyingestion_observer)

            # 3. Execute the pipeline using Gaia
            gaia = Gaia()
            success = gaia.process(
                source=file_stream,
                input_stream=input_stream,
                transform_stream=transform_stream,
                output_stream=output_stream,
                session=session,
            )

            # 4. Flush any remaining items in custom output streams
            if hasattr(output_stream, "flush") and callable(output_stream.flush):
                output_stream.flush()

            if not success:
                raise DocumentParsingError("Extraction pipeline failed or was aborted.")

        except Exception as e:
            if isinstance(e, DocumentParsingError):
                raise
            raise DocumentParsingError(f"PyIngestion pipeline failed: {str(e)}")
