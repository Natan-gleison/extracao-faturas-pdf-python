import fitz  # PyMuPDF
import pandas as pd
import re
import os
from datetime import datetime
import shutil


agora = datetime.now().strftime("%d-%m-%Y %H-%M")

# Caminho da pasta
pasta_pdfs = r"C:\Users\br02c2\Downloads\faturas"
#pasta_pdfs = r"C:\Users\NATANGLEISONDASILVA\Downloads\faturas"

dados_extraidos = []

# Dicionário de códigos e nomes de filiais
filiais = {
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
    "4242": "BOC Cubatão"
}

centro = {
    "0048-01": "4200 - ASU Cubatão",
    "0065-02": "4201 - ASU Rio de Janeiro",
    "0022-72": "4203 - ASU Salvador",
    "0029-49": "4204 - ASU Resende",
    "0072-31": "4205 - ASU Timóteo",
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
    "0072-31": "4240 - Filial Vale do Aço",
    "0002-74": "4242 - CO2 Cubatão",
    "0066-93": "4246 - ASU Curitiba",
    "0074-01": "4247 - Filial Jandaia do Sul",
    "0001-48": "4214 - Escritório Messer Alphaville"
}


# Busca por nome se código não for encontrado
def buscar_filial_por_nome_formatado(texto):
    texto_lower = texto.lower()

    if "jandaia do sul" in texto_lower:
        return "4247 - CO2 JDS/CBT"
    if "cdc jundiaí" in texto_lower or "cdc jundiai" in texto_lower:
        return "4218 - CDC Jundiaí"
    if "asu jundiaí" in texto_lower or "asu jundiai" in texto_lower:
        return "4218 - Jundiai H2"
    if "asu santa cruz" in texto_lower:
        return "4201 - ASU Rio de Janeiro"

    for codigo, nome in filiais.items():
        if nome.lower() in texto_lower:
            return f"{codigo} - {nome}"

    return "Não identificado"

# Agora retorna também tipo e operação
def extrair_filial(texto):
    texto_lower = texto.lower()

    # Detectar tipo e operação
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

        nome = filiais.get(codigo)
        if nome:
            return tipo, operacao, f"{codigo} - {nome}"
        else:
            return tipo, operacao, "Não identificado"

    # Se não encontrar código, busca por nome
    filial_nome = buscar_filial_por_nome_formatado(texto)
    return tipo, operacao, filial_nome

def extrair_mes_ano(texto):
    meses = {
        "janeiro": "01", "fevereiro": "02", "março": "03", "abril": "04",
        "maio": "05", "junho": "06", "julho": "07", "agosto": "08",
        "setembro": "09", "outubro": "10", "novembro": "11", "dezembro": "12"
    }

    padrao = r"\b(" + "|".join(meses.keys()) + r")\b\s*(\d{4})"
    resultado = re.search(padrao, texto.lower())
    if resultado:
        mes_extenso = resultado.group(1)
        ano = resultado.group(2)
        mes = meses[mes_extenso]
        return f"01/{mes}/{ano}"
    return "Não identificado"

def extrair_despesa(texto):
    texto_lower = texto.lower()

    if "frete fixo" in texto_lower or "fixo" in texto_lower:
        return "Frete Fixo"
    elif "frete variavel" in texto_lower or "frete variável" in texto_lower or "variavel" in texto_lower or "variável" in texto_lower:
        return "Frete Variável"
    elif "frota extra" in texto_lower:
        return "Frota Extra"
    
    resultado = re.search(r"REF\s*(.+?)(?=\s{2,}|$)", texto, re.IGNORECASE)
    if resultado:
        return resultado.group(1).strip()

    return "Não identificado"


# Criar pasta com data e hora
pasta_faturas = os.path.join(pasta_pdfs, f"Faturas_Salvas {agora}")
os.makedirs(pasta_faturas, exist_ok=True)

