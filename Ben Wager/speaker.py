from gtts import gTTS as speak
import json, os

file = json.loads(open("template.json", "r").read())

if not os.path.exists("Voices/"+file["id"]):
	os.makedirs("Voices/"+file["id"])

titleVoice = speak(file["title"])
titleVoice.save("Voices/"+file["id"]+"/title-" + file["id"] + ".wav")

for comment in file["comments"]:
	if os.path.exists("Voices/"+file["id"]+"/comment-"+comment["id"]+".wav"):
		continue

	print("Starting comment " + comment["id"])
	voice = speak(comment["comment"])
	voice.save("Voices/"+file["id"]+"comment-"+comment["id"]+".wav")
	print("Finished comment " + comment["id"])