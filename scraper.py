import requests, json
from math import floor

link = "https://www.reddit.com/r/askreddit.json"
req = requests.get(link, headers={"User-agent":"RedBot 0.1"}).text

data = json.loads(req)["data"]["children"]

def getScore(score):
	if score >= 1000:
		score /= 1000
		score = round(score, 1)
		return str(score)+"k"
	return str(score)

for question in data:
	question = question["data"]
	file = open(question["id"]+".txt","w+")
	questionData = {}

	print("ID: ["+question["id"]+"]")
	print("Asked by u/"+question["author"]+",")
	print(question["title"])

	questionData["title"] = question["title"]
	questionData["awards"] = question["total_awards_received"]

	print(getScore(question["score"]) + " points\n")
	questionData["score"] = getScore(question["score"])

	questionlink = question["url"][0:-1]+".json"
	questionData["url"] = question["url"]
	
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
				"awards": comment["total_awards_received"],
				"comment": comment["body"]
			})
		except:
			print("Problem with question, moving on")

	print("Completed, moving on\n")
	file.write(json.dumps(questionData))
	file.close()