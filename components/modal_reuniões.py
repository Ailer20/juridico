import dash
from dash import html, dcc
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
import pandas as pd
from datetime import datetime
from app import app
import sqlite3
from sql_beta import df_reu, df_proc



# Função para inserir dados no banco de dados
def insert_reuniao(processo, data, hora, descricao):
    conn = sqlite3.connect('sistema.db')
    c = conn.cursor()
    c.execute('''
        INSERT INTO reunioes (processo, data, hora, descricao)
        VALUES (?, ?, ?, ?)
    ''', (processo, data, hora, descricao))
    conn.commit()
    conn.close()

# Função para recuperar dados do banco de dados
def get_reunioes():
    conn = sqlite3.connect('sistema.db')
    c = conn.cursor()
    c.execute('SELECT * FROM reunioes')
    rows = c.fetchall()
    conn.close()
    return rows


layout = html.Div(className='container-fluid', children=[
    dbc.Modal(
        [
            dbc.ModalHeader(dbc.ModalTitle("Reuniões")),
            dbc.ModalBody(children=[
                html.Div(className='row', children=[
                    html.Div(className='col-4', children=[
                        html.H3("Selecione um Mês"),
                        dcc.Dropdown(
                            id='filtro-mes',
                            options=[
                                {'label': 'Janeiro', 'value': 1},
                                {'label': 'Fevereiro', 'value': 2},
                                {'label': 'Março', 'value': 3},
                                {'label': 'Abril', 'value': 4},
                                {'label': 'Maio', 'value': 5},
                                {'label': 'Junho', 'value': 6},
                                {'label': 'Julho', 'value': 7},
                                {'label': 'Agosto', 'value': 8},
                                {'label': 'Setembro', 'value': 9},
                                {'label': 'Outubro', 'value': 10},
                                {'label': 'Novembro', 'value': 11},
                                {'label': 'Dezembro', 'value': 12},
                            ],
                            value=datetime.now().month,
                            clearable=False
                        )
                    ]),
                    html.Div(className='col-8', children=[
                        html.Div(id='reunioes')
                    ]),
                ])
            ]),
            dbc.ModalFooter(
                dbc.Button("Fechar", id="view_modal", className="ml-auto", n_clicks=0)
            ),
        ],
        id="reunioes-modal",
        size="lg",
        is_open=False
    ),
    dbc.Modal([
        dbc.ModalHeader(dbc.ModalTitle("Nova Reunião")),
        dbc.ModalBody([
            dbc.Row([
                dbc.Col([
                    dbc.Label("Selecione o Processo: "),
                    dcc.Dropdown(
                    id='processo_envolvidos',
                    options=[{'label': i, 'value': i} for i in df_proc['No Processo']],
                    className='dbc'
                    )
                ])
            ]),
            html.Br(),
            dbc.Row([
                dbc.Col([
                    dbc.Label("Data"),
                    dcc.DatePickerSingle(id='reu_date')
                ])
            ]),
            html.Br(),
            dbc.Row([
                dbc.Col([
                    dbc.Label("Hora"),
                    dbc.Input(type='time', id='reu_time')
                ])
            ]),
            dbc.Row([
                dbc.Col([
                    dbc.Label("Descrição"),
                    dbc.Textarea(id='reu_descrição')
                ])
            ]),
            dbc.Row([
                dbc.Col(html.Div(id='div_erro2'))
            ])
        ]),
        dbc.ModalFooter([
            dbc.Button("Cancelar", id="cancel_button_nova_reuniao", color="danger"),
            dbc.Button("Salvar", id="schedule_meeting_button", color="success")
        ])
    ], id='modal_nova_reuniao', is_open=False)
])

@app.callback(
    Output('store_reu', 'data'),
    Output('div_erro2', 'children'),
    Output('div_erro2', 'style'),
    Input('schedule_meeting_button', 'n_clicks'),
    State('store_reu', 'data'),
    State('processo_envolvidos', 'value'),
    State('reu_date', 'date'),
    State('reu_time', 'value'),
    State('reu_descrição', 'value')
)
def novo_reu(n_clicks, store_reu_data, processo, data, hora, descrição):
    if n_clicks:
        if None in [processo, data, hora, descrição]:
            return store_reu_data, ["Todos os dados são obrigatórios para registro!"], {'margin-bottom': '15px', 'color': 'red', 'text-shadow': '2px 2px 8px #000000'}
        
        insert_reuniao(processo, data, hora, descrição)
        return store_reu_data, ["Cadastro realizado com sucesso!"], {'margin-bottom': '15px', 'color': 'green', 'text-shadow': '2px 2px 8px #000000'}
    return store_reu_data, "", {}

@app.callback(
    Output('reunioes', 'children'),
    Input('filtro-mes', 'value'),
    Input('store_reu', 'data')
)
def update_reunioes(selected_mes,store_reu_data):
    reunioes_data = get_reunioes()
    df_reu = pd.DataFrame(reunioes_data, columns=['id', 'Processo', 'Data', 'Hora', 'Descricao'])

    # Filtrar os dados para o mês selecionado
    filtered_data = df_reu[pd.to_datetime(df_reu['Data']).dt.month == selected_mes]

    # Construir o layout dos cards de reunião
    reuniao_layout = []
    for index, row in filtered_data.iterrows():
        reuniao_layout.append(html.Div([
            html.H3(f"Reunião Referente ao Processo N° {row['Processo']}"),
            html.P(f"Data: {row['Data']}"),
            html.P(f"Hora: {row['Hora']}"),
            html.P(f"Descrição: {row['Descricao']}")
        ]))
        reuniao_layout.append(html.Hr())

    return reuniao_layout

@app.callback(
    Output('processo_envolvidos', 'options'),
    Input('store_proc', 'data')
)
def atu(data):
    df = pd.DataFrame(data)
    return [{'label': i, 'value': i} for i in df['No Processo']]


if __name__ == '__main__':
    app.run_server(debug=True)