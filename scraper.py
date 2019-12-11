import requests, json
from math import floor
from time import time

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
	divider = ""

	if timeScore < 60:
		divider = [timeScore, 1, "s"]
	elif timeScore < 3600:
		divider = [60, "m"]
	elif timeScore < 86400:
		divider = [3600, "h"]
	elif timeScore < 31536000:
		divider = [86400, "d"]
	else: divider = [31536000, "y"]

	return str(round(timeScore/divider[0], 1))+divider[1]

for question in data:
	question = question["data"]
	file = open(question["id"]+".txt","w+")
	questionData = {}

	print("ID: ["+question["id"]+"]")
	print("Asked by u/"+question["author"]+",")
	print(question["title"])
	print(question.keys())

	questionData["title"] = question["title"]

	print(getScore(question["score"]) + " points\n")
	questionData["score"] = getScore(question["score"])

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
				"author": comment["author"],
				"score": getScore(comment["score"]),
				"created": getTime(start_time-comment["created_utc"]),
				"comment": comment["body"]
			})
		except:
			print("Problem with question, moving on")

	print("Completed, moving on\n")

	#print(json.dumps(questionData))
	file.write(json.dumps(questionData))
	file.close()
	break