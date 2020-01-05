#-----LunarHunter 2019-----#
#-----     Lloyd      -----#
#HOLY the genfinalvid took so long. AS YOU CAN SEE
import os, subprocess
from time import sleep
def genmp4():
    counta = 0
    while counta < 30:
        print(str(counta))
        os.system('ffmpeg -i temp\\' + str(counta) + '.png -i temp\\' + str(counta) + '.wav -af "apad=pad_dur=1" -b 30000 -vb 20M -r 11 -vf "scale=1920:-1" vidgen\\' + str(counta) + '.avi > logs\\outputmp4.txt 2> logs\\errmp4.txt')
        counta = counta + 1

def genavifile(locallocation):
    os.system('ffmpeg -i ' + locallocation + ' -b 30000 -vb 20M -r 11 -vf "scale=1920:-1" generatedavi.avi > logs\\outputmp4.txt 2> logs\\errmp4.txt')

def genfinalvid():
    try:
        os.remove('final.mp4')
    except:
        print("Failed to remove final.mp4")
    filea = ""
    fdata = open("list.txt", "w+")
    for filename in os.listdir("vidgen\\"):
        filea = filea + "file 'vidgen/" + filename + "'\n"
        filea = filea + "file 'GFX/123.avi'\n"
    #print(filea)
    fdata.write(filea)
    fdata.close()
    #os.system('mencoder -oac pcm -ovc copy -o final.mp4' + filea)
    #fdata = open("list.txt","w+")
    #    fdata.write("file 'vidgen\\" + filename + "'\n")
    #    #-vcodec mpeg4 -b 30000 -vb 20M -vf "scale=1290:-1"
    #os.system("ffmpeg -f " + filea + " -c copy result.mov > output.txt 2> err.txt")
    sleep(0.4)
    os.system("ffmpeg -f concat -i list.txt -c copy final.mp4 > logs\\output.txt 2> logs\\err.txt")

    #os.system('ffmpeg -i "concat:1.flv|2.flv" -codec copy output.mkv > output.txt 2> err.txt')
#genmp4()
#genvideoclip()
genfinalvid()
