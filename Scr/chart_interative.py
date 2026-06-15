import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os
from datetime import datetime

# Configuração da Página
st.set_page_config(page_title="Dashboard FAPESP PIPE 2026", layout="wide")


# Função para carregar dados
@st.cache_data
def load_data():
    path = "Export_csv/DataBase/PIPE_database_completo.csv"
    if not os.path.exists(path):
        path = r"C:\T.I\Python\Projetos\DataBase\Fapesp_PIPE_2026\Export_csv\DataBase\PIPE_database_completo.csv"

    if not os.path.exists(path):
        st.error(f"Arquivo não encontrado!")
        st.stop()

    df = pd.read_csv(path)
    if 'Título' not in df.columns:
        df['Título'] = df['Título (Português)'].replace(['Não Informado', '', ' ', None], pd.NA).fillna(
            df['Título (Inglês)'])

    # Converter datas usando os nomes corretos identificados no CSV
    df['Data de Início'] = pd.to_datetime(df['Data de Início'], errors='coerce')
    df['Data de Término'] = pd.to_datetime(df['Data de Término'], errors='coerce')

    return df


df = load_data()

#BARRA LATERAL
st.sidebar.header("🔍 Filtros Dinâmicos")


def get_options(column):
    opts = sorted(df[column].dropna().unique().tolist())
    if "Não Informado" in opts: opts.remove("Não Informado")
    return ["Todas"] + opts


#1 Grande Área
selected_ga = st.sidebar.selectbox("Grande Área do Conhecimento", get_options("Grande Área do Conhecimento"))

#2 Município
selected_mun = st.sidebar.selectbox("Município", get_options("Município"))

#3 País Parceiro
p_inst_all = df[~df['País Instituição (ões) no Exterior'].isin(['Brasil', 'Não Informado'])][
    'País Instituição (ões) no Exterior']
p_acordo_all = df[~df['País Acordo(s)/Convênio(s) de Cooperação com a FAPESP'].isin(['Brasil', 'Não Informado'])][
    'País Acordo(s)/Convênio(s) de Cooperação com a FAPESP']
paises_unicos = sorted(pd.concat([p_inst_all, p_acordo_all]).dropna().unique().tolist())
selected_pais = st.sidebar.selectbox("País Parceiro (Internacional)", ["Todos"] + paises_unicos)

#4 Modalidade de Apoio
selected_mod = st.sidebar.selectbox("Modalidade de Apoio", get_options("Modalidade de apoio"))

#5 Filtro Temporal
st.sidebar.subheader("📅 Período de Início")
min_date_orig = df['Data de Início'].min()
max_date_orig = df['Data de Início'].max()
if pd.isnull(min_date_orig) or pd.isnull(max_date_orig):
    min_date_orig, max_date_orig = datetime(2000, 1, 1), datetime(2026, 12, 31)

if 'date_reset_counter' not in st.session_state:
    st.session_state.date_reset_counter = 0


def reset_dates():
    st.session_state.date_reset_counter += 1


col_d1, col_d2 = st.sidebar.columns(2)
with col_d1:
    start_date = st.date_input(
        "Início:",
        value=min_date_orig,
        min_value=min_date_orig,
        max_value=max_date_orig,
        key=f"start_date_{st.session_state.date_reset_counter}"
    )
with col_d2:
    end_date = st.date_input(
        "Fim:",
        value=max_date_orig,
        min_value=min_date_orig,
        max_value=max_date_orig,
        key=f"end_date_{st.session_state.date_reset_counter}"
    )

st.sidebar.button("Resetar Datas", on_click=reset_dates)

#Aplicação
df_f = df.copy()

if selected_ga != "Todas":
    df_f = df_f[df_f["Grande Área do Conhecimento"] == selected_ga]

if selected_mun != "Todas":
    df_f = df_f[df_f["Município"] == selected_mun]

