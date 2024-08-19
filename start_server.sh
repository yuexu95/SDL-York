#!/bin/bash
# kill the server
lsof -ti:8501 | xargs kill
# start the server
nohup streamlit run SDL-LNP.py 2>&1 > ./streamlit.log &
