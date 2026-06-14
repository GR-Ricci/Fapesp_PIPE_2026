from Main import df_pipe

FILTRO_RP = df_pipe['Município'].str.strip().str.lower() == 'ribeirão preto'
df_rp = df_pipe.loc[FILTRO_RP]

#------------------------------
#Empresas e Áreas de Conhecimento
empresas_rp_categorizado = df_rp.loc[:, [
    'Empresa',
    'Grande Área do Conhecimento',
    'Área do Conhecimento',
    'Subárea do Conhecimento'
]].sort_values(by='Grande Área do Conhecimento')

#Empresas e Modalidade de Apoio
empresas_rp_tipo_auxilio = df_rp.loc[:, ['Empresa', 'Modalidade de apoio']].sort_values(by='Modalidade de apoio')

# Pesquisadores (Principais, Responsáveis e Associados) - Ribeirão Preto
pesquisador_rp = df_rp.loc[
    (df_rp['Pesquisador Responsável'] != 'Não Informado') |
    (df_rp['Pesquisadores Principais (Atuais)'] != 'Não Informado') |
    (df_rp['Pesquisadores Principais (Últimos)'] != 'Não Informado') |
    (df_rp['Pesquisadores Principais (Anteriores)'] != 'Não Informado') |
    (df_rp['Pesquisadores Associados'] != 'Não Informado'),
    ['Pesquisador Responsável', 'Pesquisadores Principais (Atuais)', 'Pesquisadores Principais (Últimos)',
     'Pesquisadores Principais (Anteriores)', 'Pesquisadores Associados']
]

#Pesquisas Nacionais (RP)
pesquisa_rp = df_rp.loc[
    (df_rp['Instituições no Exterior'] == 'Não Informado') &
    (df_rp['Título'] != 'Não Informado'),
    ['Título','Assuntos','Pesquisador Responsável','Empresa','Grande Área do Conhecimento','Área do Conhecimento','Subárea do Conhecimento']]

#Resumo -> Empresas e Pesquisa
resumo_empresa_rp = df_rp.loc[
    (df_rp['Resumo (Português)'].str.lower().str.contains('empresa|indústria|negócio|setor|produto')) &
    (df_rp['Resumo (Português)'] != 'Não Informado'),
    ['Empresa', 'Título', 'Resumo (Português)']
    ].sort_values(
    by='Empresa',
    key=lambda col: (col == 'Não Informado')
    ).rename(columns={'Resumo (Português)': 'Resumo'})


# Ribeirão Preto com projeto no exterior
mask_rp = df_pipe['Município'].str.strip().str.lower() == 'ribeirão preto'
mask_inst = (
    ((df_pipe['País Instituição (ões) no Exterior'] != 'Brasil') &
     (df_pipe['País Instituição (ões) no Exterior'] != 'Não Informado')) |
    (df_pipe['Instituições no Exterior'] != 'Não Informado')
)
empresas_rp_projeto_exterior = df_pipe.loc[mask_rp & mask_inst].copy()

colunas_exterior = [
    'Título', 'Assuntos', 'Área do Conhecimento', 'Empresa', 'Município',
    'País Instituição (ões) no Exterior', 'Pesquisador Responsável',
    'Pesquisador responsável no exterior', 'Pesquisadores Principais (Atuais)',
    'Pesquisadores Principais (Últimos)', 'Pesquisadores Principais (Anteriores)',
    'Pesquisadores Associados', 'Resumo (Português)'
]

#CSV
empresas_rp_categorizado.to_csv("../Export_csv/PIPE_Ribeirão_Preto/Values/empresas_rp_categorizado.csv", index=False, encoding="utf-8-sig")
empresas_rp_tipo_auxilio.to_csv("../Export_csv/PIPE_Ribeirão_Preto/Values/empresas_rp_tipo_auxilio.csv", index=False, encoding="utf-8-sig")
pesquisador_rp.to_csv("../Export_csv/PIPE_Ribeirão_Preto/Values/pesquisadores_rp.csv", index=False, encoding="utf-8-sig")
pesquisa_rp.to_csv("../Export_csv/PIPE_Ribeirão_Preto/Values/pesquisas_rp.csv", index=False, encoding="utf-8-sig")
resumo_empresa_rp.to_csv("../Export_csv/PIPE_Ribeirão_Preto/Values/resumo_empresas_e_pesquisas_rp.csv", index=False, encoding="utf-8-sig")
empresas_rp_projeto_exterior[colunas_exterior].to_csv("../Export_csv/PIPE_Ribeirão_Preto/Values/empresas_rp_projeto_exterior.csv",index=False, encoding="utf-8-sig")
