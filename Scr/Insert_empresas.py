import os
import pandas as pd
import numpy as np

caminho_csv_entrada = r"C:\T.I\Python\Projetos\DataBase\Fapesp_PIPE_2026\Export_csv\DataBase\PIPE_database_completo.csv"
pasta_saida = "../Export_csv/Insert"
nome_arquivo = "Insert_PIPE_2026_empresas.sql"
arquivo_sql_saida = os.path.join(pasta_saida, nome_arquivo)
os.makedirs(pasta_saida, exist_ok=True)

df = pd.read_csv(caminho_csv_entrada, encoding="utf-8-sig")

# Garantindo a feature 'Título'
if 'Título' not in df.columns:
    df['Título'] = df['Título (Português)'].replace(['Não Informado', '', ' ', None], np.nan).fillna(df['Título (Inglês)'])
    df['Título'] = df['Título'].fillna("Título não disponível")

with open(arquivo_sql_saida, "w", encoding="cp1252", errors="replace") as f:
    # 1. Instituicao_Ensino (Usando Empresa e Município)
    df_inst = df[['Empresa', 'Município']].drop_duplicates().reset_index(drop=True)
    df_inst['id_instituicao'] = df_inst.index + 1
    for id_instituicao, Empresa, Municipio in zip(df_inst['id_instituicao'], df_inst['Empresa'], df_inst['Município']):
        f.write(f'INSERT INTO "Instituicao_Ensino" ("id_instituicao", "Empresa", "Município") VALUES ({id_instituicao}, \'{str(Empresa).replace(chr(39), chr(39)*2)}\', \'{str(Municipio).replace(chr(39), chr(39)*2)}\');\n')

    # 2. Auxilio_FAPESP
    df_aux = df[['Data de Início', 'Data de Término', 'Modalidade de apoio']].drop_duplicates().reset_index(drop=True)
    df_aux['id_auxilio'] = df_aux.index + 1
    for id_auxilio, data_inicio, data_termino, modalidade_apoio in zip(df_aux['id_auxilio'], df_aux['Data de Início'], df_aux['Data de Término'], df_aux['Modalidade de apoio']):
        f.write(f'INSERT INTO "Auxilio_FAPESP" ("id_auxilio", "Data de Início", "Data de Término", "Modalidade de apoio") VALUES ({id_auxilio}, \'{data_inicio}\', \'{data_termino}\', \'{str(modalidade_apoio).replace(chr(39), chr(39)*2)}\');\n')

    # 3. Pesquisador (Vinculado via Empresa)
    df_pesq_tmp = pd.merge(df[['Pesquisador Responsável', 'Município', 'Empresa']].drop_duplicates(), df_inst, on='Empresa')
    df_pesq_tmp['id_pesquisador'] = df_pesq_tmp.index + 1
    for id_pesquisador, pesquisador_responsavel, municipio, id_instituicao in zip(df_pesq_tmp['id_pesquisador'], df_pesq_tmp['Pesquisador Responsável'], df_pesq_tmp['Município_x'], df_pesq_tmp['id_instituicao']):
        f.write(f'INSERT INTO "Pesquisador" ("id_pesquisador", "Pesquisador Responsável", "Município", "id_instituicao") VALUES ({id_pesquisador}, \'{str(pesquisador_responsavel).replace(chr(39), chr(39)*2)}\', \'{str(municipio).replace(chr(39), chr(39)*2)}\', {id_instituicao});\n')

    # 4. Projeto_Pesquisa (Vinculado via Auxílio)
    df_proj_tmp = pd.merge(df, df_aux, on=['Data de Início', 'Data de Término', 'Modalidade de apoio'])
    for n_processo, titulo, area_conhecimento, id_auxilio in zip(df_proj_tmp['N. Processo'], df_proj_tmp['Título'], df_proj_tmp['Área do Conhecimento'], df_proj_tmp['id_auxilio']):
        f.write(f'INSERT INTO "Projeto_Pesquisa" ("N. Processo", "Título", "Área do Conhecimento", "id_auxilio") VALUES (\'{n_processo}\', \'{str(titulo).replace(chr(39), chr(39)*2)}\', \'{str(area_conhecimento).replace(chr(39), chr(39)*2)}\', {id_auxilio});\n')

    # 5. Participacao_Projeto (M:N)
    df_part = pd.merge(df[['Pesquisador Responsável', 'N. Processo']], df_pesq_tmp, on='Pesquisador Responsável')
    for id_pesquisador, n_processo in zip(df_part['id_pesquisador'], df_part['N. Processo']):
        f.write(f'INSERT INTO "Participacao_Projeto" ("id_pesquisador", "N. Processo") VALUES ({id_pesquisador}, \'{n_processo}\');\n')

print(f"Script SQL gerado com sucesso em: {arquivo_sql_saida}")
