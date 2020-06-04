#-----Lloyd 2019-----#
#-----LunarHunter-----#
#This script is under the The Unlicense license!

#Ver 3.0
#This version is ready to use and has some improvements over the last ver.

#This version could support ffmpeg if I implement the speech gen into the screenshot
#loop.

#I would suggest running in a VM to avoid any problems that prevents termination.

#TODO:
#Upload automatically after qc (quality control)/manual check Not possible I think

import os, sys, requests, json
from html import escape
from random import randint
from time import time, sleep
from selenium import webdriver
from subprocess import Popen as process
import vidgen
total_time = time()
from selenium.webdriver.chrome.options import Options
answer = input('-----LunarHunter 2019-----\n-----Reddit Video Maker-----\n\nThis program is under the Unlicense license! I would suggest running in a VM to avoid any problems that prevents termination.\n\n' +
               'Notes:\n' +      
               'Please delete all files in temp and vidgen before running this program! I will add this feature soon but not currently a priority.\n' +
               'The final video requires background music so manual editing is required\n\n' +
               'Please indicate approval to running the program and agreeing to the terms of the license: [y/n]')
if not answer or answer[0].lower() != 'y':
    print('You did not indicate approval!')
    sleep(2)
    exit(1)
start_time = time()

print("Removing all files from previous generation...")

try:
  os.remove('script.txt')
  os.remove('scripttts.txt')
  os.remove('voice.wav')
except:
  print("Error removing files/folders from main dir. Resuming")

options1 = Options()


options1.add_argument('--ignore-certificate-errors')
options1.add_argument("--test-type")
options1.add_argument('--headless')
options1.add_argument('--no-sandbox')
options1.add_argument("--window-size=%s" % "1920,1080") # CHANGE RESOLUTION HERE

def getscore(score):
  if score > 1000:
    score /= 1000
    score = round(score,1)
    return str(score) + "k"
  return str(score)

print("Declaring, setting and checking important vars\n")
#print(os.path.dirname(sys.argv[0]) + "\\wkhtmltoimage.exe")

#This is how far the script goes into comments before stopping
commentdepthlimit = 25

randquestion = []
randcomment = []
selectedquestionurl = ""

link = "https://www.reddit.com/r/askreddit.json"

if commentdepthlimit <=0 or selectedquestionurl != "" or link == "":
  print("A variable is invaild - ERROR")
  quit()
print("Done checking vars\n")

print("Opening/creating files important to program...  - INFO")
script = open("script.txt","w+")
scripttts = open("scripttts.txt","w+")

#Load questions
print("Loading questions... \n")

data = json.loads(requests.get(link, headers={"User-agent":"rb0.1"}).text)["data"]["children"] #gets body from link
print("Building randquestion array...\n")
for question in data:
    question = question["data"]
    #print("u/"+question["author"])
    randquestion.append("https://www.reddit.com" + question["permalink"]) #Get permalink, so we can access the json file
    randcomment.append(question["title"])
    #print(question["title"] + "\n")

print(str(len(randquestion)-1) + " total url's found in randquestion array! - INFO\n")
print("Selecting Random URL from randquestion... - INFO\n")

genint = randint(0,len(randquestion)-1)
selectedquestionurl = str(randquestion[genint]) + ".json"

#exclusions = open("exclusions.txt", "a")
#if str(randcom[genint]) in exclusions.read():
#    print("BREAK! Link that is selected is in the exclusion list.")
#    sleep(2)
#    exit(1)

#exclusions.write(str(randcom[genint]) + "\n")
#exclusions.close()
#print(selectedquestionurl)
print("Generating question image...")
vidgen.genquestionimage(str(randquestion[genint]))
print("\nFound random URL. Getting json from said url.\n")

scripttts.write(randcomment[genint]+ "\n\n")

#Stage 2
print("\n---Starting Stage 2---\n")

print("Delcaring and setting important vars\n")
#Load questions
#print(selectedquestionurl)

#USE THIS TO OVERRIDE THE ANSWERS!
#You have to get the question manually though!
#selectedquestionurl = "https://www.reddit.com/r/AskReddit/comments/eaymhi/men_of_reddit_whats_a_thing_that_can_be_scary/.json"

