### ------ IMPORTS ------ ###

# --- dash --- #
from dash import callback, dash_table, dcc, html, Input, Output, State
from dash.dash_table.Format import Format, Scheme
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go

# --- Third part --- #
from unidecode import unidecode
import pandas as pd

### ------ datasets ------ ####
from datasets import basic_stats


### ------ Configs ------ ###
configuracoes_grafico = {
    'staticPlot': False,     # True, False
    'scrollZoom': True,      # True, False
    'doubleClick': 'reset',  # 'reset', 'autosize' or 'reset+autosize', False
    'showTips': True,       # True, False
    'displayModeBar': True,  # True, False, 'hover'
    'watermark': True,
    'modeBarButtonsToRemove': ['lasso2d'],
}


### ------ Dropdown options ------ ###
dataset_options = [
    {'label': 'Flor de Iris', 'value': 'iris'},
]



dataset_iris_options_1 = [
    {'label': 'setosa', 'value': 'setosa'},
    {'label': 'virgínica', 'value': 'virginica'},
    {'label': 'versicolor', 'value': 'versicolor'},
]

dataset_iris_options_2 = [
    {'label': 'Comprimento das sépalas', 'value': 'sepal_length'},
    {'label': 'Largura das sépalas', 'value': 'sepal_width'},
    {'label': 'Comprimento das pétalas', 'value': 'petal_length'},
    {'label': 'Largura das pétalas', 'value': 'petal_width'},
]


normalidade_options = [
    {'label': 'Shapiro-Wilk', 'value': 'Shapiro-Wilk'},
    {'label': 'Anderson-Darling', 'value': "Anderson-Darling"},
]


### ------ LAYOUTS ------ ###

# --- MENU --- #
offcanvas = html.Div(
    [
        dbc.Button(
            html.I(className="fas fa-cog fa-2x contact_icons"),
            id="estatistica-basica-open-offcanvas", n_clicks=0, className="btn bg-transparent rounded-circle border-white shadow-none",
            ),
        dbc.Offcanvas(
            children = [
                    dbc.Row([
                        dbc.Col(
                            html.Label("Dataset: "), width="auto", align="start"
                        ),
                        dbc.Col([
                            dbc.Row(
                                dbc.Col(
                                    dcc.Dropdown(
                                        id='estatistica-basica-data-set-picker', # id do dropdown
                                        value = dataset_options[0]['value'], # seta o valor inicial,
                                        options = dataset_options, # as opções que vão aparecer no dropdown
                                        clearable = False, # permite remover o valor (acho importante manter false para evitar problemas)
                                        ),
                                )
                            ),
                            dbc.Row(
                                dbc.Col(
                                    dcc.Dropdown(
                                        id='estatistica-basica-data-set-picker-aux1', # id do dropdown
                                        value = dataset_iris_options_1[0]['value'], # seta o valor inicial,
                                        options = dataset_iris_options_1, # as opções que vão aparecer no dropdown
                                        clearable = False, # permite remover o valor (acho importante manter false para evitar problemas)
                                        ),
                                )
                            ),
                            dbc.Row(
                                dbc.Col(
                                    dcc.Dropdown(
                                        id='estatistica-basica-data-set-picker-aux2', # id do dropdown
                                        value = dataset_iris_options_2[0]['value'], # seta o valor inicial,
                                        options = dataset_iris_options_2, # as opções que vão aparecer no dropdown
                                        clearable = False, # permite remover o valor (acho importante manter false para evitar problemas)
                                        ),
                                )
                            ),
                            ]),
                        ],
                    ),
                ],
            id="estatistica-basica-offcanvas",
            title="Opções",
            is_open=False,
        ),
    ]
)



