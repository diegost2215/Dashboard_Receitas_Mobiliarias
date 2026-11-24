import pandas as pd
import streamlit as st
from copy import deepcopy
from datetime import date, datetime
import plotly.express as px
import dicionarios_my4 as dimy4
import plotly.graph_objects as go


ano_atual = 2025
color_palete = list(px.colors.qualitative.Antique) + list(px.colors.qualitative.T10)
st.set_page_config(layout ="wide", initial_sidebar_state="auto", page_title='Painel de Receitas', page_icon=None)

local_VA_CNAE = 'files/VAS_anuais.xlsx'
local_nfse = 'files/Arrecadação_item_lista.xlsx'
local_arrecadacao_simples = 'files/Arrecadacao_simples.xlsx'

@st.cache_data()
def load_data():
  Dados_nfse = pd.DataFrame()
  for ano in range(2018,2026):
    temp = pd.read_excel(local_nfse, sheet_name = str(ano))
    temp.insert(0, 'Ano', str(ano))
    Dados_nfse = pd.concat([Dados_nfse, temp], axis=0)

  Dados_nfse['Item_lista'] = Dados_nfse['Atividade'].str[:5].str.strip().str.zfill(5)
  Dados_nfse['Grupo_da_lista'] = (Dados_nfse['Item_lista'].str.split('.', expand=True)[0]).str.zfill(2)
  Dados_nfse['Desc. Grupo da lista']=Dados_nfse['Grupo_da_lista'] + '-' + Dados_nfse['Grupo_da_lista'].map(dimy4.itens_servicos)
  Dados_nfse['Desc. Item lista']=Dados_nfse['Item_lista'] + '-' + Dados_nfse['Item_lista'].map(dimy4.subitens_servicos)
  Dados_nfse['Desc. Item lista'] = Dados_nfse['Desc. Item lista'].fillna('Não Aplicável/Isento/Outro')
  Dados_nfse['Desc. Grupo da lista'] = Dados_nfse['Desc. Grupo da lista'].fillna('Não Aplicável/Isento/Outro')
  Dados_nfse['ISS Total NFSE'] = Dados_nfse['Valor ISS']+Dados_nfse['Valor ISS retido']
  Dados_nfse['Desc. Grupo da lista_TM']=Dados_nfse['Grupo_da_lista'] + '-' + Dados_nfse['Grupo_da_lista'].map(dimy4.grupos_servicos_para_treemap)
  Dados_nfse['Desc. Item lista_TM']=Dados_nfse['Item_lista'] + '-' + Dados_nfse['Item_lista'].map(dimy4.subitens_servicos_treemap)
  Dados_nfse['Desc. Item lista_TM'] = Dados_nfse['Desc. Item lista_TM'].fillna('Não Aplicável/Isento/Outro')
  Dados_nfse['Desc. Grupo da lista_TM'] = Dados_nfse['Desc. Grupo da lista_TM'].fillna('Não Aplicável/Isento/Outro')
  Dados_nfse['Desc. Item lista_TM'] = Dados_nfse['Desc. Item lista_TM'].fillna('Não Aplicável/Isento/Outro')



  Arrecadacoes_Simples = pd.read_excel(local_arrecadacao_simples)
  #Arrecadacoes_Simples = pd.DataFrame()

  VA_CNAE = pd.DataFrame()
  for ano in range(2020,2025):
    temp = pd.read_excel(local_VA_CNAE, sheet_name = str(ano))
    temp.insert(0, 'Ano', str(ano))
    VA_CNAE = pd.concat([VA_CNAE, temp], axis=0)
    VA_CNAE_Itajai = VA_CNAE[VA_CNAE['Codigo do Município']==81612]

  return Dados_nfse, Arrecadacoes_Simples, VA_CNAE_Itajai



Dados_nfse, Arrecadacoes_Simples, VA_CNAE_Itajai = load_data()



#construção das métricas

