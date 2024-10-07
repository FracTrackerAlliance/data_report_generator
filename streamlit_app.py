import streamlit as st
import pandas as pd

st.title("FracTracker Data Report")
st.write("This report contains visualizations of various attribute distributions in the data set scraped from Flickr. The data used in this report is scraped from Fractracker's Flickr page found [here](https://www.flickr.com/photos/fractracker/albums/). The photos were captured and labeled by members of the FracTracker organization. These photos contain imagery of fracking sites and sites related to the fracking process across the United States. These photos were taken in support of FracTracker's initiative to document environmental, health-related, and other impacts of fracking.")

uploaded_file = st.file_uploader(label = 'Drop the .csv file scraped from Flickr here:', type = 'csv')

if uploaded_file is not None:
    st.write('Data Uploaded Successfully')
    if st.button(label = 'Download Report'):
        st.write('clicked')



# df = pd.read_csv(uploaded_file)
