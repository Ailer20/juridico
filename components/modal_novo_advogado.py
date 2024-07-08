import dash
import plotly.express as px
from dash import html, dcc
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
import pandas as pd
from components import modal_novo_advogado, modal_advogados, modal_novo_processo

from app import app
import sqlite3
from sql_beta import df_adv

    
def insert_adv(nome, oab):
    conn = sqlite3.connect('sistema.db')
    c = conn.cursor()
    c.execute('''
        INSERT INTO advogados (Advogado, OAB)
        VALUES (?, ?)
    ''', (nome, oab))
    conn.commit()
    conn.close()

# Função para recuperar dados do banco de dados
def get_adv():
    conn = sqlite3.connect('sistema.db')
    c = conn.cursor()
    c.execute('SELECT * FROM advogados')
    rows = c.fetchall()
    conn.close()
    return rows

# ========= Layout ========= #
layout = dbc.Modal([
            dbc.ModalHeader(dbc.ModalTitle("Adicione Um Advogado")),
            dbc.ModalBody([
                dbc.Row([
                    dbc.Col([
                        dbc.Label("OAB"),
                        dbc.Input(id="adv_oab", placeholder="Apenas números, referente a OAB...", type="number")
                    ], sm=12, md=6),
                ]),
                dbc.Row([
                    dbc.Col([
                        dbc.Label("Nome"),
                        dbc.Input(id="adv_nome", placeholder="Nome completo do advogado...", type="text")
                    ]),
                ]),
                html.H5(id='div_erro2_adv')  # Alterado para garantir unicidade
            ]),
            dbc.ModalFooter([
                dbc.Button("Cancelar", id="cancel_button_novo_advogado", color="danger"),
                dbc.Button("Salvar", id="save_button_novo_advogado", color="success")
            ])
        ], id="modal_new_lawyer", size="lg", is_open=False)


# ======= Callbacks ======== #
# Callback para adicionar novos advogados
@app.callback(
    Output('store_adv', 'data'),
    Output('div_erro2_adv', 'children'),  # Alterado para garantir unicidade
    Output('div_erro2_adv', 'style'),  # Alterado para garantir unicidade
    Input('save_button_novo_advogado', 'n_clicks'),
    State('store_adv', 'data'),
    State('adv_nome', 'value'),
    State('adv_oab', 'value'),
)
def novo_adv(n_clicks, dataset, advogado, oab):
    if n_clicks:
        if None in [advogado, oab]:
            return dataset, ["Todos dados são obrigatórios para registro!"], {'margin-bottom': '15px', 'color': 'red', 'text-shadow': '2px 2px 8px #000000'}

        # Convertendo o dataset em DataFrame para manipulação
        df_adv = pd.DataFrame(dataset)

        if oab in df_adv['OAB'].values:
            return dataset, ["Número de OAB já existe no sistema!"], {'margin-bottom': '15px', 'color': 'red', 'text-shadow': '2px 2px 8px #000000'}
        elif advogado in df_adv['Advogado'].values:
            return dataset, [f"Nome {advogado} já existe no sistema!"], {'margin-bottom': '15px', 'color': 'red', 'text-shadow': '2px 2px 8px #000000'}

        # Insere o novo advogado no banco de dados
        insert_adv(advogado, oab)

        # Adiciona o novo advogado ao DataFrame
        new_row = pd.DataFrame({'Advogado': [advogado], 'OAB': [oab]})
        df_adv = pd.concat([df_adv, new_row], ignore_index=True)
        
        # Converte de volta para dicionário
        dataset = df_adv.to_dict('list')
        return dataset, ["Cadastro realizado com sucesso!"], {'margin-bottom': '15px', 'color': 'green', 'text-shadow': '2px 2px 8px #000000'}
    
    return dataset, "", {}  # Retorno padrão