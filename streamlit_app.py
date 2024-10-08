import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import datetime as dt
import report_maker

st.image('2021_fractracker_logo.png')
st.title("FracTracker Data Report")
st.write("This report contains visualizations of various attribute distributions in the data set scraped from Flickr. The data used in this report is scraped from Fractracker's Flickr page found [here](https://www.flickr.com/photos/fractracker/albums/). The photos were captured and labeled by members of the FracTracker organization. These photos contain imagery of fracking sites and sites related to the fracking process across the United States. These photos were taken in support of FracTracker's initiative to document environmental, health-related, and other impacts of fracking.")

uploaded_file = st.file_uploader(label = 'Drop the .csv file scraped from Flickr here:', type = 'csv')

# if uploaded_file is not None:

#     # df = pd.read_csv(uploaded_file)
#     # report_file = report_maker.
#     # # change other data report into an external function - call function from other file here

#     st.download_button(label = "Download Report",
#                        data = report_file,
#                        file_name = 'FracTracker_Data_Report' + str(dt.datetime) + '.')


if uploaded_file is not None:
    if st.button('Create Report'):
        report_maker.make_report(uploaded_file = uploaded_file)
        
