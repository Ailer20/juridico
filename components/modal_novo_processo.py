from logging import exception
import dash
import plotly.express as px
from dash import html, dcc, callback_context
from dash.dependencies import Input, Output, State, ALL
import dash_bootstrap_components as dbc
from datetime import timedelta, date
#from components import modal_novo_advogado, modal_advogados, modal_novo_processo
import sqlite3
import json
import pandas as pd

from app import app
#import components.modal_reuniões as modal_reuniões
from sql_beta import df_adv

col_centered_style={'display': 'flex', 'justify-content': 'center'}




# Função para inserir dados no banco de dados
def insert_processo(no_processo ,unidade, tipo, acao, contrato, cidade, vara, fase, instancia,
                    data_julgamento, data_inicial, data_final, processo_tramite,
                    processo_extinto, transito_julgado, advogado, cliente, cpf_cliente,
                    Descrição):
    conn = sqlite3.connect('sistema.db')
    c = conn.cursor()
    c.execute('''
        INSERT INTO processos ("No Processo", "Unidade", "Tipo", "Ação", "Contrato", "Cidade", "Vara",
                               "Fase", "Instância", "Data julgamento", "Data Inicial",
                               "Data Final", "Processo Tramite", "Processo Extinto",
                               "Transito julgado", "Advogado", "Cliente", "Cpf Cliente",
                               "Descrição")
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (no_processo, unidade, tipo, acao, contrato, cidade, vara, fase, instancia,
          data_julgamento, data_inicial, data_final, processo_tramite,
          processo_extinto, transito_julgado, advogado, cliente, cpf_cliente,
          Descrição))
    conn.commit()
    conn.close()
# Função para recuperar dados do banco de dados
def get_proc():
    conn = sqlite3.connect('sistema.db')
    c = conn.cursor()
    c.execute('SELECT * FROM processo')
    rows = c.fetchall()
    conn.close()
    return rows


# ========= Layout ========= #
layout = dbc.Modal([
            dbc.ModalHeader(dbc.ModalTitle("Adicione Um Processo")),
            dbc.ModalBody([
                dbc.Row([
                    dbc.Col([
                        # unidade
                        dbc.Label('Unidade', html_for='unidade_matriz'),
                        dcc.Dropdown(id='unidade_matriz', clearable=False, className='dbc',
                            options=['Amazonas', 'Roraima', 'Minas Gerais']),
                        # Tipo de Processo
                        dbc.Label('Tipo de Processo', html_for='tipo_processo'),
                        dcc.Dropdown(id='tipo_processo', clearable=False, className='dbc',
                            options=['Civil', 'Criminal', 'Previdenciário', 'Trabalhista', 'Vara de Família']),
                        # Tipo de Processo
                        dbc.Label('Ação', html_for='acao'),
                        dcc.Dropdown(id='acao', clearable=False, className='dbc',
                            options=['Danos Materiais', 'Danos Morais']),
                        #contrado envolvido
                        dbc.Label('Contrato Envolvido', html_for='contrato'),
                        dbc.Input(id="input_contrato", placeholder="Envolvido no processo", type="text"),
                        #cidade
                        dbc.Label('Cidade', html_for='cidade'),
                        dbc.Input(id="input_cidade", placeholder="Digite a Cidade", type="text"),
                    ], sm=12, md=4),
                    dbc.Col([
                        dbc.Label("Descrição", html_for='input_desc'),
                        dbc.Textarea(id="input_desc", placeholder="Escreva aqui observações sobre o processo...", style={'height': '80%'}),
                    ], sm=12, md=8)
                ]),
                html.Hr(),
                dbc.Row([
                    dbc.Col([
                        dbc.Label("Vara", html_for='vara'),
                        dbc.RadioItems(id='vara',
                            options=[{'label': 'Civil', 'value': 'Civil'},
                            {'label': 'Conciliação e Julgamento', 'value': 'Conciliação e Julgamento'},
                            {'label': 'Trabalhista', 'value': 'Trabalhista'},
                            {'label': 'Vara de Família', 'value': 'Vara de Família'}])
                    ], sm=12, md=4),
                    dbc.Col([
                        dbc.Label("Fase", html_for='fase'),
                        dbc.RadioItems(id='fase', inline=True,
                            options=[{'label': 'Contestação', 'value': 'Contestação'},
                            {'label': 'Conciliação', 'value': 'Conciliação'},
                            {'label': 'Impugnação', 'value': 'Impugnação'},
                            {'label': 'Instrução', 'value': 'Instrução'},
                            {'label': 'Recurso', 'value': 'Recurso'},
                            {'label': 'Suspenso', 'value': 'Suspenso'},
                             {'label': 'Solicitação de documentos', 'value': 'Solicitação'}
                            ])
                    ], sm=12, md=5),
                    dbc.Col([
                        dbc.Label("Instância", html_for='instancia'),
                        dbc.RadioItems(id='instancia',
                            options=[{'label': '1A Instância', 'value': 1},
                            {'label': '2A Instância', 'value': 2},])
                    ], sm=12, md=3),
                    html.Hr(),
                    dbc.Row([
                        dbc.Col([
                            dbc.Row([
                                dbc.Col([
                                        dbc.Label("Data do Julgamento")
                                    ], style=col_centered_style),
                                dbc.Col([
                                    dcc.DatePickerSingle(
                                        id='data_julgamento',
                                        className='dbc',
                                        min_date_allowed=date(1999, 12, 31),
                                        max_date_allowed=date(2030, 12, 31),
                                        initial_visible_month=date.today(),
                                        date=date.today()
                                        )])
                                ], style=col_centered_style),
                            ], sm=12, md=5),
                        ]),
                ], style=col_centered_style),
                html.Hr(),
                dbc.Row([
                    dbc.Col([
                        dbc.Row([
                            dbc.Col([
                                dbc.Label("Data Inicial - Data Final")
                            ], style=col_centered_style),
                            dbc.Col([
                                dcc.DatePickerSingle(
                                    id='data_inicial',
                                    className='dbc',
                                    min_date_allowed=date(1999, 12, 31),
                                    max_date_allowed=date(2030, 12, 31),
                                    initial_visible_month=date.today(),
                                    date=date.today()
                                ),
                                dcc.DatePickerSingle(
                                    id='data_final',
                                    className='dbc',
                                    min_date_allowed=date(1999, 12, 31),
                                    max_date_allowed=date(2030, 12, 31),
                                    initial_visible_month=date.today(),
                                    date=None
                                ),
                            ], style=col_centered_style)
                        ]),
                        html.Br(),
                        dbc.Switch(id='processo_concluido', label="Processo em Trâmite", value=False),
                        dbc.Switch(id='processo_vencido', label="Processo Extinto", value=False),
                        dbc.Switch(id='transito_julgado', label="Transito em Julgado", value=False),
                        html.P("O filtro de data final só será computado se o checklist estiver marcado.", className='dbc', style={'font-size': '80%'}),
                    ], sm=12, md=5),
                    dbc.Col([
                        dbc.Row([
                            dbc.Col([
                                dbc.Label("Selecione o advogado responsável: "),
                                dcc.Dropdown(
                                    id='advogados_envolvidos',
                                    options=[{'label': i, 'value': i} for i in df_adv['Advogado']],
                                    className='dbc'
                                )
                            ])
                        ]),
                        dbc.Row([
                            dbc.Col([
                                dbc.Input(id="input_cliente", placeholder="Nome completo do Reclamante/Autor...", type="text")
                            ])
                        ], style={'margin-top': '15px', 'padding': '15px'}),
                        dbc.Row([
                            dbc.Col([
                                dbc.Input(id="input_cliente_cpf", placeholder="CPF do Reclamante/Autor (apenas números)...", type="number")
                            ])
                        ], style={'padding': '15px'}),
                    ], sm=12, md=7)
                ]),
                dbc.Row([
                    dbc.Col([
                        dcc.Dropdown(id='input_local_arquivo', clearable=False, className='dbc', placeholder="Local de Arquivo/Local Físico",
                            options=['Armário Principal', 'Armário 17 gaveta 2', 'Armário 5 gaveta 1', 'Arquivo 01', 'Arquivo 02']),
                    ], sm=12, md=5, style={'padding': '15px'}),
                    dbc.Col([
                        dbc.Input(id="input_no_processo", placeholder="Insira o número do Processo", type="number", disabled=False)
                    ], sm=12, md=7, style={'padding': '15px'})
                ], style={'margin-top': '15px'}),
                html.H5(id='div_erro')
            ]),
            dbc.ModalFooter([
                dbc.Button("Cancelar", id="cancel_button_novo_processo", color="danger"),
                dbc.Button("Salvar", id="save_button_novo_processo", color="success"),
            ]),
        ], id="modal_processo", size="lg", is_open=False)

# Callback para teste de abrir o modal
@app.callback(
    Output('modal_processo', 'is_open'),
    Output('store_intermedio', 'data'),
    Input({'type': 'editar_processo', 'index': ALL}, 'n_clicks'),
    Input('processo_button', 'n_clicks'),
    Input("cancel_button_novo_processo", 'n_clicks'),
    State('modal_processo', 'is_open'),
    State('store_proc', 'data'),
    State('store_intermedio', 'data')
)
def abrir_modal_processo(n_editar, n_new, n_cancel, is_open, store_proc, store_intermedio):
    trigg_id = callback_context.triggered[0]['prop_id'].split('.')[0]
    first_call = True if callback_context.triggered[0]['value'] == None else False
    if first_call:
        return is_open, store_intermedio

    if (trigg_id == 'processo_button') or (trigg_id == 'cancel_button_novo_processo'):
        df_int = pd.DataFrame(store_intermedio)
        df_int = df_int[:-1]
        store_intermedio = df_int.to_dict()

        return not is_open, store_intermedio

    if n_editar:
        trigg_dict = json.loads(callback_context.triggered[0]['prop_id'].split('.')[0])
        numero_processo = trigg_dict['index']

        df_int = pd.DataFrame(store_intermedio)
        df_proc = pd.DataFrame(store_proc)

        valores = df_proc.loc[df_proc['No Processo'] == numero_processo].values.tolist()
        valores = valores[0] + [True]

        df_int = df_int[:-1]
        df_int.loc[len(df_int)] = valores
        store_intermedio = df_int.to_dict()

        return not is_open, store_intermedio

# Callback para CRUD de processos
@app.callback(
    Output('store_proc', 'data'),
    Output('div_erro', 'children'),
    Output('div_erro', 'style'),
    Output('input_no_processo', 'value'),
    Output('unidade_matriz', 'value'),
    Output('tipo_processo', 'value'),
    Output('acao', 'value'),
    Output('input_contrato', 'value'),
    Output('input_cidade', 'value'),
    Output('vara', 'value'),
    Output('fase', 'value'),
    Output('instancia', 'value'),
    Output('data_julgamento', 'date'),
    Output('data_inicial', 'date'),
    Output('data_final', 'date'),
    Output('processo_concluido', 'value'),
    Output('processo_vencido', 'value'),
    Output('transito_julgado', 'value'),
    Output('advogados_envolvidos', 'value'),
    Output('input_cliente', 'value'),
    Output('input_cliente_cpf', 'value'),
    Output('input_desc', 'value'),
    Output('input_no_processo', 'disabled'),
    Input('processo_button', 'n_clicks'),
    Input('save_button_novo_processo', 'n_clicks'),
    Input({'type': 'deletar_processo', 'index': ALL}, 'n_clicks'),
    Input('store_intermedio', 'data'),
    State('modal_processo', 'is_open'),
    State('store_proc', 'data'),
    State('input_no_processo', 'value'),
    State('unidade_matriz', 'value'),
    State('tipo_processo', 'value'),
    State('acao', 'value'),
    State('input_contrato', 'value'),
    State('input_cidade', 'value'),
    State('vara', 'value'),
    State('fase', 'value'),
    State('instancia', 'value'),
    State('data_julgamento', 'date'),
    State('data_inicial', 'date'),
    State('data_final', 'date'),
    State('processo_concluido', 'value'),
    State('processo_vencido', 'value'),
    State('transito_julgado', 'value'),
    State('advogados_envolvidos', 'value'),
    State('input_cliente', 'value'),
    State('input_cliente_cpf', 'value'),
    State('input_desc', 'value'),
    prevent_initial_call=True
)
def crud_processos(n_new, n_save, n_delete, store_int, is_open, store_proc, no_processo, unidade, tipo, acao, contrato, cidade,  vara, fase, instancia, data_julgamento, data_inicial, data_final, processo_concluido, processo_vencido, transito_julgado, advogados, cliente, cpf_cliente, Descrição):
    first_call = True if (callback_context.triggered[0]['value'] == None or callback_context.triggered[0]['value'] == False) else False
    trigg_id = callback_context.triggered[0]['prop_id'].split('.')[0]

    if first_call:
        no_processo = unidade = tipo = acao = contrato = cidade = vara = fase = instancia = data_julgamento = data_inicial = data_final = advogados = cliente = cpf_cliente = Descrição = None
        processo_concluido = processo_vencido = transito_julgado = False
        return store_proc, [], {}, no_processo, unidade, tipo, acao, contrato, cidade, vara, fase, instancia, data_julgamento, data_inicial, data_final, processo_concluido, processo_vencido, transito_julgado, advogados, cliente, cpf_cliente, Descrição, False

    if trigg_id == 'save_button_novo_processo':
        df_proc = pd.DataFrame(store_proc)
        df_int = pd.DataFrame(store_int)
        
        if len(df_int.index) == 0:  # Novo processo
            if None in [no_processo, unidade, tipo, acao, contrato, cidade, vara, fase, instancia, data_julgamento, data_inicial, data_final, processo_concluido, processo_vencido, transito_julgado, advogados, cliente, cpf_cliente, Descrição]:
                return store_proc, ["Todos os dados são obrigatórios para registro!"], {'margin-bottom': '15px', 'color': 'red'}, no_processo, unidade, tipo, acao, contrato, cidade, vara, fase, instancia, data_julgamento, data_inicial, data_final, processo_concluido, processo_vencido, transito_julgado, advogados, cliente, cpf_cliente, Descrição, False
            if no_processo in df_proc['No Processo'].values:
                return store_proc, ["Número de processo já existe no sistema!"], {'margin-bottom': '15px', 'color': 'red'}, no_processo, unidade, tipo, acao, contrato, cidade, vara, fase, instancia, data_julgamento, data_inicial, data_final, processo_concluido, processo_vencido, transito_julgado, advogados, cliente, cpf_cliente, Descrição, False

            data_julgamento = pd.to_datetime(data_julgamento).date() if data_julgamento else None
            data_inicial = pd.to_datetime(data_inicial).date() if data_inicial else None
            data_final = pd.to_datetime(data_final).date() if data_final else None

            insert_processo(no_processo, unidade, tipo, acao, contrato, cidade, vara, fase, instancia, data_julgamento, data_inicial, data_final, processo_concluido, processo_vencido, transito_julgado, advogados, cliente, cpf_cliente, Descrição)
            
            # Verifique se df_proc está inicializado corretamente com as colunas necessárias
            if df_proc.empty:
                df_proc = pd.DataFrame(columns=['No Processo', 'Unidade', 'Tipo', 'Ação', 'Contrato', 'Cidade', 'Vara', 'Fase', 'Instância',
                                                'Data Julgamento', 'Data Inicial', 'Data Final', 'Processo Concluído', 'Processo Vencido',
                                                'Trânsito Julgado', 'Advogados', 'Cliente', 'CPF Cliente', 'Descrição'])

            # Depois, ao adicionar um novo processo
            df_proc.loc[df_proc.shape[0]] = [no_processo, unidade, tipo, acao, contrato, cidade, vara, fase, instancia, data_julgamento, data_inicial, data_final,
                                            processo_concluido, processo_vencido, transito_julgado, advogados, cliente, cpf_cliente, Descrição]

            store_proc = df_proc.to_dict()
            no_processo = unidade = tipo = acao = contrato = cidade = vara = fase = instancia = data_julgamento = data_inicial = data_final = advogados = cliente = cpf_cliente = Descrição = None
            processo_concluido = processo_vencido = transito_julgado = False
            return store_proc, ['Processo salvo com sucesso!'], {'margin-bottom': '15px', 'color': 'green'}, no_processo, unidade, tipo, acao, contrato, cidade, vara, fase, instancia, data_julgamento, data_inicial, data_final, processo_concluido, processo_vencido, transito_julgado, advogados, cliente, cpf_cliente, Descrição, False

        else:  # Edição de processo
            processo_concluido = 0 if processo_concluido == False else 1
            processo_vencido = 0 if processo_vencido == False else 1
            transito_julgado = 0 if transito_julgado == False else 1
            if processo_concluido == 0: data_final = None

            index = df_proc.loc[df_proc['No Processo'] == no_processo].index[0]
            df_proc.loc[index, df_proc.columns] = [no_processo, unidade, tipo, acao, contrato, cidade, vara, fase, instancia, data_julgamento, data_inicial, data_final, processo_concluido, processo_vencido, transito_julgado, advogados, cliente, cpf_cliente, Descrição]
            
            store_proc = df_proc.to_dict()
            no_processo = unidade = tipo = acao = contrato = cidade = vara = fase = instancia = data_julgamento = data_inicial = data_final = advogados = cliente = cpf_cliente = Descrição = None
            processo_concluido = processo_vencido = transito_julgado = False
            
            return store_proc, ['Processo salvo com sucesso!'], {'margin-bottom': '15px', 'color': 'green'}, no_processo, unidade, tipo, acao, contrato, cidade, vara, fase, instancia, data_julgamento, data_inicial, data_final, processo_concluido, processo_vencido, transito_julgado, advogados, cliente, cpf_cliente, Descrição, False
    
    if 'deletar_processo' in trigg_id:
        df_proc = pd.DataFrame(store_proc)
        
        trigg_id_dict = json.loads(trigg_id)
        numero_processo = trigg_id_dict['index']
        index_processo = df_proc.loc[df_proc['No Processo'] == numero_processo].index[0]
        df_proc.drop(index_processo, inplace=True)
        df_proc.reset_index(drop=True, inplace=True)
        store_proc = df_proc.to_dict()
        
        no_processo = unidade = tipo = acao = contrato = cidade = vara = fase = instancia = data_julgamento = data_inicial = data_final = advogados = cliente = cpf_cliente = Descrição = None
        processo_concluido = processo_vencido = transito_julgado = False
        return store_proc, [], {}, no_processo, unidade, tipo, acao, contrato, cidade, vara, fase, instancia, data_julgamento, data_inicial, data_final, processo_concluido, processo_vencido, transito_julgado, advogados, cliente, cpf_cliente, Descrição, False

    if (trigg_id == 'store_intermedio') and is_open:
        try:
            df = pd.DataFrame(callback_context.triggered[0]['value'])
            df_proc = pd.DataFrame(store_proc)
            valores = df.head(1).values.tolist()[0]

            no_processo, unidade, tipo, acao, contrato, cidade, vara, fase, instancia, data_julgamento, data_inicial, data_final, processo_concluido, processo_vencido, transito_julgado, advogados, cliente, cpf_cliente, Descrição = disabled = valores
            
            processo_concluido = False if processo_concluido == 0 else True
            processo_vencido = False if processo_vencido == 0 else True
            transito_julgado = False if transito_julgado == 0 else True
            
            return store_proc, ['Modo de Edição: Número de Processo não pode ser alterado'], {'margin-bottom': '15px', 'color': 'green'}, no_processo, unidade, tipo, acao, contrato, cidade, vara, fase, instancia, data_julgamento, data_inicial, data_final, processo_concluido, processo_vencido, transito_julgado, advogados, cliente, cpf_cliente, Descrição, disabled
        except:
            no_processo = unidade = tipo = acao = contrato = cidade = vara = fase = instancia = data_julgamento = data_inicial = data_final = advogados = cliente = cpf_cliente = Descrição = None
            processo_concluido = processo_vencido = transito_julgado = False
            return store_proc, [], {}, no_processo, unidade, tipo, acao, contrato, cidade, vara, fase, instancia, data_julgamento, data_inicial, data_final, processo_concluido, processo_vencido, transito_julgado, advogados, cliente, cpf_cliente, Descrição, False
    no_processo = unidade = tipo = acao = contrato = cidade = vara = fase = instancia = data_julgamento = data_inicial = data_final = advogados = cliente = cpf_cliente = Descrição = None
    processo_concluido = processo_vencido = transito_julgado = False
    return store_proc, [], {}, no_processo, unidade, tipo, acao, contrato, cidade, vara, fase, instancia, data_julgamento, data_inicial, data_final, processo_concluido, processo_vencido, transito_julgado, advogados, cliente, cpf_cliente, Descrição, False
    
    
# Callback pra atualizar o dropdown de advogados
@app.callback(
    Output('advogados_envolvidos', 'options'),
    Input('store_adv', 'data')
)
def atu(data):
    df = pd.DataFrame(data)
    return [{'label': i, 'value': i} for i in df['Advogado']]
