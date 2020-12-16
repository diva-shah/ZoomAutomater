#! python3
# zoomAutomater.py - A bot that joins and exits Zoom calls, as well as
# joining breakout rooms when prompted.

import datetime, time, os, re
import pyautogui, pprint, subprocess

os.chdir('.') # For good luck's sake

if os.path.exists('.//log.py') == True:
    print(';3')
    import log
else:
    print('''Usage warning: This bot will error if Zoom.exe is
not visible onto the screen window.
For that reason, this bot is not recommended
to be used if you're already using your computer,
as you'd constantly have to give screen space to Zoom.
CTRL-C ends the program prematurely, if you can't X it out.''')
    input()
    classtimes = {'Classes':[]}
    classlist = 0
    print('''Input the directory to Zoom.exe.
Ex. C:\\Users\John\Zoom.exe''')
    prezoomdir = input() 
    zoomRegex = re.compile('[/]')
    zoomdir = zoomRegex.sub('//', prezoomdir)
    print("Input the number of classes you wish to automate.")
    classnum = input()
    for x in range(0,int(classnum)):
        print('''Input the start time of your class in military time.
Ex: 13:25 or 00:25''')
        start = input()
        print('''Input the end time of your class in military time.
Ex: 15:55 or 02:55''')
        end = input()
        print('''Input the Zoom ID with no spaces.
Ex: 00000000000''')
        ID = input()
        print('''Input the Zoom Password.
Ex: 000000''')
        Pass = input()
        print("Class # " + str(x+1) + " logged.")
        classtimes['Classes'].append({'Class': str(x+1), 'Start': start, 'End': end,
                                      'ID': ID, 'Password': Pass})
        classlist = 1 + classlist
    print("Initializing...")
    scriptFile = open('log.py', 'w')
    scriptFile.write('classTimes = ' + pprint.pformat(classtimes) + '\n')
    scriptFile.write('classlist = ' + pprint.pformat(classnum) + '\n')
    scriptFile.write('zoomdir = ' + pprint.pformat(zoomdir) + '\n')
    scriptFile.close()
    import log

if subprocess.Popen(log.zoomdir).poll() == None:
    subprocess.Popen(log.zoomdir)

for x in range(0, int(log.classlist)):
    while True:
        a = datetime.datetime.strptime(log.classTimes['Classes'][x]['Start'], "%H:%M") # a is the stripped 'Start' time into Hours:Minutes int
        b = datetime.datetime.strptime(log.classTimes['Classes'][x]['End'], "%H:%M")   # b is the stripped 'End' time into Hours:Minutes int
        if datetime.datetime.now().hour >= a.hour and datetime.datetime.now().hour <= b.hour and datetime.datetime.now().minute >= a.minute:
            time.sleep(2)
            join = pyautogui.locateOnScreen('join.PNG')
            joincentered = pyautogui.center(join)
            pyautogui.click(joincentered)
            time.sleep(5) # Grace period for it to load
            pyautogui.typewrite(log.classTimes['Classes'][x]['ID'])
            pyautogui.typewrite('\n')
            time.sleep(5)
            pyautogui.typewrite(log.classTimes['Classes'][x]['Password'])
            pyautogui.typewrite('\n')
            while True:
                if pyautogui.locateOnScreen("zoomlogo.PNG") != None: ## add breakoutroom .png
                    pyautogui.typewrite('\n')
                elif datetime.datetime.now().hour > b.hour or datetime.datetime.now().hour == b.hour and datetime.datetime.now().minute > b.minute:
                    break
                else:
                    time.sleep(5)
            try:        
                while datetime.datetime.now().hour > b.hour or datetime.datetime.now().hour == b.hour and datetime.datetime.now().minute >= (b.minute-1): 
                    leave = pyautogui.locateOnScreen('leave.PNG')   # I tried to make it form this exact section on time, but for some reason, it always does it 
                    leavecentered = pyautogui.center(leave)         # one minute after b.minute's value. It doesn't even confirm when I subtract 1 from it. 
                    pyautogui.click(leavecentered)          
                    leave2 = pyautogui.locateOnScreen('leavemeeting.PNG')
                    leavecentered2 = pyautogui.center(leave2)
                    pyautogui.click(leavecentered2)
                    break
            except TypeError:   # In case the Zoom is terminated by the host
                break
            break
        else:
            time.sleep(10)

print("Freedom!!")
input()