# Loop pelos PDFs
for nome_arquivo in os.listdir(pasta_pdfs):
    if nome_arquivo.lower().endswith(".pdf"):
        caminho_pdf = os.path.join(pasta_pdfs, nome_arquivo)
        doc = fitz.open(caminho_pdf)

        texto_completo = ""
        for page in doc:
            texto_completo += page.get_text()

        doc.close()
        texto = texto_completo.replace("\n", " ").replace("\u200b", "").strip()

        # CNPJs
        cnpjs = re.findall(r"\d{2}\.\d{3}\.\d{3}/\d{4}-\d{2}", texto)
        cnpj_ic = cnpjs[0] if len(cnpjs) > 0 else ""
        cnpj_cliente = cnpjs[1] if len(cnpjs) > 1 else ""

        # Datas
        data_emissao = re.search(r"Emissão\s*(\d{2}/\d{2}/\d{4})", texto)
        vencimento = re.search(r"Vencimento\s*(\d{2}/\d{2}/\d{4})", texto)

        # ICMS
        icms = re.search(r"ICMS\s*:\s*(\d{1,3}(?:\.\d{3})*,\d{2})", texto)

        # Faturas
        padrao_faturas = r"(\d{1,3}(?:\.\d{3})*,\d{2})\s+(\d{7,8})\s+\(\("
        faturas_encontradas = re.findall(padrao_faturas, texto)

        # Extrações principais
        tipo, operacao, filial_detectada = extrair_filial(texto)
        mes_ano = extrair_mes_ano(texto)
        despesa = extrair_despesa(texto)

        # Preencher o campo Centro usando o dicionário centro e o sufixo do CNPJ do cliente
        if cnpj_cliente:
            sufixo_centro = cnpj_cliente.split("/")[-1] if "/" in cnpj_cliente else ""
            centro_valor = centro.get(sufixo_centro, "")
                    # Preencher o campo Cód. Filial com o número antes do '-' sem zeros à esquerda
            cod_filial = sufixo_centro.split('-')[0].lstrip('0') if '-' in sufixo_centro else ""
        else:
            centro_valor = ""
            cod_filial = ""

        for valor, num_fatura in faturas_encontradas:
            dados_extraidos.append({
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
                "Dt Emissão Fat": data_emissao.group(1) if data_emissao else "",
                "Nº Fatura": num_fatura,
                "Vencimento Fatura": vencimento.group(1) if vencimento else "",
                "Venc.  Conf. contrato": "",
                "Valor da Fatura": valor,
                "ICMS/ISS": icms.group(1) if icms else ""
            })


            # Salvar cópia do PDF com "- IC"
            nome_novo_pdf = os.path.splitext(nome_arquivo)[0] + " - IC.pdf"
            caminho_novo_pdf = os.path.join(pasta_faturas, nome_novo_pdf)
            shutil.copy2(caminho_pdf, caminho_novo_pdf)

# Exportar para Excel
df = pd.DataFrame(dados_extraidos)
df["Mês"] = pd.to_datetime(df["Mês"], format="%d/%m/%Y", errors='coerce')


# Converter valores para número
df["Valor da Fatura"] = (
    df["Valor da Fatura"]
    .str.replace(".", "", regex=False)  # remove milhar
    .str.replace(",", ".", regex=False)  # vírgula -> ponto
    .astype(float)
)

df["ICMS/ISS"] = (
    df["ICMS/ISS"]
    .str.replace(".", "", regex=False)  # remove milhar
    .str.replace(",", ".", regex=False)  # vírgula -> ponto
    .astype(float)
)

df["Nº Fatura"] = (
    df["Nº Fatura"]
    .astype(int)
)
df["Cód. Filial"] = pd.to_numeric(df["Cód. Filial"], errors='coerce')

df = df.drop_duplicates()

# Nome do Excel com timestamp
nome_excel = f"Faturas_Extraidas_{agora}.xlsx"
caminho_excel = os.path.join(pasta_faturas, nome_excel)
df.to_excel(caminho_excel, index=False)

print(f"PDFs e Excel salvos em: {pasta_faturas}")
