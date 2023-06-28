# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
    style={'textAlign': 'center', 'color': '#503D36', 'font-size': 40})],
),
# TASK 1: Add a Launch Site Drop-down Input Component
                                
dcc.Dropdown(id='site-dropdown',
    options=[
        {'label': 'All Sites', 'value': 'ALL'},
        {'label': 'CCAFS LC-40', 'value': 'site1'},
        {'label': 'CCAFS SLC-40', 'value': 'site2'},
        {'label': 'KFC LC-40', 'value': 'site3'},
        {'label': 'VAFT SLC-4E', 'value': 'site4'}
    ],
    value='ALL',
    placeholder="Select a Launch Site here",
    searchable=True
),
                                    
html.Br(),

# TASK 2:
# Add a callback function to render success-pie-chart based on selected site dropdown

# Function decorator to specify function input and output
@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
              Input(component_id='site-dropdown', component_property='value')
)

def get_pie_chart(entered_site):
    filtered_df = spacex_df
    if entered_site == 'ALL':
        fig = px.pie(spacex_df, values='class', 
        names='Launsh Site', 
        title='Total Successful Launches by Site')
        return fig
    else:
        launches_df = spacex_df.loc[spacex_df['Launch Site'] == entered_site]
        fig = px.pie(launches_df, names='class', title='Total Successful Launches for site',
            color_discrete_sequence = ['red', 'blue'])
        return fig

        # return the outcomes piechart for a selected site
# TASK 3: Add a slider to select payload
dcc.RangeSlider(id='payload-slider',
    min=0, max=10000, step=1000,
    marks={0: '0',
        100: '100'},
    value=[min_payload, max_layload]),


# TASK 4:
# Add a callback function for to render the `success-payload-scatter-chart` scatter plot
@app.callback(Output(component_id='success-payload-scatter-chart', component_property='figure'),
              [Input(component_id='site-dropdown', component_property='value'),
              Input(component_id='payload-slider', component_property='value')])

def get_scatter_plot(dropdown, slider):
    if dropdown == 'ALL':
        filtered_df2 = spacex_df[(spacex_df["Payload Mass (kg)"] >= slider[0]) & (spacex_df["Payload Mass (kg)"] <= slider[1])]
        fig2 = px.scatter(filtered_df2, x="Payload Mass (kg)", y="class", color="Booster Version Category",
                          title = "Payload and Success for All Sites",
                          color_discrete_sequence = ['blue', 'red', 'orange','yellow', 'violet'])
        return fig2
    else:
        filtered_df = spacex_df.loc[spacex_df["Launch Site"] == dropdown]
        filtered_df2 = filtered_df[(spacex_df["Payload Mass (kg)"] >= slider[0]) & (spacex_df["Payload Mass (kg)"] <= slider[1])]
        fig2 = px.scatter(filtered_df2, x="Payload Mass", y="class", color="Booster Version Category",
                          title = "Payload and Success for ")
    
        return fig2

# Run the app
if __name__ == '__main__':
    app.run_server()
