from pathlib import Path
from typing import Any

import pandas as pd


def exportar_excel(dados: list[dict[str, Any]], caminho_saida: str) -> None:
    Path(caminho_saida).parent.mkdir(parents=True, exist_ok=True)
    df = pd.DataFrame(dados)
    df.to_excel(caminho_saida, index=False)