data = json.loads(requests.get(selectedquestionurl, headers={"User-agent":"rb0.1"}).text)[1]["data"]["children"] #Loads answers

print("Building answer data file...\n")
i = 0
for answer in data:
    if i >= commentdepthlimit:
      print("Depth Limit Reached: " + str(i) +"\n")
      break
    answer = answer["data"]
    #print(answer.keys())
    if answer.get("author") == None: continue
    if answer["author"] == "AutoModerator": continue
    if answer["author"].lower() == "deleted": continue
    try:
      script.write("u/"+answer["author"] + "||" + getscore(answer["score"]) + " points||")
      script.write( answer["body"] + "¬¬¬¬¬")
      #fdata2.write(answer["body"] + ".\n\n")
    except:
      print("Error Occurred while writing in script.txt, skipping body..\n")
      continue
    
    i = i + 1
    #randcom.append("https://www.reddit.com" + question["permalink"]) #Get permalink, so we can access the json file
    #print(question["title"] + "\n")


print("Closing script files...\n")
script.close()
scripttts.close()

print("Script Generation finished at:")
print("--- %s seconds ---" % round(time() - start_time, 2))

start_time = time()
partnumber = 0
parts = ["author","score","comment"]
authorscorecomments = []
splitscript = open("script.txt").read()

driver = webdriver.Chrome(options=options1)

process(["balcon", "-n", "Daniel", "-t", open("scripttts.txt", "r").read(), "-w", "temp\question.wav"])

try:
  screenshotnumber = 0
  for question in splitscript.split("¬¬¬¬¬"):

    for part in question.split("||"):
      if partnumber > 2:
        partnumber = 0
      print(part + " " + parts[partnumber])
      authorscorecomments.append(part)
      partnumber = partnumber + 1
    print(authorscorecomments)
    #sleep(0.3)
    #SCREENSHOT WEBSITE HERE

    print("Generating TTS for sep file...")

    ttstext = authorscorecomments[2]
    print("Starting TTS Generation and removing invaild characters...")
    ttstext = ttstext.replace("\"", "")
    ttstext = ttstext.replace("\\", "")
    #ttstext = ttstext.replace("\n", "")
    ttstext = ttstext.replace("\\\\\"", "")
    ttstext = ttstext.replace('"', "")
    process(["balcon", "-n", "Daniel", "-t", ttstext, "-w", "temp\\"+str(screenshotnumber)+".wav"])
    
    authorscorecomments[2] = authorscorecomments[2].replace("\"", "\\\"")
    authorscorecomments[2] = authorscorecomments[2].replace("\\", "\\\\")
    authorscorecomments[2] = authorscorecomments[2].replace("\n", "\\n")
    authorscorecomments[2] = authorscorecomments[2].replace("\\\\\"", "\\\"")
    
    driver.get(os.path.dirname(sys.argv[0]) + "\\index.html")
    script = "author=\"" + authorscorecomments[0] + "\";score=\"" + authorscorecomments[1] + "\";comment=\"" + authorscorecomments[2] +"\";"
    print(script)
    driver.execute_script(script)
    sleep(0.4)
    driver.save_screenshot("temp\\"+str(screenshotnumber)+".png")

    print("Driver Screenshot completed: " + str(screenshotnumber))
    
    screenshotnumber = screenshotnumber + 1
    authorscorecomments = []
    
    #to ensure that the system running the script doesn't get overloaded with the balcom program.
    #sleep(1)
    
except Exception as e:
  print("Exception Occurred, probably normal. Continuing: " + str(e))

driver.quit()

print("P5 screenshot finished at:")
print("--- %s seconds ---" % round(time() - start_time, 2))

print("Starting ffmpeg combine...")

start_time = time()

vidgen.combinesoundandimage()

print("FFMPEG combine finished at:")
print("--- %s seconds ---" % round(time() - start_time, 2))

print("Starting ffmpeg final generation...")

start_time = time()

vidgen.genfinalvid()

print("FFMPEG final generation finished at:")
print("--- %s seconds ---" % round(time() - start_time, 2))


print("\n\nTotal finished at:")
print("--- %s seconds ---" % round(time() - total_time, 2))

print("\n\nProgram finished!")
