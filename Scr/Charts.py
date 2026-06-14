import matplotlib.pyplot as plt
import seaborn as sns
import textwrap
from Variables_Counts import *
from Variables_Counts_Ribeirao_Preto import *
import numpy as np

#ok
def grafico_areas_subareas(largura_label=25):
    # Filtra "Não Informado" e pega top N
    top_area = empresas_area[empresas_area.index != "Não Informado"].nlargest(20)
    top_sub = empresas_subarea[empresas_subarea.index != "Não Informado"].nlargest(20)

    # Função para quebrar labels longos
    def divisao_label(labels, largura):
        return [
            '\n'.join(textwrap.wrap(lbl, largura)) if len(str(lbl)) > largura else lbl
            for lbl in labels
        ]

    # Cria subplots
    fig, axes = plt.subplots(1, 2, figsize=(16, 10))

    # Função para gerar heatmap
    def grafico_heatmap(ax, series, title):
        dfm = series.to_frame(name="Quantidade de Empresas")
        dfm.index = divisao_label(dfm.index, largura_label)
        sns.heatmap(
            dfm, annot=True, fmt="d", cmap="Blues", cbar=False, ax=ax,
            annot_kws={"fontsize": 10}, linewidths=0.5, linecolor="lightgray"
        )
        ax.set_title(title, fontsize=12, pad=10)
        ax.set_ylabel("")
        ax.set_yticklabels(ax.get_yticklabels(), rotation=0, fontsize=10)

    # Plota os dois gráficos
    grafico_heatmap(axes[0], top_area, "Área do Conhecimento")
    grafico_heatmap(axes[1], top_sub, "Subárea do Conhecimento")

    plt.tight_layout()
    plt.show()
#ok
def grafico_grande_area(largura_label=25):
    # Filtra "Não Informado" e ordena do maior para o menor
    total_grande_area = empresas_grande_area[empresas_grande_area.index != "Não Informado"].sort_values(ascending=False)

    # Função para quebrar labels longos
    def divisao_label(labels, largura):
        return [
            '\n'.join(textwrap.wrap(lbl, largura)) if len(str(lbl)) > largura else lbl
            for lbl in labels
        ]

    dfm = total_grande_area.to_frame(name="Quantidade de Empresas")
    dfm.index = divisao_label(dfm.index, largura_label)

    plt.figure(figsize=(8, len(dfm)*0.5 + 2))  # altura ajusta conforme número de áreas
    sns.heatmap(
        dfm, annot=True, fmt="d", cmap="Blues", cbar=False,
        annot_kws={"fontsize": 10}, linewidths=0.5, linecolor="lightgray"
    )
    plt.title("Grande Área do Conhecimento", fontsize=12, pad=10)
    plt.ylabel("")
    plt.yticks(rotation=0, fontsize=10)
    plt.tight_layout()
    plt.show()

#ok
def grafico_pesquisadores():
    valores = [
        total_pesquisadores,
        pesquisadores_responsaveis,
        principais_geral,
        qt_principais_atuais,
        qt_principais_anteriores,
        qt_principais_ultimos,
        qt_associados,
        pesquisadores_exterior,
        total_pesquisadores_cooperacao_exterior
    ]

    categorias = [
        'Total',
        'Responsáveis',
        'Principais Total',
        'Principais (Atuais)',
        'Principais (Anteriores)',
        'Principais (Últimos)',
        'Associados',
        'Exterior',
        'Cooperação'
    ]

    # Função que define a cor de acordo com o grupo
    def cor_por_grupo(categoria):
        if categoria == 'Total':
            return 'red'               # Total
        elif categoria.startswith('Principais'):
            return 'steelblue'         # Todos os Principais
        elif categoria in ['Exterior', 'Cooperação']:
            return 'green'             # Exterior e Cooperação
        elif categoria == 'Associados':
            return 'orange'            # Associados
        else:  # 'Responsáveis' (e outros, se houver)
            return 'purple'              # Cor neutra

    cores = [cor_por_grupo(cat) for cat in categorias]

    plt.figure(figsize=(10, 8))
    barras = plt.barh(categorias, valores, color=cores)
    plt.title('Distribuição de Pesquisadores', fontsize=14, pad=15)
    plt.gca().invert_yaxis()

    # Adiciona os números no final de cada barra
    for barra in barras:
        largura = barra.get_width()
        plt.text(largura + (max(valores) * 0.01), barra.get_y() + barra.get_height()/2,
                 str(int(largura)), va='center', fontsize=10)

    plt.tight_layout()
    plt.show()
