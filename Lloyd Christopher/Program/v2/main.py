#-----Lloyd 2019-----#
#-----LunarHunter-----#
#This script is under the The Unlicense license!

#Ver 2.0
#This version is ready to use and has some improvements over the last ver.

#This version could support ffmpeg if I implement the speech gen into the screenshot
#loop.

#I would suggest running in a VM to avoid any problems that prevents termination.

#TODO:
#Upload automatically after qc (quality control)/manual check Not possible I think

import requests, json, os, sys, shutil
from html import escape
from random import randint
from time import time, sleep
from selenium import webdriver
from subprocess import Popen as process
import vidgen
total_time = time()
start_time = time()
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

print("Removing all files from previous generation...")

try:
  os.remove('script.txt')
  os.remove('scripttts.txt')
  os.remove('voice.wav')
except:
  print("Error removing files/folders from main dir. Resuming")
  
WINDOW_SIZE = "1920,1080"
options1 = Options()

#You can uncomment these param if you replace the webdriver with chrome instead of opera

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

print("Opening/creating files important to program...  - INFO")
fdata = open("script.txt","w+")
fdata2 = open("scripttts.txt","w+")



#Load questions

#req = requests.get(link, headers={"User-agent":"rb0.1"}).text #gets body from link
req = open("data.json", "r").read()
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

#exclusions = open("exclusions.txt", "a")
#if str(randcom[genint]) in exclusions.read():
#    print("BREAK! Link that is selected is in the exclusion list.")
#    sleep(2)
#    exit(1)

#exclusions.write(str(randcom[genint]) + "\n")
#exclusions.close()
#print(selectedurl)
print("Generating question image...")
#vidgen.genquestionimage(str(randcom[genint]))
print("\nFound random URL. Getting json from said url.\n")

fdata2.write(randcomquestion[genint]+ "\n\n")

#Stage 2
print("\n---Starting Stage 2---\n")

print("Delcaring and setting important vars\n")
#Load questions
#print(selectedurl)

#USE THIS TO OVERRIDE THE ANSWERS!
#You have to get the question manually though!
#selectedurl = "https://www.reddit.com/r/AskReddit/comments/eaymhi/men_of_reddit_whats_a_thing_that_can_be_scary/.json"
print(selectedurl)
req1 = open("data1.json", "r").read()

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
    if answer["author"].lower() == "deleted": continue
    try:
      fdata.write("u/"+answer["author"] + "||" + getscore(answer["score"]) + " points||")
      fdata.write( answer["body"] + "¬¬¬¬¬")
      #fdata2.write(answer["body"] + ".\n\n")
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

start_time = time()
partnumber = 0
parts = ["author","score","comment"]
authorscorecomments = []
splitscript = open("script.txt").read()

driver = webdriver.Chrome(options=options1)

command = ["/../../../Utilities/speak", "-n", "David", "-t", open("scripttts.txt", "r").read(), "-w", "temp\question.wav"]
process(command)

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
    command = ["/../../../Utilities/speak", "-n", "David", "-t", ttstext, "-w", "temp\\"+str(screenshotnumber)+".wav"]
    process(command)
    
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

vidgen.genmp4()

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
