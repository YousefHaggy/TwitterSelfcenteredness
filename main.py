
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
    tweetCount=1
    selfCenteredCount=0;
    for tweet in tweets:
        tweetCount+=1
        sentences=tweet.text_content().split(".")
        find=False;
        for sentence in sentences:
	        if sentence.find("You always have the option to delete your Tweet location history")!=-1 or sentence.find("You can add location information to your Tweets, such as your city or precise location")!=-1:
	            break;
	        words=sentence.split()
	        for word in words:
	            if word.lower()=="I" or word.lower()=="my" or word.lower()=="me":
	                selfCenteredCount+=1
	                find=True
	                break;
	        if find:
	            break;
    return(jsonify({"Self-Centeredness":str(selfCenteredCount/tweetCount*100)+"%"}))



