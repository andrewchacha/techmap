import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import os
from streamlit_option_menu import option_menu
import helper
import advance_helper
import association
#import getforecast
import numpy as np
from pyvis.network import Network
import streamlit.components.v1 as components

#from statsmodels.tsa.seasonal import seasonal_decompose
#from prophet import Prophet
#from prophet.diagnostics import cross_validation
#from prophet.diagnostics import performance_metrics
#from prophet.plot import plot_cross_validation_metric

st.set_option('deprecation.showPyplotGlobalUse', False)

my_path = os.getcwd()
print(my_path)

from sqlalchemy import create_engine
my_conn = create_engine("mysql+pymysql://root:Tanzania1@localhost:3306/techtrends")
query = "SELECT * FROM techtrends"
dataset = pd.read_sql(query, my_conn)
dataset['tech_word'] = dataset['tech_word'] .str.strip()

#dataset = pd.read_csv(my_path+'/march2023.csv')
#dataset['tech_word'] = dataset['tech_word'] .str.strip()

APP_TITTLE = "TREND OF TECH ITEMS IN IT JOB ADS"


st.set_page_config(APP_TITTLE, layout="wide")
st.title(APP_TITTLE)


hide_streamlit_style = """
               <style>
               #MainMenu {visibility: hidden;}
               footer {visibility: hidden;}
               header {visibility: hidden;}
               </style>
               """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)


with st.sidebar:
    selected = option_menu(
        menu_title=None,
        options=["Home","Trends","Association"],
        icons=["house","bar-chart-fill","bricks"],
        default_index=0,
   )


if selected == "Home":
    st.subheader(f'Home')


    def main():
        # Load Data
        # Display Filters and Map
        year = helper.display_time_filters(dataset)
        month = helper.display_month_filters(dataset)
        title = helper.display_title_filter(dataset)
        country = helper.display_map(dataset, year)
        country = helper.display_country_filter(dataset, country)
        country2 = helper.display_country_filter2(dataset, country)

        # Display Statistics
        st.subheader(f'{year} {title} Trending Tech Words')

        hide_table_row_index = """
                    <style>
                    thead tr th:first-child {display:none}
                    tbody th {display:none}
                    </style>
                    """
        st.markdown(hide_table_row_index, unsafe_allow_html=True)

        dispay_top2 = helper.display_all_results(dataset, year, country, title, month)
        if (country2):
            dispay_top3 = helper.display_all_results(dataset, year, country2, title, month)

        col1, col2 = st.columns(2)
        with col1:
            if (country):
                st.subheader(f'{country} {title} Top Words')
            else:
                st.subheader(f'Top Words')
            st.table(dispay_top2.sort_values(by=['Number of ads'], ascending=False).head(20))
            tobar = dispay_top2.sort_values(by=['Number of ads'], ascending=False).head(10)

            st.subheader(f'{country} {title} Bar Graph')

            st.bar_chart(data=tobar, x='Keyword', y='Number of ads', height=450, use_container_width=True)

            # world Cloud
            st.subheader(f'{country} {title} Word Cloud')

            wordsc = dispay_top2.set_index('Keyword').to_dict()['Number of ads']
            wc = WordCloud(width=800, height=400, max_words=200).generate_from_frequencies(wordsc)
            fig, ax = plt.subplots(figsize=(10, 10))
            ax.imshow(wc, interpolation='bilinear')
            plt.axis('off')
            st.pyplot(fig)
        with col2:
            if (country2):
                st.subheader(f'{country2} {title} Top Words')
                st.table(dispay_top3.sort_values(by=['Number of ads'], ascending=False).head(20))
                tobar = dispay_top3.sort_values(by=['Number of ads'], ascending=False).head(10)

                st.subheader(f'{country2} {title} Bar Graph')

                st.bar_chart(data=tobar, x='Keyword', y='Number of ads', height=450, use_container_width=True)

                # world Cloud
                st.subheader(f'{country2} {title} Word Cloud')

                wordsc = dispay_top3.set_index('Keyword').to_dict()['Number of ads']
                wc = WordCloud(width=800, height=400, max_words=200).generate_from_frequencies(wordsc)
                fig, ax = plt.subplots(figsize=(10, 10))
                ax.imshow(wc, interpolation='bilinear')
                plt.axis('off')
                st.pyplot(fig)


