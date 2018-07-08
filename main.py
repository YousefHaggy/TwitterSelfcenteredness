
# A very simple Flask Hello World app for you to get started with...

from flask import Flask, jsonify, request
import requests
import time
from lxml import html
app = Flask(__name__)

@app.route("/")
def _scrape():
    my_session = requests.session()
    username=request.args.get('username');
    page = my_session.get("https://twitter.com/"+username)

    tree = html.fromstring(page.text.encode("ascii","ignore"))

    tweets = tree.xpath("//li//p")
    tweetCount=0
    selfCenteredCount=0;
    for tweet in tweets[:len(tweets)-1]:
        tweetCount+=1
        sentences=tweet.text_content().split(".")
        find=False;
        for sentence in sentences:
	        words=sentence.split()
	        for word in words:
	            if word.lower()=="i" or word.lower()=="my" or word.lower()=="me":
	                selfCenteredCount+=1
	                find=True
	                break;
	        if find:
	            break;
    if tweetCount==0:
        return(jsonify({"result": "no tweets on this acc!"}))
    return(jsonify({"Self-Centeredness":str(selfCenteredCount/tweetCount*100)+"%", "Github":"https://github.com/YousefHaggy/TwitterSelfcenteredness"}))
