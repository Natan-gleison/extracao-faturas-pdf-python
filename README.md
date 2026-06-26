# Extração de Faturas PDF (Python)

Robô em Python para extração automatizada de dados de faturas em PDF (faturas de transporte), com identificação de filial/centro de custo via CNPJ, classificação de tipo de despesa, e exportação consolidada para Excel.

O projeto é totalmente local: não depende de IA externa, API paga ou serviço em nuvem. Toda a extração é feita com `PyMuPDF` (leitura do PDF) e expressões regulares (`re`).

## ✨ Funcionalidades

- Leitura em lote de todos os PDFs de uma pasta de entrada.
- Identificação automática de:
  - Filial / unidade pagadora (por código ou por nome).
  - Tipo de operação (BULK, PGP/Suprimento, Outro).
  - Tipo de despesa (Frete Fixo, Frete Variável, Frota Extra, etc.).
  - CNPJs (fornecedor e cliente), datas de emissão/vencimento, ICMS.
  - Centro de custo e código da filial a partir do CNPJ do cliente.
- Suporte a múltiplas faturas dentro do mesmo PDF.
- Exportação para uma planilha `.xlsx` única, com os valores já convertidos para tipos numéricos/data.
- Cópia dos PDFs processados para a pasta de saída (sufixo ` - IC`).
- Log de execução em arquivo (`logs/execucao.log`), com tratamento de erro por PDF (um arquivo com problema não interrompe o processamento dos demais).

## 📂 Estrutura do projeto

```
extracao-faturas-pdf-python/
│
├── data/
│   ├── input/              # Coloque aqui os PDFs das faturas a processar
│   └── output/              # Pasta com os arquivos gerados (PDFs copiados + Excel)
│
├── logs/
│   └── execucao.log         # Log de cada execução
│
├── src/
│   ├── extractor.py         # Leitura/extração de texto bruto dos PDFs (PyMuPDF)
│   ├── parser.py             # Regras de negócio: regex, dicionários de filiais/centro
│   ├── exporter.py           # Geração do DataFrame e exportação para Excel
│   └── utils.py               # Logging e geração de timestamps
│
├── tests/
│   └── test_parser.py        # Testes unitários (pytest) das regras de parsing
│
├── main.py                    # Ponto de entrada (orquestra todo o fluxo)
├── requirements.txt
└── README.md
```

## 🚀 Como usar

1. Clone o repositório e crie um ambiente virtual (recomendado):

   ```bash
   git clone https://github.com/seu-usuario/extracao-faturas-pdf-python.git
   cd extracao-faturas-pdf-python
   python -m venv .venv
   source .venv/bin/activate      # Windows: .venv\Scripts\activate
   ```

2. Instale as dependências:

   ```bash
   pip install -r requirements.txt
   ```

3. Coloque os PDFs das faturas dentro de `data/input/`.

4. Execute:

   ```bash
   python main.py
   ```

5. Os resultados serão gerados em `data/output/Faturas_Salvas <data-hora>/`:
   - Cópias dos PDFs processados (com sufixo ` - IC`).
   - Um arquivo Excel `Faturas_Extraidas_<data-hora>.xlsx` com todos os dados consolidados.

O andamento da execução fica registrado em `logs/execucao.log`.

## 🧩 Adaptando para o seu cenário

As regras de negócio (códigos de filial, mapeamento de centro de custo, padrões de regex para valor/número de fatura) estão concentradas em `src/parser.py`. Para adaptar o robô a um layout de fatura diferente, normalmente basta:

- Atualizar os dicionários `FILIAIS` e `CENTRO`.
- Ajustar os padrões (`re.search`/`re.findall`) das funções `extrair_*` conforme o texto do seu PDF.

## ✅ Testes

O projeto usa `pytest` para validar as funções de parsing isoladamente (sem precisar de PDFs reais):

```bash
pytest
```

## 🛣️ Possíveis melhorias futuras

- Suporte a configuração externa (YAML/JSON) para os dicionários de filial/centro, em vez de hardcoded no código.
- Validação de schema do Excel de saída.
- Processamento em paralelo para grandes volumes de PDFs.
- Empacotamento como executável (PyInstaller) para uso sem ambiente Python instalado.

## 📄 Licença

Este projeto está disponível sem uma licença definida. Adicione um arquivo `LICENSE` (ex.: MIT) se quiser deixar explícito o uso permitido por terceiros.