# --- MAIN LAYOUT --- #
layout = html.Div([
    # Titulo geral
    dbc.Row([
        dbc.Col(
            sm = 0,
            lg = 1,
            align="center"
        ),
        dbc.Col(
            html.H2("Stat 101"),
            width = {"size": 10},
            align = "center"
        ),
        dbc.Col(
            offcanvas,
            width = {"size": 1},
            align="center"
        ),
    ], style = {'textAlign': 'center', 'paddingTop': '30px', 'paddingBottom': '30px'},),
    dbc.Row(
        dbc.Col(
            id='estatistica-basica-titulo', style={"textAlign": "center", "paddingBottom": "20px"}
        )
    ),
    ### Tabela com os dados, gráfico t de student e tabela com o resumo dos daddos e barra de controle de n amostral
    dbc.Row([
        ## Tabela com os dados
        dbc.Col(
            id="estatistica-basica-table-dataset", style={"textAlign": "center"},
            lg=2
        ),
        ## Gráfico t de Student, tabela com resumo dos dados e barra de conrole de n amostral
        dbc.Col([
            # Gráfico t de Student, tabela com resumo dos dados
            dbc.Row([
                dbc.Col(id="estatistica-basica-table-summary-central"),
                dbc.Col(id="estatistica-basica-table-summary-dispersion",),
                dbc.Col(id="estatistica-basica-table-summary-other",),

            ]),
            dbc.Row(
                dbc.Col(id="estatistica-basica-table-info", style={"textAlign": "right"}),
            ),
            dbc.Row([
                # Gráfico t de Studentdos
                dbc.Col(
                    dcc.Graph(id="estatistica-basica-boxplot", config=configuracoes_grafico),
                    # lg=10,
                ),
            ], align="start", justify="center"),
            # barra de conrole de n amostral
            dbc.Row(
                # barra de conrole de n amostral
                dbc.Col(
                    dcc.Slider(
                        id='estatistica-basica-slider', min=1, value=10, max=50, tooltip={"placement": "bottom", "always_visible": True},
                        ),
                    # lg=8
                ), style={"paddingTop": "20px", "paddingBottom": "20px"}
            )
        ], lg=10),
    ], align="start", justify="center"),
    ### Gráfico Animado
    dbc.Row([
        dbc.Col(
            html.H3("Variação das medidas em relação ao tamanho amostral", style={"textAlign": "center", "paddingTop": "30px", "paddingBottom": "15px"})
        )
    ]),
    ### Aleatorização do gráfico animado
    dbc.Row(
        dbc.Col(
            dcc.Graph(id='estatistica-basica-animated-plot', config=configuracoes_grafico)
        )
    ),
    dbc.Row([
        dbc.Col(
            html.H3("Variação das medidas de dispersão em relação ao tamanho amostral", style={"textAlign": "center", "paddingTop": "30px", "paddingBottom": "15px"})
        )
    ]),
    dbc.Row(
        dbc.Col(
            dcc.Graph(id='estatistica-basica-animated-dispersion-plot', config=configuracoes_grafico)
        )
    ),
    dbc.Row(
        dbc.Col(
            "", style={"paddingTop": "30px"}
        )
    ),

    # store dataset filtered
    dcc.Store(id='estatistica-basica-store-data'),
    dcc.Store(id='estatistica-basica-store-data-summary'),
    dcc.Store(id='estatistica-basica-store-data-animation'),
    dcc.Store(id='estatistica-basica-store-data-info'),

],)






### ------ CALLBACKS ------ ###

# --- Callback to filter the dataset --- #
@callback(
    [
    Output(component_id='estatistica-basica-store-data', component_property='data'),
    Output(component_id='estatistica-basica-store-data-summary', component_property='data'),
    Output(component_id='estatistica-basica-store-data-animation', component_property='data'),
    Output(component_id='estatistica-basica-store-data-info', component_property='data'),
    ],
    [Input(component_id='estatistica-basica-data-set-picker', component_property='value'),
    Input(component_id='estatistica-basica-data-set-picker-aux1', component_property='value'),
    Input(component_id='estatistica-basica-data-set-picker-aux2', component_property='value'),
    ],
    prevent_initial_callback=True
)
def dataset_filter(dataset_key, drop_1, drop_2):

    if dataset_key == "iris":

        df = basic_stats.df_iris_dataset.copy()
        df = df[df['species'] == drop_1]
        df = df[[drop_2]]

        df_summary = basic_stats.df_iris_dataset_summary.copy()
        df_summary = df_summary[df_summary['data_set'] == dataset_key]
        df_summary = df_summary[df_summary['species'] == drop_1]
        df_summary = df_summary[df_summary['kind'] == drop_2]

        df_animation = basic_stats.df_iris_dataset_animation.copy()
        df_animation = df_animation[df_animation['data_set'] == dataset_key]
        df_animation = df_animation[df_animation['species'] == drop_1]
        df_animation = df_animation[df_animation['kind'] == drop_2]
        df_animation.reset_index(inplace=True, drop=True)

        df_info = basic_stats.df_iris_info.copy()
        df_info = df_info[df_info['variedade'] == drop_1]
        df_info = df_info[df_info['variavel'] == drop_2]


    else:
        pass


    return [
        df.to_json(date_format='iso', orient='split'),
        df_summary.to_json(date_format='iso', orient='split'),
        df_animation.to_json(date_format='iso', orient='split'),
        df_info.to_json(date_format='iso', orient='split'),]



