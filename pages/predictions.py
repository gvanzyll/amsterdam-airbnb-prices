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


from joblib import load
model_xgb = load('assets/model_xgb.joblib')
print('pipeline loaded')


# 1 column layout
# https://dash-bootstrap-components.opensource.faculty.ai/l/components/layout



column1 = dbc.Col(
    [
        dcc.Markdown(
            """

            # Prediction Criteria

            Choose your Airbnb criteria and get a nightly cost estiamte.

            """,
            style={'textAlign': 'center'}
        ),


        # column1 = dbc.Col(


        #         html.H2('Prediction Criteria',
        #                 className='mb-5',
        #                 style={'textAlign': 'center'}),

        # ),

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

        # dcc.Markdown('#### Superhost?'),
        # dcc.Slider(
        #     id='host_is_superhost',
        #     min=0,
        #     max=1,
        #     step=1,
        #     marks={0: 'Yes',
        #            1: 'No'},
        #     value=1,
        #     className='mb-5'
        # ),

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

        # dcc.Markdown('#### Instant Book?'),
        # dcc.Slider(
        #     id='instant_bookable',
        #     min=0,
        #     max=1,
        #     step=1,
        #     marks={0: 'Yes',
        #            1: 'No'},
        #     value=1,
        #     className='mb-5'
        # )

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

column2 = dbc.Col(
    [

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
        html.Div(
            id='image',
            style={
                'textAlign': 'center'
            }
        )
    ]
)

layout = dbc.Row([column1, column2])


@ app.callback(
    Output('prediction-content', 'children'),
    [Input('room_type', 'value'),
     Input('guests_included', 'value'),
     Input('review_scores_rating', 'value'),
     Input('beds', 'value'),
     Input('host_is_superhost', 'value'),
     Input('instant_bookable', 'value'),
     ],
)
def predict(room_type, guests_included, review_scores_rating, beds, host_is_superhost, instant_bookable):
    df = pd.DataFrame(
        columns=['room_type', 'guests_included', 'review_scores_rating',
                 'beds', 'host_is_superhost', 'instant_bookable'],
        data=[[room_type, guests_included, review_scores_rating,
               beds, host_is_superhost, instant_bookable]]
    )
    y_pred = model_xgb.predict(df)[0]
    y_pred_low = y_pred*.94
    y_pred_high = y_pred*1.06
    return f'€{y_pred_low:.0f} - €{y_pred_high:.0f}'


@app.callback(
    Output('image', 'children'),
    [Input('room_type', 'value')]
)
def imgage(room_type):
    if room_type <= 1:
        return html.Img(src='assets/pic.jpg', className='img', style={'height': '500px'})
