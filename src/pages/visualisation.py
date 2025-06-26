from dash import html, dcc, Dash
from dash.dependencies import Output, Input, State, ALL
import pandas as pd
import src.state as state
import os

# und o no an liniadiagramm wo zeigt welche genres am meista gmacht wora sind im jeweiliga johr oder so
# zum beispiel an balka diagramm, wo s mean rating zeigt vo allna film vo jeweilige genres


def get_layout():


    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    GENRES_PATH = os.path.join(BASE_DIR, '..', 'Data', 'visdata', 'genres_amount.csv')
    GENRES_PATH = os.path.abspath(GENRES_PATH)


    # Daten aus state laden
    genres_amount = pd.read_csv(GENRES_PATH)

    # Falls es eine Series ist, in DataFrame umwandeln
    if isinstance(genres_amount, pd.Series):
        genres_amount = genres_amount.sort_values(ascending=True)
        df = genres_amount.reset_index()
        df.columns = ['Genre', 'Anzahl']
    else:
        # Falls schon DataFrame mit 'Genre' und 'Anzahl'
        df = genres_amount.sort_values(by=genres_amount.columns[0], ascending=True)

    # Plot erstellen
    fig = px.bar(
        df,
        x='Anzahl',
        y='Genre',
        orientation='h',
        color='Anzahl',
        color_continuous_scale='Viridis',
        title='🎬 Anzahl an Filmen pro Genre'
    )

    fig.update_layout(
        xaxis_title='Anzahl Filme',
        yaxis_title='Genre',
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(size=14),
        title_font_size=22,
    )

    fig.update_traces(texttemplate='%{x}', textposition='outside')

    # Dash-Komponenten zurückgeben
    return html.Div([
        html.H2("Film-Genres Übersicht"),
        dcc.Graph(figure=fig)
    ])
