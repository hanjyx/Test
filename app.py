import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html
from dash.dependencies import Input, Output

# Data from Task 10.10
data = pd.read_csv("student_lifestyle_dataset.csv")
df = pd.DataFrame(data)

# Dash
app = Dash(__name__)

# For deployment
server = app.server

# App Layout
app.layout = html.Div([
    html.H1("Impact of Study Hours on a Student's GPA and Stress Levels", style = {'textAlign': 'center'}),

    html.Label('Select Stress Level:'),
    dcc.Dropdown(
        id = 'stress-dropdown',
        options = [{'label': stress, 'value': stress} for stress in df['Stress_Level'].unique()],
        value = [],
        multi = True,
        placeholder = 'Select stress level'
    ),
    dcc.Graph(id = 'stress-chart')
])

# App callback
@app.callback(
    Output('stress-chart', 'figure'),
    [Input('stress-dropdown', 'value')]
)

def update_chart(selected_stress):
    if not selected_stress:
        filtered_df = df  # Show all data if no stress level is selected
    else:
        filtered_df = df[df['Stress_Level'].isin(selected_stress)]

    fig = px.scatter(
        filtered_df,
        x='Study_Hours_Per_Day',
        y='GPA',
        color='Stress_Level',
        color_discrete_map={
            "High": "orangered",
            "Moderate": "orange",
            "Low": "seagreen"
        },
        title="Impact of Study Hours on a Student's GPA and Stress Levels",
        labels={'Study_Hours_Per_Day': 'Study Hours per Day', 'GPA': 'GPA', 'Stress_Level': 'Stress Level'}
    )
    return fig

if __name__ == "__main__":
    app.run(debug=True)