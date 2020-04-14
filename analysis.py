import matplotlib
matplotlib.use('TkAgg')
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from tweepy import API
from pandastable import Table, TableModel
from tweepy import Cursor
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
from tweepy import TweepError
from textblob import TextBlob
from PIL import ImageTk
import PIL.Image
import credentials
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import re
try:
    import Tkinter as tk
except:
    import tkinter as tk
from PIL import ImageTk, Image
from tkinter import *

class Error(Exception):
   pass
class ValueTooLargeError(Error):
   pass

class Demo:
    def __init__(self, top):
        self.name=""
        la=Label(top, text="")
        la.pack()
        la=Label(top, text="")
        la.pack()
        frame_e = Frame(top)
        self.t_name = StringVar()
        self.t_count=IntVar()
        la=Label(frame_e, text="Enter Twitter username to be searched")
        la.pack()
        text = Entry(frame_e, textvariable=self.t_name, bg="white",justify=CENTER)
        text.pack()
        text.focus_force()
        la=Label(frame_e, text="No. of tweets you want deal with")
        la.pack()
        text = Entry(frame_e, textvariable=self.t_count, bg="white",justify=CENTER)
        text.pack()
        text.focus_force()
        la=Label(frame_e, text="Value of no. tweets should be less than 3200 and Username should be valid")
        la.pack()
        frame_e.pack()
        nameButton = Button(frame_e, text="Accept", command=self.Naming)
        nameButton.pack(side=BOTTOM, anchor=S)
        la=Label(top, text="")
        la.pack()
        la=Label(top, text="")
        la.pack()
        la=Label(top, text="-:Project By:-",font='Helvetica 10 bold')
        la.pack()
        la=Label(top, text="18BCE070-Gaurav Vaghasiya")
        la.pack()
        la=Label(top, text="18BCE071-Gaurav Parekhiya")
        la.pack()
        la=Label(top, text="18BCE089-Pranav Kansagra")
        la.pack()
    def Naming(self):
    
        self.name = self.t_name.get()
        self.count=self.t_count.get()
        root.destroy()

class TwitterClient():
    def __init__(self, twitter_user=None):
        self.auth = TwitterAuthenticator().authenticate_twitter_app()
        self.twitter_client = API(self.auth)

        self.twitter_user = twitter_user

    def get_twitter_client_api(self):
        return self.twitter_client

    def get_user_timeline_tweets(self, num_tweets):
        tweets = []
        for tweet in Cursor(self.twitter_client.user_timeline, id=self.twitter_user).items(num_tweets):
            tweets.append(tweet)
        return tweets

    def get_friend_list(self, num_friends):
        friend_list = []
        for friend in Cursor(self.twitter_client.friends, id=self.twitter_user).items(num_friends):
            friend_list.append(friend)
        return friend_list

    def get_home_timeline_tweets(self, num_tweets):
        home_timeline_tweets = []
        for tweet in Cursor(self.twitter_client.home_timeline, id=self.twitter_user).items(num_tweets):
            home_timeline_tweets.append(tweet)
        return home_timeline_tweets

class TwitterAuthenticator():

    def authenticate_twitter_app(self):
        auth = OAuthHandler(credentials.CONSUMER_KEY, credentials.CONSUMER_SECRET)
        auth.set_access_token(credentials.ACCESS_TOKEN,credentials.ACCESS_TOKEN_SECRET)
        return auth

class TwitterStreamer():
    
    def __init__(self):
        self.twitter_autenticator = TwitterAuthenticator()    

    def stream_tweets(self, fetched_tweets_filename, hash_tag_list):
       
        listener = TwitterListener(fetched_tweets_filename)
        auth = self.twitter_autenticator.authenticate_twitter_app() 
        stream = Stream(auth, listener)

        stream.filter(track=hash_tag_list)

