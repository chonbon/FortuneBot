from bs4 import BeautifulSoup
from seleniumwire import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.proxy import Proxy, ProxyType
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.remote.remote_connection import LOGGER
from datetime import date,datetime
from pytz import timezone
from sys import executable
from playsound import playsound
from flask import Flask
from flask import request
from multiprocessing import Process
from subprocess import check_call
from threading import Thread
from tkinter import *
from PIL import ImageTk, Image
import tkinter.font as font
from PyQt5 import QtWidgets 
import logging,requests,json,time,os,stat,sys,multiprocessing,random,subprocess,tempfile,jwt,click,re

botVersion = "v0.2"

#JWT Secret
jwtSecret = 'fortunebotbychon'

if sys.platform == 'win32':
    # win
    CHROME_DRIVER_PATH = '.\\driver\\chromedriver.exe'
    assetFolder = ".\\assets\\"
    folder = ".\\User Data"
    folder2 = ".\\User Data\\Temp"
    filename = ".\\User Data\\tasks.json"
    filename1 = ".\\User Data\\profiles.json"
    filename2 = ".\\User Data\\webhook.json"
    filename3 = ".\\User Data\\proxies.txt"
    filename4 = ".\\User Data\\accounts.txt"
    filename5 = ".\\User Data\\settings.json"
else:
    # mac
    CHROME_DRIVER_PATH = './driver/chromedriver'
    assetFolder = "./assets/"
    folder = "./User Data"
    folder2 = "./User Data/Temp"
    filename = "./User Data/tasks.json"
    filename1 = "./User Data/profiles.json"
    filename2 = "./User Data/webhook.json"
    filename3 = "./User Data/proxies.txt"
    filename4 = "./User Data/accounts.txt"
    filename5 = "./User Data/settings.json"

# Discord stuff
API_ENDPOINT = 'https://discord.com/api/v8'
CLIENT_ID = '829097899501420605'
CLIENT_SECRET = 'MquIWhSPe6XD74lJ4UFrbB7o0YJXdIS3'
REDIRECT_URI = 'http://localhost:8080/'

# Path to file
def resource_path(relative_path: str) -> str:
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.dirname(__file__)
    return os.path.join(base_path, relative_path)

LOGGER.setLevel(logging.WARNING)

tempServer = Flask(__name__)
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

def secho(text, file=None, nl=None, err=None, color=None, **styles):
    pass

def echo(text, file=None, nl=None, err=None, color=None, **styles):
    pass

click.echo = echo
click.secho = secho

# Profile Module
def profileModule(mode,profile,position):
    #load profiles mode =1, save a new profile mode =2, delete profile is mode =3
    if mode == 1:
        try:
            with open(filename1, 'r') as json_file:
                json_file = json_file.read()
                #print(str(json_file))
                if len(json_file) != 0:
                    data = json.loads(json_file)
                    return data
                return False
        except FileNotFoundError:
            with open(filename1, 'w') as json_file:
                return False
    if mode == 2:
        data = {}
        with open(filename1, 'r') as json_file1:
            json_file1 = json_file1.read()
            #print(str(json_file1))
            if len(json_file1) != 0:
                data = json.loads(json_file1)
        with open(filename1, 'w') as json_file:
            if len(data) > 0:
                if position == -1:
                    data["profileList"].append(profile)
                else:
                    data['profileList'][position] = profile
                json.dump(data, json_file)
                print("Saved Profile!")
                return True
            data["profileList"] = [profile]
            json.dump(data, json_file)
            print("Saved Profile!")
            return True
    if mode == 3:
        data = {}
        with open(filename1, 'r') as json_file1:
            json_file1 = json_file1.read()
            #print(str(json_file1))
            if len(json_file1) != 0:
                data = json.loads(json_file1)
            for i in range(len(data["profileList"])):
                if data["profileList"][i]["profileName"] == profile:
                    data["profileList"].pop(i)
                    break
        with open(filename1, 'w') as json_file:
            json.dump(data, json_file)
            print("Deleted Profile!")
            return True

# Accounts Module
def accountsModule(mode,account):
    if mode == 1:
        try:
            with open(filename4, 'r') as json_file:
                accounts = []
                for line in json_file:
                    temp = line.split(':')
                    account = {
                            "email":temp[0],
                            "password":temp[1]
                        }
                    accounts.append(account)
                if accounts == []:
                    return False
                return accounts
        except FileNotFoundError:
            with open(filename4, 'w') as json_file:
                return False

# Settings Module
def settingsModule(mode,setting):
    if mode == 1:
        try:
            with open(filename5, 'r') as json_file:
                json_file = json_file.read()
                #print(str(json_file))
                if len(json_file) != 0:
                    data = json.loads(json_file)
                    return data
                return False
        except FileNotFoundError:
            with open(filename5, 'w') as json_file:
                return False
    if mode == 2:
        data = {}
        with open(filename5, 'r') as json_file1:
            json_file1 = json_file1.read()
            #print(str(json_file1))
            if len(json_file1) != 0:
                data = json.loads(json_file1)
        with open(filename5, 'w') as json_file:
            if len(data) > 0:
                data["forceCheckout"] = setting
                json.dump(data, json_file)
                print("Saved Setting!")
                return True
            data["forceCheckout"] = setting
            json.dump(data, json_file)
            return True
    if mode == 3:
        data = {}
        with open(filename5, 'r') as json_file1:
            json_file1 = json_file1.read()
            #print(str(json_file1))
            if len(json_file1) != 0:
                data = json.loads(json_file1)
        with open(filename5, 'w') as json_file:
            if len(data) > 0:
                data["headless"] = setting
                json.dump(data, json_file)
                return True
            data["headless"] = setting
            json.dump(data, json_file)
            return True
    if mode == 4:
        data = {}
        with open(filename5, 'r') as json_file1:
            json_file1 = json_file1.read()
            #print(str(json_file1))
            if len(json_file1) != 0:
                data = json.loads(json_file1)
        with open(filename5, 'w') as json_file:
            if len(data) > 0:
                data["key"] = setting
                json.dump(data, json_file)
                return True
            data["key"] = setting
            json.dump(data, json_file)
            return True
    if mode == 5:
        data = {}
        with open(filename5, 'r') as json_file1:
            json_file1 = json_file1.read()
            #print(str(json_file1))
            if len(json_file1) != 0:
                data = json.loads(json_file1)
        with open(filename5, 'w') as json_file:
            if len(data) > 0:
                data["queueTasks"] = setting
                json.dump(data, json_file)
                return True
            data["queueTasks"] = setting
            json.dump(data, json_file)
            return True
    if mode == 6:
        data = {}
        with open(filename5, 'r') as json_file1:
            json_file1 = json_file1.read()
            #print(str(json_file1))
            if len(json_file1) != 0:
                data = json.loads(json_file1)
        with open(filename5, 'w') as json_file:
            if len(data) > 0:
                data["qtProfile"] = setting
                json.dump(data, json_file)
                return True
            data["qtProfile"] = setting
            json.dump(data, json_file)
            return True

# Proxy Module
def proxyModule():
    try:
        with open(filename3, 'r') as json_file:
            #print(str(json_file))
            lines = []
            for line in json_file:
                temp = line.split(':')
                proxy = temp[2]+":"+temp[3]+'@'+temp[0]+":"+temp[1]
                lines.append("".join(proxy.splitlines()))
            if len(lines) == 0:
                return False
            return lines
    except FileNotFoundError:
        with open(filename3, 'w') as json_file:
            return False

# Webhook Module
def webhookModule(hitInfo, webhook, mode):

    # Send Webhook
    if mode == 1:
        hitInfo['decline'] = False
        webhookModule(hitInfo,None,6)
        orderUrl = "https://www.bestbuy.com/profile/ss/orders/order-details/"+hitInfo["order"]+"/view"
        #urls = ["https://discord.com/api/webhooks/812164510478499852/rIbrqb9JimJ7McpznS5lB9oY-aDznWcxzriwXWHT_tWYxwI-HBU7kCvYx7fjtA5No_TM","https://discord.com/api/webhooks/812177398191357992/oWcKfmtBnofVuWN2bMPUXh9zRzzjol6c7-EsbrMi0dN9oWMMO9R0HzALx1xsX9SrQCtN"]

        try:
            with open(filename2, 'r') as json_file:
                json_file = json_file.read()
                #print(str(json_file))
                if len(json_file) == 0:
                    print("Cant send Success, no webhooks!")
                    return False
                data = json.loads(json_file)
                urls = data["urls"]

        except FileNotFoundError:
            with open(filename2, 'w') as json_file:
                print("Cant send Success, no webhooks!")
                return False

        data = {
            "username": "FortuneBot"
        }

        data["embeds"] = [
            {
                "title" : "Checkout Successful - "+ str(hitInfo['item']),
                "fields": [
                        {
                            "value" : "Best Buy (Alpha)",
                            "name" : "Store",
                            "inline": True
                        },
                        {
                            "value" : "|| ["+hitInfo["order"]+"]("+orderUrl+") ||",
                            "name" : "Order #",
                            "inline": True
                        },
                        {
                            "value" : hitInfo["itemName"] ,
                            "name" : "Product"
                        },
                        {
                            "value" : hitInfo["q"] ,
                            "name" : "Quantity",
                            "inline": True
                        },
                        {
                            "value" : hitInfo["price"] ,
                            "name" : "Price",
                            "inline": True
                        },
                        {
                            "value" : "|| "+hitInfo["profile"]+" ||" ,
                            "name" : "Profile",
                            "inline": True
                        }
                 ],
                "footer":{ "text": botVersion },
                "thumbnail": {"url": hitInfo["itemUrl"]}
            }

        ]
        print("Sending success to webhook")
        for url in urls:
            result = requests.post(url, json = data)
            #print(str(result))
        return

    # View webhooks
    if mode == 2:
        try:
            with open(filename2, 'r') as json_file:
                json_file = json_file.read()
                #print(str(json_file))
                if len(json_file) != 0:
                    data = json.loads(json_file)
                    return data
                return False
        except FileNotFoundError:
            with open(filename2, 'w') as json_file:
                return False

    # Save webhook
    if mode == 3:
        data = {}
        try:
            with open(filename2, 'r') as json_file1:
                json_file1 = json_file1.read()
                #print(str(json_file1))
                if len(json_file1) != 0:
                    data = json.loads(json_file1)
        except FileNotFoundError:
            with open(filename2, 'w') as json_file:
                if len(data) > 0:
                    data["urls"].append(webhook)
                    json.dump(data, json_file)
                    print("Saved Webhook!")
                    return True
                data["urls"] = [webhook]
                json.dump(data, json_file)
                print("Saved Webhook!")
                return True
        with open(filename2, 'w') as json_file:
                if len(data) > 0:
                    data["urls"].append(webhook)
                    json.dump(data, json_file)
                    print("Saved Webhook!")
                    return True
                data["urls"] = [webhook]
                json.dump(data, json_file)
                print("Saved Webhook!")
                return True

    # Delete webhook
    if mode == 4:
        data = {}
        with open(filename2, 'r') as json_file1:
            json_file1 = json_file1.read()
            #print(str(json_file1))
            if len(json_file1) != 0:
                data = json.loads(json_file1)
                data["urls"].pop(int(webhook))
        with open(filename2, 'w') as json_file:
            json.dump(data, json_file)
            print("Deleted Webhook!")
            return True

    # Send Decline
    if mode == 5:
        hitInfo['decline'] = True
        webhookModule(hitInfo,None,6)
        try:
            with open(filename2, 'r') as json_file:
                json_file = json_file.read()
                #print(str(json_file))
                if len(json_file) == 0:
                    print("Cant send Success, no webhooks!")
                    return False
                data = json.loads(json_file)
                urls = data["urls"]

        except FileNotFoundError:
            with open(filename2, 'w') as json_file:
                print("Cant send Success, no webhooks!")
                return False

        data = {
            "username": "FortuneBot"
        }

        data["embeds"] = [
            {
                "title" : "Payment Declined - "+ str(hitInfo['item']),
                "fields": [
                        {
                            "value" : "Best Buy (Alpha)",
                            "name" : "Store",
                            "inline": True
                        },
                        {
                            "value" : hitInfo["itemName"] ,
                            "name" : "Product"
                        },
                        {
                            "value" : "|| "+hitInfo["profile"]+" ||" ,
                            "name" : "Profile",
                            "inline": True
                        }
                 ],
                "footer":{ "text": botVersion },
                "thumbnail": {"url": hitInfo["itemUrl"]}
            }

        ]
        print("Sending failure to webhook")
        for url in urls:
            result = requests.post(url, json = data)
            #print(str(result))
        return

    # public hook, every webhook
    if mode == 6:
        orderUrl = "https://www.bestbuy.com/profile/ss/orders/order-details/"+hitInfo["order"]+"/view"
        url = "https://discord.com/api/webhooks/827314007304044574/Fv4pS9SxDC36aPwVY1SAyJ-2Qi0a25mQOVyIlek-63diD8WGsowJ88V98YbDwXlq6Vnk"
        text = ""
        if hitInfo["decline"] == False:
            text = "Checkout Successful - "
        if hitInfo["decline"] == True:
            text = "Checkout Declined - "

        data = {
            "username": "FortuneBot"
        }

        data["embeds"] = [
            {
                "title" : text + str(hitInfo['item']),
                "fields": [
                        {
                            "value" : "Best Buy (Alpha)",
                            "name" : "Store",
                            "inline": True
                        },
                        {
                            "value" : "|| ["+hitInfo["order"]+"]("+orderUrl+") ||",
                            "name" : "Order #",
                            "inline": True
                        },
                        {
                            "value" : hitInfo["itemName"] ,
                            "name" : "Product"
                        },
                        {
                            "value" : hitInfo["q"] ,
                            "name" : "Quantity",
                            "inline": True
                        },
                        {
                            "value" : hitInfo["price"] ,
                            "name" : "Price",
                            "inline": True
                        },
                        {
                            "value" : "|| "+hitInfo["profile"]+" ||" ,
                            "name" : "Profile",
                            "inline": True
                        }
                 ],
                "footer":{ "text": botVersion },
                "thumbnail": {"url": hitInfo["itemUrl"]}
            }

        ]

        result = requests.post(url, json = data)
        return

