import streamlit as st
import requests
import plotly.graph_objs as go

BASE_URLS = {
    "Feeder-server-0": "http://raspberrypi2feeder.local:8000",
    "Feeder-server-1": "http://raspberrypi2feeder.local:9001",
    "Feeder-server-2": "http://raspberrypi2feeder.local:9002",
    "Feeder-server-3": "http://raspberrypi2feeder.local:9003",
}

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

def generate_plotly_chart(server_name):
    x_data = [1, 2, 3, 4, 5]
    y_data = [10, 20, 15, 25, 30]
    
    fig = go.Figure(data=go.Scatter(x=x_data, y=y_data, mode='lines+markers'))
    fig.update_layout(title=f'Chart for {server_name}', xaxis_title='X Axis', yaxis_title='Y Axis')
    
    return fig

# Define the updated CSS with !important to ensure styles are applied
updated_css = """
<style>
    .move-down {
        background-color: #f44336 !important; /* Red */
        color: white !important;
        padding: 10px 24px !important;
        border: none !important;
        border-radius: 5px !important;
        cursor: pointer !important;
        margin: 5px 0 !important;
    }
    .move-down:hover {
        background-color: #d32f2f !important;
    }
    .move-up {
        background-color: #4CAF50 !important; /* Green */
        color: white !important;
        padding: 10px 24px !important;
        border: none !important;
        border-radius: 5px !important;
        cursor: pointer !important;
        margin: 5px 0 !important;
    }
    .move-up:hover {
        background-color: #388E3C !important;
    }
</style>
"""

# Function to update the CSS in Streamlit
def update_css_in_streamlit():
    import streamlit as st
    st.markdown(updated_css, unsafe_allow_html=True)

# Call the function to update the CSS in Streamlit
update_css_in_streamlit()

def main():
    st.title("Move Cargo")
    cargo_num = st.number_input("Enter Cargo Number:", min_value=0, value=1, step=1)
    

    for server_name in BASE_URLS.keys():
        col1, col2 = st.columns(2)  # Create two columns for each server

        with col1:
            st.header(server_name)
            # Move Down button with color and function
            move_down_button = st.markdown(
                f'<button class="move-down" onclick="window.location.href=\'#move_down_{server_name}\'">Move Down Cargo on {server_name}</button>',
                unsafe_allow_html=True,
            )
            if st.button(f"Move Down Cargo on {server_name}", key=f"move_down_{server_name}"):
                result = move_cargo(server_name, cargo_num, "down")
                if result:
                    st.write(f"Response from {server_name} for Moving Down Cargo:")
                    st.json(result)

            st.header(server_name)
            # Move Up button with color and function
            move_up_button = st.markdown(
                f'<button class="move-up" onclick="window.location.href=\'#move_up_{server_name}\'">Move Up Cargo on {server_name}</button>',
                unsafe_allow_html=True,
            )
            if st.button(f"Move Up Cargo on {server_name}", key=f"move_up_{server_name}"):
                result = move_cargo(server_name, cargo_num, "up")
                if result:
                    st.write(f"Response from {server_name} for Moving Up Cargo:")
                    st.json(result)


        with col2:
            fig = generate_plotly_chart(server_name)
            st.plotly_chart(fig)

if __name__ == "__main__":
    main()
