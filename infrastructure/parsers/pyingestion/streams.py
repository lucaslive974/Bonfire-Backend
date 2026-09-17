import io
import re
import unicodedata
from typing import Any, Generator, cast

import numpy as np
import pandas as pd
from docx import Document
from docx.document import Document as DocxDocument
from docx.oxml.table import CT_Tbl
from docx.oxml.text.paragraph import CT_P
from docx.table import Table
from docx.text.paragraph import Paragraph
from pyingestion import ExtractionSession, InputStream, OutputStream, TransformStream

from domain.entities import AutoInfracao
from infrastructure.parsers.exceptions import (
    DocumentReadError,
    IncorrectInstanceError,
    InvalidDocumentDataError,
    PublicationDateNotFoundError,
    QuantityOfAtasMismatchError,
)
from infrastructure.parsers.pyingestion.pubsub import SyncBatchProcessor

# ==========================================
# WRITE STREAMS (Output)
# ==========================================


class BonfireRecursoWriteStream(OutputStream[Any]):
    def __init__(self, db_manager, first_instance: bool = True, batch_size: int = 100):
        self.db_manager = db_manager
        self.first_instance = first_instance
        self.processor = SyncBatchProcessor(self._process_batch, batch_size=batch_size)
        self.processor.start()
        super().__init__()

    def write(self, item: Any) -> None:
        if isinstance(item, list):
            for i in item:
                self.processor.publish(i)
        else:
            self.processor.publish(item)

    def _process_batch(self, batch: list[Any]) -> int:
        with self.db_manager.session() as session:
            repo = session.get_recurso_repository()
            if self.first_instance:
                return repo.insert_primeira_instancia(batch)
            else:
                return repo.insert_segunda_instancia(batch)

    def flush(self) -> None:
        self.processor.stop()


class BonfireInfracaoWriteStream(OutputStream[Any]):
    def __init__(self, db_manager, ignore: bool = False, batch_size: int = 1000):
        self.db_manager = db_manager
        self.ignore = ignore
        self.processor = SyncBatchProcessor(self._process_batch, batch_size=batch_size)
        self.processor.start()
        super().__init__()

    def write(self, item: Any) -> None:
        if isinstance(item, list):
            for i in item:
                self.processor.publish(i)
        else:
            self.processor.publish(item)

    def _process_batch(self, batch: list[Any]) -> int:
        with self.db_manager.session() as session:
            repo = session.get_autoinfracao_repository()
            autos = [AutoInfracao(**item) for item in batch]
            return repo.insert_bulk(autos)

    def flush(self) -> None:
        self.processor.stop()


# ==========================================
# INPUT STREAMS
# ==========================================


