from dash import Dash, html, dcc
from pages import home, search
import dash

# Initialising the page
app = Dash(__name__)
app.layout = html.Div(home.get_layout(), id="app-content")


# When a navigation button is pressed, it gets read and then changes the layout to the desired page
@app.callback(
    dash.dependencies.Output("app-content", "children"),
    [dash.dependencies.Input("change-search-view", "n_clicks")],
)
def change_page(change_to_search_view):
    if change_to_search_view > 0:
        return search.get_layout()

    return home.get_layout()


app.run(debug=True)
