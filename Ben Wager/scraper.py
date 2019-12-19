import requests, json, os
from math import floor
from time import time
from shutil import rmtree

link = "https://www.reddit.com/r/askreddit.json"
req = requests.get(link, headers={"User-agent":"RedBot 0.1"}).text

data = json.loads(req)["data"]["children"]
start_time = time()

def getScore(score):
	if score >= 1000:
		score /= 1000
		score = round(score, 1)
		return str(score)+"k"
	return str(score)

def getTime(timeScore):
	divider = []
	if timeScore < 60:
		divider = [1, "second"]
	elif timeScore < 3600:
		divider = [60, "minute"]
	elif timeScore < 86400:
		divider = [3600, "hour"]
	elif timeScore < 31536000:
		divider = [86400, "day"]
	else: divider = [31536000, "year"]


	return str(int(round(timeScore/divider[0], 0)))+" "+divider[1]+("s" if not round(timeScore/divider[0], 0) == 1 else "")

if os.path.exists("Outputs"):
	rmtree("Outputs")
os.makedirs("Outputs")

for question in data:
	question = question["data"]
	questionData = {}

	print("ID: ["+question["id"]+"]")
	print("Asked by u/"+question["author"]+",")
	print(question["title"])

	questionData["title"] = question["title"]
	questionData["id"] = question["id"]

	print(getScore(question["score"]) + " points\n")
	questionData["score"] = getScore(question["score"])
	questionData["author"] = question["author"]

	questionlink = question["url"][0:-1]+".json"
	questionData["url"] = question["url"]
	questionData["created"] = getTime(start_time-question["created_utc"])
	
	try:
		comments = json.loads(requests.get(questionlink, headers={"User-agent":"RedBot 0.1"}).text)[1]["data"]["children"]
	except:
		print("Error has occurred.")
	questionData["comments"] = []

	for comment in comments:
		comment = comment["data"]
		try:
			if comment.get("author") == None: continue
			questionData["comments"].append({
				"id": comment["id"],
				"author": comment["author"],
				"score": getScore(comment["score"]),
				"created": getTime(start_time-comment["created_utc"]),
				"comment": comment["body"]
			})
		except:
			print("Problem with question, moving on")

	print("Completed, moving on\n")

	#print(json.dumps(questionData))
	file = open("Outputs/"+question["id"]+".json","w+")
	file.write(json.dumps(questionData))
	file.close()