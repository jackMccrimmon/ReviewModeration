import pandas as pd
from langdetect import detect


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


def main():
    df = pd.read_json('Data/review.json', lines=True)

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

    write = df.to_json(orient='records', lines=True)

    with open('Data/enriched_reviews.json', 'w') as file:
        file.write(write)


if __name__ == '__main__':
    main()


