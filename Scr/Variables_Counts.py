from Main import df_pipe
import pandas as pd
from Def import _extrair_nomes

#Quantidade Empresas distintas e suas Areas de Conhecimento (em ordem decrescente)

empresas_grande_area = df_pipe.groupby("Grande Área do Conhecimento")["Empresa"].nunique()
empresas_area = df_pipe.groupby("Área do Conhecimento")["Empresa"].nunique()
empresas_subarea = df_pipe.groupby("Subárea do Conhecimento")["Empresa"].nunique()

#CSV
empresas_grande_area_csv = df_pipe.groupby("Grande Área do Conhecimento")["Empresa"].nunique()
empresas_grande_area_df = empresas_grande_area_csv.reset_index()
empresas_grande_area_df.columns = ["Grande Área do Conhecimento", "Quantidade de Empresas"]
empresas_grande_area_df = empresas_grande_area_df.sort_values(by="Quantidade de Empresas", ascending=False)
empresas_grande_area_df.to_csv("../Export_csv/PIPE/Counts/empresas_grande_area.csv", index=False, encoding="utf-8-sig")

empresas_area_csv = df_pipe.groupby("Área do Conhecimento")["Empresa"].nunique()
empresas_area_df = empresas_area_csv.reset_index()
empresas_area_df.columns = ["Área do Conhecimento", "Quantidade de Empresas"]
empresas_area_df = empresas_area_df.sort_values(by="Quantidade de Empresas", ascending=False)
empresas_area_df.to_csv("../Export_csv/PIPE/Counts/empresas_area.csv", index=False, encoding="utf-8-sig")

# --- NOVO: Top 20 Áreas por Quantidade de Empresas Distintas ---
# empresas_area_df_top20 = empresas_area_df.head(20) # Apenas um comentário lembrando do seu objetivo

empresas_subarea_csv = df_pipe.groupby("Subárea do Conhecimento")["Empresa"].nunique()
empresas_subarea_df = empresas_subarea_csv.reset_index()
empresas_subarea_df.columns = ["Subárea do Conhecimento", "Quantidade de Empresas"]
empresas_subarea_df = empresas_subarea_df.sort_values(by="Quantidade de Empresas", ascending=False)
empresas_subarea_df.to_csv("../Export_csv/PIPE/Counts/empresas_subarea.csv", index=False, encoding="utf-8-sig")

'-------------------------------------------------------------------------'

#Assuntos
assuntos_valores = df_pipe.loc[df_pipe['Assuntos'] != 'Não Informado', 'Assuntos'].value_counts()
assuntos_quantidade = df_pipe.loc[df_pipe['Assuntos'] != 'Não Informado', 'Assuntos'].nunique()

#CSV
assuntos_df = assuntos_valores.reset_index()
assuntos_df.columns = ['Assunto', 'Quantidade']
assuntos_df.to_csv("../Export_csv/PIPE/Counts/assuntos_frequencias.csv", index=False, encoding="utf-8-sig")

pd.DataFrame({'Assuntos': ['Total de assuntos distintos'], 'Quantidade': [assuntos_quantidade]}).to_csv(
    "../Export_csv/PIPE/Counts/assuntos_quantidade.csv", index=False, encoding="utf-8-sig")

'-------------------------------------------------------------------------'
#Quantidade Pesquisadores

pesquisadores_responsaveis = df_pipe.loc[df_pipe['Pesquisador Responsável'] != 'Não Informado','Pesquisador Responsável'].pipe(_extrair_nomes).nunique()

principais_atuais = df_pipe.loc[df_pipe['Pesquisadores Principais (Atuais)'] != 'Não Informado', 'Pesquisadores Principais (Atuais)']
principais_ultimos = df_pipe.loc[df_pipe['Pesquisadores Principais (Últimos)'] != 'Não Informado', 'Pesquisadores Principais (Últimos)']
principais_anteriores = df_pipe.loc[df_pipe['Pesquisadores Principais (Anteriores)'] != 'Não Informado', 'Pesquisadores Principais (Anteriores)']
pesquisadores_associados = df_pipe.loc[df_pipe['Pesquisadores Associados'] != 'Não Informado', 'Pesquisadores Associados']

qt_principais_atuais = principais_atuais.pipe(_extrair_nomes).nunique()
qt_principais_ultimos = principais_ultimos.pipe(_extrair_nomes).nunique()
qt_principais_anteriores = principais_anteriores.pipe(_extrair_nomes).nunique()
qt_associados = pesquisadores_associados.pipe(_extrair_nomes).nunique()

