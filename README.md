# SubredditLockBot
A bot that locks your subreddit on a specific day and preventing posting and comments.


## Installing required packages
```
pip install -r requirements.txt
```

### config.ini
```
[main]
USER = yourusername
PASSWORD= yourpassword
CLIENT_ID= yourclientid
SECRET= yoursecret
DAY=6
SUBREDDIT=yoursubreddit
DEBUG=False
```

#### DAY
The days are as follows,
```
1 = Monday
2 = Tuesday
3 = Wednesday
4 = Thursday
5 = Friday
6 = Saturday
7 = Sunday
```
##### Setting up automoderator in conjuction for this script
https://www.reddup.co/r/AutoModerator/comments/1z7rlu/now_available_for_testing_wikiconfigurable
