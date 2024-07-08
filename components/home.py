import dash
from dash import html, dcc, callback_context
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
import pandas as pd
import io
import plotly.express as px
import plotly.graph_objects as go
from fpdf import FPDF
import matplotlib.pyplot as plt
from sqlalchemy import create_engine
from dash import dash_table
from dash.dash_table.Format import Group

from app import app
from components import modal_novo_advogado, modal_advogados, modal_novo_processo


from sql_beta import df_adv, df_proc


# ========= Styles ========= #
card_style={'height': '100%',  'margin-bottom': '12px'}


# Funções para gerar os Cards =======================
# Checar o DataFrame e gerar os icones
def gerar_icones(df_proc_aux, i):
    df_aux = df_proc_aux.iloc[i]
    if df_aux['Processo Tramite'] == 'Sim' and df_aux['Processo Extinto'] == 'Não' and df_aux['Transito julgado'] == 'Não':
        concluido = 'fa fa-check'
        vencido = 'fa fa-times'
        julgado = 'fa fa-times'
        color_c = 'green'
        color_v = 'red'
        color_j= 'red'
        concluido_text = 'Em Trâmite'
        vencido_text = 'Extinto'
        julgado_text = 'Em Julgado'
    elif df_aux['Processo Tramite'] == 'Não' and df_aux['Processo Extinto'] == 'Sim' and df_aux['Transito julgado'] == 'Não':
        concluido = 'fa fa-times'
        vencido = 'fa fa-check'
        julgado = 'fa fa-times'
        color_c = 'red'
        color_v = 'green'
        color_j= 'red'
        concluido_text = 'Em Trâmite'
        vencido_text = 'Extinto'
        julgado_text = 'Em Julgado'
    elif df_aux['Processo Tramite'] == 'Não' and df_aux['Processo Extinto'] == 'Não' and df_aux['Transito julgado'] == 'Sim':
        concluido = 'fa fa-times'
        vencido = 'fa fa-times'
        julgado = 'fa fa-check'
        color_c = 'red'
        color_v = 'red'
        color_j= 'green'
        concluido_text = 'Em Trâmite'
        vencido_text = 'Extinto'
        julgado_text = 'Em Julgado'
    return df_aux, concluido, vencido, julgado, color_c, color_v, color_j, concluido_text, vencido_text, julgado_text

# Card padrão de contagem
def gerar_card_padrao(qnt_procs):
    card_padrao = dbc.Card([
        dbc.CardBody([
            html.H3(f"{qnt_procs} PROCESSOS ENCONTRADOS", style={'font-weight': 'bold', 'color': 'white'})
        ])
    ], style={'height': '100%', 'margin-bottom': '12px', 'background-color': '#646464'})
    return card_padrao

