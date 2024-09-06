from typing import Dict
import pandas as pd
import streamlit as st
import plotly.graph_objects as go
import numpy as np
import requests


base_url = "http://192.168.1.11:8700"


def get_entries():
    # Placeholder for the method that fetches available entry IDs
    # Replace with the actual implementation
    request_url = base_url + "/entries"
    return requests.get(request_url).json()


def get_entry_readings(entry_id):
    request_url = base_url + f"/entry/{entry_id}/readings"
    response = requests.get(request_url)
    if response.status_code == 200:
        return response.json()
    else:
        st.error("Failed to fetch data. Please check the entry ID.")


def log_and_norm_reading(readings) -> Dict[str, Dict]:
    """loop and call the _log_and_norm_reading function"""
    return {key: _log_and_norm_reading(value) for key, value in readings.items()}


def _log_and_norm_reading(reading, clip_negative=True):
    """
    Normalize the readings by calling the log and norm function. Essentially, it logs the readings and normalizes them by the control well readings. The first two wells that have none components are the control wells. The others of none components are the benchmark lipids of MC3. The rest are the experimental wells.

    Args:
        readings (dict): A dictionary containing the readings for each well.
        example:
        {
            "A1": {"reading": 0.0, "components": {...}},
            "A2": {"reading": 0.0, "components": {...}},
            ...
        }
        clip_negative (bool): Whether to clip the negative values to zero.

    Returns:
        dict: A dictionary containing the normalized readings for each well.
        example:
        {
            "A1": {"reading": 0.0, "components": {...}, "type": "control"},
            "A2": {"reading": 0.0, "components": {...}, "type": "mc3"},
            ...
        }
    """
    # log transform the data
    log_reading = {}
    for key, value in reading.items():
        log_reading[key] = {
            "reading": np.log2(value["reading"]),
            "components": value["components"],
        }

    # find all wells that have none components
    empty_and_positive_control_wells = []
    for key, value in reading.items():
        if value["components"]["amines"] is None:
            empty_and_positive_control_wells.append(key)
    empty_wells = empty_and_positive_control_wells[:2]
    positive_control_wells = empty_and_positive_control_wells[2:]
    assert empty_wells[0] == "A1"
    assert empty_wells[1] == "B1"

    # assign the type of the well
    for key in log_reading.keys():
        if key in empty_wells:
            log_reading[key]["type"] = "control"
        elif key in positive_control_wells:
            log_reading[key]["type"] = "mc3"
        else:
            log_reading[key]["type"] = "experimental"

    # normalize the data
    ctrl = np.mean([log_reading[key]["reading"] for key in empty_wells])
    for key in log_reading.keys():
        log_reading[key]["reading"] = log_reading[key]["reading"] - ctrl
        if clip_negative:
            log_reading[key]["reading"] = max(log_reading[key]["reading"], 0)

    return log_reading


def qc_entry_readings(nomalized_readings, threshold=3):
    """
    Quality control the readings for each well in the 96-well plate. Each entry can have readings of maximum four replicates. The first two are two repeated readings of one well, and the other two are two repeated readings of another well. Sometimes there are only two replicates, then the third and fourth readings are missing.

    1. check whther the readings are trustworthy: if the difference between the two readings is less than `threshold`, then the readings are trustworthy.
    2. If the readings are trustworthy, then calculate the average of the two readings as the final reading for that well.
    3. Across wells for the same lipid structure, using the larger value as the final value.

    Args:
        readings (dict): A dictionary containing the readings for each well.
        example:
        {
            "0": {
                "A1": {"reading": 0.0, "components": {...}, "type": "control"},
                "A2": {"reading": 0.0, "components": {...}, "type": "mc3"},
                ...
            },
            "1": {
                "A1": {"reading": 0.0, "components": {...}, "type": "control"},
                "A2": {"reading": 0.0, "components": {...}, "type": "mc3"},
                ...
            },
            ...
        }
        threshold (float): The threshold to determine whether the readings are trustworthy. Note this is in the log scale.

    Returns:
        dict: A dictionary containing the normalized readings for each well.
        example:
        {
            "A1": {"reading": 0.0, "components": {...}, "type": "control"},
            "A2": {"reading": 0.0, "components": {...}, "type": "mc3"},
            ...
        }
    """
    qc_data = {}
    for key, readings in nomalized_readings.items():
        for well, reading in readings.items():
            if well not in qc_data:
                qc_data[well] = {
                    "reading": [],
                    "components": reading["components"],
                    "type": reading["type"],
                }
            qc_data[well]["reading"].append(reading["reading"])

    def _process_data(data0, data1, threshold, message_prefix=""):
        if abs(data0 - data1) < threshold:
            return np.mean([data0, data1])
        elif max(data0, data1) > 7:
            return max(data0, data1)
        else:
            st.write(
                f"{message_prefix} The difference between the two readings ({data0:.2f},{data1:.2f}) is larger than {threshold}."
            )
            return np.nan

    for well, data in qc_data.items():
        if len(data["reading"]) == 1:
            qc_data[well]["reading"] = data["reading"][0]
        elif len(data["reading"]) == 2:
            data0, data1 = data["reading"]
            qc_data[well]["reading"] = _process_data(
                data0, data1, threshold, f"Replicates of {well}:"
            )
        elif len(data["reading"]) == 4:
            data0, data1, data2, data3 = data["reading"]
            reading1 = _process_data(
                data0, data1, threshold, f"Replicates #0,1 of well {well}:"
            )
            reading2 = _process_data(
                data2, data3, threshold, f"Replicates #2,3 of well {well}:"
            )

            qc_data[well]["reading"] = max(reading1, reading2)
        else:
            qc_data[well]["reading"] = np.nan

    return qc_data


