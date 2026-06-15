from Path import pipe_path
import io
import pandas as pd

#Tratamento de Erros
with open(pipe_path, 'r', encoding='utf-8-sig') as pipe:
    lines = pipe.readlines()

if not lines[0].strip().endswith(';'):
    lines[0] = lines[0].rstrip() + ';\n'

lines = [v for v in lines if ';' in v]

#Config Pandas
df_pipe_base = pd.read_csv(io.StringIO(''.join(lines)), sep=';')
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', None)

#Data
features = [
    'N. Processo', 'Título (Português)', 'Título (Inglês)', 'Beneficiário',
    'Instituição', 'Cidade Instituição', 'Instituição Parceira', 'Empresa',
    'Município', 'Pesquisador Responsável',
    'Pesquisadores Principais (Atuais)', 'Pesquisadores Principais (Últimos)', 'Pesquisadores Principais (Anteriores)',
    'Pesquisadores Associados', 'Supervisor', 'Local de Pesquisa',
    'Pesquisador Visitante', 'Instituição do Pesquisador Visitante',
    'Modalidade de apoio', 'Grande Área do Conhecimento',
    'Área do Conhecimento', 'Subárea do Conhecimento', 'Assuntos',
    'Data de Início', 'Data de Término',
    'Acordo(s)/Convênio(s) de Cooperação com a FAPESP',
    'Instituições no Exterior',
    'País Acordo(s)/Convênio(s) de Cooperação com a FAPESP',
    'País Instituição (ões) no Exterior',
    'Pesquisador responsável no exterior', 'Resumo (Português)',
    'Resumo (Inglês)', 'Processos Vinculados'
]

df_pipe_base = df_pipe_base[features]
df_pipe = df_pipe_base.copy()
df_pipe = df_pipe.fillna("Não Informado")
df_pipe = df_pipe.astype(object)

#CSV
df_pipe.to_csv("../Export_csv/DataBase/PIPE_database_completo.csv", index=False, encoding="utf-8-sig")

#Feature Nova
df_pipe['Título'] = df_pipe['Título (Português)'].replace(['Não Informado', '', ' ', None],pd.NA).fillna(df_pipe['Título (Inglês)'])



#Explicações sobre feature e tratamento de erros


#Explicação feature nova
"""
Alguns dados de título tem apenas a versão em ingles, para isso criei uma feature que prioriza o titulo em portugues
mas que para não mostrar uma pesquisa com dado null, mostre o titulo em ingles caso seja a ultma opcao
exceto em casos de pesquisas no exterior, onde é viavel mostrar o titulo originalmente em ingles
"""

#Explicação erros index
"""
Processo de index do CSV
o Arquivo estava deslocando os valores para a direita, não mostrando o dado real de sua feature

poderia ser resolvido deslocando a index com iloc
mas pensando em escalabilidade, futuramente um csv corrigido poderia quebrar essa solução
então resolvi tentar achar o problema real do qual estava gerando essa dispariedade

usei comandos para buscar o dado bruto do csv, podendo ver como estavam ecritos

with open(pipe_path, 'r', encoding='utf-8-sig') as f:
    for i in range(3):
        # O repr() mostra caracteres invisíveis como \n ou espaços extras
        print(f"Linha {i}: {repr(f.readline())}")

vendo os dados de cada linha, encontrei possiveis causas
a linha 1 tinha um problema de ter dois ; sendo esse o delimiter
poderia ser o responsavel por gerar dados novos, mas apenas geraria um valor nulo extra, então isso não deveria quebrar nada
depois verifiquei diferenças de aspas, tendo linhas com aspas duplas e outros com aspas simples, mas também não parecia que causaria uma quebra, apenas talvez dados nulos extras
então verifiquei que a linha 0, as features, não tinha um delimiter final, e esse poderia ser o verdadeiro causador, uma vez que o dado ficaria em aberto até o edlimiter ser encontrado

sendo assim, pensei em resolver isso no codigo
editar o csv seria um processo viavel mas momentaneamente
então criei no codigo um verificador, caso algo seja mudado no csv e o mesmo acabe por terminar com ; nada acontece, pois tudo seguira normalmente
mas caso o ; não exista, ele é adicionado, e assim todos os valores passam a pertencer corretmente a seu feature

"""
#Explicação erro linha final
"""


as ultimas 3 linhas do csv eram informações externas, referentes a biblioteca, url e data 
print("\n--- [4] AS ÚLTIMAS 5 LINHAS DO ARQUIVO ---")
with open(pipe_path, 'r', encoding='utf-8-sig') as f:
    all_lines = f.readlines()
    for i, line in enumerate(all_lines[-5:]):
        print(f"Linha {len(all_lines) - 5 + i}: {repr(line)}")


Linha 5720: '>>> Biblioteca Virtual da FAPESP (BV FAPESP) <<<\n'
Linha 5721: 'Dados gerados em: 09/Jun/26 15:46:19\n'
Linha 5722: 'URL: https://bv.fapesp.br/57782\n'

essas foram retiradas, garantido que apenas os dados ficassem expostos
(conferido diretamente com o excel, o total de 5716 dados foram confirmados entre o pandas e a verificação visual
"""