if selected_pais != "Todos":
    mask_pais = (df_f['País Instituição (ões) no Exterior'] == selected_pais) | \
                (df_f['País Acordo(s)/Convênio(s) de Cooperação com a FAPESP'] == selected_pais)
    df_f = df_f[mask_pais]

if selected_mod != "Todas":
    df_f = df_f[df_f["Modalidade de apoio"] == selected_mod]

df_f = df_f[
    (df_f['Data de Início'] >= pd.to_datetime(start_date)) & (df_f['Data de Início'] <= pd.to_datetime(end_date))]

#CABEÇALHO
st.title("📊 Análise Quantitativa FAPESP PIPE 2026")
st.markdown("---")

#MÉTRICAS
c1, c2, c3, c4 = st.columns(4)
total_p = len(df_f[df_f['Título (Português)'] != 'Não Informado'])
total_e = df_f[df_f['Empresa'] != 'Não Informado']['Empresa'].nunique()


def count_unique_pesq(df, columns):
    all_names_series = pd.concat([df[c] for c in columns if c in df.columns])
    all_names_series = all_names_series.dropna().astype(str)
    all_names_series = all_names_series[all_names_series != 'Não Informado']

    names_list = []
    for entry in all_names_series:
        # Divide por ponto e vírgula e limpa espaços
        names_list.extend([name.strip() for name in str(entry).split(';') if name.strip()])

    return pd.Series(names_list).nunique()


#Variáveis de pesquisadores atualizadas
total_pesq = count_unique_pesq(df_f, [
    'Pesquisador Responsável',
    'Pesquisadores Principais (Atuais)',
    'Pesquisadores Principais (Últimos)',
    'Pesquisadores Principais (Anteriores)',
    'Pesquisadores Associados',
    'Pesquisador responsável no exterior'
])

c1.metric("Total de Projetos", total_p)
c2.metric("Empresas Distintas", total_e)
c3.metric("Total de Pesquisadores", total_pesq)
c4.metric("Municípios Atendidos", df_f[df_f['Município'] != 'Não Informado']['Município'].nunique())

st.markdown("---")

# Ranking
col1, col2 = st.columns(2)

with col1:
    st.subheader("📍 Top 5 Municípios")
    top_m = df_f[df_f['Município'] != 'Não Informado']['Município'].value_counts().head(5)
    fig_m = px.bar(top_m, orientation='h', color_discrete_sequence=['steelblue'],
                   labels={'value': 'Quantidade Pesquisas'})
    fig_m.update_layout(yaxis_title="", showlegend=False, yaxis={'categoryorder': 'total ascending'}, margin=dict(l=0))
    fig_m.update_traces(texttemplate='%{x}', textposition='outside', textangle=0)
    st.plotly_chart(fig_m, use_container_width=True)

with col2:
    st.subheader("🌍 Top 5 Países Parceiros")
    p_inst = df_f[~df_f['País Instituição (ões) no Exterior'].isin(['Brasil', 'Não Informado'])][
        'País Instituição (ões) no Exterior']
    p_acordo = df_f[~df_f['País Acordo(s)/Convênio(s) de Cooperação com a FAPESP'].isin(['Brasil', 'Não Informado'])][
        'País Acordo(s)/Convênio(s) de Cooperação com a FAPESP']
    top_paises = pd.concat([p_inst, p_acordo]).value_counts().head(5)

    if not top_paises.empty:
        fig_paises = px.bar(top_paises, orientation='h', color_discrete_sequence=['#d62728'],
                            labels={'value': 'Quantidade Pesquisas', 'index': 'País'})
        fig_paises.update_layout(yaxis_title="", showlegend=False, yaxis={'categoryorder': 'total ascending'})
        fig_paises.update_traces(texttemplate='%{x}', textposition='outside', textangle=0)
        st.plotly_chart(fig_paises, use_container_width=True)
    else:
        st.info("Nenhum dado internacional para os filtros selecionados.")

