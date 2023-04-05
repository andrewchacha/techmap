import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
import os

my_path = os.getcwd()
print(my_path)


def display_map(df,year):
    df = df[(df['dyear'] == year)]
    map = folium.Map(location=[1.6, 26.17],zoom_start=2.2, scrollWheelZoom = False,tiles='CartoDB positron')

    choropleth = folium.Choropleth(
        geo_data=my_path+'/data/world-administrative-boundaries.geojson',
        data=df,
        columns=('country','dyear'),
        key_on='feature.properties.name',
        line_opacity=0.8,
        highlight=True
    )
    choropleth.geojson.add_to(map)

    df = df.set_index('country')

    st_map = st_folium(map, width=700, height=450)

    country = ''
    if st_map['last_active_drawing']:
        country = st_map['last_active_drawing']['properties']['name']
    return country

def display_time_filters(df):
    year_list = list(df['dyear'].unique())
    year_list.sort(reverse=True)
    year = st.sidebar.selectbox('Year',[""]+year_list)
    return  year

def display_country_filter(df,state_name):
    state_list = [''] + list(df['country'].unique())
    state_list.sort()
    state_index = state_list.index(state_name) if state_name and state_name in state_list else 0
    return st.sidebar.selectbox('Country', state_list, state_index)


def display_country_filter2(df,state_name):
    state_list = [''] + list(df['country'].unique())
    state_list.sort()
    state_index = state_list.index(state_name) if state_name and state_name in state_list else 0
    return st.sidebar.selectbox('Comparison country', state_list, state_index)

def display_title_filter(df):
    title_list = [''] + list(df['dposition'].unique())
    title_list.sort()
    title = st.sidebar.selectbox('Job Title', title_list)
    return title


def display_month_filters(df):
    month_list = ['',1,2,3,4,5,6,7,8,9,10,11,12]
    month = st.sidebar.selectbox('Month', month_list)
    return month

@st.cache_data()
def display_all_results(dataset, year, country, title, month):
    if (country and not (title or month or year)):
        used_dataset = dataset[(dataset['country'] == country)]

    if (title and not (country or month or year)):
        used_dataset = dataset[(dataset['dposition'] == title)]

    if (year and not (title or month or country)):
        used_dataset = dataset[(dataset['dyear'] == year)]

    if (month and not (title or country or year)):
        used_dataset = dataset[(dataset['dmonth'] == month)]

    if (year and country and month and title):
        used_dataset = dataset[(dataset['dyear'] == year) & (dataset['country'] == country) & (dataset['dposition'] == title) & (dataset['dmonth'] == month)]

    if (year and country and title and not(month)):
        used_dataset = dataset[(dataset['dyear'] == year) & (dataset['country'] == country) & (dataset['dposition'] == title)]

    if (year and country and month and not(title)):
        used_dataset = dataset[(dataset['dyear'] == year) & (dataset['country'] == country) & (dataset['dmonth'] == month)]

    if (year and title and month and not (country)):
        used_dataset = dataset[(dataset['dyear'] == year) & (dataset['dposition'] == title) & (dataset['dmonth'] == month)]

    # year

    if (year and country and not (month or title)):
        used_dataset = dataset[(dataset['dyear'] == year) & (dataset['country'] == country)]

    if (year and title and not (month or country)):
        used_dataset = dataset[(dataset['dyear'] == year) & (dataset['dposition'] == title)]

    if (year and month and not (country or title)):
        used_dataset = dataset[(dataset['dyear'] == year) & (dataset['dmonth'] == month)]

    # Country
    if (country and title and not (month or year)):
        used_dataset = dataset[(dataset['country'] == country) & (dataset['dposition'] == title)]

    if (country and month and not (year or title)):
        used_dataset = dataset[(dataset['country'] == country) & (dataset['dmonth'] == month)]

    # Title
    if (title and month and not (year or country)):
        used_dataset = dataset[(dataset['dposition'] == title) & (dataset['dmonth'] == month)]

    if (not (title or month or year or country)):
        used_dataset = dataset

    totalads = used_dataset.groupby(['dyear', 'dmonth', 'dposition', 'country'])['allads'].unique().sum()
    all_ads = used_dataset.groupby(['tech_word'])['wcount'].sum().reset_index()
    sorted_all_ads = all_ads.sort_values(by=['wcount'], ascending=False)
    sorted_all_ads['Total Ads'] = int(totalads)
    sorted_all_ads['Percentage'] = round((sorted_all_ads['wcount'] / sorted_all_ads['Total Ads']) * 100).astype(int)
    sorted_all_ads.rename(columns={'tech_word': 'Keyword', 'wcount': 'Number of ads'}, inplace=True)
    return sorted_all_ads.head(50)

