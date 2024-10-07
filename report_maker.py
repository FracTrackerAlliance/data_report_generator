import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import plotly.express as px

def make_report(uploaded_file):
    df = pd.read_csv(uploaded_file)

    st.subheader("Attribute Overview")
    shape = df.shape
    st.markdown("This data set has " + str(shape[0]) + " photos and " + str(shape[1]) + " attributes per photo.")
    st.markdown(
    """
    Here is a brief description of each of the attributes:
    - `PhotoID`: Unique identifier for each photo scraped from Flickr
    - `AlbumID`: List of IDs for the albums that contain the photo 
    - `AlbumTitle`: List of titles for the albums 
    - `Date_taken`: Date and time when the photo was taken 
    - `Description`: Description of the photo entered on Flickr
    - `Latitude`: Latitude where the photo was taken 
    - `Longitude`: Longitude where the photo was taken 
    - `Title`: Title of the photo entered on Flickr
    - `LightHawk`: True or False value indicating whether the photographer used LightHawk to obtain the photo (pulled from the title column)
    - `Mission`: The mission name associated with the photo (pulled from the title column)
    - `Mission Description`: Detailed description of the mission (pulled from the title column)
    - `st_count`: State and county information (pulled from the title column)
    - `Title_photo_attr`: Attribution for the photo title (pulled from the title column)
    """
    )
    