# grafico Geografico
st.markdown("---")
st.subheader("🗺️ Distribuição Geográfica")

ctrl1_geo, ctrl2_geo = st.columns([1, 2])
with ctrl1_geo:
    view_type_geo = st.radio("Tipo de Visualização:", ["Comparativo %", "Quantitativo"], horizontal=True,
                             key="view_type_geo")
    ranking_geo = st.radio("Filtro de Ranking:", ["Top 5", "Top 10", "Mostrar Todos", "Seleção Manual"],
                           horizontal=True, key="ranking_geo")

with ctrl2_geo:
    nivel_geo = st.radio("Escolha o nível geográfico:", ["Municípios", "Países", "Países e Municípios"],
                         horizontal=True, key="nivel_geo")


df_paises_series = pd.concat([
    df_f[~df_f['País Instituição (ões) no Exterior'].isin(['Brasil', 'Não Informado'])][
        'País Instituição (ões) no Exterior'],
    df_f[~df_f['País Acordo(s)/Convênio(s) de Cooperação com a FAPESP'].isin(['Brasil', 'Não Informado'])][
        'País Acordo(s)/Convênio(s) de Cooperação com a FAPESP']
])
dist_paises = df_paises_series.value_counts()
dist_municipios = df_f[df_f['Município'] != 'Não Informado']['Município'].value_counts()

if nivel_geo == "Municípios":
    dist_data_geo = dist_municipios
    color_geo = 'steelblue'
elif nivel_geo == "Países":
    dist_data_geo = dist_paises
    color_geo = '#d62728'
else:
    dist_data_geo = pd.concat([dist_paises, dist_municipios])
    dist_data_geo = dist_data_geo.groupby(dist_data_geo.index).sum().sort_values(ascending=False)

n_rank_geo = 5 if ranking_geo == "Top 5" else 10 if ranking_geo == "Top 10" else None

if view_type_geo == "Comparativo %":
    fig_geo = go.Figure()
    fig_geo.add_trace(
        go.Pie(values=[1], labels=["Nenhum"], marker=dict(colors=['#E5E5E5']), showlegend=False, textinfo='none',
               hoverinfo='none'))
    fig_geo.add_trace(
        go.Pie(values=dist_data_geo.values, labels=dist_data_geo.index, marker=dict(colors=px.colors.qualitative.Safe),
               textinfo='percent', hoverinfo='label+percent+value'))
    if ranking_geo == "Seleção Manual":
        fig_geo.update_layout(hiddenlabels=dist_data_geo.index.tolist())
    elif n_rank_geo:
        labels_to_hide = [label for label in dist_data_geo.index if
                          label not in dist_data_geo.nlargest(n_rank_geo).index]
        fig_geo.update_layout(hiddenlabels=labels_to_hide)
    fig_geo.update_layout(margin=dict(t=30, b=30, l=30, r=30),
                          legend=dict(orientation="v", yanchor="middle", y=0.5, xanchor="left", x=1.05))
