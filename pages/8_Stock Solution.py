import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
import matplotlib.colors as mcolors
import matplotlib.cm as cm
import numpy as np

# Sample data
data = [
    {"location": "A1", "name": "A1", "volume": -560.0, "lipid_structure": {"amines": "A1", "isocyanide": None, "lipid_carboxylic_acid": None, "lipid_aldehyde": None}},
    {"location": "B1", "name": "None", "volume": None, "lipid_structure": {"amines": None, "isocyanide": None, "lipid_carboxylic_acid": None, "lipid_aldehyde": None}},
    {"location": "C1", "name": "None", "volume": None, "lipid_structure": {"amines": None, "isocyanide": None, "lipid_carboxylic_acid": None, "lipid_aldehyde": None}},
    {"location": "D1", "name": "None", "volume": None, "lipid_structure": {"amines": None, "isocyanide": None, "lipid_carboxylic_acid": None, "lipid_aldehyde": None}},
    {"location": "E1", "name": "None", "volume": None, "lipid_structure": {"amines": None, "isocyanide": None, "lipid_carboxylic_acid": None, "lipid_aldehyde": None}},
    {"location": "F1", "name": "None", "volume": None, "lipid_structure": {"amines": None, "isocyanide": None, "lipid_carboxylic_acid": None, "lipid_aldehyde": None}},
    {"location": "G1", "name": "D13", "volume": 880.0, "lipid_structure": {"amines": None, "isocyanide": None, "lipid_carboxylic_acid": "D13", "lipid_aldehyde": None}},
    {"location": "H1", "name": "None", "volume": None, "lipid_structure": {"amines": None, "isocyanide": None, "lipid_carboxylic_acid": None, "lipid_aldehyde": None}},
    {"location": "A2", "name": "A2", "volume": 240.0, "lipid_structure": {"amines": "A2", "isocyanide": None, "lipid_carboxylic_acid": None, "lipid_aldehyde": None}},
    {"location": "B2", "name": "None", "volume": None, "lipid_structure": {"amines": None, "isocyanide": None, "lipid_carboxylic_acid": None, "lipid_aldehyde": None}},
    {"location": "C2", "name": "None", "volume": None, "lipid_structure": {"amines": None, "isocyanide": None, "lipid_carboxylic_acid": None, "lipid_aldehyde": None}},
    {"location": "D2", "name": "None", "volume": None, "lipid_structure": {"amines": None, "isocyanide": None, "lipid_carboxylic_acid": None, "lipid_aldehyde": None}},
    {"location": "E2", "name": "None", "volume": None, "lipid_structure": {"amines": None, "isocyanide": None, "lipid_carboxylic_acid": None, "lipid_aldehyde": None}},
    {"location": "F2", "name": "None", "volume": None, "lipid_structure": {"amines": None, "isocyanide": None, "lipid_carboxylic_acid": None, "lipid_aldehyde": None}},
    {"location": "G2", "name": "None", "volume": None, "lipid_structure": {"amines": None, "isocyanide": None, "lipid_carboxylic_acid": None, "lipid_aldehyde": None}},
    {"location": "H2", "name": "D26", "volume": 880.0, "lipid_structure": {"amines": None, "isocyanide": None, "lipid_carboxylic_acid": "D26", "lipid_aldehyde": None}},
    {"location": "A3", "name": "None", "volume": None, "lipid_structure": {"amines": None, "isocyanide": None, "lipid_carboxylic_acid": None, "lipid_aldehyde": None}},
    {"location": "B3", "name": "None", "volume": None, "lipid_structure": {"amines": None, "isocyanide": None, "lipid_carboxylic_acid": None, "lipid_aldehyde": None}},
    {"location": "C3", "name": "None", "volume": None, "lipid_structure": {"amines": None, "isocyanide": None, "lipid_carboxylic_acid": None, "lipid_aldehyde": None}},
    {"location": "D3", "name": "B7", "volume": 400.0, "lipid_structure": {"amines": None, "isocyanide": "B7", "lipid_carboxylic_acid": None, "lipid_aldehyde": None}},
    {"location": "E3", "name": "None", "volume": None, "lipid_structure": {"amines": None, "isocyanide": None, "lipid_carboxylic_acid": None, "lipid_aldehyde": None}},
    {"location": "F3", "name": "None", "volume": None, "lipid_structure": {"amines": None, "isocyanide": None, "lipid_carboxylic_acid": None, "lipid_aldehyde": None}},
    {"location": "G3", "name": "None", "volume": None, "lipid_structure": {"amines": None, "isocyanide": None, "lipid_carboxylic_acid": None, "lipid_aldehyde": None}},
    {"location": "H3", "name": "D27", "volume": 880.0, "lipid_structure": {"amines": None, "isocyanide": None, "lipid_carboxylic_acid": "D27", "lipid_aldehyde": None}},
    {"location": "A4", "name": "A4", "volume": 2000.0, "lipid_structure": {"amines": "A4", "isocyanide": None, "lipid_carboxylic_acid": None, "lipid_aldehyde": None}},
    {"location": "B4", "name": "None", "volume": None, "lipid_structure": {"amines": None, "isocyanide": None, "lipid_carboxylic_acid": None, "lipid_aldehyde": None}},
    {"location": "C4", "name": "None", "volume": None, "lipid_structure": {"amines": None, "isocyanide": None, "lipid_carboxylic_acid": None, "lipid_aldehyde": None}},
    {"location": "D4", "name": "None", "volume": None, "lipid_structure": {"amines": None, "isocyanide": None, "lipid_carboxylic_acid": None, "lipid_aldehyde": None}},
    {"location": "E4", "name": "None", "volume": None, "lipid_structure": {"amines": None, "isocyanide": None, "lipid_carboxylic_acid": None, "lipid_aldehyde": None}},
    {"location": "F4", "name": "None", "volume": None, "lipid_structure": {"amines": None, "isocyanide": None, "lipid_carboxylic_acid": None, "lipid_aldehyde": None}},
    {"location": "G4", "name": "None", "volume": None, "lipid_structure": {"amines": None, "isocyanide": None, "lipid_carboxylic_acid": None, "lipid_aldehyde": None}},
    {"location": "H4", "name": "None", "volume": None, "lipid_structure": {"amines": None, "isocyanide": None, "lipid_carboxylic_acid": None, "lipid_aldehyde": None}},
    {"location": "A5", "name": "A5", "volume": 2000.0, "lipid_structure": {"amines": "A5", "isocyanide": None, "lipid_carboxylic_acid": None, "lipid_aldehyde": None}},
    {"location": "B5", "name": "None", "volume": None, "lipid_structure": {"amines": None, "isocyanide": None, "lipid_carboxylic_acid": None, "lipid_aldehyde": None}},
    {"location": "C5", "name": "None", "volume": None, "lipid_structure": {"amines": None, "isocyanide": None, "lipid_carboxylic_acid": None, "lipid_aldehyde": None}},
    {"location": "D5", "name": "None", "volume": None, "lipid_structure": {"amines": None, "isocyanide": None, "lipid_carboxylic_acid": None, "lipid_aldehyde": None}},
    {"location": "E5", "name": "C9", "volume": 920.0, "lipid_structure": {"amines": None, "isocyanide": None, "lipid_carboxylic_acid": None, "lipid_aldehyde": "C9"}},
    {"location": "F5", "name": "None", "volume": None, "lipid_structure": {"amines": None, "isocyanide": None, "lipid_carboxylic_acid": None, "lipid_aldehyde": None}},
    {"location": "G5", "name": "None", "volume": None, "lipid_structure": {"amines": None, "isocyanide": None, "lipid_carboxylic_acid": None, "lipid_aldehyde": None}},
    {"location": "H5", "name": "None", "volume": None, "lipid_structure": {"amines": None, "isocyanide": None, "lipid_carboxylic_acid": None, "lipid_aldehyde": None}},
    {"location": "A6", "name": "None", "volume": None, "lipid_structure": {"amines": None, "isocyanide": None, "lipid_carboxylic_acid": None, "lipid_aldehyde": None}},
    {"location": "B6", "name": "None", "volume": None, "lipid_structure": {"amines": None, "isocyanide": None, "lipid_carboxylic_acid": None, "lipid_aldehyde": None}},
    {"location": "C6", "name": "None", "volume": None, "lipid_structure": {"amines": None, "isocyanide": None, "lipid_carboxylic_acid": None, "lipid_aldehyde": None}},
    {"location": "D6", "name": "None", "volume": None, "lipid_structure": {"amines": None, "isocyanide": None, "lipid_carboxylic_acid": None, "lipid_aldehyde": None}},
    {"location": "E6", "name": "C10", "volume": 920.0, "lipid_structure": {"amines": None, "isocyanide": None, "lipid_carboxylic_acid": None, "lipid_aldehyde": "C10"}},
    {"location": "F6", "name": "None", "volume": None, "lipid_structure": {"amines": None, "isocyanide": None, "lipid_carboxylic_acid": None, "lipid_aldehyde": None}},
    {"location": "G6", "name": "None", "volume": None, "lipid_structure": {"amines": None, "isocyanide": None, "lipid_carboxylic_acid": None, "lipid_aldehyde": None}},
    {"location": "H6", "name": "None", "volume": None, "lipid_structure": {"amines": None, "isocyanide": None, "lipid_carboxylic_acid": None, "lipid_aldehyde": None}},
    {"location": "A7", "name": "None", "volume": None, "lipid_structure": {"amines": None, "isocyanide": None, "lipid_carboxylic_acid": None, "lipid_aldehyde": None}},
    {"location": "B7", "name": "None", "volume": None, "lipid_structure": {"amines": None, "isocyanide": None, "lipid_carboxylic_acid": None, "lipid_aldehyde": None}},
    {"location": "C7", "name": "None", "volume": None, "lipid_structure": {"amines": None, "isocyanide": None, "lipid_carboxylic_acid": None, "lipid_aldehyde": None}},
    {"location": "D7", "name": "B11", "volume": 400.0, "lipid_structure": {"amines": None, "isocyanide": "B11", "lipid_carboxylic_acid": None, "lipid_aldehyde": None}},
    {"location": "E7", "name": "None", "volume": None, "lipid_structure": {"amines": None, "isocyanide": None, "lipid_carboxylic_acid": None, "lipid_aldehyde": None}},
    {"location": "F7", "name": "None", "volume": None, "lipid_structure": {"amines": None, "isocyanide": None, "lipid_carboxylic_acid": None, "lipid_aldehyde": None}},
    {"location": "G7", "name": "None", "volume": None, "lipid_structure": {"amines": None, "isocyanide": None, "lipid_carboxylic_acid": None, "lipid_aldehyde": None}},
    {"location": "H7", "name": "None", "volume": None, "lipid_structure": {"amines": None, "isocyanide": None, "lipid_carboxylic_acid": None, "lipid_aldehyde": None}},
    {"location": "A8", "name": "None", "volume": None, "lipid_structure": {"amines": None, "isocyanide": None, "lipid_carboxylic_acid": None, "lipid_aldehyde": None}},
    {"location": "B8", "name": "None", "volume": None, "lipid_structure": {"amines": None, "isocyanide": None, "lipid_carboxylic_acid": None, "lipid_aldehyde": None}},
    {"location": "C8", "name": "None", "volume": None, "lipid_structure": {"amines": None, "isocyanide": None, "lipid_carboxylic_acid": None, "lipid_aldehyde": None}},
    {"location": "D8", "name": "B12", "volume": 880.0, "lipid_structure": {"amines": None, "isocyanide": "B12", "lipid_carboxylic_acid": None, "lipid_aldehyde": None}},
    {"location": "E8", "name": "None", "volume": None, "lipid_structure": {"amines": None, "isocyanide": None, "lipid_carboxylic_acid": None, "lipid_aldehyde": None}},
    {"location": "F8", "name": "None", "volume": None, "lipid_structure": {"amines": None, "isocyanide": None, "lipid_carboxylic_acid": None, "lipid_aldehyde": None}},
    {"location": "G8", "name": "None", "volume": None, "lipid_structure": {"amines": None, "isocyanide": None, "lipid_carboxylic_acid": None, "lipid_aldehyde": None}},
    {"location": "H8", "name": "None", "volume": None, "lipid_structure": {"amines": None, "isocyanide": None, "lipid_carboxylic_acid": None, "lipid_aldehyde": None}},
    {"location": "A9", "name": "None", "volume": None, "lipid_structure": {"amines": None, "isocyanide": None, "lipid_carboxylic_acid": None, "lipid_aldehyde": None}},
    {"location": "B9", "name": "None", "volume": None, "lipid_structure": {"amines": None, "isocyanide": None, "lipid_carboxylic_acid": None, "lipid_aldehyde": None}},
    {"location": "C9", "name": "None", "volume": None, "lipid_structure": {"amines": None, "isocyanide": None, "lipid_carboxylic_acid": None, "lipid_aldehyde": None}},
    {"location": "D9", "name": "None", "volume": None, "lipid_structure": {"amines": None, "isocyanide": None, "lipid_carboxylic_acid": None, "lipid_aldehyde": None}},
    {"location": "E9", "name": "None", "volume": None, "lipid_structure": {"amines": None, "isocyanide": None, "lipid_carboxylic_acid": None, "lipid_aldehyde": None}},
    {"location": "F9", "name": "None", "volume": None, "lipid_structure": {"amines": None, "isocyanide": None, "lipid_carboxylic_acid": None, "lipid_aldehyde": None}},
    {"location": "G9", "name": "None", "volume": None, "lipid_structure": {"amines": None, "isocyanide": None, "lipid_carboxylic_acid": None, "lipid_aldehyde": None}},
    {"location": "H9", "name": "None", "volume": None, "lipid_structure": {"amines": None, "isocyanide": None, "lipid_carboxylic_acid": None, "lipid_aldehyde": None}},
    {"location": "A10", "name": "None", "volume": None, "lipid_structure": {"amines": None, "isocyanide": None, "lipid_carboxylic_acid": None, "lipid_aldehyde": None}},
    {"location": "B10", "name": "None", "volume": None, "lipid_structure": {"amines": None, "isocyanide": None, "lipid_carboxylic_acid": None, "lipid_aldehyde": None}},
    {"location": "C10", "name": "None", "volume": None, "lipid_structure": {"amines": None, "isocyanide": None, "lipid_carboxylic_acid": None, "lipid_aldehyde": None}},
    {"location": "D10", "name": "None", "volume": None, "lipid_structure": {"amines": None, "isocyanide": None, "lipid_carboxylic_acid": None, "lipid_aldehyde": None}},
    {"location": "E10", "name": "None", "volume": None, "lipid_structure": {"amines": None, "isocyanide": None, "lipid_carboxylic_acid": None, "lipid_aldehyde": None}},
    {"location": "F10", "name": "None", "volume": None, "lipid_structure": {"amines": None, "isocyanide": None, "lipid_carboxylic_acid": None, "lipid_aldehyde": None}},
    {"location": "G10", "name": "None", "volume": None, "lipid_structure": {"amines": None, "isocyanide": None, "lipid_carboxylic_acid": None, "lipid_aldehyde": None}},
    {"location": "H10", "name": "None", "volume": None, "lipid_structure": {"amines": None, "isocyanide": None, "lipid_carboxylic_acid": None, "lipid_aldehyde": None}},
    {"location": "A11", "name": "None", "volume": None, "lipid_structure": {"amines": None, "isocyanide": None, "lipid_carboxylic_acid": None, "lipid_aldehyde": None}},
    {"location": "B11", "name": "None", "volume": None, "lipid_structure": {"amines": None, "isocyanide": None, "lipid_carboxylic_acid": None, "lipid_aldehyde": None}},
    {"location": "C11", "name": "None", "volume": None, "lipid_structure": {"amines": None, "isocyanide": None, "lipid_carboxylic_acid": None, "lipid_aldehyde": None}},
    {"location": "D11", "name": "None", "volume": None, "lipid_structure": {"amines": None, "isocyanide": None, "lipid_carboxylic_acid": None, "lipid_aldehyde": None}},
    {"location": "E11", "name": "C15", "volume": 920.0, "lipid_structure": {"amines": None, "isocyanide": None, "lipid_carboxylic_acid": None, "lipid_aldehyde": "C15"}},
    {"location": "F11", "name": "None", "volume": None, "lipid_structure": {"amines": None, "isocyanide": None, "lipid_carboxylic_acid": None, "lipid_aldehyde": None}},
    {"location": "G11", "name": "None", "volume": None, "lipid_structure": {"amines": None, "isocyanide": None, "lipid_carboxylic_acid": None, "lipid_aldehyde": None}},
    {"location": "H11", "name": "None", "volume": None, "lipid_structure": {"amines": None, "isocyanide": None, "lipid_carboxylic_acid": None, "lipid_aldehyde": None}},
    {"location": "A12", "name": "None", "volume": None, "lipid_structure": {"amines": None, "isocyanide": None, "lipid_carboxylic_acid": None, "lipid_aldehyde": None}},
    {"location": "B12", "name": "None", "volume": None, "lipid_structure": {"amines": None, "isocyanide": None, "lipid_carboxylic_acid": None, "lipid_aldehyde": None}},
    {"location": "C12", "name": "None", "volume": None, "lipid_structure": {"amines": None, "isocyanide": None, "lipid_carboxylic_acid": None, "lipid_aldehyde": None}},
    {"location": "D12", "name": "None", "volume": None, "lipid_structure": {"amines": None, "isocyanide": None, "lipid_carboxylic_acid": None, "lipid_aldehyde": None}},
    {"location": "E12", "name": "C16", "volume": 920.0, "lipid_structure": {"amines": None, "isocyanide": None, "lipid_carboxylic_acid": None, "lipid_aldehyde": "C16"}},
    {"location": "F12", "name": "D12", "volume": 1040.0, "lipid_structure": {"amines": None, "isocyanide": None, "lipid_carboxylic_acid": "D12", "lipid_aldehyde": None}},
    {"location": "G12", "name": "None", "volume": None, "lipid_structure": {"amines": None, "isocyanide": None, "lipid_carboxylic_acid": None, "lipid_aldehyde": None}},
    {"location": "H12", "name": "None", "volume": None, "lipid_structure": {"amines": None, "isocyanide": None, "lipid_carboxylic_acid": None, "lipid_aldehyde": None}}
]

