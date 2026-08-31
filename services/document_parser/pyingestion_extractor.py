from typing import Any, BinaryIO, Callable

from pyingestion import ExtractionSession, Gaia
from pyingestion.observer import PipelineEvents

from services.document_parser.core import DocumentExtractor
from services.document_parser.exceptions import DocumentParsingError
from utils.logger import logger


class PyIngestionDocumentExtractor(DocumentExtractor):
    """Concrete DocumentExtractor that orchestrates PyIngestion's ETL pipeline asynchronously."""

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
        return PyIngestionDocumentExtractor(
            input_stream_class=self.input_stream_class,
            transform_stream_class=self.transform_stream_class,
            write_stream_factory=self.write_stream_factory,
        )

    def extract(self, file_stream: BinaryIO) -> dict:
        self.metrics = {"rows_processed": 0}
        self._run_extraction_pipeline(file_stream)
        return self.metrics

    def _run_extraction_pipeline(self, file_stream: BinaryIO) -> None:
        try:
            input_stream = self.input_stream_class()
            transform_stream = self.transform_stream_class()
            output_stream = self.write_stream_factory()

            session = ExtractionSession()

            # Register Pub/Sub listeners
            session.bus.on(PipelineEvents.EXTRACTION_STARTED, self._on_start)
            session.bus.on(PipelineEvents.PAGE_PROCESSED, self._on_page_processed)
            session.bus.on(PipelineEvents.EXTRACTION_ERROR, self._on_error)
            session.bus.on(PipelineEvents.EXTRACTION_COMPLETED, self._on_complete)

            gaia = Gaia()
            success = gaia.process(
                source=file_stream,
                input_stream=input_stream,
                transform_stream=transform_stream,
                output_stream=output_stream,
                session=session,
            )

            if hasattr(output_stream, "flush") and callable(output_stream.flush):
                output_stream.flush()

            if hasattr(output_stream, "processor") and hasattr(
                output_stream.processor, "inserted_count"
            ):
                self.metrics["rows_processed"] = output_stream.processor.inserted_count

            if not success:
                raise DocumentParsingError("Extraction pipeline failed or was aborted.")

        except Exception as e:
            if isinstance(e, DocumentParsingError):
                raise
            raise DocumentParsingError(f"PyIngestion pipeline failed: {str(e)}")

    def _on_start(self, session, total_files: int, **kwargs):
        logger.info(
            f"PyIngestion Event: EXTRACTION_STARTED - Total files: {total_files}"
        )

    def _on_page_processed(
        self,
        session,
        success: bool,
        extracted_pages: int,
        error_pages: int,
        page_index: int,
        total_pages: int,
        **kwargs,
    ):
        if not success:
            logger.warn(
                f"PyIngestion Event: PAGE_PROCESSED - Page {page_index}/{total_pages} processing failed."
            )

    def _on_error(self, session, error_message: str, **kwargs):
        logger.error(f"PyIngestion Event: EXTRACTION_ERROR - {error_message}")

    def _on_complete(self, session, successful_pages: int, total_pages: int, **kwargs):
        logger.info(
            f"PyIngestion Event: EXTRACTION_COMPLETED - Extracted {successful_pages}/{total_pages} pages successfully."
        )