# Task Mod Logic
def taskMod(task):
    running = True
    global tempFilename
    if sys.platform == 'win32':
        tempFilename = ".\\User Data\\Temp\\"+task["name"]+"Status.json"
    else:
        tempFilename = "./User Data/Temp/"+task["name"]+"Status.json"
    settings = settingsModule(1,None)
    if "forceCheckout" not in settings:
        settings["forceCheckout"] = False
        settingsModule(2,False)
    while running:
        taskStatus(None, -1)
        os.system('cls' if os.name == 'nt' else 'clear')
        if task['date'] != False:
            today = date.today().strftime("%m/%d/%Y")
            now = datetime.now(timezone('US/Eastern'))
            if task['date'] <= today:
                if task['date'] == today:
                    #task is today check for time
                    taskTime = datetime.strptime(task['time'], "%I:%M%p")
                    if taskTime.time() < now.time():
                        taskStatus("Running...",0)
                        result = bbSearchModule(task,None)
                        if result == True:
                            taskStatus("Item In Stock, attempting to checkout",0)
                            cart = bbCartModule(task['sku'],task,0)
                        if cart == True:
                            taskStatus("Successful Cart!",0)
                            running = False
                            break
                        if cart == False:
                            taskStatus("Error Carting",0)
                        if cart == None:
                            break

                        if settings['forceCheckout'] == True:
                            taskStatus("Forcing Cart and Checkout",0)
                            cart = bbCartModule(task['sku'],task,0)
                            if cart == True:
                                taskStatus("Successful Cart!",0)
                                running = False
                                break
                            if cart == False:
                                taskStatus("Force Carting did not work, trying again.",0)
                            if cart == None:
                                break
                        continue
                    taskStatus("Not Running...",0)
                    continue
                    taskStatus("Running Restock...",0)
                    result = bbSearchModule(task,None)
                    if result == True:
                        taskStatus("Item In Stock, Attemping to checkout",0)
                        cart = bbCartModule(task['sku'],task,0)
                        if cart == True:
                            taskStatus("Succesful Cart!",0)
                            running = False
                            break
                        if cart == False:
                            taskStatus("",0)
                        if cart == None:
                            break
                    if settings['forceCheckout'] == True:
                            taskStatus("Forcing Cart and Checkout!",0)
                            cart = bbCartModule(task['sku'],task,0)
                            if cart == True:
                                taskStatus("Succesful Cart!",0)
                                running = False
                                break
                            if cart == False:
                                taskStatus("Force Carting did not work, trying again.",0)
                            if cart == None:
                                break
                    time.sleep(1)
                    continue
                    #task was in the past, dont check for time and run
                taskStatus("Not Running Today...",0)    
            taskStatus("Running...",0)
            result = bbSearchModule(task,None)
            if result == True:
                taskStatus("Item In Stock, attempting to checkout",0)
                cart = bbCartModule(task['sku'],task,0)
                if cart == True:
                    taskStatus("Successful Cart!",0)
                    running = False
                    break
                if cart == False:
                    taskStatus("Error Carting",0)
                if cart == None:
                    break
                if settings['forceCheckout'] == True:
                    taskStatus("Forcing Cart and Checkout",0)
                    cart = bbCartModule(task['sku'],task,0)
                    if cart == True:
                        taskStatus("Succesful Cart!",0)
                        running = False
                        break
                    if cart == False:
                        taskStatus("Force Carting did not work, trying again.",0)
                    if cart == None:
                        break
            time.sleep(1)

def setTempfilename(tempfilename):
    global tempFilename
    tempFilename = tempfilename

# Status manager for task running
def taskStatus(status, id):
    temp = status
    global tempFilename
    #tempFilename = ".\\User Data\\status.json"
    if not os.path.exists(tempFilename):
        open(tempFilename, 'w').close()

    data = {"statusList":[]}

    settings = settingsModule(1,None)

    for i in range(int(settings["queueTasks"])+1):
        data["statusList"].append("")

    if id == -1:
        with open(tempFilename, 'w') as json_file1:
            json.dump(data, json_file1)
            return

    if id == -2:
        return
    with open(tempFilename, 'r') as  json_file:
        json_file = json_file.read()
        if len(json_file) != 0:
            data = json.loads(json_file)

    data["statusList"][id] = status

    with open(tempFilename, 'w') as json_file1:
        json.dump(data, json_file1)

    os.system('cls' if os.name == 'nt' else 'clear')
    for i in range(len(data["statusList"])):
        if data["statusList"][i] != "":
            print(data["statusList"][i])

    return

# returns statuslist from a task
def getTaskStatus(task):
    if sys.platform == 'win32':
        tempFilename = ".\\User Data\\Temp\\"+task["name"]+"Status.json"
    else:
        tempFilename = "./User Data/Temp/"+task["name"]+"Status.json"
    
    data = {}
    try:
        with open(tempFilename, 'r') as json_file:
            json_file = json_file.read()
            if len(json_file) != 0:
                data = json.loads(json_file)
                return data
            else:
                return False
    except FileNotFoundError:
        return False

# Saves Tasks to the file
def taskSaveModule(mode, task, position):
    #load tasks mode =1, save a new task mode =2, delete task is mode =3
    if mode == 1:
        try:
            with open(filename, 'r') as json_file:
                json_file = json_file.read()
                #print(str(json_file))
                if len(json_file) != 0:
                    data = json.loads(json_file)
                    return data
                return False
        except FileNotFoundError:
            with open(filename, 'w') as json_file:
                return False
    if mode == 2:
        data = {}
        with open(filename, 'r') as json_file1:
            json_file1 = json_file1.read()
            #print(str(json_file1))
            if len(json_file1) != 0:
                data = json.loads(json_file1)
        with open(filename, 'w') as json_file:
            if len(data) > 0:
                if position == -1:
                    data["taskList"].append(task)
                else:
                    data['taskList'][position] = task
                json.dump(data, json_file)
                print("Saved Task!")
                return True
            data["taskList"] = [task]
            json.dump(data, json_file)
            print("Saved Task!")
            return True
    if mode == 3:
        data = {}
        with open(filename, 'r') as json_file1:
            json_file1 = json_file1.read()
            #print(str(json_file1))
            if len(json_file1) != 0:
                data = json.loads(json_file1)
            data["taskList"].pop(position)
        with open(filename, 'w') as json_file:
            json.dump(data, json_file)
            print("Deleted Task!")
            return True

# Best Buy Search Module
def bbSearchModule(sku,proxy):
    startTime = time.time()
    #print("Searching for " + str(sku))
    baseUrl = "https://www.bestbuy.com/site/searchpage.jsp?st="+sku['sku']+"&_dyncharset=UTF-8&_dynSessConf=&id=pcat17071&type=page&sc=Global&cp=1&nrp=&sp=&qp=&list=n&af=true&iht=y&usc=All+Categories&ks=960&keys=keys"
    headers = {
        'authority':'www.bestbuy.com',
        'accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'referer':baseUrl,
        'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36'}
    #run proxy
    if proxy != None:
        #print("running with proxy: "+ str(proxy))
        proxies = {
        "http":"http://"+proxy
        }
        try:
            page = requests.get(baseUrl,headers=headers,proxies=proxies)
        except:
            print("Request Refused")
            return False
    #run local
    if proxy == None:
        try:
            page = requests.get(baseUrl,headers=headers)
        except:
            print("Request Refused")
            return False

    if page.status_code == 200:
        soup = BeautifulSoup(page.content, 'html.parser')
        #print(soup)

        # Check if item matches
        item = soup.find('div', class_ = 'list-item lv')

        if item != None:
            if item.attrs.get('data-sku-id') == str(sku['sku']):
                #print("Found Item!")
                # Check if in stock and able to be carted
                cartButton = item.find('button', class_ = 'btn btn-primary btn-sm btn-block btn-leading-ficon add-to-cart-button')
                if cartButton != None:
                    print(sku['name']+"               Item In Stock",end='\r')
                    return True
                os.system('cls' if os.name == 'nt' else 'clear')
                print(sku['name']+"               OOS",end='\r')
                return False
            print("No item found with "+str(sku))
            return 
        
        item = soup.find('button', class_ = 'btn btn-disabled btn-lg btn-block add-to-cart-button')
        if item != None:
            os.system('cls' if os.name == 'nt' else 'clear')
            print(sku['name']+"               OOS",end='\r')
            return False
        item = soup.find('button', class_ = 'btn btn-secondary btn-lg btn-block add-to-cart-button')
        if item != None:
            print(sku['name']+"               Check Stores, OOS or In store only",end='\r')
            return False

        item = soup.find('button', class_ = 'btn btn-primary btn-lg btn-block btn-leading-ficon add-to-cart-button')
        if item != None:
            print(sku['name']+"               Item In Stock",end='\r')
            return True

        print("No item found with "+str(sku))
        return False
    print("Search Failed: "+str(page.status_code))
    return False

