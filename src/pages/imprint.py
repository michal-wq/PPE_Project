from dash import html

header = html.Button(
    [
        html.Img(src="./assets/img/Logo.svg", className="search-bar-logo"),
    ],
    id={"type": "nav-button", "route": "home"},
    className="search-bar-container",
)

layout = html.Div(
    [
        header,
        html.Div(
            [
                html.H2("Imprint"),
                html.H4("Website Created By"),
                html.P("Filip Vrlec"),
                html.P("Michał Ryszard Karczmarzyk"),
                html.P("Alessio Luigi De Icco"),
                html.Br(),
                html.P("University of Applied Sciences of the Grisons (FHGR)"),
                html.P("Pulvermühlestrasse 57"),
                html.P("7000 Chur"),
                html.P("Switzerland"),
                html.Hr(),
                html.H4("Purpose of the Website"),
                html.P(
                    "This website was created as part of a university course project at the "
                    "University of Applied Sciences of the Grisons (FHGR), in the context of "
                    "programming and prompt engineering."
                ),
                html.P(
                    "Its sole purpose is to demonstrate technical skills in data handling, interactive web applications, "
                    "and recommendation systems using Python and Dash."
                ),
                html.P(
                    "This is a non-commercial student project. No user data is collected or stored."
                ),
                html.Hr(),
                html.H4("Data Source"),
                html.P(
                    [
                        "Movie information is based on publicly available data from ",
                        html.A(
                            "MovieLens",
                            href="https://grouplens.org/datasets/movielens/",
                            target="_blank",
                        ),
                        ", provided by the GroupLens research lab at the University of Minnesota.",
                    ]
                ),
                html.P("All rights to that data remain with the original owners."),
                html.Hr(),
                html.H4("Disclaimer"),
                html.P("This site is for demonstration and academic purposes only."),
                html.P(
                    "The creators do not guarantee the accuracy or completeness of any content shown."
                ),
                html.Hr(),
                html.H4("Copyright Notice"),
                html.P(
                    "© 2025 Filip Vrlec, Michał Ryszard Karczmarzyk, Alessio Luigi De Icco"
                ),
                html.P("All rights reserved unless otherwise stated."),
            ]
        ),
    ],
    className="imprint-content",
)


def get_layout():
    return layout
