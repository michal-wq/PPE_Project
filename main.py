from dash import ALL, Dash, Input, Output, ctx, html
from pages import evaluation, home, search


# Initialising the page
app = Dash(__name__)
app.layout = html.Div(home.get_layout(), id="app-content")
app.config.suppress_callback_exceptions = True


@app.callback(
    Output("app-content", "children"),
    Input({"type": "nav-button", "route": ALL}, "n_clicks"),
)
def route_handler(n_clicks):
    triggered = ctx.triggered_id

    if not triggered:
        return home.get_layout()

    route = triggered.get("route")

    match route:
        case "home":
            return home.get_layout()
        case "search":
            return search.get_layout()
        case "evaluation":
            return evaluation.get_layout()
        case _:
            return html.Div("404 – Page Not Found")


search.register_callbacks(app)

app.run(debug=True)