# Best Buy Cart Module
def bbCartModule(sku,billing,id):
    global tempFilename
    if sys.platform == 'win32':
        tempFilename = ".\\User Data\\Temp\\"+billing["name"]+"Status.json"
    else:
        tempFilename = "./User Data/Temp/"+billing["name"]+"Status.json"

    settings = settingsModule(1,None)
    proxies = proxyModule()

    startTime = time.time()

    guestCheckoutFlag = True
    launchedQueueTasks = False
    qtToBuy = int(billing['quantity'])
    tempPurchaseAmount = 1

    running = True
    
    userAgentList = ['Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
                     'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.53 Safari/537.36',
                     'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36',
                     'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.110 Safari/537.36',
                     ('Mozilla/5.0 (X11; Linux x86_64) '
                     'AppleWebKit/537.36 (KHTML, like Gecko) '
                     'Chrome/63.0.3239.108 '
                     'Safari/537.36'),
                     ]

    if "headless" not in settings:
        settings["headless"] = False
        settingsModule(3,False)
    if "queueTasks" not in settings:
        settings["queueTasks"] = 1
        settingsModule(5,1)
    if "storePickup" not in billing:
        billing["storePickup"] = False

    options = webdriver.ChromeOptions()

    if settings["headless"] == False:
        options.add_argument('--headless')
        options.add_argument('--disable-gpu')
        options.add_argument("--log-level=3")
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        options.add_argument('--window-size=1920,1080')
        options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36")

    options.add_experimental_option('excludeSwitches', ['enable-logging'])

    if proxies != False:
        proxy = random.choice(proxies)
        soptions = {
            'proxy':{
                'http':"http://"+proxy,
                'https':"https://"+proxy,
                'no_proxy': 'localhost,127.0.0.1'
                }
        }
        driver = webdriver.Chrome(resource_path(CHROME_DRIVER_PATH),options=options,seleniumwire_options=soptions)
    else:
        driver = webdriver.Chrome(resource_path(CHROME_DRIVER_PATH),options=options)

    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

    if id != 0:
        st = taskStatus("Queue Task "+str(id)+" starting...",id)

    driver.get("https://bestbuy.com/")

    driver.execute_cdp_cmd('Network.setUserAgentOverride', {"userAgent": random.choice(userAgentList)})

    if id == 0:
        # Add To cart link
        st = taskStatus("Adding to Cart!",id)
        driver.get("https://api.bestbuy.com/click/-/"+str(sku)+"/cart")

    while running:
        # Check for checkout button
        try:
            checkoutButton = WebDriverWait(driver, 7).until(EC.presence_of_element_located((By.CSS_SELECTOR, "button[class='btn btn-lg btn-block btn-primary']")))
        except TimeoutException:
            # Might be Queue
            if id == 0:
                st = taskStatus("Unable To Cart link, trying for queue",id)
                
            baseUrl = "https://www.bestbuy.com/site/searchpage.jsp?st="+str(sku)+"&_dyncharset=UTF-8&_dynSessConf=&id=pcat17071&type=page&sc=Global&cp=1&nrp=&sp=&qp=&list=n&af=true&iht=y&usc=All+Categories&ks=960&keys=keys"
            driver.get(baseUrl)
            driver.execute_cdp_cmd('Network.setUserAgentOverride', {"userAgent": random.choice(userAgentList)})
            try:
                productPage = WebDriverWait(driver,3).until(EC.presence_of_element_located((By.CSS_SELECTOR, "span[class='c-accordion-trigger-label']")))
            except TimeoutException:
                try:
                    productLink = WebDriverWait(driver,3).until(EC.presence_of_element_located((By.CSS_SELECTOR, "a[class='image-link']")))
                    link = productLink.get_attribute("href")
                    driver.get(link)
                except TimeoutException:
                    st = taskStatus("Error Occured",id)
                    return False

            try:
                addToCartButton = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "button[class='btn btn-primary btn-lg btn-block btn-leading-ficon add-to-cart-button']")))
            except TimeoutException:
                st = taskStatus("Check Stores, OOS or In store only.",id)
                return False
            st = taskStatus("Trying to enter queue",id)
            ActionChains(driver).click(addToCartButton).perform()

            # check for queue error
            try:
                qAlert = WebDriverWait(driver, 7).until(EC.presence_of_element_located((By.CSS_SELECTOR, "div[class='c-alert-content']")))
            except TimeoutException:
                st = taskStatus("Entering Queue took too long, wait to try again or use fresh proxies.",id)
                return False

            if id == 0:
                if settings["queueTasks"] > 1 and launchedQueueTasks != True:
                    st = taskStatus("Handing off task to queue tasks",id)
                    for i in range(int(settings['queueTasks'])-1):
                        p = multiprocessing.Process(target=bbCartModule, args=[sku,billing,i+1])
                        p.start()
                        time.sleep(.75)
                    launchedQueueTasks = True
            inQueue = True
            st = taskStatus("In Queue....",id)

            while inQueue:
                color = addToCartButton.value_of_css_property("background-color")
                #print(str(color))
                if str(color) != "rgba(197, 203, 213, 1)":
                    st = taskStatus("Your Turn in the queue!",id)
                    inQueue = False
                    
            time.sleep(1)
            carting = True

            while carting:
                st = taskStatus("Trying to cart!",id)
                ActionChains(driver).click(addToCartButton).perform()

                try:
                    cartButton = WebDriverWait(driver,5).until(EC.presence_of_element_located((By.CSS_SELECTOR, "div[class='dot']")))
                    if cartButton.text != "0":
                        carting = False
                except TimeoutException:
                    st = taskStatus("Did not cart, trying again",id)
                time.sleep(random.choice([1,1.5,2]))

            driver.get("https://www.bestbuy.com/cart")
            try:
                checkoutButton = WebDriverWait(driver, 7).until(EC.presence_of_element_located((By.CSS_SELECTOR, "button[class='btn btn-lg btn-block btn-primary']")))
            except TimeoutException:
                st = taskStatus("Error, Couldnt cart after queue",id)
                return False
        #QT check
        if qtToBuy > 1:
            try:
                qtSelect = Select(WebDriverWait(driver, 2).until(EC.presence_of_element_located((By.CSS_SELECTOR, "select[class='c-dropdown v-medium fluid-item__quantity']"))))
            except TimeoutException:
                st = taskStatus("Unable to select Quantity",id)

            if int(billing['quantity']) >= (len(qtSelect.options)):
                temp = len(qtSelect.options)-2
                qtSelect.select_by_index(temp)
                tempPurchaseAmount = temp
                st = taskStatus("Max QT per Checkout is "+str(temp),id)
                time.sleep(1)
            if int(billing['quantity']) < (len(qtSelect.options)):
                qtSelect.select_by_visible_text(str(qtToBuy))
                tempPurchaseAmount = qtToBuy
                st = taskStatus("Able to checkout with requested amount of ",id)
                running = False
                time.sleep(1)

        # Click checkout
        st = taskStatus("Checking Out!",id)
        ActionChains(driver).click(checkoutButton).perform()

        
        try:
            buttonParent = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "div[class='button-wrap ']")))
        except TimeoutException:
            st = taskStatus("Gotta try and check out again",id)
            # Check for checkout button
            try:
                checkoutButton = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "button[class='btn btn-lg btn-block btn-primary']")))
            except TimeoutException:
                st = taskStatus("Unable To Cart",id)
                return False 
            # Click checkout
            st = taskStatus("Checking Out!",id)
            ActionChains(driver).click(checkoutButton).perform()

            try:
                buttonParent = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "div[class='button-wrap ']")))
            except TimeoutException:
                st = taskStatus("Unable to Checkout, maybe oos?",id)
                return False


        # Determine if we can guest checkout or log in
        try:
            guestCheckout = WebDriverWait(driver, 4).until(EC.presence_of_element_located((By.CSS_SELECTOR, "button[class='btn btn-secondary btn-lg cia-guest-content__continue guest']")))
            st = taskStatus("Guest Checkout",id)
            ActionChains(driver).click(guestCheckout).perform()
        except:
            st = taskStatus("Guest Checkout Not Available",id)
            try:
                st = taskStatus("Signing In",id)
                accounts = accountsModule(1,None)
                if accounts == False:
                    st = taskStatus("Couldnt sign in, no accounts in /User Data/accounts.txt",id)
                    return
                email = driver.find_element_by_css_selector("input[id='fld-e']")
                email.send_keys(accounts[0]['email'])
                password = driver.find_element_by_css_selector("input[id='fld-p1']")
                password.send_keys(accounts[0]['password'])
                signIn = driver.find_element_by_css_selector("button[class='btn btn-secondary btn-lg btn-block btn-leading-ficon c-button-icon c-button-icon-leading cia-form__controls__submit ']")
                ActionChains(driver).click(signIn).perform()
                guestCheckoutFlag = False

                #check for verification code
                try:
                    verifyButton = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, "button[data-track='Forgot Password - Continue']")))
                    st = taskStatus("You need to verify your account, a code has been sent to your email.",id)
                    playsound(resource_path(assetFolder+'decline.wav'))
                    #playsound('.//assets//verify.wav')
                    print("Enter Code Below",flush=True)
                    code = input()
                    print("Testing code "+code)
                    verifyInput = driver.find_element_by_css_selector("input[id='verificationCode']")
                    verifyInput.send_keys(code)
                    ActionChains(driver).click(verifyButton).perform()
               
                    try:
                        error = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, "div[class='c-alert-icon']")))
                        st = taskStatus("Incorrect or expired code, restarting flow",id)
                        return False
                    except TimeoutException:
                        st = taskStatus("Correct Code, moving on",id)

                except TimeoutException:
                    st = ""

            except TimeoutException:
                st = taskStatus("Checkout Flow Error",id)
                return False
        
        # Wait for ispu switch
        try:
            ispuSwitch = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, "a[class='ispu-card__switch']")))
            if ispuSwitch.text == "Switch to Shipping":
                if billing["storePickup"] != True:
                    st = taskStatus("Changing from store pickup to ship to home",id)
                    ActionChains(driver).click(ispuSwitch).perform()
            else:
                if billing["storePickup"]:
                    st = taskStatus("Changing from shipping to Store pickup",id)
                    ActionChains(driver).click(ispuSwitch).perform()
        except TimeoutException:
            st = taskStatus("Unable to switch fulfilment",id)
            #return

        if billing["storePickup"]:

            if guestCheckoutFlag:
                try:
                    st = taskStatus("Updating store location",id)
                    changeStore = WebDriverWait(driver,5).until(EC.presence_of_element_located((By.CSS_SELECTOR, "a[data-track='Change Store']")))
                    ActionChains(driver).click(changeStore).perform()

                    time.sleep(.7)

                    updateLocation = WebDriverWait(driver,5).until(EC.presence_of_element_located((By.CSS_SELECTOR, "div[class='css-1dbjc4n r-1awozwy r-18u37iz r-1777fci']")))
                    ActionChains(driver).click(updateLocation).perform()

                    time.sleep(1)

                    zipInput = driver.find_element_by_css_selector("input[class='css-1cwyjr8 r-14lw9ot r-pul571 r-z2wwpe r-rs99b7 r-1orvn2u r-dta0w2 r-a023e6 r-zso239 r-1ffoksr r-rjfia']")
                    zipInput.send_keys(billing['profile']['billZip'])

                    updateButton = driver.find_element_by_css_selector("div[data-update-button='update']")
                    ActionChains(driver).click(updateButton).perform()

                    time.sleep(2)

                    storeOptions = driver.find_elements_by_css_selector("div[class='css-1dbjc4n r-oucylx r-qklmqi']")
                    ActionChains(driver).click(storeOptions[0]).perform()
                    time.sleep(.5)

                    selectLocationButton = driver.find_element_by_css_selector("div[data-test-id='select-store-button']")
                    ActionChains(driver).click(selectLocationButton).perform()
                    time.sleep(2)
                except:
                    st = taskStatus("Unable to change to closest store",id)
                    return False

                st = taskStatus("Autofill email",id)

                email = WebDriverWait(driver, 1).until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[id='user.emailAddress']")))
                email.send_keys(billing['profile']['email'])
                phone = driver.find_element_by_css_selector("input[id='user.phone']")
                phone.send_keys(billing['profile']['phone'])

                continuePayment = driver.find_element_by_css_selector("button[class='btn btn-lg btn-block btn-secondary']")
                ActionChains(driver).click(continuePayment).perform()

                try:
                    ccNum = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[id='optimized-cc-card-number']")))
                except TimeoutException:
                    st = taskStatus("Timed out",id)
                    return False
                st = taskStatus("Autofill payment",id)

                ccNum.send_keys(billing['profile']['cc'])
                ccMM = Select(driver.find_element_by_css_selector("select[name='expiration-month']"))
                ccMM.select_by_visible_text(billing['profile']['ccExpMM'])
                ccYYYY = Select(driver.find_element_by_css_selector("select[name='expiration-year']"))
                ccYYYY.select_by_visible_text(billing['profile']['ccExpYYYY'])
                ccSC = driver.find_element_by_css_selector("input[id='credit-card-cvv']")
                ccSC.send_keys(billing['profile']['cvv'])

                total = driver.find_elements_by_css_selector("div[class='order-summary__price']")
                total = total[len(total)-1].text
                picUrl = driver.find_element_by_css_selector("img[class='item-list__image-content']").get_attribute("src")
                name = driver.find_element_by_css_selector("h4[class='item-list__spacer text-left item-list__title']").text

                fName = driver.find_element_by_css_selector("input[id='payment.billingAddress.firstName']")
                fName.send_keys(billing['profile']['fName'])
                lName = driver.find_element_by_css_selector("input[id='payment.billingAddress.lastName']")
                lName.send_keys(billing['profile']['lName'])
                addy1 = driver.find_element_by_css_selector("input[id='payment.billingAddress.street']")
                addy1.send_keys(billing['profile']['billStreet1'])
                try:
                    hideSuggestions = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "button[class='autocomplete__toggle']")))
                except TimeoutException:
                    st = taskStatus("Timed out",id)
                    return False
                #hideSuggestions.click()
                ActionChains(driver).click(hideSuggestions).perform()
                if billing['profile']['billStreet2'] != "":
                    try:
                        addy2Span = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "button[class='btn btn-link v-medium address-form__showAddress2Link']")))
                    except TimeoutException:
                        st = taskStatus("Timed out",id)
                        return False
                    ActionChains(driver).click(addy2Span).perform()
                    #addy2Span.click()

                    try:
                        addy2 = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[id='payment.billingAddress.street2']")))
                    except TimeoutException:
                        st = taskStatus("Timed out",id)
                        return False

                    addy2.send_keys(billing['profile']['billStreet2'])

                city = driver.find_element_by_css_selector("input[id='payment.billingAddress.city']")
                city.send_keys(billing['profile']['billCity'])
                state = Select(driver.find_element_by_css_selector("select[id='payment.billingAddress.state']"))
                state.select_by_visible_text(billing['profile']['billState'])
                zip = driver.find_element_by_css_selector("input[id='payment.billingAddress.zipcode']")
                zip.send_keys(billing['profile']['billZip'])

                st = taskStatus("Placing Order",id)
                placeButton = driver.find_element_by_css_selector("button[class='btn btn-lg btn-block btn-primary']")
                ActionChains(driver).click(placeButton).perform()

                stopTime = time.time()

            else:
                try:
                    ispuSwitch = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, "a[class='btn-default-link link-styled-button ispu-card__switch']")))
                    if ispuSwitch.text != "Switch to Shipping":
                        st = taskStatus("Changing from shipping to Store pickup",id)
                        ActionChains(driver).click(ispuSwitch).perform()
                    try:
                        st = taskStatus("Updating store location",id)
                        changeStore = WebDriverWait(driver,5).until(EC.presence_of_element_located((By.CSS_SELECTOR, "a[data-track='Store Availability: Change Location']")))
                        ActionChains(driver).click(changeStore).perform()

                        time.sleep(1)

                        zipInput = driver.find_element_by_css_selector("input[class='css-1cwyjr8 r-14lw9ot r-pul571 r-z2wwpe r-rs99b7 r-1orvn2u r-dta0w2 r-a023e6 r-zso239 r-1ffoksr r-rjfia']")
                        zipInput.send_keys(billing['profile']['billZip'])

                        updateButton = driver.find_element_by_css_selector("div[data-update-button='update']")
                        ActionChains(driver).click(updateButton).perform()

                        time.sleep(2)

                        storeOptions = driver.find_elements_by_css_selector("div[class='css-1dbjc4n r-oucylx r-qklmqi']")
                        ActionChains(driver).click(storeOptions[0]).perform()
                        time.sleep(.5)

                        selectLocationButton = driver.find_element_by_css_selector("div[data-test-id='select-store-button']")
                        ActionChains(driver).click(selectLocationButton).perform()
                        time.sleep(2)
                    except:
                        st = taskStatus("No store within 250 miles",id)
                        return False
                except TimeoutException:
                    st = taskStatus("Unable to switch fulfilment",id)
                    #return

        else:
            if guestCheckoutFlag != True:
                try:
                    addNewAddy = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "button[class='btn-default-link saved-addresses__add-new-link']")))
                    ActionChains(driver).click(addNewAddy).perform()
                    st = taskStatus("Adding new address",id)
                except TimeoutException:
                    st = ""

                try:
                    st = taskStatus("Autofill address info",id)
                    saveAddress = WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.CSS_SELECTOR, "button[class='address-form-modal__btn btn-secondary btn-block btn-lg btn btn-default']")))
                    time.sleep(1)
                    fName = driver.find_element_by_css_selector("input[id='ui.address.firstName']")
                    fName.send_keys(billing['profile']['fName'])
                    lName = driver.find_element_by_css_selector("input[id='ui.address.lastName']")
                    lName.send_keys(billing['profile']['lName'])
                    addy1 = driver.find_element_by_css_selector("input[id='ui.address.street']")
                    addy1.send_keys(billing['profile']['billStreet1'])
                    try:
                        hideSuggestions = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "button[class='autocomplete__toggle']")))
                    except TimeoutException:
                        st = taskStatus("Timed out",id)
                        return False
                    #hideSuggestions.click()
                    ActionChains(driver).click(hideSuggestions).perform()
                    if billing['profile']['billStreet2'] != "":
                        try:
                            addy2Span = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "button[class='btn btn-link v-medium address-form__showAddress2Link']")))
                        except TimeoutException:
                            st = taskStatus("Timed out",id)
                            return False
                        ActionChains(driver).click(addy2Span).perform()
                        #addy2Span.click()

                        try:
                            addy2 = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[id='ui.address.street2']")))
                        except TimeoutException:
                            st = taskStatus("Timed out",id)
                            return False

                        addy2.send_keys(billing['profile']['billStreet2'])

                    city = driver.find_element_by_css_selector("input[id='ui.address.city']")
                    city.send_keys(billing['profile']['billCity'])
                    state = Select(driver.find_element_by_css_selector("select[id='ui.address.state']"))
                    state.select_by_visible_text(billing['profile']['billState'])
                    zip = driver.find_element_by_css_selector("input[id='ui.address.zipcode']")
                    zip.send_keys(billing['profile']['billZip'])

                    saveAddress = WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.CSS_SELECTOR, "button[class='address-form-modal__btn btn-secondary btn-block btn-lg btn btn-default']")))
                    ActionChains(driver).click(saveAddress).perform()

                    time.sleep(5)
                    addCard = driver.find_element_by_partial_link_text("Use a different card")
                    ActionChains(driver).click(addCard).perform()

                    addNewCard = WebDriverWait(driver, 2).until(EC.presence_of_element_located((By.CSS_SELECTOR, "button[data-track='Payment Method: Add a new card']")))
                    ActionChains(driver).click(addNewCard).perform()
                
                    st = taskStatus("Autofill payment",id)

                    ccNum = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[id='optimized-cc-card-number']")))

                    ccNum.send_keys(billing['profile']['cc'])
                    ccMM = Select(driver.find_element_by_css_selector("select[name='expiration-month']"))
                    ccMM.select_by_visible_text(billing['profile']['ccExpMM'])
                    ccYYYY = Select(driver.find_element_by_css_selector("select[name='expiration-year']"))
                    ccYYYY.select_by_visible_text(billing['profile']['ccExpYYYY'])
                    ccSC = driver.find_element_by_css_selector("input[id='credit-card-cvv']")
                    ccSC.send_keys(billing['profile']['cvv'])

                    saveCard = WebDriverWait(driver, 4).until(EC.presence_of_element_located((By.CSS_SELECTOR, "button[class='btn btn-lg btn-block btn-secondary']")))
                    ActionChains(driver).click(saveCard).perform()

                    total = driver.find_elements_by_css_selector("div[class='order-summary__price']")
                    total = total[len(total)-1].text
                    picUrl = driver.find_element_by_css_selector("img[class='item-list__image-content']").get_attribute("src")
                    name = driver.find_element_by_css_selector("h4[class='item-list__spacer text-left item-list__title']").text

                    st = taskStatus("Placing Order",id)
                    placeButton = driver.find_element_by_css_selector("button[class='btn btn-lg btn-block btn-primary button__fast-track']")
                    time.sleep(1.5)
                    ActionChains(driver).click(placeButton).perform()

                    stopTime = time.time()

                except TimeoutException:
                    st = taskStatus("ERROR with sign in checkout",id)
                    return False
            else:
                inputNum = "2"
                # Wait for First Name field, sometimes delayed
                try:
                    fName = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[id='consolidatedAddresses.ui_address_"+inputNum+".firstName']")))
                    fName.send_keys(billing['profile']['fName'])

                except TimeoutException:
                    st = taskStatus("Best Buy antibot measures detected",id)
                    try:
                        inputNum = "5"
                        fName = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[id='consolidatedAddresses.ui_address_"+inputNum+".firstName']")))
                        fName.send_keys(billing['profile']['fName'])
                    except TimeoutException:
                        st = taskStatus("Error with name input fields",id)
                        return False
     
                lName = driver.find_element_by_css_selector("input[id='consolidatedAddresses.ui_address_"+inputNum+".lastName']")
                lName.send_keys(billing['profile']['lName'])

                email = WebDriverWait(driver, 1).until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[id='user.emailAddress']")))
                email.send_keys(billing['profile']['email'])

                addy1 = driver.find_element_by_css_selector("input[id='consolidatedAddresses.ui_address_"+inputNum+".street']")
                addy1.send_keys(billing['profile']['billStreet1'])
                try:
                    hideSuggestions = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "button[class='autocomplete__toggle']")))
                except TimeoutException:
                    st = taskStatus("Timed out",id)
                    return False
                #hideSuggestions.click()
                ActionChains(driver).click(hideSuggestions).perform()
                #if need second line of address
                if billing['profile']['billStreet2'] != "":
                    try:
                        addy2Span = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "button[class='btn btn-link v-medium address-form__showAddress2Link']")))
                    except TimeoutException:
                        st = taskStatus("Timed out",id)
                        return False
                    ActionChains(driver).click(addy2Span).perform()
                    #addy2Span.click()

                    try:
                        addy2 = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[id='consolidatedAddresses.ui_address_"+inputNum+".street2']")))
                    except TimeoutException:
                        st = taskStatus("Timed out",id)
                        return False

                    addy2.send_keys(billing['profile']['billStreet2'])

                city = driver.find_element_by_css_selector("input[id='consolidatedAddresses.ui_address_"+inputNum+".city']")
                city.send_keys(billing['profile']['billCity'])
                state = Select(driver.find_element_by_css_selector("select[id='consolidatedAddresses.ui_address_"+inputNum+".state']"))
                state.select_by_visible_text(billing['profile']['billState'])
                zip = driver.find_element_by_css_selector("input[id='consolidatedAddresses.ui_address_"+inputNum+".zipcode']")
                zip.send_keys(billing['profile']['billZip'])
  
                phone = driver.find_element_by_css_selector("input[id='user.phone']")
                phone.send_keys(billing['profile']['phone'])

                continuePayment = driver.find_element_by_css_selector("button[class='btn btn-lg btn-block btn-secondary']")
                ActionChains(driver).click(continuePayment).perform()

                try:
                    ccNum = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[id='optimized-cc-card-number']")))
                except TimeoutException:
                    st = taskStatus("Timed out",id)
                    return False
                st = taskStatus("Autofill payment",id)

                ccNum.send_keys(billing['profile']['cc'])
                ccMM = Select(driver.find_element_by_css_selector("select[name='expiration-month']"))
                ccMM.select_by_visible_text(billing['profile']['ccExpMM'])
                ccYYYY = Select(driver.find_element_by_css_selector("select[name='expiration-year']"))
                ccYYYY.select_by_visible_text(billing['profile']['ccExpYYYY'])
                ccSC = driver.find_element_by_css_selector("input[id='credit-card-cvv']")
                ccSC.send_keys(billing['profile']['cvv'])

                total = driver.find_elements_by_css_selector("div[class='order-summary__price']")
                total = total[len(total)-1].text
                picUrl = driver.find_element_by_css_selector("img[class='item-list__image-content']").get_attribute("src")
                name = driver.find_element_by_css_selector("h4[class='item-list__spacer text-left item-list__title']").text

                st = taskStatus("Placing Order",id)
                placeButton = driver.find_element_by_css_selector("button[class='btn btn-lg btn-block btn-primary']")
                ActionChains(driver).click(placeButton).perform()

                stopTime = time.time()

        alert = None 

        try:
            alert = WebDriverWait(driver, 8).until(EC.presence_of_element_located((By.CSS_SELECTOR, "div[class='order-errors']")))
        except TimeoutException:
            st = taskStatus("No Errors!",id)
        
        if alert != None:
            cardDeclineText = "Unfortunately, we were unable to process your credit card. Please try again or use a different card to continue with your order. For questions regarding your credit card, please contact your bank."
            maxQtLimitText = "If you have other items you'd like to buy, you'll need to remove this item to continue."
            st = taskStatus("Order Error!",id)
            if cardDeclineText == driver.find_element_by_css_selector("div[class='error-spacing']").text:
                st = taskStatus("Card Declined",id)
                hitInfo = {
                "item": sku,
                "itemName": name,
                "itemUrl": picUrl,
                "order": "",
                "price": total,
                "q": tempPurchaseAmount,
                "profile": billing['profile']['profileName']
                }
                webhookModule(hitInfo,{},5)
                playsound(resource_path(assetFolder+'decline.wav'))
                return
            if maxQtLimitText == driver.find_element_by_css_selector("div[class='error-spacing']").text:
                st = taskStatus("Max Items reached for this profile and sku",id)
                return
            st = taskStatus("Max Items reached for this profile and sku",id)
            return
            return False

        order = ""
        try:
            test = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "span[class='thank-you-enhancement__emphasis']")))
        except TimeoutException:
            st = taskStatus("Timed out",id)
        order = test[2].text
    
        hitInfo = {
            "item": sku,
            "itemName": name,
            "itemUrl": picUrl,
            "order": order.replace("Order #", ''),
            "price": total,
            "q": tempPurchaseAmount,
            "profile": billing['profile']['profileName']
            }
        webhookModule(hitInfo,{},1)
        playsound(resource_path(assetFolder+'success.mp3'))
        st = taskStatus("Checkout Successful! Total = " + total + " & took " + str(stopTime-startTime),id)
        qtToBuy -= tempPurchaseAmount
        if qtToBuy == 0:
            st = taskStatus("",-2)
            return True
    return True

