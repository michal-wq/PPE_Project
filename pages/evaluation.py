from dash import html
from dash.dependencies import Output, Input

layout = html.Div(
    ["ik ben het aan werken"],
    className="homepage-content",
)


def get_layout():
    return layout