# Card qualquer de processo
def gerar_card_processo(df_aux, concluido, vencido, julgado, color_c, color_v, color_j, concluido_text, vencido_text, julgado_text):        
    card_processo = dbc.Card([
        dbc.CardBody([
            dbc.Row([
                dbc.Col([
                    dbc.Row([
                        dbc.Col([   
                            html.H2(f"Processo nº {df_aux['No Processo']}")
                        ])
                    ]),
                    dbc.Row([
                        dbc.Col([  
                            html.P("Processo corre em segredo de justiça por questões similares.", style={'text-align': 'left'})
                        ])
                    ]),
                    dbc.Row([
                        dbc.Col([
                            html.Ul([
                                html.Li([html.B("DATA DO JULGAMENTO: ", style={'font-weight': 'bold'}), f"{df_aux['Data julgamento']}"]),
                                html.Li([html.B("DATA: ", style={'font-weight': 'bold'}), f"{df_aux['Data Inicial']} - {df_aux['Data Final']}"]),
                                html.Li([html.B("AÇÃO: ", style={'font-weight': 'bold'}), f"{df_aux['Ação']}"]),
                                html.Li([html.B("INSTÂNCIA: ", style={'font-weight': 'bold'}), f"{df_aux['Instância']}"]),
                                html.Li([html.B("FASE: ", style={'font-weight': 'bold'}), f"{df_aux['Fase']}"]),
                                html.Li([html.B("DESCRIÇÃO: ", style={'font-weight': 'bold'}), f"{df_aux['Descrição']}"]),
                            ]),
                        ])
                    ])
                ], style={'border-right': '2px solid lightgrey', 'margin-bottom': '12px'}),
                dbc.Col([
                    dbc.Row([
                        dbc.Col([
                            html.Ul([
                                html.Li([html.B("RECLAMANTE/AUTOR: ", style={'font-weight': 'bold'}), f"{df_aux['Cliente']}"]),
                                html.Li([html.B("CONTRATO: ", style={'font-weight': 'bold'}), f"{df_aux['Contrato']}"]),
                                html.Li([html.B("UNIDADE: ", style={'font-weight': 'bold'}), f"{df_aux['Unidade']}"]),
                                html.Li([html.B("CIDADE: ", style={'font-weight': 'bold'}), f"{df_aux['Cidade']}"]),
                                html.Li([html.B("ADVOGADO: ", style={'font-weight': 'bold'}), f"{df_aux['Advogado']}"])
                            ]),
                        ])
                    ], style={'margin-bottom': '32px'}),
                    dbc.Row([
                        dbc.Col([
                            html.H5("STATUS", style={'margin-bottom': 0}),
                        ], sm=5, style={'text-align': 'right'}),
                        dbc.Col([
                            html.I(className=f'{concluido} fa-2x dbc', style={'color': f'{color_c}'}),
                        ], sm=2),
                        dbc.Col([
                            html.H5(f"{concluido_text}", style={'margin-bottom': 0}),
                        ], sm=5, style={'text-align': 'left'}),
                    ], style={'display': 'flex', 'align-items': 'center', 'justify-content': 'center'}),
                    
                    dbc.Row([
                        dbc.Col([
                            html.H5("STATUS", style={'margin-bottom': 0})
                        ], sm=5, style={'text-align': 'right'}),
                        dbc.Col([
                            html.I(className=f'{vencido} fa-2x dbc', style={'color': f'{color_v}'})
                        ], sm=2),
                        dbc.Col([
                            html.H5(f'{vencido_text}', style={'margin-bottom': 0})
                        ], sm=5, style={'text-align': 'left'}),
                    ], style={'display': 'flex', 'align-items': 'center', 'justify-content': 'center'}),
                    
                    dbc.Row([
                        dbc.Col([
                            html.H5("STATUS", style={'margin-bottom': 0})
                        ], sm=5, style={'text-align': 'right'}),
                        dbc.Col([
                            html.I(className=f'{julgado} fa-2x dbc', style={'color': f'{color_j}'})
                        ], sm=2),
                        dbc.Col([
                            html.H5(f'{julgado_text}', style={'margin-bottom': 0})
                        ], sm=5, style={'text-align': 'left'}),
                    ], style={'display': 'flex', 'align-items': 'center', 'justify-content': 'center'}),
                    html.Br(),
                    dbc.Row([
                        dbc.Col([ #TODO REMOVER BOTÃO FAN
                            dbc.Button(["Botão fantasma, para solucionar o callback"], id={'type': 'ghost_processo', 'index': str(df_aux['No Processo'])}, style={'display': 'none'}),
                        ], md=2),
                        dbc.Col([
                          dbc.Button(html.I(className = "fa fa-pencil fa-2x"), style={'color': 'black'}, size='sm', outline=True,
                                id={'type': 'editar_processo', 'index': int(df_aux['No Processo'])})
                        ], md=2),
                        dbc.Col([
                            dbc.Button(html.I(className = "fa fa-trash fa-2x"), style={'color': 'red'}, size='sm', outline=True,
                                id={'type': 'deletar_processo', 'index': int(df_aux['No Processo'])})
                        ], md=2)
                    ], style={'display': 'flex', 'justify-content': 'flex-end'})
                ], sm=12, md=6, style={'height': '100%', 'margin-top': 'auto', 'margin-bottom': 'auto'}),
            ], style={'margin-top': '12px'})
        ])
    ], style=card_style, className='card_padrao')
    return card_processo