# Newegg Search Module
def neweggSearchModule(model,proxy):
    startTime = time.time()
    #print("Searching for " + str(sku))
    baseUrl = "https://www.newegg.com/p/pl?d="+model
    headers = {
        'authority':'www.newegg.com',
        'accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'referer':baseUrl,
        'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36'}
    #run proxy
    if proxy != None:
        print("running with proxy: "+ str(proxy))
        proxies = {
        "http":proxy
        }
        try:
            page = requests.get(baseUrl,headers=headers,proxies=proxies)
        except:
            print("Request Refused")
            return False
    #run local
    if proxy == None:
        try:
            page = requests.get(baseUrl,headers=headers)
        except:
            print("Request Refused")
            return False
    if page.status_code == 200:
        soup = BeautifulSoup(page.content, 'html.parser')
        #print(soup)

        #Make sure the item number matches and we are on the same page
        itemNumber = soup.find('li', class_='is-current')
        if itemNumber != None:
            if model in itemNumber.text:
                #check for cart button
                cartButton = soup.find('button', class_='btn btn-primary btn-wide')

                if cartButton != None:
                    print("In Stock!")
                    return True

                print("OOS!")
                return False
            print("Couldnt find product")
            return False
        print("Page loaded, but nothing on it")
        return False
    print("Error loading page")
    return False