valor_servicos_ano_atual = Dados_nfse[Dados_nfse['Ano']==str(ano_atual)]['Valor serviços'].sum()
valor_servicos_ano_anterior = Dados_nfse[Dados_nfse['Ano']==str(ano_atual-1)]['Valor serviços'].sum()
valor_servicos_delta = (valor_servicos_ano_atual-valor_servicos_ano_anterior)/valor_servicos_ano_anterior*100

n_notas_ano_atual = Dados_nfse[Dados_nfse['Ano']==str(ano_atual)]['Qtd.'].sum()
n_notas_ano_anterior = Dados_nfse[Dados_nfse['Ano']==str(ano_atual-1)]['Qtd.'].sum()
n_notas_delta = (n_notas_ano_atual-n_notas_ano_anterior)/n_notas_ano_anterior*100

valor_ISS_nota_ano_atual = Dados_nfse[Dados_nfse['Ano']==str(ano_atual)]['ISS Total NFSE'].sum()
valor_ISS_nota_ano_anterior = Dados_nfse[Dados_nfse['Ano']==str(ano_atual-1)]['ISS Total NFSE'].sum()
valor_ISS_nota_delta = (valor_ISS_nota_ano_atual-valor_ISS_nota_ano_anterior)/valor_ISS_nota_ano_anterior*100

Arrecadacao_Simples_ano_atual = Arrecadacoes_Simples[Arrecadacoes_Simples['Ano']==ano_atual]['Arrecadação_simples'].sum()
Arrecadacao_Simples_ano_anterior = Arrecadacoes_Simples[Arrecadacoes_Simples['Ano']==(ano_atual-1)]['Arrecadação_simples'].sum()
Arrecadacao_Simples_delta = (Arrecadacao_Simples_ano_atual-Arrecadacao_Simples_ano_anterior)/Arrecadacao_Simples_ano_anterior*100

ano_recente_Icms = ano_atual-1
VA_ICMS_ano_recevente = VA_CNAE_Itajai[(VA_CNAE_Itajai['Ano']==str(ano_recente_Icms))]['Valor Adicionado'].sum()  #ICMS vai ter defasagem de dois anos
VA_ICMS_ano_recevente_anterior = VA_CNAE_Itajai[(VA_CNAE_Itajai['Ano']==str(ano_recente_Icms-1))]['Valor Adicionado'].sum()  #ICMS vai ter defasagem de dois anos
VA_ICMS_delta = (VA_ICMS_ano_recevente-VA_ICMS_ano_recevente_anterior)/VA_ICMS_ano_recevente_anterior*100







with st.container(border=True):
  col1_A,col1_B,col1_C, col1_D,col1_E = st.columns([0.25, 0.25, 0.25, 0.25, 0.25])
  with col1_A:
    metric1 = st.metric(label = "Valor dos Serviços", value = f'R$ {round(valor_servicos_ano_atual/1000000,2)} mi.', delta= f'{round(valor_servicos_delta,2)} %')
  with col1_B:
    metric2 = st.metric(label = "Notas Emitidas", value = f'{round(n_notas_ano_atual/1000000,2)} mi.', delta= f'{round(n_notas_delta,2)} %')
  with col1_C:
    metric3 = st.metric(label = "Arecadação ISS (NFSE)", value = f'R$ {round(valor_ISS_nota_ano_atual/1000000, 2)} mi.', delta= f'{round(valor_ISS_nota_delta,2)} %')
  with col1_D:
    metric4 = st.metric(label = "Arecadação Simples Nacional", value = f'R$ {round(Arrecadacao_Simples_ano_atual/1000000, 2)} mi.', delta= f'{round(Arrecadacao_Simples_delta,2)} %')
  with col1_E:
    metric5 = st.metric(label = "Valor Adicionado (ICMS)", value = f'R$ {round(VA_ICMS_ano_recevente/1000000, 2)} mi.', delta= f'{round(VA_ICMS_delta,2)} %')