# ========= Layout ========= #
layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            html.H3("ENCONTRE O PROCESSO QUE VOCÊ PROCURA"),
            html.Button(["Excel", html.Img(src="https://s3.amazonaws.com/s3-gpm/includes/icons/excel.PNG", style={'height':'20px', 'margin-right':'5px', 'background': 'green','color': 'white'})], id="btn_excel"),
            dcc.Download(id="download_excel"),
            html.Button("Download PDF", id="btn_pdf"),
            dcc.Download(id="download_pdf"),
            html.Button("Download JPG", id="btn_jpg"),
            dcc.Download(id="download_jpg"),
        ], style={'text-align': 'left', 'margin-left': '32px'})
    ], style={'margin-top': '14px'}),
    html.Hr(),
    dbc.Row([
        # Filtros
        dbc.Col([
            dbc.Row([
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            dbc.Row([
                                dbc.Col([
                                    html.H3("Nº DO PROCESSO")
                                ], sm=12)
                            ]),
                            dbc.Row([
                                dbc.Col([
                                    dbc.Input(id='processos_filter', placeholder="Insira...", type="number")
                                ], sm=12, md=12, lg=8),
                                dbc.Col([
                                    dbc.Button([html.I(className='fa fa-search')], id="pesquisar_num_proc", color='dark')
                                ], sm=12, md=12, lg=4)
                            ], style={'margin-bottom': '32px'}),
                            dbc.Row([
                                dbc.Col([
                                    html.H3("STATUS")
                                ])
                            ], style={'margin-top': '32px'}),
                            dbc.Row([
                                dbc.Col([
                                    dbc.Checklist(
                                        options=[{"label": "Processo em Trãmite", "value": 1}, {"label": "Processo Extinto", "value": 2}, {"label": "Transito em Julgado", "value": 3}],
                                        value=[],
                                        id="switches_input",
                                        switch=True,
                                    ),
                                ])
                            ]),
                            dbc.Row([
                                dbc.Col([
                                    html.H3("INSTÂNCIA")
                                ])
                            ], style={'margin-top': '24px'}),
                            dbc.Row([
                                dbc.Col([
                                    dbc.Checklist(
                                        options=[{"label": "1a Instância", "value": 1}, 
                                                {"label": "2a Instância", "value": 2}],
                                        value=[1, 2],
                                        id="checklist_input"
                                    ),
                                ])
                            ]),
                            dbc.Row([
                                dbc.Col([
                                    html.H3("CPF")
                                ])
                            ], style={'margin-top': '24px'}),
                            dbc.Row([
                                dbc.Col([
                                    dbc.Button([html.I(className='fa fa-search')], id="pesquisar_cpf", color='light')
                                ], sm=2),
                                dbc.Col([
                                    dbc.Input(id="input_cpf_pesquisa", placeholder="DIGITE O CPF", type="number")
                                ], sm=10)
                            ]),
                            dbc.Row([
                                dbc.Col([
                                    html.H3("ADVOGADO")
                                ])
                            ], style={'margin-top': '24px'}),
                            dbc.Row([
                                dbc.Col([
                                    dcc.Dropdown(
                                        id='advogado_filter',
                                        options=[{'label': i, 'value': i} for i in df_adv['Advogado']],
                                        placeholder='SELECIONE O ADVOGADO',
                                        className='dbc'
                                    ),
                                ])
                            ]),
                            dbc.Row([
                                dbc.Col([
                                    dbc.Button("Todos os Processos", id="todos_processos", style={'width': '100%'}, color="dark")
                                ])
                            ], style={'margin-top': '24px'})
                        ], style={'margin': '20px'})
                    ])
                ])
            ])
        ], sm=12, md=5, lg=4),
        dbc.Col([
            dbc.Container(id='card_generator', fluid=True, style={'width': '100%', 'padding': '0px 0px 0px 0px', 'margin': '0px 0px 0px 0px'}),
            html.Div(id='div_fant')
        ], sm=12, md=7, lg=8, style={'padding-left': '0px'})
    ])

], fluid=True, style={'height': '100%', 'padding': '10px', 'margin': 0, 'padding-left': 0})


@app.callback(
    Output("download_jpg", "data"),
    Input("btn_jpg", "n_clicks"),
    prevent_initial_call=True,
)
def download_jpg(n_clicks):
    img_bytes = to_jpg()
    return dcc.send_bytes(img_bytes.read(), "processos.jpg")
# Função para gerar o conteúdo do JPG
def to_jpg():
    df = df_proc
    fig, ax = plt.subplots()
    ax.axis('tight')
    ax.axis('off')
    table = ax.table(cellText=df.values, colLabels=df.columns, cellLoc='center', loc='center')
    fig.tight_layout()

    img_bytes = io.BytesIO()
    plt.savefig(img_bytes, format='jpg')
    img_bytes.seek(0)
    plt.close(fig)  # Fechar a figura para liberar memória
    return img_bytes


