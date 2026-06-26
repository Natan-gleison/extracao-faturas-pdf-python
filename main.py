"""
main.py

Ponto de entrada da aplicacao. Orquestra a leitura dos PDFs de entrada
(data/input), o parsing das faturas e a exportacao dos resultados para
Excel (data/output), registrando todo o processo em logs/execucao.log.
"""

import os
import sys
import logging

# Garante que o pacote `src` seja encontrado independentemente de onde
# o script for chamado.
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(BASE_DIR)

from src import extractor, parser, exporter, utils  # noqa: E402

PASTA_INPUT = os.path.join(BASE_DIR, "data", "input")
PASTA_OUTPUT_RAIZ = os.path.join(BASE_DIR, "data", "output")
PASTA_LOGS = os.path.join(BASE_DIR, "logs")

logger = logging.getLogger(__name__)


def main() -> None:
    timestamp = utils.gerar_timestamp()
    caminho_log = os.path.join(PASTA_LOGS, "execucao.log")
    utils.configurar_logging(caminho_log)

    logger.info("=== Iniciando processamento de faturas ===")
    logger.info("Pasta de entrada: %s", PASTA_INPUT)

    pasta_saida = os.path.join(PASTA_OUTPUT_RAIZ, f"Faturas_Salvas {timestamp}")
    os.makedirs(pasta_saida, exist_ok=True)

    arquivos_pdf = extractor.listar_pdfs(PASTA_INPUT)
    if not arquivos_pdf:
        logger.warning("Nenhum PDF encontrado em '%s'. Encerrando.", PASTA_INPUT)
        print(f"Nenhum PDF encontrado em: {PASTA_INPUT}")
        return

    dados_extraidos = []

    for nome_arquivo in arquivos_pdf:
        caminho_pdf = os.path.join(PASTA_INPUT, nome_arquivo)
        logger.info("Processando: %s", nome_arquivo)

        try:
            texto = extractor.extrair_texto_pdf(caminho_pdf)
            registros = parser.processar_texto_fatura(texto)

            if not registros:
                logger.warning("Nenhuma fatura identificada em: %s", nome_arquivo)
                continue

            dados_extraidos.extend(registros)
            exporter.salvar_copia_pdf(caminho_pdf, pasta_saida, nome_arquivo)

        except Exception:
            logger.exception("Erro ao processar '%s'. Arquivo ignorado.", nome_arquivo)
            continue

    df = exporter.montar_dataframe(dados_extraidos)

    if df.empty:
        logger.warning("Nenhum dado extraido. Excel nao sera gerado.")
        print("Nenhum dado foi extraido dos PDFs processados.")
        return

    nome_excel = f"Faturas_Extraidas_{timestamp}.xlsx"
    caminho_excel = os.path.join(pasta_saida, nome_excel)
    exporter.exportar_excel(df, caminho_excel)

    logger.info("=== Processamento concluido com sucesso ===")
    print(f"PDFs e Excel salvos em: {pasta_saida}")


if __name__ == "__main__":
    main()
