from subprocess import run
from os import path, makedirs, mkdir, listdir

def makeSegment(video, comment, isTitle=False, filePath="/", fileName="out"):
	precursor = "title-" if isTitle else "comment-"
	screenshotsName = "Title.png" if isTitle else comment+".png"
	command = ["../Utilities/ffmpeg", "-i", f"Screenshots/{video}/{screenshotsName}", "-i",
				f"Voices/{video}/{precursor}{comment}.wav", "-af", "apad=pad_dur=1", "-b", "30000",
				"-vb", "20M", "-r", "11", "-vf", "scale=1920:-1", f"{filePath}/{fileName}.avi"]
	run(command)

if not path.exists("Sections"):
	mkdir("Sections")

questionId = "0"
while not path.exists(f"Voices/{questionId}/") or not path.exists(f"Screenshots/{questionId}/"):
	questionId = input("Choose a video to make (from outputs): ")

files = listdir(f"Voices/{questionId}")

if not path.exists(f"Sections/{questionId}"):
	mkdir(f"Sections/{questionId}")

if not path.exists("Videos"):
	mkdir("Videos")

if not path.exists(f"Videos/{questionId}"):
	mkdir(f"Videos/{questionId}")

sections = open(f"Videos/{questionId}/sections.txt", "w+")
sections.write(f"file '../../Sections/{questionId}/Title.avi'\n")
for file in files:

	commentId = (".".join(file.split(".")[:-1])).split("-")[1]
	isTitle = file.startswith("title-")

	fileName = "Title" if isTitle else commentId
	makeSegment(questionId, commentId, isTitle, f"Sections/{questionId}", fileName)
	if fileName == "Title":
		continue
	sections.write(f"file '../../Sections/{questionId}/{fileName}.avi'\n")
sections.close()

command = ["../Utilities/ffmpeg", "-f", "concat", "-safe", "0", "-i", f"Videos/{questionId}/sections.txt", "-c",
			"copy", f"Videos/{questionId}/output.mp4"]
run(command)