class RecursosDocxInputStream(InputStream[Any, dict[str, Any]]):
    """
    Extracts appeals from DOCX files and yields items one by one in stream fashion.
    """

    PATTERN_NUM_ATA = r"ATA\s+DA\s+(\d+)"

    def __init__(self, first_instance: bool = True):
        self.first_instance = first_instance
        self.current_unit_index = 0
        self.total_units = 0

    def extract_data_publ(self, doc: DocxDocument) -> str:
        data_publicacao_extracted = " ".join([p.text for p in doc.paragraphs])
        padrao_data = r"PUBLICADO NO DI[ÁA]RIO OFICIAL DO MUNIC[ÍI]PIO DE BELO HORIZONTE EM (\d{2}[/.-]\d{2}[/.-]\d{2,4})"
        match_data_publicacao = re.search(padrao_data, data_publicacao_extracted)
        dat_publ = match_data_publicacao.group(1) if match_data_publicacao else None

        if dat_publ is not None:
            from dateutil.parser import parse as parse_date

            try:
                parsed_date = parse_date(dat_publ, dayfirst=True)
                dat_publ = parsed_date.strftime("%Y-%m-%d")
            except Exception:
                raise PublicationDateNotFoundError(
                    f"A data de publicação encontrada ('{dat_publ}') está em um formato inválido."
                )
        else:
            raise PublicationDateNotFoundError(
                "Data de publicação não encontrada no documento"
            )
        return dat_publ

    def process_table(self, table: Table, dat_publ: str, num_ata: int | str | None):
        for row_idx, row in enumerate(table.rows):
            row_data = [cell.text.strip() for cell in row.cells]

            if not row_data:
                continue

            num_recurso = row_data[0]
            if num_recurso == "RECURSO":
                continue

            if len(row_data) < 4:
                raise InvalidDocumentDataError(
                    f"Erro na tabela DOCX (Ata {num_ata or 'Desconhecida'}): A linha {row_idx + 1} possui {len(row_data)} coluna(s), mas 4 eram esperadas."
                )

            if not num_recurso:
                raise InvalidDocumentDataError(
                    f"Erro na tabela DOCX (Ata {num_ata or 'Desconhecida'}): O número do recurso está vazio na linha {row_idx + 1}."
                )

            num_ai = normalize_auto_infraction_id(row_data[1])
            if not num_ai:
                raise InvalidDocumentDataError(
                    f"Erro na tabela DOCX (Ata {num_ata or 'Desconhecida'}): O número do Auto de Infração está vazio na linha {row_idx + 1}."
                )

            nom_conc = row_data[2]
            valida_resultado = str(row_data[3]).upper()
            resultado = valida_resultado != "IMPROCEDENTE"

            recurso = {
                "NUM_RECURSO": num_recurso,
                "NUM_AI": num_ai,
                "NOM_CONC": nom_conc,
                "RESULTADO": resultado,
                "DAT_PUBL": dat_publ,
            }
            if num_ata:
                recurso["NUM_ATA"] = num_ata
            yield recurso

    def _iter_block_items(
        self, doc: DocxDocument
    ) -> Generator[Paragraph | Table, None, None]:
        """Iterates through document body elements in document order."""
        for child in doc._element.body:
            if isinstance(child, CT_P):
                yield Paragraph(child, doc)
            elif isinstance(child, CT_Tbl):
                yield Table(child, doc)

    def validate_num_ata(self, num_ata: str | None) -> None:
        if self.first_instance:
            if num_ata is None:
                raise QuantityOfAtasMismatchError(
                    0,
                    0,
                    "Tabela encontrada antes de qualquer ata no documento",
                )
        elif num_ata is not None:
            raise IncorrectInstanceError(
                "Instância incorreta. Importe como recurso de primeira instância"
            )

    def read(
        self, source: Any, session: ExtractionSession | None = None
    ) -> Generator[dict[str, Any], None, None]:
        doc = Document(source)
        dat_publ = self.extract_data_publ(doc)

        current_ata: str | None = None
        for block in self._iter_block_items(doc):
            if isinstance(block, Paragraph):
                match_num_ata = re.search(self.PATTERN_NUM_ATA, block.text)
                if match_num_ata:
                    current_ata = match_num_ata.group(1)
            elif isinstance(block, Table):
                self.validate_num_ata(current_ata)
                if session:
                    session.process_page_result(True, 1, 1)
                yield from self.process_table(block, dat_publ, current_ata)


class SanitizedTextIO(io.TextIOBase):
    """
    Wrapper that intercepts the binary file stream,
    removes accents and encoding garbage BEFORE pandas attempts to parse it.
    """

    def __init__(self, binary_stream):
        self.binary_stream = binary_stream

    def read(self, size=-1):
        raw_bytes = self.binary_stream.read(size)
        if not raw_bytes:
            return ""

        # 1. Try UTF-8 or Latin-1, forcing the drop (ignore) of corrupted bytes
        try:
            text = raw_bytes.decode("utf-8", errors="ignore")
        except Exception:
            text = raw_bytes.decode("latin_1", errors="ignore")

        # 2. Normalize NFKD (remove accents) and drop any non-ASCII character
        return (
            unicodedata.normalize("NFKD", text)
            .encode("ascii", "ignore")
            .decode("ascii")
        )

    def seek(self, offset, whence=0):
        return self.binary_stream.seek(offset, whence)


class InfracoesCsvInputStream(InputStream[Any, pd.DataFrame]):
    """InputStream for CSV infraction files."""

    def __init__(self):
        self.current_unit_index = 0
        self.total_units = 0

    def _detect_separator(self, source: Any) -> str:
        """Reads the first bytes of the stream to infer the separator and resets the cursor."""
        try:
            first_chunk = source.read(2048)
            try:
                text = first_chunk.decode("utf-8", errors="ignore")
            except Exception:
                text = first_chunk.decode("latin_1", errors="ignore")

            sep_counts = {
                ",": text.count(","),
                ";": text.count(";"),
                "|": text.count("|"),
            }
            best_sep = max(sep_counts, key=lambda k: sep_counts[k])

            source.seek(0)
            return best_sep if sep_counts[best_sep] > 0 else ";"
        except Exception:
            try:
                source.seek(0)
            except Exception:
                pass
            return ";"

    def read(
        self, source: Any, session: ExtractionSession | None = None
    ) -> Generator[pd.DataFrame, None, None]:
        try:
            best_sep = self._detect_separator(source)
            clean_source = SanitizedTextIO(source)
            for chunk in pd.read_csv(
                cast(Any, clean_source),
                header=0,
                delimiter=best_sep,
                chunksize=1000,
            ):
                yield chunk
        except Exception as e:
            raise DocumentReadError(f"Severe failure reading CSV: {str(e)}")


