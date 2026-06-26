from pathlib import Path
import logging


def setup_logger() -> None:
    """
    Configura o logger da aplicação.
    """

    Path("logs").mkdir(exist_ok=True)
    logging.basicConfig(
        filename="logs/extracao.log",
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s"
    )


def listar_pdfs(caminho: str) -> list[Path]:
    """
    Lista todos os PDFs na pasta de entrada.
    """

    Path(caminho).mkdir(parents=True, exist_ok=True)
    return list(Path(caminho).glob("*.pdf"))
