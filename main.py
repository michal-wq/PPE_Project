from dash import Dash, html
from pages import home, search


# Initialising the page
app = Dash(__name__)
app.layout = html.Div(home.get_layout(), id="app-content")
app.config.suppress_callback_exceptions = True

home.register_callbacks(app)
search.register_callbacks(app)

app.run(debug=True)
