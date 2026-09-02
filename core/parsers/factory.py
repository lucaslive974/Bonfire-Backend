from core.parsers.core import DocumentExtractor
from core.parsers.pyingestion.pyingestion_extractor import (
    PyIngestionDocumentExtractor,
)
from core.parsers.pyingestion.streams import (
    BonfireInfracaoWriteStream,
    BonfireRecursoWriteStream,
    InfracoesCsvInputStream,
    InfracoesTransformStream,
    InfracoesXlsInputStream,
    NoOpTransformStream,
    RecursosDocxInputStream,
)


class ParserFactory:
    def __init__(self, service_factory):
        self.service_factory = service_factory

    def create_primeira_instancia_parser(self) -> DocumentExtractor:
        return PyIngestionDocumentExtractor(
            input_stream_class=lambda: RecursosDocxInputStream(first_instance=True),
            transform_stream_class=NoOpTransformStream,
            write_stream_factory=lambda: BonfireRecursoWriteStream(
                self.service_factory, first_instance=True
            ),
        )

    def create_segunda_instancia_parser(self) -> DocumentExtractor:
        return PyIngestionDocumentExtractor(
            input_stream_class=lambda: RecursosDocxInputStream(first_instance=False),
            transform_stream_class=NoOpTransformStream,
            write_stream_factory=lambda: BonfireRecursoWriteStream(
                self.service_factory, first_instance=False
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
            write_stream_factory=lambda: BonfireInfracaoWriteStream(
                self.service_factory, ignore=ignore
            ),
        )

    def create_infracoes_xls_parser(self, ignore: bool = False) -> DocumentExtractor:
        return PyIngestionDocumentExtractor(
            input_stream_class=InfracoesXlsInputStream,
            transform_stream_class=lambda: InfracoesTransformStream(
                datetime_format="%Y-%m-%d %H:%M:%S",
                date_format="%Y-%m-%d",
                convert_val_infr=False,
            ),
            write_stream_factory=lambda: BonfireInfracaoWriteStream(
                self.service_factory, ignore=ignore
            ),
        )
