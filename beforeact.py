#Code for setting all intial values in a proper manner to start bot
import redis
import pickle
from pymongo import MongoClient
import datetime

#creating mongoclient where quotes are stored in my db
mydb = MongoClient('localhost')['goodread'] 

#Create a redis instance
red = redis.Redis()
red.set('per_day',120)
red.set('today_balance',0)
red.set('today_or_yesterday',datetime.datetime.today().timetuple().tm_mday)

#Storing category names in redis for future use
for i in mydb.collection_names():
	if i!='system.indexes':
		for cur in mydb[i].find():
			red.sadd(i,str(cur['_id']))
		red.sadd('cats',i)

#Creating a dictionary for mapping category to day in a month
days_cats = {i+1:k for i,k in enumerate(red.smembers('cats'))}

#Writing that mapping to a pickle file 
with open('dayscats.pickle','wb') as f:
	pickle.dump(days_cats,f)


