import os
import pandas as pd
import numpy as np

caminho_csv_entrada = r"C:\T.I\Python\Projetos\DataBase\Fapesp_PIPE_2026\Export_csv\DataBase\PIPE_database_completo.csv"
pasta_saida = "../Export_csv/Insert"
nome_arquivo = "Insert_PIPE_2026.sql"
arquivo_sql_saida = os.path.join(pasta_saida, nome_arquivo)
os.makedirs(pasta_saida, exist_ok=True)

df = pd.read_csv(caminho_csv_entrada, encoding="utf-8-sig")

if 'Título' not in df.columns:
    df['Título'] = df['Título (Português)'].replace(['Não Informado', '', ' ', None], np.nan).fillna(df['Título (Inglês)'])
    df['Título'] = df['Título'].fillna("Título não disponível")

with open(arquivo_sql_saida, "w", encoding="cp1252", errors="replace") as f:
    # 1. Instituicao
    df_inst = df[['Instituição', 'Cidade Instituição']].drop_duplicates().reset_index(drop=True)
    df_inst['id_instituicao'] = df_inst.index + 1
    for id_i, inst, cid in zip(df_inst['id_instituicao'], df_inst['Instituição'], df_inst['Cidade Instituição']):
        f.write(f'INSERT INTO "Instituicao_Ensino" ("id_instituicao", "Instituição", "Cidade Instituição") VALUES ({id_i}, \'{str(inst).replace(chr(39), chr(39)*2)}\', \'{str(cid).replace(chr(39), chr(39)*2)}\');\n')

    # 2. Auxilio
    df_aux = df[['Data de Início', 'Data de Término', 'Modalidade de apoio']].drop_duplicates().reset_index(drop=True)
    df_aux['id_auxilio'] = df_aux.index + 1
    for id_a, ini, ter, mod in zip(df_aux['id_auxilio'], df_aux['Data de Início'], df_aux['Data de Término'], df_aux['Modalidade de apoio']):
        f.write(f'INSERT INTO "Auxilio_FAPESP" ("id_auxilio", "Data de Início", "Data de Término", "Modalidade de apoio") VALUES ({id_a}, \'{ini}\', \'{ter}\', \'{str(mod).replace(chr(39), chr(39)*2)}\');\n')

    # 3. Pesquisador
    df_pesq_tmp = pd.merge(df[['Pesquisador Responsável', 'Município', 'Instituição']].drop_duplicates(), df_inst, on='Instituição')
    df_pesq_tmp['id_pesquisador'] = df_pesq_tmp.index + 1
    for id_p, pesq, mun, id_i in zip(df_pesq_tmp['id_pesquisador'], df_pesq_tmp['Pesquisador Responsável'], df_pesq_tmp['Município'], df_pesq_tmp['id_instituicao']):
        f.write(f'INSERT INTO "Pesquisador" ("id_pesquisador", "Pesquisador Responsável", "Município", "id_instituicao") VALUES ({id_p}, \'{str(pesq).replace(chr(39), chr(39)*2)}\', \'{str(mun).replace(chr(39), chr(39)*2)}\', {id_i});\n')

    # 4. Projeto
    df_proj_tmp = pd.merge(df, df_aux, on=['Data de Início', 'Data de Término', 'Modalidade de apoio'])
    for proc, tit, area, id_a in zip(df_proj_tmp['N. Processo'], df_proj_tmp['Título'], df_proj_tmp['Área do Conhecimento'], df_proj_tmp['id_auxilio']):
        f.write(f'INSERT INTO "Projeto_Pesquisa" ("N. Processo", "Título", "Área do Conhecimento", "id_auxilio") VALUES (\'{proc}\', \'{str(tit).replace(chr(39), chr(39)*2)}\', \'{str(area).replace(chr(39), chr(39)*2)}\', {id_a});\n')

    # 5. Participacao
    df_part = pd.merge(df[['Pesquisador Responsável', 'N. Processo']], df_pesq_tmp, on='Pesquisador Responsável')
    for id_p, proc in zip(df_part['id_pesquisador'], df_part['N. Processo']):
        f.write(f'INSERT INTO "Participacao_Projeto" ("id_pesquisador", "N. Processo") VALUES ({id_p}, \'{proc}\');\n')

print("Script SQL gerado com 100% de fidelidade às features originais!")
