import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import plotly.express as px
import datetime as dt

def make_report(uploaded_file):
    df = pd.read_csv(uploaded_file)

    st.title("Data Report " + str(dt.datetime.now.strftime("%d %B %Y")))

    st.header("Attribute Overview")
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
    
    st.header("`PhotoID`")
    st.markdown('There are ' + str(len(df.PhotoID.unique())) + ' unique PhotoIDs in this data set.')
    st.markdown('There are ' + str(len(df[df.duplicated(subset = ['PhotoID']) == True])) + ' repeat PhotoIDs in this data set.')

    st.header("`AlbumID` and `AlbumTitle`")
    df['AlbumID'] = df['AlbumID'].apply(lambda x: x.replace('[', ''))
    df['AlbumTitle'] = df['AlbumTitle'].apply(lambda x: x.replace('[', ''))
    df['AlbumID'] = df['AlbumID'].apply(lambda x: x.replace(']', ''))
    df['AlbumTitle'] = df['AlbumTitle'].apply(lambda x: x.replace(']', ''))
    df['AlbumTitle'] = df['AlbumTitle'].apply(lambda x: x.replace('\', ', '|'))
    df['AlbumTitle'] = df['AlbumTitle'].apply(lambda x: x.replace('\'', ''))
    alb_df = pd.DataFrame()
    count = 0
    for lis in df.AlbumTitle.apply(lambda x: x.split('|')):
        for item in lis:
            alb_df.loc[count, 'Album'] = item
            count+=1
    albs = alb_df.value_counts()
    plt.figure(figsize=(15, 6))
    bars = albs.plot(kind='bar', color='pink')
    # Add counts on top of each bar
    for bar in bars.patches:
        bars.annotate(f'{int(bar.get_height())}', 
                    (bar.get_x() + bar.get_width() / 2, bar.get_height()), 
                    ha='center', va='bottom', fontsize=10)
    plt.title('Distribution of Photos across Albums (including repeats in multiple albums)')
    plt.xlabel('Album Titles')
    plt.ylabel('Number of Photos')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    # plt.show()
    st.pyplot(plt)
    num_albums_per_pic = df.AlbumID.apply(lambda x: x.count(',')+1)
    alb_counts = num_albums_per_pic.value_counts().sort_index()

    plt.figure(figsize=(10, 6))
    bars = alb_counts.plot(kind='bar', color='pink')

    # Add counts on top of each bar
    for bar in bars.patches:
        bars.annotate(f'{int(bar.get_height())}', 
                    (bar.get_x() + bar.get_width() / 2, bar.get_height()), 
                    ha='center', va='bottom', fontsize=10)

    plt.title('Photos in Multiple Albums')
    plt.xlabel('Number of Albums the photos belong to')
    plt.ylabel('Number of Photos')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    # plt.show()
    st.pyplot(plt)

    st.header("`Date_taken`")
    # Convert 'Date_taken' to datetime for time series plotting
    df['Date_taken'] = pd.to_datetime(df['Date_taken'])
    date_counts = df['Date_taken'].dt.to_period('M').value_counts().sort_index()
    plt.figure(figsize=(10, 6))
    date_counts.plot(kind='line', color='green')
    plt.title('Photos Taken Over Time')
    plt.xlabel('Date')
    plt.ylabel('Number of Photos')
    # plt.show()
    st.pyplot(plt)
    months = df['Date_taken'].apply(lambda x: x.month)
    month_count = months.value_counts().sort_index()
    plt.figure(figsize=(10, 6))
    bars = month_count.plot(kind='bar', color='indigo')
    # Add counts on top of each bar
    for bar in bars.patches:
        bars.annotate(f'{int(bar.get_height())}', 
                    (bar.get_x() + bar.get_width() / 2, bar.get_height()), 
                    ha='center', va='bottom', fontsize=10)
    bars.set_xticklabels(['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 
                        'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'])
    plt.title('Month Distribution with counts')
    plt.xlabel('Month')
    plt.ylabel('Number of Photos')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    # plt.show()
    st.pyplot(plt)

    st.header("`Description`")
    st.markdown('There are ' + str(len(df.Description.unique())) + ' unique photo descriptions. The most common one is:')
    description = df.Description.value_counts().head(1)
    st.markdown('*' + str(description) + '*')

    st.header("`Latitude` and `Longitude`")
    fig = px.scatter_mapbox(df, 
                        lat="Latitude", 
                        lon="Longitude",
                        color_discrete_sequence=["#901be3"],
                        zoom=3, 
                        height=400,
                        width=700,
                        opacity=0.2,
                       )
    fig.update_traces(
        marker=dict(
            size=12
        ),
        selector=dict(mode="markers"),
    )
    fig.update_layout(mapbox_style="open-street-map")
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    # fig.show()
    st.plotly_chart(fig)
    st.markdown('There are ' + str(len(df[df['Latitude'].isna() == True])) + ' photos missing a value for `Latitude`.')
    st.markdown('There are ' + str(len(df[df['Longitude'].isna() == True])) + ' photos missing a value for `Longitude`.')

    st.header("`Title`")
    s = df.loc[0,'Title'] # grab the first cell's contents of the Title column
    st.markdown("An example from the title column:")
    st.markdown("*" + s + "*")
    st.subheader("Title Field Structure")
    st.markdown("The structure of the title field is explained under each photo's listed title as `Photographer_topic-sitespecific-siteowner-county-state_partneraffiliation_date(version)`. The structure we used to separate out the important attributes is as follows: `PhotoAttribution _ Type-of-Hazardous-Site _ CommercialName _ CountyState _ MonthYear`. From `Title`, we determined the following fields: `LightHawk`, `Mission`, `Mission Description`, `st_count`, `Title_photo_attr`")

    st.header("`Mission`")
    # Mission Distribution
    mission_counts = df['Mission'].value_counts()
    # Plot the Mission Distribution with counts on top of each bar
    plt.figure(figsize=(10, 6))
    bars = mission_counts.plot(kind='bar', color='skyblue')
    # Add counts on top of each bar
    for bar in bars.patches:
        bars.annotate(f'{int(bar.get_height())}', 
                    (bar.get_x() + bar.get_width() / 2, bar.get_height()), 
                    ha='center', va='bottom', fontsize=10)
    plt.title('Mission Distribution with counts')
    plt.xlabel('Mission')
    plt.ylabel('Number of Photos')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    # plt.show()
    st.pyplot(plt)

    st.header("`Mission Description`")
    st.markdown('There are ' + str(len(df['Mission Description'].value_counts())) + ' unique Mission Descriptions.')
    mission_df = pd.DataFrame(df['Mission Description'].value_counts().head())
    st.markdown('Top 5 Most Used Mission Descriptions:')
    st.dataframe(mission_df)

    st.header("`st_count`")
    st.markdown('The photos in this data set are located in ' + str(len(df.st_count.value_counts())) + ' counties.')
    states = df.st_count.apply(lambda x: x.split(', ')[1])
    state_counts = states.value_counts()
    # Plot the Mission Distribution with counts on top of each bar
    plt.figure(figsize=(10, 6))
    bars = state_counts.plot(kind='bar', color='orange')
    # Add counts on top of each bar
    for bar in bars.patches:
        bars.annotate(f'{int(bar.get_height())}', 
                    (bar.get_x() + bar.get_width() / 2, bar.get_height()), 
                    ha='center', va='bottom', fontsize=10)
    plt.title('Distribution of Photos across States')
    plt.xlabel('State')
    plt.ylabel('Number of Photos')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    # plt.show()
    st.pyplot(plt)