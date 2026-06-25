# extracao-faturas-pdf-python


-- Extração de Faturas PDF com Python --

Automação para extração, tratamento e consolidação de dados de faturas em PDF utilizando Python. O projeto foi desenvolvido com foco em ganho de produtividade, redução de atividades manuais e aumento da confiabilidade dos dados para análises e tomada de decisão.



-- Case de Negócio --

Este projeto simula um cenário real de operações logísticas onde analistas precisam consolidar informações de dezenas ou centenas de faturas mensalmente.

A automação reduz o tempo gasto com atividades operacionais, aumenta a qualidade dos dados e disponibiliza informações estruturadas para análises estratégicas.



-- Sobre o Projeto --

Em muitas operações logísticas e financeiras, informações importantes ficam armazenadas em arquivos PDF, exigindo digitação manual para consolidação e análise.

Este projeto automatiza esse processo através da leitura de múltiplas faturas PDF, extração dos dados relevantes, tratamento das informações e geração de uma base estruturada em Excel para posterior utilização em ferramentas de análise como Power BI.



-- Objetivos --

Automatizar a leitura de faturas PDF.
Extrair informações relevantes de forma estruturada.
Reduzir erros manuais de digitação.
Consolidar dados em uma única base.
Disponibilizar informações para análise e criação de dashboards.



-- Funcionalidades --

. Leitura automática de múltiplos PDFs

. Extração de dados através de Regex

. Tratamento e padronização dos dados

. Consolidação em DataFrame Pandas

. Exportação para Excel

. Registro de logs de execução

. Estrutura modular e escalável



-- Informações Extraídas --

O sistema pode extrair campos como:

. Campo	Descrição
. Número da Fatura	Identificação da fatura
. Data de Emissão	Data de emissão do documento
. Valor do Frete	Valor cobrado pelo transporte
. ICMS	Valor do imposto
. Valor da Mercadoria	Valor total da carga
. Remetente	Empresa remetente
. Destinatário	Empresa destinatária
. CNPJ	Documento da empresa
. Cidade de Origem	Local de embarque
. Cidade de Destino	Local de entrega


-- Tecnologias Utilizadas --

Python 3.12+
Pandas
PDFPlumber
Regex (re)
OpenPyXL
Logging
Pathlib

-- Estrutura do Projeto --

extracao-faturas-pdf-python/
│
├── data/
│   ├── input/
│   │   └── PDFs de entrada
│   │
│   └── output/
│       └── Arquivos gerados
│
├── logs/
│   └── execucao.log
│
├── src/
│   ├── extractor.py
│   ├── parser.py
│   ├── exporter.py
│   └── utils.py
│
├── tests/
│
├── main.py
├── requirements.txt
├── README.md
└── .gitignore


-- Instalação --

Clone o repositório:

git clone https://github.com/seu-usuario/extracao-faturas-pdf-python.git

Entre na pasta:

cd extracao-faturas-pdf-python

Crie um ambiente virtual:

python -m venv venv

Ative o ambiente:

Windows
venv\Scripts\activate
Linux / Mac
source venv/bin/activate

Instale as dependências:

pip install -r requirements.txt


▶️ Como Executar

Coloque os PDFs na pasta:
data/input/
Execute:
python main.py
O arquivo consolidado será gerado em:
data/output/


📈 Fluxo do Processo

PDFs
   │
   ▼
Leitura dos Arquivos
   │
   ▼
Extração de Texto
   │
   ▼
Identificação dos Campos
   │
   ▼
Tratamento dos Dados
   │
   ▼
Consolidação
   │
   ▼
Excel Final


-- Possíveis Aplicações

Controle de fretes
Auditoria de faturas
Conferência de cobranças
Consolidação financeira
Integração com Power BI
Indicadores logísticos


🔮 Próximas Melhorias

Interface gráfica com Streamlit
Banco de dados SQLite
Dashboard Power BI integrado
Processamento automático de e-mails
API para upload de documentos
OCR para PDFs escaneados
Inteligência Artificial para layouts variados

-- Exemplo de Saída

Número	Data	Frete
12345	01/06/2026	R$ 850,00
12346	02/06/2026	R$ 920,00


👨‍💻 Autor

Natan Gleison

Analista de Dados com experiência em:

B.I
Dashboards
Automação de Processos
Power Automate
Python para Análise de Dados

LinkedIn: (https://www.linkedin.com/in/natan-silva-3a14b6262/)

GitHub: Adicionar seu perfil
