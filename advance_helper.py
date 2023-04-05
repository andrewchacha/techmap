import streamlit as st
import pandas as pd


def display_time_filters(df):
    year_list = list(df['dyear'].unique())
    year_list.sort(reverse=True)
    year = st.sidebar.multiselect(
        "Select Year(s)",
        options=year_list
        )
    return  year
def display_skill_filters(df):
    skill = st.sidebar.multiselect(
        "Select Skill(s)",
        options=df['tech_word'].unique(),
        default=None
    )
    return skill
@st.cache_data()
def display_skills(dataset,skill,year):
    no_years = len(year)
    no_skills = len(skill)
    if (no_skills > 0):
        if (no_years > 1):
            use_df = dataset[dataset.dyear.isin(year)]
            new_df = use_df.groupby(['tech_word', 'dyear'])['wcount'].sum().reset_index()
            sorted_df = new_df.sort_values(by=['wcount'], ascending=False)
            sorted_df = sorted_df.sort_values(by=['dyear'], ascending=True)
            displaydf = sorted_df[sorted_df.tech_word.isin(skill)]
            displaydf.rename(columns={'tech_word': 'Keyword', 'wcount': 'Ads', 'dyear': 'Year'}, inplace=True)
            skillsets = skill
        elif (no_years == 1):
            use_df = dataset[dataset.dyear.isin(year)]
            new_df = use_df.groupby(['tech_word', 'dmonth'])['wcount'].sum().reset_index()
            sorted_df = new_df.sort_values(by=['wcount'], ascending=False)
            sorted_df = sorted_df.sort_values(by=['dmonth'], ascending=True)
            displaydf = sorted_df[sorted_df.tech_word.isin(skill)]
            displaydf.rename(columns={'tech_word': 'Keyword', 'wcount': 'Ads', 'dmonth': 'Month'}, inplace=True)
            skillsets = skill
        else:
            new_df = dataset.groupby(['tech_word', 'dyear'])['wcount'].sum().reset_index()
            sorted_df = new_df.sort_values(by=['wcount'], ascending=False)
            sorted_df = sorted_df.sort_values(by=['dyear'], ascending=True)
            displaydf = sorted_df[sorted_df.tech_word.isin(skill)]
            displaydf.rename(columns={'tech_word': 'Keyword', 'wcount': 'Ads', 'dyear': 'Year'}, inplace=True)
            skillsets = skill
    else:
        new_df = dataset.groupby(['tech_word', 'dyear'])['wcount'].sum().reset_index()
        sorted_df = new_df.sort_values(by=['wcount'], ascending=False)
        skillsets = sorted_df.tech_word[:5].tolist()
        sorted_df = sorted_df.sort_values(by=['dyear'], ascending=True)
        displaydf = sorted_df[sorted_df.tech_word.isin(skillsets)]
        displaydf.rename(columns={'tech_word': 'Keyword', 'wcount': 'Ads','dyear': 'Year'}, inplace=True)
    return displaydf, skillsets