#ok
def grafico_pesquisas_e_pesquisadores_vertical():
    # Valores de pesquisadores atualizados
    valores_pesquisadores = [
        total_pesquisadores,
        pesquisadores_responsaveis,
        principais_geral,
        qt_associados,
        pesquisadores_exterior,
        total_pesquisadores_cooperacao_exterior
    ]
    categorias_pesquisadores = ['Total', 'Responsaveis', 'Principais', 'Associados', 'Exterior', 'Cooperação']

    # Valores de pesquisas
    valores_pesquisas = [
        total_pesquisas,
        pesquisas_nacionais_sem_inst,
        pesquisas_exterior,
        pesquisas_cooperacao_pais_exterior
    ]
    categorias_pesquisas = ['Total', 'Nacionais', 'Exterior', 'Cooperação']

    fig, axes = plt.subplots(1, 2, figsize=(14, 6))

    # Cores ajustadas para Pesquisadores
    # Ordem: Total, Responsaveis, Principais, Associados, Exterior, Cooperação
    cores_pesquisadores = ['red', 'purple', 'steelblue', 'darkorange', 'green', 'green']

    # Cores ajustadas para Pesquisas
    # Ordem: Total, Nacionais, Exterior, Cooperação
    cores_pesquisas = ['red', 'steelblue', 'green', 'green']

    # Gráfico de Pesquisadores (vertical)
    barras = axes[0].bar(categorias_pesquisadores, valores_pesquisadores, color=cores_pesquisadores)
    axes[0].set_title('Pesquisadores', pad=10)
    for barra in barras:
        altura = barra.get_height()
        axes[0].text(barra.get_x() + barra.get_width()/2, altura + max(valores_pesquisadores)*0.01,
                     str(int(altura)), ha='center', va='bottom', fontsize=10)

    # Gráfico de Pesquisas (vertical)
    barras2 = axes[1].bar(categorias_pesquisas, valores_pesquisas, color=cores_pesquisas)
    axes[1].set_title('Pesquisas', pad=10)
    for barra in barras2:
        altura = barra.get_height()
        axes[1].text(barra.get_x() + barra.get_width()/2, altura + max(valores_pesquisas)*0.01,
                     str(int(altura)), ha='center', va='bottom', fontsize=10)

    plt.tight_layout()
    plt.show()
#ok
def grafico_pesquisas_e_pesquisadores_misto():
    # Valores de pesquisadores
    valores_pesquisadores = [
        total_pesquisadores,
        pesquisadores_responsaveis,
        principais_geral,
        qt_associados,
        total_pesquisadores_cooperacao_exterior
    ]
    categorias_pesquisadores = ['Total', 'Resp.', 'Princ.', 'Assoc.', 'Coop.']

    # Valores de pesquisas para o gráfico de pizza
    valores_pesquisas = [
        pesquisas_nacionais_sem_inst,
        pesquisas_exterior
    ]
    categorias_pesquisas = ['Nacionais', 'Internacionais']

    fig, axes = plt.subplots(1, 2, figsize=(14, 6))

    # Subplot 1: Pesquisadores (barras)
    barras = axes[0].bar(categorias_pesquisadores, valores_pesquisadores, color='steelblue')
    axes[0].set_title('Pesquisadores', pad=10)
    for barra in barras:
        altura = barra.get_height()
        axes[0].text(barra.get_x() + barra.get_width()/2, altura + max(valores_pesquisadores)*0.01,
                     str(int(altura)), ha='center', va='bottom', fontsize=10)

    # Subplot 2: Pesquisas (pizza)
    axes[1].pie(valores_pesquisas, labels=categorias_pesquisas, autopct='%1.1f%%',
                startangle=90, colors=['#FFA500', '#FF6347'])
    axes[1].set_title('Pesquisas (Nacional vs Internacional)', pad=10)

    plt.tight_layout()
    plt.show()