class TwitterListener(StreamListener):
    def __init__(self, fetched_tweets_filename):
        self.fetched_tweets_filename = fetched_tweets_filename

    def on_data(self, data):
        try:
            print(data)
            with open(self.fetched_tweets_filename, 'a') as tf:
                tf.write(data)
            return True
        except BaseException as e:
            print("Error on_data %s" % str(e))
        return True
          
    def on_error(self, status):
        if status == 420:
            return False
        print(status)


class TweetAnalyzer():
    def clean_tweet(self, tweet):
        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())

    def analyze_sentiment(self, tweet):
        analysis = TextBlob(self.clean_tweet(tweet))
        
        if analysis.sentiment.polarity > 0:
            return 1
        elif analysis.sentiment.polarity == 0:
            return 0
        else:
            return -1

    def tweets_to_data_frame(self, tweets):
        df = pd.DataFrame(data=[tweet.text for tweet in tweets], columns=['tweets'])

        df['id'] = np.array([tweet.id for tweet in tweets])
        df['len'] = np.array([len(tweet.text) for tweet in tweets])
        df['date'] = np.array([tweet.created_at for tweet in tweets])
        df['source'] = np.array([tweet.source for tweet in tweets])
        df['likes'] = np.array([tweet.favorite_count for tweet in tweets])
        df['retweets'] = np.array([tweet.retweet_count for tweet in tweets])

        return df
class mclass:
    def __init__(self,  window):
        self.window = window
        la=Label(window, text="Some Statistical Data",font='Helvetica 18 bold',fg='blue')
        la.pack()
        la=Label(window, text="")
        la.pack()
        la=Label(window, text="")
        la.pack()
        fl=Frame(window)
        la=Label(fl, text="Mean Length of tweets:-",font='Helvetica 10 bold')
        la.pack(side='left')
        la=Label(fl, text=int(np.mean(df['len'])))
        la.pack(side='left')
        fl.pack()
        fl=Frame(window)
        la=Label(fl, text="Maximum no. of likes:-",font='Helvetica 10 bold')
        la.pack(side='left')
        la=Label(fl, text=np.max(df['likes']))
        la.pack(side='left')
        fl.pack()
        fl=Frame(window)
        la=Label(fl, text="Maximum no. of retweets:-",font='Helvetica 10 bold')
        la.pack(side='left')
        la=Label(fl, text=np.max(df['retweets']))
        la.pack(side='left')
        fl.pack()
        la=Label(window, text="")
        la.pack()
        la=Label(window, text="")
        la.pack()
        fl=Frame(window)
        self.button = Button (fl, text="Display likes vs date ", command=self.plot1,activebackground='blue')
        self.button.pack(side='left')
        la=Label(fl, text=" ")
        la.pack(side='left')
        self.button = Button (fl, text="Display length vs date", command=self.plot2,activebackground='blue')
        self.button.pack(side='left')
        la=Label(fl, text=" ")
        la.pack(side='left')
        self.button = Button (fl, text="Display retweets vs date", command=self.plot3,activebackground='blue')
        self.button.pack(side='left')
        la=Label(fl, text=" ")
        la.pack(side='left')
        self.button = Button (fl, text=" Display Combine graph", command=self.plot,activebackground='blue')
        self.button.pack(side='left')
        fl.pack()
        la=Label(window, text="")
        la.pack()
        la=Label(window, text="")
        la.pack()
        la=Label(window, text=("-:Users {0} last {1} tweets:-".format(D.name,D.count)),font='Helvetica 10 bold',fg='blue')
        la.pack()
        self.button = Button (window, text="Close", command=self.quit,activebackground='blue')
        self.button.pack()
        self.TestApp(df).mainloop()
    def quit(self):
       window.destroy()
    def plot (self):
        fig = plt.figure("Tweet analyzer")
        time_likes = pd.Series(data=df['len'].values, index=df['date'])
        time_likes.plot(figsize=(16, 4), label="length",legend=True)
        time_likes = pd.Series(data=df['likes'].values, index=df['date'])
        time_likes.plot(figsize=(16, 4), label="likes", legend=True)
        time_retweets = pd.Series(data=df['retweets'].values, index=df['date'])
        time_retweets.plot(figsize=(16, 4), label="retweets", legend=True)
        plt.show()
    def plot1(self):
        fig = plt.figure("Tweet analyzer:Likes vs Date")
        time_likes = pd.Series(data=df['likes'].values, index=df['date'])
        time_likes.plot(figsize=(16, 4), label="likes", legend=True)
        plt.show()
    def plot2(self):
        fig = plt.figure("Tweet analyzer:Length vs Date")
        time_likes = pd.Series(data=df['len'].values, index=df['date'])
        time_likes.plot(figsize=(16, 4), label="length",legend=True)
        plt.show()
    def plot3(self):
        fig = plt.figure("Tweet analyzer:Retweets vs Date")
        time_retweets = pd.Series(data=df['retweets'].values, index=df['date'])
        time_retweets.plot(figsize=(16, 4), label="retweets", legend=True)
        plt.show()
    class TestApp(Frame):
        def __init__(self, parent=None):
            self.parent = parent
            Frame.__init__(self)
            self.main = self.master
            self.main.overrideredirect(True)
            self.main.geometry("{0}x{1}+0+0".format(self.main.winfo_screenwidth(), self.main.winfo_screenheight()))
            self.main.focus_set()  # <-- move focus to this widget
            self.main.bind("<Escape>", lambda e: e.widget.quit())
            self.main.title('Tweets records')
            f = Frame(self.main)
            f.pack(fill=BOTH,expand=1)
            self.table = pt = Table(f, dataframe=df.head(D.count),
                                showtoolbar=False, showstatusbar=True)
            pt.show()
            return
 