if selected == "Trends":
    st.subheader(f'Advanced Skills search')
    hide_table_row_index = """
                        <style>
                        thead tr th:first-child {display:none}
                        tbody th {display:none}
                        </style>
                        """
    st.markdown(hide_table_row_index, unsafe_allow_html=True)
    def main():
        year = advance_helper.display_time_filters(dataset)
        skill = advance_helper.display_skill_filters(dataset)
        skill_df,rskill = advance_helper.display_skills(dataset,skill,year)
        no_years = len(year)
        no_skills = len(skill)

        fig, ax = plt.subplots(figsize=(10, 5))
        for i in rskill:
            todraw = skill_df[skill_df.Keyword == i]
            if (no_skills > 0):
                if (no_years == 1):
                    plt.plot(np.array(todraw.Month).astype(str), todraw.Ads, marker='.', label=i)
                else:
                    plt.plot(np.array(todraw.Year).astype(str), todraw.Ads, marker='.', label=i)
            else:
                plt.plot(np.array(todraw.Year).astype(str), todraw.Ads, marker='.', label=i)
        plt.legend()
        plt.xlabel('Year')
        plt.ylabel('Job Ads')
        plt.tight_layout()
        plt.grid(True)
        plt.title('Changes in skills')
        st.pyplot(fig)

        st.table(skill_df)

if selected == "Association":
    hide_table_row_index = """
                           <style>
                           thead tr th:first-child {display:none}
                           tbody th {display:none}
                           </style>
                           """
    st.markdown(hide_table_row_index, unsafe_allow_html=True)
    def main():
        st.subheader("Skills Association")

        areas = ['','Software','Data','Developer','Engineer','Support','Network']
        areas.sort(reverse=False)
        areas_q = st.sidebar.selectbox('Job Title',areas)


        if areas_q == 'Software':
            adata = pd.read_csv('data/software_association.csv')
            bdata = pd.read_csv('data/software.csv')

        elif areas_q == 'Data':
            adata = pd.read_csv('data/data_association.csv')
            bdata = pd.read_csv('data/data.csv')

        elif areas_q == 'Developer':
            adata = pd.read_csv('data/dev_association.csv')
            bdata = pd.read_csv('data/developer.csv')

        elif areas_q == 'Engineer':
            adata = pd.read_csv('data/engineer_association.csv')
            bdata=pd.read_csv('data/engineer.csv')

        elif areas_q == 'Support':
            adata = pd.read_csv('data/support_association.csv')
            bdata = pd.read_csv('data/support.csv')

        elif areas_q == 'Network':
            adata = pd.read_csv('data/network_association.csv')
            bdata = pd.read_csv('data/network.csv.csv')
        else:
            adata = pd.read_csv('data/all_association.csv')
            bdata = pd.read_csv('data/all.csv')

        selected_key = association.fetch_skill(adata)
        associations = association.get_association(adata,selected_key)
        st.table(associations)

        #st.subheader(f'Top 30 words appearing with {selected_key} ')
        top_asscociations = association.fetch_top(bdata,selected_key)
        #for row in top_asscociations:
        #    st.write(f'{row},')

        soft_net = Network(height='750px', width='100%', bgcolor='#222222', font_color='white', notebook=True)
        soft_net.repulsion()
        for e in top_asscociations:
            src = e[0]
            dist = e[1]
            w = np.log(e[2])

            soft_net.add_node(src, src, title=src)
            soft_net.add_node(dist, dist, title=dist)
            soft_net.add_edge(src, dist, value=w)

        neighbor_map = soft_net.get_adj_list()
        for node in soft_net.nodes:
            node['title'] += ' Neighbors:' + ''.join(neighbor_map[node['id']])
            node['value'] = len(neighbor_map[node['id']])

        soft_net.show('data.html')

        from IPython.core.display import display, HTML
        display(HTML("data.html"))

        st.header(f"{selected_key} Network")
        HtmlFile = open("data.html", 'r', encoding='utf-8')
        source_code = HtmlFile.read()
        components.html(source_code, height=760)


if __name__ == '__main__':
    main()