principais_geral = pd.concat([principais_atuais, principais_ultimos, principais_anteriores]).pipe(_extrair_nomes).nunique()

pesquisadores_exterior = df_pipe.loc[df_pipe['Pesquisador responsável no exterior'] != 'Não Informado','Pesquisador responsável no exterior'].pipe(_extrair_nomes).nunique()

total_pesquisadores = pd.concat([
    df_pipe.loc[df_pipe['Pesquisador Responsável'] != 'Não Informado', 'Pesquisador Responsável'],
    pd.concat([principais_atuais, principais_ultimos, principais_anteriores]),
    pesquisadores_associados,
    df_pipe.loc[df_pipe['Pesquisador responsável no exterior'] != 'Não Informado', 'Pesquisador responsável no exterior']
]).pipe(_extrair_nomes).nunique()



#Pesquisadores em cooperacao com exterior
mask_coop = ~df_pipe['País Acordo(s)/Convênio(s) de Cooperação com a FAPESP'].isin(['Brasil', 'Não Informado'])
total_pesquisadores_cooperacao_exterior = pd.concat([
    df_pipe.loc[mask_coop & (df_pipe['Pesquisador Responsável'] != 'Não Informado'), 'Pesquisador Responsável'],
    df_pipe.loc[mask_coop & (df_pipe['Pesquisadores Principais (Atuais)'] != 'Não Informado'), 'Pesquisadores Principais (Atuais)'],
    df_pipe.loc[mask_coop & (df_pipe['Pesquisadores Principais (Últimos)'] != 'Não Informado'), 'Pesquisadores Principais (Últimos)'],
    df_pipe.loc[mask_coop & (df_pipe['Pesquisadores Principais (Anteriores)'] != 'Não Informado'), 'Pesquisadores Principais (Anteriores)'],
    df_pipe.loc[mask_coop & (df_pipe['Pesquisadores Associados'] != 'Não Informado'), 'Pesquisadores Associados']
]).pipe(_extrair_nomes).nunique()

#CSV metrica geral
csv_pesquisadores = {
    "Pesquisadores": [
        "Total de Pesquisadores (todas categorias)",
        "Pesquisadores Responsáveis",
        "Total de Pesquisadores Principais",
        "Pesquisadores Principais (Atuais)",
        "Pesquisadores Principais (Últimos)",
        "Pesquisadores Principais (Anteriores)",
        "Pesquisadores Associados",
        "Pesquisadores Responsáveis no Exterior",
        "Pesquisadores em Projetos com Cooperação Exterior"],
    "Quantidade": [
        total_pesquisadores,
        pesquisadores_responsaveis,
        principais_geral,
        qt_principais_atuais,
        qt_principais_ultimos,
        qt_principais_anteriores,
        qt_associados,
        pesquisadores_exterior,
        total_pesquisadores_cooperacao_exterior ]}

pesquisadores_df = pd.DataFrame(csv_pesquisadores)
pesquisadores_df.to_csv("../Export_csv/PIPE/Counts/quantidade_pesquisadores.csv", index=False, encoding="utf-8-sig")
'-------------------------------------------------------------------------'

#Quantidade Pesquisas

df_validas = df_pipe[df_pipe['Título'] != 'Não Informado']

# 1. Pesquisas no exterior ou nacionais com cooperação exterior
coop_mask = (
    (df_validas['Instituições no Exterior'] != 'Não Informado') |
    (~df_validas['País Instituição (ões) no Exterior'].isin(['Brasil', 'Não Informado'])) |
    (~df_validas['País Acordo(s)/Convênio(s) de Cooperação com a FAPESP'].isin(['Brasil', 'Não Informado']))
)
pesquisas_exterior_e_cooperacao = coop_mask.sum()
pesquisas_nacionais_sem_coop = (~coop_mask).sum()

# 2. Pesquisas com instituição no exterior
inst_mask = (
    (df_validas['Instituições no Exterior'] != 'Não Informado') |
    (~df_validas['País Instituição (ões) no Exterior'].isin(['Brasil', 'Não Informado']))
)
pesquisas_exterior = inst_mask.sum()
pesquisas_nacionais_sem_inst = (~inst_mask).sum()

