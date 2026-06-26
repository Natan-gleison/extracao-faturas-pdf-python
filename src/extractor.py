from pathlib import Path
import pdfplumber


def extrair_texto_pdf(pdf_path: Path) -> str:
    """
    Extrai todo o texto de um PDF.
    """

    texto = ""

    with pdfplumber.open(pdf_path) as pdf:
        for pagina in pdf.pages:
            pagina_texto = pagina.extract_text()
            if pagina_texto:
                texto += pagina_texto + "\n"

    return texto.strip()
