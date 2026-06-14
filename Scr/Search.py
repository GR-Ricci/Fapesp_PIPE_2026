import pandas as pd
from Path import pipe_path
from Main import df_pipe
from Def import _extrair_nomes


pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', None)
df_pipe_subset = df_pipe

#---- Pesquisas simples para informações uteis  ----#

'Resultados:'

# Valores Nulos
"""
    > Totalmente nulos (7 colunas)
    Cidade Instituição                                       5716
    Instituição                                              5716
    Instituição Parceira                                     5716
    Supervisor                                               5716
    Pesquisador Visitante                                    5716
    Instituição do Pesquisador Visitante                     5716
    Local de Pesquisa                                        5716

    > Altas quantidades de nulos
    Subárea do Conhecimento                                  1251
    Título (Inglês)                                          1424
    Município                                                2269
    Processos Vinculados                                     2967
    Resumo (Inglês)                                          3140
    Pesquisadores Associados                                 4416
    Acordo(s)/Convênio(s) de Cooperação com a FAPESP         4901
    País Acordo(s)/Convênio(s) de Cooperação com a FAPESP    4901
    Pesquisadores Principais (últimos)                       5137
    Pesquisadores Principais (Anteriores)                    5524
    Pesquisadores Principais (atuais)                        5640

    > Poucos Nulos
    Beneficiário                                                1
    Pesquisador Responsável                                     1
    Resumo (Português)                                          2
    Assuntos                                                   12
    Empresa                                                   181
    Área do Conhecimento                                      332
    
     > Exterior (Nulos não importam) -> 8 dados viaveis de exterior
    Instituições no Exterior                                  5708 nulos / 8 viaveis 
    Paísinstituição (ões) no Exterior                         5708 nulos/ 8 viaveis
    Pesquisador responsável no exterior                       5708 nulos / 8 viaveis
    País Acordo(s)/Convênio(s) de Cooperação com a FAPESP     4901 nulos/ 17 viaveis (e 798 sobre brasil)
"""

# Quantitativas
"""
Colunas ligadas a ribeirao preto 
-> Título (Português) / Título (Inglês) / Município / Assuntos / Resumo (Português) /Resumo (Inglês) / Título

Empresas de ribeirão que usam a modalidade de apoio 
-> 194 empresas usam apoio

Empresas unicas em ribeirão preto 
-> 90

Total de projetos em ribeirão preto 
-> 194

Total de empresas e projetos no exterior: 
-> 6 empresas -> Canadá (17), organizações multinacionais (4), Alemanha(2), Espanha (1), Portugal com Itália (1)
"""

# Tabela de Valores quantitativos e Informativos
""" 
-- Dados Gerais:

print(df_pipe_subset['Área do Conhecimento'].value_counts().head(20))
print(df_pipe_subset['Subárea do Conhecimento'].value_counts())
print(df_pipe_subset['Município'].value_counts())
print(df_pipe_subset['Empresa'].value_counts())
print(df_pipe_subset['Acordo(s)/Convênio(s) de Cooperação com a FAPESP'].value_counts())
print(df_pipe_subset['País Acordo(s)/Convênio(s) de Cooperação com a FAPESP'].value_counts())

print(df_pipe_subset['País Instituição (ões) no Exterior'].value_counts())
print(df_pipe['Resumo (Português)'].head())

--- Empresas por cidade, area, subarea:

empresas_area = df_pipe_subset.groupby("Área do Conhecimento")["Empresa"].nunique()
empresas_subarea = df_pipe_subset.groupby("Subárea do Conhecimento")["Empresa"].nunique()
empresas_por_cidade = df_pipe_subset.groupby("Município")["Empresa"].count()

print(empresas_subarea)
print(empresas_area)
print(empresas_por_cidade.sort_values(ascending=False))
"""

# Tentativa de verificar possibilidade para novo Feature de Pesquisadores Principais
"""
Verifiquei se seria possivel simplificar as 3 features de pesquisadores principais, em apenas uma
na qual iria implementar sua categoria entre parenteses
Para isso verifiquei se existia linhas com informações em pelo menos 2 desses 3 features
173 linhas possvem mais de um valor preenchido, sendo problematico então unificar esses dados
porém, sendo possivel em uma apresentação excell mostrar de forma organizada
uma vez que existe 173 dessas problemaicas duplas, enquanto existem mais de 5 mil dados nulos e 500 com apenas 1 campo
"""

#------------------------
'Processos das Buscas:'

#Busca por Nulos:
""" 
colunas_total_nao_informado = [col for col in df_pipe.columns if (df_pipe[col] == "Não Informado").all()]
print(colunas_total_nao_informado)
print(f"Quantidade: {len(colunas_total_nao_informado)}")

contagem = (df_pipe == "Não Informado").sum()
print(contagem[contagem > 0].sort_values())
"""

