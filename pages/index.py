# Imports from 3rd party libraries
import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px

# Imports from this application
from app import app

# 2 column layout. 1st column width = 4/12
# https://dash-bootstrap-components.opensource.faculty.ai/l/components/layout
column1 = dbc.Col(
    [
        dcc.Markdown(
            """
        
            ## Thinking about visitng Amsterdam? 

            Get an idea of Airbnb prices in and around the city.

            Plug in your ideal accomodation criteria and see how much to expect to spend.

            """
        ),
        dcc.Link(dbc.Button('Predict Prices!', color='primary'),
                 href='/predictions')
    ],
    md=4,
)


column2 = dbc.Col(
    [
        html.Img(src='assets/home.jpg', className='img-fluid'),

    ]
)

layout = dbc.Row([column1, column2])