import praw
from configparser import ConfigParser
from datetime import date, datetime
import requests, requests.auth
from apscheduler.schedulers.background import BackgroundScheduler
import logging

class Lock_Bot():

    def __init__(self):
        self.user_agent = "LockBot/V1.1 by ScoopJr"
        print('Starting up...', self.user_agent)
        CONFIG = ConfigParser()
        CONFIG.read('config.ini')
        self.user = CONFIG.get('main', 'USER')
        self.password = CONFIG.get('main', 'PASSWORD')
        self.client = CONFIG.get('main', 'CLIENT_ID')
        self.secret = CONFIG.get('main', 'SECRET')
        self.day = int(CONFIG.get('main', 'DAY'))
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
        self.holiday_title = []
        for item in self.parse['items']:
            self.holiday_title.append(item['title'])
            self.holidays.append(item['date'])
        self.debug = CONFIG.getboolean('main', 'DEBUG')



    def get_token(self):
        client_auth = requests.auth.HTTPBasicAuth(self.client, self.secret)
        post_data = {'grant_type': 'password', 'username': self.user, 'password': self.password}
        headers = {'User-Agent': self.user_agent}
        response = requests.Session()
        response2 = response.post(self.token_url, auth=client_auth, data=post_data, headers=headers)
        self.token = response2.json()['access_token']
        self.t_type = response2.json()['token_type']

    def return_title(self):
        today = date.today()
        self.hol_check = False
        self.hol_index = None
        for dt in self.holidays:
            date_time = datetime.strptime(dt, '%Y-%m-%d').date()
            if today == date_time:
                self.hol_check = True
                self.hol_index = self.holidays.index(dt)
        if (today.isoweekday() == self.day) & self.hol_check:
            return 'manually-closed day and ' + self.holiday_title[self.hol_index]
        elif today.isoweekday() == self.day:
            return 'manually-closed day'
        elif self.hol_check:
            return self.holiday_title[self.hol_index]





    def check_date(self):
        today = date.today()
        date_holiday = False
        for dt in self.holidays:
            date_time = datetime.strptime(dt, '%Y-%m-%d').date()
            if today == date_time:
                date_holiday = True
        if today.isoweekday() == self.day or date_holiday:
            return False
        else:
            return True

    def lock_subreddit(self):
        if self.reddit.subreddit(self.subreddit).mod.settings()['subreddit_type'] == 'public':
            print('Your subreddit is now locked. Today is ' + self.return_title() + '.')
            return self.reddit.subreddit(self.subreddit).mod.update(subreddit_type='restricted', spam_comments='all')
        elif self.reddit.subreddit(self.subreddit).mod.settings()['subreddit_type'] == 'restricted':
            return print('Your subreddit:', self.subreddit, 'is already restricted. Today is ' + self.return_title() + '.')

    def unlock_subreddit(self):
        if self.reddit.subreddit(self.subreddit).mod.settings()['subreddit_type'] == 'restricted':
            print('Your subreddit is now unlocked.')
            return self.reddit.subreddit(self.subreddit).mod.update(subreddit_type='public', spam_comments='low')
        elif self.reddit.subreddit(self.subreddit).mod.settings()['subreddit_type'] == 'public':
            return print('Your subreddit:', self.subreddit, 'is already public.')

    def run_bot(self):
        if self.check_date():
            return self.unlock_subreddit()
        else:
            return self.lock_subreddit()

if __name__ == '__main__':
    bot = Lock_Bot()
    if bot.debug:
        logging.basicConfig()
        logging.getLogger('apscheduler').setLevel(logging.DEBUG)
    sched = BackgroundScheduler()
    sched.add_job(bot.run_bot,'cron',hour='0,12')
    sched.start()
    input('The bot is running in the background and will run every dat at 12:00am. Press enter to exit.')
    sched.shutdown()



