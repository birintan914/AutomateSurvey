from selenium import webdriver
from time import time,sleep

from selenium.webdriver import ActionChains
from speech_recognition import Microphone, Recognizer, UnknownValueError, RequestError
import pyautogui

"""
INITIALIZE:
"""
# Conect to CableA Output
recog = Recognizer()
mic = Microphone()
x = 0
for i in mic.list_microphone_names():
    if(i=="CABLE-A Output (VB-Audio Cable "):
        print(i)
        break
    x+=1
mic = Microphone(0)
driver = webdriver.Firefox()
driver.get(
    "http://209.202.72.54:81/1afa19ec-4463-4a90-a761-f2819dc688dd.php?fbclid=IwAR01ppskIaAZyMvPmWILccd7Ni52z6bj_ucRr3VyWjvIYTrgqrmbvsXgico")

"""
FUNCTIONS:
"""
vm = False

def login():
    # USER LOGIN
    user = driver.find_element_by_xpath("/html/body/form/center/table/tbody/tr[3]/td[2]/input")
    user.send_keys("birintank")
    userp = driver.find_element_by_xpath("/html/body/form/center/table/tbody/tr[4]/td[2]/input")
    userp.send_keys("password")

    login = driver.find_element_by_xpath("/html/body/form/center/table/tbody/tr[5]/td/input")
    login.click()

    phoneusr = driver.find_element_by_xpath("/html/body/form/center/table/tbody/tr[3]/td[2]/input")
    phoneusr.send_keys("834")
    phonepass = driver.find_element_by_xpath("/html/body/form/center/table/tbody/tr[4]/td[2]/input")
    phonepass.send_keys("kswiss23")


def write_unrecoq(results):
    undected_responses = ["hello", "Nothing"]
    if any(ext in results for ext in undected_responses):
        pass
    else:
        f = open("unrecoq.txt", "a+")
        s = results + "\n" + "\n"
        f.write(s)
        f.close()


def getSrc():
    try:
        imgXpath = driver.find_element_by_xpath("/html/body/form[1]/span[3]/table/tbody/tr/td[5]/img")
        src = imgXpath.get_attribute("src")
    except:
        src = "img not found"
    return src


def playIntro():
    sleep(0.3)
    pyautogui.press("b")
    return


def stopIntro():
    pyautogui.press("v")
    return


def hangup(type):
    try:

        element = driver.find_element_by_xpath(
            "/html/body/form[1]/span[5]/table/tbody/tr[3]/td[1]/font/center[2]/span[10]/a/img")
        element.click()
    except:
        print("hangup not found")
    sleep(1.35)

    if type == "am":
        answermachine()

    elif type == "ni":
        notin()


def notin():
    sleep(1.35)
    try:
        element_n = driver.find_element_by_xpath(
            "/html/body/form[1]/span[46]/table/tbody/tr/td/font[3]/span[5]/table/tbody/tr[2]/td[2]/font/span/font[2]/a")
        actionn = ActionChains(driver)
        actionn.double_click(element_n).perform()
    except:
        print("not interested: failed")


def answermachine():
    try:
        element_a = driver.find_element_by_xpath(
            "/html/body/form[1]/span[46]/table/tbody/tr/td/font[3]/span[5]/table/tbody/tr[2]/td[1]/font/span/font[1]/a")
        action = ActionChains(driver)
        action.double_click(element_a).perform()

    except:
        print("answer machine: except command")


def voicedialinput(time):
    with mic:
        audio = recog.record(mic, time)

    try:
        recognized = recog.recognize_google(audio)
        return recognized
    except:
        return "Nothing"


def checkCall(results):
    voicemail_dialogs = ["this phone is protected", "automated voice", "forwarded", "leave a message",
                         "Magic Jack customer", "unavailable to take", "please leave a message", "leave your message",
                         "voicemail", "missed your call", "record your message", "hang up", "you have reached",
                         "not available", "at the tone", "please call", "we are not", "robo", "forwarded", "automated",
                         "call has been", "google assistant", "the number", "1", "2", "3", "4", "5", "6", "7", "8", "9",
                         "number", "bitch", "robo caller", "google assistant", "your message for",
                         "your message at the",
                         "please leave a", "the person you called", "right back to you", "after the tone",
                         "please leave your",
                         "can't get to", "please leave", "not here right now", "we're not here",
                         "trying to reach", "voice mailbox", "not been setup", "you've reached", "back to you",
                         "leave your name",
                         "come to the", "can't take your call", "Google Assistant", "Google Assistant", "voice mailbox",
                         "leave me a", "voice message system", "I'm unavailable",
                         "no one is available to take your call",
                         "take your call", "no one is available", "take your call", "I'm unable", "not avail",
                         "away from",
                         "away from my phone", "for calling", "residence", "sorry we're not", "I'm sorry I can't",
                         "the mailbox", "voice messaging system", "thank you", "leaving message", "leave a message",
                         "sorry I can't", "the person you're calling", "I will call you back", "message system",
                         "dialled is not in service", "please try again", "can't answer", "call again later", "goodbye"
                                                                                                              "please try your",
                         "messaging system", "message system", "call back", "unable to answer",
                         "unavailable", "cannot be completed", "sorry I missed", "unable", "please", "hi this",
                         "hello this", "voice message", "Buddha Buddha", "hi this is", "goodbye goodbye", "you back",
                         "at this time", "this phone", "this is", "person you are calling", "I'm sorry", "leave us a message",
                         "this is", "sorry", "phone", "person", "mailbox is full", "leave message", "message", "siete"
                         ,"cuatro"]

    if any(ext in results for ext in voicemail_dialogs):
        global vm
        vm = True
        hangup("am")
    else:
        if not (results == "Nothing (Voicedial:exception)" or results == "hello"):
            write_unrecoq(results)
        print("UD: ")


def liveCall():
    src = getSrc()
    return src == "http://209.202.72.54/agc/images/agc_live_call_ON.gif"


"""
MAIN:
"""

try:
    login()
except:
    print("login failed")

sleep(25)
print("Beep Boop Beep")
while True:
    vm = False #VoiceMail

    print()
    src = getSrc()
    if liveCall():  # Call is live
        time_start = time()

        print("LIVE CALL: ")
        results1 = voicedialinput(3.5)
        checkCall(results1)
        print("first call: "+results1)
        if(vm==False):
            results1 = voicedialinput(3.7)
            checkCall(results1)
            print("second call: " + results1)
        while liveCall(): #and ((time() - time_start) < 15):
            pass
        stopIntro()


        # Call Ended
        if(vm==False and ((time() - time_start) < 25)):
            hangup("ni")



    else:
        print("Not in Call")
        while not liveCall():
            sleep(0.1)

