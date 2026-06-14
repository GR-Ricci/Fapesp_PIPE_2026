from Main import df_pipe
import pandas as pd
from Def import _extrair_nomes

FILTRO_RP = df_pipe['Município'].str.strip().str.lower() == 'ribeirão preto'
df_rp = df_pipe.loc[FILTRO_RP]

# ------------------------------
# Quantidade Pesquisadores

principais_atuais_rp = df_rp.loc[df_rp['Pesquisadores Principais (Atuais)'] != 'Não Informado', 'Pesquisadores Principais (Atuais)']
principais_ultimos_rp = df_rp.loc[df_rp['Pesquisadores Principais (Últimos)'] != 'Não Informado', 'Pesquisadores Principais (Últimos)']
principais_anteriores_rp = df_rp.loc[df_rp['Pesquisadores Principais (Anteriores)'] != 'Não Informado', 'Pesquisadores Principais (Anteriores)']
pesquisadores_associados_rp = df_rp.loc[df_rp['Pesquisadores Associados'] != 'Não Informado', 'Pesquisadores Associados']

qt_principais_atuais_rp = principais_atuais_rp.pipe(_extrair_nomes).nunique()
qt_principais_ultimos_rp = principais_ultimos_rp.pipe(_extrair_nomes).nunique()
qt_principais_anteriores_rp = principais_anteriores_rp.pipe(_extrair_nomes).nunique()
qt_associados_rp = pesquisadores_associados_rp.pipe(_extrair_nomes).nunique()

total_pesquisadores_principais_rp = pd.concat([principais_atuais_rp, principais_ultimos_rp, principais_anteriores_rp]).pipe(_extrair_nomes).nunique()
total_pesquisadores_responsaveis_rp = df_rp.loc[df_rp['Pesquisador Responsável'] != 'Não Informado','Pesquisador Responsável'].pipe(_extrair_nomes).nunique()

# Total Geral RP (Incluindo Associados)
total_pesquisadores_rp = pd.concat([
    df_rp.loc[df_rp['Pesquisador Responsável'] != 'Não Informado', 'Pesquisador Responsável'],
    pd.concat([principais_atuais_rp, principais_ultimos_rp, principais_anteriores_rp]),
    pesquisadores_associados_rp
]).pipe(_extrair_nomes).nunique()



# Pesquisadores em cooperação com exterior (específico para RP)
mask_coop_rp = (df_rp['País Acordo(s)/Convênio(s) de Cooperação com a FAPESP'] != 'Brasil') & (df_rp['País Acordo(s)/Convênio(s) de Cooperação com a FAPESP'] != 'Não Informado')
total_pesquisadores_cooperacao_exterior_rp = pd.concat([
    df_rp.loc[mask_coop_rp & (df_rp['Pesquisador Responsável'] != 'Não Informado'), 'Pesquisador Responsável'],
    df_rp.loc[mask_coop_rp & (df_rp['Pesquisadores Principais (Atuais)'] != 'Não Informado'), 'Pesquisadores Principais (Atuais)'],
    df_rp.loc[mask_coop_rp & (df_rp['Pesquisadores Principais (Últimos)'] != 'Não Informado'), 'Pesquisadores Principais (Últimos)'],
    df_rp.loc[mask_coop_rp & (df_rp['Pesquisadores Principais (Anteriores)'] != 'Não Informado'), 'Pesquisadores Principais (Anteriores)'],
    df_rp.loc[mask_coop_rp & (df_rp['Pesquisadores Associados'] != 'Não Informado'), 'Pesquisadores Associados']
]).pipe(_extrair_nomes).nunique()

# CSV Pesquisadores RP (Ordem padronizada com o Geral)
csv_pesquisadores_rp = {
    "Pesquisadores": [
        "Total de Pesquisadores (todas categorias)",
        "Pesquisadores Responsáveis",
        "Total de Pesquisadores Principais",
        "Pesquisadores Principais (Atuais)",
        "Pesquisadores Principais (Últimos)",
        "Pesquisadores Principais (Anteriores)",
        "Pesquisadores Associados",
        "Pesquisadores em Projetos com Cooperação Exterior"],
    "Quantidade": [
        total_pesquisadores_rp,
        total_pesquisadores_responsaveis_rp,
        total_pesquisadores_principais_rp,
        qt_principais_atuais_rp,
        qt_principais_ultimos_rp,
        qt_principais_anteriores_rp,
        qt_associados_rp,
        total_pesquisadores_cooperacao_exterior_rp ]}

pd.DataFrame(csv_pesquisadores_rp).to_csv("../Export_csv/PIPE_Ribeirão_Preto/Counts/quantidade_pesquisadores_rp.csv", index=False, encoding="utf-8-sig")

# ------------------------------

# Pesquisas Nacionais (Sem exterior)
quantidade_pesquisas_nacionais_rp = (
    (df_rp['Pesquisador responsável no exterior'] == 'Não Informado') &
    (df_rp['Instituições no Exterior'] == 'Não Informado') &
    (df_rp['Título'] != 'Não Informado')
).sum()

