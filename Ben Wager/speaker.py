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
	arr = ["../Utilities/speak", "-n", "David", "-t", wordsNew.replace("\"", "'")]
	if not directory_fileName is None:
		arr.append("-w")
		arr.append("Voices/"+directory_fileName[0]+"/"+directory_fileName[1]+".wav")
	run(arr)

def speakVoice(id):
        file = json.loads(open("Outputs/"+id+".json", "r").read())

        questionTitle, questionId = file["title"], file["id"]
        questionScore, questionAuthor = file["score"], file["author"]
        questionUrl, questionCreated = file["url"], file["created"]
        comments = file["comments"]

        speak(questionTitle, [questionId,"/title-"+questionId])
        print("\n")

        for comment in comments:
                commentAuthor, commentScore = comment["author"], comment["score"]
                commentedCreated, commentComment = comment["created"], comment["comment"]
                commentId = comment["id"]

                speak(commentComment, [questionId,"comment-"+commentId])
                print()
