from dash import html, dcc
import os
import pandas as pd
import plotly.express as px

def get_layout():
    PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
    DATA_DIR = os.path.join(PROJECT_ROOT, 'Data', 'visdata')

    GENRES_PATH = os.path.join(DATA_DIR, 'genres_amount.csv')
    RATINGS_PATH = os.path.join(DATA_DIR, 'genre_ratings.csv')

    if not os.path.exists(GENRES_PATH):
        return html.Div(f"⚠️ Datei nicht gefunden: {GENRES_PATH}")
    if not os.path.exists(RATINGS_PATH):
        return html.Div(f"⚠️ Datei nicht gefunden: {RATINGS_PATH}")

    # --- Diagramm 1: Anzahl Filme pro Genre ---
    genres_amount = pd.read_csv(GENRES_PATH, index_col=0)
    genres_amount.columns = ['Anzahl']
    genres_amount = genres_amount.sort_values('Anzahl', ascending=True)

    fig1 = px.bar(
        genres_amount,
        x='Anzahl',
        y=genres_amount.index,
        orientation='h',
        color='Anzahl',
        color_continuous_scale='Viridis',
        title='🎬 Anzahl an Filmen pro Genre',
        labels={'Anzahl': 'Anzahl Filme', 'index': 'Genre'}
    )

    fig1.update_layout(
        height=800,
        margin=dict(l=160, r=40, t=80, b=40),
        xaxis_title='Anzahl Filme',
        yaxis_title='Genre',
        title_font_size=22,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(size=14, color='#FFFFFF'),
        xaxis=dict(color='#FFFFFF'),
        yaxis=dict(color='#FFFFFF'),
    )

    fig1.update_traces(
        texttemplate='%{x}',
        textposition='outside',
        textfont=dict(color='#FFFFFF', size=10)
    )

    # --- Diagramm 2: Durchschnittliche Bewertung pro Genre ---
    genre_ratings = pd.read_csv(RATINGS_PATH, index_col=0)
    genre_ratings = genre_ratings.sort_values('mean_rating', ascending=True)

    fig2 = px.bar(
        genre_ratings,
        x='mean_rating',
        y=genre_ratings['genres'],
        orientation='h',
        color='mean_rating',
        color_continuous_scale='Bluered',
        title='⭐ Durchschnittliche Bewertung pro Genre',
        labels={'mean_rating': 'Durchschnittliche Bewertung', 'genres': 'Genre'}
    )

    fig2.update_layout(
        height=800,
        margin=dict(l=160, r=40, t=80, b=40),
        xaxis_title='Durchschnittliche Bewertung',
        yaxis_title='Genre',
        title_font_size=22,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(size=14, color='#FFFFFF'),
        xaxis=dict(color='#FFFFFF'),
        yaxis=dict(color='#FFFFFF'),
    )

    fig2.update_traces(
        texttemplate='%{x:.2f}',
        textposition='outside',
        textfont=dict(color='#FFFFFF', size=10)
    )

    # --- Layout zurückgeben ---
    return html.Div([
        html.H2("Film-Genres Übersicht"),
        dcc.Graph(figure=fig1),
        html.H2("Durchschnittliche Bewertung nach Genre"),
        dcc.Graph(figure=fig2)
    ])
