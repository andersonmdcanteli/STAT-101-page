### ------ Importações ------ ###
### ------ From dash ------ ###
# from dash import dcc, html, dash_table
# import dash_bootstrap_components as dbc

### ------ Third part ------ ###
import pandas as pd



### ------ loading ------ ###

df_iris_dataset = pd.read_csv('datasets\\basic_stats_datasets\\iris_dataset.csv')

df_iris_dataset_summary = pd.read_csv('datasets\\basic_stats_datasets\\iris_dataset_summary.csv')

df_iris_dataset_animation = pd.read_csv('datasets\\basic_stats_datasets\\iris_animation_dataset.csv')

df_iris_info = pd.DataFrame({
    "variavel": ["sepal_length", "sepal_width", "petal_length", "petal_width"]*3,
    "traducao": ["comprimento das sépalas", "largura das sépalas", "comprimento das pétalas", "largura das pétalas"]*3,
    "unidades": ["cm", "cm", "cm", "cm"]*3,
    "variedade": ["setosa", "setosa", "setosa", "setosa", "virginica", "virginica", "virginica", "virginica", "versicolor", "versicolor", "versicolor", "versicolor"]
})


























#
