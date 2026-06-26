"""
parser.py

Contem toda a logica de interpretacao (parsing) do texto extraido das faturas:
identificacao de filial, tipo de operacao, mes de referencia, tipo de despesa,
CNPJs, datas, valores e numero da fatura.
"""

import re
import logging
from typing import Dict, List, Tuple

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Dicionarios de referencia (codigos e nomes de filiais / centros)
# Ajuste estes dicionarios conforme a realidade da sua empresa.
# ---------------------------------------------------------------------------

FILIAIS: Dict[str, str] = {
    "4237": "Filial Simões Filho",
    "4220": "CDC Jaboatão",
    "4225": "Filial Canoas",
    "4227": "Filial Goiânia",
    "4228": "Filial Blumenau",
    "4236": "Filial Chapecó",
    "4223": "Filial Curitiba",
    "4224": "Filial Cambé",
    "4239": "Filial Fortaleza",
    "4234": "Filial Uberaba",
    "4229": "Filial Bauru",
    "4222": "Filial Sertãozinho",
    "4218": "Jundiai H2",
    "4221": "Filial São Paulo",
    "4231": "Filial Macaé",
    "4235": "Filial Vitória",
    "4233": "Filial Juiz de Fora",
    "4219": "CDC Avenida Brasil",
    "4240": "Filial Vale do Aço",
    "4232": "Filial Contagem",
    "4226": "Filial Cuiabá",
    "4246": "ASU Curitiba",
    "4205": "ASU Timoteo",
    "4201": "ASU Rio de Janeiro",
    "4200": "ASU Cubatão",
    "4203": "ASU Salvador",
    "4247": "CO2 JDS/CBT",
    "4242": "BOC Cubatão",
}

# Mapeamento Centro (sufixo do CNPJ) -> "codigo - nome da filial"
CENTRO: Dict[str, str] = {
    "0048-01": "4200 - ASU Cubatão",
    "0065-02": "4201 - ASU Rio de Janeiro",
    "0022-72": "4203 - ASU Salvador",
    "0029-49": "4204 - ASU Resende",
    "0072-31": "4240 - Filial Vale do Aço",
    "0039-10": "4218 - CDC Jundiaí",
    "0040-54": "4209 - H2 Bauru",
    "0034-06": "4219 - CDC Avenida Brasil",
    "0012-09": "4220 - CDC Jaboatão",
    "0002-29": "4221 - Filial São Paulo",
    "0025-15": "4222 - Filial Sertãozinho",
    "0035-97": "4223 - Filial Curitiba",
    "0041-35": "4224 - Filial Cambé",
    "0059-64": "4225 - Filial Canoas",
    "0004-90": "4226 - Filial Cuiabá",
    "0049-92": "4227 - Filial Goiânia",
    "0051-07": "4228 - Filial Blumenau",
    "0057-00": "4229 - Filial Bauru",
    "0054-50": "4231 - Filial Macaé",
    "0016-24": "4232 - Filial Contagem",
    "0017-05": "4233 - Filial Juiz de Fora",
    "0019-77": "4234 - Filial Uberaba",
    "0033-25": "4235 - Filial Vitória",
    "0021-91": "4236 - Filial Chapecó",
    "0009-03": "4237 - Filial Simões Filho",
    "0014-62": "4239 - Filial Fortaleza",
    "0002-74": "4242 - CO2 Cubatão",
    "0066-93": "4246 - ASU Curitiba",
    "0074-01": "4247 - Filial Jandaia do Sul",
    "0001-48": "4214 - Escritório Messer Alphaville",
}

MESES: Dict[str, str] = {
    "janeiro": "01", "fevereiro": "02", "março": "03", "abril": "04",
    "maio": "05", "junho": "06", "julho": "07", "agosto": "08",
    "setembro": "09", "outubro": "10", "novembro": "11", "dezembro": "12",
}


def buscar_filial_por_nome_formatado(texto: str) -> str:
    """
    Tenta identificar a filial a partir do nome mencionado no texto.
    Usado como alternativa quando o codigo numerico nao e encontrado.
    """
    texto_lower = texto.lower()

    if "jandaia do sul" in texto_lower:
        return "4247 - CO2 JDS/CBT"
    if "cdc jundiaí" in texto_lower or "cdc jundiai" in texto_lower:
        return "4218 - CDC Jundiaí"
    if "asu jundiaí" in texto_lower or "asu jundiai" in texto_lower:
        return "4218 - Jundiai H2"
    if "asu santa cruz" in texto_lower:
        return "4201 - ASU Rio de Janeiro"

    for codigo, nome in FILIAIS.items():
        if nome.lower() in texto_lower:
            return f"{codigo} - {nome}"

    return "Não identificado"


def extrair_filial(texto: str) -> Tuple[str, str, str]:
    """
    Identifica o tipo de operacao (BULK/PGP/Outro), a operacao correspondente
    e a filial associada ao texto da fatura.

    Returns:
        Tupla (tipo, operacao, filial_detectada).
    """
    texto_lower = texto.lower()

    tipo = "Outro"
    operacao = "Outro"

    if "bulk" in texto_lower:
        tipo = "BULK"
        operacao = "BULK"
    elif "pgp" in texto_lower or "cilindro" in texto_lower:
        tipo = "PGP"
        operacao = "Suprimento"

    padrao_codigo = r"//\s*(\d{4})\s*-"
    resultado = re.search(padrao_codigo, texto)
    if resultado:
        codigo = resultado.group(1)

        if tipo == "PGP" and codigo == "4218":
            return tipo, operacao, "4218 - CDC Jundiaí"

        nome = FILIAIS.get(codigo)
        if nome:
            return tipo, operacao, f"{codigo} - {nome}"
        return tipo, operacao, "Não identificado"

    filial_nome = buscar_filial_por_nome_formatado(texto)
    return tipo, operacao, filial_nome


