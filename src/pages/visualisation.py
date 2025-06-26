from dash import html, dcc, Dash
from dash.dependencies import Output, Input, State, ALL
import os
import pandas as pd
import plotly.express as px
from dash import html, dcc

def get_layout():
    PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
    GENRES_PATH = os.path.join(PROJECT_ROOT, 'Data', 'visdata', 'genres_amount.csv')

    if not os.path.exists(GENRES_PATH):
        return html.Div(f"⚠️ Datei nicht gefunden: {GENRES_PATH}")

    # CSV laden und Spalten richtig benennen
    genres_amount = pd.read_csv(GENRES_PATH, index_col=0)
    genres_amount.columns = ['Anzahl']
    genres_amount = genres_amount.sort_values('Anzahl', ascending=True)

    # Plot erstellen
    fig = px.bar(
        genres_amount,
        x='Anzahl',
        y=genres_amount.index,
        orientation='h',
        color='Anzahl',
        color_continuous_scale='Viridis',
        title='🎬 Anzahl an Filmen pro Genre',
        labels={'Anzahl': 'Anzahl Filme', 'index': 'Genre'}
    )

    fig.update_layout(
    xaxis_title='Anzahl Filme',
    yaxis_title='Genre',
    title_font_size=22,
    plot_bgcolor='rgba(0,0,0,0)',
    paper_bgcolor='rgba(0,0,0,0)',
    font=dict(size=14, color='#FFFFFF'),
    xaxis=dict(color='#FFFFFF'),
    yaxis=dict(color='#FFFFFF'),
    )

    fig.update_traces(
        texttemplate='%{x}',
        textposition='outside',
        textfont=dict(color='#FFFFFF')
    )

    return html.Div([
        html.H2("Film-Genres Übersicht"),
        dcc.Graph(figure=fig)
    ])