# OK
def grafico_rp():
    # --- Configurações Iniciais ---
    fig, axes = plt.subplots(1, 2, figsize=(20, 8))

    # --- Subplot 1: Métricas Gerais (Permanece igual, com cores distintas) ---
    valores_totais = [
        total_pesquisas_rp,
        quantidade_pesquisas_exterior_rp,
        total_pesquisadores_rp,
        empresas_totais_rp,
        empresas_diferentes_rp
    ]
    categorias_totais = ['Pesquisas', 'Pesquisas Exterior', 'Pesquisadores', 'Empresas', 'Empresas Distintas']

    barras = axes[0].bar(categorias_totais, valores_totais,
                         color=['#4682B4', '#E31A1C', '#33A02C', '#B2DF8A', '#1F78B4'])
    axes[0].set_title('Métricas Gerais - Ribeirão Preto', fontsize=14, fontweight='bold', pad=20)

    for barra in barras:
        altura = barra.get_height()
        axes[0].text(barra.get_x() + barra.get_width() / 2, altura + (max(valores_totais) * 0.01),
                     f'{int(altura)}', ha='center', va='bottom', fontsize=11, fontweight='bold')

    # --- Subplot 2: Comparativo Modalidades (Projetos Totais vs Empresas Distintas) ---
    # Usando as variáveis do seu Counts RP
    # 1. Total de projetos por modalidade
    projetos_por_mod = empresas_rp_quantidade_modalidade_apoio_total.sort_values(ascending=False)
    # 2. Empresas distintas por modalidade (alinhando com a ordem dos projetos)
    empresas_por_mod = empresas_distintas_rp_quantidade_modalidade_apoio.reindex(projetos_por_mod.index)

    if not projetos_por_mod.empty:
        x = np.arange(len(projetos_por_mod))  # Localização das modalidades
        largura = 0.35  # Largura das barras

        # Criar as duas barras agrupadas
        barras_proj = axes[1].bar(x - largura / 2, projetos_por_mod.values, largura, label='Total de Projetos',
                                  color='#6A3D9A')
        barras_emp = axes[1].bar(x + largura / 2, empresas_por_mod.values, largura, label='Empresas Distintas',
                                 color='#CAB2D6')

        # Configurações do Eixo X
        labels_quebrados = ['\n'.join(textwrap.wrap(str(lbl), 15)) for lbl in projetos_por_mod.index]
        axes[1].set_xticks(x)
        axes[1].set_xticklabels(labels_quebrados)
        axes[1].set_title('Modalidade de Apoio - Ribeirão Preto', fontsize=14, fontweight='bold', pad=20)
        axes[1].legend()

        # Adicionar números em cima das barras de projetos
        for barra in barras_proj:
            altura = barra.get_height()
            axes[1].text(barra.get_x() + barra.get_width() / 2, altura + (max(projetos_por_mod.values) * 0.01),
                         f'{int(altura)}', ha='center', va='bottom', fontsize=9, fontweight='bold')

        # Adicionar números em cima das barras de empresas
        for barra in barras_emp:
            altura = barra.get_height()
            axes[1].text(barra.get_x() + barra.get_width() / 2, altura + (max(projetos_por_mod.values) * 0.01),
                         f'{int(altura)}', ha='center', va='bottom', fontsize=9, color='black')
    else:
        axes[1].text(0.5, 0.5, 'Sem dados de modalidade', ha='center', va='center')

    plt.tight_layout()
    plt.show()

