# Imports from 3rd party libraries
import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import dash_daq as daq
from dash.dependencies import Input, Output
import pandas as pd

# Imports from this application
from app import app

# Import the model from local machine (also available on Colab)
from joblib import load
model_xgb = load('assets/model_xgb.joblib')
print('pipeline loaded')

# 1 column layout
# https://dash-bootstrap-components.opensource.faculty.ai/l/components/layout
# This will be the section that the user uses to input their ideal criteria
column1 = dbc.Col(
    [
        # Column title, intro text, and format
        dcc.Markdown(
            """

            # Prediction Criteria

            Choose your Airbnb criteria and get a nightly cost estiamte.

            """,
            style={'textAlign': 'center'}
        ),

        # Accomodation type dropdown
        dcc.Markdown('#### Accomodation Type'),
        dcc.Dropdown(
            id='room_type',
            options=[
                {'label': 'Entire home/apt', 'value': 1},
                {'label': 'Shared home/apt', 'value': 0}
            ],
            placeholder='Select an accomodation type',
            value=2,
            className='mb-5'
        ),

        # Rating slider
        # Including everything 4 stars and under together
        dcc.Markdown('#### Rating'),
        dcc.Slider(
            id='review_scores_rating',
            min=4,
            max=5,
            step=.1,
            marks={4: '<= 4',
                   4.2: '4.2',
                   4.4: '4.4',
                   4.6: '4.6',
                   4.8: '4.8',
                   5: '5'},
            value=4,
            className='mb-5'
        ),

        # Number of guests slider
        # Inclduing all guest count over 7 together
        dcc.Markdown('#### Number of Guests'),
        dcc.Slider(
            id='guests_included',
            min=1,
            max=7,
            step=1,
            marks={1: '1',
                   2: '2',
                   3: '3',
                   4: '4',
                   5: '5',
                   6: '6',
                   7: '7+'},
            value=1,
            className='mb-5'

        ),

        # Number of beds slider
        # Inclduing all bed counts over 7 together
        dcc.Markdown('#### Beds'),
        dcc.Slider(
            id='beds',
            min=1,
            max=6,
            step=1,
            marks={1: '1',
                   2: '2',
                   3: '3',
                   4: '4',
                   5: '5',
                   6: '6+'},
            value=1,
            className='mb-5'
        ),

        # Super Host slider
        dcc.Markdown('#### Super Host?'),
        dcc.Dropdown(
            id='host_is_superhost',
            options=[
                {'label': 'Yes', 'value': 1},
                {'label': 'No', 'value': 0}
            ],
            value=2,
            placeholder='Superhost?',
            className='mb-5'
        ),

        # Instant Book dropdown
        dcc.Markdown('#### Instant Book?'),
        dcc.Dropdown(
            id='instant_bookable',
            options=[
                {'label': 'Yes', 'value': 1},
                {'label': 'No', 'value': 0}
            ],
            value=2,
            placeholder='Instant BooK?',
            className='mb-5'
        )

    ],
    md=6,
)
# END COLUMN 1

# START COLUMN 2
# This is where the nightly price estimate will be served

column2 = dbc.Col(
    [
        # Column title and format
        html.H1('Predicted Nightly Price',
                className='mb-5',
                style={'textAlign': 'center'}),
        html.Div(
            id='prediction-content',
            className='lead',
            style={
                'textAlign': 'center',
                'fontSize': 25
            }
        ),
        # Call image function listed below to return image
        html.Div(
            id='image',
            style={
                'textAlign': 'center'
            }
        )
    ]
)

# Page layout setup
layout = dbc.Row([column1, column2])


@ app.callback(
    # Match the columns to the user inputs, make the prediction
    Output('prediction-content', 'children'),
    [Input('room_type', 'value'),
     Input('guests_included', 'value'),
     Input('review_scores_rating', 'value'),
     Input('beds', 'value'),
     Input('host_is_superhost', 'value'),
     Input('instant_bookable', 'value'),
     ],
)
# Prediction function
def predict(room_type, guests_included, review_scores_rating,
            beds, host_is_superhost, instant_bookable):
    ''' 
    Creates a DataFrame from user inputs, then uses the model imported
    in line 13 to make a prediction 
    '''
    # Create DataFrame with user inputs
    # Matches the DatFrame format that the model was trained on
    df = pd.DataFrame(
        columns=['room_type', 'guests_included', 'review_scores_rating',
                 'beds', 'host_is_superhost', 'instant_bookable'],
        data=[[room_type, guests_included, review_scores_rating,
               beds, host_is_superhost, instant_bookable]]
    )
    # Uses the model to make a prediction
    y_pred = model_xgb.predict(df)[0]
    # Create a high and low prediction range
    y_pred_low = y_pred*.94
    y_pred_high = y_pred*1.06
    # Return the prediction to the user
    return f'€{y_pred_low:.0f} - €{y_pred_high:.0f}'


@app.callback(
    # Return the image once a user engages with the prediction criteria
    Output('image', 'children'),
    [Input('room_type', 'value')]
)
# Image function
def imgage(room_type):
    '''Simple image function to return an image to accompany a prediction'''
    if room_type <= 1:
        return html.Img(src='assets/pic.jpg', className='img', style={'height': '500px'})
