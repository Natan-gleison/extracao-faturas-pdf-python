"""
utils.py

Funcoes auxiliares de uso geral: configuracao de logging e geracao de
timestamps usados na nomenclatura de pastas e arquivos de saida.
"""

import os
import logging
from datetime import datetime


def gerar_timestamp() -> str:
    """
    Retorna o timestamp atual no formato 'dd-mm-aaaa HH-MM'.
    """
    return datetime.now().strftime("%d-%m-%Y %H-%M")


def configurar_logging(caminho_log: str) -> None:
    """
    Configura o logging da aplicacao para gravar em arquivo e exibir no console.

    Args:
        caminho_log: Caminho completo do arquivo de log (ex: logs/execucao.log).
    """
    os.makedirs(os.path.dirname(caminho_log), exist_ok=True)

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
        handlers=[
            logging.FileHandler(caminho_log, encoding="utf-8"),
            logging.StreamHandler(),
        ],
        force=True,
    )
