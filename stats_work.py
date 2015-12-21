############################
#NOTE:
#	add one more row at the TOP of user_bought_hisotry file
# 	user_id item_id create_id
#
############################

import csv
import pandas as pd
from collections import defaultdict
import json
import multiprocessing as mp

#read in the matchset
matchset = []
with open("dim_fashion_matchsets(new).txt") as matchfile:
	reader = csv.reader(matchfile, delimiter=' ')
	for row in reader:
		matchset.append(row)

#clean the matchset
#now every item of matchset is of the form:
#['111111','222222','333333,444444','555555']
matchset = [item[1].split(";") for item in matchset]

#further process the matchest
#now every item(match_rule) of matchset is of the form:
#['111111','222222',('333333','444444'),'555555']
for match_rule in matchset:
	for index, item in enumerate(match_rule):
		if ',' in item:
			match_rule[index] = tuple(item.split(','))

#read in the user bought history
history = pd.read_csv("user_bought_history(new).txt",sep=' ')

#unique_users is of type: array
unique_users = history.user_id.unique()

# match_rule is the of the form:
# ['111111','222222',('333333','444444'),'555555']
# bought_history is the of the form:
# [11111,22222,33333,44444]
def is_fit(match_rule, bought_history):
	for item in match_rule:
		#item like ('222','333')
		if isinstance(item, tuple):
			if not filter(lambda x: int(x) in bought_history, item):
				return False
		else:
			#item like '11111'
			if not int(item) in bought_history:
				return False
	return True

size_all = len(unique_users)

#the whole set is divided into 15 groups
groups = 15

#size of each group
size_group = size_all/groups

def generate_expert_user(group):

	#expert user
	expert_user = defaultdict(int)

	#the size of the last group is not necessarily the same as previous ones
	if group == (groups-1):
		start = group*size_group
		#the index of end is the total size
		end = size_all
	else:
		start = group*size_group
		end = start+size_group

	for index, user in enumerate(unique_users[start:end]):
		print "user",(index+1+start),":",user,"Now expert_user_number:",len(expert_user)
		user_bought_history = history[history['user_id']==user].item_id.tolist()

		for match_rule in matchset:
			if is_fit(match_rule, user_bought_history):
				expert_user[user] += 1
				print "AWESOME! user",user,"has match"
				print "Now expert_user_number:",len(expert_user)

	print "size:",len(expert_user)
	print expert_user

	with open("result|"+group,"w") as myfile:
		json.dump(expert_user, myfile)

	return "success"

#create a list to store all the processes
jobs = []

for group in range(groups):
	#create process to run target method
	p = mp.Process(target=generate_expert_user, args=(group,))
	jobs.append(p)
	print "group",group,"start"
	p.start()