else:
    if nivel_geo == "Países e Municípios":
        c_sel1, c_sel2 = st.columns(2)
        with c_sel1:
            default_p = [] if ranking_geo == "Seleção Manual" else dist_paises.nlargest(
                n_rank_geo).index.tolist() if n_rank_geo else dist_paises.index.tolist()
            sel_paises = st.multiselect("Selecione Países:", options=dist_paises.index.tolist(), default=default_p)
        with c_sel2:
            default_m = [] if ranking_geo == "Seleção Manual" else dist_municipios.nlargest(
                n_rank_geo).index.tolist() if n_rank_geo else dist_municipios.index.tolist()
            sel_muns = st.multiselect("Selecione Municípios:", options=dist_municipios.index.tolist(),
                                      default=default_m)
        filtered_p = dist_paises[dist_paises.index.isin(sel_paises)]
        filtered_m = dist_municipios[dist_municipios.index.isin(sel_muns)]
        fig_geo = go.Figure()
        if not filtered_p.empty: fig_geo.add_trace(
            go.Bar(y=filtered_p.index, x=filtered_p.values, orientation='h', name='Países', marker_color='#d62728',
                   text=filtered_p.values, textposition='auto'))
        if not filtered_m.empty: fig_geo.add_trace(
            go.Bar(y=filtered_m.index, x=filtered_m.values, orientation='h', name='Municípios',
                   marker_color='steelblue', text=filtered_m.values, textposition='auto'))
        fig_geo.update_traces(texttemplate='%{x}', textposition='outside', textangle=0)
        fig_geo.update_layout(height=max(300, (len(filtered_p) + len(filtered_m)) * 35), barmode='group',
                              yaxis={'categoryorder': 'total ascending'}, showlegend=True)
    else:
        default_geo = [] if ranking_geo == "Seleção Manual" else dist_data_geo.nlargest(
            n_rank_geo).index.tolist() if n_rank_geo else dist_data_geo.index.tolist()
        selected_geo = st.multiselect(f"Selecione {nivel_geo}:", options=dist_data_geo.index.tolist(),
                                      default=default_geo)
        if selected_geo:
            filtered_geo = dist_data_geo[dist_data_geo.index.isin(selected_geo)]
            fig_geo = go.Figure(
                go.Bar(y=filtered_geo.index, x=filtered_geo.values, orientation='h', marker_color=color_geo,
                       text=filtered_geo.values, textposition='auto'))
            fig_geo.update_traces(texttemplate='%{x}', textposition='outside', textangle=0)
            fig_geo.update_layout(height=max(300, len(filtered_geo) * 35), yaxis={'categoryorder': 'total ascending'})
        else:
            st.info("Selecione itens para visualizar.");
            fig_geo = go.Figure()
st.plotly_chart(fig_geo, use_container_width=True)

# grafico Áreas De Conhecimento
st.markdown("---")
st.subheader("🏢 Distribuição por Áreas do Conhecimento")
ctrl1, ctrl2 = st.columns([1, 2])
with ctrl1:
    view_type = st.radio("Tipo de Visualização:", ["Comparativo %", "Quantitativo"], horizontal=True,
                         key="view_type_radio")
    ranking_conhec = st.radio("Filtro de Ranking:", ["Top 5", "Top 10", "Mostrar Todos", "Seleção Manual"],
                              horizontal=True, key="ranking_conhec")
with ctrl2:
    nivel = st.radio("Escolha o nível para visualizar:", ["Grande Área", "Área", "Subárea"], horizontal=True,
                     key="nivel_radio")
col_map = {"Grande Área": "Grande Área do Conhecimento", "Área": "Área do Conhecimento",
           "Subárea": "Subárea do Conhecimento"}
selected_column = col_map[nivel]
dist_data = df_f[df_f[selected_column] != 'Não Informado'][selected_column].value_counts()
n_rank_conhec = 5 if ranking_conhec == "Top 5" else 10 if ranking_conhec == "Top 10" else None
if view_type == "Comparativo %":
    fig_dist = go.Figure()
    fig_dist.add_trace(
        go.Pie(values=[1], labels=["Nenhum"], marker=dict(colors=['#E5E5E5']), showlegend=False, textinfo='none',
               hoverinfo='none'))
    fig_dist.add_trace(
        go.Pie(values=dist_data.values, labels=dist_data.index, marker=dict(colors=px.colors.qualitative.Safe),
               textinfo='percent', hoverinfo='label+percent+value'))
    if ranking_conhec == "Seleção Manual":
        fig_dist.update_layout(hiddenlabels=dist_data.index.tolist())
    elif n_rank_conhec:
        labels_to_hide = [label for label in dist_data.index if label not in dist_data.nlargest(n_rank_conhec).index]
        fig_dist.update_layout(hiddenlabels=labels_to_hide)
    fig_dist.update_layout(margin=dict(t=30, b=30, l=30, r=30),
                           legend=dict(orientation="v", yanchor="middle", y=0.5, xanchor="left", x=1.05))