# Newegg Cart Module
def neweggCartModule(model,billing,id):
    settings = settingsModule(1,None)

    if "headless" not in settings:
        settings["headless"] = False
        settingsModule(3,False)

    options = webdriver.ChromeOptions()
    if settings["headless"] == True:
        options.add_argument('--headless')
        options.add_argument('--disable-gpu')
        options.add_argument('--window-size=1920,1080')
        options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36")
    options.add_experimental_option('excludeSwitches', ['enable-logging'])

    proxyauth_plugin_path = create_proxyauth_extension(
        proxy_host="154.28.212.244",
        proxy_port=6690,
        proxy_username="VJ3H9",
        proxy_password="L9MEQW4W"
    )
    proxies = proxyModule()
    proxy = random.choice(proxies)

    driver = webdriver.Chrome(resource_path(CHROME_DRIVER_PATH),options=options)

    driver.get("https://newegg.com/")
    driver.implicitly_wait(5)
    driver.get("https://www.newegg.com/p/pl?d="+model)

    #check for cart button
    try:
        cartButton = WebDriverWait(driver,10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "button[class='btn btn-primary btn-wide']"))) 
    except TimeoutException:
        print("Item OOS!")
        return False
    print("Adding to Cart!")
    ActionChains(driver).click(cartButton).perform()

    time.sleep(1)

    driver.get("https://secure.newegg.com/shop/cart")

    try:
        cartButton = WebDriverWait(driver,5).until(EC.presence_of_element_located((By.CSS_SELECTOR, "button[class='btn btn-primary btn-wide']")))
        color = cartButton.value_of_css_property("background-color")
        if  str(color) == "rgb(228, 228, 228)":
            print("Didnt Cart")
            return False
    except TimeoutException:
        try:
            popup = WebDriverWait(driver,5).until(EC.presence_of_element_located((By.CSS_SELECTOR, "button[class='close']")))
            ActionChains(driver).click(popup).perform()
            cartButton = WebDriverWait(driver,10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "button[class='btn btn-primary btn-wide']")))
        except TimeoutException:
            "Error Carting"
            return False
    print("Checking out!")
    ActionChains(driver).click(cartButton).perform()

    # Check for guest checkout
    try:
        guestCheckout = WebDriverWait(driver,5).until(EC.presence_of_element_located((By.CSS_SELECTOR, "button[class='btn btn-gray']")))
    except TimeoutException:
        print("Not able to guest checkout, not supported!")
        return False

    ActionChains(driver).click(guestCheckout).perform()

    try:
        addNewAddy = WebDriverWait(driver,5).until(EC.presence_of_element_located((By.CSS_SELECTOR, "div[class='card card-add-new']")))
    except TimeoutException:
        print("Error with adding new address!")
        return False

    ActionChains(driver).click(addNewAddy).perform()
    print("Autofill")

    try:
        fName = WebDriverWait(driver,5).until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[name='FirstName']")))
    except TimeoutException:
        print("Error with getting input")
        return False

    fName.send_keys(billing['profile']['fName'])

    lName = driver.find_element_by_css_selector("input[name='LastName']")
    lName.send_keys(billing['profile']['lName'])

    addy1 = driver.find_element_by_css_selector("input[name='Address1']")
    addy1.send_keys(billing['profile']['billStreet1'])

    if billing['profile']['billStreet2'] != "":
        addy2 = driver.find_element_by_css_selector("input[name='Address2']")
        addy2.send_keys(billing['profile']['billStreet2'])

    city = driver.find_element_by_css_selector("input[name='City']")
    city.send_keys(billing['profile']['billCity'])

    state = Select(driver.find_element_by_css_selector("select[name='State']"))
    stateOption = driver.find_element_by_css_selector("option[value='{}']".format(billing['profile']['billState']))
    state.select_by_visible_text(stateOption.text)

    zipcode = driver.find_element_by_css_selector("input[name='ZipCode']")
    zipcode.send_keys(billing['profile']['billZip'])

    phone = driver.find_element_by_css_selector("input[name='Phone']")
    phone.send_keys(billing['profile']['phone'])

    email = driver.find_element_by_css_selector("input[name='Email']")
    email.send_keys(billing['profile']['email'])

    saveButton = driver.find_element_by_css_selector("button[class='btn btn-primary']")
    ActionChains(driver).click(saveButton).perform()

    driver.implicitly_wait(5)
    # Checks for Exisiting Customer popup
    try:
        popup = WebDriverWait(driver,5).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "button[class='btn btn-primary']")))
        for temp in range(popup):
            if temp.text == "Continue as Guest":
                ActionChains(driver).click(temp).perform()
    except TimeoutException:
        print("")            

    # checks for suggested address popup
    try:
        popup = WebDriverWait(driver,5).until(EC.presence_of_element_located((By.CSS_SELECTOR, "button[class='btn btn-primary']")))
        if popup.text == "Use Address":
            ActionChains(driver).click(popup).perform()
    except TimeoutException:
        print("")

    #continue checkout
    try:
        continueDelivery = WebDriverWait(driver,5).until(EC.presence_of_element_located((By.CSS_SELECTOR, "button[class='btn btn-primary checkout-step-action-done layout-quarter']")))
    except TimeoutException:
        print("")

    ActionChains(driver).click(continueDelivery).perform()

    try:
        continueDelivery = WebDriverWait(driver,5).until(EC.presence_of_element_located((By.CSS_SELECTOR, "button[class='btn btn-primary checkout-step-action-done layout-quarter']")))
    except TimeoutException:
        print("")

    ActionChains(driver).click(continueDelivery).perform()

    try:
        addNewPayment = WebDriverWait(driver,5).until(EC.presence_of_element_located((By.CSS_SELECTOR, "div[class='card card-add-new']")))
    except TimeoutException:
        print("Error with adding new payment!")
        return False

    ActionChains(driver).click(addNewPayment).perform()

# Home Depot Search Module
def homedepotSearchModule(sku,proxy):
    startTime = time.time()

    baseUrl = "https://www.homedepot.com"

    userAgentList = ['Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
                     'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.53 Safari/537.36',
                     'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36',
                     'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.110 Safari/537.36',
                     ('Mozilla/5.0 (X11; Linux x86_64) '
                     'AppleWebKit/537.36 (KHTML, like Gecko) '
                     'Chrome/63.0.3239.108 '
                     'Safari/537.36'),
                     ]

    options = webdriver.ChromeOptions()
    #options.add_argument('--headless')
    #options.add_argument('--disable-gpu')
    #options.add_argument('--disable-blink-features=AutomationControlled')
    #options.add_experimental_option("excludeSwitches", ["enable-automation"])
    #options.add_experimental_option('useAutomationExtension', False)
    #options.add_argument('--window-size=1920,1080')
    options.add_argument("user-agent="+random.choice(userAgentList))
    options.add_experimental_option('excludeSwitches', ['enable-logging'])

    #run proxy
    if proxy != None:
        print("running with proxy: "+ str(proxy))
        soptions = {
            'proxy':{
                'http':"http://"+proxy,
                'https':"https://"+proxy,
                'no_proxy': 'localhost,127.0.0.1'
                }
        }
        driver = webdriver.Chrome(resource_path(CHROME_DRIVER_PATH),options=options,seleniumwire_options=soptions)
        
    #run local
    if proxy == None:
        driver = webdriver.Chrome(resource_path(CHROME_DRIVER_PATH),options=options)

    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

    driver.get(baseUrl+"/s/"+sku+"?NCNI-5")

    try:
        WebDriverWait(driver, 7).until(EC.presence_of_element_located((By.CSS_SELECTOR, "div[class='price-detailed__wrapper']")))

        try:
            addToCart = driver.find_element_by_css_selector("img[class='add-to-cart__icon']")

            if addToCart != None:
                print("In Stock!")
                homedepotCartModule(None,driver)
                return True
            print("OOS!")
            return False
        except:
            print("OOS!")
            return False
    except:
        print("Error loading webpage")
        return False

