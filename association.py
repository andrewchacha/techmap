import pandas as pd
import  streamlit as st

def fetch_skill(df):
    df['consequents'] = df['consequents'].astype(str)
    word_list = list(df['consequents'].unique())
    word_list.sort()
    word = st.sidebar.multiselect(
        "Select Skill(s)",
        options=word_list,
        default=None
    )
    #word = st.sidebar.selectbox('Key word', word_list)
    st.header(f'{list(word)} Association')
    return word


def get_association(dataset,selected):
    sort_df = pd.DataFrame()
    for i in selected:
        #fdf = dataset[dataset.antecedents.isin(i)].reset_index()
        fdf = dataset[dataset['consequents'] == i].reset_index()
        results = fdf[['antecedents', 'consequents', 'support', 'confidence', 'lift']]
        sorted_associations = results.sort_values(by='lift', ascending=False)

        sort_df = pd.concat([sort_df,sorted_associations.head(5)])
    return sort_df