else:
    dist_data_sorted = dist_data.sort_values(ascending=False)
    default_conhec = [] if ranking_conhec == "Seleção Manual" else dist_data_sorted.nlargest(
        n_rank_conhec).index.tolist() if n_rank_conhec else dist_data_sorted.index.tolist()
    selected_categories = st.multiselect(f"Selecione as {nivel}s:", options=dist_data_sorted.index.tolist(),
                                         default=default_conhec)
    if selected_categories:
        filtered_dist_data = dist_data_sorted[dist_data_sorted.index.isin(selected_categories)].reindex(
            selected_categories)
        fig_dist = go.Figure(
            go.Bar(y=filtered_dist_data.index, x=filtered_dist_data.values, orientation='h', marker_color='darkorange',
                   text=filtered_dist_data.values, textposition='auto'))
        fig_dist.update_traces(texttemplate='%{x}', textposition='outside', textangle=0)
        fig_dist.update_layout(height=max(300, len(filtered_dist_data) * 35),
                               yaxis={'categoryorder': 'total ascending'}, showlegend=False)
    else:
        st.info("Selecione categorias.");
        fig_dist = go.Figure()
st.plotly_chart(fig_dist, use_container_width=True)

# grafico Pesquisadores
st.markdown("---")
st.subheader("👥 Distribuição por Pesquisadores")

ctrl1_p, ctrl2_p = st.columns([1, 2])
with ctrl1_p:
    view_type_p = st.radio("Tipo de Visualização:", ["Comparativo %", "Quantitativo"], horizontal=True,
                           key="view_type_p")

with ctrl2_p:
    ranking_p = st.radio("Filtro de Ranking:", ["Categorizados", "Mostrar Todos", "Seleção Manual"],
                         horizontal=True,
                         key="ranking_p")

# Dados de pesquisadores
q_resp = count_unique_pesq(df_f, ['Pesquisador Responsável'])
q_principais_atuais = count_unique_pesq(df_f, ['Pesquisadores Principais (Atuais)'])
q_principais_ultimos = count_unique_pesq(df_f, ['Pesquisadores Principais (Últimos)'])
q_principais_anteriores = count_unique_pesq(df_f, ['Pesquisadores Principais (Anteriores)'])
q_associados = count_unique_pesq(df_f, ['Pesquisadores Associados'])
q_ext = count_unique_pesq(df_f, ['Pesquisador responsável no exterior'])

q_principais_geral = count_unique_pesq(df_f, ['Pesquisadores Principais (Atuais)', 'Pesquisadores Principais (Últimos)',
                                              'Pesquisadores Principais (Anteriores)'])

q_total_geral = total_pesq

ORDEM_PESQ = [
    "Responsáveis",
    "Responsáveis no Exterior",
    "Principais (Atuais)",
    "Principais (Últimos)",
    "Principais (Anteriores)",
    "Associados",
    "Total de pesquisadores Principais",
    "Total de pesquisadores"
]
CATEGORIZADOS = ["Responsáveis", "Responsáveis no Exterior", "Total de pesquisadores Principais", "Associados",
                 "Total de pesquisadores"]

dist_data_p = pd.Series({
    "Responsáveis": q_resp,
    "Responsáveis no Exterior": q_ext,
    "Principais (Atuais)": q_principais_atuais,
    "Principais (Últimos)": q_principais_ultimos,
    "Principais (Anteriores)": q_principais_anteriores,
    "Associados": q_associados,
    "Total de pesquisadores Principais": q_principais_geral,
    "Total de pesquisadores": q_total_geral
}).reindex(ORDEM_PESQ)