with st.container(border=True):
  df_todos_item = pd.pivot_table(Dados_nfse, index = ['Ano', 'Desc. Item lista'], values= ['Valor serviços','ISS Total NFSE', 'Qtd.'], aggfunc='sum')
  df_total_anual = pd.pivot_table(Dados_nfse, index = 'Ano', values= ['Valor serviços','ISS Total NFSE', 'Qtd.'], aggfunc='sum')
  df_total_anual.reset_index(inplace=True)
  df_todos_item.reset_index(inplace=True)
  df_total_anual["Crescimento Serviços % (todos itens)"] = df_total_anual['Valor serviços'].pct_change() * 100
  df_total_anual["Crescimento ISS % (todos itens)"] = df_total_anual['ISS Total NFSE'].pct_change() * 100

  pills_options_ISS_bar = ["ISS (todos itens)", "ISS por item da lista²", "Valor dos Serviços (item da lista)",
                           "Valor dos Serviços (todos itens)", "Crescimento anual ISS % (todos itens)", "Crescimento anual Serviços % (todos itens)", 'Notas emitidas por item', 'Notas Emitidas Total']
  pills_options_ISS_line = ["Inativo", "ISS (todos itens)", "Valor dos Serviços (todos itens)",
                            "Crescimento anual ISS % (todos itens)", "Crescimento anual Serviços % (todos itens)"]

  option_ISS_bar = st.pills("Informação Barras", options=pills_options_ISS_bar, selection_mode ='single', default = pills_options_ISS_bar[0], required=True, width='stretch')
  option_ISS_line = st.pills("Informação Linhas", options=pills_options_ISS_line, selection_mode ='single', default = pills_options_ISS_line[0], required=True, width='stretch')
  servicos_selecionados_disabled = False if option_ISS_bar in ["ISS por item da lista²", "Valor dos Serviços (item da lista)", 'Notas emitidas por item'] else True
  servicos_selecionados = st.multiselect("Selecione os Serviços", options = list(df_todos_item['Desc. Item lista'].unique()), 
                                        default =list(df_todos_item['Desc. Item lista'].unique())[0],  disabled =servicos_selecionados_disabled)
  df_item = df_todos_item[df_todos_item['Desc. Item lista'].isin(servicos_selecionados)]
  
  dict_pills_ISS = {"ISS (todos itens)":(df_total_anual, 'ISS Total NFSE'),
                  "ISS por item da lista²":(df_item, 'ISS Total NFSE'),
                  "Valor dos Serviços (item da lista)":(df_item, 'Valor serviços'),
                  "Valor dos Serviços (todos itens)":(df_total_anual, 'Valor serviços'),
                  "Crescimento anual ISS % (todos itens)":(df_total_anual, "Crescimento ISS % (todos itens)"),
                  "Crescimento anual Serviços % (todos itens)":(df_total_anual, 'Crescimento Serviços % (todos itens)'),
                  'Notas emitidas por item':(df_item, 'Qtd.'), 'Notas Emitidas Total':(df_total_anual, 'Qtd.')
                  }

  
  # Criando a figura
  # Adicionando as Barras
  if option_ISS_bar in ["ISS por item da lista²", "Valor dos Serviços (item da lista)", 'Notas emitidas por item']:
    fig_1a = px.bar(
        x=(dict_pills_ISS[option_ISS_bar][0])['Ano'],
        y=(dict_pills_ISS[option_ISS_bar][0])[dict_pills_ISS[option_ISS_bar][1]],
        color =(dict_pills_ISS[option_ISS_bar][0])['Desc. Item lista'],
        barmode ='group',
        color_discrete_sequence=color_palete
    )
  else:
    fig_1a = px.bar(
        x=(dict_pills_ISS[option_ISS_bar][0])['Ano'],
        y=(dict_pills_ISS[option_ISS_bar][0])[dict_pills_ISS[option_ISS_bar][1]],
        color_discrete_sequence=color_palete
    )


  if option_ISS_line != 'Inativo':
    # Adicionando a Linha
    fig_1a.add_trace(go.Scatter(
        x=(dict_pills_ISS[option_ISS_line][0])['Ano'],
        y=(dict_pills_ISS[option_ISS_line][0])[dict_pills_ISS[option_ISS_line][1]],
        name=option_ISS_line,
        yaxis='y2',
        mode='lines+markers',
        line=dict(color='black', width=3)
    ))

  fig_1a.update_layout(
      title={
          'text': f'ISS: Evolução do {option_ISS_bar} e {option_ISS_line}',
          'x': 0.5,             # Centraliza o título horizontalmente
          'xanchor': 'center',  # Define a âncora no centro
          'yanchor': 'top'
      },

      template='plotly_white',
      xaxis=dict(
          title=dict(
              text='<b>Ano</b>', # Título do eixo X em negrito
              font=dict(color='black')
          ),
          tickfont=dict(color='black')
      ),
      yaxis=dict(
          title=dict(
              text=option_ISS_bar,  # Título do eixo Y em negrito
              font=dict(color='black')
          ),
          tickfont=dict(color='black')
      ),
      yaxis2=dict(
          title=dict(
              text= option_ISS_line, # Título do eixo Y2
              font=dict(color='black')
          ),
          tickfont=dict(color='black'),
          overlaying='y',
          side='right',

      ),
  )
  # Exibindo o gráfico

  fig_1a.update_layout(
      legend=dict(
          orientation="h",       # Torna a legenda horizontal
          yanchor="bottom",      # Ancora a base da caixa de legenda
          y=-0.25,               # Move para baixo da área do gráfico (valor negativo)
          xanchor="center",      # Centraliza a legenda
          x=0.5,                  # Posição centralizada no eixo X
          title=None,
          font=dict(size=10)
      ),
      margin=dict(b=80)          # Aumenta a margem inferior para dar espaço à legenda
  )
  fig_1a.update_layout(colorway=color_palete)
  st.plotly_chart(fig_1a,  use_container_width=True,    width="stretch")


