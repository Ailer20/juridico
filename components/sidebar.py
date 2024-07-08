import dash
import plotly.express as px
from dash import html, dcc, callback_context
from dash.dependencies import Input, Output, State, ALL
import dash_bootstrap_components as dbc
import json
import pandas as pd

from components import modal_novo_advogado, modal_advogados
from app import app

import components.modal_reuniões as modal_reuniões
from . import modal_novo_processo

# ========= Layout ========= #
layout = dbc.Container([
        modal_novo_processo.layout,
        modal_novo_advogado.layout,
        modal_advogados.layout,
        modal_reuniões.layout,
        dbc.Container([
            dbc.Row([
                dbc.Col([
                    html.H1("NORTE TECH", style={'color': 'yellow'})
                ])
            ]),
            dbc.Row([
                dbc.Col([
                    html.H3("JURÍDICO", style={'color': 'white'})
                ]),
            ]),
        ], style={'padding-top': '50px', 'margin-bottom': '50px'}, className='text-center'),
        html.Hr(),
        dbc.Row([
            dbc.Col([
                dbc.Nav([
                    dbc.NavItem(dbc.NavLink([html.I(className='fa fa-home dbc'), "\tINÍCIO"], href="/home", active=True, style={'text-align': 'left'})),
                    html.Br(),
                    dbc.NavItem(dbc.NavLink([html.I(className='fa fa-plus-circle dbc'), "\tPROCESSOS"], id='processo_button', active=True, style={'text-align': 'left'})),
                    html.Br(),
                    dbc.NavItem(dbc.NavLink([html.I(className='fa fa-user-plus dbc'), "\tADVOGADOS"], id='lawyers_button', active=True, style={'text-align': 'left'})),
                    html.Br(),
                    dbc.NavItem(dbc.NavLink([html.I(className='fa fa-home dbc'), "\tAGENDA"], id='agenda_button', active=True, style={'text-align': 'left'})),
                    html.Br(),
                    dbc.NavItem(dbc.NavLink([html.I(className='fa fa-plus-circle dbc'), "\tREUNIÕES"], id='reunioes_button', active=True, style={'text-align': 'left'})),
                ], vertical="lg", pills=True, fill=True)
            ])
        ]),
], style={'height': '100vh', 'padding': '0px', 'position':'sticky', 'top': 0, 'background-color': '#232423'})

# ======= Callbacks ======== #
#Callback para abrir/fechar o modal de novo advogado:
@app.callback(
    Output('modal_new_lawyer', "is_open"),
    [Input('new_adv_button', 'n_clicks'), Input("cancel_button_novo_advogado", 'n_clicks')],
    [State('modal_new_lawyer', "is_open")]
)
def toggle_modal_new_lawyer(n, n2, is_open):
    if n or n2:
        return not is_open
    return is_open

# Callback para abrir/fechar o modal de advogados:
@app.callback(
    Output('modal_lawyers', "is_open"),
    [Input('lawyers_button', 'n_clicks'), Input('quit_button', 'n_clicks'), Input('new_adv_button', 'n_clicks')],
    [State('modal_lawyers', "is_open")]
)
def toggle_modal_lawyers(n, n2, n3, is_open):
    if n or n2 or n3:
        return not is_open
    return is_open



# Callback para abrir e fechar o modal das reuniões
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