# Home Depot Cart Module
def homedepotCartModule(task,driver):
    #Switch to shipping
    print("switching to ship to home")
    try:
        switchShip = WebDriverWait(driver,7).until(EC.presence_of_element_located((By.CSS_SELECTOR, "a[class='card mobile--margin-right card-container card-unselected card-enabled']")))
        ActionChains(driver).click(switchShip).perform()
    except:
        print("Ship to home not available")
        return False

    #Add to cart
    print("Trying to add to cart")
    try:
        addToCart = WebDriverWait(driver,7).until(EC.presence_of_element_located((By.CSS_SELECTOR, "button[class='bttn bttn--primary']")))
        ActionChains(driver).click(addToCart).perform()
        
    except:
        print("No Cart Button")
        return False
    #Find checkout button
    try:
        time.sleep(1)
        driver.switch_to.frame(driver.find_element_by_css_selector("iframe[class='thd-overlay-frame']"))
        checkout = WebDriverWait(driver,20).until(EC.presence_of_element_located((By.CSS_SELECTOR, "button[data-automation-id='checkoutNowButton']")))
        ActionChains(driver).click(checkout).perform()
        driver.switch_to.default_content()
    except:
        print("No checkout Button")
        return False
    print("Added to cart, checking out!")

    try:
        emailInput = WebDriverWait(driver,10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[data-automation-id='signInEmailField']")))
    except:
        print("Unable to find sign in page")
        return False

    emailInput.send_keys("austinchoncek@hotmail.com")
    passInput = driver.find_element_by_css_selector("input[data-automation-id='signInPasswordField']")
    passInput.send_keys("Worldrace88")
    
    print("Signing in")
    time.sleep(1.5)
    signIn = driver.find_element_by_css_selector("button[data-automation-id='signInSignInButton']")
    ActionChains(driver).click(signIn).perform()

    #Check for Verification code
    try:
        verifyInput = WebDriverWait(driver,10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[data-automation-id='TwoFactorAuthPassCodeField']")))
        print("You need to enter the verification code sent to you: ")
        code = input()
        verifyInput.send_keys(code)

        time.sleep(1)

        verifyButton = WebDriverWait(driver,10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "button[data-automation-id='TwoFactorAuthVerifyButton']")))
        ActionChains(driver).click(verifyButton).perform()
    except:
        print("")

    try:
        veriAddy = WebDriverWait(driver,5).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "input[name='selectAddress']")))

        ActionChains(driver).click(veriAddy[1]).perform()

        continueButton = WebDriverWait(driver,5).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "button[class='u__m-left-normal bttn bttn--primary bttn--inline']"))) 
        ActionChains(driver).click(continueButton).perform()
    except:
        print("")

    try:
        newAddy = WebDriverWait(driver,7).until(EC.presence_of_element_located((By.CSS_SELECTOR, "a[data-automation-id='useAnotherAddressLink']")))
        ActionChains(driver).click(newAddy).perform()

        time.sleep(1)

        newAddy1 = WebDriverWait(driver,7).until(EC.presence_of_element_located((By.CSS_SELECTOR, "span[data-automation-id='addANewAddress']")))
        ActionChains(driver).click(newAddy1).perform()
    except:
        print("")


    try:
        firstName = WebDriverWait(driver,5).until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[data-automation-id='firstName']")))
    except:
        print("Unable to reach final checkout page")
        return False

    print("Auto Fill Shipping & Billing")
    firstName.send_keys("Austin")
    lastName = driver.find_element_by_css_selector("input[data-automation-id='lastName']")
    lastName.send_keys("Choncek")
    phone = driver.find_element_by_css_selector("input[data-automation-id='phone']")
    phone.send_keys("7244969006")
    addyLine1 = driver.find_element_by_css_selector("input[data-automation-id='line1']")
    addyLine1.send_keys("130 Farmstead Lane")
    addyLine2 = driver.find_element_by_css_selector("input[data-automation-id='line2']")
    addyLine2.send_keys("Apt 161")
    zipcode = driver.find_element_by_css_selector("input[data-automation-id='zipCodeField']")
    zipcode.send_keys("16803")

    try:
        veriAddy = WebDriverWait(driver,10).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "input[name='selectAddress']")))
        time.sleep(2)
        ActionChains(driver).click(veriAddy[1]).perform()

        continueButton = WebDriverWait(driver,5).until(EC.presence_of_element_located((By.CSS_SELECTOR, "button[class='u__m-left-normal bttn bttn--primary bttn--inline']")))
        ActionChains(driver).click(continueButton).perform()
    except:
        print("")

    print("Auto Fill Payment")

    cc = driver.find_element_by_css_selector("input[data-automation-id='cardNumber']")
    cc.send_keys("4403931793605388")
    ccMM = Select(driver.find_element_by_css_selector("select[name='cardExpiryMonth']"))
    ccMM.select_by_value("07")
    ccYYYY = Select(driver.find_element_by_css_selector("select[name='cardExpiryYear']"))
    ccYYYY.select_by_value("2024")
    cvv = driver.find_element_by_css_selector("input[data-automation-id='cvvField']")
    cvv.send_keys("4403931793605388")

    print("Placing order")

    try:
        placeOrder = WebDriverWait(driver,10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "button[name='placeOrderButton']")))

        ActionChains(driver).click(placeOrder).perform()
    except:
        print("Unable to place order")
        return False

    #check for errors

    try:
        errorBox = WebDriverWait(driver,10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "span[class='alert alert--danger']")))

        print(errorBox.text)

        return False
    except:
        print("Success!")

# Poke Center Search Module
def pokemonSearchModule(sku, proxy):

    startTime = time.time()

    baseUrl = "https://www.pokemoncenter.com/product/"

    userAgentList = ['Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
                     'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.53 Safari/537.36',
                     'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36',
                     'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.110 Safari/537.36',
                     ('Mozilla/5.0 (X11; Linux x86_64) '
                     'AppleWebKit/537.36 (KHTML, like Gecko) '
                     'Chrome/63.0.3239.108 '
                     'Safari/537.36'),
                     ]

    options = webdriver.ChromeOptions()
    #options.add_argument('--headless')
    #options.add_argument('--disable-gpu')
    #options.add_argument('--disable-blink-features=AutomationControlled')
    #options.add_experimental_option("excludeSwitches", ["enable-automation"])
    #options.add_experimental_option('useAutomationExtension', False)
    #options.add_argument('--window-size=1920,1080')
    options.add_argument("user-agent="+random.choice(userAgentList))
    options.add_experimental_option('excludeSwitches', ['enable-logging'])

    #run proxy
    if proxy != None:
        print("running with proxy: "+ str(proxy))
        soptions = {
            'proxy':{
                'http':"http://"+proxy,
                'https':"https://"+proxy,
                'no_proxy': 'localhost,127.0.0.1'
                }
        }
        driver = webdriver.Chrome(resource_path(CHROME_DRIVER_PATH),options=options,seleniumwire_options=soptions)
        
    #run local
    if proxy == None:
        driver = webdriver.Chrome(resource_path(CHROME_DRIVER_PATH),options=options)

    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

    driver.get("https://www.pokemoncenter.com")
    time.sleep(2)
    driver.get(baseUrl+sku)

    try:
        WebDriverWait(driver, 7).until(EC.presence_of_element_located((By.CSS_SELECTOR, "h1[class='_1WH6oLm7bR-AQmemV8WMJR']")))

        try:
            addToCart = driver.find_element_by_css_selector("button[class='_20FB4-Kigsuh33ROnhb1CX _2EgyS2JF4vSMMGt9KgAEkN _2Vyo6t5xf0vISrGJtN0OKA']")

            if addToCart != None:
                print("In Stock!")
                pokemonCartModule(None, driver)
                return True
            print("OOS!")
            return False
        except:
            print("OOS!")
            return False
    except:
        print("Error loading webpage")
        return False

# Pokemon Center Cart Module
def pokemonCartModule(task, driver):
    # Change to correct quantity
    print("Changing quantity")
    try:
        qtInput = WebDriverWait(driver,5).until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[class='_1qlS_PAMoIq7Swm6JTdGW2']")))
        qtInput.send_keys(2)
    except:
        print("quantity not available")
        return

    #add to cart
    print("Adding to Cart!")

    addToCart = driver.find_element_by_css_selector("button[class='_20FB4-Kigsuh33ROnhb1CX _2EgyS2JF4vSMMGt9KgAEkN _2Vyo6t5xf0vISrGJtN0OKA']")
    ActionChains(driver).click(addToCart).perform()

    try:
        cartLink = WebDriverWait(driver,15).until(EC.presence_of_element_located((By.CSS_SELECTOR, "a[data-count='2']")))
        print("Added To Cart!")
    except:
        print("Unable to add to cart or timed out!")
        return False

    driver.get("https://www.pokemoncenter.com/cart")

# Handles callback from discord
def callbackFlow(code,func):
    global root
    splash = root.splash
    func()
    data = {
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': REDIRECT_URI,
        'scope': 'identify email connections'
        }
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
        }
    r = requests.post('%s/oauth2/token' % API_ENDPOINT, data=data, headers=headers)
    if r.status_code == 200:
        headers = {
        'Authorization': 'Bearer '+r.json()['access_token']
        }
        r2 = requests.get('%s/users/@me' % API_ENDPOINT,headers=headers)
        if r2.status_code == 200:
            userID = r2.json()['id']
            
            r3 = requests.get("https://fortunebot-io.herokuapp.com/v1/getkey?id="+userID)
            if r3.status_code == 200:
                jsonResult = r3.json()
                #print(str(jsonResult))

                if "Success" in jsonResult:
                    print("Found binded key!")
                    encodedKey = jwt.encode({"key":jsonResult['Success']}, jwtSecret, algorithm="HS256")
                    temp = encodedKey
                    #
                    #print(temp)
                    settings = settingsModule(4,temp)
                    return
                print("No Keys binded!")
    return

# temp server to capture callback
def serverRun():
    HOST = os.environ.get('SERVER_HOST', 'localhost')
    try:
       PORT = 8080
    except ValueError:
       PORT = 8080
    tempServer.run(HOST, PORT)

# callback route
@tempServer.route('/')
def callback():
    code = request.args.get('code')
    func = request.environ.get('werkzeug.server.shutdown')
    if code == None:
        return
    callbackFlow(code, func)
    return ""

# INIT
def appInit():

    if not os.path.exists(folder):
        os.makedirs(folder)
    if not os.path.exists(folder2):
        os.makedirs(folder2)
    if not os.path.exists(filename):
        open(filename, 'w').close()
    if not os.path.exists(filename1):
       open(filename1, 'w').close()
    if not os.path.exists(filename2):
       open(filename2, 'w').close()
    if not os.path.exists(filename3):
       open(filename3, 'w').close()
    if not os.path.exists(filename4):
       open(filename4, 'w').close()
    if not os.path.exists(filename5):
       open(filename5, 'w').close()

    settings = settingsModule(1,None)

    if settings == False:
        settings = {}

    if "forceCheckout" not in settings:
        settings["forceCHeckout"] = False
        settingsModule(2,False)
    if "headless" not in settings:
        settings["headless"] = False
        settingsModule(3,False)
    if "queueTasks" not in settings:
        settings["headless"] = 1
        settingsModule(5,1)
    if "key" not in settings:
        settings["key"] = ""
        settingsModule(4,"")
    if "qtProfile" not in settings:
        settings["qtProfile"] = ""
        settingsModule(6,"")

    return True

# Main App Method
def app():
    global root
    splash = root.splash

    #Key auth flow
    keyAuth = False

    splash.setStatus("Validating Key...")
    while keyAuth == False:
        settings = settingsModule(1,None)
        key = settings['key']
        if key != "":
            key = jwt.decode(key, jwtSecret, algorithms=["HS256"])
        
            url = "https://fortunebot-io.herokuapp.com/v1/verify?key="+str(key["key"])

            try:
                result = requests.get(url)
            except:
                print("Request Refused")
                return False

            if result.status_code == 200:
                jsonResult = result.json()
                #print(str(jsonResult))

                if "Success" in jsonResult:
                    splash.setStatus("Key Validated, Happy Cooking!")
                    keyAuth = True
                    break
            splash.setStatus("Invalid Key!")
        splash.setStatus("Redirecting you to login via discord!")
        url = "https://discord.com/api/oauth2/authorize?client_id=829097899501420605&redirect_uri=http%3A%2F%2Flocalhost%3A8080%2F&response_type=code&scope=identify"
        
        #p1 = subprocess.Popen("start chrome /new-tab {}".format(url.replace("&","^&")),shell=True)
        if sys.platform == 'win32':
            os.startfile(url)
        else:
            os.system(url)
        serverRun()
    
    time.sleep(2)
    root.afterSplash()
    return

def appThread():
    global appT
    appT = Thread(target=app)
    appT.start()

def stopAppThread():
    global appT
    #appT.join()

#############
#
# UI
#
#############

# Center window
def center(toplevel):
    toplevel.update_idletasks()

    # Tkinter way to find the screen resolution
    # screen_width = toplevel.winfo_screenwidth()
    # screen_height = toplevel.winfo_screenheight()

    # PyQt way to find the screen resolution
    app = QtWidgets.QApplication([])
    screen_width = app.desktop().screenGeometry().width()
    screen_height = app.desktop().screenGeometry().height()

    size = tuple(int(_) for _ in toplevel.geometry().split('+')[0].split('x'))
    x = screen_width/2 - size[0]/2
    y = screen_height/2 - size[1]/2

    toplevel.geometry("+%d+%d" % (x, y))

