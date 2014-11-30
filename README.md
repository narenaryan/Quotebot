Quotebot
========

A twitter bot that posts Famous quotes every day on Twitter without intervention of a human operator. 
The main difference between this bot and others is data posted is purely fetched by Spiders and stored in
MongoDB.

Twitter allows only 140 characters length of text,but quotes can be much longer.Inorder to overcome that issue ,if quote is converted into image it can be uploaded as a media file and serves the purpose.

So this project uses an API for converting text to Image,and then uploads it to Twitter.

Quotes will have the subject according to day in a month,means every 2nd of month Love Quotes will be posted,
3rd Inspiration quotes,etc.Daily Maximum 120 Quotes will be posted at maximum.For every 5 minutes,bot checks the
connection automatically when system is active and posts the Quote image.

Two APIs Twitter API,Img4free API are used to achieve the task.  

tweetit.py creates a class for encapsulating user details.
beforeact.py do all housekeeping task and sets every thing ready for Quotebot to run.
dayscats.pickle consists of mapping of month day -> category.

postlog.log stores all logs of posted quotes and also network statistics
