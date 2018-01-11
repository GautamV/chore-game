from flask import Flask, request, redirect
from twilio.twiml.messaging_response import MessagingResponse
from datetime import datetime, timedelta
import db_utils
import os

app = Flask(__name__)

@app.route("/sms", methods=['GET', 'POST'])
def incoming_sms():

	body = request.values.get('Body', None)
	words = body.split()

	if len(words) == 0:
		return 

	if words[0] == 'add':
		if len(words) != 3:
			resp = MessagingResponse()
			resp.message("wrong command syntax")
			return str(resp)

		if words[1] == 'chore':
			return add_chore(words[2])
		elif words[1] == 'user':
			return add_user(words[2])
		elif words[1] == 'instance':
			return add_instance(words[2])
		else:
			resp = MessagingResponse()
			resp.message("i'm not sure what you're tryong to add")
			return str(resp)

	elif words[0] == 'stats':
		if len(words) == 2:
			return get_stats(words[1])
		elif len(words) == 3: 
			return get_stats_by_date(words[1], words[2])
		else:
			resp = MessagingResponse()
			resp.message("wrong command syntax")
			return str(resp)

	else: 
		resp = MessagingResponse()
		resp.message("i have no idea what you're saying")
		return str(resp)

def add_chore(chore):
	db_utils.add_chore(chore)
	resp = MessagingResponse()
	resp.message("added chore {0}".format(chore))
	return str(resp)

def add_user(name):
	number = request.values.get('From', None)
	db_utils.add_user(name, number)
	resp = MessagingResponse()
	resp.message("added user {0} with number {1}".format(name, number))
	return str(resp)

def add_instance(chore):
	number = request.values.get('From', None)

	data = db_utils.get_user_by_phone(number)
	if data is None:
		resp = MessagingResponse()
		resp.message("you are not a registered user. please register to play the chore game")
		return str(resp)
	user_id, user_name = data

	data = db_utils.get_chore_id_by_name(chore)
	if data is None:
		resp = MessagingResponse()
		resp.message("there is no chore called \"{0}\". please add this chore first".format(chore))
		return str(resp)
	chore_id = data[0]

	db_utils.add_instance(user_id, chore_id)
	resp = MessagingResponse()
	resp.message("recorded that {0} did {1}. good job!".format(user_name, chore))
	return str(resp)

def get_stats(chore):
	if chore == 'all':
		data = db_utils.get_chores_stats()
	else: 
		data = db_utils.get_chore_stats(chore)
	if data is None or len(data) == 0: 
		resp = MessagingResponse()
		resp.message("no data available")
		return str(resp)

	if chore == 'all':
		dic = {}
		for row in data:
			if row[1] in dic: 
				dic[row[1]].append((row[0], row[2]))
			else:
				dic[row[1]] = [(row[0], row[2])]
		s = "stats\n\n"
		for k, v in dic.iteritems(): 
			s += "Stats for {0}:\n".format(k)
			for row in v: 
				s += "{0}: {1} \n".format(row[0], row[1])
			s += "\n"

	else: 
		s = "stats\n\n"
		s += "Stats for {0}:\n".format(chore)
		for row in data: 
			s += "{0}: {1} \n".format(row[0], row[1])

	resp = MessagingResponse()
	resp.message(s)
	return str(resp)

def get_stats_by_date(chore, days):
	try: 
		delta = int(days)
	except:
		resp = MessagingResponse()
		resp.message("third argument must be an integer number of days")
		return str(resp)

	end = datetime.utcnow()
	start = end - timedelta(days=delta)

	if chore == 'all':
		data = db_utils.get_chores_stats(start_date=start, end_date=end)
	else: 
		data = db_utils.get_chore_stats(chore, start_date=start, end_date=end)
	if data is None or len(data) == 0: 
		resp = MessagingResponse()
		resp.message("no data available")
		return str(resp)

	if chore == 'all':
		dic = {}
		for row in data:
			if row[1] in dic: 
				dic[row[1]].append((row[0], row[2]))
			else:
				dic[row[1]] = [(row[0], row[2])]
		s = "stats for last {0} days\n\n".format(days)
		for k, v in dic.iteritems(): 
			s += "Stats for {0}:\n".format(k)
			for row in v: 
				s += "{0}: {1} \n".format(row[0], row[1])
			s += "\n"

	else: 
		s = "stats for last {0} days\n\n".format(days)
		s += "Stats for {0}:\n".format(chore)
		for row in data: 
			s += "{0}: {1} \n".format(row[0], row[1])

	resp = MessagingResponse()
	resp.message(s)
	return str(resp)

if __name__ == "__main__":
	port = int(os.environ.get('PORT', 5000))
	app.run(port=port)

