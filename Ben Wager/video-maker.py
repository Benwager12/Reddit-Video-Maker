from subprocess import call as run
from os import path, makedirs

def makeSegment(video, comment, isTitle=False):
	precursor = "title-" if isTitle else "comment-"
	command = ["../Utilities/ffmpeg", "-loop", "1", "-i", "Screenshots/" + video + "/" + comment + ".png",
				"-i", "Voices/" + video + "/" + precursor + comment + ".wav", "-c:v", "libx264", "-tune",
				"stillimage", "-c:a", "aac", "-b:a", "192k", "-pix_fmt", "yuv420p", "-shortest", "out.mp4"]
	run(command)

makeSegment("ekx7gi","fde9lgp")