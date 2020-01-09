from subprocess import call as run
from os import path

import screenshotter, speaker, videomaker

questionId = "0"

while not path.exists("Outputs/"+questionId+".json"):
    questionId = input("Please enter a question ID: ")
    if not path.exists("Outputs/"+questionId+".json"):
        print("File not found.\n")
print("Selected question: "+ questionId+"\n")

print("Speaking voices")
speaker.speakVoice(questionId)

print("Screenshotting video")
screenshotter.takeScreenshots(questionId)

print("Making video")
videomaker.makeVideo(questionId)
