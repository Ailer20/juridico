import dash
from dash import html, dcc
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
import pandas as pd
from datetime import datetime
from sql_beta import df_proc, df_reu
import sqlalchemy
from app import app
engine = sqlalchemy.create_engine('sqlite:///sistema.db')


# Ensure 'Data' column is in datetime format
df_reu['Data'] = pd.to_datetime(df_reu['Data'], errors='coerce').dt.date
# Layout of the page with buttons to open modals
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

app.layout = layout

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
def novo_reu(n, dataset, processo, data, hora, descrição):
    erro = []
    style = {}
    if n:
        if None in [processo, data, hora, descrição]:
            return dataset, ["Todos os dados são obrigatórios para registro!"], {'margin-bottom': '15px', 'color': 'red', 'text-shadow': '2px 2px 8px #000000'}

        df_reu = pd.DataFrame(dataset)
        
      
        # Adicionar nova reunião ao DataFrame
        new_row = pd.DataFrame([{'Processo': processo, 'Data': data, 'Hora': hora, 'Descrição': descrição}])
        df_reu = pd.concat([df_reu, new_row], ignore_index=True)
        
        # Atualizar o store
        dataset = df_reu.to_dict('records')

        # Salvar no banco de dados
        try:
            df_reu.to_sql('reuniao', con=engine, if_exists='replace', index=False)
            return dataset, ["Reunião agendada com sucesso!"], {'margin-bottom': '15px', 'color': 'green', 'text-shadow': '2px 2px 8px #000000'}
        except Exception as e:
            return dataset, [f"Erro ao salvar no banco de dados: {e}"], {'margin-bottom': '15px', 'color': 'red', 'text-shadow': '2px 2px 8px #000000'}

    return dataset, erro, style



@app.callback(
    Output('reunioes', 'children'),
    Input('filtro-mes', 'value'),
    Input('store_reu', 'data')
)
def update_reunioes(selected_mes, reunioes_data):
    df_reu = pd.DataFrame(reunioes_data)
    # Filtrar os dados para o mês selecionado
    filtered_data = df_reu[pd.to_datetime(df_reu['Data']).dt.month == selected_mes]

    # Construir o layout dos cards de reunião
    reuniao_layout = []
    for index, row in filtered_data.iterrows():
        reuniao_layout.append(html.Div([
            html.H3(f"Reunião Referente ao Processo N° {row['Processo']}"),
            html.P(f"Data: {row['Data']}"),
            html.P(f"Hora: {row['Hora']}"),
            html.P(f"Descrição: {row['Descrição']}")
        ]))
        reuniao_layout.append(html.Hr())

    return reuniao_layout

# Callbacks to open and close modals
@app.callback(
    Output('modal_nova_reuniao', 'is_open'),
    Input('reunioes_button', 'n_clicks'),
    Input('cancel_button_nova_reuniao', 'n_clicks'),
    State('modal_nova_reuniao', 'is_open')
)
def toggle_add_modal(n1, n2, is_open):
    if n1 or n2:
        return not is_open
    return is_open

@app.callback(
    Output('reunioes-modal', 'is_open'),
    Input('agenda_button', 'n_clicks'),
    Input('view_modal', 'n_clicks'),
    State('reunioes-modal', 'is_open')
)
def toggle_view_modal(n1, n2, is_open):
    if n1 or n2:
        return not is_open
    return is_open

@app.callback(
    Output('processo_envolvidos', 'options'),
    Input('store_proc', 'data')
)
def atu(data):
    df = pd.DataFrame(data)
    return [{'label': i, 'value': i} for i in df['No Processo']]


if __name__ == '__main__':
    app.run_server(debug=True)
