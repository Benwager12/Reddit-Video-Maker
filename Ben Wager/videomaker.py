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

def makeVideo(id):
        files = listdir(f"Voices/{id}")

        if not path.exists(f"Sections/{id}"):
                mkdir(f"Sections/{id}")

        if not path.exists("Videos"):
                mkdir("Videos")

        if not path.exists(f"Videos/{id}"):
                mkdir(f"Videos/{id}")

        sections = open(f"Videos/{id}/sections.txt", "w+")
        sections.write(f"file '../../Sections/{id}/Title.avi'\n")
        for file in files:

                commentId = (".".join(file.split(".")[:-1])).split("-")[1]
                isTitle = file.startswith("title-")

                fileName = "Title" if isTitle else commentId
                makeSegment(id, commentId, isTitle, f"Sections/{id}", fileName)
                if fileName == "Title":
                        continue
                sections.write(f"file '../../Sections/{id}/{fileName}.avi'\n")
        sections.close()

        command = ["../Utilities/ffmpeg", "-f", "concat", "-safe", "0", "-i", f"Videos/{id}/sections.txt", "-c",
			"copy", f"Videos/{id}/output.mp4"]
        run(command)
