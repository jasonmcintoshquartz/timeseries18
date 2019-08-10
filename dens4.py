import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import gaussian_kde

import pandas as pd
import plotly.graph_objs as go

import gcsfs

import matplotlib.pyplot as plt
from scipy.stats import gaussian_kde


df_2 = pd.read_csv('gs://jason_bucket12/sp3.csv')
df_3 = pd.read_csv('gs://jason_bucket12/density.csv')
df_1 = pd.read_csv('gs://jason_bucket12/ave.csv')

#jason_css = ['https://raw.githubusercontent.com/jasonmcintoshquartz/timeseries8/master/bWLwgP.css']

app = dash.Dash(__name__)

app.layout = html.Div([
    dcc.Graph(id='graph-with-slider'),
    dcc.Slider(
        id='year-slider',
        min=df_2['year'].min(),
        max=df_2['year'].max(),
        value=df_2['year'].min(),
        marks={str(year): str(year) for year in df_2['year'].unique()},
        step=None
    )
])

@app.callback(
    Output('graph-with-slider', 'figure'),
    [Input('year-slider', 'value')])
def update_figure(selected_year):
    filtered_df_2 = df_2[df_2.year == selected_year]
    filtered_df_3 = df_3[df_3.year == selected_year]
    filtered_df_1 = df_1[df_1.year == selected_year]
    traces1 = []
    for A in filtered_df_1.Forecast.unique():
        df_1_by_Forecast = filtered_df_1
        traces1.append(go.Scatter(
            x=df_1_by_Forecast['pop'],
            y=df_1_by_Forecast['ave'],
            mode='lines',
            opacity=0.7,
            marker={
                'size': 2,
                'line': {'width': 0.2},
				'color': 'black'
            },
        ))
		
    traces2 = []
    for B in filtered_df_2.Ratio.unique():
        df_2_by_Ratio = filtered_df_2[filtered_df_2['Ratio'] == B]
        traces2.append(go.Scatter(
            x=df_2_by_Ratio['pop'],
            y=df_2_by_Ratio['close_adj'],
            mode='lines',
            opacity=0.7,
            marker={
                'size': 2,
                'line': {'width': 0.2, 'color': 'grey'},
				'color': 'black'
            },
			name=B
        ))
		
    traces3 = []
    for C in filtered_df_3.Ratio1.unique():
        df_3_by_Ratio = filtered_df_3[filtered_df_3['Ratio1'] == C]

        # data
        xp = df_3_by_Ratio['pop']
        yp = df_3_by_Ratio['scat']

        # Calculate the point density
        xy = np.vstack([xp,yp])
        z = gaussian_kde(xy)(xy)

        # Sort the points by density, so that the densest points are plotted last
        idx = z.argsort()
        xl, yl, z = xp.iloc[idx], yp.iloc[idx], z[idx]
        traces3.append(go.Scatter(
            x=xl,
            y=yl,
            mode='markers',
            opacity=0.8,
            marker={
			    #size is z if you want variable
                'size': 5,
                'sizemode': 'area',
                #'sizeref': 1.*max(z)/(3.**2),
                #'sizemin': 1,
                'line': {'width': 0.01},
                'color': z,
                'colorscale':'Jet'
            },
            name=C
        ))
	
    return {
        'data': traces3+traces2+traces1,
        'layout': go.Layout(
            xaxis={'type': 'linear', 'title': 'Date', 'showgrid': True, 'gridcolor': ('#F1F1F1'), 'automargin': True, 'tickmode': 'array', 'tickvals': df_2['pop'], 'ticktext': df_2['date'], 'showgrid': False, 'showticklabels': False},
            yaxis={'title': 'Close', 'range': [20, 5000], 'showgrid': True, 'gridcolor': ('#F1F1F1'), 'automargin': True},
            margin={'l': 60, 'b': 60, 't': 10, 'r': 10},
            legend={'x': 0, 'y': 1},
			font = dict(family='Courier New,  monospace', size=12, color="#7f7f7f"),
            hovermode='closest'
        )
   }
   
if __name__ == '__main__':
    app.run_server(debug=True)
	
#main_div = html.Div(children = [
    # sub-div for the plot
    #html.Div(children = [
                #dcc.Graph(id = 'my-plot'),
    #])
    #],
    # set the sizing of the parent div
    #style = {'display': 'inline-block', 'width': '48%'})	