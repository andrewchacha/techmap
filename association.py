import pandas as pd
import  streamlit as st
from collections import Counter

def fetch_skill(df):
    '''
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
    '''
    df['consequents'] = df['consequents'].astype(str)
    word_list = list(df['consequents'].unique())
    word_list.sort()
    word = st.sidebar.selectbox('Key word', word_list)
    st.header(f'{word} Association')
    return word


def get_association(dataset,selected):
    sort_df = pd.DataFrame()
    #for i in selected:
        #fdf = dataset[dataset.antecedents.isin(i)].reset_index()
        #fdf = dataset[dataset.consequents.isin(i)].reset_index()
    fdf = dataset[dataset['consequents'] == selected].reset_index()
    results = fdf[['antecedents', 'consequents', 'support', 'confidence', 'lift']]
    sorted_associations = results.sort_values(by='lift', ascending=False)

    sort_df = pd.concat([sort_df,sorted_associations.head(5)])
    return sort_df

def fetch_top(dataset,selected):
    # Split the values in the relevant column into separate words
    data = dataset['liststring'].apply(lambda x: str(x)).str.split(',').tolist()
    data = [' '.join(map(str, row)) for row in data]

    # Define the query word
    query_word1 = str(selected).strip(",")
    query_word = query_word1.split()[0]


    # Use Counter to count word combinations
    word_counts = Counter()

    for row in data:
        words = row.split()
        if query_word in words:
            for word in words:
                if word != query_word:
                    word_counts[(query_word, word)] += 1

    # Get the top 3 words that appear with the query word
    top_words = word_counts.most_common(20)

    # Format the results in the desired format
    results = [[query_word, word_count[0][1], word_count[1]] for word_count in top_words]
    return results