if __name__ == '__main__':
    while True:
        try:
            root = Tk()
            root.title("Twitto to get username")
            la=Label(root,text="Twitter Sentiment Analysis",font='Helvetica 18 bold',fg='blue')
            la.pack()
            root.overrideredirect(True)
            root.geometry("{0}x{1}+0+0".format(root.winfo_screenwidth(), root.winfo_screenheight()))
            root.focus_set()  # <-- move focus to this widget
            root.bind("<Escape>", lambda e: e.widget.quit())
            path = "Aaron.jpg"
            img = ImageTk.PhotoImage(PIL.Image.open(path))
            panel = tk.Label(root, image = img)
            panel.pack(side = "top", fill = "both", expand = "no")
            D=Demo(root)
            root.mainloop()
            if(D.count>3200):
                raise ValueTooLargeError
            twitter_client = TwitterClient()
            tweet_analyzer = TweetAnalyzer()

            api = twitter_client.get_twitter_client_api()
            alltweets = []	
            new_tweets = api.user_timeline(screen_name =D.name,count=200)
            alltweets.extend(new_tweets)
            oldest = alltweets[-1].id - 1
            while len(new_tweets) > 0:
                new_tweets = api.user_timeline(screen_name = D.name,count=200,max_id=oldest)
                alltweets.extend(new_tweets)
                oldest = alltweets[-1].id - 1
            df = tweet_analyzer.tweets_to_data_frame(alltweets)
            df['sentiment'] = np.array([tweet_analyzer.analyze_sentiment(tweet) for tweet in df['tweets']])
            window= Tk()
            window.title("Tweets Analysis")
            window.overrideredirect(True)
            window.geometry("{0}x{1}+0+0".format(window.winfo_screenwidth(), window.winfo_screenheight()))
            window.focus_set()  # <-- move focus to this widget
            window.bind("<Escape>", lambda e: e.widget.quit())
            start= mclass (window)
            window.mainloop()
            break
        except ValueTooLargeError:
            print("value less then 3200")
            print()
        except TweepError:
            print("Valid Username should be entered and net should be connected")
            print()
        except:
            print("Value should be entered in username")
            print()