# Pesquisas com Instituições no Exterior (RP)
quantidade_pesquisas_exterior_rp = (
    (df_rp['Instituições no Exterior'] != 'Não Informado') &
    (df_rp['Título'] != 'Não Informado')
).sum()

total_pesquisas_rp = (df_rp['Título'] != 'Não Informado').sum()

csv_pesquisas_rp = {
    "Categoria": [
        "Total de Pesquisas (RP)",
        "Pesquisas Nacionais (RP)",
        "Pesquisas com Instituição no Exterior (RP)"],

    "Quantidade": [
        total_pesquisas_rp,
        quantidade_pesquisas_nacionais_rp,
        quantidade_pesquisas_exterior_rp]}

pd.DataFrame(csv_pesquisas_rp).to_csv("../Export_csv/PIPE_Ribeirão_Preto/Counts/quantidade_pesquisas_rp.csv", index=False, encoding="utf-8-sig")

# -------------------------------------------------------------------------


#Quantidade Empresas
empresas_totais_rp = df_rp.shape[0]
empresas_diferentes_rp = df_rp['Empresa'].nunique()

# CSV Empresas RP
csv_empresas_rp = {
    "Categoria": [
        "Total de Ocorrências de Empresas (RP)",
        "Total de Empresas Distintas (RP)"
    ],
    "Quantidade": [
        empresas_totais_rp,
        empresas_diferentes_rp
    ]
}
pd.DataFrame(csv_empresas_rp).to_csv("../Export_csv/PIPE_Ribeirão_Preto/Counts/quantidade_empresas_rp.csv", index=False, encoding="utf-8-sig")


#Quantidade Empresas por Área do Conhecimento (Distintas)
empresas_rp_grande_area = df_rp[df_rp['Grande Área do Conhecimento'] != 'Não Informado'].groupby("Grande Área do Conhecimento")["Empresa"].nunique().sort_values(ascending=False)
empresas_rp_area = df_rp[df_rp['Área do Conhecimento'] != 'Não Informado'].groupby("Área do Conhecimento")["Empresa"].nunique().sort_values(ascending=False)
empresas_rp_subarea = df_rp[df_rp['Subárea do Conhecimento'] != 'Não Informado'].groupby("Subárea do Conhecimento")["Empresa"].nunique().sort_values(ascending=False)

#Quantidade Empresas por Área do Conhecimento (Total) -
empresas_rp_grande_area_total = df_rp[df_rp['Grande Área do Conhecimento'] != 'Não Informado'].groupby("Grande Área do Conhecimento")["Empresa"].count().sort_values(ascending=False)
empresas_rp_area_total = df_rp[df_rp['Área do Conhecimento'] != 'Não Informado'].groupby("Área do Conhecimento")["Empresa"].count().sort_values(ascending=False)
empresas_rp_subarea_total = df_rp[df_rp['Subárea do Conhecimento'] != 'Não Informado'].groupby("Subárea do Conhecimento")["Empresa"].count().sort_values(ascending=False)

# Contagem de áreas distintas em Ribeirão Preto
qt_grande_area = df_rp[df_rp['Grande Área do Conhecimento'] != 'Não Informado']['Grande Área do Conhecimento'].nunique()
qt_area = df_rp[df_rp['Área do Conhecimento'] != 'Não Informado']['Área do Conhecimento'].nunique()
qt_subarea = df_rp[df_rp['Subárea do Conhecimento'] != 'Não Informado']['Subárea do Conhecimento'].nunique()

# Totais gerais de ocorrências (sem ser distintos)
total_geral_grande_area = df_rp[df_rp['Grande Área do Conhecimento'] != 'Não Informado']['Grande Área do Conhecimento'].count()
total_geral_area = df_rp[df_rp['Área do Conhecimento'] != 'Não Informado']['Área do Conhecimento'].count()
total_geral_subarea = df_rp[df_rp['Subárea do Conhecimento'] != 'Não Informado']['Subárea do Conhecimento'].count()



#Quantidade Empresas por Modalidade de Apoio
empresas_distintas_rp_quantidade_modalidade_apoio = df_rp.groupby("Modalidade de apoio")["Empresa"].nunique()
empresas_rp_quantidade_modalidade_apoio_total = df_rp.groupby("Modalidade de apoio")["Empresa"].count()

#Quantidade Empresas
empresas_rp_quantidade_por_empresa = df_rp['Empresa'].value_counts().reset_index()
empresas_rp_quantidade_por_empresa.columns = ['Empresa', 'Quantidade']

#Quantidade Empresas com cooperação Fapesp Exterior
empresas_cooperacao_exterior = df_pipe.loc[
    (df_pipe['País Acordo(s)/Convênio(s) de Cooperação com a FAPESP'] != 'Brasil') &
    (df_pipe['País Acordo(s)/Convênio(s) de Cooperação com a FAPESP'] != 'Não Informado') &
    (df_pipe['Empresa'] != 'Não Informado'), 'Empresa'].nunique()

