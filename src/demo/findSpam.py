import io,json

storeList = {}
allList = {}

with open("restaurant.json", "r") as file:
#	c =0
	for line in file:
		line = line[:-1]
		content = {}
		content.update({"diff":json.loads(line)["our_score"] - json.loads(line)["stars"]})
		content.update({"our_score":json.loads(line)["our_score"]})
		content.update({"original_score":json.loads(line)["stars"]})
		content.update({"data":json.loads(line)})
		storeList.update({json.loads(line)["business_id"]:json.loads(line)["our_score"] - json.loads(line)["stars"]})
		allList.update({json.loads(line)["business_id"]:content})
		# c+=1
		# if c>50:
		# 	break
#print allList["Mx4VdkKKavzans54VwMP1Q"]

#print allStores
with open("spamList.js","w+") as wFile:
	wFile.write("var spamList = [")
	ranked = sorted(storeList.iteritems(), key=lambda x: float(x[1])) 
	#print ranked[0][0],ranked[0][1]
	for i in range(len(ranked)):
		string = '{"name":"'+allList[ranked[i][0]]["data"]["name"].encode('utf-8')+'","business_id":"'+str(ranked[i][0])+'","diff":'+str(ranked[i][1])+"},"
		wFile.write(string)
	wFile.write("]")


for i in range(20):
	print allList[ranked[i][0]]["data"]["name"].encode('utf-8')
	print "Official: ",allList[ranked[i][0]]["data"]["stars"]
	print "Our Score: ",allList[ranked[i][0]]["data"]["our_score"]
	print "Diff: ",ranked[i][1]
	print allList[ranked[i][0]]["data"]["full_address"]
	print "----"

with open("spamStoresName.txt","w+") as wFile:
	wFile.write("[")
	for i in range(20):
		wFile.write('"')
		wFile.write(allList[ranked[i][0]]["data"]["business_id"].encode('utf-8'))
		wFile.write('",')
	wFile.write("]")