#ok
def grafico_empresas():
    empresas_top15_cidade = empresas_por_cidade.head(15)

    fig, axes = plt.subplots(1, 2, figsize=(16, 6))

    # Subplot 1: Heatmap top 15 cidades
    df_top15 = empresas_top15_cidade.to_frame(name="Quantidade")
    df_top15.index = ['\n'.join(textwrap.wrap(lbl, 15)) for lbl in df_top15.index]

    sns.heatmap(df_top15, annot=True, fmt="d", cmap="Blues", cbar=False,
                annot_kws={"fontsize": 10}, linewidths=0.5, linecolor="lightgray", ax=axes[0])
    axes[0].set_title("Empresas por cidade", pad=15)
    axes[0].set_ylabel("")
    axes[0].set_yticklabels(axes[0].get_yticklabels(), rotation=0, fontsize=10)

    # Subplot 2: Barras verticais com totais
    valores_totais = [total_empresas, empresas_cidades_distintas]
    categorias_totais = ['Total de Empresas', 'Cidades Distintas']
    barras = axes[1].bar(categorias_totais, valores_totais, color=['steelblue', 'darkorange'])
    axes[1].set_title("Totais Gerais", pad=15)
    for barra in barras:
        altura = barra.get_height()
        axes[1].text(barra.get_x() + barra.get_width() / 2, altura + max(valores_totais) * 0.01,
                     str(int(altura)), ha='center', va='bottom', fontsize=10)

    plt.tight_layout()
    plt.show()

def grafico_circular_pesquisas():
    """
    Gera um gráfico de pizza comparando as categorias de pesquisas:
    Nacionais (sem inst), Nacionais (sem coop), Exterior e Cooperação.
    """
    valores = [
        pesquisas_nacionais_sem_inst,
        pesquisas_nacionais_sem_coop,
        pesquisas_exterior,
        pesquisas_cooperacao_pais_exterior
    ]

    categorias = [
        'Nacionais (Sem Inst. Ext.)',
        'Nacionais (Sem Coop. Ext.)',
        'Instituições no Exterior',
        'Cooperação FAPESP Exterior'
    ]

    cores = ['#4CAF50', '#8BC34A', '#2196F3', '#FF9800']

    plt.figure(figsize=(10, 7))
    plt.pie(valores, labels=categorias, autopct='%1.1f%%', startangle=140, colors=cores, pctdistance=0.85)

    # Desenha um círculo no meio para transformar em gráfico de rosca
    centro_circulo = plt.Circle((0, 0), 0.70, fc='white')
    fig = plt.gcf()
    fig.gca().add_artist(centro_circulo)

    plt.title('Distribuição de Pesquisas: Nacional vs Internacional', fontsize=14, pad=20)
    plt.axis('equal')
    plt.tight_layout()
    plt.show()

def grafico_localizacao_pesquisas(top_n=10):
    """
    Gera dois gráficos horizontais, um embaixo do outro:
    1. Top Países no Exterior
    2. Top Municípios no Brasil
    """
    fig, axes = plt.subplots(2, 1, figsize=(12, 12))

    # --- Subplot 1: Países Exterior ---
    top_paises = paises_exterior_qt_pesquisas.sort_values(ascending=False).head(top_n)

    barras1 = axes[0].barh(top_paises.index, top_paises.values, color='steelblue')
    axes[0].set_title(f'Total de Países em Pesquisas no Exterior', fontsize=13, pad=15)
    axes[0].invert_yaxis()

    for barra in barras1:
        largura = barra.get_width()
        axes[0].text(largura + (max(top_paises.values) * 0.01), barra.get_y() + barra.get_height() / 2,
                     f'{int(largura)}', va='center', fontsize=10)

    # --- Subplot 2: Municípios Brasil ---
    top_municipios = municipios_brasil_qt_pesquisas.sort_values(ascending=False).head(top_n)

    barras2 = axes[1].barh(top_municipios.index, top_municipios.values, color='darkorange')
    axes[1].set_title(f'Top {top_n} Municípios Brasileiros em Pesquisas', fontsize=13, pad=15)
    axes[1].invert_yaxis()

    for barra in barras2:
        largura = barra.get_width()
        axes[1].text(largura + (max(top_municipios.values) * 0.01), barra.get_y() + barra.get_height() / 2,
                     f'{int(largura)}', va='center', fontsize=10)

    plt.tight_layout(pad=4.0)
    plt.show()

grafico_localizacao_pesquisas()
