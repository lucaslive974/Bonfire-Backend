from abc import ABC, abstractmethod
from typing import BinaryIO


class DocumentExtractor(ABC):
    @abstractmethod
    def extract(self, file_stream: BinaryIO) -> dict:
        pass