# Função para gerar o conteúdo do PDF
def to_pdf():
    df = df_proc
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    for i in range(len(df)):
        pdf.cell(200, 10, txt=str(df.iloc[i].to_list()), ln=True, align='L')
    pdf_output = pdf.output(dest='S').encode('latin1')  # Corrigir o problema de encoding
    return pdf_output
# Callback para gerar e baixar o arquivo PDF
@app.callback(
    Output("download_pdf", "data"),
    Input("btn_pdf", "n_clicks"),
    prevent_initial_call=True,
)
def download_pdf(n_clicks):
    pdf_output = to_pdf()
    return dcc.send_bytes(pdf_output, "processos.pdf")

# Callback para gerar e baixar o arquivo JPG


#excel
def fetch_data_from_db():
    # Configure sua conexão aqui
    engine = create_engine('sqlite:///sistema.db')
    query = "SELECT * FROM processos"
    df = pd.read_sql(query, engine)
    return df

def to_excel(bytes_io, df):
    with pd.ExcelWriter(bytes_io, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False)
@app.callback(
    Output("download_excel", "data"),
    Input("btn_excel", "n_clicks"),
    prevent_initial_call=True,
)
def download_excel(n_clicks):
    df = fetch_data_from_db()  # Puxa os dados do banco de dados
    bytes_io = io.BytesIO()
    to_excel(bytes_io, df)  # Converte os dados em Excel
    bytes_io.seek(0)
    return dcc.send_bytes(bytes_io.read(), "processos.xlsx")

# ======= Callbacks ======== #
# Callback pra atualizar o dropdown de advogado
@app.callback(
    Output('advogado_filter', 'options'),
    Input('store_adv', 'data')
)
def atu(data):
    df = pd.DataFrame(data)
    return [{'label': i, 'value': i} for i in df['Advogado']]

# Callback pra atualizar o dropdown de clientes
@app.callback(
    Output('clientes_filter', 'options'),
    Input('store_proc', 'data')
)
def atu(data):
    df = pd.DataFrame(data)
    return [{'label': i, 'value': i} for i in df['Cliente'].unique()]

# Callback pra atualizar o dropdown de processos
@app.callback(
    Output('processos_filter', 'options'),
    Input('store_proc', 'data')
)
def atu(data):
    df = pd.DataFrame(data)
    return [{'label': i, 'value': i} for i in df['No Processo']]

