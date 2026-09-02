from abc import ABC, abstractmethod
from typing import BinaryIO


class DocumentExtractor(ABC):
    """Abstract interface for all document extractors."""

    @abstractmethod
    def extract(self, file_stream: BinaryIO) -> dict:
        """
        Executes the extraction pipeline on the given file stream asynchronously.
        Delegates data saving to configured Write Streams.
        """
        pass


class DocumentParserFactory(ABC):
    """Abstract Factory for creating specific document extractors based on domain use cases."""

    @abstractmethod
    def create_primeira_instancia_parser(self) -> DocumentExtractor:
        pass

    @abstractmethod
    def create_segunda_instancia_parser(self) -> DocumentExtractor:
        pass

    @abstractmethod
    def create_infracoes_csv_parser(self) -> DocumentExtractor:
        pass

    @abstractmethod
    def create_infracoes_xls_parser(self, ignore: bool = False) -> DocumentExtractor:
        pass