class InfracoesXlsInputStream(InputStream[Any, pd.DataFrame]):
    """InputStream for XLS infraction files."""

    def __init__(self):
        self.current_unit_index = 0
        self.total_units = 0

    def read(
        self, source: Any, session: ExtractionSession | None = None
    ) -> Generator[pd.DataFrame, None, None]:
        try:
            data_frame = pd.read_excel(source, header=0)
            yield data_frame
        except Exception as e:
            raise DocumentReadError(
                f"Problema ao processar o arquivo no Load: {source}. {e}"
            )


# ==========================================
# TRANSFORM STREAMS
# ==========================================


class InfracoesTransformStream(TransformStream[pd.DataFrame, list[dict[str, Any]]]):
    """
    Transforms the Infractions DataFrame by formatting columns and dates.
    Accepts date/time formats in the constructor to reuse logic between CSV and XLS.
    """

    def __init__(
        self, datetime_format: str, date_format: str, convert_val_infr: bool = False
    ):
        self.datetime_format = datetime_format
        self.date_format = date_format
        self.convert_val_infr = convert_val_infr
        super().__init__()

    def _parse_date_column(
        self, data_frame: pd.DataFrame, col: str, expected_format: str
    ) -> None:
        if col not in data_frame.columns:
            return

        if pd.api.types.is_datetime64_any_dtype(data_frame[col]):
            return

        raw_series = data_frame[col]
        is_non_empty = raw_series.notna() & (
            ~raw_series.astype(str).str.strip().isin(["", "nan", "None", "NaT"])
        )

        parsed = pd.to_datetime(
            raw_series,
            format=expected_format,
            errors="coerce",
        )

        invalid_mask = is_non_empty & parsed.isna()
        if invalid_mask.any():
            err_row_idx = data_frame[invalid_mask].index[0]
            err_line = err_row_idx + 2
            bad_val = data_frame.loc[err_row_idx, col]
            raise InvalidDocumentDataError(
                f"Erro no arquivo: Campo '{col}' na linha {err_line} possui valor inválido ('{bad_val}'). "
                f"Formato esperado: {expected_format}."
            )

        data_frame[col] = parsed

    def _concatenate_date_and_time(self, data_frame: pd.DataFrame) -> None:
        if "DAT_OCOR_INFR" not in data_frame.columns:
            return

        if "HORA" in data_frame.columns:
            has_date = data_frame["DAT_OCOR_INFR"].notna() & (
                ~data_frame["DAT_OCOR_INFR"]
                .astype(str)
                .str.strip()
                .isin(["", "nan", "None", "NaT"])
            )
            has_hora = data_frame["HORA"].notna() & (
                ~data_frame["HORA"]
                .astype(str)
                .str.strip()
                .isin(["", "nan", "None", "NaT"])
            )
            date_col = data_frame["DAT_OCOR_INFR"].astype(str).str.strip()
            hora_col = data_frame["HORA"].astype(str).str.strip()
            combined = date_col.str.cat(hora_col, sep=" ")
            data_frame["DAT_OCOR_INFR"] = combined.where(has_date & has_hora, None)
            data_frame.drop(columns=["HORA"], inplace=True)
            self._parse_date_column(data_frame, "DAT_OCOR_INFR", self.datetime_format)
        else:
            self._parse_date_column(data_frame, "DAT_OCOR_INFR", self.date_format)

    def _clean_empty_unnamed_columns(self, data_frame: pd.DataFrame) -> pd.DataFrame:
        """Drop columns that have no name/header and contain only empty/null values."""
        unnamed_empty_cols = [
            col
            for col in data_frame.columns
            if (
                str(col).strip().lower().startswith("unnamed:")
                or str(col).strip() == ""
            )
            and (
                data_frame[col].isna()
                | data_frame[col]
                .astype(str)
                .str.strip()
                .isin(["", "nan", "None", "NaT"])
            ).all()
        ]
        if unnamed_empty_cols:
            return data_frame.drop(columns=unnamed_empty_cols)
        return data_frame

    def _clean_blank_and_header_rows(self, data_frame: pd.DataFrame) -> pd.DataFrame:
        """Drop completely blank rows and duplicated header rows."""
        is_blank = data_frame.isna() | data_frame.astype(str).apply(
            lambda col: col.str.strip().isin(["", "nan", "None"])
        )
        data_frame = data_frame[~is_blank.all(axis=1)]

        if "NUM_AI" in data_frame.columns:
            data_frame = data_frame[
                data_frame["NUM_AI"].astype(str).str.strip().str.upper() != "NUM_AI"
            ]
        return data_frame

    def _validate_required_fields(self, data_frame: pd.DataFrame) -> None:
        """Validate that mandatory fields (NUM_AI, DAT_LIMT_RECU) are present and non-empty."""
        if "NUM_AI" in data_frame.columns:
            missing_ai = data_frame[
                data_frame["NUM_AI"].isna()
                | (data_frame["NUM_AI"].astype(str).str.strip() == "")
            ]
            if not missing_ai.empty:
                err_idx = missing_ai.index[0] + 2
                raise InvalidDocumentDataError(
                    f"Erro no arquivo: Campo 'Número do AI' (NUM_AI) está vazio na linha {err_idx}."
                )

        if "DAT_LIMT_RECU" in data_frame.columns:
            missing_dat = data_frame[
                data_frame["DAT_LIMT_RECU"].isna()
                | (data_frame["DAT_LIMT_RECU"].astype(str).str.strip() == "")
            ]
            if not missing_dat.empty:
                err_idx = missing_dat.index[0] + 2
                raise InvalidDocumentDataError(
                    f"Erro no arquivo: Campo 'Data Limite do Recurso' (DAT_LIMT_RECU) está vazio na linha {err_idx}."
                )

    def _normalize_columns(self, data_frame: pd.DataFrame) -> None:
        """Format and convert data types for specific columns (COD_LINH, NOM_LINH, VAL_INFR)."""
        if "COD_LINH" in data_frame.columns:
            data_frame["COD_LINH"] = (
                data_frame["COD_LINH"]
                .fillna("")
                .apply(
                    lambda x: (
                        str(int(x))
                        if isinstance(x, float) and x.is_integer()
                        else (str(x).strip() if pd.notna(x) else "")
                    )
                )
            )

        if "NOM_LINH" in data_frame.columns:
            data_frame["NOM_LINH"] = (
                data_frame["NOM_LINH"].fillna("").astype(str).str.strip()
            )

        if self.convert_val_infr and "VAL_INFR" in data_frame.columns:
            data_frame["VAL_INFR"] = data_frame["VAL_INFR"].map(_parse_val_infr)

    def _parse_dates(self, data_frame: pd.DataFrame) -> None:
        """Parse all date/time columns in the DataFrame."""
        self._concatenate_date_and_time(data_frame=data_frame)
        self._parse_date_column(data_frame, "DAT_EMIS_NOTF", self.date_format)
        self._parse_date_column(data_frame, "DAT_LIMT_RECU", self.date_format)

        if "DAT_CANC" in data_frame.columns and not bool(
            data_frame["DAT_CANC"].isnull().all()
        ):
            self._parse_date_column(data_frame, "DAT_CANC", self.date_format)

    def _to_records(self, data_frame: pd.DataFrame) -> list[dict[str, Any]]:
        """Clean NaN values to None and convert DataFrame to list of dictionaries."""
        cast(Any, data_frame).replace([np.nan], [None], inplace=True)
        return cast(list[dict[str, Any]], data_frame.to_dict(orient="records"))

    def transform(self, data_frame: pd.DataFrame) -> list[dict[str, Any]]:
        try:
            data_frame = self._clean_empty_unnamed_columns(data_frame)
            data_frame = self._clean_blank_and_header_rows(data_frame)

            if data_frame.empty:
                return []

            self._validate_required_fields(data_frame)
            self._normalize_columns(data_frame)
            self._parse_dates(data_frame)

            return self._to_records(data_frame)
        except InvalidDocumentDataError:
            raise
        except Exception as e:
            raise DocumentReadError(f"Erro no transform de Infrações. {e}")


class NoOpTransformStream(TransformStream[Any, Any]):
    """Pass-through TransformStream that forwards chunks unaltered."""

    def transform(self, data: Any) -> Any:
        return data


def normalize_auto_infraction_id(ai: str) -> str:
    if not ai:
        return ai

    if "-" in ai:
        return ai

    if ai[len(ai) - 1] == "-":
        return ai

    return f"{ai[:-1]}-{ai[-1]}"


def _parse_val_infr(value: Any) -> float | None:
    """Convert optional Brazilian currency text into a database-ready number."""
    if pd.isna(value):
        return None

    normalized = str(value).replace("R$", "").strip()
    if not normalized:
        return None
    if "," in normalized:
        normalized = normalized.replace(".", "").replace(",", ".")

    return float(pd.to_numeric(normalized))
