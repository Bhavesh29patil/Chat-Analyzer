import streamlit as st
import preprocessor,helper
import matplotlib.pyplot as plt
import seaborn as sns

on = st.sidebar.toggle('Click Here For Instructions')
if on:
    st.sidebar.write("Upload your Whatsapp Chat (Strictly in 24 hrs format. 12 hrs (am/pm) is not accepted will lead to an error)")
    st.sidebar.image('instruction_image.jpg')


uploaded_file = st.sidebar.file_uploader(":green[Choose a file]")
if uploaded_file is None:
    st.title("WhatsApp Chat Analyzer")
    st.text("")
    st.image("whatsapp_logo.png", width=200)
    st.text("")
    st.text("")
    st.text("")
    st.write("Check Source Code : [Link](https://github.com/Bhavesh29patil/Chat-Analyzer/tree/main)")

if uploaded_file is not None:
    st.sidebar.title(":green[WhatsApp Chat Analyzer]")
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode("utf-8")
    df = preprocessor.preprocess(data)

    #fetch unique users
    user_list = df['user'].unique().tolist()
    user_list.remove('group_notification')
    user_list.sort()
    user_list.insert(0, "Overall")

    selected_user = st.sidebar.selectbox("Show analysis wrt", user_list)

    if st.sidebar.button("Show Messages"):
        if selected_user != 'Overall':
            st.title(f'_:green[{selected_user}]_')
            df = df[df['user'] == selected_user]
        else:
            st.title(f'_:green[All Chats]_')
        st.dataframe(df[['date','user','message']].rename(columns={'date':'Date','user':'User','message':'Message'}))


    if st.sidebar.button("Show Analysis"):
        num_messages, words, num_media_messages, num_links = helper.fetch_stats(selected_user, df)
        if selected_user != 'Overall':
            st.title(f'_:green[{selected_user}]_')
        else:
            st.title(f'_:green[Overall Analysis]_')

        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.header("Messages")
            st.title(f':violet[{num_messages}]')
        with col2:
            st.header("Words")
            st.title(f':violet[{words}]')
        with col3:
            st.header("Media")
            st.title(f':violet[{num_media_messages}]')
        with col4:
            st.header("Links")
            st.title(f':violet[{num_links}]')

        # monthly timeline
        st.title('_Monthly Timeline_')
        timeline = helper.monthly_timeline(selected_user, df)
        fig, ax = plt.subplots()
        ax.plot(timeline['time'], timeline['message'], color='green')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        # activity map
        st.title('_Activity Map_')
        col1, col2 = st.columns(2)

        with col1:
            st.header("_Most busy day_")
            busy_day = helper.week_activity_map(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(busy_day.index, busy_day.values, color='purple')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        with col2:
            st.header("_Most busy month_")
            busy_month = helper.month_activity_map(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(busy_month.index, busy_month.values, color='orange')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        st.title("_Weekly Activity Map_")
        user_heatmap = helper.activity_heatmap(selected_user, df)
        fig, ax = plt.subplots()
        ax = sns.heatmap(user_heatmap)
        st.pyplot(fig)

        # busiest user
        if selected_user == 'Overall':
            st.title('_Most Busy Users_')
            x, new_df = helper.most_busy_users(df)
            fig, ax = plt.subplots()

            col1, col2 = st.columns(2)

            with col1:
                ax.bar(x.index, x.values, color='red')
                plt.xticks(rotation='vertical')
                plt.ylabel('Messages')
                st.pyplot(fig)
            with col2:
                st.dataframe(new_df)

        # WordCloud
        st.title("_Wordcloud_")
        df_wc = helper.create_wordcloud(selected_user, df)
        fig, ax = plt.subplots()
        ax.imshow(df_wc)
        st.pyplot(fig)

        # common words
        most_common_df = helper.most_common_words(selected_user, df)
        fig, ax = plt.subplots()
        ax.barh(most_common_df[0], most_common_df[1])
        plt.xticks(rotation='vertical')
        st.title('_Most commmon words_')
        st.pyplot(fig)

        # emoji's
        emoji_df = helper.emoji_helper(selected_user, df)
        st.title("_Emoji Analysis_")

        col1, col2 = st.columns(2)

        with col1:
            st.dataframe(emoji_df)
        with col2:
            fig, ax = plt.subplots()
            ax.pie(emoji_df['Count'].head(), labels=emoji_df['Emoji'].head(), autopct="%0.2f")
            st.pyplot(fig)
