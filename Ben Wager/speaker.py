import json
from subprocess import Popen as process
from os import path, makedirs

def speak(words, directory_fileName=None):
	print(path.exists("/Voices/"+directory_fileName[0]+"/"))
	try:
		makedirs("Voices/"+directory_fileName[0]+"/")
	except FileExistsError:
		pass
	arr = ["speak", "-n", "Daniel", "-t", words]
	if not directory_fileName is None:
		arr.append("-w")
		arr.append("Voices/"+directory_fileName[0]+"/"+directory_fileName[1]+".wav")
	#process(arr)

def saveSpeak(words, directory_fileName=None):
	print("Started voice output... ", end="")
	speak(questionTitle, directory_fileName)
	print("Ended voice output")

file = json.loads(open("template.json", "r").read())

questionTitle, questionId = file["title"], file["id"]
questionScore, questionAuthor = file["score"], file["author"]
questionUrl, questionCreated = file["url"], file["created"]
comments = file["comments"]

# author points · created ago
# title
print(f"{questionAuthor}  {questionScore} · {questionCreated} ago")
print(questionTitle)
saveSpeak(questionTitle, [questionId,"/title-"+questionId])
print("\n")

for comment in comments:
	commentAuthor, commentScore = comment["author"], comment["score"]
	commentedCreated, commentComment = comment["created"], comment["comment"]
	commentId = comment["id"]

	print(f"{commentAuthor}  {commentScore} · {commentedCreated} ago")
	print(commentComment)
	saveSpeak(commentComment, [questionId,"/comment-"+commentId])
	print("")