# Splash Pane
class SplashPane:
    global root
    def __init__(self):
        self.frame = Frame(width=1280,height=720,bg="#F06543")

        self.var = StringVar()
        self.var.set('...')

        self.img = Image.open(assetFolder+"logo-mock1.png")
        self.img_logo = ImageTk.PhotoImage(self.img.resize((200,200), Image.ANTIALIAS))
        self.lbl_logo = Label(self.frame,image=self.img_logo)
        self.lbl_logo.image = self.img_logo
       
        self.lbl_header = Label(self.frame,text="FortuneBot",bg="#F06543",font=font.Font(size=45),pady=50)

        self.lbl_status = Label(self.frame,textvariable=self.var,bg="#F06543",font=font.Font(size=30),pady=50)

        self.lbl_header.place(relx = 0.5, rely = 0.0, anchor='n')
        self.lbl_logo.place(relx = 0.5, rely = 0.5, anchor = 'center')
        self.lbl_status.place(relx = 0.5, rely = 1.0, anchor='s')

    def setStatus(self,status):
        self.var.set(status)
        root.roots.update()

# enu Pane
class MenuPane:
    global root
    def __init__(self):
        self.frame = Frame(width=200,height=720,bg="#141425")

        self.lbl_logo = Label(self.frame,text="FortuneBot",fg="#F06543",bg="#141425",font=font.Font(size=30))
        self.lbl_version = Label(self.frame,text=botVersion,fg="#F06543",bg="#141425")

        self.btn_search = Button(self.frame,text="Search (Developer)",width=50,height=3)
        self.btn_tasks = Button(self.frame,text="Tasks",width=50,height=3,command=root.showTasks)
        self.btn_profiles = Button(self.frame,text="Profiles",width=50,height=3,command=root.showProfiles)
        self.btn_settings = Button(self.frame,text="Settings",width=50,height=3,command=root.showSettings)

        self.lbl_logo.grid(row=0,column=0)

        self.btn_search.grid(row=2,column=0)
        self.btn_tasks.grid(row=3,column=0)
        self.btn_profiles.grid(row=4,column=0)
        self.btn_settings.grid(row=5,column=0)

        self.lbl_version.grid(row=7,column=0)

# Tasks Pane
class TaskPane:
    
    statusFlag = True

    def taskStatusThread(self):

        while self.statusFlag:
            for i in range(len(root.threads)):
                if root.threads[i] != False:
                    status = getTaskStatus(self.tasks['taskList'][i])
                    if status != False:
                        self.lblStatus[i].set(status['statusList'][0])
                else:
                    self.lblStatus[i].set("Not Running...")

            time.sleep(0.5)
    
    def __init__(self):
        self.frame = Frame(width=1070,height=720)
        self.statusThread = Thread(target=self.taskStatusThread)
        self.stores = ['Best Buy']
        
    def saveTask(self,position):
        task = {}

        if position == -2:
            if self.qtSku.get() == "":
                return
            sku = self.qtSku.get()
            settings = settingsModule(1,None)

            task = {
                    'name': 'QuickTask'+sku,
                    'store': 'Best Buy',
                    'sku':sku,
                    'quantity':1,
                    'storePickup':False,
                    'profile':settings['qtProfile'],
                    'date':False,
                    'time':False
                    }

            wait = taskSaveModule(2,task,-1)
            self.threads.append(False)
            self.lblStatus.append(StringVar(self.frame,value='Not Running...'))
            root.showTasks()
            return

        if self.store.get() == '':
            return
        task['store'] = self.store.get()

        if self.name.get() == '':
            return
        task['name'] = self.name.get()

        if self.sku.get() == '':
            return
        task['sku'] = self.sku.get()

        if self.qt.get() == '':
            return
        task['quantity'] = self.qt.get()

        if self.storePickup.get() == '':
            return
        task['storePickup'] = self.storePickup.get()

        if self.profile.get() == '':
            return
        task['profile'] = self.profile.get()

        if self.futureTask.get() == True:
            if self.date.get() == '':
                return
            task['date'] = self.date.get()

            if self.time.get() == '':
                return
            task['time'] = self.time.get()
        else:
            task['date'] = False
            task['time'] = False

        wait = taskSaveModule(2,task,position)

        self.threads.append(False)
        self.lblStatus.append(StringVar(self.frame,value='Not Running...'))

        self.popup.destroy()
        root.showTasks()

    def taskAction(self,mode,position):
        # Delete Task
        if mode == 2:
            taskSaveModule(3,None,position)
            self.threads.pop(position)
            self.lblStatus.pop(position)
            root.showTasks()
            return

        # Clone Task
        if mode == 3:
            task = self.tasks['taskList'][position]
            task['name']+='Clone'
            wait = taskSaveModule(2,task,-1)
            self.threads.append(False)
            self.lblStatus.append(StringVar(self.frame,value='Not Running...'))
            root.showTasks()
            return

        self.popup = Tk()
        self.popup.resizable(False, False)
        self.popup.geometry('300x300')
        center(self.popup)

        self.store = StringVar(self.popup,value="Best Buy")
        self.name = StringVar(self.popup)
        self.sku = StringVar(self.popup)
        self.qt = IntVar(self.popup,value=1)
        self.storePickup = BooleanVar(self.popup,value=False)
        self.profile = StringVar(self.popup)
        self.futureTask = BooleanVar(self.popup,value=False)
        self.date = StringVar(self.popup)
        self.time = StringVar(self.popup)

        self.profiles = profileModule(1,{},None)
        self.profileMenu = []
        
        if self.profiles == False:
            self.profileMenu.append("You dont have any profiles!")
            self.profile.set(self.profileMenu[0])
        else:
            self.profileMenu.append("Select a profile")
            self.profile.set(self.profileMenu[0])
            for profile in self.profiles['profileList']:
                self.profileMenu.append(profile['profileName'])

        if mode == 0:
            self.popup.title("New Task")
        if mode == 1:
            self.popup.title("Edit Task")
            task = self.tasks['taskList'][position]

            if "store" not in task:
                task['store'] = "Best Buy"

            if "storePickup" not in task:
                task['storePickup'] = False

            self.store = StringVar(self.popup,value=str(task['store']))
            self.name = StringVar(self.popup, value=str(task['name']))
            self.sku = StringVar(self.popup, value=str(task['sku']))
            self.qt = IntVar(self.popup, value=int(task['quantity']))
            self.storePickup = BooleanVar(self.popup, value=bool(task['storePickup']))
            self.profile = StringVar(self.popup, value=str(task['profile']['profileName']))
            if task['date'] == False:
                self.futureTask = BooleanVar(self.popup, value=False)
            else:
                self.futureTask = BooleanVar(self.popup, value=True)
                self.date = StringVar(self.popup, value=str(task['date']))
                self.time = StringVar(self.popup, value=str(task['time']))

        Label(self.popup,text="Task Name").grid(row=0,column=0)
        Entry(self.popup,textvariable=self.name).grid(row=0,column=1)

        Label(self.popup,text="Store").grid(row=1,column=0)
        OptionMenu(self.popup,self.store,*self.stores).grid(row=1,column=1)

        Label(self.popup,text="Sku").grid(row=2,column=0)
        Entry(self.popup,textvariable=self.sku).grid(row=2,column=1)

        Label(self.popup,text="Quantity").grid(row=3,column=0)
        Spinbox(self.popup,textvariable=self.qt,from_=1,to=99).grid(row=3,column=1)

        Checkbutton(self.popup,text="Store Pickup?",variable=self.storePickup,onvalue=True,offvalue=False).grid(row=4,column=0)

        Label(self.popup,text="Profile").grid(row=5,column=0)
        OptionMenu(self.popup,self.profile,*self.profileMenu).grid(row=5,column=1)

        Checkbutton(self.popup,text='Future Task?',variable=self.futureTask,onvalue=True,offvalue=False).grid(row=6,column=0)

        Label(self.popup,text="Date MM/DD/YYYY").grid(row=7,column=0)
        Entry(self.popup,textvariable=self.date).grid(row=7,column=1)
        Label(self.popup,text="Time HH:MM AM/PM").grid(row=8,column=0)
        Entry(self.popup,textvariable=self.time).grid(row=8,column=1)

        Button(self.popup,text='Save Task',command= lambda: self.saveTask(position)).grid(row=10,column=1)

    def runTask(self,taskPos):

        self.statusFlag = True
        self.taskButtons[taskPos].grid_forget()
        self.taskButtons[taskPos] = Button(self.frame,text="Stop",command= lambda: self.stopTask(taskPos))
        self.taskButtons[taskPos].grid(row=taskPos+2,column=0)

        self.lblStatus[taskPos].set('Running...')

        root.threads[taskPos] = Process(target=taskMod, args=(self.tasks['taskList'][taskPos],))
        root.threads[taskPos].start()

        if self.statusThread.is_alive() == False:
            self.statusThread = Thread(target=self.taskStatusThread)
            self.statusThread.start()

    def stopTask(self,taskPos):

        if sys.platform == 'win32':
            setTempfilename(".\\User Data\\Temp\\"+self.tasks['taskList'][taskPos]['name']+"Status.json")
        else:
            setTempfilename("./User Data/Temp/"+self.tasks['taskList'][taskPos]['name']+"Status.json")
            
        self.taskButtons[taskPos].grid_forget()
        self.taskButtons[taskPos] = Button(self.frame,text="Run",command= lambda: self.runTask(taskPos))
        self.taskButtons[taskPos].grid(row=taskPos+2,column=0)

        taskStatus("Not Running...",0)
        root.threads[taskPos].terminate()
        root.threads[taskPos] = False

        if not any(root.threads):
            print("Thread killed")
            self.statusFlag = False
            self.statusThread.join()
            self.lblStatus[taskPos].set("Not Running...")

    def getPane(self):
        self.tasks = taskSaveModule(1,{},None)
        self.qtSku = StringVar(self.frame)
        self.taskButtons = []

        self.threads = root.threads
        self.lblStatus = root.lblStatus

        for i in range(len(self.tasks['taskList'])):
            if len(self.threads) < i + 1:
                self.threads.append(False)
            if len(self.lblStatus) < i + 1:
                self.lblStatus.append(StringVar(self.frame,value='Not Running...'))

        self.btn_new = Button(self.frame,text="New Task",command= lambda: self.taskAction(0,-1))
        self.btn_new.grid(row=0,column=0)

        Label(self.frame,text=("Quick Task Sku:")).grid(row=0,column=1)
        Entry(self.frame,textvariable=self.qtSku).grid(row=0,column=2)
        self.btn_qt = Button(self.frame,text=("Run Quick Task"),command= lambda: self.saveTask(-2))

        self.settings = settingsModule(1, None)

        if self.settings['qtProfile'] == "":
            self.btn_qt['state'] = "disabled"
            self.btn_qt['text'] = "Need to set quick task profile in settings!"

        self.btn_qt.grid(row=0,column=3)
        Label(self.frame,text="Task Name").grid(row=1,column=1)
        Label(self.frame,text="Task Status").grid(row=1,column=5,padx=150)

        for i in range(len(self.tasks['taskList'])):
            if self.threads[i] == False:
                self.taskButtons.append(Button(self.frame,text="Run",command= lambda i=i: self.runTask(i)))
                self.taskButtons[i].grid(row=i+2,column=0)
            else:
                self.taskButtons.append(Button(self.frame,text="Stop",command= lambda i=i: self.stopTask(i)))
                self.taskButtons[i].grid(row=i+2,column=0)
            Label(self.frame,text=self.tasks['taskList'][i]['name']).grid(row=i+2,column=1)
            Button(self.frame,text="Edit",command= lambda i=i: self.taskAction(1,i)).grid(row=i+2,column=2)
            Button(self.frame,text="Clone",command= lambda i=i: self.taskAction(3,i)).grid(row=i+2,column=3)
            Button(self.frame,text="Delete",command= lambda i=i: self.taskAction(2,i)).grid(row=i+2,column=4)
            Label(self.frame,textvariable=self.lblStatus[i]).grid(row=i+2,column=5)
        return self.frame