# --- Callback to update the data-table --- #
@callback(
    Output(component_id='estatistica-basica-table-dataset', component_property='children'),
    [
    Input(component_id='estatistica-basica-store-data', component_property='data'),
    Input(component_id='estatistica-basica-slider', component_property='value'),
    Input(component_id='estatistica-basica-store-data-info', component_property='data')
    ],
)
def update_dataset_table(df_cleaned,slider_value, df_cleaned_2):
    # getting the correct title
    df_title = pd.read_json(df_cleaned_2, orient='split').copy()
    titulo = f"{df_title['traducao'].values[0].capitalize()} ({df_title['unidades'].values[0]})"

    # transforming data back to df
    df = pd.read_json(df_cleaned, orient='split').copy()
    df = df[:slider_value]
    df.rename({df.columns[0]: titulo}, inplace=True, axis=1)

    # preparing columns
    columns = []
    for col in df.columns:
        col_options = {"name": col, "id": col}
        if df[col].dtype != object:
            col_options["type"] = "numeric"
            col_options['format'] = Format(precision=3,)
        columns.append(col_options)

    # criando a tabela
    table = dash_table.DataTable(
                columns = columns,
                data = df.to_dict('records'),
                style_data = {
                    'whiteSpace': 'normal',
                    'height': 'auto'
                    },
                style_table = {
                    'overflowX': 'auto',
                    'overflowY': 'auto',
                    'maxHeight': '800px',
                    },
                style_cell = {
                    'font_size': 'clamp(1rem, 0.5vw, 0.5vh)',
                    'textAlign': 'center',
                    'height': 'auto',
                    'minWidth': '100px',
                    'width': '100px',
                    'maxWidth': '100px',
                    'whiteSpace': 'normal'
                },
                sort_action="native",
                style_header = {
                    'fontWeight': 'bold', # deixando em negrito
                    }
              )

    # retornando a tabela
    return table




# --- Callback to update the title --- #
@callback(
    Output(component_id='estatistica-basica-titulo', component_property='children'),
    [
    Input(component_id='estatistica-basica-data-set-picker', component_property='value'),
    Input(component_id='estatistica-basica-store-data-info', component_property='data')
    ]
)
def update_title(dataset_key, df_cleaned):
    df = pd.read_json(df_cleaned, orient='split').copy()
    if dataset_key == 'iris':
        titulo = f"{df['traducao'].values[0].capitalize()} ({df['unidades'].values[0]}) da flor de Iris "
        variedade = f"{df['variedade'].values[0]}"
        output = html.H3(children=[
            titulo,
            html.I(variedade)
        ])
    else:
        pass
    return output


# --- Callback to update the slider --- #
@callback(
    [
    Output(component_id='estatistica-basica-slider', component_property='value'),
    Output(component_id='estatistica-basica-slider', component_property='min'),
    Output(component_id='estatistica-basica-slider', component_property='step'),
    Output(component_id='estatistica-basica-slider', component_property='max'),
    Output(component_id='estatistica-basica-slider', component_property='marks'),
    ],
    [Input(component_id='estatistica-basica-store-data', component_property='data')]
)
def update_slider(df_cleaned):

    # transforming data back to df
    df = pd.read_json(df_cleaned, orient='split').copy()

    marks = list(range(0, df.shape[0]+1, 5))
    marks = marks[1:]
    marks.insert(0, 1)
    marks = dict(zip(marks, map(str, marks)))


    return [
            10, # value
            1, # min
            1, # step
            df.shape[0], # max
            marks # marks
    ]



