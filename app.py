import os
import sys

# Wrapper to run streamlit_api_assistant.py
with open(os.path.join(os.path.dirname(__file__), "streamlit_api_assistant.py"), encoding="utf-8") as f:
    exec(f.read(), globals())
