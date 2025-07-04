from dash import ALL, Dash, Input, Output, ctx, html
from src.pages import evaluation, home, search, imprint, visualisation
from dash.exceptions import PreventUpdate
import src.state as state

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

    # Guard: only act if a button was actually clicked
    if not triggered:
        return home.get_layout()

    global user_inputs, min_rating, max_rating
    i = [i for i, btn_id in enumerate(ctx.inputs_list[0]) if btn_id["id"] == triggered][
        0
    ]
    if n_clicks[i] is None or n_clicks[i] < 1:
        raise PreventUpdate

    route = triggered.get("route")

    match route:
        case "search":
            state.reset_search_page_vars()
            return search.get_layout()
        case "evaluation":
            state.reset_evaluation_page_vars()
            return evaluation.get_layout(
                state.user_inputs, state.min_rating, state.max_rating
            )
        case "home":
            return home.get_layout()
        case "imprint":
            return imprint.get_layout()
        case "visualisation":
            return visualisation.get_layout()
        case _:
            return html.Div("404 – Page Not Found")


search.register_callbacks(app)

app.run(debug=True)
