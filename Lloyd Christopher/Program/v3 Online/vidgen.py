﻿#-----LunarHunter 2019-----#
#-----     Lloyd      -----#
#HOLY the genfinalvid took so long. AS YOU CAN SEE
import os
from PIL import Image
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from time import sleep
def combinesoundandimage():
    counta = 0
    os.system('ffmpeg -i temp\\question1.png -i temp\\question.wav -af "apad=pad_dur=1" -b 30000 -vb 20M -r 11 -vf "scale=1920:-1" vidgen\\question.avi > logs\\outputmp4.txt 2> logs\\errmp4.txt')
    while counta < 30:
        print(str(counta))
        os.system('ffmpeg -i temp\\' + str(counta) + '.png -i temp\\' + str(counta) + '.wav -af "apad=pad_dur=1" -b 30000 -vb 20M -r 11 -vf "scale=1920:-1" vidgen\\' + str(counta) + '.avi > logs\\outputmp4.txt 2> logs\\errmp4.txt')
        counta = counta + 1

def videotoavi(locallocation):
    os.system('ffmpeg -i ' + locallocation + ' -b 30000 -vb 20M -r 11 -vf "scale=1920:-1" generatedavi.avi > logs\\outputmp4.txt 2> logs\\errmp4.txt')

def genfinalvid():
    try:
        os.remove('final.mp4')
        os.remove('finalgen_video.mp4')
    except:
        print("Failed to remove final.mp4 and/or finalgen_video.mp4")
    filea = "file 'vidgen/question.avi'\n"
    fdata = open("list.txt", "w+") #opens the list of files that need to be combined together
    for filename in os.listdir("vidgen\\"):
        if 'question.avi' in filename:
            continue
        filea = filea + "file 'vidgen/" + filename + "'\n"
        filea = filea + "file 'GFX/123.avi'\n" #Attempts to add a static transition effect after each comment
    #print(filea)
    fdata.write(filea)
    fdata.close()
    #os.system('mencoder -oac pcm -ovc copy -o final.mp4' + filea)
    #fdata = open("list.txt","w+")
    #    fdata.write("file 'vidgen\\" + filename + "'\n")
    #    #-vcodec mpeg4 -b 30000 -vb 20M -vf "scale=1290:-1"
    #os.system("ffmpeg -f " + filea + " -c copy result.mov > output.txt 2> err.txt")

    sleep(0.4) #This sleep may not be necessary, TODO: Remove if not necessary

    os.system("ffmpeg -f concat -i list.txt -c copy final.mp4 > logs\\output.txt 2> logs\\err.txt") #Runs the concat commant from ffmpeg
    #os.system("ffmpeg -i final.mp4 -i SFX\\1.mp3 -map 0:1 -map 1:0 finalgen_video.mp4 > logs\\output.txt 2> logs\\err.txt")
    #os.system('ffmpeg.exe -i final.mp4 -i SFX\\1.mp3 -filter_complex "[1:0]volume=0.5[a1];[0:a][a1]amix=inputs=2:duration=first" -vf "pad=ceil(iw/2)*2:ceil(ih/2)*2" -map 0:v:0 finalgen_video.mp4 -c copy > logs\\outputfinalgen.txt 2> logs\\errfinalgen.txt')
    #os.system('mencoder final.mp4 -o finalgen_video.mp4 -ovc copy -oac copy -audiofile SFX\\1.mp4')
    #os.system('ffmpeg -i "concat:1.flv|2.flv" -codec copy output.mkv > output.txt 2> err.txt')
def genquestionimage(url):
    #init settings of driver
    options1 = Options()
    options1.add_argument('--ignore-certificate-errors')
    options1.add_argument("--test-type")
    options1.add_argument('--headless')
    options1.add_argument('--no-sandbox')
    options1.add_argument("--window-size=%s" % "1280,600") # RESOLUTION HERE
    driver = webdriver.Chrome(options=options1) #Starts the chrome driver
    driver.get(url) #goes to reddit question to screenshot
    driver.save_screenshot("temp\\question.png")#screenshot page
    driver.quit()#close the driver
    im = Image.open("temp\\question.png")#save the image in var
    im1 = im.crop((100,100,780,265))#TODO: if possible, replace im1 to just im
    im1.save("temp\\question1.png")#save the image on the disk
#genmp4()
#genvideoclip()
#genfinalvid()
#genquestionimage("https://www.reddit.com/r/AskReddit/comments/ek7l30/if_cats_had_pockets_what_would_you_find_in_your/")
