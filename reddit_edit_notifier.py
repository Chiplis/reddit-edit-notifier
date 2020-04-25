from twilio.rest import Client
import praw
import time
import os

# Twilio credentials, see twilio.com/console
account_sid     =   None
auth_token      =   None
receiver_number =   None
sender_number   =   "+14155238886"


# Reddit credentials, see https://github.com/reddit-archive/reddit/wiki/oauth2
reddit_username         =   None
reddit_password         =   None
reddit_client_id        =   None
reddit_client_secret    =   None

# Client instantiation
twilio_client = Client(account_sid, auth_token)
reddit_client = praw.Reddit(
    user_agent='Reddit WhatsApp Edit Notifier - /u/' + reddit_username,
    client_id=reddit_client_id,
    client_secret=reddit_client_secret,
    username=reddit_username,
    password=reddit_password
)

def thread_files(folder):
    ls = []
    with os.scandir(folder) as entries:
        for entry in entries:
            ls.append(entry.name)
    return ls

def init_threads(folder):
    thread_map = {}
    for thread in thread_files(folder):
        with open(folder + "/" + thread, "r") as file:
            content = file.read()
            thread_map[thread] = content
    return thread_map

def update_file(folder, thread, new_content):
    with open(folder + "/" + thread, "w") as file:
        file.write(new_content)

def notify_user(url):
    twilio_client.messages.create(body=url, from_="whatsapp:" + sender_number, to="whatsapp:" + receiver_number)

def monitor_edits(folder):
    while True:
        thread_map = init_threads(folder)
        for thread, content in thread_map.items():
            new_content = reddit_client.submission(id=thread).selftext 
            if new_content != content:
                url = "https://www.reddit.com/comments/" + thread
                thread_map[thread] = new_content
                update_file(folder, thread, new_content)
                notify_user(url)
        time.sleep(10)

monitor_edits("threads")
