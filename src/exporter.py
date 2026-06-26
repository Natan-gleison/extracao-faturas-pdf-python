"""
exporter.py

Responsavel por salvar copias dos PDFs processados e exportar os dados
extraidos para um arquivo Excel (.xlsx).
"""

import os
import shutil
import logging
from typing import List, Dict

import pandas as pd

logger = logging.getLogger(__name__)


def salvar_copia_pdf(caminho_pdf: str, pasta_destino: str, nome_arquivo: str) -> None:
    """
    Salva uma copia do PDF original na pasta de saida, com o sufixo ' - IC'.
    """
    os.makedirs(pasta_destino, exist_ok=True)
    nome_novo_pdf = os.path.splitext(nome_arquivo)[0] + " - IC.pdf"
    caminho_novo_pdf = os.path.join(pasta_destino, nome_novo_pdf)
    try:
        shutil.copy2(caminho_pdf, caminho_novo_pdf)
    except Exception as exc:
        logger.error("Falha ao copiar PDF '%s': %s", nome_arquivo, exc)


def montar_dataframe(dados: List[Dict]) -> pd.DataFrame:
    """
    Constroi o DataFrame final a partir dos registros extraidos, aplicando
    as conversoes de tipo (datas, valores numericos) e removendo duplicatas.
    """
    df = pd.DataFrame(dados)

    if df.empty:
        logger.warning("Nenhum dado foi extraido dos PDFs.")
        return df

    df["Mês"] = pd.to_datetime(df["Mês"], format="%d/%m/%Y", errors="coerce")

    for coluna in ("Valor da Fatura", "ICMS/ISS"):
        df[coluna] = (
            df[coluna]
            .str.replace(".", "", regex=False)  # remove separador de milhar
            .str.replace(",", ".", regex=False)  # virgula -> ponto decimal
            .astype(float)
        )

    df["Nº Fatura"] = df["Nº Fatura"].astype(int)
    df["Cód. Filial"] = pd.to_numeric(df["Cód. Filial"], errors="coerce")

    df = df.drop_duplicates()
    return df


def exportar_excel(df: pd.DataFrame, caminho_excel: str) -> None:
    """
    Exporta o DataFrame para um arquivo Excel (.xlsx).
    """
    os.makedirs(os.path.dirname(caminho_excel), exist_ok=True)
    df.to_excel(caminho_excel, index=False)
    logger.info("Excel exportado em: %s", caminho_excel)
