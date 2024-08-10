import streamlit as st
import requests
import toml

# Load configuration from TOML file
config = toml.load("services_config.toml")


def check_service_health(host, port):
    try:
        response = requests.get(f"http://{host}:{port}/health")
        if response.status_code == 200:
            return response.json().get("is_healthy", False)
        else:
            return False
    except Exception as e:
        return False


st.title("API Services Health Check")

status = {}

if st.button("Check All Services"):
    for service_name, service_info in config.items():
        host = service_info.get("host")
        port = service_info.get("port")
        with st.spinner(f"Checking {service_name}..."):
            is_healthy = check_service_health(host, port)
            status[service_name] = is_healthy

for service_name, service_info in config.items():
    col1, col2 = st.columns([2, 1])
    with col1:
        st.write(f"{service_name} ({service_info['host']}:{service_info['port']})")
    with col2:
        if service_name in status:
            if status[service_name]:
                st.success("Healthy")
            else:
                st.error("Not Healthy")
        else:
            st.write("Not Checked")
