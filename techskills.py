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
import numpy as np

my_path = os.getcwd()
print(my_path)


dataset = pd.read_csv(my_path+'/march2023.csv')

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
        options=["Home","Skills"],
        icons=["house","bar-chart-fill"],
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


if selected == "Skills":
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


if __name__ == '__main__':
    main()

