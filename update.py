'''
The heart of the QuoteBot
Here goes the actual thing.The tasks done here in following manner
1)Check the post limit
2)Fetch quote from database
3)Convert it into image(.png) using API 
4)Upload it to twitter

'''

#Imports for tweet and store

from tweetit import QUOTE

import datetime

from beforeact import red,mydb

import pickle,sys

from bson import ObjectId

import logging,requests

logging.basicConfig(filename='postlog.log',level=logging.DEBUG)

days_cats = pickle.load(open('dayscats.pickle','r'))

quote = QUOTE()

#credentials to be changed
qhandle = quote.get_handle()

def return_date():
	day_of_month = datetime.datetime.today().timetuple().tm_mday
	return day_of_month

def today_category():
	day = return_date()
	return days_cats[day]

#Creating categories set in redis which is used to Implement day category
def generate_quote_image(qs,qid):
	payload = {'text':qs,'font':'arial','color':'000000','size':20,'bcolor':'FFFFFF','type':'png'}
	result1 = requests.get('http://api.img4me.com',params=payload)
	result2 = requests.get(result1.text.encode('utf-8'))
	with open(qid+'.png','wb') as f:
		f.write(result2.content)
	return qid+'.png'


def give_quote():
	quote_id = red.spop(today_category())
	quote = (mydb[today_category()].find_one({'_id':ObjectId(quote_id)})['quote'].lstrip()).rstrip()
	author = mydb[today_category()].find_one({'_id':ObjectId(quote_id)})['author']
	message = quote+'\n---\n'+author
	try:
		filename = generate_quote_image(message,quote_id)
	except:
		red.sadd(today_category,details[quote_id])
		sys.exit()
	return locals()

def do_status():
	details = give_quote()
	try:
		qhandle.update_with_media(details['filename'])
		red.sadd('O'+today_category(),details['quote_id'])
		red.incr('today_balance')
	except:
		red.sadd(today_category,details[quote_id])
		sys.exit()

#Main program which runs the 
def run_it():
	#Stop posting if count is greater than 120
	if int(red.get('today_balance'))<int(red.get('per_day')) and int(red.get('today_or_yesterday')) == int(return_date()):
		do_status()
		logging.debug('Posted at %s'%(datetime.date.today().ctime()))
	elif red.get('today_or_yesterday') != return_date():
		red.set('today_balance',0)
		red.set('today_or_yesterday',return_date())
	else:
		sys.exit()

if __name__ == '__main__':
	run_it()