@callback(
    Output(component_id='estatistica-basica-table-info', component_property='children'),
    [Input(component_id='estatistica-basica-slider', component_property='value')]
)
def update_info_table(slider_value):
    return html.P(f"*Resultados  para n = {slider_value}")








# --- Callback to uptade the summary table --- #
@callback(
    [
    Output(component_id='estatistica-basica-table-summary-central', component_property='children'),
    Output(component_id='estatistica-basica-table-summary-dispersion', component_property='children'),
    Output(component_id='estatistica-basica-table-summary-other', component_property='children'),
    ],
    [
    Input(component_id='estatistica-basica-store-data-summary', component_property='data'),
    Input(component_id='estatistica-basica-slider', component_property='value'),
    Input(component_id='estatistica-basica-store-data-info', component_property='data')
    ],
)
def update_table_summary(df_cleaned,slider_value, df_cleaned_2):
    df = pd.read_json(df_cleaned_2, orient='split').copy()
    unidade = df['unidades'].values[0]
    # transforming data back to df
    df = pd.read_json(df_cleaned, orient='split').copy()
    df = df[df['size'] == slider_value]
    df.drop(['size', 'species', 'kind', 'data_set'], axis=1, inplace=True)

    df = df.transpose()


    df_medidas_centrais = df[:3].copy()
    df_medidas_centrais = df_medidas_centrais.rename_axis('Medidas de tendência central').reset_index()
    df_medidas_centrais.rename({df_medidas_centrais.columns[-1]: f"Resultado ({unidade})"}, inplace=True, axis=1)

    df_dispersao = df[3:7].copy()
    df_dispersao = df_dispersao.rename_axis('Medidas de dispersão').reset_index()
    df_dispersao.rename({df_dispersao.columns[-1]: f"Resultado ({unidade})"}, inplace=True, axis=1)

    df_outras = df[7:].copy()
    df_outras = df_outras.rename_axis('Outras').reset_index()
    df_outras.rename({df_outras.columns[-1]: "Resultado (admensional)"}, inplace=True, axis=1)



    style_data = {
        'whiteSpace': 'normal',
        'height': 'auto'
        }
    style_table = {
        'overflowX': 'auto',
        'overflowY': 'auto',
        'maxHeight': '700px',
    }

    style_cell = {
        'font_size': 'clamp(1rem, 0.5vw, 0.5vh)',
        'textAlign': 'center',
        'height': 'auto',
        'minWidth': '100px',
        'width': '100px',
        'maxWidth': '100px',
        'whiteSpace': 'normal'
    }
    style_header = {
        'fontWeight': 'bold', # deixando em negrito
        }


    # criando a tabela
    table_medidas_centrais = dash_table.DataTable(
                columns = [{'name': str(i), 'id': str(i)} for i in df_medidas_centrais.columns],
                data = df_medidas_centrais.to_dict('records'),
                style_data = style_data,
                style_table = style_table,
                style_cell = style_cell,
                style_header = style_header
                )


    # criando a tabela
    table_dispersao = dash_table.DataTable(
                columns = [{'name': str(i), 'id': str(i)} for i in df_dispersao.columns],
                data = df_dispersao.to_dict('records'),
                style_data = style_data,
                style_table = style_table,
                style_cell = style_cell,
                style_header = style_header
                )

    # criando a tabela
    table_outras = dash_table.DataTable(
                columns = [{'name': str(i), 'id': str(i)} for i in df_outras.columns],
                data = df_outras.to_dict('records'),
                style_data = style_data,
                style_table = style_table,
                style_cell = style_cell,
                style_header = style_header
                )

    # retornando a tabela
    return [table_medidas_centrais, table_dispersao, table_outras]








