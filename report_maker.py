import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import plotly.express as px

def make_report(uploaded_file):
    df = pd.read_csv(uploaded_file)

    st.subheader("Attribute Overview")
    shape = df.shape
    st.markdown("This data set has " + str(shape[0]) + " photos and " + str(shape[1]) + " attributes per photo.")
    st.markdown("The attributes in this data set are " + str(list(df.columns)))
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
    
    st.subheader("`PhotoID`")
    st.markdown('There are ' + str(len(df.PhotoID.unique())) + ' unique PhotoIDs in this data set.')
    st.markdown('There are ' + str(len(df[df.duplicated(subset = ['PhotoID']) == True])) + ' repeat PhotoIDs in this data set.')

    st.subheader("`AlbumID` and `AlbumTitle`")

    st.subheader("`Date_taken`")
    # Convert 'Date_taken' to datetime for time series plotting
    df['Date_taken'] = pd.to_datetime(df['Date_taken'])

    date_counts = df['Date_taken'].dt.to_period('M').value_counts().sort_index()

    st.pyplot(plt.figure(figsize=(10, 6)))
    date_counts.plot(kind='line', color='green')
    plt.title('Photos Taken Over Time')
    plt.xlabel('Date')
    plt.ylabel('Number of Photos')
    plt.show()

    st.subheader("Description")

    st.subheader("Latitude and Longitude")

    st.subheader("Title")

    st.subheader("Mission")

    st.subheader("Mission Description")

    st.subheader("st_count")