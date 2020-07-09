import praw
import re
import time
from googletrans import Translator
from datetime import datetime

reddit = praw.Reddit(
    client_id='********',
    client_secret ="********",
    username="********",
    password="********",
    user_agent="********"
) # account with access to subreddit you wanna copy

reddit2 = praw.Reddit(
    client_id='********',
    client_secret ="********",
    username="********",
    password="********",
    user_agent="********"
) # account with access to subreddit you wanna copy to

subreddit = reddit.subreddit("********") # subreddit you wanna copy
subreddit2 = reddit2.subreddit("********") # subreddit you wanna copy to
thisdict = {}
submissionlist=[]

for submission in subreddit.new(limit=1000): # can't go higher than 1000 because of api limits
        submissionlist.add(submission)

for submission in reversed(submissionlist):
        breakpoint=True
        submid=submission.id
        title = submission.title
        selftext = submission.selftext
        author=submission.author
        ts=int(submission.created_utc)
        ts2=datetime.utcfromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S'+" UTC")
        file1 = open("submissionids.txt", "r+")  # writes to file which submissions got copied so you can stop and resume at a later time without duplicates
        for line in file1:
            if (submid+"\n")==line:
                breakpoint=False
                break
        if breakpoint:
            file1.write(submid+"\n")
        file1.close() 
        if breakpoint:
            submission2=subreddit2.submit(title=title, selftext="Author: "+ str(submission.author)+"\n"+"\n"+str(ts2)+"\n"+"\n"+submission.id+"\n"+"\n"+submission.url+"\n"+"\n"+"Score: "+str(submission.score)+"\n"+"\n"+selftext)
            submission.comments.replace_more(limit=None)
            if submission.comments.list():
                for comment in submission.comments.list():
                    commid=str(comment.parent_id)
                    commid=commid[3:]
                    if commid==submission.id:
                        ts=int(comment.created_utc)
                        ts2=datetime.utcfromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S'+" UTC")
                        comment3=submission2.reply(str(comment.author)+"\n"+"\n"+str(ts2)+"\n"+"\n"+"Parent-Comment-ID: "+comment.parent_id+"\n"+"\n"+"Comment-ID: "+comment.id+"\n"+"\n"+comment.permalink+"\n"+"\n"+"Score: "+str(comment.score)+"\n"+"\n"+comment.body)
                        thisdict[comment.id]=comment3.id
                    else:
                        if commid in thisdict:
                            commid2=thisdict.get(commid)
                            comment2 = reddit2.comment(commid2)
                            ts=int(comment.created_utc)
                            ts2=datetime.utcfromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S'+" UTC")
                            comment4=comment2.reply(str(comment.author)+"\n"+"\n"+str(ts2)+"\n"+"\n"+"Parent-Comment-ID: "+comment.parent_id+"\n"+"\n"+"Comment-ID: "+comment.id+"\n"+"\n"+comment.permalink+"\n"+"\n"+"Score: "+str(comment.score)+"\n"+"\n"+comment.body)
                            thisdict[comment.id]=comment4.id
