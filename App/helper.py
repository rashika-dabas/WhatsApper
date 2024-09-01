import pandas as pd
import emoji

from urlextract import URLExtract
from wordcloud import WordCloud
from collections import Counter


extractor = URLExtract()


def fetch_stats(selected, df):
    if selected != 'Overall':
        df = df[df['user'] == selected]
    messages = df.shape[0]
    words = []
    for message in df['user_message']:
        words.extend(message.split())
    media_messages = df[df['user_message'] == "<Media omitted>\n"].shape[0]
    links = []
    for message in df['user_message']:
        links.extend(extractor.find_urls(message))
    return messages, len(words), media_messages, len(links)


def most_active_user(df):
    x = df['user'].value_counts().head()
    df = round((df['user'].value_counts() / df.shape[0]) * 100, 2).reset_index().rename(
        columns={'index': 'Name', 'user': 'Percentage'})
    return x, df


def create_wordcloud(selected, df):
    if selected != 'Overall':
        df = df[df['user'] == selected]
    wc = WordCloud(width=400, height=400, min_font_size=8, background_color='white')
    df_wc = wc.generate(df['user_message'].str.cat(sep=' '))
    return df_wc


def most_common_word(selected, df):
    f = open('stop_hinglish.txt', 'r')
    stop_words = f.read()
    if selected != 'Overall':
        df = df[df['user'] == selected]
    df1 = df[df['user'] != 'group notification']
    df2 = df1[df1['user_message'] != '<Media omitted>\n']
    temp = df2[df2['user_message'] != 'This message was deleted\n']
    words = []
    for message in temp['user_message']:
        for word in message.lower().split():
            if word not in stop_words:
                if word == '@917506941616':
                    words.append('admin tagged')
                else:
                    words.append(word)
    df_common = pd.DataFrame(Counter(words).most_common(20), columns=['Word', 'Frequency'])
    return df_common


def emoji_used(selected, df):
    if selected != 'Overall':
        df = df[df['user'] == selected]
    emojis = []
    for i in df['user_message']:
        emojis.extend([c for c in i if c in emoji.UNICODE_EMOJI['en']])
    emoji_df = pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))),  columns=['Emoji', 'Frequency'])
    return emoji_df


def mon_timeline(selected, df):
    if selected != 'Overall':
        df = df[df['user'] == selected]
    timeline = df.groupby(['year', 'month', 'month_num']).count()['user_message'].reset_index()
    time = []
    for i in range(timeline.shape[0]):
        time.append(timeline['month'][i] + " - " + str(timeline['year'][i]))
    timeline['time'] = time
    return timeline


def daily_timeline(selected, df):
    if selected != 'Overall':
        df = df[df['user'] == selected]
    timeline_date = df.groupby('only_date').count()['user_message'].reset_index()
    return timeline_date
