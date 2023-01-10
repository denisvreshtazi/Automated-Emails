import datetime
import yagmail
import pandas as pd
from news import NewsFeed
import time

while True:
    # To execute it at a certain time of the day
    if datetime.datetime.now().hour == 17 and datetime.datetime.now().minute == 33:
        df = pd.read_excel('people.xlsx')

        for index, row in df.iterrows():
            email = yagmail.SMTP(user="Insert your email", password="Insert your google app password")
            today = datetime.datetime.now().strftime("%Y-%m-%d")
            # An alternative: today = date.today().strftime("%Y-%m-%d")
            yesterday = (datetime.datetime.now() - datetime.timedelta(days=1)).strftime("%Y-%m-%d")
            news_feed = NewsFeed(row['interest'], today, yesterday).get()
            email.send(to=row['email'],
                       subject=f"Here are the news about {row['interest']}  for today!",
                       contents=f"Dear {row['name']} \n Check out the news about {row['interest']} : \n {news_feed}",
                       attachments="design.txt")
    time.sleep(60)
