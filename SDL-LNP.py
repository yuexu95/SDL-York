import streamlit as st
import pandas as pd
import altair as alt
import plotly.graph_objects as go
from streamlit_extras.colored_header import colored_header
from datetime import datetime, timedelta


def make_progress():
    # Define the progress of the experiment (e.g., 23%)
    progress = 23

    # Create the figure
    fig = go.Figure(
        go.Indicator(
            mode="gauge+number",
            value=progress,
            domain={"x": [0, 1], "y": [0, 1]},
            title={"text": "Progress"},
            gauge={
                "axis": {
                    "range": [None, 100],
                    "tickwidth": 1,
                    "tickcolor": "darkgreen",
                },
                "bar": {"color": "darkgreen"},
                "bgcolor": "white",
                "borderwidth": 2,
                # 'bordercolor': "gray",
                "steps": [{"range": [0, progress], "color": "lightgreen"}],
                "threshold": {
                    # 'line': {'color': "red", 'width': 4},
                    "thickness": 0.75,
                    "value": progress,
                },
            },
        )
    )

    fig.update_layout(paper_bgcolor="white", font={"color": "black", "family": "Arial"})

    return fig


def make_plate():
    # fmt: off
    data = [
        [0.123, 0.234, 0.345, 0.456, 0.567, 0.678, 0.789, 0.890, 0.901, 1.012, 1.123, 1.234],
        [0.234, 0.345, 0.456, 0.567, 0.678, 0.789, 0.890, 0.901, 1.012, 1.123, 1.234, 1.345],
        [0.345, 0.456, 0.567, 0.678, 0.789, 0.890, 0.901, 1.012, 1.123, 1.234, 1.345, 1.456],
        [0.456, 0.567, 0.678, 0.789, 0.890, 0.901, 1.012, 1.123, 1.234, 1.345, 1.456, 1.567],
        [0.567, 0.678, 0.789, 0.890, 0.901, 1.012, 1.123, 1.234, 1.345, 1.456, 1.567, 1.678],
        [0.678, 0.789, 0.890, 0.901, 1.012, 1.123, 1.234, 1.345, 1.456, 1.567, 1.678, 1.789],
        [0.789, 0.890, 0.901, 1.012, 1.123, 1.234, 1.345, 1.456, 1.567, 1.678, 1.789, 1.890],
        [0.890, 0.901, 1.012, 1.123, 1.234, 1.345, 1.456, 1.567, 1.678, 1.789, 1.890, 2.001]
    ]
    # fmt: on

    text = [
        f'{chr(ord("A") + i )}{j + 1} {chr(ord("A") + i )}{j + 1} {chr(ord("A") + i )}{j + 1}'
        for i in range(8)
        for j in range(12)
    ]

    # Flatten the data and calculate positions
    x_positions = [j for i in range(8) for j in range(1, 13)]
    y_positions = [i for i in range(1, 9) for _ in range(12)]
    z_values = [data[i][j] for i in range(8) for j in range(12)]

    fig = go.Figure()

    # Add scatter plot with rounded markers
    fig.add_trace(
        go.Scatter(
            x=x_positions,
            y=y_positions,
            mode="markers",
            marker=dict(
                size=25,
                color=z_values,
                colorscale="Viridis",
                line=dict(width=2.5, color="DarkSlateGrey"),
                symbol="circle",
            ),
            text=text,
            hoverinfo="text",
        )
    )

    # Update layout to mimic a 96-well plate look
    fig.update_layout(
        title="Experiment-id: ",
        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        plot_bgcolor="white",
    )

    return fig


def make_plate_legacy():
    data = [
        [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 1.1, 1.2],
        [0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 1.1, 1.2, 1.3],
        [0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 1.1, 1.2, 1.3, 1.4],
        [0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 1.1, 1.2, 1.3, 1.4, 1.5],
        [0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 1.1, 1.2, 1.3, 1.4, 1.5, 1.6],
        [0.6, 0.7, 0.8, 0.9, 1.0, 1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7],
        [0.7, 0.8, 0.9, 1.0, 1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7, 1.8],
        [0.8, 0.9, 1.0, 1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7, 1.8, 1.9],
    ]

    text = [
        [
            f'{chr(ord("A") + i )}{j + 1} {chr(ord("A") + i )}{j + 1} {chr(ord("A") + i )}{j + 1}'
            for i in range(8)
        ]
        for j in range(12)
    ]

    # show all columns and rows
    fig = go.Figure(
        data=go.Heatmap(
            z=data,
            x=["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12"],
            y=["A", "B", "C", "D", "E", "F", "G", "H"],
            hoverongaps=False,
            text=text,
            colorscale="Viridis",
            showscale=True,
            hoverinfo="text",
        )
    )

    fig.update_layout(title="Regaent Plate", xaxis_title="Column", yaxis_title="Row")
    return fig


def get_data(file_path: str) -> pd.DataFrame:
    """
    Function to read data from a CSV file into a pandas DataFrame.

    Parameters:
    - file_path (str): Path to the CSV file.

    Returns:
    - pd.DataFrame: DataFrame containing the data from the CSV file.
    """
    return pd.read_csv(file_path)


def get_chart(data: pd.DataFrame) -> alt.Chart:
    """
    Function to create an Altair chart from a pandas DataFrame.

    Parameters:
    - data (pd.DataFrame): Input DataFrame containing the data.

    Returns:
    - alt.Chart: Altair chart object.
    """
    chart = (
        alt.Chart(data)
        .mark_point()
        .encode(
            x="date:T",
            y="value:Q",
            color="symbol:N",  # Nominal (categorical) data
            tooltip=["date:T", "value:Q", "symbol:N"],
        )
        .interactive()
    )

    return chart


def get_annotations_chart(chart: alt.Chart, annotations: list) -> alt.Chart:
    """
    Function to add annotations to an Altair chart.

    Parameters:
    - chart (alt.Chart): Altair chart object to which annotations will be added.
    - annotations (list): List of tuples, each containing (date, annotation_text).

    Returns:
    - alt.Chart: Altair chart object with annotations added.
    """
    for date, text in annotations:
        chart += (
            alt.Chart(pd.DataFrame({"date": [date], "text": [text]}))
            .mark_text(
                align="left",
                baseline="middle",
                dx=7,
                dy=-10,
                fontSize=10,
                color="black",
            )
            .encode(
                x="date:T",
                y=alt.value(50),  # Vertical position of the annotation
                text="text",
            )
        )

    return chart


# Main function for the Streamlit app
def example() -> None:
    st.set_page_config(
        page_title="SDL Dashboard",
        page_icon="🦾",
        layout="wide",
        initial_sidebar_state="expanded",
    )

    # Display the current date and time
    current_datetime = datetime.now()

    # Use colored_header to display a header with the current system time
    colored_header(
        label="SDL-LNP",
        description=f"The current system time: {current_datetime.strftime('%H:%M:%S')}",
        color_name="green-100",
    )


if __name__ == "__main__":
    example()


alt.themes.enable("dark")

col = st.columns((1.8, 4.5), gap="large")

with col[0]:
    st.markdown("#### Progress")
    progress = make_progress()
    st.plotly_chart(progress, use_container_width=True)

with col[1]:
    choices = ["Feeder", "Current Experiment", "Chemical Stock"]
    plate_choice = st.selectbox("Select", choices)

    # Determine which plate to create based on the user's choice
    if plate_choice == "Feeder":
        plate = make_plate_legacy()
    elif plate_choice == "Current Experiment":
        plate = make_plate()
    elif plate_choice == "Chemical Stock":
        plate = make_plate()

    st.plotly_chart(plate, use_container_width=True)
