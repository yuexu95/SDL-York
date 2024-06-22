import streamlit as st
import requests
import plotly.graph_objs as go
from plotly.subplots import make_subplots
from streamlit_extras.colored_header import colored_header
import datetime
import pandas as pd

# Base URLs for different feeder servers
BASE_URLS = {
    "Feeder-server-0": "http://raspberrypi2feeder.local:8000",
    "Feeder-server-1": "http://raspberrypi2feeder.local:9001",
    "Feeder-server-2": "http://raspberrypi2feeder.local:9002",
    "Feeder-server-3": "http://raspberrypi2feeder.local:9003",
}

# Initialize plate numbers in session state
if 'plates_number' not in st.session_state:
    st.session_state['plates_number'] = {
        "Feeder-server-0": 6,
        "Feeder-server-1": 2,
        "Feeder-server-2": 2,
        "Feeder-server-3": 2,
    }

# Define colors for each server
server_colors = {
    "Feeder-server-0": "red",
    "Feeder-server-1": "blue",
    "Feeder-server-2": "green",
    "Feeder-server-3": "orange",
}

# Function to move cargo in a specified direction
def move_cargo(server_name, cargo_num, direction):
    url = f"{BASE_URLS[server_name]}/move_{direction}_cargo/{cargo_num}"
    headers = {'Accept': 'application/json'}
    try:
        with st.spinner(f"Moving cargo {direction} on {server_name}, please wait..."):
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Failed to fetch data from FastAPI on {server_name}: {e}")
        return None

# Function to generate a Plotly chart as a column chart
def generate_plotly_chart():
    server_names = list(BASE_URLS.keys())
    plates_number = [st.session_state['plates_number'][server] for server in server_names]
    colors = [server_colors[server] for server in server_names]

    fig = go.Figure(data=go.Bar(
        x=server_names, 
        y=plates_number, 
        marker_color=colors,
        text=plates_number,
        textposition='auto',
        width=[0.3] * len(server_names)  # Adjust the width of the bars here
    ))
    fig.update_layout(
        title='Chart for Server and Plates Number', 
        xaxis_title='Server Names', 
        yaxis_title='Plates Number',
        template='plotly_dark',
        xaxis=dict(tickmode='array', tickvals=server_names),
        yaxis=dict(range=[0, 13]),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        transition={'duration': 500},
    )
    return fig

# Main function for the Streamlit app
def example() -> None:
    st.set_page_config(
        page_title="SDL Dashboard",
        page_icon="🦾",
        layout="wide",
        initial_sidebar_state="expanded",
    )

    # Display the current date and time
    current_datetime = datetime.datetime.now()

    # Use colored_header to display a header with the current system time
    colored_header(
        label="SDL-LNP",
        description=f"The current system time: {current_datetime.strftime('%H:%M:%S')}",
        color_name="green-100",
    )

if __name__ == "__main__":
    example()

def main():
    st.title("Move Cargo Management System")
    st.sidebar.title("Configuration")
    cargo_num = st.sidebar.number_input("Enter Cargo Number:", min_value=0, value=1, step=1)

    col1, col2 = st.columns((1, 3), gap="large")

    with col1:
        for server_name in BASE_URLS.keys():
            server_color = server_colors[server_name]
            st.markdown(f'<div class="server-header" style="color: {server_color}; font-weight: bold;">{server_name}</div>', unsafe_allow_html=True)
            
            button_col1, button_col2 = st.columns(2)
            
            with button_col1:
                move_down_disabled = st.session_state['plates_number'][server_name] >= 12
                if st.button("Move Down Cargo", key=f"move_down_{server_name}", disabled=move_down_disabled):
                    if not move_down_disabled:
                        result = move_cargo(server_name, cargo_num, "down")
                        if result:
                            st.session_state['plates_number'][server_name] += 1
                            st.write(f"Response from {server_name} for Moving Down Cargo:")
                            st.json(result)
                            fig = generate_plotly_chart()
                            st.plotly_chart(fig, use_container_width=True)
                    else:
                        st.warning(f"Maximum number of plates (12) reached for {server_name}!")

            with button_col2:
                move_up_disabled = st.session_state['plates_number'][server_name] <= 0
                if st.button("Move Up Cargo", key=f"move_up_{server_name}", disabled=move_up_disabled):
                    if not move_up_disabled:
                        result = move_cargo(server_name, cargo_num, "up")
                        if result:
                            st.session_state['plates_number'][server_name] -= 1
                            st.write(f"Response from {server_name} for Moving Up Cargo:")
                            st.json(result)
                            fig = generate_plotly_chart()
                            st.plotly_chart(fig, use_container_width=True)
                    else:
                        st.warning(f"Minimum number of plates (0) reached for {server_name}!")
    
    with col2:
        fig = generate_plotly_chart()
        st.plotly_chart(fig, use_container_width=True)

if __name__ == "__main__":
    main()