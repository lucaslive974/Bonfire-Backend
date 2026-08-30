from abc import ABC, abstractmethod
from typing import Any, BinaryIO, Dict, Optional


class ExtractionObserver:
    """Observer to track metrics and events during PyIngestion extraction"""
    def __init__(self):
        self.metrics: Dict[str, Any] = {
            "rows_processed": 0,
            "warnings": [],
            "status": "pending"
        }

    def on_event(self, event_name: str, event_data: Any = None) -> None:
        """Handles events emitted by the extraction pipeline"""
        if event_name == "row_processed":
            self.metrics["rows_processed"] += 1
        elif event_name == "warning":
            self.metrics["warnings"].append(event_data)
        elif event_name == "status_change":
            self.metrics["status"] = event_data


class DocumentExtractor(ABC):
    """Abstract interface for all document extractors."""
    
    @abstractmethod
    def extract(self, file_stream: BinaryIO, observer: Optional[ExtractionObserver] = None) -> None:
        """
        Executes the extraction pipeline on the given file stream.
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
