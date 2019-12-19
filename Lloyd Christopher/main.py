#-----Lloyd 2019-----#

import requests, json, os, sys, shutil
from html import escape
from random import randint
from time import time, sleep
from selenium import webdriver
from subprocess import Popen as process
total_time = time()
start_time = time()
from selenium.webdriver.opera.options import Options

print("Reverting sketch.js...")
shutil.copy('backup\sketch.js', 'sketch.js')
sleep(1)
WINDOW_SIZE = "1260,1020"
options1 = Options()
#options1.add_argument('--ignore-certificate-errors')
#options1.add_argument("--test-type")
#options1.add_argument('--headless')
#options1.add_argument('--no-sandbox')
options1.add_argument("--window-size=%s" % WINDOW_SIZE)

def getscore(score):
  if score > 1000:
    score /= 1000
    score = round(score,1)
    return str(score) + "k"
  return str(score)

print("Declaring, setting and checking important vars\n")
#print(os.path.dirname(sys.argv[0]) + "\\wkhtmltoimage.exe")
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

#USE THIS TO OVERRIDE THE ANSWERS!
#You have to get the question manually though!
#selectedurl = "https://www.reddit.com/r/AskReddit/comments/eaymhi/men_of_reddit_whats_a_thing_that_can_be_scary/.json"

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
      fdata.write( answer["body"] + "¬¬¬¬¬")
      fdata2.write(answer["body"] + ".\n\n")
    except:
      print("Error Occurred while writing in script.txt, skipping body..\n")
      continue
    
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
ttstext = f.read()
#ttsobj = gTTS(ttstext,lang="en", slow=False)

#ttsobj.save("script.wav")
print("Starting TTS Generation")
command = ["balcon", "-n", "Daniel", "-t", ttstext, "-w", "voice.wav"]
process(command)

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

driver = webdriver.Opera(options=options1)

try:
  i2 = 0
  screenshotnumber = 0
  for question in splitscript.split("¬¬¬¬¬"):

    if i2 == 0:
      i2 = i2 + 1
      continue
    for part in question.split("||"):
      #print("1")
      if partnumber > 2:
        partnumber = 0
      print(part + " " + parts[partnumber])
      authorscorecomments.append(part)
      partnumber = partnumber + 1
    #print(authorscorecomments)
    #if '"' in authorscorecomments[2]:
    #  print("1")
    #  continue
    #fin = open("sketch.js","rt")
    #data1 = fin.read()

    
    #data1 = data1.replace("replaceme1author",authorscorecomments[0])
    #data1 = data1.replace("replaceme2score",authorscorecomments[1])
    #authorscorecomments[2] = authorscorecomments[2].replace("\\","\\\\").replace("\n","").replace("\"", "\\\"").replace("\'", "\\\'")
    #authorscorecomments[2] = escape(authorscorecomments[2])
    #data1 = data1.replace("replaceme3comment",authorscorecomments[2])

    #fin.close()

    #fin = open("sketch.js","wt")
    #fin.write(data1)
    #fin.close()
    
    sleep(0.3)
    #SCREENSHOT WEBSITE HERE
    #print(screenshotnumber)
    authorscorecomments[2] = authorscorecomments[2].replace("\"", "\\\"")
    authorscorecomments[2] = authorscorecomments[2].replace("\\", "\\\\")
    authorscorecomments[2] = authorscorecomments[2].replace("\n", "\\n")
    authorscorecomments[2] = authorscorecomments[2].replace("\\\\\"", "\\\"")
    
    driver.get(os.path.dirname(sys.argv[0]) + "\\index.html")
    script = "author=\"" + authorscorecomments[0] + "\";score=\"" + authorscorecomments[1] + "\";comment=\"" + authorscorecomments[2] +"\";"
    print(script)
    driver.execute_script(script)
    sleep(0.4)
    driver.save_screenshot("generated_screenshots\\screenshot"+str(screenshotnumber)+".png")
    #sleep(5)
    #driver.quit()
    #print(authorscorecomments[0])
    #print(authorscorecomments[1])
    #print(authorscorecomments[2])
    print("Driver Screenshot completed: " + str(screenshotnumber))
    #fin = open("sketch.js","rt")
    #data1 = fin.read()
    
    #data1 = data1.replace(authorscorecomments[0],"replaceme1author")
    #data1 = data1.replace(authorscorecomments[1],"replaceme2score")
    #data1 = data1.replace(authorscorecomments[2],"replaceme3comment")
    #fin.close()

    #fin = open("sketch.js","wt")
    #fin.write(data1)
    #fin.close()
    screenshotnumber = screenshotnumber + 1
    authorscorecomments = []
    
except Exception as e:
  print("Exception Occurred, probably normal. Continuing: " + str(e))

print("P5 screenshot finished at:")
print("--- %s seconds ---" % round(time() - start_time, 2))

driver.quit()

print("\n\nTotal finished at:")
print("--- %s seconds ---" % round(time() - total_time, 2))

print("\n\nProgram finished!")