if view_type_p == "Comparativo %":
    fig_p = go.Figure()
    fig_p.add_trace(
        go.Pie(values=[1], labels=["Nenhum"], marker=dict(colors=['#E5E5E5']), showlegend=False, textinfo='none',
               hoverinfo='none'))

    cores_pesq = px.colors.qualitative.Pastel.copy()
    color_map_p = {
        "Responsáveis no Exterior": "#d62728",  # Vermelho
        "Total de pesquisadores": "darkorange"
    }

    fig_p.add_trace(
        go.Pie(values=dist_data_p.values, labels=dist_data_p.index,
               marker=dict(colors=[color_map_p.get(label, cores_pesq[i % len(cores_pesq)]) for i, label in
                                   enumerate(dist_data_p.index)]),
               textinfo='percent', hoverinfo='label+percent+value', sort=False))
    if ranking_p == "Seleção Manual":
        fig_p.update_layout(hiddenlabels=dist_data_p.index.tolist())
    elif ranking_p == "Categorizados":
        labels_to_hide = [label for label in dist_data_p.index if label not in CATEGORIZADOS]
        fig_p.update_layout(hiddenlabels=labels_to_hide)
    fig_p.update_layout(margin=dict(t=30, b=30, l=30, r=30),
                        legend=dict(orientation="v", yanchor="middle", y=0.5, xanchor="left", x=1.05))
else:
    default_p = [] if ranking_p == "Seleção Manual" else CATEGORIZADOS if ranking_p == "Categorizados" else ORDEM_PESQ
    selected_p = st.multiselect("Selecione as categorias para comparar:", options=ORDEM_PESQ, default=default_p)
    if selected_p:
        filtered_p = dist_data_p[dist_data_p.index.isin(selected_p)].reindex(
            [opt for opt in ORDEM_PESQ if opt in selected_p])

        cores_barras = []
        for label in filtered_p.index:
            if label == "Responsáveis no Exterior":
                cores_barras.append("#d62728")
            elif label == "Total de pesquisadores":
                cores_barras.append("darkorange")
            else:
                cores_barras.append("steelblue")

        fig_p = go.Figure(go.Bar(y=filtered_p.index, x=filtered_p.values, orientation='h', marker_color=cores_barras,
                                 text=filtered_p.values, textposition='auto'))
        fig_p.update_traces(texttemplate='%{x}', textposition='outside', textangle=0)
        fig_p.update_layout(height=max(300, len(filtered_p) * 60),
                            yaxis={'categoryorder': 'array', 'categoryarray': filtered_p.index.tolist()[::-1]})
    else:
        st.info("Selecione categorias para visualizar.");
        fig_p = go.Figure()
st.plotly_chart(fig_p, use_container_width=True)

# database tabela
st.markdown("---")
st.subheader("🔍 Explorador de Dados Dinâmico")
if st.checkbox("Ativar Explorador de Tabela", value=True):
    todas_colunas = df.columns.tolist()
    default_cols = ['Título', 'Empresa', 'Município', 'Grande Área do Conhecimento']
    default_cols = [c for c in default_cols if c in todas_colunas]
    colunas_selecionadas = st.multiselect("Escolha as features:", options=todas_colunas, default=default_cols)
    if colunas_selecionadas:
        configuracao_colunas = {}
        for col in colunas_selecionadas:
            if col == 'Título' or df_f[col].astype(str).str.len().max() > 5:
                configuracao_colunas[col] = st.column_config.TextColumn(col, width="large")
            else:
                configuracao_colunas[col] = st.column_config.Column(width="medium")
        st.dataframe(df_f[colunas_selecionadas].head(200), use_container_width=True, column_config=configuracao_colunas)
        st.info("💡 **Dica**: duplo clique para ver texto completo.")
    else:
        st.warning("Selecione pelo menos uma feature.")
st.caption("Dashboard FAPESP PIPE 2026 | Desenvolvido para análise quantitativa interativa.")
