######################################################
#                                                    #
# Licensed under the GNU General Public License v3.0 #
#                                                    #
######################################################

from tkinter import *
import datetime

root = Tk()
root.wm_title("TikToq")

#definining time variables for realtime clock
oldtime = ''
nowtime = ''

#defining time variables for fast clock
hour = 0
minute = 0
second = 0

#initial fasttime condition
fasttime = False

#initial hexacode so code won't crash
hexcode = "FF00FF"

#defining time periods
now = datetime.datetime.now().time()   
morning = now.replace(hour = 12, minute = 0, second = 0, microsecond = 0)
evening = now.replace(hour = 18, minute = 0, second = 0, microsecond = 0)
timeLoop = 200
#testing which time period we're in
if (now < morning):
    w = Label(root, text = "Good Morning", bg = "green", fg = "black")
    w.pack(fill=BOTH)
elif (now < evening and now >= morning):
    w = Label(root, text = "Good Afternoon", bg = "green", fg = "black")
    w.pack(fill=BOTH)
else:
    w = Label(root, text = "Good Evening", bg = "green", fg = "black")
    w.pack(fill=BOTH)

destroy = False #It is there to start

#to deal with later 1 digit outputs
def pad(x):
    if len(x) == 1: #checks if hexpart output is one digit
        return("0" + x)
    else:
        return(x)

#inital condition of font colour
whatColour = "black"

#function for changing font colour
def colourChange():
    global whatColour
    if whatColour == "black":
        clock.config(fg = "white")
        hexlabel.config(fg = "white")
        w.config(fg = "white")
        whatColour = "white"
    else:
        clock.config(fg = "black")
        hexlabel.config(fg = "black")
        w.config(fg = "black")
        whatColour = "black"

#defining function that toggles fast time 
def fast():
    global fasttime
    if fasttime == False:
        fasttime = True
    else:
        fasttime = False
    
    global nowtime, hour, minute, second
    nowtime = datetime.datetime.now().time()
    hour = nowtime.hour
    minute = nowtime.minute
    second = nowtime.second

#main clockfunction from which other functions run
def tick():
    global hour, minute, second

    if fasttime == False:#for when in realtime setting current time
        global nowtime
        nowtime = datetime.datetime.now().time()
        hour = nowtime.hour
        minute = nowtime.minute
        second = nowtime.second

    else:#for when in fast time
        if second >= 59:
            second = 0
            minute += 1
        else:
            second += 0.5

        if minute > 59:
            minute = 0
            hour += 1
        

    #converting all 3 parts seperately to one part of hexcode
    #pad function will deal with 1 digit output
    
    #alternating increasing or decreasing seconds hexcode
    if minute%2==0:
        hexseconds = pad(hex(int(second * (16**2/60)))[2:])
    elif minute%2==1:
        hexseconds = pad(hex((16**2-1) - int(second * (16**2/60)))[2:])
        
    #alternating increasing or decreasing minutes hexcode
    if hour%2==0:
        hexminutes = pad(hex(int(minute * (16**2/60)))[2:])
    elif hour%2==1:
        hexminutes = pad(hex((16**2-1) - int(minute * (16**2/60)))[2:])
        
    hexhours = pad(hex(int(hour * (16**2/24)))[2:])

    hexcode = ("#" + hexhours + hexminutes + hexseconds)#produces the string that defines the background colour
    #print(hexcode)
    
    global destroy, timeLoop
    
    if fasttime == False: #for upgrading the background in realtime
        global oldtime
        # if time string has changed, update it
        if nowtime != oldtime:
            oldtime = nowtime
            clock.config(text=nowtime.strftime('%H:%M:%S'))
            clock.config(bg=hexcode)
            hexlabel.config(bg=hexcode)
            hexlabel.config(text=hexcode)
            textbutton.config(highlightbackground=hexcode)
            fastbutton.config(highlightbackground=hexcode)
            if destroy == False:
                w.config(bg=hexcode)

        if timeLoop == 0:
            destroy = True
            w.destroy()
        else:
            timeLoop -= 1
        # calls itself every 200 milliseconds
        # to update the time display as needed
        # could use >200 ms, but display gets jerky

    else:#for upgrading the background in fasttime
        clock.config(text=pad(str(hour)) + ':' + pad(str(minute)) + ':' + pad(str(round(second))))
        clock.config(bg=hexcode)
        hexlabel.config(bg=hexcode)
        hexlabel.config(text=hexcode)
        textbutton.config(highlightbackground=hexcode)
        fastbutton.config(highlightbackground=hexcode)
        if destroy == False:
            w.config(bg=hexcode)

        if timeLoop == 0:
            destroy = True
            w.destroy()
        else:
            timeLoop -= 1

        
    
    clock.after(50, tick)

clock = Label(root, font=("Ariel", 80), bg= "green", fg = "black")#styles for clock box
clock.pack(fill=BOTH, expand=1)
hexlabel = Label(root,font=("Ariel", 45), bg= "green", fg = "black")#styles for hexadecimal box
hexlabel.pack(fill=BOTH)#,expand=1)
fastbutton = Button(root, command=fast, text="Fast Mode", highlightbackground="green")#styles for fastbutton
fastbutton.pack(fill=BOTH)
textbutton = Button(root, text = "Toggle Font Colour", command= colourChange, highlightbackground= "green", relief= RAISED)
textbutton.pack(fill=BOTH)#styles for text button
root.geometry("500x300") #setting 
   
tick() #runs tick function
root.mainloop()#runs TKInter window
