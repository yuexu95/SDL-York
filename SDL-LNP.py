import streamlit as st
import pandas as pd
import altair as alt
import plotly.graph_objects as go
from streamlit_extras.colored_header import colored_header
from datetime import datetime, timedelta


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
