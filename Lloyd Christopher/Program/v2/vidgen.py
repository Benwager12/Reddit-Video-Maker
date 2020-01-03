#-----LunarHunter 2019-----#
#-----     Lloyd      -----#
#THE GENFINALVID DOES NOT WORK YET! DO NOT RUN!

import os, subprocess
def genmp4():
    counta = 0
    while counta < 30:
        os.system('ffmpeg -i temp\\' + str(counta) + '.png -i temp\\' + str(counta) + '.wav -b 30000 -vb 20M -vf "scale=1920:-1" vidgen\\' + str(counta) + '.flv > logs\\outputmp4.txt 2> logs\\errmp4.txt')
        counta = counta + 1
def genfinalvid():
    filea = ""
    fdata = open("list.txt","w+")
    for filename in os.listdir("vidgen\\"):
        filea = filea + " -i vidgen\\" + filename
        fdata.write("file 'vidgen\\" + filename + "'\n")
        #-vcodec mpeg4 -b 30000 -vb 20M -vf "scale=1290:-1"
    #os.system("ffmpeg -f " + filea + " -c copy result.mov > output.txt 2> err.txt")
    os.system("ffmpeg -f concat -safe 0 -i \"list.txt\" -c copy -y concat.mp4 > logs\\output.txt 2> logs\\err.txt")

#genmp4()
#genfinalvid()
