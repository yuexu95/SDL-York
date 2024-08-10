import streamlit as st
import requests
import time  # Importing time for demonstration purposes

# Define the FastAPI service URL
API_URL = "http://192.168.1.30:9006"

# Flag to track if Open clamp API call is in progress
clamp_in_progress = False


def call_api(endpoint):
    url = f"{API_URL}/{endpoint}"
    response = requests.get(url)
    return response.json()


def main():
    st.title("Clamp")

    col1, col2, col3 = st.columns(3)

    with col1:
        global clamp_in_progress
        if not clamp_in_progress and st.button("Clamp"):
            clamp_in_progress = True
            direction = "Clamp"  # Example direction
            server_name = "Raspberry Pi"  # Example server name
            with st.spinner(f"{direction} on {server_name}, please wait..."):
                result = call_api("clamp")
                time.sleep(2)  # Simulating a delay for demonstration
                st.write("Clamp:", result)
            clamp_in_progress = False

    with col2:
        if st.button("Release"):
            direction = "Release"  # Example direction
            server_name = "Raspberry Pi"  # Example server name
            with st.spinner(f"{direction} on {server_name}, please wait..."):
                result = call_api("release")
                time.sleep(2)  # Simulating a delay for demonstration
                st.write("Release:", result)

    with col3:
        if st.button("Reset"):
            direction = "Reset"  # Example direction
            server_name = "Raspberry Pi"  # Example server name
            with st.spinner(f"{direction} on {server_name}, please wait..."):
                result = call_api("reset_clamped")
                time.sleep(2)  # Simulating a delay for demonstration
                st.write("Reset:", result)


if __name__ == "__main__":
    main()
