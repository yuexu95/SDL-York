import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
import matplotlib.colors as mcolors
import numpy as np
import requests

# import plotly.graph_objects as go

# API URL for reagent data
api_url = "http://192.168.1.11:8700/reagent"

# Fetch data from API
data = requests.get(api_url).json()

# Ensure all wells are represented
rows = ["A", "B", "C", "D", "E", "F", "G", "H"]
cols = list(range(1, 13))
all_wells = [f"{r}{c}" for r in rows for c in cols]

# Fill missing wells with default values
filled_data = {
    well: {
        "location": well,
        "name": "None",
        "volume": 0,
        "lipid_structure": {
            "amines": None,
            "isocyanide": None,
            "lipid_carboxylic_acid": None,
            "lipid_aldehyde": None,
        },
    }
    for well in all_wells
}

# Update filled_data with actual data from the API
for entry in data:
    filled_data[entry["location"]] = entry

# Convert to DataFrame
df = pd.DataFrame(list(filled_data.values()))

# Handle missing volumes by filling them with 0 for visualization
df["volume"] = df["volume"].fillna(0)

# Use session state to persist data
if "df" not in st.session_state:
    st.session_state.df = df.copy()

# Define a colormap using the correct method
min_volume = st.session_state.df["volume"].min()
max_volume = st.session_state.df["volume"].max()
cmap = plt.get_cmap("coolwarm")
norm = mcolors.Normalize(vmin=min_volume, vmax=max_volume)

# Sidebar for updating volumes
st.sidebar.title("Update Stock Solutions")
location = st.sidebar.selectbox(
    "Select Location", options=st.session_state.df["location"].unique()
)
volume_change = st.sidebar.number_input("Volume Change", value=0.0)

if st.sidebar.button("Update Volume"):
    # Find the row to update
    current_volume = st.session_state.df.loc[
        st.session_state.df["location"] == location, "volume"
    ].values[0]
    st.session_state.df.loc[st.session_state.df["location"] == location, "volume"] = (
        current_volume + volume_change
    )
    st.sidebar.success(f"Updated volume at {location}")

    # Recalculate color normalization with the updated data
    min_volume = st.session_state.df["volume"].min()
    max_volume = st.session_state.df["volume"].max()
    norm = mcolors.Normalize(vmin=min_volume, vmax=max_volume)

# Main page display
st.title("96-Well Plate Stock Solution Management")

# Redraw the plot to reflect changes
fig, ax = plt.subplots(figsize=(12, 8))
for idx, row in st.session_state.df.iterrows():
    row_idx = rows.index(row["location"][0])
    col_idx = int(row["location"][1:]) - 1

    # Determine color based on updated volume using colormap
    color = cmap(norm(row["volume"]))

    # Plot circle (dot) for each well
    circle = Circle((col_idx, row_idx), 0.3, color=color, alpha=0.6)
    ax.add_patch(circle)

    # Annotate the circle with the name and updated volume
    ax.text(
        col_idx,
        row_idx,
        f"{row['name']}\n{row['volume']:.1f}",
        ha="center",
        va="center",
        fontsize=8,
        color="black",
    )

# Label the axes
ax.set_xticks(np.arange(len(cols)))
ax.set_xticklabels(cols)
ax.set_yticks(np.arange(len(rows)))
ax.set_yticklabels(rows)
ax.set_xlabel("Column")
ax.set_ylabel("Row")
ax.set_title("96-Well Plate Solution Volumes with Gradient Colors")

# Set the axis limits and aspect
ax.set_xlim(-0.5, len(cols) - 0.5)
ax.set_ylim(-0.5, len(rows) - 0.5)
ax.set_aspect("equal")

# Add grid lines
ax.grid(False)

# Show plot in Streamlit
st.pyplot(fig)
st.dataframe(st.session_state.df)

# # add a line break
# st.markdown("---")

# # BEGIN THE HEATMAP CODE
# df = pd.DataFrame(data)

# # Function to convert well location to grid coordinates
# def location_to_coords(location):
#     if location == 'None':
#         return None, None
#     row = ord(location[0]) - ord('A')
#     col = int(location[1:]) -1
#     return row, col

# # Initialize the 8x12 grid
# grid = np.zeros((8, 12))
# text_grid = [['' for _ in range(12)] for _ in range(8)]

# # Fill the grid with volumes and text information
# for item in data:
#     row, col = location_to_coords(item['location'])
#     if row is not None and col is not None:
#         grid[row, col] = item['volume'] if item['volume'] is not None else 0
#         lipid_structure = item['lipid_structure']
#         lipid_type = next((key for key, value in lipid_structure.items() if value), 'Unknown')
#         text_grid[row][col] = f"location: {item['location']}<br>Volume: {item['volume']}<br>Type: {lipid_type}"

# # Create a heatmap using Plotly
# fig = go.Figure(data=go.Heatmap(
#     # reverse the rows to display in the correct order
#     z=grid[::-1],
#     text=text_grid[::-1],
#     hoverinfo='text',
#     colorscale='Viridis',
#     colorbar=dict(title='Volume')
# ))

# # Update layout
# fig.update_layout(
#     title='96-Well Plate Visualization',
#     xaxis=dict(title='Column', tickmode='array', tickvals=list(range(12)), ticktext=[str(i+1) for i in range(12)]),
#     yaxis=dict(title='Row', tickmode='array', tickvals=list(range(8)), ticktext=[chr(i + ord('A')) for i in range(8)][::-1]
#                ),
#     # width=800,
#     # height=600
# )

# # Display in Streamlit
# st.plotly_chart(fig)
