"""
extractor.py

Responsavel pela extracao do texto bruto dos arquivos PDF de faturas.
Utiliza a biblioteca PyMuPDF (fitz) para abrir e ler o conteudo de cada PDF.
"""

import os
import logging
from typing import List

import fitz  # PyMuPDF

logger = logging.getLogger(__name__)


def listar_pdfs(pasta: str) -> List[str]:
    """
    Lista todos os arquivos PDF presentes em uma pasta.

    Args:
        pasta: Caminho da pasta a ser analisada.

    Returns:
        Lista com os nomes dos arquivos .pdf encontrados (ordem alfabetica).
    """
    if not os.path.isdir(pasta):
        logger.warning("Pasta de entrada nao encontrada: %s", pasta)
        return []

    arquivos = sorted(
        nome for nome in os.listdir(pasta)
        if nome.lower().endswith(".pdf")
    )
    logger.info("Encontrados %d arquivo(s) PDF em '%s'.", len(arquivos), pasta)
    return arquivos


def extrair_texto_pdf(caminho_pdf: str) -> str:
    """
    Abre um arquivo PDF e extrai todo o texto contido nele.

    Args:
        caminho_pdf: Caminho completo do arquivo PDF.

    Returns:
        Texto extraido, com quebras de linha removidas e espacos normalizados.

    Raises:
        Exception: caso o PDF nao possa ser aberto/lido pelo PyMuPDF.
    """
    texto_completo = ""
    try:
        with fitz.open(caminho_pdf) as doc:
            for pagina in doc:
                texto_completo += pagina.get_text()
    except Exception as exc:
        logger.error("Falha ao abrir/ler o PDF '%s': %s", caminho_pdf, exc)
        raise

    texto = texto_completo.replace("\n", " ").replace("\u200b", "").strip()
    return texto
