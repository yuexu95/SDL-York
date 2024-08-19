import streamlit as st
import plotly.graph_objects as go
import numpy as np
import requests


base_url = "http://192.168.1.11:8700"


def get_entries():
    # Placeholder for the method that fetches available entry IDs
    # Replace with the actual implementation
    request_url = base_url + "/entries"
    return [entry["id"] for entry in requests.get(request_url).json()]


st.title("96-well Plate Readings Heatmap")

# Get available entry IDs
entry_ids = get_entries()

with st.expander("Select Entry ID"):
    entry_id = st.selectbox("Choose an entry ID:", entry_ids)

if entry_id:
    request_url = base_url + f"/entry/{entry_id}/readings"
    response = requests.get(request_url)
    if response.status_code == 200:
        data = response.json()

        # Extracting readings and hover text
        for key in data.keys():
            wells = sorted(data[key].keys())
            rows = sorted(list(set(well[0] for well in wells)), reverse=True)
            columns = sorted(list(set(int(well[1:]) for well in wells)))

            heatmap_data = np.zeros((len(rows), len(columns)))
            hovertext = np.empty((len(rows), len(columns)), dtype=object)
            ctrl = np.log2(
                (data[key]["A1"]["reading"] + data[key]["B1"]["reading"]) / 2
            )

            for well in wells:
                row_idx = rows.index(well[0])
                col_idx = columns.index(int(well[1:]))
                heatmap_data[row_idx, col_idx] = data[key][well]["reading"]

                components = data["0"][well]["components"]
                hovertext[row_idx, col_idx] = (
                    f"Well: {well}<br>Reading: {data[key][well]['reading']}"
                    f"<br>log(reading): {round(np.log2(heatmap_data[row_idx, col_idx]) - ctrl, 2)}"
                    f"<br>Amines: {components['amines']}<br>Isocyanide: {components['isocyanide']}"
                    f"<br>Lipid Aldehyde: {components['lipid_aldehyde']}"
                    f"<br>Lipid Carboxylic Acid: {components['lipid_carboxylic_acid']}"
                )

            # blank
            # log transform the data
            heatmap_data = np.log2(heatmap_data) - ctrl
            fig = go.Figure(
                data=go.Heatmap(
                    z=heatmap_data,
                    x=[str(col) for col in columns],
                    y=rows,
                    text=hovertext,
                    hoverinfo="text",
                    colorscale="Viridis",
                )
            )

            fig.update_layout(
                title=f"96-well Plate Readings Heatmap; rep {key}",
                xaxis_title="Column",
                yaxis_title="Row",
            )

            st.plotly_chart(fig)
    else:
        st.error("Failed to fetch data. Please check the entry ID.")
