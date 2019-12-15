#-----Lloyd 2019-----

#IT WORKS! I THINK

import requests, json, os, sys
from random import randint
from time import time, sleep
from gtts import gTTS
from selenium import webdriver
total_time = time()
start_time = time()
from selenium.webdriver.opera.options import Options

#print("Init Opera Driver...")

#WINDOW_SIZE = "0,0"
options1 = Options()
#options1.add_argument('--ignore-certificate-errors')
#options1.add_argument("--test-type")
#options1.add_argument('--headless')
#options1.add_argument('--no-sandbox')
#options1.add_argument("--window-size=%s" % WINDOW_SIZE)



def getscore(score):
  if score > 1000:
    score /= 1000
    score = round(score,1)
    return str(score) + "k"
  return str(score)

print("Declaring, setting and checking important vars\n")
print(os.path.dirname(sys.argv[0]) + "\\wkhtmltoimage.exe")
#This is how far the script goes into comments before stopping
depthlimit = 25

randcom = []
randcomquestion = []
selectedurl = ""
link = "https://www.reddit.com/r/askreddit.json"


if depthlimit <=0 or selectedurl != "" or link == "":
  print("A variable is invaild - ERROR")
  quit()
print("Done checking vars\n")

print("Opening data.txt...  - INFO")
fdata = open("script.txt","w+")
fdata2 = open("scripttts.txt","w+")


#Load questions

req = requests.get(link, headers={"User-agent":"rb0.1"}).text #gets body from link
data = json.loads(req)["data"]["children"]
print("Building randcom array...\n")
for question in data:
    question = question["data"]
    #print("u/"+question["author"])
    randcom.append("https://www.reddit.com" + question["permalink"]) #Get permalink, so we can access the json file
    randcomquestion.append(question["title"])
    #print(question["title"] + "\n")
    
    

print(str(len(randcom)-1) + " total url's found in randcom array! - INFO\n")
print("Selecting Random URL from randcom... - INFO\n")
genint = randint(0,len(randcom)-1)
selectedurl = str(randcom[genint]) + ".json"
#print(selectedurl)
print("\nFound random URL. Getting json from said url.\n")

fdata.write(randcomquestion[genint] + "\n\n")
fdata2.write(randcomquestion[genint]+ "\n\n")

#Stage 2
print("\n---Starting Stage 2---\n")

print("Delcaring and setting important vars\n")
#Load questions
#print(selectedurl)
req1 = requests.get(selectedurl, headers={"User-agent":"rb0.1"}).text

data = json.loads(req1)[1]["data"]["children"]

print("Building answer data file...\n")
i = 0
for answer in data:
    if i >= depthlimit:
      print("Depth Limit Reached: " + str(i) +"\n")
      break
    answer = answer["data"]
    #print(answer.keys())
    if answer.get("author") == None: continue
    if answer["author"] == "AutoModerator": continue
    try:
      fdata.write("u/"+answer["author"] + "||" + getscore(answer["score"]) + " points||")
      fdata.write( answer["body"] + "/////")
    except:
      print("Error Occurred while writing in script.txt, skipping body..\n")
      continue
    
    fdata2.write(answer["body"] + ".\n\n")
    i = i + 1
    #randcom.append("https://www.reddit.com" + question["permalink"]) #Get permalink, so we can access the json file
    #print(question["title"] + "\n")


print("Closing script files...\n")
fdata.close()
fdata2.close()
print("Script Generation finished at:")
print("--- %s seconds ---" % round(time() - start_time, 2))
print("Starting TTS Generation...")
start_time = time()
f = open("scripttts.txt")
#ttstext = f.read()
#ttsobj = gTTS(ttstext,lang="en", slow=False)

#ttsobj.save("script.wav")
f.close()
print("TTS Generation finished at:")
print("--- %s seconds ---" % round(time() - start_time, 2))

#Somewhat working script, unable to take screenshots of website
#without driver for chrome
#Doing it in VB instead

#Gets all parts of the script like author, score and author

start_time = time()
partnumber = 0
parts = ["author","score","comment"]
authorscorecomments = []
splitscript = open("script.txt").read()


try:

  i2 = 0
  screenshotnumber = 0
  for question in splitscript.split("/////"):
    if i2 == 0:
      i2 = i2 + 1
      continue
    for part in question.split("||"):
      if partnumber > 2:
        partnumber = 0
      #print(part + " " + parts[partnumber])
      authorscorecomments.append(part)
      partnumber = partnumber + 1
    #print(authorscorecomments)
    if '"' in authorscorecomments[2]:
      continue
    fin = open("sketch.js","rt")
    data1 = fin.read()
    data1 = data1.replace("replaceme1author",authorscorecomments[0])
    data1 = data1.replace("replaceme2score",authorscorecomments[1])
    data1 = data1.replace("replaceme3comment",authorscorecomments[2])

    fin.close()

    fin = open("sketch.js","wt")
    fin.write(data1)
    fin.close()
    
    sleep(0.5)
    #SCREENSHOT WEBSITE HERE
    #print(screenshotnumber)
    driver = webdriver.Opera(options=options1)
    driver.get(os.path.dirname(sys.argv[0]) + "\\index.html")
    sleep(0.5)
    driver.save_screenshot("generated_screenshots\\screenshot"+str(screenshotnumber)+".png")

    driver.quit()
    print("Driver Screenshot completed: " + str(screenshotnumber))
    sleep(5)
    fin = open("sketch.js","rt")
    data1 = fin.read()
    
    data1 = data1.replace(authorscorecomments[0],"replaceme1author")
    data1 = data1.replace(authorscorecomments[1],"replaceme2score")
    data1 = data1.replace(authorscorecomments[2],"replaceme3comment")
    fin.close()

    fin = open("sketch.js","wt")
    fin.write(data1)
    fin.close()
    screenshotnumber = screenshotnumber + 1
    authorscorecomments = []
except Exception as e:
  print("Exception Occurred, probably normal. Continuing: " + str(e))

#print("P5 screenshot prep finished at:")
#print("--- %s seconds ---" % round(time() - start_time, 2))

print("\n\nTotal finished at:")
print("--- %s seconds ---" % round(time() - total_time, 2))
