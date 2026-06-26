"""
Testes unitarios basicos para o modulo src.parser.

Executar com:
    pytest
ou
    python -m pytest tests/
"""

import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src import parser


def test_extrair_mes_ano_encontrado():
    texto = "Referente ao periodo de Março 2026 - Fatura mensal"
    assert parser.extrair_mes_ano(texto) == "01/03/2026"


def test_extrair_mes_ano_nao_encontrado():
    texto = "Texto sem nenhuma referencia de mes"
    assert parser.extrair_mes_ano(texto) == "Não identificado"


def test_extrair_despesa_frete_fixo():
    texto = "Descrição: Frete Fixo mensal contratado"
    assert parser.extrair_despesa(texto) == "Frete Fixo"


def test_extrair_despesa_frete_variavel():
    texto = "Cobrança referente a Frete Variável do período"
    assert parser.extrair_despesa(texto) == "Frete Variável"


def test_extrair_despesa_frota_extra():
    texto = "Lançamento de Frota Extra no mês"
    assert parser.extrair_despesa(texto) == "Frota Extra"


def test_extrair_cnpjs():
    texto = "Fornecedor 12.345.678/0001-90 Cliente 98.765.432/0001-10"
    cnpj_ic, cnpj_cliente = parser.extrair_cnpjs(texto)
    assert cnpj_ic == "12.345.678/0001-90"
    assert cnpj_cliente == "98.765.432/0001-10"


def test_extrair_datas():
    texto = "Emissão 01/06/2026 Vencimento 15/06/2026"
    emissao, vencimento = parser.extrair_datas(texto)
    assert emissao == "01/06/2026"
    assert vencimento == "15/06/2026"


def test_extrair_icms():
    texto = "Detalhamento ICMS : 1.234,56 total"
    assert parser.extrair_icms(texto) == "1.234,56"


def test_extrair_faturas():
    texto = "Valor: 1.234,56 1234567 (( outras infos"
    resultado = parser.extrair_faturas(texto)
    assert resultado == [("1.234,56", "1234567")]


def test_montar_centro_e_codigo():
    cnpj_cliente = "12.345.678/0002-29"
    centro_valor, cod_filial = parser.montar_centro_e_codigo(cnpj_cliente)
    assert centro_valor == "4221 - Filial São Paulo"
    assert cod_filial == "2"


def test_montar_centro_e_codigo_vazio():
    centro_valor, cod_filial = parser.montar_centro_e_codigo("")
    assert centro_valor == ""
    assert cod_filial == ""


def test_extrair_filial_por_codigo():
    texto = "Transporte // 4225 - referente ao mes"
    tipo, operacao, filial = parser.extrair_filial(texto)
    assert filial == "4225 - Filial Canoas"
