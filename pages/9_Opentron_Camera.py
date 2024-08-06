import streamlit as st
import requests
import time  # Importing time for demonstration purposes

import requests
from PIL import Image
from io import BytesIO


# def fetch_camera_image(host, port, user):
#     url = f'http://{host}:{port}/camera/picture'
#     headers = {
#         'Opentrons-Version': '2'
#     }
#     response = requests.post(url, headers=headers, auth=(user, ''))
#     if response.status_code == 200:
#         return Image.open(BytesIO(response.content))
#     else:
#         st.error(f'Failed to fetch image from {host}:{port}')
#         return None

# def display_robot_camera(host, port, user, title):
#     st.header(title)
#     image = fetch_camera_image(host, port, user)
#     if image:
#         st.image(image, caption=f'Camera Image from {title}')

# def main():
#     st.title('Opentrons OT-2 Camera Viewer')

#     # Connection information
#     robots = {
#         'opentron0': {'host': '192.168.1.10', 'port': 31950, 'user': 'root'},
#         'opentron1': {'host': '192.168.1.54', 'port': 31950, 'user': 'root'}
#     }

#     for robot_name, info in robots.items():
#         display_robot_camera(info['host'], info['port'], info['user'], robot_name)
    
#     if st.button('Refresh'):
#         st.experimental_rerun()

# if __name__ == '__main__':
#     main()