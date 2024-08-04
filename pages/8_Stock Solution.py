import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

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
# Convert to DataFrame
df = pd.DataFrame(data)
df.fillna('None', inplace=True)  # Handle missing data by filling 'None'

# Sidebar for updating volumes
with st.sidebar:
    st.title("Update Stock Solutions")
    location = st.selectbox("Select Location", options=df['location'].unique())
    volume = st.number_input("Volume", value=0)

    if st.button("Update Volume"):
        if df.loc[df['location'] == location, 'volume'].dtype == 'O':  # Check if the current volume is a string (None)
            df.loc[df['location'] == location, 'volume'] = 0  # Initialize with zero if previously 'None'
        df.loc[df['location'] == location, 'volume'] += volume
        st.success(f"Updated volume at {location}")

# Main page display
st.title("Stock Solution Management")
st.dataframe(df)

# Plotting the volumes
fig, ax = plt.subplots()
numeric_filter = df['volume'].apply(lambda x: isinstance(x, (int, float)))
negative_volumes = df[numeric_filter]['volume'] < 0
ax.bar(df[numeric_filter]['location'][negative_volumes], df[numeric_filter]['volume'][negative_volumes], color='red')
ax.bar(df[numeric_filter]['location'][~negative_volumes], df[numeric_filter]['volume'][~negative_volumes], color='blue')
ax.set_xlabel("Location")
ax.set_ylabel("Volume")
ax.set_title("Solution Volumes by Location")
st.pyplot(fig)