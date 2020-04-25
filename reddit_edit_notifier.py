import twilio.rest
import praw
import time
import os

# Twilio credentials, see twilio.com/console
twilio_sid      = None
twilio_token    = None
receiver_number = None
sender_number   = None

# Reddit credentials, see https://github.com/reddit-archive/reddit/wiki/oauth2
reddit_username         = None
reddit_client_id        = None
reddit_client_secret    = None
reddit_password         = None

# Clients instantiation
twilio_client = twilio.rest.Client(twilio_sid, twilio_token)
reddit_client = praw.Reddit(
    user_agent      = 'Reddit WhatsApp Edit Notifier - /u/' + reddit_username,
    client_id       = reddit_client_id,
    client_secret   = reddit_client_secret,
    username        = reddit_username,
    password        = reddit_password
)

# Return all file names in the specified folder as an array of strings
def thread_files(folder):
    ls = []
    with os.scandir(folder) as entries:
        for entry in entries:
            ls.append(entry.name)
    return ls

# Initialize a dictionary of threads, where each thread's ID is mapped to its content
def init_threads(folder):
    threads = {}
    for thread in thread_files(folder):
        with open(folder + "/" + thread, "r") as file:
            content = file.read()
            threads[thread] = content
    return threads

# Update a particular thread's corresponding file to prevent unnecessary messaging on reruns
def update_file(folder, thread, new_content):
    with open(folder + "/" + thread, "w") as file:
        file.write(new_content)

# Sends the specified number a WhatsApp message
def notify_user(message):
    twilio_client.messages.create(
        body    = message,
        from_   = "whatsapp:" + sender_number,
        to      = "whatsapp:" + receiver_number
    )

def monitor_edits(folder):
    while True:
        threads = init_threads(folder)
        for thread_id, content in threads.items():
            new_content = reddit_client.submission(id = thread_id).selftext 
            if new_content != content:
                message = "https://www.reddit.com/comments/" + thread_id
                threads[thread_id] = new_content
                update_file(folder, thread_id, new_content)
                notify_user(message)
        time.sleep(10)

monitor_edits("threads")
