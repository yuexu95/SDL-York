import streamlit as st
import pandas as pd
import numpy as np
import plost

# Set the title and favicon that appear in the Browser's tab bar.
st.set_page_config(
    page_title='96-Well Plate Tracker',
    page_icon=':test_tube:',  # This is an emoji shortcode. Could be a URL too.
)

initial_data = [
    {"location": "A1", "name": "A1", "volume": 560.0, "lipid_structure": {"amines": "A1", "isocyanide": None, "lipid_carboxylic_acid": None, "lipid_aldehyde": None}},
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

# Ensure all 96 wells are initialized
rows = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
cols = list(range(1, 13))
all_wells = [f"{r}{c}" for r in rows for c in cols]

# Fill missing wells with default values
filled_data = {
    well: {
        "location": well,
        "name": "None",
        "volume": 0.0,
        "lipid_structure": "None"
    }
    for well in all_wells
}

# Update with initial data
for entry in initial_data:
    filled_data[entry["location"]] = entry

# Convert filled data to DataFrame
df = pd.DataFrame(list(filled_data.values()))

# Add row and column indices
df['row'] = df['location'].str.extract('([A-H])', expand=False)
df['column'] = df['location'].str.extract('(\d+)', expand=False).astype(int)

# Map rows to numeric values for plotting
row_mapping = {row: i + 1 for i, row in enumerate(rows)}
df['row_num'] = df['row'].map(row_mapping)

# Identify negative volumes and prepare reminders
negative_wells = df[df['volume'] < 0]
if not negative_wells.empty:
    st.error("Warning: The following wells have negative volumes and should be checked:")
    for index, row in negative_wells.iterrows():
        st.warning(f"Well {row['location']} has a negative volume of {row['volume']}.")

# Handle NaN and negative volumes for visualization
df['volume'] = df['volume'].fillna(0)  # Replace NaNs with 0
df['size'] = df['volume'].apply(lambda x: max(x, 0))  # Ensure size is non-negative

# -----------------------------------------------------------------------------
# Draw the actual page, starting with the inventory table.

st.title(':test_tube: 96-Well Plate Tracker')
st.write("**Welcome to the 96-Well Plate Tracker!**")
st.info('''
    Use the table below to add, remove, and edit wells.
    And don't forget to commit your changes when you're done.
''')

# Display data with editable table
edited_df = st.data_editor(
    df,
    disabled=['location', 'row', 'column'],  # Don't allow editing the 'location', 'row', 'column' columns.
    num_rows='dynamic',  # Allow appending/deleting rows.
    key='well_table'
)

# Check for uncommitted changes
has_uncommitted_changes = any(len(v) for v in st.session_state.well_table.values())

# Update the in-memory data with edited values
if st.button('Commit changes', disabled=not has_uncommitted_changes):
    df.update(edited_df)
    st.success('Changes committed successfully!')

# -----------------------------------------------------------------------------
# 2D Histogram Plot of 96-Well Plate

st.markdown('---')
st.subheader('2D Visualization of Well Volumes Using plost.xy_hist')

# Prepare the data for plost.xy_hist
df['row_label'] = df['row'].map(row_mapping)  # Numeric row mapping for plost
df['column_label'] = df['column']  # Column numbers already numeric

# Create a 2D histogram plot using plost
plost.xy_hist(
    data=df,
    x='column_label',
    y='row_label',
    x_bin=dict(maxbins=12),  # Ensure correct binning for 12 columns
    y_bin=dict(maxbins=8),   # Ensure correct binning for 8 rows
    color='volume',          # Use volume for color intensity
    height=400,
)

st.caption('Each cell represents a well, with color intensity representing the volume.')

# -----------------------------------------------------------------------------
st.subheader('Volume Updates')

# Sidebar for updating volumes
location = st.selectbox("Select Well Location", options=df['location'].unique())
volume_change = st.number_input("Volume Change", value=0.0)

if st.button("Update Volume"):
    # Update the volume in the DataFrame
    df.loc[df['location'] == location, 'volume'] += volume_change
    st.success(f"Volume at {location} updated to {df.loc[df['location'] == location, 'volume'].values[0]:.2f}")

# Display updated data
st.write(df)