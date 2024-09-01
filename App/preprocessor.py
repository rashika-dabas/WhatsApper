import pandas as pd
import re


def preprocess(data):
    pattern = '\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s-\s'
    message = re.split(pattern, data)[1:]
    dates = re.findall(pattern, data)

    df = pd.DataFrame({'user_message': message, 'date': dates})

    df['date'] = pd.to_datetime(df['date'], format='%d/%m/%y, %H:%M - ')

    user = []
    messages = []

    for chat in df['user_message']:
        if ":" in chat:
            e = re.split('([\w\W]+?):\s', chat)

            user.append(e[1])
            messages.append(e[2])
        else:
            user.append('group notification')
            messages.append(chat)

    df['user_message'] = messages
    df['user'] = user

    df['year'] = df['date'].dt.year
    df['month'] = df['date'].dt.month_name()
    df['day'] = df['date'].dt.day
    df['hour'] = df['date'].dt.hour
    df['minute'] = df['date'].dt.minute
    df['month_num'] = df['date'].dt.month
    df['only_date'] = df['date'].dt.date

    return df
