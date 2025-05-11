from dash import Dash, html, dcc
import home_page

app = Dash(__name__)


app.layout = home_page.layout

app.run(debug=True)
