from Main import df_pipe
import pandas as pd

#--------------------------------

#Empresas e Auxilio (quantitativo e dados)
total_auxilio = (df_pipe["Modalidade de apoio"] != 'Não Informado').sum()
empresas_tipo_auxilio = (df_pipe.loc[df_pipe['Empresa'] != 'Não Informado',['Empresa', 'Modalidade de apoio']].sort_values(by='Modalidade de apoio'))
empresas_quantidade_auxilio_distintos = df_pipe.loc[:,['Empresa', 'Modalidade de apoio']].groupby("Modalidade de apoio")["Empresa"].nunique()
empresas_quantidade_auxilio_total = df_pipe.loc[:,['Empresa', 'Modalidade de apoio']].groupby("Modalidade de apoio").size()

#CSV
empresas_tipo_auxilio.to_csv("../Export_csv/PIPE/Values/empresas_e_modalidade_auxilio.csv", index=False, encoding="utf-8-sig")

total_auxilio_df = pd.DataFrame( {'Total de Modalidades de Apoio Fornecidos': [total_auxilio]})
total_auxilio_df.to_csv("../Export_csv/PIPE/Values/total_modalidade_apoio.csv", index=False, encoding="utf-8-sig")

empresas_quantidade_auxilio_df = empresas_quantidade_auxilio_distintos.reset_index()
empresas_quantidade_auxilio_df.columns = ["Modalidade de apoio", "Total de Empresas Distintas Apoiadas"]
empresas_quantidade_auxilio_df = empresas_quantidade_auxilio_df[empresas_quantidade_auxilio_df["Modalidade de apoio"] != 'Não Informado']
empresas_quantidade_auxilio_df = empresas_quantidade_auxilio_df.sort_values(by="Total de Empresas Distintas Apoiadas", ascending=False)
empresas_quantidade_auxilio_df.to_csv("../Export_csv/PIPE/Values/Apoio_empresas_disitintas.csv", index=False, encoding="utf-8-sig")

empresas_quantidade_auxilio_df = empresas_quantidade_auxilio_total.reset_index()
empresas_quantidade_auxilio_df.columns = ["Modalidade de apoio", "Total de Auxílio Fornecido por Modalidade"]
empresas_quantidade_auxilio_df = empresas_quantidade_auxilio_df[empresas_quantidade_auxilio_df["Modalidade de apoio"] != 'Não Informado']
empresas_quantidade_auxilio_df = empresas_quantidade_auxilio_df.sort_values(by="Total de Auxílio Fornecido por Modalidade", ascending=False)
empresas_quantidade_auxilio_df.to_csv("../Export_csv/PIPE/Values/Apoio_empresas_total.csv", index=False, encoding="utf-8-sig")


#--------------------------------
#Area do conhecimento
empresas_area_geral = df_pipe.loc[df_pipe['Empresa'] != 'Não Informado', ['Empresa', 'Grande Área do Conhecimento', 'Área do Conhecimento', 'Subárea do Conhecimento']]

#CSV
empresas_area_geral.to_csv("../Export_csv/PIPE/Values/empresas_e_areas.csv", index=False, encoding="utf-8-sig")


'-------------------------------------------------------------------------'

# Pesquisa Exterior
pesquisa_exterior = df_pipe.loc[
    (df_pipe['Pesquisador responsável no exterior'] != 'Não Informado') &
    (df_pipe['Instituições no Exterior'] != 'Não Informado') &
    (df_pipe['Título (Inglês)'] != 'Não Informado'),
    ['Título (Inglês)', 'Assuntos', 'Pesquisador responsável no exterior',
     'Instituições no Exterior', 'País Instituição (ões) no Exterior',
     'Empresa', 'Grande Área do Conhecimento', 'Área do Conhecimento', 'Subárea do Conhecimento']
].rename(columns={
    'Título (Inglês)': 'Título',
    'Pesquisador responsável no exterior': 'Pesquisador Responsável no Exterior',
    'Instituições no Exterior': 'Instituição Exterior',
    'País Instituição (ões) no Exterior': 'País',
})

# Pesquisa Cooperação Exterior
pesquisa_cooperacao_exterior = df_pipe.loc[
    (df_pipe['Pesquisador responsável no exterior'] != 'Não Informado') &
    (df_pipe['Instituições no Exterior'] != 'Não Informado') &
    (df_pipe['Título (Inglês)'] != 'Não Informado') &
    (df_pipe['País Acordo(s)/Convênio(s) de Cooperação com a FAPESP'] != 'Brasil') &
    (df_pipe['País Acordo(s)/Convênio(s) de Cooperação com a FAPESP'] != 'Não Informado'),
    ['Título (Inglês)', 'Assuntos', 'Pesquisador responsável no exterior',
     'Instituições no Exterior', 'País Acordo(s)/Convênio(s) de Cooperação com a FAPESP',
     'Empresa', 'Grande Área do Conhecimento', 'Área do Conhecimento', 'Subárea do Conhecimento']
].rename(columns={
    'Título (Inglês)': 'Título',
    'Pesquisador responsável no exterior': 'Pesquisador Responsável no Exterior',
    'Instituições no Exterior': 'Instituição Exterior',
    'País Acordo(s)/Convênio(s) de Cooperação com a FAPESP': 'País (Acordo/Convênio)',
})

