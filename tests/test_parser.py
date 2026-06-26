from src.parser import extrair_dados_fatura


def test_extracao_numero():
    texto = """
    Fatura: 12345
    """

    resultado = extrair_dados_fatura(texto)

    assert resultado[0]["Nº Fatura"] == "12345"


def test_extracao_datas_e_valor():
    texto = """
    Emissão 01/06/2026
    Vencimento 15/06/2026
    ICMS: 1.234,56
    850,00 12345678 ((
    """

    resultado = extrair_dados_fatura(texto)

    assert resultado[0]["Dt Emissão Fat"] == "01/06/2026"
    assert resultado[0]["Vencimento Fatura"] == "15/06/2026"
    assert resultado[0]["Valor da Fatura"] == "850,00"
    assert resultado[0]["ICMS/ISS"] == "1.234,56"