#Dados Uteis para Exterior:
"""
--Empresas e quantidade de projetos:

> Dados focados no Exterior:

paises = pd.concat([
    df_pipe['País Acordo(s)/Convênio(s) de Cooperação com a FAPESP'],
    df_pipe['País Instituição (ões) no Exterior']
])
paises = paises[~paises.isin(['Brasil', 'Não Informado'])]
print(paises.value_counts().to_string())

_______________________________________________________________________________

> Dados da Featura País Acordo/Convênio (dados focados entre exterior e nacional):

coluna = df_pipe['País Acordo(s)/Convênio(s) de Cooperação com a FAPESP']
brasil = (coluna == 'Brasil').sum()
nao_informado = (coluna == 'Não Informado').sum()
exterior = (~coluna.isin(['Brasil', 'Não Informado'])).sum()
total = len(coluna)

print(f"Brasil: {brasil}")
print(f"Não Informado: {nao_informado}")
print(f"Exterior (outros países): {exterior}")
"""

#Dados uteis Ribeirão Preto:
"""

> Colunas que usam ribeirão preto

for col in df_pipe.columns:
    if df_pipe[col].astype(str).str.contains('Ribeirão Preto', case=False, na=False).any():
        print(f"'Ribeirão Preto' encontrado na coluna: {col}")

_______________________________________________________________________________
> Empresas em ribeirão que usam modalidade de apoio

empresas_rp_modalidade = df_pipe_subset[
    df_pipe_subset['Município'].str.contains('Ribeirão Preto', case=False, na=False) &
    df_pipe_subset['Modalidade de apoio'].notna()  # garante que exista algum apoio
]
print(f"Quantidade de projetos: {len(empresas_rp_modalidade)}")

_______________________________________________________________________________

> Empresas únicas em Ribeirão Preto
unicas = df_pipe[df_pipe['Município'].str.contains('Ribeirão Preto', case=False, na=False)]['Empresa'].nunique()
print("Empresas únicas em Ribeirão Preto:", unicas)

_______________________________________________________________________________

> Total de empresas gerais em Ribeirão Preto
total_empresas = df_pipe[df_pipe['Município'].str.contains('Ribeirão Preto', case=False, na=False)]['Empresa'].count()
print("Total de projetos com empresa em Ribeirão Preto:", total_empresas)

_______________________________________________________________________________

> Total de projetos em Ribeirão Preto
total_projetos = df_pipe[df_pipe['Município'].str.contains('Ribeirão Preto', case=False, na=False)].shape[0]
print("Total de projetos em Ribeirão Preto:", total_projetos)

_______________________________________________________________________________
"""

#Feature Pesquisadores Principais
"""
cols = ['Pesquisadores Principais (Atuais)', 'Pesquisadores Principais (Últimos)', 'Pesquisadores Principais (Anteriores)']
tem_mais_de_um = ((df_pipe[cols] != 'Não Informado').sum(axis=1) >= 2).sum()
print("Projetos com 2 ou 3 colunas preenchidas:", tem_mais_de_um)
"""


#Verificação sobre Exterior e cooperação com exterior
"""
print("Instituições no Exterior (diferente de 'Não Informado'):", (df_pipe['Instituições no Exterior'] != 'Não Informado').sum())

for col in ['País Acordo(s)/Convênio(s) de Cooperação com a FAPESP', 'País Instituição (ões) no Exterior']:
    qtd = df_pipe[~df_pipe[col].isin(['Brasil', 'Não Informado'])].shape[0]
    print(f"{col} (exterior, sem Brasil):", qtd)


filtro = df_pipe[~df_pipe['País Acordo(s)/Convênio(s) de Cooperação com a FAPESP'].isin(['Brasil', 'Não Informado'])]
print(f"Total de linhas: {len(filtro)}\n")
print(filtro[['N. Processo', 'Município', 'Pesquisador responsável no exterior', 'País Acordo(s)/Convênio(s) de Cooperação com a FAPESP']].to_string(index=False))
"""