# Pesquisa Nacional
pesquisa_nacional = df_pipe.loc[
    (df_pipe['Instituições no Exterior'] == 'Não Informado') &
    (df_pipe['Título'] != 'Não Informado'),
    ['Título', 'Assuntos', 'Pesquisador Responsável', 'Empresa', 'Município',
     'Grande Área do Conhecimento', 'Área do Conhecimento', 'Subárea do Conhecimento']
]

# CSV
pesquisa_exterior.to_csv("../Export_csv/PIPE/Values/pesquisas_exterior.csv", index=False, encoding="utf-8-sig")
pesquisa_cooperacao_exterior.to_csv("../Export_csv/PIPE/Values/pesquisas_cooperacao_exterior.csv", index=False, encoding="utf-8-sig")
pesquisa_nacional.to_csv("../Export_csv/PIPE/Values/pesquisas_nacional.csv", index=False, encoding="utf-8-sig")
#------------------------------
# Pesquisadores

# > Pesquisador Exterior
pesquisador_exterior = df_pipe.loc[
    (df_pipe['Pesquisador responsável no exterior'] != 'Não Informado'),
    ['Pesquisador responsável no exterior', 'País Instituição (ões) no Exterior']
].rename(columns={ 'Pesquisador responsável no exterior': 'Pesquisador Responsável no Exterior','País Instituição (ões) no Exterior': 'País',})

# > Pesquisador Cooperação Exterior
pesquisador_cooperacao_exterior = df_pipe.loc[
    (df_pipe['País Acordo(s)/Convênio(s) de Cooperação com a FAPESP'] != 'Brasil') &
    (df_pipe['País Acordo(s)/Convênio(s) de Cooperação com a FAPESP'] != 'Não Informado'),
    ['Pesquisador Responsável', 'Pesquisador responsável no exterior', 'Pesquisadores Associados', 'País Acordo(s)/Convênio(s) de Cooperação com a FAPESP']
].rename(columns={'País Acordo(s)/Convênio(s) de Cooperação com a FAPESP': 'País (Acordo/Convênio)',})

#  Pesquisador Nacional
pesquisador_nacional = df_pipe.loc[
    (df_pipe['Pesquisador responsável no exterior'] == 'Não Informado') &
    ((df_pipe['Pesquisadores Principais (Atuais)'] != 'Não Informado') |
     (df_pipe['Pesquisadores Principais (Últimos)'] != 'Não Informado') |
     (df_pipe['Pesquisadores Principais (Anteriores)'] != 'Não Informado') |
     (df_pipe['Pesquisadores Associados'] != 'Não Informado')), # Filtro inclui associados
    ['Pesquisador Responsável','Pesquisadores Principais (Atuais)', 'Pesquisadores Principais (Últimos)',
     'Pesquisadores Principais (Anteriores)', 'Pesquisadores Associados', 'Município']].sort_values(by='Município')

# CSV
pesquisador_exterior.to_csv("../Export_csv/PIPE/Values/pesquisadores_exterior.csv", index=False, encoding="utf-8-sig")
pesquisador_cooperacao_exterior.to_csv("../Export_csv/PIPE/Values/pesquisadores_cooperacao_exterior.csv", index=False, encoding="utf-8-sig")
pesquisador_nacional.to_csv("../Export_csv/PIPE/Values/pesquisadores_nacional.csv", index=False, encoding="utf-8-sig")
#------------------------------

# Resumo -> Empresas e Pesquisa
resumo_empresa = df_pipe.loc[
    (df_pipe['Resumo (Português)'].str.lower().str.contains('empresa|indústria|negócio|setor|produto')) &
    (df_pipe['Resumo (Português)'] != 'Não Informado'),
    ['Empresa', 'Título', 'Resumo (Português)']
    ].sort_values(by='Empresa',key=lambda col: (col == 'Não Informado')
    ).rename(columns={
    'Resumo (Português)': 'Resumo'})

#CSV
resumo_empresa.to_csv("../Export_csv/PIPE/Values/resumo_empresas_e_pesquisas.csv",index=False,encoding="utf-8-sig")