# Callback pra gerar o conteudo dos cards
@app.callback(
    Output('card_generator', 'children'),
    Output('advogado_filter', 'value'),
    Output('processos_filter', 'value'),
    Output('input_cpf_pesquisa', 'value'),
    Input('pesquisar_cpf', 'n_clicks'),
    Input('todos_processos', 'n_clicks'),
    Input('advogado_filter', 'value'),
    Input('pesquisar_num_proc', 'n_clicks'),
    Input('store_proc', 'data'),
    Input('store_adv', 'data'),
    Input('switches_input', 'value'),
    Input('checklist_input', 'value'),
    State('processos_filter', 'value'),
    State('input_cpf_pesquisa', 'value')
)
def generate_cards(n, n_all, adv_filter, proc_button, proc_data, adv_data, switches, checklist, proc_filter, cpf):
    trigg_id = callback_context.triggered[0]['prop_id'].split('.')[0]

    # Iniciando os cards vazios
    cards = []

    # Iniciando os dataframes possíveis
    df_adv_aux = pd.DataFrame(adv_data)
    df_proc_aux = pd.DataFrame(proc_data)
        
    # Caso default - Todos os casos por ordem de data   
    if (trigg_id == '' or trigg_id == 'store_proc' or trigg_id == 'store_adv' or trigg_id == 'todos_processos' or trigg_id == 'switches_input' or trigg_id == 'checklist_input'):
        if trigg_id != 'todos_processos':
            # Filtrando pelos switches
            if all(elem in switches for elem in [1, 2, 3]):
                df_proc_aux = df_proc_aux.loc[(df_proc_aux['Processo Tramite'] == 1) & (df_proc_aux['Processo Extinto'] == 1) & (df_proc_aux['Transito julgado'] == 1)]
            elif switches == [1]: df_proc_aux = df_proc_aux.loc[df_proc_aux['Processo Tramite'] == 1]
            elif switches == [2]: df_proc_aux = df_proc_aux.loc[df_proc_aux['Processo Extinto'] == 1]
            elif switches == [3]: df_proc_aux = df_proc_aux.loc[df_proc_aux['Transito julgado'] == 1]
                

            if (1 in checklist) and (2 in checklist): pass
            elif checklist == [1]: df_proc_aux = df_proc_aux.loc[df_proc_aux['Instância'] == 1]
            elif checklist == [2]: df_proc_aux = df_proc_aux.loc[df_proc_aux['Instância'] == 2]
            
        df_proc_aux = df_proc_aux.sort_values(by='Data Inicial', ascending=False)

        df_proc_aux.loc[df_proc_aux['Processo Tramite'] == 0, 'Processo Tramite'] = 'Não'
        df_proc_aux.loc[df_proc_aux['Processo Tramite'] == 1, 'Processo Tramite'] = 'Sim'
        df_proc_aux.loc[df_proc_aux['Processo Extinto'] == 0, 'Processo Extinto'] = 'Não'
        df_proc_aux.loc[df_proc_aux['Processo Extinto'] == 1, 'Processo Extinto'] = 'Sim'
        df_proc_aux.loc[df_proc_aux['Transito julgado'] == 0, 'Transito julgado'] = 'Não'
        df_proc_aux.loc[df_proc_aux['Transito julgado'] == 1, 'Transito julgado'] = 'Sim'
        
        df_proc_aux = df_proc_aux.fillna('-')

        # Inserido o card padrão com a quantidade de processos
        qnt_procs = len(df_proc_aux)
        cards += [gerar_card_padrao(qnt_procs)]
        
        # Iterando sobre os processos
        for i in range(len(df_proc_aux)):
            df_aux, concluido, vencido, julgado, color_c, color_v, color_j, concluido_text, vencido_text, julgado_text  = gerar_icones(df_proc_aux, i)
            card = gerar_card_processo(df_aux, concluido, vencido, julgado, color_c, color_v, color_j, concluido_text, vencido_text, julgado_text)
            cards += [card]
        
        return cards, None, None, None

    # Pesquisa de texto por número de processo
    elif (trigg_id == 'pesquisar_num_proc'):
        # Dados
        df_proc_aux = df_proc_aux.loc[df_proc_aux['No Processo'] == proc_filter].sort_values(by='Data Inicial', ascending=False)
        if len(df_proc_aux) == 0:
            cards += [gerar_card_padrao(len(df_proc_aux))]
            return cards, None, proc_filter, None

        # Processos
        df_proc_aux = df_proc_aux.sort_values(by='Data Inicial', ascending=False)
        df_proc_aux.loc[df_proc_aux['Processo Tramite'] == 0, 'Processo Tramite'] = 'Não'
        df_proc_aux.loc[df_proc_aux['Processo Tramite'] == 1, 'Processo Tramite'] = 'Sim'
        df_proc_aux.loc[df_proc_aux['Processo Extinto'] == 0, 'Processo Extinto'] = 'Não'
        df_proc_aux.loc[df_proc_aux['Processo Extinto'] == 1, 'Processo Extinto'] = 'Sim'
        df_proc_aux.loc[df_proc_aux['Transito julgado'] == 0, 'Transito julgado'] = 'Não'
        df_proc_aux.loc[df_proc_aux['Transito julgado'] == 1, 'Transito julgado'] = 'Sim'
        
        df_proc_aux = df_proc_aux.fillna('-')

        # Inserido o card padrão com a quantidade de processos
        qnt_procs = len(df_proc_aux)
        cards += [gerar_card_padrao(qnt_procs)]

        # Iterando sobre os processos possíveis
        for i in range(len(df_proc_aux)):
            df_aux, concluido, vencido, julgado, color_c, color_v, color_j, concluido_text, vencido_text, julgado_text = gerar_icones(df_proc_aux, i)
            card = gerar_card_processo(df_aux, concluido, vencido, julgado, color_c, color_v, color_j, concluido_text, vencido_text, julgado_text)
            cards += [card]

        return cards, None, proc_filter, None

    # Pesquisa de cliente por CPF
    elif trigg_id == 'pesquisar_cpf':
        if cpf in df_proc['Cpf Cliente'].values:

            # Dados
            df_proc_aux = df_proc_aux.loc[df_proc_aux['Cpf Cliente'] == cpf].sort_values(by='Data Inicial', ascending=False)
            nome = df_proc_aux.iloc[0]['Cliente']

            # Card do Cliente
            card_cliente = dbc.Card([
                dbc.CardBody([
                    dbc.Row([
                        dbc.Col([
                            html.H4(f"Cliente: {nome}"),
                            html.Hr(),
                            html.H4(f"CPF: {cpf}"),
                        ]),
                    ])
                ])
            ], style=card_style)
            cards += [card_cliente]

            # Processos
            df_proc_aux = df_proc_aux.sort_values(by='Data Inicial', ascending=False)
            df_proc_aux.loc[df_proc_aux['Processo Tramite'] == 0, 'Processo Tramite'] = 'Não'
            df_proc_aux.loc[df_proc_aux['Processo Tramite'] == 1, 'Processo Tramite'] = 'Sim'
            df_proc_aux.loc[df_proc_aux['Processo Extinto'] == 0, 'Processo Extinto'] = 'Não'
            df_proc_aux.loc[df_proc_aux['Processo Extinto'] == 1, 'Processo Extinto'] = 'Sim'
            df_proc_aux.loc[df_proc_aux['Transito julgado'] == 0, 'Transito julgado'] = 'Não'
            df_proc_aux.loc[df_proc_aux['Transito julgado'] == 1, 'Transito julgado'] = 'Sim'

            df_proc_aux = df_proc_aux.fillna('-')

            # Inserido o card padrão com a quantidade de processos
            qnt_procs = len(df_proc_aux)
            cards += [gerar_card_padrao(qnt_procs)]

            # Iterando sobre os processos
            for i in range(len(df_proc_aux)):
                df_aux, concluido, vencido, julgado, color_c, color_v, color_j, concluido_text, vencido_text, julgado_text = gerar_icones(df_proc_aux, i)
                card = gerar_card_processo(df_aux, concluido, vencido, julgado, color_c, color_v, color_j, concluido_text, vencido_text, julgado_text )
                cards += [card]

            return cards, None, None, cpf
        else:
            card = dbc.Card([
                dbc.CardBody([
                    dbc.Row([
                        dbc.Col([
                            html.I(className='fa fa-exclamation dbc', style={'font-size': '4em'})
                        ], sm=3, className='text-center'),
                        dbc.Col([
                            html.H1("Nenhum CPF correspondente no banco de dados.")
                        ], sm=9)
                    ])
                ])
            ], style=card_style)
            cards += [card]
            return cards, None, None, cpf
    
    # Filtro DROPDOWN de advogado
    elif (trigg_id == 'advogado_filter'):
        # Dados
        df_aux = df_adv_aux.loc[df_adv_aux['Advogado'] == adv_filter]
        nome = df_aux.iloc[0]['Advogado']
        oab = df_aux.iloc[0]['OAB']
        
        # Card do Advogado
        card_adv = dbc.Card([
            dbc.CardBody([
                dbc.Row([
                    dbc.Col([
                        html.H4(f"Advogado: {nome}"),
                        html.Hr(),
                        html.H4(f"OAB: {oab}"),
                    ]),
                ])
            ])
        ], style=card_style)
        cards += [card_adv]

        # Processos
        df_proc_aux = df_proc_aux[df_proc_aux['Advogado'] == nome]
        df_proc_aux = df_proc_aux.sort_values(by='Data Inicial', ascending=False)
        df_proc_aux.loc[df_proc_aux['Processo Tramite'] == 0, 'Processo Tramite'] = 'Não'
        df_proc_aux.loc[df_proc_aux['Processo Tramite'] == 1, 'Processo Tramite'] = 'Sim'
        df_proc_aux.loc[df_proc_aux['Processo Extinto'] == 0, 'Processo Extinto'] = 'Não'
        df_proc_aux.loc[df_proc_aux['Processo Extinto'] == 1, 'Processo Extinto'] = 'Sim'
        df_proc_aux.loc[df_proc_aux['Transito julgado'] == 0, 'Transito julgado'] = 'Não'
        df_proc_aux.loc[df_proc_aux['Transito julgado'] == 1, 'Transito julgado'] = 'Sim'

        df_proc_aux = df_proc_aux.fillna('-')

        # Inserido o card padrão com a quantidade de processos
        qnt_procs = len(df_proc_aux)
        cards += [gerar_card_padrao(qnt_procs)]

        # Iterando sobre os processos
        for i in range(len(df_proc_aux)):
            df_aux, concluido, vencido, julgado, color_c, color_v, color_j, concluido_text, vencido_text, julgado_text = gerar_icones(df_proc_aux, i)
            card = gerar_card_processo(df_aux, concluido, vencido, julgado, color_c, color_v, color_j, concluido_text, vencido_text, julgado_text )
            cards += [card]
        return cards, adv_filter, None, None