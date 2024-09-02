import streamlit as st
import preprocessor
import helper
import matplotlib.pyplot as plt


st.sidebar.title('WhatsApper')

uploaded_file = st.sidebar.file_uploader('Choose a file')
if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode('utf-8')
    df = preprocessor.preprocess(data)

    st.title('Data')
    st.dataframe(df)

    user_list = df['user'].unique().tolist()
    user_list.remove('group notification')
    user_list.sort()
    user_list.insert(0, 'Overall')

    selected = st.sidebar.selectbox('Select user', user_list)

    if st.sidebar.button('Show Analysis'):

        st.title('Chat Statistics and Analysis')

        messages, words, media_messages, links = helper.fetch_stats(selected, df)

        st.title('Statistics')
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.header('Messages')
            st.subheader(messages)

        with col2:
            st.header('Words')
            st.subheader(words)

        with col3:
            st.header('Media')
            st.subheader(media_messages)

        with col4:
            st.header('Links')
            st.subheader(links)

        if selected == 'Overall':
            x, new_df = helper.most_active_user(df)
            fig, ax = plt.subplots()

            col1, col2 = st.columns(2)

            with col1:
                st.header('Users')
                ax.bar(x.index, x.values)
                plt.ylabel('Number of messages')
                plt.xticks(rotation='vertical')
                st.pyplot(fig)

            with col2:
                st.header('Activity')
                st.dataframe(new_df)

        st.title('Analysis')
        st.header('Word Cloud')
        df_wc = helper.create_wordcloud(selected, df)
        fig, ax = plt.subplots()
        ax.imshow(df_wc)
        st.pyplot(fig)

        st.header("Common Words")
        df_common = helper.most_common_word(selected, df)

        col1, col2 = st.columns(2)

        with col1:
            st.subheader('Count')
            st.dataframe(df_common)

        with col2:
            st.subheader('Percentage')
            fig, ax = plt.subplots()
            ax.pie(df_common['Frequency'].head(), labels=df_common['Word'].head(), autopct='%0.2f')
            st.pyplot(fig)

        st.header('Emojis')
        emoji_df = helper.emoji_used(selected, df)

        col1, col2 = st.columns(2)

        with col1:
            st.subheader('Count')
            st.dataframe(emoji_df)

        with col2:
            st.subheader('Percentage')
            fig, ax = plt.subplots()
            ax.pie(emoji_df['Frequency'].head(), labels=emoji_df['Emoji'].head(), autopct='%0.2f')
            st.pyplot(fig)

        st.header('Timeline')
        col1, col2 = st.columns(2)

        with col1:
            st.subheader('Monthly')
            timeline = helper.mon_timeline(selected, df)
            fig, ax = plt.subplots()
            ax.plot(timeline['time'], timeline['user_message'])
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        with col2:
            st.subheader('Daily')
            timeline_date = helper.daily_timeline(selected, df)
            fig, ax = plt.subplots()
            ax.plot(timeline_date['only_date'], timeline_date['user_message'])
            plt.xticks(rotation='vertical')
            st.pyplot(fig)
