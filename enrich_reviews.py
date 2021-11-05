import pandas as pd
from langdetect import detect
import plotly.offline as pyo
import plotly.graph_objs as go
from plotly.subplots import make_subplots


def check_language(df):
    text = df.iloc[:, 2]
    lang = []
    for msg in text:
        if msg != "":
            temp = detect(msg)
        else:
            temp = "none"
        lang.append(temp)
    df['language'] = lang


def low_score(df):
    score = df.iloc[:, 1]
    temp = []
    for x in score:
        if x <= 2.5:
            temp.append(1)
        if x > 2.5:
            temp.append(0)
    df['low_score'] = temp


def high_score(df):
    score = df.iloc[:, 1]
    temp = []
    for x in score:
        if x <= 2.5:
            temp.append(0)
        if x > 2.5:
            temp.append(1)
    df['high_score'] = temp


def num_words(df):
    text = df.iloc[:, 2]
    word_count = []
    for msg in text:
        temp = msg.split()
        word_count.append(len(temp))
    df['word_count'] = word_count


def is_anonymous(df):
    user = df.iloc[:, 0]
    temp = []
    for name in user:
        if name == 'Anonymous':
            temp.append(1)
        else:
            temp.append(0)
    df['anonymous'] = temp


def flag_fake(df):
    flags = []
    for index, row in df.iterrows():
        total = 0
        if row["anonymous"] == 1:
            total += 1
        if row["language"] != "en":
            total += 1
        if row["word_count"] == 0:
            total += 1
        if row["word_count"] < 20 and row["low_score"] == 1:
            total += 1
        flags.append(total)
    df['flag_tally'] = flags


def flagged(df):
    temp = df.iloc[:, 8]
    create_flag = []
    for ind in temp:
        if ind > 1:
            create_flag.append("Flagged Fake")
        else:
            create_flag.append("---")
    df['is_flagged'] = create_flag


def flagged_list(df):
    temp = []
    for row in df.iterrows():
        if row['is_flagged'] == "Flagged Fake":
            temp.append(row)

    df_1 = pd.DataFrame(temp)
    write = df_1.to_json(orient='records', lines=True)

    with open('Data/flagged_reviews.json', 'w') as file:
        file.write(write)

def print_dashboard(df):
    # Number of reviews by rating
    df1 = df.groupby(['rating'])['user_id'].count().reset_index()
    df1 = df1.sort_values(by=['user_id'], ascending=[False])

    # Number of flagged reviews
    df2 = df.groupby(['is_flagged'])['rating'].count().reset_index()

    # Number of flagged reviews by rating
    df3 = df[df['is_flagged'] == "Flagged Fake"].groupby(['rating'])['user_id'].count().reset_index()
    df4 = df[df['is_flagged'] != "Flagged Fake"].groupby(['rating'])['user_id'].count().reset_index()
    print(df3)
    print(df4)

    fig = make_subplots(rows=3, cols=1, subplot_titles=("Flagged Fake Breakdown", "Reviews by Rating", "Reviews by Rating With Flagged Fake"), specs=[[ {'type' : 'pie'}],[{'type' : 'bar'}],[{'type' : 'bar'}]])
    fig.add_trace(go.Pie(labels=["Not Flagged Fake (Pie Chart)", "Flagged Fake (Pie Chart)"], values=df2['rating']), row=1, col=1)
    fig.add_trace(go.Bar(x=df1['rating'], y=df1['user_id'], name='Reviews Without Flags', marker_color='rgb(26, 200, 26)'), row=2, col=1)
    fig.add_trace(go.Bar(x=df4['rating'], y=df4['user_id'], name='Not Flagged Fake', marker_color='rgb(26, 118, 255)'), row=3, col=1)
    fig.add_trace(go.Bar(x=df3['rating'], y=df3['user_id'], name='Flagged Fake', marker_color='rgb(255, 50, 26)'), row=3, col=1)
    fig.update_layout(height=600, width=800, title_text="Product Review Report", barmode='stack')

    pyo.plot(fig, filename='ReviewDashboard.html')

def main(file):
    df = pd.read_json(file, lines=True)

    print("\nData Frame Before Enrichment:")
    print(df)

    check_language(df)
    low_score(df)
    high_score(df)
    num_words(df)
    is_anonymous(df)
    flag_fake(df)
    flagged(df)

    print("\nData Frame After Enrichment:")
    print(df)

    print_dashboard(df)

    write = df.to_json(orient='records', lines=True)

    with open('Data/enriched_reviews.json', 'w') as file:
        file.write(write)