# Ensure all wells are represented
rows = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
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
            "lipid_aldehyde": None
        }
    }
    for well in all_wells
}

# Update filled_data with actual data
for entry in data:
    filled_data[entry["location"]] = entry

# Convert to DataFrame
df = pd.DataFrame(list(filled_data.values()))

# Handle missing volumes by filling them with 0 for visualization
df['volume'] = df['volume'].fillna(0)

# Use session state to persist data
if "df" not in st.session_state:
    st.session_state.df = df.copy()

# Define a colormap using the correct method
min_volume = st.session_state.df['volume'].min()
max_volume = st.session_state.df['volume'].max()
cmap = plt.get_cmap('coolwarm')
norm = mcolors.Normalize(vmin=min_volume, vmax=max_volume)

# Sidebar for updating volumes
st.sidebar.title("Update Stock Solutions")
location = st.sidebar.selectbox("Select Location", options=st.session_state.df['location'].unique())
volume_change = st.sidebar.number_input("Volume Change", value=0.0)

if st.sidebar.button("Update Volume"):
    # Find the row to update
    current_volume = st.session_state.df.loc[st.session_state.df['location'] == location, 'volume'].values[0]
    st.session_state.df.loc[st.session_state.df['location'] == location, 'volume'] = current_volume + volume_change
    st.sidebar.success(f"Updated volume at {location}")
    
    # Recalculate color normalization with the updated data
    min_volume = st.session_state.df['volume'].min()
    max_volume = st.session_state.df['volume'].max()
    norm = mcolors.Normalize(vmin=min_volume, vmax=max_volume)

# Main page display
st.title("96-Well Plate Stock Solution Management")

# Redraw the plot to reflect changes
fig, ax = plt.subplots(figsize=(12, 8))
for idx, row in st.session_state.df.iterrows():
    row_idx = rows.index(row['location'][0])
    col_idx = int(row['location'][1:]) - 1

    # Determine color based on updated volume using colormap
    color = cmap(norm(row['volume']))

    # Plot circle (dot) for each well
    circle = Circle((col_idx, row_idx), 0.3, color=color, alpha=0.6)
    ax.add_patch(circle)

    # Annotate the circle with the name and updated volume
    ax.text(col_idx, row_idx, f"{row['name']}\nVol: {row['volume']:.1f}", ha='center', va='center', fontsize=8, color='black')

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
ax.set_aspect('equal')

# Add grid lines
ax.grid(False)

# Show plot in Streamlit
st.pyplot(fig)
st.dataframe(st.session_state.df)