# --- Callback para atualizar o boxplot --- ###
@callback(
    Output(component_id='estatistica-basica-boxplot', component_property='figure'),
    [
    Input(component_id='estatistica-basica-slider', component_property='value'),
    Input(component_id='estatistica-basica-store-data', component_property='data'),
    Input(component_id='estatistica-basica-store-data-info', component_property='data')
    ],
)
def update_boxplot(slider_value, df_cleaned, df_cleaned_2):
    df = pd.read_json(df_cleaned_2, orient='split').copy()
    eixo_y = f"{df['traducao'].values[0].capitalize()} da flor de Iris {df['variedade'].values[0]} ({df['unidades'].values[0]})"


    df = pd.read_json(df_cleaned, orient='split').copy()
    fig = go.Figure()
    for i in range(1, slider_value+1):
        df_aux = df[:i].copy()
        fig.add_trace(go.Box(y=df_aux[df_aux.columns[0]], boxmean=True, name=str(i), width=0.25))

    fig.update_layout(template='simple_white', # deixando o layout branco
                margin={"r":0,"l":0,"b":0, 't':30}, # removendo margens desnecessárias
                xaxis_title = "Tamanho amostral",
                yaxis_title = eixo_y,
                )
    fig.update_xaxes(showline=True, linewidth=1, linecolor='black', mirror=True) # adicionando linhas no eixo x do grafico
    fig.update_yaxes(showline=True, linewidth=1, linecolor='black', mirror=True) # adicionando linhas no eixo y do gráfico

    # retornando o gráfico
    return fig







@callback(
    [
    Output(component_id='estatistica-basica-animated-plot', component_property='figure'),
    Output(component_id='estatistica-basica-animated-dispersion-plot', component_property='figure'),
    ],
    [
    Input(component_id='estatistica-basica-store-data-animation', component_property='data'),
    Input(component_id='estatistica-basica-store-data-info', component_property='data')
    ],
)
def update_animated_plot(df_cleaned, df_cleaned_2):
    df = pd.read_json(df_cleaned_2, orient='split').copy()
    eixo_y = f"{df['traducao'].values[0].capitalize()} ({df['unidades'].values[0]})"

    # transforming data back to df
    df = pd.read_json(df_cleaned, orient='split').copy()
    df.drop(['data_set'], axis=1, inplace=True)

    fig = px.bar(df, x="Medidas", y="Valores", color="Medidas",
          animation_frame="Tamanho amostral",
          range_y=[0,df['Valores'].max()*1.1]
          )

    fig.update_layout(template='simple_white', # deixando o layout branco
                margin={"r":0,"l":0,"b":0, 't':30}, # removendo margens desnecessárias
                xaxis_title = "",
                yaxis_title = eixo_y
                )

    fig.add_hline(y=0, line_width=1, line_color="black")
    fig.update_xaxes(showline=True, linewidth=1, linecolor='black', mirror=True) # adicionando linhas no eixo x do grafico
    fig.update_yaxes(showline=True, linewidth=1, linecolor='black', mirror=True) # adicionando linhas no eixo y do gráfico




    ####
    df_dispersao = df[df['type'] == 'dispersao'].copy()

    fig_dispersao = px.bar(df_dispersao, x="Medidas", y="Valores", color="Medidas",
          animation_frame="Tamanho amostral",
          range_y=[0,df_dispersao['Valores'].max()*.25]
          )

    fig_dispersao.update_layout(template='simple_white', # deixando o layout branco
                margin={"r":0,"l":0,"b":0, 't':30}, # removendo margens desnecessárias
                xaxis_title = "",
                yaxis_title = eixo_y
                )

    fig_dispersao.add_hline(y=0, line_width=1, line_color="black")
    fig_dispersao.update_xaxes(showline=True, linewidth=1, linecolor='black', mirror=True) # adicionando linhas no eixo x do grafico
    fig_dispersao.update_yaxes(showline=True, linewidth=1, linecolor='black', mirror=True) # adicionando linhas no eixo y do gráfico







    # retornando o gráfico
    return [fig, fig_dispersao]

























#################################################
### Calback para abrir a aba de configurações ###
#################################################
@callback(
    Output("estatistica-basica-offcanvas", "is_open"),
    Input("estatistica-basica-open-offcanvas", "n_clicks"),
    [State("estatistica-basica-offcanvas", "is_open")],
)
def toggle_offcanvas(n1, is_open):
    if n1:
        return not is_open
    return is_open
