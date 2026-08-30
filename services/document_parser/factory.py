from services.document_parser.core import DocumentExtractor, DocumentParserFactory
from services.document_parser.pyingestion_extractor import PyIngestionDocumentExtractor
from services.document_parser.streams import (
    BonfireInfracaoWriteStream,
    BonfireRecursoWriteStream,
    InfracoesCsvInputStream,
    InfracoesTransformStream,
    InfracoesXlsInputStream,
    NoOpTransformStream,
    RecursosDocxInputStream,
)


class PyIngestionParserFactory(DocumentParserFactory):
    """Concrete Abstract Factory that uses PyIngestion to create document extractors."""

    def create_primeira_instancia_parser(self) -> DocumentExtractor:
        return PyIngestionDocumentExtractor(
            input_stream_class=lambda: RecursosDocxInputStream(first_instance=True),
            transform_stream_class=NoOpTransformStream,
            write_stream_factory=lambda: BonfireRecursoWriteStream(first_instance=True),
        )

    def create_segunda_instancia_parser(self) -> DocumentExtractor:
        return PyIngestionDocumentExtractor(
            input_stream_class=lambda: RecursosDocxInputStream(first_instance=False),
            transform_stream_class=NoOpTransformStream,
            write_stream_factory=lambda: BonfireRecursoWriteStream(
                first_instance=False
            ),
        )

    def create_infracoes_csv_parser(self, ignore: bool = False) -> DocumentExtractor:
        return PyIngestionDocumentExtractor(
            input_stream_class=InfracoesCsvInputStream,
            transform_stream_class=lambda: InfracoesTransformStream(
                datetime_format="%d/%m/%Y %H:%M",
                date_format="%d/%m/%Y",
                convert_val_infr=True,
            ),
            write_stream_factory=lambda: BonfireInfracaoWriteStream(ignore=ignore),
        )

    def create_infracoes_xls_parser(self, ignore: bool = False) -> DocumentExtractor:
        return PyIngestionDocumentExtractor(
            input_stream_class=InfracoesXlsInputStream,
            transform_stream_class=lambda: InfracoesTransformStream(
                datetime_format="%Y-%m-%d %H:%M:%S",
                date_format="%Y-%m-%d",
                convert_val_infr=False,
            ),
            write_stream_factory=lambda: BonfireInfracaoWriteStream(ignore=ignore),
        )
