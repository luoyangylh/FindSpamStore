import io,json

allStores = ""
with open("restaurant.json", "r") as file:
	for line in file:
		line = line[:-1]
		allStores = '"'+json.loads(line)["business_id"].encode('utf-8')+'":'+line+","+allStores

#print allStores
with open("store.js","w") as wFile:
	wFile.write("var restaurantList = {")
	wFile.write(allStores)
	wFile.write("}")
