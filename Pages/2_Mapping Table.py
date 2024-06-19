import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
from streamlit_extras.colored_header import colored_header

# Main function for the Streamlit app
def example() -> None:
    st.set_page_config(
        page_title="SDL mapping table",
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

# 96-well plate layout: 8 rows and 12 columns
rows = 8
columns = 12

# Create an empty list to store input data for each well
plate_data = []

# Generate the plate layout
for row in range(rows):
    cols = st.columns(columns)
    row_data = []
    for col in range(columns):
        well_label = f"{chr(65 + row)}{col + 1}"
        data = cols[col].text_input(well_label, "")
        row_data.append(data)
    plate_data.append(row_data)

# Convert the collected data into a DataFrame
well_labels = [[f"{chr(65 + r)}{c + 1}" for c in range(columns)] for r in range(rows)]
data_df = pd.DataFrame(plate_data, index=[f"Row {chr(65 + r)}" for r in range(rows)], columns=[f"Column {c + 1}" for c in range(columns)])

# Display the DataFrame as a table
st.write("96-well plate data as a table:")
st.dataframe(data_df)