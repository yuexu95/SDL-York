import streamlit as st
import requests
import pandas as pd
import numpy as np
import plotly.graph_objects as go



import requests

base_url = "http://192.168.1.11:8700"
def fetch_stock_soliution():
    requets_url = base_url + "/reagent"
    return requests.get(requets_url).json()

st.title('Stock Solution Information')

data = fetch_stock_soliution()
# Convert data to DataFrame
df = pd.DataFrame(data)

# Function to convert well location to grid coordinates
def location_to_coords(location):
    if location == 'None':
        return None, None
    row = ord(location[0]) - ord('A')
    col = int(location[1:]) -1
    return row, col

# Initialize the 8x12 grid
grid = np.zeros((8, 12))
text_grid = [['' for _ in range(12)] for _ in range(8)]

# Fill the grid with volumes and text information
for item in data:
    row, col = location_to_coords(item['location'])
    if row is not None and col is not None:
        grid[row, col] = item['volume'] if item['volume'] is not None else 0
        lipid_structure = item['lipid_structure']
        lipid_type = next((key for key, value in lipid_structure.items() if value), 'Unknown')
        text_grid[row][col] = f"location: {item['location']}<br>Volume: {item['volume']}<br>Type: {lipid_type}"

# Create a heatmap using Plotly
fig = go.Figure(data=go.Heatmap(
    # reverse the rows to display in the correct order
    z=grid[::-1],
    text=text_grid[::-1],
    hoverinfo='text',
    colorscale='Viridis',
    colorbar=dict(title='Volume')
))

# Update layout
fig.update_layout(
    title='96-Well Plate Visualization',
    xaxis=dict(title='Column', tickmode='array', tickvals=list(range(12)), ticktext=[str(i+1) for i in range(12)]),
    yaxis=dict(title='Row', tickmode='array', tickvals=list(range(8)), ticktext=[chr(i + ord('A')) for i in range(8)][::-1]
               ),
    width=800,
    height=600
)

# Display in Streamlit
st.plotly_chart(fig)