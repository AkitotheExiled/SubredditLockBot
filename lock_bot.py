import praw
from configparser import ConfigParser
from datetime import date
import requests, requests.auth
import json


class Lock_Bot():

    def __init__(self):
        self.user_agent = "LockBot/V1.0 by ScoopJr"
        print('Starting up...', self.user_agent)
        CONFIG = ConfigParser()
        CONFIG.read('config.ini')
        self.user = CONFIG.get('main', 'USER')
        self.password = CONFIG.get('main', 'PASSWORD')
        self.client = CONFIG.get('main', 'CLIENT_ID')
        self.secret = CONFIG.get('main', 'SECRET')
        self.day = CONFIG.get('main', 'DAY')
        self.subreddit = CONFIG.get('main', 'SUBREDDIT')
        self.token_url = "https://www.reddit.com/api/v1/access_token"
        self.token = ""
        self.t_type = ""
        self.reddit = praw.Reddit(client_id=self.client,
                             client_secret=self.secret,
                             password=self.password,
                             user_agent=self.user_agent,
                             username=self.user)
        self.parse = requests.get('https://www.hebcal.com/hebcal/?v=1&cfg=json&maj=on&min=on&mod=on&nx=on&year=now&month=x&ss=on&mf=on&c=off&geo=none&m=50&s=on').json()
        self.holidays = []
        for item in self.parse['items']:
            self.holidays.append(item['date'])


    def get_token(self):
        client_auth = requests.auth.HTTPBasicAuth(self.client, self.secret)
        post_data = {'grant_type': 'password', 'username': self.user, 'password': self.password}
        headers = {'User-Agent': self.user_agent}
        response = requests.Session()
        response2 = response.post(self.token_url, auth=client_auth, data=post_data, headers=headers)
        self.token = response2.json()['access_token']
        self.t_type = response2.json()['token_type']

    def check_date(self):
        today = date.today()
        if today.isoweekday() == self.day or today.isoformat() in self.holidays:
            return True
        else:
            return False

    def lock_subreddit(self):
        if self.reddit.subreddit(self.subreddit).mod.settings()['subreddit_type'] == 'public':
            return self.reddit.subreddit(self.subreddit).mod.update(subreddit_type='restricted', spam_comments='all')
        elif self.reddit.subreddit(self.subreddit).mod.settings()['subreddit_type'] == 'restricted':
            return print('Your subreddit:', self.subreddit, 'is already restricted.')

    def unlock_subreddit(self):
        if self.reddit.subreddit(self.subreddit).mod.settings()['subreddit_type'] == 'restricted':
            return self.reddit.subreddit(self.subreddit).mod.update(subreddit_type='public', spam_comments='low')
        elif self.reddit.subreddit(self.subreddit).mod.settings()['subreddit_type'] == 'public':
            return print('Your subreddit:', self.subreddit, 'is already public.')

if __name__ == '__main__':
    bot = Lock_Bot()
    if bot.check_date():
        bot.unlock_subreddit()
    else:
        bot.lock_subreddit()