with st.container(border=True):
  dado_px_tree = st.pills('Selecione a Informação', options = ['ISS Total NFSE', 'Valor serviços'],selection_mode ='single',
                          default = 'Valor serviços', required =True)


  df_Iss_px_tree = Dados_nfse[Dados_nfse['Ano']==str(ano_atual)]

  fig_2a = px.treemap(
      df_Iss_px_tree,
      path=['Ano', 'Desc. Grupo da lista_TM', 'Desc. Item lista_TM'],
      values=dado_px_tree,
      maxdepth=2,
      height = 600
  )

  fig_2a.update_traces(textinfo='label+value+percent root')
  fig_2a.update_traces(hovertemplate='%{label}<br>',textfont=dict(size=16), marker=dict(cornerradius=8), marker_line_color="black")
  fig_2a.update_layout(margin=dict(t=2, b=2, l=2, r=2))
  fig_2a.update_layout(colorway=color_palete)
  st.plotly_chart(fig_2a,  use_container_width=True,    width="stretch")


with st.container(border=True):
    itens_VA_CNAE = list(VA_CNAE_Itajai['Descrição Atividade'].unique())
    itens_VA_CNAE_Selecionados = st.multiselect("Selecione as Atividades", options = itens_VA_CNAE, default =itens_VA_CNAE[0:3],)
    fig_4a = px.bar(VA_CNAE_Itajai[VA_CNAE_Itajai['Descrição Atividade'].isin(itens_VA_CNAE_Selecionados)],
        x='Ano',
        y='Valor Adicionado',
        color ='Descrição Atividade',
        barmode ='group',
        color_discrete_sequence=color_palete)

    fig_4a.update_layout(
        legend=dict(
            orientation="h",       # Torna a legenda horizontal
            yanchor="bottom",      # Ancora a base da caixa de legenda
            y=-0.25,               # Move para baixo da área do gráfico (valor negativo)
            xanchor="center",      # Centraliza a legenda
            x=0.5,                  # Posição centralizada no eixo X
            title=None,
            font=dict(size=10)
        ),
        margin=dict(b=80),          # Aumenta a margem inferior para dar espaço à legenda
        template='plotly_white'
    )

    st.plotly_chart(fig_4a,  use_container_width=True,    width="stretch")
