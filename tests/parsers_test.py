import os
import tempfile
import pytest
from docx import Document
from services.parsers import normalize_auto_infraction_id
from services.document_parser.streams import RecursosDocxInputStream
from exceptions.CustomExceptions import ErrDataPubli


def test_normalize_auto_infraction_id():
    assert normalize_auto_infraction_id("12345A") == "12345-A"
    assert normalize_auto_infraction_id("12345-A") == "12345-A"
    assert normalize_auto_infraction_id("1234-") == "1234-"
    assert normalize_auto_infraction_id("") == ""


def test_parse_docx_recursos():
    # Create a temporary DOCX file with expected structure
    with tempfile.NamedTemporaryFile(suffix=".docx", delete=False) as temp_file:
        doc_path = temp_file.name

    try:
        doc = Document()
        # Add publication date paragraph
        doc.add_paragraph("PUBLICADO NO DIARIO OFICIAL DO MUNICIPIO DE BELO HORIZONTE EM 15/05/2026")
        # Add Session/Ata header paragraph
        doc.add_paragraph("ATA DA 5ª SESSÃO ORDINÁRIA")
        
        # Add table
        table = doc.add_table(rows=2, cols=4)
        # Row 0: Headers
        table.cell(0, 0).text = "RECURSO"
        table.cell(0, 1).text = "AUTO DE INFRAÇÃO"
        table.cell(0, 2).text = "RECORRENTE"
        table.cell(0, 3).text = "DECISÃO"
        # Row 1: Valid Data
        table.cell(1, 0).text = "123/2026"
        table.cell(1, 1).text = "345678A"
        table.cell(1, 2).text = "Consórcio BH Leste"
        table.cell(1, 3).text = "IMPROCEDENTE"
        
        doc.save(doc_path)

        # Parse the docx using the new InputStream
        stream = RecursosDocxInputStream(first_instance=True)
        recursos = list(stream.read(doc_path))
        assert len(recursos) == 1
        recurso = recursos[0]
        assert recurso["NUM_RECURSO"] == "123/2026"
        assert recurso["NUM_ATA"] == "5"
        assert recurso["NUM_AI"] == "345678-A"
        assert recurso["NOM_CONC"] == "Consórcio BH Leste"
        assert recurso["RESULTADO"] is False
        assert recurso["DAT_PUBL"] == "2026-05-15 00:00:00"

    finally:
        if os.path.exists(doc_path):
            os.remove(doc_path)


def test_parse_docx_recursos_missing_date():
    with tempfile.NamedTemporaryFile(suffix=".docx", delete=False) as temp_file:
        doc_path = temp_file.name

    try:
        doc = Document()
        doc.add_paragraph("ATA DA 5ª SESSÃO ORDINÁRIA")
        doc.save(doc_path)

        with pytest.raises(ErrDataPubli):
            stream = RecursosDocxInputStream(first_instance=True)
            list(stream.read(doc_path))

    finally:
        if os.path.exists(doc_path):
            os.remove(doc_path)
