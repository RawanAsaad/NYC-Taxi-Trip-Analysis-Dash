
import pandas as pd
import plotly.express as px
import dash
from dash import dcc, html, dash_table
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc

# Load dataset
df = pd.read_csv("ny_taxi.csv")
df = df[df['fare_amount'] > 0]
df = df[(df['passenger_count'] > 0) & (df['passenger_count'] <= 6)]

# Convert datetime columns
df['pickup_datetime'] = pd.to_datetime(df['tpep_pickup_datetime'])
df['dropoff_datetime'] = pd.to_datetime(df['tpep_dropoff_datetime'])

# Add derived columns
df['trip_duration'] = (df['dropoff_datetime'] - df['pickup_datetime']).dt.total_seconds() / 60
df = df[df['trip_duration'] > 0]

# Filter out bad lat/lon ranges
df = df[
    (df['pickup_longitude'].between(-74.5, -73.5)) &
    (df['dropoff_longitude'].between(-74.5, -73.5)) &
    (df['pickup_latitude'].between(40.5, 41)) &
    (df['dropoff_latitude'].between(40.5, 41))
]

# Prepare values for controls
vendors = df['VendorID'].dropna().unique()
fare_min = df['fare_amount'].min()
fare_max = df['fare_amount'].max()
date_min = df['pickup_datetime'].min().date()
date_max = df['pickup_datetime'].max().date()

# Start Dash app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.MINTY])

# Visualization functions
def map_pickups(dff):
    fig = px.scatter_mapbox(
        dff,
        lat='pickup_latitude',
        lon='pickup_longitude',
        color='VendorID',
        zoom=10,
        height=500,
        mapbox_style='open-street-map',
        title='🗺️ Pickup Locations by Vendor'
    )
    return dcc.Graph(figure=fig)

def fare_histogram(dff):
    fig = px.histogram(
        dff,
        x='fare_amount',
        color='VendorID',
        nbins=60,
        title='💰 Fare Distribution per Vendor'
    )
    return dcc.Graph(figure=fig)

def duration_vs_distance(dff):
    fig = px.scatter(
        dff,
        x='trip_distance',
        y='trip_duration',
        color='payment_type',
        title='🕒 Trip Duration vs Distance by Payment Type',
        labels={'trip_distance': 'Distance (miles)', 'trip_duration': 'Duration (min)'}
    )
    return dcc.Graph(figure=fig)

def trip_summary(dff):
    most_common_payment = dff['payment_type'].mode().iloc[0] if not dff.empty else 'N/A'
    most_common_pickup = (dff['pickup_latitude'].astype(str) + ", " + dff['pickup_longitude'].astype(str)).mode().iloc[0] if not dff.empty else 'N/A'
    summary_df = pd.DataFrame({
        'Metric': ['Total Trips', 'Average Fare', 'Most Common Payment', 'Most Frequent Pickup Location'],
        'Value': [
            len(dff),
            round(dff['fare_amount'].mean(), 2) if not dff.empty else 0,
            most_common_payment,
            most_common_pickup
        ]
    })
    return dash_table.DataTable(
        columns=[{"name": i, "id": i} for i in summary_df.columns],
        data=summary_df.to_dict('records'),
        style_table={'width': '100%'},
        style_cell={'textAlign': 'left'},
        style_header={'fontWeight': 'bold'}
    )

# Layout
app.layout = dbc.Container([
    html.H2("🚖 NYC Taxi Trip Dashboard", className="text-center my-4", style={"font-weight": "bold"}),

    dbc.Card([
        dbc.CardBody([
            dbc.Row([
                dbc.Col([
                    html.Label("🧭 Vendor", style={"font-weight": "bold"}),
                    dcc.Dropdown(
                        id='vendor-dropdown',
                        options=[{'label': f'Vendor {v}', 'value': v} for v in vendors],
                        value=list(vendors),
                        multi=True
                    )
                ], md=4),

                dbc.Col([
                    html.Label("💲 Max Fare Amount", style={"font-weight": "bold"}),
                    dcc.Slider(
                        id='fare-slider',
                        min=fare_min,
                        max=fare_max,
                        value=50,
                        step=1,
                        marks={int(f): str(int(f)) for f in range(int(fare_min), int(fare_max), 30)},
                        tooltip={"placement": "bottom", "always_visible": True}
                    )
                ], md=4),

                dbc.Col([
                    html.Label("📅 Pickup Date Range", style={"font-weight": "bold"}),
                    dcc.DatePickerRange(
                        id='date-picker',
                        start_date=date_min,
                        end_date=date_max,
                        min_date_allowed=date_min,
                        max_date_allowed=date_max
                    )
                ], md=4)
            ])
        ])
    ], className="mb-4"),

    dbc.Alert(id='live-summary', color="light", className="text-center font-weight-bold"),

    dbc.Tabs([
        dbc.Tab(label="Summary", tab_id="summary"),
        dbc.Tab(label="Fare Histogram", tab_id="histogram"),
        dbc.Tab(label="Trip Duration vs Distance", tab_id="scatter"),
        dbc.Tab(label="Pickup Locations", tab_id="map")
    ], id="tabs", active_tab="summary", className="mb-4"),

    html.Div(id="tab-output")
])

# Callbacks
@app.callback(
    Output("live-summary", "children"),
    Input("vendor-dropdown", "value"),
    Input("fare-slider", "value"),
    Input("date-picker", "start_date"),
    Input("date-picker", "end_date")
)
def update_live_summary(vendor_ids, max_fare, start_date, end_date):
    dff = df[
        (df['VendorID'].isin(vendor_ids)) &
        (df['fare_amount'] <= max_fare) &
        (df['pickup_datetime'].dt.date >= pd.to_datetime(start_date).date()) &
        (df['pickup_datetime'].dt.date <= pd.to_datetime(end_date).date())
    ]
    return f"📊 Q3: Total Trips = {len(dff)} | 💵 Q4: Avg Fare = ${dff['fare_amount'].mean():.2f}"

@app.callback(
    Output("tab-output", "children"),
    Input("tabs", "active_tab"),
    Input("vendor-dropdown", "value"),
    Input("fare-slider", "value"),
    Input("date-picker", "start_date"),
    Input("date-picker", "end_date")
)
def update_tab(tab, vendor_ids, max_fare, start_date, end_date):
    dff = df[
        (df['VendorID'].isin(vendor_ids)) &
        (df['fare_amount'] <= max_fare) &
        (df['pickup_datetime'].dt.date >= pd.to_datetime(start_date).date()) &
        (df['pickup_datetime'].dt.date <= pd.to_datetime(end_date).date())
    ]

    if tab == "summary":
        return trip_summary(dff)
    elif tab == "histogram":
        return fare_histogram(dff)
    elif tab == "map":
        return map_pickups(dff)
    elif tab == "scatter":
        return duration_vs_distance(dff)
    return html.Div("Select a tab.")

# Run the app
if __name__ == "__main__":
    app.run(debug=True)