# 3. Pesquisas Com cooperação no exterior
acordo_mask = ~df_validas['País Acordo(s)/Convênio(s) de Cooperação com a FAPESP'].isin(['Brasil', 'Não Informado'])
pesquisas_cooperacao_pais_exterior = acordo_mask.sum()
pesquisas_nacionais_cooperacao_exterior = (~acordo_mask).sum()
pesquisas_cooperacao = (df_validas['País Acordo(s)/Convênio(s) de Cooperação com a FAPESP'] != 'Não Informado').sum()

# Total de pesquisas válidas
total_pesquisas = len(df_validas)

# CSV
csv_pesquisas = {
    "Pesquisas": [
        "Total de Pesquisas",
        "Pesquisas com Cooperação Exterior (qualquer)",
        "Pesquisas Nacionais (sem cooperação exterior)",
        "Pesquisas com Instituição no Exterior",
        "Pesquisas Nacionais (sem instituição exterior)",
        "Pesquisas com Cooperação FAPESP Exterior (Geral)",
        "Pesquisas com Acordo/Convênio Exterior",
        "Pesquisas Nacionais (sem acordo/convênio exterior)"
    ],
    "Quantidade": [
        total_pesquisas,
        pesquisas_exterior_e_cooperacao,
        pesquisas_nacionais_sem_coop,
        pesquisas_exterior,
        pesquisas_nacionais_sem_inst,
        pesquisas_cooperacao,
        pesquisas_cooperacao_pais_exterior,
        pesquisas_nacionais_cooperacao_exterior
    ]
}


pesquisas_df = pd.DataFrame(csv_pesquisas)
pesquisas_df.to_csv("../Export_csv/PIPE/Counts/quantidade_pesquisas.csv", index=False, encoding="utf-8-sig")

'-------------------------------------------------------------------------'

# --- Auxílios (Modalidade de Apoio) ---

# 1. Geral (Projetos e Empresas Distintas)
df_auxilio_valido = df_pipe[df_pipe['Modalidade de apoio'] != 'Não Informado']
auxilio_geral_projetos = df_auxilio_valido['Modalidade de apoio'].value_counts()
total_geral_projetos = auxilio_geral_projetos.sum()

# Cálculo de Empresas Distintas por Modalidade
auxilio_empresas_distintas = df_auxilio_valido[df_auxilio_valido['Empresa'] != 'Não Informado'].groupby('Modalidade de apoio')['Empresa'].nunique().sort_values(ascending=False)
total_geral_empresas_distintas = df_auxilio_valido.loc[df_auxilio_valido['Empresa'] != 'Não Informado', 'Empresa'].nunique()

# 2. Ribeirão Preto
mask_rp = df_pipe['Município'].str.strip().str.lower() == 'ribeirão preto'
total_rp = df_pipe.loc[mask_rp & (df_pipe['Modalidade de apoio'] != 'Não Informado'), 'Modalidade de apoio'].count()

# 3. Exterior
mask_ext = (df_pipe['Instituições no Exterior'] != 'Não Informado') | (~df_pipe['País Instituição (ões) no Exterior'].isin(['Brasil', 'Não Informado']))
total_ext = df_pipe.loc[mask_ext & (df_pipe['Modalidade de apoio'] != 'Não Informado'), 'Modalidade de apoio'].count()

# 4. Cooperação exterior
mask_coop_aux = ~df_pipe['País Acordo(s)/Convênio(s) de Cooperação com a FAPESP'].isin(['Brasil', 'Não Informado'])
total_coop = df_pipe.loc[mask_coop_aux & (df_pipe['Modalidade de apoio'] != 'Não Informado'), 'Modalidade de apoio'].count()

# 5. Nacional
mask_nac = ~(mask_ext | mask_coop_aux)
total_nac = df_pipe.loc[mask_nac & (df_pipe['Modalidade de apoio'] != 'Não Informado'), 'Modalidade de apoio'].count()

# CSV - Totais por Categoria (Corrigido)
totais_df = pd.DataFrame({
    'Categoria': ['Instituições Exterior', 'Cooperação Exterior', 'Ribeirão Preto', 'Nacional', 'Total Projetos (Geral)', 'Total Empresas Distintas (Geral)'],
    'Quantidade': [total_ext, total_coop, total_rp, total_nac, total_geral_projetos, total_geral_empresas_distintas]
})
totais_df.to_csv("../Export_csv/PIPE/Counts/apoio_totais_categoria.csv", index=False, encoding="utf-8-sig")

