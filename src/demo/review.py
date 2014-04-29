import io,json,string

spamStores = ["koCfyexzjjF3pZrzijlL3g","hAq4y3FK6tRbjfjvfXAaww","ZZlMGUiKZNiDyPLmra7RZQ","frZdH7hTGIs7nykH4jeIPA","Tg0D45xHJBN0jOMq_v04XA","x0NOgX6P4x-82cC0kcO1hg","0yBs5wbVw9gTIDe9Z-rMTg","jHte0SjUldZeDDZ5py0ZhA","d87fxJ47AzTlREZCnUmaFA","oMycF1cQgR1UVkafXfof7A","IkSF5GEHcl7DePGlXksl5A","pSiR8m18iick2D7TFdmb-Q","fmuj7u1gflmEjW-h0v9bwg","SPBZxmt8_nT30rNVnKHYKA","0vzZ_Bcb02rJljeMU9XkBw","UedVu1tCV_Q3twZZtwtl8Q","vA8T8QXh78iSXhxShLNgQA","SkcccvAydbt5zlQI0EUL2g","zp713qNhx8d9KCJJnrw1xA","cc9KFNrcY9gA7t9D1a3FpA"]

userNameId = {}
with open("yelp_academic_dataset_user.json", "r") as file:
	for line in file:
		line = line[:-1]
		name = json.loads(line)["name"]
		userId = json.loads(line)["user_id"]
		userNameId.update({userId:name})

#print userNameId


reviewDic = {}
allStores = ""
with open("restaurant_grouped_ranked_reviews.json", "r") as file:
	for line in file:
		line = line[:-1]
		l = json.loads(line)
		business_id = l["business_id"]
		count = 0
		if business_id in spamStores:
			if business_id not in reviewDic.keys():
				revs = []
				
				#print json.dumps(json.loads(line)["text"].encode('utf-8'))
				revs.append('{"userName":"'+userNameId[l["user_id"]]+'","review":'+json.dumps(l["text"].encode('utf-8'))+"}")
				
			elif business_id in reviewDic.keys():
				revs.append('{"userName":"'+userNameId[l["user_id"]]+'","review":'+json.dumps(l["text"].encode('utf-8'))+"}")
			reviewDic.update({l["business_id"]:revs})
			#print count,revs

#print reviewDic["VZYMInkjRJVHwXVFqeoMWg"]
# for key in reviewDic.keys():
# 	print reviewDic[key]
	# #print key
	# reviews = ""
	# for value in range(len(reviewDic[key])):
	# 	#print value
	# 	reviews = reviews+","+reviewDic[key][value]
	#print reviews
	#allStores = '"'+key+'":'+reviewDic[key]+","+allStores

#print allStores

#print allStores






with open("r.js","w+") as wFile:
	wFile.write("var REVIEWS = {")
	for key in reviewDic.keys():
		wFile.write('"'+key+'":')
		
		
		wFile.write('[')
		for value in range(len(reviewDic[key])):
			#wFile.write(string.replace(reviewDic[key][value],'"',"'").encode('utf-8'))
			#print json.dumps(reviewDic[key][value])
			#print reviewDic[key][value]
			# wFile.write('{')
			# wFile.write(reviewDic[key][value])
			# wFile.write(':')
			wFile.write(reviewDic[key][value])
			wFile.write(',')
		wFile.write('],')

		# wFile.write('","'.join(reviewDic[key]).encode('utf-8'))
		# wFile.write(",")
	wFile.write("}")

