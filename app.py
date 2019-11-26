import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

import dash_bootstrap_components as dbc

import altair as alt
import vega_datasets

app = dash.Dash(__name__, assets_folder='assets')
server = app.server

app.title = 'Dash app with pure Altair HTML'

def make_plot(xaxis_column_name = 'Displacement', yaxis_column_name = 'Horsepower'):
    
    def mds_special():
        font = "Arial"
        axisColor = "#000000"
        gridColor = "#DEDDDD"
        return {
            "config": {
                "title": {
                    "fontSize": 24,
                    "font": font,
                    "anchor": "start", # equivalent of left-aligned.
                    "fontColor": "#000000"
                },
                'view': {
                    "height": 300, 
                    "width": 400
                },
                "axisX": {
                    "domain": True,
                    #"domainColor": axisColor,
                    "gridColor": gridColor,
                    "domainWidth": 1,
                    "grid": False,
                    "labelFont": font,
                    "labelFontSize": 12,
                    "labelAngle": 0, 
                    "tickColor": axisColor,
                    "tickSize": 5, # default, including it just to show you can change it
                    "titleFont": font,
                    "titleFontSize": 16,
                    "titlePadding": 10, # guessing, not specified in styleguide
                    "title": "X Axis Title (units)", 
                },
                "axisY": {
                    "domain": False,
                    "grid": True,
                    "gridColor": gridColor,
                    "gridWidth": 1,
                    "labelFont": font,
                    "labelFontSize": 14,
                    "labelAngle": 0, 
                    #"ticks": False, # even if you don't have a "domain" you need to turn these off.
                    "titleFont": font,
                    "titleFontSize": 16,
                    "titlePadding": 10, # guessing, not specified in styleguide
                    "title": "Y Axis Title (units)", 
                    # titles are by default vertical left of axis so we need to hack this 
                    #"titleAngle": 0, # horizontal
                    #"titleY": -10, # move it up
                    #"titleX": 18, # move it to the right so it aligns with the labels 
                },
            }
                }

# register the custom theme under a chosen name
    alt.themes.register('mds_special', mds_special)

    # enable the newly registered theme
    alt.themes.enable('mds_special')
    #alt.themes.enable('none') # to return to default

    typeDict = {'Displacement':'quantitative',
                'Cylinders':'quantitative',
                'Miles_per_Gallon':'quantitative'
    }

        # Create a plot of the Displacement and the Horsepower of the cars dataset
    chart = alt.Chart(vega_datasets.data.cars.url).mark_point(size=90).encode(
                alt.X(xaxis_column_name,type='quantitative', title="xaxis_column_name"),
                alt.Y(yaxis_column_name,type='quantitative', title = "y_axis"),
                tooltip = [{"type":typeDict[xaxis_column_name], "field":xaxis_column_name},
                            'Horsepower:Q',]
            ).properties(title='Horsepower vs. Displacement',
                        width=500, height=350).interactive()

    return chart

app.layout = html.Div([

    ### ADD CONTENT HERE like: html.H1('text'),
    html.H1('My first dashboard is so cool'),
    #html.img('img.jpg')

    html.Img(src='https://upload.wikimedia.org/wikipedia/commons/thumb/b/b7/Unico_Anello.png/1920px-Unico_Anello.png', 
            width='10%'),

    html.Iframe(
        sandbox='allow-scripts',
        id='plot',
        height='1000',
        width='1800',
        style={'border-width': '0'},

        ################ The magic happens here
        srcDoc=make_plot().to_html()
        ################ The magic happens here
        ),
    dcc.Markdown('''
    ### Here is a markdown cell
     <!--![Image](https://upload.wikimedia.org/wikipedia/commons/thumb/b/b7/Unico_Anello.png/1920px-Unico_Anello.png)>

     ```
     print("yay")
     ```
    '''
     ),

dcc.Dropdown(
id='dd-chart',
options=[
    {'label': 'Miles_per_Gallon', 'value': 'Miles_per_Gallon'},
    {'label': 'Cylinders', 'value': 'Cylinders'},
    {'label': 'Displacement', 'value': 'Displacement'},
    # Missing option here
],
value='Displacement',
style=dict(width='45%',
           verticalAlign="middle")
          ),
dcc.Dropdown(
id='dd-chart-y',
options=[
    {'label': 'Miles_per_Gallon', 'value': 'Miles_per_Gallon'},
    {'label': 'Cylinders', 'value': 'Cylinders'},
    {'label': 'Displacement', 'value': 'Displacement'},
    # Missing option here
],
value='Displacement',
style=dict(width='45%',
           verticalAlign="middle")
          )

        ])
@app.callback(
    dash.dependencies.Output('plot', 'srcDoc'),
    [dash.dependencies.Input('dd-chart', 'value'),
    dash.dependencies.Input('dd-chart-y', 'value')])
def update_plot(xaxis_column_name, yaxis_column_name):
    '''
    Takes in an xaxis_column_name and calls make_plot to update our Altair figure
    '''
    updated_plot = make_plot(xaxis_column_name, yaxis_column_name).to_html()
    return updated_plot


if __name__ == '__main__':
    app.run_server(debug=True)