#Verificação sobre auxilios (quantidade total e modalidades)
"""
# 1. Geral (apenas modalidades válidas)
auxilio_geral = df_pipe.loc[df_pipe['Modalidade de apoio'] != 'Não Informado', 'Modalidade de apoio'].value_counts()
total_geral = auxilio_geral.sum()

# 2. Ribeirão Preto
mask_rp = df_pipe['Município'].str.strip().str.lower() == 'ribeirão preto'
auxilio_rp = df_pipe.loc[mask_rp & (df_pipe['Modalidade de apoio'] != 'Não Informado'), 'Modalidade de apoio'].value_counts()
total_rp = auxilio_rp.sum()

# 3. Exterior (Instituições no Exterior ou País Instituição) – SEM acordo
mask_ext = (
    (df_pipe['Instituições no Exterior'] != 'Não Informado') |
    (~df_pipe['País Instituição (ões) no Exterior'].isin(['Brasil', 'Não Informado']))
)
auxilio_exterior = df_pipe.loc[mask_ext & (df_pipe['Modalidade de apoio'] != 'Não Informado'), 'Modalidade de apoio'].value_counts()
total_ext = auxilio_exterior.sum()

# 4. Cooperação exterior (apenas País Acordo)
mask_coop = ~df_pipe['País Acordo(s)/Convênio(s) de Cooperação com a FAPESP'].isin(['Brasil', 'Não Informado'])
auxilio_cooperacao = df_pipe.loc[mask_coop & (df_pipe['Modalidade de apoio'] != 'Não Informado'), 'Modalidade de apoio'].value_counts()
total_coop = auxilio_cooperacao.sum()

# 5. Nacional (não está em nenhum dos dois filtros acima, E modalidade válida)
mask_nac = ~(mask_ext | mask_coop)
auxilio_nacional = df_pipe.loc[mask_nac & (df_pipe['Modalidade de apoio'] != 'Não Informado'), 'Modalidade de apoio'].value_counts()
total_nac = auxilio_nacional.sum()

# Exibir
print("=== TOTAL DE PROJETOS COM MODALIDADE VÁLIDA POR CATEGORIA ===")
print(f"Geral: {total_geral}")
print(f"Ribeirão Preto: {total_rp}")
print(f"Exterior (instituições): {total_ext}")
print(f"Cooperação exterior (acordos): {total_coop}")
print(f"Nacional: {total_nac}\n")

print("=== DISTRIBUIÇÃO DAS MODALIDADES (APENAS VALORES VÁLIDOS) ===")
print("\n--- Geral ---")
print(auxilio_geral)
print("\n--- Ribeirão Preto ---")
print(auxilio_rp)
print("\n--- Exterior ---")
print(auxilio_exterior)
print("\n--- Cooperação exterior ---")
print(auxilio_cooperacao)
print("\n--- Nacional ---")
print(auxilio_nacional)
"""

#assuntos
"""
print("Quantidade de valores únicos na coluna 'Assuntos':", df_pipe['Assuntos'].nunique())
print("\nTop 20 assuntos mais frequentes:")
print(df_pipe['Assuntos'].value_counts().head(20))
"""

#Ribeirao e exterior quantidade
"""
mask_rp = df_pipe['Município'].str.strip().str.lower() == 'ribeirão preto'

# Empresas com acordo/convênio exterior
mask_acordo = ~df_pipe['País Acordo(s)/Convênio(s) de Cooperação com a FAPESP'].isin(['Brasil', 'Não Informado'])
empresas_rp_acordo = df_pipe.loc[mask_rp & mask_acordo & (df_pipe['Empresa'] != 'Não Informado'), 'Empresa'].nunique()

# Empresas com instituição no exterior
mask_inst = (
    (df_pipe['Instituições no Exterior'] != 'Não Informado') |
    (~df_pipe['País Instituição (ões) no Exterior'].isin(['Brasil', 'Não Informado']))
)
empresas_rp_inst = df_pipe.loc[mask_rp & mask_inst & (df_pipe['Empresa'] != 'Não Informado'), 'Empresa'].nunique()

print("Empresas RP com acordo exterior:", empresas_rp_acordo)
print("Empresas RP com instituição exterior:", empresas_rp_inst)
"""

