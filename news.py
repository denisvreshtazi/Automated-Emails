# API key: Insert your API Key from newsapi.org
from datetime import date, timedelta
import requests


class NewsFeed:
    """ Representing  multiple news titles and links as a single string
    """
    base_url = 'https://newsapi.org/v2/everything?'
    # api_key: insert it here
    api_key = '3cda9b2b3fdd4ed4b997d96b12ff4088'

    def __init__(self, interest, from_date, to_date, language='en'):
        self.interest = interest
        self.from_date = from_date
        self.to_date = to_date
        self.language = language

    def get(self):
        request = requests.get(f'{self.base_url}'
                               f'qInTitle={self.interest}&'
                               f'from={self.from_date}&'
                               f'to={self.to_date}&'
                               'sortBy=publishedAt&'
                               f'language={self.language}&'
                               f'apiKey={self.api_key}')
        response = request.json()
        articles = response['articles']

        email_body = ''
        for article in articles:
            email_body += article['title'] + '\n' + article['url'] + '\n\n'

        return email_body


if __name__ == '__main__':
    today = date.today()
    yesterday = today - timedelta(days=1)
    news_feed = NewsFeed('bitcoin', today, yesterday)

    print(news_feed.get())