# Profiles Pane
class ProfilePane:
    global root
    def __init__(self):
        self.frame = Frame(width=1070,height=720)

    def saveProfile(self,position):
        profile = {}

        if self.pName.get() == "":
            print("Field Cant be empty")
            return
        profile['profileName'] = self.pName.get()

        if self.fName.get() == "":
            print("Field Cant be empty")
            return
        profile['fName'] = self.fName.get()

        if self.lName.get() == "":
            print("Field Cant be empty")
            return
        profile['lName'] = self.lName.get()

        if self.email.get() == "":
            print("Field Cant be empty")
            return
        profile['email'] = self.email.get()

        if self.phone.get() == "":
            print("Field Cant be empty")
            return
        profile['phone'] = self.phone.get()

        if self.bill1.get() == "":
            print("Field Cant be empty")
            return
        profile['billStreet1'] = self.bill1.get()

        profile['billStreet2'] = self.bill2.get()

        if self.city.get() == "":
            print("Field Cant be empty")
            return
        profile['billCity'] = self.city.get()

        if self.state.get() == "":
            print("Field Cant be empty")
            return
        profile['billState'] = self.state.get()

        if self.zip.get() == "":
            print("Field Cant be empty")
            return
        profile['billZip'] = self.zip.get()

        if self.cc.get() == "":
            print("Field Cant be empty")
            return
        profile['cc'] = self.cc.get()

        if self.ccExpMM.get() == "":
            print("Field Cant be empty")
            return
        profile['ccExpMM'] = self.ccExpMM.get()

        if self.ccExpYYYY.get() == "":
            print("Field Cant be empty")
            return
        profile['ccExpYYYY'] = self.ccExpYYYY.get()

        if self.cvv.get() == "":
            print("Field Cant be empty")
            return
        profile['cvv'] = self.cvv.get()

        wait = profileModule(2,profile,position)

        self.popup.destroy()

        root.showProfiles()

    def profileAction(self,mode,position):

        # Delete Profile
        if mode == 2:
            print(position)
            profileModule(3,self.profiles['profileList'][position]['profileName'],None)
            root.showProfiles()
            return

        # Clone Profile
        if mode == 3:
            profile = self.profiles['profileList'][position]
            profile['profileName']+='Clone'
            wait = profileModule(2,profile,-1)
            root.showProfiles()
            return

        self.popup = Tk()
        self.popup.resizable(False, False)
        self.popup.geometry('650x300')
        center(self.popup)

        self.pName = StringVar(self.popup)
        self.fName = StringVar(self.popup)
        self.lName = StringVar(self.popup)
        self.email = StringVar(self.popup)
        self.phone = StringVar(self.popup)
        self.bill1 = StringVar(self.popup)
        self.bill2 = StringVar(self.popup)
        self.city = StringVar(self.popup)
        self.state = StringVar(self.popup)
        self.zip = StringVar(self.popup)
        self.cc = StringVar(self.popup)
        self.ccExpMM = StringVar(self.popup)
        self.ccExpYYYY = StringVar(self.popup)
        self.cvv = StringVar(self.popup)

        # New Profile
        if mode == 0:
            self.popup.title("New Profile")
            
        # Edit Profile
        if mode == 1:
            self.popup.title("Edit Profile")
            profile = self.profiles['profileList'][position]

            self.pName = StringVar(self.popup,value=str(profile['profileName']))
            self.fName = StringVar(self.popup,value=str(profile['fName']))
            self.lName = StringVar(self.popup,value=str(profile['lName']))
            self.email = StringVar(self.popup,value=str(profile['email']))
            self.phone = StringVar(self.popup,value=str(profile['phone']))
            self.bill1 = StringVar(self.popup,value=str(profile['billStreet1']))
            self.bill2 = StringVar(self.popup,value=str(profile['billStreet2']))
            self.city = StringVar(self.popup,value=str(profile['billCity']))
            self.state = StringVar(self.popup,value=str(profile['billState']))
            self.zip = StringVar(self.popup,value=str(profile['billZip']))
            self.cc = StringVar(self.popup,value=str(profile['cc']))
            self.ccExpMM = StringVar(self.popup,value=str(profile['ccExpMM']))
            self.ccExpYYYY = StringVar(self.popup,value=str(profile['ccExpYYYY']))
            self.cvv = StringVar(self.popup,value=str(profile['cvv']))

        Label(self.popup,text="Profile Name").grid(row=0,column=0,sticky='e')
        self.lbl_profile = Entry(self.popup,textvariable=self.pName).grid(row=0,column=1)

        Label(self.popup,text="First Name").grid(row=1,column=0,sticky='e')
        Entry(self.popup,textvariable=self.fName).grid(row=1,column=1)
        Label(self.popup,text="Last Name").grid(row=1,column=2,sticky='e')
        Entry(self.popup,textvariable=self.lName).grid(row=1,column=3)

        Label(self.popup,text="Email").grid(row=2,column=0,sticky='e')
        Entry(self.popup,textvariable=self.email).grid(row=2,column=1)
        Label(self.popup,text="Phone").grid(row=2,column=2,sticky='e')
        Entry(self.popup,textvariable=self.phone).grid(row=2,column=3)

        Label(self.popup,text="Billing/Shipping").grid(row=3,column=0,sticky='e')

        Label(self.popup,text="Address Line 1").grid(row=4,column=0,sticky='e')
        Entry(self.popup,textvariable=self.bill1).grid(row=4,column=1)

        Label(self.popup,text="Apt/Suite (Opt)").grid(row=5,column=0,sticky='e')
        Entry(self.popup,textvariable=self.bill2).grid(row=5,column=1)

        Label(self.popup,text="City").grid(row=6,column=0,sticky='e')
        Entry(self.popup,textvariable=self.city).grid(row=6,column=1)
        Label(self.popup,text="State i.e. PA").grid(row=6,column=2,sticky='e')
        Entry(self.popup,textvariable=self.state).grid(row=6,column=3)
        Label(self.popup,text="Zipcode").grid(row=6,column=4,sticky='e')
        Entry(self.popup,textvariable=self.zip).grid(row=6,column=5)

        Label(self.popup,text="Card Info").grid(row=7,column=0,sticky='e')

        Label(self.popup,text="Card Number").grid(row=8,column=0,sticky='e')
        Entry(self.popup,textvariable=self.cc).grid(row=8,column=1)

        Label(self.popup,text="Card Exp MM").grid(row=9,column=0,sticky='e')
        Entry(self.popup,textvariable=self.ccExpMM).grid(row=9,column=1)
        Label(self.popup,text="Card Exp YYYY").grid(row=9,column=2,sticky='e')
        Entry(self.popup,textvariable=self.ccExpYYYY).grid(row=9,column=3)
        Label(self.popup,text=" CVV").grid(row=9,column=4,sticky='e')
        Entry(self.popup,textvariable=self.cvv).grid(row=9,column=5)

        Button(self.popup,text='Save Profile',command= lambda: self.saveProfile(position)).grid(row=10,column=5)

    def getPane(self):
        self.btn_new = Button(self.frame,text="New Profile",command= lambda: self.profileAction(0,-1))
        self.profiles = profileModule(1,{},None)

        self.btn_new.grid(row=0,column=0)

        Label(self.frame,text="Profile Name").grid(row=1,column=0)

        for i in range(len(self.profiles['profileList'])):
            Label(self.frame,text=self.profiles['profileList'][i]['profileName']).grid(row=i+2,column=0)
            Button(self.frame,text="Edit",command= lambda i=i: self.profileAction(1,i)).grid(row=i+2,column=1)
            Button(self.frame,text="Clone",command= lambda i=i: self.profileAction(3,i)).grid(row=i+2,column=2)
            Button(self.frame,text="Delete",command= lambda i=i: self.profileAction(2,i)).grid(row=i+2,column=3)
        return self.frame

# Settings Pane
class SettingsPane:
    def __init__(self):
        self.frame = Frame(width=1070,height=720)

    def toggleForceCheckout(self):
        settingsModule(2,not self.settings['forceCheckout'])
    def toggleDevMode(self):
        settingsModule(3,not self.settings['headless'])
    def toggleQueue(self,*args):
        try:
            if self.queue.get() != 0:
                settingsModule(5,self.queue.get())
        except:
            pass
    def toggleQuickTask(self,*args):
        if self.quickProfile.get() != "Select a profile":
            for profile in self.profiles['profileList']:
                if profile['profileName'] == self.quickProfile.get():
                    settingsModule(6,profile)
    def saveWebhook(self):
        if self.webhook.get() == "":
            return
        webhookModule({},self.webhook.get(),3)
        root.showSettings()
        return
    def deleteWebhook(self,position):
        webhookModule({},position,4)
        root.showSettings()
        return

    def getPane(self):
        self.settings = settingsModule(1, None)
        self.force = BooleanVar(value=bool(self.settings['forceCheckout']))
        self.dev = BooleanVar(value=bool(self.settings['headless']))
        self.queue = IntVar(value=int(self.settings['queueTasks']))
        self.queue.trace("w",self.toggleQueue)
        self.profiles = profileModule(1,{},None)
        self.quickProfile = StringVar()
        self.profileMenu = []
        self.webhook = StringVar(self.frame)
        self.webhooks = webhookModule({},"",2)

        if self.profiles == False:
            self.profileMenu.append("You dont have any profiles!")
            self.quickProfile.set(self.profileMenu[0])
        else:
            if self.settings['qtProfile'] == "":
                self.profileMenu.append("Select a profile")
                self.quickProfile.set(self.profileMenu[0])
            else:
                self.quickProfile.set(self.settings['qtProfile']['profileName'])
            for profile in self.profiles['profileList']:
                self.profileMenu.append(profile['profileName'])
            self.quickProfile.trace('w',self.toggleQuickTask)

        self.forceCheckout = Checkbutton(self.frame, text='Force Checkout',variable=self.force, onvalue=True, offvalue=False, command=self.toggleForceCheckout)
        self.devMode = Checkbutton(self.frame, text='Developer Mode',variable=self.dev, onvalue=True, offvalue=False, command=self.toggleDevMode)
        self.lbl_queue = Label(self.frame,text="Queue Tasks")
        self.queueTasks = Entry(self.frame, textvariable=self.queue)
        self.lbl_quickTask = Label(self.frame,text="Quick Task Profile")
        self.profileOption = OptionMenu(self.frame,self.quickProfile,*self.profileMenu)

        self.ent_webhook = Entry(self.frame, textvariable=self.webhook)
        self.btn_webhook = Button(self.frame, text="Add Webhook",command=self.saveWebhook)

        self.forceCheckout.grid(row=0,column=0)
        self.devMode.grid(row=1,column=0)
        self.lbl_queue.grid(row=2,column=0,sticky='w')
        self.queueTasks.grid(row=2,column=1)
        self.lbl_quickTask.grid(row=3,column=0,sticky='w')
        self.profileOption.grid(row=3,column=1)
        Label(self.frame,text="Webhooks").grid(row=4,column=0)
        self.ent_webhook.grid(row=5,column=0)
        self.btn_webhook.grid(row=5,column=1)

        for i in range(len(self.webhooks["urls"])):
            Label(self.frame,text=self.webhooks['urls'][i],wraplength=120,justify=LEFT).grid(row=6+i,column=0)
            Button(self.frame,text="Delete",command=lambda i=i: self.deleteWebhook(i)).grid(row=6+i,column=1)

        return self.frame

# Root Window
class RootWindow:

    def __init__(self):
        self.roots = Tk()

        self.splash = SplashPane()
        self.splashPane = self.splash.frame

        self.lblStatus = []
        self.threads = []

        self.roots.resizable(False, False)
        self.roots.title("FortuneBot")
        self.roots.geometry('1280x720')

        center(self.roots)

        self.roots.after(1000, appThread)

        self.splashPane.pack(fill=BOTH,side=TOP)
        
    def start(self):
        self.roots.mainloop()

    def afterSplash(self):
        stopAppThread()
        if self.splashPane != None:
            self.splashPane.pack_forget()
        self.menu = MenuPane().frame
        self.menu.pack(fill=BOTH,side=LEFT)
        self.content = Frame(width=1070,height=720)
        self.content.pack(fill=BOTH,side=RIGHT)

    def showTasks(self):
        if self.content != None:
            self.content.pack_forget()
        self.content = TaskPane().getPane()
        self.content.pack(fill=BOTH)

    def showProfiles(self):
        if self.content != None:
            self.content.pack_forget()
        self.content = ProfilePane().getPane()
        self.content.pack(fill=BOTH)

    def showSettings(self):
        if self.content != None:
            self.content.pack_forget()
        self.content = SettingsPane().getPane()
        self.content.pack(fill=BOTH)

# Main Function
if __name__ == "__main__":
    global root

    multiprocessing.freeze_support()

    wait = appInit()

    root = RootWindow()
    
    root.start()
    
    
    