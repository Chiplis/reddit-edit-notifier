# reddit-edit-notifier

The script will monitor your chosen Reddit threads, and send you a link via WhatsApp to acccess them whenever they are edited.

## Requirements:
* [Python 3](https://www.python.org/])
* [PRAW - Python Reddit API Wrapper](https://praw.readthedocs.io/en/latest/)
* [Twilio's Python API](https://www.twilio.com/docs/libraries/python)

## Usage:
* Configure the script with your Reddit/Twilio/WhatsApp credentials (relevant links shown in the script itself)
* Create a blank file named the same as your chosen thread's ID (e.g https://www.reddit.com/r/AskReddit/comments/g6ydky/covid19_megathread_week_of_april_23april_29 -> **g6ydky**) in the "threads" folder.
* Run the script! It should send you a WhatsApp link the first time its executed, and every time any of the monitored threads is edited.


An thread is already included to test that everything works correctly.
