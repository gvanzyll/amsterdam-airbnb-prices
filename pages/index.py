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
             
            Great choice! Amsterdam is an amazing city with great people, tasty food, and much more.          
            
            The one and only downside about visiting Amsterdam is that it can get expensive.
            
            I built this app to help people get an idea of accomodation prices before they go.
            
            Plug in your ideal accomodation criteria and see how much to expect to spend.

            If you want to learn more about how the model works, you can check out my Medium post [here](https://medium.com/@gerrit.van.zyll?p=ae53ab03cbea).

            """
        ),
        dcc.Link(dbc.Button('Predict Prices!', color='primary',
                            style={
                                'fontSize': 25
                            },
                            ),
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
