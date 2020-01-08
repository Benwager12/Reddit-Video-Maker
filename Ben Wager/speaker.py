import json
from subprocess import call as run
from os import path, makedirs
import string

def speak(words, directory_fileName=None):
	printable = set(string.printable)
	wordsNew = ''.join(filter(lambda x: x in printable, words))
	print(wordsNew)

	try:
		makedirs("Voices/"+directory_fileName[0]+"/")
	except FileExistsError:
		pass
	#print(words)
	arr = ["../Utilities/speak", "-n", "Daniel", "-t", wordsNew.replace("\"", "'")]
	if not directory_fileName is None:
		arr.append("-w")
		arr.append("Voices/"+directory_fileName[0]+"/"+directory_fileName[1]+".wav")
	print(arr)
	run(arr)

def saveSpeak(words, directory_fileName=None):
	#print("Started voice output... ", end="")
	speak(words, directory_fileName)
	#print("Ended voice output")

question = "0"
while not path.exists("Outputs/"+question+".json"):
        question = input("Choose the question to speak (from outputs): ")
        print("Outputs/"+question+".json")
        if not path.exists("Outputs/"+question+".json"):
                print("File does not exist.\n")
file = json.loads(open("Outputs/"+question+".json", "r").read())

questionTitle, questionId = file["title"], file["id"]
questionScore, questionAuthor = file["score"], file["author"]
questionUrl, questionCreated = file["url"], file["created"]
comments = file["comments"]

# author points · created ago
# title
#print(f"{questionAuthor}  {questionScore} · {questionCreated} ago")
#print(questionTitle)
saveSpeak(questionTitle, [questionId,"/title-"+questionId])
print("\n")

for comment in comments:
	commentAuthor, commentScore = comment["author"], comment["score"]
	commentedCreated, commentComment = comment["created"], comment["comment"]
	commentId = comment["id"]

	#print(f"{commentAuthor}  {commentScore} · {commentedCreated} ago")
	#print(commentComment)

	#print(commentComment)
	#print([questionId,"/comment-"+commentId])
	#print()


	saveSpeak(commentComment, [questionId,"comment-"+commentId])
	print("")
