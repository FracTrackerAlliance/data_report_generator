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
    plt.show()
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
    plt.show()
    st.pyplot(plt)

    st.subheader("`Date_taken`")
    # Convert 'Date_taken' to datetime for time series plotting
    df['Date_taken'] = pd.to_datetime(df['Date_taken'])
    date_counts = df['Date_taken'].dt.to_period('M').value_counts().sort_index()
    plt.figure(figsize=(10, 6))
    date_counts.plot(kind='line', color='green')
    plt.title('Photos Taken Over Time')
    plt.xlabel('Date')
    plt.ylabel('Number of Photos')
    plt.show()
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
    plt.show()
    st.pyplot(plt)

    st.subheader("`Description`")
    st.markdown('There are ' + str(len(df.Description.unique())) + ' unique photo descriptions. The most common one is:')
    description = df.Description.value_counts().head(1)
    st.markdown('*' + str(description) + '*')

    st.subheader("`Latitude` and `Longitude`")
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

    st.subheader("`Title`")

    st.subheader("`Mission`")

    st.subheader("`Mission Description`")

    st.subheader("`st_count`")