# CSV - Detalhamento por tipo
auxilio_geral_projetos.to_csv("../Export_csv/PIPE/Counts/apoio_geral_projetos.csv", header=True)
auxilio_empresas_distintas.to_csv("../Export_csv/PIPE/Counts/apoio_geral_empresas_distintas.csv", header=True)

'-------------------------------------------------------------------------'

#Quantidade Empresas

# Totais originais
empresas_por_cidade = df_pipe.loc[df_pipe['Município'] != 'Não Informado', 'Município'].value_counts()
total_empresas = df_pipe.loc[df_pipe['Município'] != 'Não Informado', 'Empresa'].count()
total_empresas_distintas = df_pipe.loc[df_pipe['Município'] != 'Não Informado', 'Empresa'].nunique()
empresas_cidades_distintas = df_pipe.loc[df_pipe['Município'] != 'Não Informado', 'Município'].nunique()

# Empresas com institution no exterior (Instituições no Exterior ou País Instituição)
empresas_exterior = df_pipe.loc[
    ((df_pipe['Instituições no Exterior'] != 'Não Informado') |
     (df_pipe['País Instituição (ões) no Exterior'] != 'Brasil') &
     (df_pipe['País Instituição (ões) no Exterior'] != 'Não Informado')) &
    (df_pipe['Empresa'] != 'Não Informado'), 'Empresa'
].nunique()

# Empresas com acordo/convênio exterior
empresas_cooperacao = df_pipe.loc[
    (df_pipe['País Acordo(s)/Convênio(s) de Cooperação com a FAPESP'] != 'Brasil') &
    (df_pipe['País Acordo(s)/Convênio(s) de Cooperação com a FAPESP'] != 'Não Informado') &
    (df_pipe['Empresa'] != 'Não Informado'), 'Empresa'
].nunique()

# CSV: cidades e empresas
empresas_por_cidade_csv = df_pipe.loc[df_pipe['Município'] != 'Não Informado'].groupby('Município').size()
empresas_por_cidade_df = empresas_por_cidade_csv.reset_index()
empresas_por_cidade_df.columns = ['Município', 'Quantidade de Empresas']
empresas_por_cidade_df = empresas_por_cidade_df.sort_values(by="Quantidade de Empresas", ascending=False)
empresas_por_cidade_df.to_csv("../Export_csv/PIPE/Counts/cidades_e_empresas.csv", index=False, encoding="utf-8-sig")

# CSV: totais (incluindo as novas métricas)
dados_metricas = {
    "Empresas": [
        "Total de Empresas",
        "Total de Empresas Distintas",
        "Total de Empresas em Cidades Distintas",
        "Empresas com Cooperação no Exterior",
    "Empresas com Instituição no Exterior"],
    "Quantidade": [
        total_empresas,
        total_empresas_distintas,
        empresas_cidades_distintas,
        empresas_cooperacao,
        empresas_exterior]
}

metricas_cidade_df = pd.DataFrame(dados_metricas)
metricas_cidade_df.to_csv("../Export_csv/PIPE/Counts/quantidade_empresa.csv", index=False, encoding="utf-8-sig")

'-------------------------------------------------------------'
#Paises e Municipios com Mais Pesquisas


#paises

paises_inst = df_pipe.loc[~df_pipe['País Instituição (ões) no Exterior'].isin(['Brasil', 'Não Informado']), 'País Instituição (ões) no Exterior']
paises_acordo = df_pipe.loc[~df_pipe['País Acordo(s)/Convênio(s) de Cooperação com a FAPESP'].isin(['Brasil', 'Não Informado']), 'País Acordo(s)/Convênio(s) de Cooperação com a FAPESP']

paises_exterior_qt_pesquisas = pd.concat([paises_inst, paises_acordo]).value_counts().sort_values(ascending=False)

#csv
paises_exterior_qt_pesquisas.to_csv("../Export_csv/PIPE/Counts/paises_exterior_qt_pesquisas.csv",header=True, encoding="utf-8-sig")


#municipios

municipios_brasil_qt_pesquisas = (df_pipe.loc[df_pipe['Município'] != 'Não Informado', 'Município'].value_counts().sort_values(ascending=False))

#csv
municipios_brasil_qt_pesquisas.to_csv("../Export_csv/PIPE/Counts/municipios_brasil_qt_pesquisas.csv",header=True, encoding="utf-8-sig")
