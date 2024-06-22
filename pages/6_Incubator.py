import streamlit as st
import requests
import time  # Importing time for demonstration purposes

# Define the FastAPI service URL
API_URL = 'http://192.168.1.30:9007'

# Flag to track if Open Incubator API call is in progress
open_incubator_in_progress = False

def call_api(endpoint):
    url = f"{API_URL}/{endpoint}"
    response = requests.get(url)
    return response.json()

def main():
    st.title('Incubator Control Panel')

    col1, col2, col3 = st.columns(3)

    with col1:
        global open_incubator_in_progress
        if not open_incubator_in_progress and st.button('Open Incubator'):
            open_incubator_in_progress = True
            direction = 'Opening'  # Example direction
            server_name = 'Raspberry Pi'  # Example server name
            with st.spinner(f"{direction} on {server_name}, please wait..."):
                result = call_api('open_incubator')
                time.sleep(2)  # Simulating a delay for demonstration
                st.write('Open Incubator:', result)
            open_incubator_in_progress = False

    with col2:
        if st.button('Close Incubator'):
            direction = 'Closing'  # Example direction
            server_name = 'Raspberry Pi'  # Example server name
            with st.spinner(f"{direction} on {server_name}, please wait..."):
                result = call_api('close_incubator')
                time.sleep(2)  # Simulating a delay for demonstration
                st.write('Close Incubator:', result)

    with col3:
        if st.button('Shutdown'):
            direction = 'Shutting down'  # Example direction
            server_name = 'Raspberry Pi'  # Example server name
            with st.spinner(f"{direction} on {server_name}, please wait..."):
                result = call_api('shutdown')
                time.sleep(2)  # Simulating a delay for demonstration
                st.write('Shutdown:', result)

if __name__ == '__main__':
    main()