#ribeirao e com projeto exterior
"""

# Filtro para Ribeirão Preto
mask_rp = df_pipe['Município'].str.strip().str.lower() == 'ribeirão preto'

# 1. Cooperação exterior (País Acordo)
mask_coop = (
    (df_pipe['País Acordo(s)/Convênio(s) de Cooperação com a FAPESP'] != 'Brasil') &
    (df_pipe['País Acordo(s)/Convênio(s) de Cooperação com a FAPESP'] != 'Não Informado')
)
projetos_coop_rp = df_pipe.loc[mask_rp & mask_coop].copy()

# 2. Instituição no exterior
mask_inst = (
    ((df_pipe['País Instituição (ões) no Exterior'] != 'Brasil') &
     (df_pipe['País Instituição (ões) no Exterior'] != 'Não Informado')) |
    (df_pipe['Instituições no Exterior'] != 'Não Informado')
)
projetos_inst_rp = df_pipe.loc[mask_rp & mask_inst].copy()

# Colunas de interesse na ordem solicitada
colunas_interesse = [
    'Título',
    'Assuntos',
    'Área do Conhecimento',
    'Empresa',
    'Município',
    'País Instituição (ões) no Exterior',
    'Pesquisador Responsável',
    'Pesquisador responsável no exterior',
    'Pesquisadores Principais (Atuais)',
    'Pesquisadores Principais (Últimos)',
    'Pesquisadores Principais (Anteriores)',
    'Resumo (Português)'
]

# Filtrar apenas as colunas existentes
colunas_existentes = [c for c in colunas_interesse if c in df_pipe.columns]

# Prints
print("=== PROJETOS DE RIBEIRÃO PRETO COM COOPERAÇÃO EXTERIOR (ACORDO) ===")
print(f"Total: {len(projetos_coop_rp)}")
if not projetos_coop_rp.empty:
    print(projetos_coop_rp[colunas_existentes].to_string(index=False, max_rows=20))
else:
    print("Nenhum projeto encontrado.")

print("\n=== PROJETOS DE RIBEIRÃO PRETO COM INSTITUIÇÃO NO EXTERIOR ===")
print(f"Total: {len(projetos_inst_rp)}")
if not projetos_inst_rp.empty:
    print(projetos_inst_rp[colunas_existentes].to_string(index=False, max_rows=20))
else:
    print("Nenhum projeto encontrado.")

"""


# Pesquisador em cooperacao com exterior
"""
mask_coop = (df_pipe['País Acordo(s)/Convênio(s) de Cooperação com a FAPESP'] != 'Brasil') & \
            (df_pipe['País Acordo(s)/Convênio(s) de Cooperação com a FAPESP'] != 'Não Informado')

amostra = df_pipe.loc[mask_coop, ['Pesquisador Responsável', 'Pesquisador responsável no exterior', 'País Acordo(s)/Convênio(s) de Cooperação com a FAPESP']]

print(amostra.head(10).to_string(index=False))
"""


# Filtra os projetos onde o país do acordo/convênio é 'Brasil'
brasil_acordo = df_pipe[df_pipe['País Acordo(s)/Convênio(s) de Cooperação com a FAPESP'] == 'Brasil']

# Mostra as primeiras 10 linhas com colunas de interesse
"""
colunas_ver = [
    'N. Processo',
    'Município',
    'Instituições no Exterior',
    'País Instituição (ões) no Exterior',
    'Pesquisador responsável no exterior',
    'País Acordo(s)/Convênio(s) de Cooperação com a FAPESP'
]
print(brasil_acordo[colunas_ver].head(10).to_string(index=False))

# Se quiser ver quantos registros existem:
print(f"Total de projetos com 'Brasil' nessa coluna: {len(brasil_acordo)}")



# Filtro: exclui Brasil e Não Informado
cooperacao_exterior = df_pipe[~df_pipe['País Acordo(s)/Convênio(s) de Cooperação com a FAPESP'].isin(['Brasil', 'Não Informado'])]

colunas_ver = [
    'N. Processo',
    'Município',
    'Instituições no Exterior',
    'País Instituição (ões) no Exterior',
    'Pesquisador responsável no exterior',
    'País Acordo(s)/Convênio(s) de Cooperação com a FAPESP'
]

print(cooperacao_exterior[colunas_ver].head(10).to_string(index=False))
print(f"Total: {len(cooperacao_exterior)}")
"""

# Pesquisadores cooperacao com exterior (sem pesquisador no exterior)
"""
mask_coop_pesq = ~df_pipe['País Acordo(s)/Convênio(s) de Cooperação com a FAPESP'].isin(['Brasil', 'Não Informado'])


coop_responsaveis = df_pipe.loc[mask_coop_pesq & (df_pipe['Pesquisador Responsável'] != 'Não Informado'), 'Pesquisador Responsável']
coop_princ_atuais = df_pipe.loc[mask_coop_pesq & (df_pipe['Pesquisadores Principais (Atuais)'] != 'Não Informado'), 'Pesquisadores Principais (Atuais)']
coop_princ_ultimos = df_pipe.loc[mask_coop_pesq & (df_pipe['Pesquisadores Principais (Últimos)'] != 'Não Informado'), 'Pesquisadores Principais (Últimos)']
coop_princ_anteriores = df_pipe.loc[mask_coop_pesq & (df_pipe['Pesquisadores Principais (Anteriores)'] != 'Não Informado'), 'Pesquisadores Principais (Anteriores)']

# Concatena tudo e aplica extração de nomes + nunique
total_pesquisadores_cooperacao_exterior = pd.concat([
    coop_responsaveis, coop_princ_atuais, coop_princ_ultimos, coop_princ_anteriores
]).pipe(_extrair_nomes).nunique()

print(f"Total de pesquisadores distintos em projetos com cooperação exterior: {total_pesquisadores_cooperacao_exterior}")
"""
