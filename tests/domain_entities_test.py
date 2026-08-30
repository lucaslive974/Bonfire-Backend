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
    assert linha.esta_ativa() is True
    assert linha.COD_LINH == "61"

    # Desativação
    dt = datetime(2026, 8, 28, 12, 0, 0)
    linha.desativar(dt)
    assert linha.esta_ativa() is False
    assert linha.DAT_BAIX == dt

    # Desativação dupla deve lançar ErrUpdateData
    with pytest.raises(ErrUpdateData) as exc:
        linha.desativar()
    assert exc.value.status == 400

    # Reativação
    linha.ativar()
    assert linha.esta_ativa() is True
    assert linha.DAT_BAIX is None

    # Serialização pythônica nativa via dict()
    data = dict(linha)
    assert data["COD_LINH"] == "61"
    assert data["LINH_ATIV_EMPR"] is True
    assert data["DAT_BAIX"] is None


def test_veiculo_domain_methods():
    veiculo = Veiculo(NUM_VEIC=1111, IDN_PLAC_VEIC="ABC1234", VEIC_ATIV_EMPR=True)
    assert veiculo.esta_ativo() is True

    # Desativação
    dt = datetime(2026, 8, 28, 14, 0, 0)
    veiculo.desativar(dt)
    assert veiculo.esta_ativo() is False
    assert veiculo.DAT_BAIX == dt

    # Desativação dupla deve lançar ErrUpdateData
    with pytest.raises(ErrUpdateData) as exc:
        veiculo.desativar()
    assert exc.value.status == 400

    # Reativação
    veiculo.ativar()
    assert veiculo.esta_ativo() is True
    assert veiculo.DAT_BAIX is None

    # Serialização pythônica nativa via dict()
    data = dict(veiculo)
    assert data["NUM_VEIC"] == 1111
    assert data["IDN_PLAC_VEIC"] == "ABC1234"
    assert data["VEIC_ATIV_EMPR"] is True


def test_operadora_domain_methods():
    operadora = Operadora(ID=107, NOME="Milenio", CONCESSIONARIA="Pampulha")
    data = dict(operadora)
    assert data == {"ID": 107, "NOME": "Milenio", "CONCESSIONARIA": "Pampulha"}

    operadora.atualizar({"NOME": "Milenio Alterado"})
    assert operadora.NOME == "Milenio Alterado"


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
