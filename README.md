tweetful
========

Part of Thinkful curriculum to demonstrate Oauth and API utilization.  

Command line app to interface with Twitter.

example:
python tweetful.py tweet 'This is a tweet'
    Will make a tweet to authorized account: 'This is a tweet'
    
python tweetful.py trends 2487889
    Will return latest trending tweets (Top 10) from that WOEID (location)
    trend -h --> to see link to lookup WOEID



Must create the following file and add to directory:
Secret.py
-- contents below ---
CLIENT_KEY = "insert key here"
CLIENT_SECRET = "insert secret here"
