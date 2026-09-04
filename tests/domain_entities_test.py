from datetime import datetime

import pytest

from classes.AutoInfracao import AutoInfracao
from classes.Linha import Linha
from classes.Operadora import Operadora
from classes.Recurso import RecursoPrimeiraInstancia
from classes.Veiculo import Veiculo
from exceptions.CustomExceptions import ErrUpdateData


def test_linha_domain_methods():
    linha = Linha(
        COD_LINH="61", ID_OPERADORA=107, COMPARTILHADA=False, LINH_ATIV_EMPR=True
    )
    assert linha.is_active() is True
    assert linha.COD_LINH == "61"

    # Deactivation
    dt = datetime(2026, 8, 28, 12, 0, 0)
    linha.deactivate(dt)
    assert linha.is_active() is False
    assert linha.DAT_BAIX == dt

    # Double deactivation should raise ErrUpdateData
    with pytest.raises(ErrUpdateData) as exc:
        linha.deactivate()
    assert exc.value.status == 400

    # Reactivation
    linha.activate()
    assert linha.is_active() is True
    assert linha.DAT_BAIX is None

    # Test getters and setters
    assert linha.get_line_code() == "61"
    assert linha.get_operator_id() == 107
    assert linha.is_shared() is False
    linha.set_shared(True)
    assert linha.is_shared() is True
    assert linha.COMPARTILHADA is True

    # Native Python serialization via dict()
    data = dict(linha)
    assert data["COD_LINH"] == "61"
    assert data["LINH_ATIV_EMPR"] is True
    assert data["DAT_BAIX"] is None
    assert data["COMPARTILHADA"] is True


def test_veiculo_domain_methods():
    veiculo = Veiculo(NUM_VEIC=1111, IDN_PLAC_VEIC="ABC1234", VEIC_ATIV_EMPR=True)
    assert veiculo.is_active() is True

    # Deactivation
    dt = datetime(2026, 8, 28, 14, 0, 0)
    veiculo.deactivate(dt)
    assert veiculo.is_active() is False
    assert veiculo.DAT_BAIX == dt

    # Double deactivation should raise ErrUpdateData
    with pytest.raises(ErrUpdateData) as exc:
        veiculo.deactivate()
    assert exc.value.status == 400

    # Reactivation
    veiculo.activate()
    assert veiculo.is_active() is True
    assert veiculo.DAT_BAIX is None

    # Test getters and setters
    assert veiculo.get_vehicle_number() == 1111
    assert veiculo.get_license_plate() == "ABC1234"
    veiculo.set_license_plate("XYZ9876")
    assert veiculo.get_license_plate() == "XYZ9876"
    assert veiculo.IDN_PLAC_VEIC == "XYZ9876"

    # Native Python serialization via dict()
    data = dict(veiculo)
    assert data["NUM_VEIC"] == 1111
    assert data["IDN_PLAC_VEIC"] == "XYZ9876"
    assert data["VEIC_ATIV_EMPR"] is True


def test_operadora_domain_methods():
    operadora = Operadora(ID=107, NOME="Milenio", CONCESSIONARIA="Pampulha")
    data = dict(operadora)
    assert data == {"ID": 107, "NOME": "Milenio", "CONCESSIONARIA": "Pampulha"}

    # Test getters
    assert operadora.get_id() == 107
    assert operadora.get_name() == "Milenio"
    assert operadora.get_concessionaire() == "Pampulha"

    # Test setters
    operadora.set_name("Milenio Alterado")
    assert operadora.get_name() == "Milenio Alterado"
    assert operadora.NOME == "Milenio Alterado"

    operadora.set_concessionaire("Nova Concessionaria")
    assert operadora.get_concessionaire() == "Nova Concessionaria"
    assert operadora.CONCESSIONARIA == "Nova Concessionaria"


def test_autoinfracao_and_recurso_serialization():
    ai = AutoInfracao(
        NUM_AI="12345-A", VAL_INFR=150.50, DAT_EMIS_NOTF="2026-08-28T10:00:00"
    )
    ai_dict = dict(ai)
    assert ai_dict["NUM_AI"] == "12345-A"
    assert ai_dict["VAL_INFR"] == 150.50
    assert ai_dict["DAT_EMIS_NOTF"] == "2026-08-28T10:00:00"

    rec1 = RecursoPrimeiraInstancia(
        NUM_AI="12345-A", NUM_ATA=5, RESULTADO=True, DAT_PUBL="2026-08-28"
    )
    rec1_dict = dict(rec1)
    assert rec1_dict["NUM_AI"] == "12345-A"
    assert rec1_dict["NUM_ATA"] == 5
    assert rec1_dict["RESULTADO"] is True
    assert rec1_dict["DAT_PUBL"] == "2026-08-28"