#Quantidade Empresas ligadas a projetos no exterior
empresas_instituicao_exterior = df_pipe.loc[
    ((df_pipe['Instituições no Exterior'] != 'Não Informado') |
     ((df_pipe['País Instituição (ões) no Exterior'] != 'Brasil') & (df_pipe['País Instituição (ões) no Exterior'] != 'Não Informado'))) &
    (df_pipe['Empresa'] != 'Não Informado'), 'Empresa'].nunique()

#CSV
empresas_rp_grande_area.to_csv("../Export_csv/PIPE_Ribeirão_Preto/Counts/empresas_rp_grande_area.csv", encoding="utf-8-sig")
empresas_rp_area.to_csv("../Export_csv/PIPE_Ribeirão_Preto/Counts/empresas_rp_area.csv", encoding="utf-8-sig")
empresas_rp_subarea.to_csv("../Export_csv/PIPE_Ribeirão_Preto/Counts/empresas_rp_subarea.csv", encoding="utf-8-sig")

empresas_rp_grande_area_total.to_csv("../Export_csv/PIPE_Ribeirão_Preto/Counts/empresas_rp_grande_area_total.csv", encoding="utf-8-sig")
empresas_rp_area_total.to_csv("../Export_csv/PIPE_Ribeirão_Preto/Counts/empresas_rp_area_total.csv", encoding="utf-8-sig")
empresas_rp_subarea_total.to_csv("../Export_csv/PIPE_Ribeirão_Preto/Counts/empresas_rp_subarea_total.csv", encoding="utf-8-sig")
rp_qt_areas_distintas = pd.DataFrame({"Categoria": ["Grande Área", "Área", "Subárea"],"Quantidade_Distintas": [qt_grande_area, qt_area, qt_subarea]})
rp_qt_areas_distintas.to_csv("../Export_csv/PIPE_Ribeirão_Preto/Counts/rp_qt_areas_distintas.csv", index=False, encoding="utf-8-sig")

empresas_distintas_rp_quantidade_modalidade_apoio.to_csv("../Export_csv/PIPE_Ribeirão_Preto/Counts/empresas_distintas_rp_quantidade_modalidade_apoio.csv", encoding="utf-8-sig")
empresas_rp_quantidade_modalidade_apoio_total.to_csv("../Export_csv/PIPE_Ribeirão_Preto/Counts/empresas_rp_quantidade_modalidade_apoio_total.csv", encoding="utf-8-sig")

empresas_rp_quantidade_por_empresa.to_csv("../Export_csv/PIPE_Ribeirão_Preto/Counts/empresas_rp_quantidade_por_empresa.csv", index=False, encoding="utf-8-sig")

pd.DataFrame({'Descrição': ['Empresas com cooperação FAPESP exterior'], 'Quantidade': [empresas_cooperacao_exterior]}).to_csv(
    "../Export_csv/PIPE/Counts/empresas_cooperacao_exterior.csv", index=False, encoding="utf-8-sig")

pd.DataFrame({'Descrição': ['Empresas ligadas a projetos no exterior'], 'Quantidade': [empresas_instituicao_exterior]}).to_csv(
    "../Export_csv/PIPE/Counts/empresas_instituicao_exterior.csv", index=False, encoding="utf-8-sig")

# Criando o CSV com o resumo dos Totais
rp_totais_areas = pd.DataFrame({"Categoria": ["Grande Área", "Área", "Subárea"],"Total_Ocorrencias": [total_geral_grande_area, total_geral_area, total_geral_subarea]})
rp_totais_areas.to_csv("../Export_csv/PIPE_Ribeirão_Preto/Counts/rp_areas_conhecimento_totais.csv", index=False, encoding="utf-8-sig")

# -------------------------------------------------------------------------
#Assuntos (Ribeirão Preto)
assuntos_valores_rp = df_rp.loc[df_rp['Assuntos'] != 'Não Informado', 'Assuntos'].value_counts()
assuntos_quantidade_rp = df_rp.loc[df_rp['Assuntos'] != 'Não Informado', 'Assuntos'].nunique()

#CSV
assuntos_df_rp = assuntos_valores_rp.reset_index()
assuntos_df_rp.columns = ['Assunto', 'Quantidade']
assuntos_df_rp.to_csv("../Export_csv/PIPE_Ribeirão_Preto/Counts/assuntos_frequencias_rp.csv", index=False, encoding="utf-8-sig")

pd.DataFrame({'Assuntos': ['Total de assuntos distintos (Ribeirão Preto)'], 'Quantidade': [assuntos_quantidade_rp]}).to_csv(
    "../Export_csv/PIPE_Ribeirão_Preto/Counts/assuntos_quantidade_rp.csv", index=False, encoding="utf-8-sig")
# -------------------------------------------------------------------------