st.title("96-well Plate Readings Heatmap")

# Get available entry IDs
entries = get_entries()

# TODO: move the analysis to separate script and use the DAO instead of info_api
# normalize and integrate all readings
st.subheader("Processing all readings:")
with st.container(height=300):
    integrated_data = {}
    for entry in entries:
        entry_id = entry["id"]
        st.write(f"Processing entry {entry_id}...")

        data = get_entry_readings(entry_id)
        normalized_data = log_and_norm_reading(data)
        qc_data = qc_entry_readings(normalized_data)

        integrated_data[entry_id] = qc_data

# st.write(integrated_data)

# make the integrated data to dataframe, including the experimental type readings
# each row contains the recordings for a lipid structure of AxBxCxDx
# each row should be |name|max|mean|std|reading1|reading2|reading3|readingN|
# the readings are the readings of the wells of the same lipid structure
df_data = {}
for entry_id, data in integrated_data.items():
    for well, reading in data.items():
        if reading["type"] == "experimental":
            lipid_structure = "".join(
                [
                    reading["components"][key]
                    for key in sorted(reading["components"].keys())
                ]
            )
            if lipid_structure not in df_data:
                df_data[lipid_structure] = {}
                df_data[lipid_structure]["amine"] = reading["components"]["amines"]
                df_data[lipid_structure]["isocyanide"] = reading["components"][
                    "isocyanide"
                ]
                df_data[lipid_structure]["aldehyde"] = reading["components"][
                    "lipid_aldehyde"
                ]
                df_data[lipid_structure]["carboxylic_acid"] = reading["components"][
                    "lipid_carboxylic_acid"
                ]
            df_data[lipid_structure][f"reading.{entry_id}"] = reading["reading"]
# make the dataframe
df = pd.DataFrame(df_data).T
# add the mean, std, and max columns
df.insert(4, "max", df.filter(like="reading").max(axis=1, skipna=True))
df.insert(5, "mean", df.filter(like="reading").mean(axis=1, skipna=True))
df.insert(6, "std", df.filter(like="reading").std(axis=1, skipna=True))

# full screen width
st.subheader("Integrated readings:")
st.write(df, use_container_width=True)

# VISUALIZE one entry
# with st.expander("Select an entry to visualize"):
entry = st.selectbox("Select an entry ID:", entries)
entry_id = entry["id"]
entry_date = entry["last_updated"]

if entry_id:
    st.markdown(f"## {entry_date}")

    data = get_entry_readings(entry_id)
    normalized_data = log_and_norm_reading(data)

    # Extracting readings and hover text
    for key in data.keys():
        wells = sorted(data[key].keys())
        rows = sorted(list(set(well[0] for well in wells)), reverse=True)
        columns = sorted(list(set(int(well[1:]) for well in wells)))

        heatmap_data = np.zeros((len(rows), len(columns)))
        hovertext = np.empty((len(rows), len(columns)), dtype=object)

        for well in wells:
            row_idx = rows.index(well[0])
            col_idx = columns.index(int(well[1:]))
            heatmap_data[row_idx, col_idx] = normalized_data[key][well]["reading"]

            components = data["0"][well]["components"]
            hovertext[row_idx, col_idx] = (
                f"Well: {well}<br>log(reading): {heatmap_data[row_idx, col_idx]:.2f}"
                f"<br>Reading: {data[key][well]['reading']}"
                + (
                    f"<br>Amines: {components['amines']}<br>Isocyanide: {components['isocyanide']}"
                    f"<br>Aldehyde: {components['lipid_aldehyde']}"
                    f"<br>Carboxylic Acid: {components['lipid_carboxylic_acid']}"
                    if normalized_data[key][well]["type"] == "experimental"
                    else f"<br>Type: {normalized_data[key][well]['type']}"
                )
            )

        # blank
        # log transform the data
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