def extrair_mes_ano(texto: str) -> str:
    """
    Extrai o mes de referencia da fatura a partir do texto (ex: 'Janeiro 2026').

    Returns:
        Data no formato 'dd/mm/aaaa' (sempre dia 01) ou 'Não identificado'.
    """
    padrao = r"\b(" + "|".join(MESES.keys()) + r")\b\s*(\d{4})"
    resultado = re.search(padrao, texto.lower())
    if resultado:
        mes_extenso, ano = resultado.group(1), resultado.group(2)
        return f"01/{MESES[mes_extenso]}/{ano}"
    return "Não identificado"


def extrair_despesa(texto: str) -> str:
    """
    Classifica o tipo de despesa da fatura (Frete Fixo, Variavel, Frota Extra...).
    """
    texto_lower = texto.lower()

    if "frete fixo" in texto_lower or "fixo" in texto_lower:
        return "Frete Fixo"
    if ("frete variavel" in texto_lower or "frete variável" in texto_lower
            or "variavel" in texto_lower or "variável" in texto_lower):
        return "Frete Variável"
    if "frota extra" in texto_lower:
        return "Frota Extra"

    resultado = re.search(r"REF\s*(.+?)(?=\s{2,}|$)", texto, re.IGNORECASE)
    if resultado:
        return resultado.group(1).strip()

    return "Não identificado"


def extrair_cnpjs(texto: str) -> Tuple[str, str]:
    """
    Extrai os CNPJs presentes no texto.

    Returns:
        Tupla (cnpj_fornecedor, cnpj_cliente). String vazia se nao encontrado.
    """
    cnpjs = re.findall(r"\d{2}\.\d{3}\.\d{3}/\d{4}-\d{2}", texto)
    cnpj_ic = cnpjs[0] if len(cnpjs) > 0 else ""
    cnpj_cliente = cnpjs[1] if len(cnpjs) > 1 else ""
    return cnpj_ic, cnpj_cliente


def extrair_datas(texto: str) -> Tuple[str, str]:
    """
    Extrai a data de emissao e a data de vencimento da fatura.
    """
    data_emissao = re.search(r"Emissão\s*(\d{2}/\d{2}/\d{4})", texto)
    vencimento = re.search(r"Vencimento\s*(\d{2}/\d{2}/\d{4})", texto)
    return (
        data_emissao.group(1) if data_emissao else "",
        vencimento.group(1) if vencimento else "",
    )


def extrair_icms(texto: str) -> str:
    """
    Extrai o valor de ICMS informado na fatura.
    """
    icms = re.search(r"ICMS\s*:\s*(\d{1,3}(?:\.\d{3})*,\d{2})", texto)
    return icms.group(1) if icms else ""


def extrair_faturas(texto: str) -> List[Tuple[str, str]]:
    """
    Extrai todos os pares (valor, numero da fatura) presentes no texto.
    """
    padrao_faturas = r"(\d{1,3}(?:\.\d{3})*,\d{2})\s+(\d{7,8})\s+\(\("
    return re.findall(padrao_faturas, texto)


def montar_centro_e_codigo(cnpj_cliente: str) -> Tuple[str, str]:
    """
    A partir do sufixo do CNPJ do cliente, busca o Centro correspondente
    e deriva o codigo numerico da filial (sem zeros a esquerda).
    """
    if not cnpj_cliente:
        return "", ""

    sufixo_centro = cnpj_cliente.split("/")[-1] if "/" in cnpj_cliente else ""
    centro_valor = CENTRO.get(sufixo_centro, "")
    cod_filial = (
        sufixo_centro.split("-")[0].lstrip("0") if "-" in sufixo_centro else ""
    )
    return centro_valor, cod_filial


def processar_texto_fatura(texto: str) -> List[Dict]:
    """
    Processa o texto completo de um PDF e retorna uma lista de registros
    (um registro por fatura encontrada dentro do documento).
    """
    cnpj_ic, cnpj_cliente = extrair_cnpjs(texto)
    data_emissao, vencimento = extrair_datas(texto)
    icms = extrair_icms(texto)
    faturas_encontradas = extrair_faturas(texto)

    tipo, operacao, filial_detectada = extrair_filial(texto)
    mes_ano = extrair_mes_ano(texto)
    despesa = extrair_despesa(texto)
    centro_valor, cod_filial = montar_centro_e_codigo(cnpj_cliente)

    registros = []
    for valor, num_fatura in faturas_encontradas:
        registros.append({
            "Tipo": tipo,
            "Operação": operacao,
            "Mês": mes_ano,
            "Documento": "Fatura",
            "CNPJ Filial Fatura": cnpj_cliente,
            "Centro": centro_valor,
            "Cód. Filial": cod_filial,
            "CNPJ Fornec.": cnpj_ic,
            "Cód Forn.": "",
            "Fornecedor": "",
            "Contrato": "",
            "Cond. Pgto": "",
            "Despesa": despesa,
            "Unidade Pagadora": filial_detectada,
            "CC": "",
            "Conta Contábil": "",
            "Dt Emissão Fat": data_emissao,
            "Nº Fatura": num_fatura,
            "Vencimento Fatura": vencimento,
            "Venc.  Conf. contrato": "",
            "Valor da Fatura": valor,
            "ICMS/ISS": icms,
        })

    return registros
