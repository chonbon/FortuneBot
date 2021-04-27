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
def profileModule(mode,profile):
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
                data["profileList"].append(profile)
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
                data["urls"].pop(int(webhook)-1)
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
                  print(task['name']+"               running...",end='\r')
                  result = bbSearchModule(task,None)
                  if result == True:
                    print(task['name']+"               Item In Stock, attempting to checkout",end='\r')
                    cart = bbCartModule(task['sku'],task,0)
                    if cart == True:
                      print(task['name']+"               Success!",end='\r')
                      running = False
                      break
                    if cart == False:
                      print(task['name']+"               Error Carting",end='\r')
                    if cart == None:
                      break

                  if settings['forceCheckout'] == True:
                     print(task['name']+"               Forcing Cart and Checkout",end='\r')
                     cart = bbCartModule(task['sku'],task,0)
                     if cart == True:
                        print(task['name']+"               Success!",end='\r')
                        running = False
                        break
                     if cart == False:
                        print(task['name']+"               Force Carting did not work, trying again.",end='\r')
                     if cart == None:
                        break
                  continue
                print(task['name']+"               Not Running...",end='\r')
                continue
              print(task['name']+"               Running Restock!",end='\r')
              result = bbSearchModule(task,None)
              if result == True:
                    print(task['name']+"               Item In Stock, attempting to checkout",end='\r')
                    cart = bbCartModule(task['sku'],task,0)
                    if cart == True:
                      print(task['name']+"               Success!",end='\r')
                      running = False
                      break
                    if cart == False:
                        print(task['name']+"               Error Carting",end='\r')
                    if cart == None:
                        break
              if settings['forceCheckout'] == True:
                     print(task['name']+"               Forcing Cart and Checkout",end='\r')
                     cart = bbCartModule(task['sku'],task,0)
                     if cart == True:
                        print(task['name']+"               Success!",end='\r')
                        running = False
                        break
                     if cart == False:
                        print(task['name']+"               Force Carting did not work, trying again.",end='\r')
                     if cart == None:
                        break
              time.sleep(1)
              continue
              #task was in the past, dont check for time and run    
            print(task['name']+"               Not Running today...",end='\r')
        print(task['name']+"               running...",end='\r')
        result = bbSearchModule(task,None)
        if result == True:
            print(task['name']+"               Item In Stock, attempting to checkout",end='\r')
            cart = bbCartModule(task['sku'],task,0)
            if cart == True:
                print(task['name']+"               Success!",end='\r')
                running = False
                break
            if cart == False:
                print(task['name']+"               Error Carting",end='\r')
            if cart == None:
                break
            if settings['forceCheckout'] == True:
                print(task['name']+"               Forcing Cart and Checkout",end='\r')
                cart = bbCartModule(task['sku'],task,0)
                if cart == True:
                    print(task['name']+"               Success!",end='\r')
                    running = False
                    break
                if cart == False:
                    print(task['name']+"               Force Carting did not work, trying again.",end='\r')
                if cart == None:
                    break
        time.sleep(1)

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

# Saves Tasks to the file
def taskSaveModule(mode, task):
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
                data["taskList"].append(task)
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
            for i in range(len(data["taskList"])):
                if data["taskList"][i]["name"] == task:
                    data["taskList"].pop(i)
                    break
        with open(filename, 'w') as json_file:
            json.dump(data, json_file)
            print("Deleted Task!")
            return True

#Best Buy Search Module
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
        tempFilename = ".\\User Data\\Temp\\"+task["name"]+"Status.json"
    else:
        tempFilename = "./User Data/Temp/"+task["name"]+"Status.json"

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
        chrome_options.add_argument("--log-level=3")
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
        st = taskStatus(billing['name']+"              Queue Task "+str(id)+" starting...",id)

    driver.get("https://bestbuy.com/")

    driver.execute_cdp_cmd('Network.setUserAgentOverride', {"userAgent": random.choice(userAgentList)})

    if id == 0:
        # Add To cart link
        st = taskStatus(billing['name']+"              Adding to Cart!",id)
        driver.get("https://api.bestbuy.com/click/-/"+str(sku)+"/cart")

    while running:
        # Check for checkout button
        try:
            checkoutButton = WebDriverWait(driver, 7).until(EC.presence_of_element_located((By.CSS_SELECTOR, "button[class='btn btn-lg btn-block btn-primary']")))
        except TimeoutException:
            # Might be Queue
            if id == 0:
                st = taskStatus(billing['name']+"             Unable To Cart link, trying for queue",id)
                
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
                    st = taskStatus(billing['name']+"             Error Occured",id)
                    return False

            try:
                addToCartButton = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "button[class='btn btn-primary btn-lg btn-block btn-leading-ficon add-to-cart-button']")))
            except TimeoutException:
                st = taskStatus(billing['name']+"             Check Stores, OOS or In store only.",id)
                return False
            st = taskStatus(billing['name']+"             Trying to enter queue",id)
            ActionChains(driver).click(addToCartButton).perform()

            # check for queue error
            try:
                qAlert = WebDriverWait(driver, 7).until(EC.presence_of_element_located((By.CSS_SELECTOR, "div[class='c-alert-content']")))
            except TimeoutException:
                st = taskStatus(billing['name']+"             Entering Queue took too long, wait to try again or use fresh proxies.",id)
                return False

            if id == 0:
                if settings["queueTasks"] > 1 and launchedQueueTasks != True:
                    st = taskStatus(billing['name']+"             Handing off task to queue tasks",id)
                    for i in range(int(settings['queueTasks'])-1):
                        p = multiprocessing.Process(target=bbCartModule, args=[sku,billing,i+1])
                        p.start()
                        time.sleep(.75)
                    launchedQueueTasks = True
            inQueue = True
            st = taskStatus(billing['name']+"             In Queue....",id)

            while inQueue:
                color = addToCartButton.value_of_css_property("background-color")
                #print(str(color))
                if str(color) != "rgba(197, 203, 213, 1)":
                    st = taskStatus(billing['name']+"             Your Turn in the queue!",id)
                    inQueue = False
                    
            time.sleep(1)
            carting = True

            while carting:
                st = taskStatus(billing['name']+"            Trying to cart!",id)
                ActionChains(driver).click(addToCartButton).perform()

                try:
                    cartButton = WebDriverWait(driver,5).until(EC.presence_of_element_located((By.CSS_SELECTOR, "div[class='dot']")))
                    if cartButton.text != "0":
                        carting = False
                except TimeoutException:
                    st = taskStatus(billing['name']+"             Did not cart, trying again",id)
                time.sleep(random.choice([1,1.5,2]))

            driver.get("https://www.bestbuy.com/cart")
            try:
                checkoutButton = WebDriverWait(driver, 7).until(EC.presence_of_element_located((By.CSS_SELECTOR, "button[class='btn btn-lg btn-block btn-primary']")))
            except TimeoutException:
                st = taskStatus(billing['name']+"             Error, Couldnt cart after queue",id)
                return False
        #QT check
        if qtToBuy > 1:
            try:
                qtSelect = Select(WebDriverWait(driver, 2).until(EC.presence_of_element_located((By.CSS_SELECTOR, "select[class='c-dropdown v-medium fluid-item__quantity']"))))
            except TimeoutException:
                st = taskStatus(billing['name']+"             Unable to select Quantity",id)

            if int(billing['quantity']) >= (len(qtSelect.options)):
                temp = len(qtSelect.options)-2
                qtSelect.select_by_index(temp)
                tempPurchaseAmount = temp
                st = taskStatus(billing['name']+"             Max QT per Checkout is "+str(temp),id)
                time.sleep(1)
            if int(billing['quantity']) < (len(qtSelect.options)):
                qtSelect.select_by_visible_text(str(qtToBuy))
                tempPurchaseAmount = qtToBuy
                st = taskStatus(billing['name']+"             Able to checkout with requested amount of ",id)
                running = False
                time.sleep(1)

        # Click checkout
        st = taskStatus(billing['name']+"             Checking Out!",id)
        ActionChains(driver).click(checkoutButton).perform()

        
        try:
            buttonParent = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "div[class='button-wrap ']")))
        except TimeoutException:
            st = taskStatus(billing['name']+"             Gotta try and check out again",id)
            # Check for checkout button
            try:
                checkoutButton = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "button[class='btn btn-lg btn-block btn-primary']")))
            except TimeoutException:
                st = taskStatus(billing['name']+"             Unable To Cart",id)
                return False 
            # Click checkout
            st = taskStatus(billing['name']+"             Checking Out!",id)
            ActionChains(driver).click(checkoutButton).perform()

            try:
                buttonParent = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "div[class='button-wrap ']")))
            except TimeoutException:
                st = taskStatus(billing['name']+"             Unable to Checkout, maybe oos?",id)
                return False


        # Determine if we can guest checkout or log in
        try:
            guestCheckout = WebDriverWait(driver, 4).until(EC.presence_of_element_located((By.CSS_SELECTOR, "button[class='btn btn-secondary btn-lg cia-guest-content__continue guest']")))
            st = taskStatus(billing['name']+"             Guest Checkout",id)
            ActionChains(driver).click(guestCheckout).perform()
        except:
            st = taskStatus(billing['name']+"             Guest Checkout Not Available",id)
            try:
                st = taskStatus(billing['name']+"             Signing In",id)
                accounts = accountsModule(1,None)
                if accounts == False:
                    st = taskStatus(billing['name']+"             Couldnt sign in, no accounts in /User Data/accounts.txt",id)
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
                    st = taskStatus(billing['name']+"             You need to verify your account, a code has been sent to your email.",id)
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
                        st = taskStatus(billing['name']+"             Incorrect or expired code, restarting flow",id)
                        return False
                    except TimeoutException:
                        st = taskStatus(billing['name']+"             Correct Code, moving on",id)

                except TimeoutException:
                    st = ""

            except TimeoutException:
                st = taskStatus(billing['name']+"             Checkout Flow Error",id)
                return False
        
        # Wait for ispu switch
        try:
            ispuSwitch = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, "a[class='ispu-card__switch']")))
            if ispuSwitch.text == "Switch to Shipping":
                if billing["storePickup"] != True:
                    st = taskStatus(billing['name']+"             Changing from store pickup to ship to home",id)
                    ActionChains(driver).click(ispuSwitch).perform()
            else:
                if billing["storePickup"]:
                    st = taskStatus(billing['name']+"             Changing from shipping to Store pickup",id)
                    ActionChains(driver).click(ispuSwitch).perform()
        except TimeoutException:
            st = taskStatus(billing['name']+"             Unable to switch fulfilment",id)
            #return

        if billing["storePickup"]:

            if guestCheckoutFlag:
                try:
                    st = taskStatus(billing['name']+"             Updating store location",id)
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
                    st = taskStatus(billing['name']+"             Unable to change to closest store",id)
                    return False

                st = taskStatus(billing['name']+"             Autofill email",id)

                email = WebDriverWait(driver, 1).until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[id='user.emailAddress']")))
                email.send_keys(billing['profile']['email'])
                phone = driver.find_element_by_css_selector("input[id='user.phone']")
                phone.send_keys(billing['profile']['phone'])

                continuePayment = driver.find_element_by_css_selector("button[class='btn btn-lg btn-block btn-secondary']")
                ActionChains(driver).click(continuePayment).perform()

                try:
                    ccNum = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[id='optimized-cc-card-number']")))
                except TimeoutException:
                    st = taskStatus(billing['name']+"             Timed out",id)
                    return False
                st = taskStatus(billing['name']+"             Autofill payment",id)

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
                    st = taskStatus(billing['name']+"             Timed out",id)
                    return False
                #hideSuggestions.click()
                ActionChains(driver).click(hideSuggestions).perform()
                if billing['profile']['billStreet2'] != "":
                    try:
                        addy2Span = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "button[class='btn btn-link v-medium address-form__showAddress2Link']")))
                    except TimeoutException:
                        st = taskStatus(billing['name']+"             Timed out",id)
                        return False
                    ActionChains(driver).click(addy2Span).perform()
                    #addy2Span.click()

                    try:
                        addy2 = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[id='payment.billingAddress.street2']")))
                    except TimeoutException:
                        st = taskStatus(billing['name']+"             Timed out",id)
                        return False

                    addy2.send_keys(billing['profile']['billStreet2'])

                city = driver.find_element_by_css_selector("input[id='payment.billingAddress.city']")
                city.send_keys(billing['profile']['billCity'])
                state = Select(driver.find_element_by_css_selector("select[id='payment.billingAddress.state']"))
                state.select_by_visible_text(billing['profile']['billState'])
                zip = driver.find_element_by_css_selector("input[id='payment.billingAddress.zipcode']")
                zip.send_keys(billing['profile']['billZip'])

                st = taskStatus(billing['name']+"             Placing Order",id)
                placeButton = driver.find_element_by_css_selector("button[class='btn btn-lg btn-block btn-primary']")
                ActionChains(driver).click(placeButton).perform()

                stopTime = time.time()

            else:
                try:
                    ispuSwitch = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, "a[class='btn-default-link link-styled-button ispu-card__switch']")))
                    if ispuSwitch.text != "Switch to Shipping":
                        st = taskStatus(billing['name']+"             Changing from shipping to Store pickup",id)
                        ActionChains(driver).click(ispuSwitch).perform()
                    try:
                        st = taskStatus(billing['name']+"             Updating store location",id)
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
                        st = taskStatus(billing['name']+"             No store within 250 miles",id)
                        return False
                except TimeoutException:
                    st = taskStatus(billing['name']+"             Unable to switch fulfilment",id)
                    #return

        else:
            if guestCheckoutFlag != True:
                try:
                    addNewAddy = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "button[class='btn-default-link saved-addresses__add-new-link']")))
                    ActionChains(driver).click(addNewAddy).perform()
                    st = taskStatus(billing['name']+"             Adding new address",id)
                except TimeoutException:
                    st = ""

                try:
                    st = taskStatus(billing['name']+"             Autofill address info",id)
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
                        st = taskStatus(billing['name']+"             Timed out",id)
                        return False
                    #hideSuggestions.click()
                    ActionChains(driver).click(hideSuggestions).perform()
                    if billing['profile']['billStreet2'] != "":
                        try:
                            addy2Span = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "button[class='btn btn-link v-medium address-form__showAddress2Link']")))
                        except TimeoutException:
                            st = taskStatus(billing['name']+"             Timed out",id)
                            return False
                        ActionChains(driver).click(addy2Span).perform()
                        #addy2Span.click()

                        try:
                            addy2 = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[id='ui.address.street2']")))
                        except TimeoutException:
                            st = taskStatus(billing['name']+"             Timed out",id)
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
                
                    st = taskStatus(billing['name']+"             Autofill payment",id)

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

                    st = taskStatus(billing['name']+"             Placing Order",id)
                    placeButton = driver.find_element_by_css_selector("button[class='btn btn-lg btn-block btn-primary button__fast-track']")
                    time.sleep(1.5)
                    ActionChains(driver).click(placeButton).perform()

                    stopTime = time.time()

                except TimeoutException:
                    st = taskStatus(billing['name']+"             ERROR with sign in checkout",id)
                    return False
            else:
                inputNum = "2"
                # Wait for First Name field, sometimes delayed
                try:
                    fName = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[id='consolidatedAddresses.ui_address_"+inputNum+".firstName']")))
                    fName.send_keys(billing['profile']['fName'])

                except TimeoutException:
                    st = taskStatus(billing['name']+"             Best Buy antibot measures detected",id)
                    try:
                        inputNum = "5"
                        fName = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[id='consolidatedAddresses.ui_address_"+inputNum+".firstName']")))
                        fName.send_keys(billing['profile']['fName'])
                    except TimeoutException:
                        st = taskStatus(billing['name']+"             Error with name input fields",id)
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
                    st = taskStatus(billing['name']+"             Timed out",id)
                    return False
                #hideSuggestions.click()
                ActionChains(driver).click(hideSuggestions).perform()
                #if need second line of address
                if billing['profile']['billStreet2'] != "":
                    try:
                        addy2Span = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "button[class='btn btn-link v-medium address-form__showAddress2Link']")))
                    except TimeoutException:
                        st = taskStatus(billing['name']+"             Timed out",id)
                        return False
                    ActionChains(driver).click(addy2Span).perform()
                    #addy2Span.click()

                    try:
                        addy2 = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[id='consolidatedAddresses.ui_address_"+inputNum+".street2']")))
                    except TimeoutException:
                        st = taskStatus(billing['name']+"             Timed out",id)
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
                    st = taskStatus(billing['name']+"             Timed out",id)
                    return False
                st = taskStatus(billing['name']+"             Autofill payment",id)

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

                st = taskStatus(billing['name']+"             Placing Order",id)
                placeButton = driver.find_element_by_css_selector("button[class='btn btn-lg btn-block btn-primary']")
                ActionChains(driver).click(placeButton).perform()

                stopTime = time.time()

        alert = None 

        try:
            alert = WebDriverWait(driver, 8).until(EC.presence_of_element_located((By.CSS_SELECTOR, "div[class='order-errors']")))
        except TimeoutException:
            st = taskStatus(billing['name']+"             No Errors!",id)
        
        if alert != None:
            cardDeclineText = "Unfortunately, we were unable to process your credit card. Please try again or use a different card to continue with your order. For questions regarding your credit card, please contact your bank."
            maxQtLimitText = "If you have other items you'd like to buy, you'll need to remove this item to continue."
            st = taskStatus(billing['name']+"             Order Error!",id)
            if cardDeclineText == driver.find_element_by_css_selector("div[class='error-spacing']").text:
                st = taskStatus(billing['name']+"             Card Declined",id)
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
                st = taskStatus(billing['name']+"             Max Items reached for this profile and sku",id)
                return
            st = taskStatus(billing['name']+"             Max Items reached for this profile and sku",id)
            return
            return False

        order = ""
        try:
            test = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "span[class='thank-you-enhancement__emphasis']")))
        except TimeoutException:
            st = taskStatus(billing['name']+"             Timed out",id)
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
        st = taskStatus(billing['name']+"             Checkout Successful! Total = " + total + " & took " + str(stopTime-startTime),id)
        qtToBuy -= tempPurchaseAmount
        if qtToBuy == 0:
            st = taskStatus("",-2)
            return True
    return True

#Newegg Search Module
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

#temp server to capture callback
def serverRun():
    HOST = os.environ.get('SERVER_HOST', 'localhost')
    try:
       PORT = 8080
    except ValueError:
       PORT = 8080
    tempServer.run(HOST, PORT)

#callback route
@tempServer.route('/')
def callback():
    code = request.args.get('code')
    func = request.environ.get('werkzeug.server.shutdown')
    if code == None:
        return
    callbackFlow(code, func)
    return ""

#INIT
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
        os.startfile(url)

        serverRun()
    
    time.sleep(2)
    root.afterSplash()
    return

    while running:
        print(welcomeText)

        if userInput == None:
            print("Main Menu\n1. Search\n2. Tasks\n3. Profiles\n4. Webhook\n5. Settings\n6. Exit")
            userInput = input()

        # Search Menu
        if str(userInput).lower() == "search" or str(userInput) == "1":
            os.system('cls' if os.name == 'nt' else 'clear')
            print("Quick Search\nChoose BestBuy, Newegg, Home Depot, Pokemon Center or Back:")
            searchInput = input()
            if str(searchInput).lower() == "bestbuy":
                print("Enter the sku:")
                sku = {}
                sku['name'] = "Search"
                sku['sku'] = input()
                bbSearchModule(sku, None)
            if str(searchInput).lower() == "newegg":
                print("Enter the model:")
                neweggSearchModule(input(), None)
            if str(searchInput).lower() == "home depot":
                print("Enter the internet#:")
                homedepotSearchModule(input(), None)
            if str(searchInput).lower() == "pokemon center":
                print("Enter the sku:")
                pokemonSearchModule(input(), None)
            if str(searchInput).lower() == "back":
                userInput = None
                os.system('cls' if os.name == 'nt' else 'clear')

        # Tasks Menu
        if str(userInput).lower() == "tasks" or str(userInput) == "2":
            os.system('cls' if os.name == 'nt' else 'clear')
            print("Tasks Module\n1.Run\n2.Quick Task\n3.Create\n4.View\n5.Delete\n6.Back")
            taskInput = input()
            if str(taskInput).lower() == "run" or str(taskInput) == "1":
                tasks = taskSaveModule(1,{})
                if tasks == False:
                    print("You dont have any Tasks to Run!")
                if tasks != False:
                    print("Choose one of the tasks below by name, type all for all or hit any key to go back\n")
                    counter = 1
                    for task in tasks["taskList"]:
                        print(str(counter)+". "+task["name"])
                        counter+=1
                    print()
                    selectInput = input()
                    if str(selectInput).lower() == "all":
                        for i in range(len(tasks["taskList"])):
                            #with tempfile.NamedTemporaryFile(suffix='.command') as f:
                                #tempString = "#! /bin/bash\ncd ~/Desktop/App Projects(Local)/FortuneBot/\npython3 main.py {} True\n".format(i)
                                #f.write(tempString.encode('utf-8'))
                                #st = os.stat(f.name)
                                #os.chmod(f.name, st.st_mode | stat.S_IEXEC)
                                #subprocess.call(['open', '-W', f.name])
                            if exeMode == True:
                                subprocess.Popen('start /wait FortuneBot.exe "'+str(i)+'" True', shell=True)
                            if exeMode == False:
                                subprocess.Popen('start /wait python FortuneBot.py "'+str(i)+'" True', shell=True)
                    for i in range(len(tasks["taskList"])):
                        if str(selectInput).lower() == tasks["taskList"][i]["name"].lower() or selectInput == str(i+1):

                            #with tempfile.NamedTemporaryFile(suffix='.command') as f:

                                #tempString = "#! /bin/bash\ncd ~/Desktop/App Projects(Local)/FortuneBot/\npython3 main.py {} True\n".format(i)
                                #f.write(tempString.encode('utf-8'))
                                #st = os.stat(f.name)
                                #os.chmod(f.name, st.st_mode | stat.S_IEXEC)
                                #subprocess.call(['open', '-W', f.name])
                            if exeMode == True:
                                subprocess.Popen('start /wait FortuneBot.exe "'+str(i)+'" True', shell=True)
                            if exeMode == False:
                                subprocess.Popen('start /wait python FortuneBot.py "'+str(i)+'" True', shell=True)
            if str(taskInput).lower() == "quick task" or str(taskInput) == "2":
                settings = settingsModule(1,None)
                if settings['qtProfile'] == "":
                    print("Quick Task profile not set, go to settings and set one!")
                    taskInput = None

                print("Enter the sku to start or type back: ")
                sku = input()
                if str(sku).lower() == "back":
                    taskInput = None
                else:
                    task = {
                        'name': 'QuickTask'+sku,
                        'sku':sku,
                        'quantity':1,
                        'storePickup':False,
                        'profile':settings['qtProfile'],
                        'date':False,
                        'time':False
                        }
                    taskSaveModule(2,task)
                    tasks = taskSaveModule(1,{})

                    if exeMode == True:
                        subprocess.Popen('start /wait FortuneBot.exe "'+str(len(tasks['taskList'])-1)+'" True', shell=True)
                    if exeMode == False:
                        subprocess.Popen('start /wait python FortuneBot.py "'+str(len(tasks['taskList'])-1)+'" True', shell=True)
            if str(taskInput).lower() == "create" or str(taskInput) == "3":
                task = {}
                print("Enter Task Name")
                task['name'] = input()
                print("Enter item Sku")
                task['sku'] = input()
                print("Enter item quantity")
                task['quantity'] = input()
                print("Store Pickup? Yes/No")
                storePickup = input()
                if str(storePickup).lower() == "yes":
                    task['storePickup'] = True
                if str(storePickup).lower() == "no":
                    task['storePickup'] = False
                print("Choose Profile")
                profiles = profileModule(1,{})
                if profiles == False:
                    print("You dont have any profiles!")
                    taskInput = None
                if profiles != False:
                    counter = 1
                    for profile in profiles["profileList"]:
                        print(str(counter)+". "+profile["profileName"])
                        counter += 1
                profileSelect = input()
                for i in range(len(profiles["profileList"])):
                    if profiles["profileList"][i]["profileName"].lower() == profileSelect.lower() or profileSelect == str(i+1):
                        task['profile'] = profiles["profileList"][i]
                print("Is this for a task in the future? Yes/No")
                dateTask = input()
                if str(dateTask).lower() == "yes":
                    print("Enter task date, i.e. MM/DD/YYYY")
                    task['date'] = input()
                    print("Enter time to execute, i.e. 12:00PM")
                    task['time'] = input()
                if str(dateTask).lower() == "no":
                    task['date'] = False
                    task['time'] = False
                print("Confirm Task Info:")
                print("Name: "+task["name"])
                print("Sku: "+task["sku"])
                print("Quantity: "+task["quantity"])
                print("Store Pickup: "+str(task["storePickup"]))
                print("Profile: "+task["profile"]["profileName"])
                print("Date: "+str(task["date"]))
                print("Time: "+str(task["time"]))
                print("Correct? Yes/No")
                answer = input()
                if str(answer).lower() == "yes":
                    taskSaveModule(2,task)
                if str(answer).lower() == "no":
                    taskInput = None
            if str(taskInput).lower() == "view" or str(taskInput) == "4":
                tasks = taskSaveModule(1,{})
                if tasks == False:
                    print("You dont have any Tasks!")
                if tasks != False:
                    for task in tasks["taskList"]:
                        print(task["name"])
                input()
            if str(taskInput).lower() == "delete" or str(taskInput) == "5":
                tasks = taskSaveModule(1,{})
                if tasks == False:
                    print("You dont have any Tasks to Delete!")
                if tasks != False:
                    for task in tasks["taskList"]:
                        print(task["name"])
                    print("Type the name of the task you want to delete")
                    taskSaveModule(3,input())
            if str(taskInput).lower() == "back" or str(taskInput) == "6":
                userInput = None
                os.system('cls' if os.name == 'nt' else 'clear')

        # Profiles Menu
        if str(userInput).lower() == "profiles" or str(userInput) == "3":
            os.system('cls' if os.name == 'nt' else 'clear')
            print("Profiles Module\n1.Create\n2.Delete\n3.View\n4.Back")
            profileInput = input()

            if str(profileInput).lower() == "create" or str(profileInput) == "1":
                profile = {}
                print("Profile Name")
                profile['profileName'] = input()
                print("First Name")
                profile['fName'] = input()
                print("Last Name")
                profile['lName'] = input()
                print("Email")
                profile['email'] = input()
                print("Phone")
                profile['phone'] = input()
                print("Billing Street 1")
                profile['billStreet1'] = input()
                print("Billing Street 2, hit enter to skip")
                profile['billStreet2'] = input()
                print("Billing City")
                profile['billCity'] = input()
                print("Billing State - Two Letters i.e. PA")
                profile['billState'] = input()
                print("Billing Zip")
                profile['billZip'] = input()
                print("Credit Card #")
                profile['cc'] = input()
                print("Credit Card Exp Month i.e. MM")
                profile['ccExpMM'] = input()
                print("Credit Card Exp Year i.e. YYYY")
                profile['ccExpYYYY'] = input()
                print("Credit Card CVV")
                profile['cvv'] = input()
                profileModule(2,profile)
            if str(profileInput).lower() == "delete" or str(profileInput) == "2":
                profiles = profileModule(1,{})
                if profiles != False:
                    for profile in profiles["profileList"]:
                        print(profile["profileName"])
                    print("Type the name of the profile you want to delete")
                    profileModule(3,input())
                if profiles == False:
                    print("You dont have any profiles to delete!")
            if str(profileInput).lower() == "view" or str(profileInput) == "3":
                profiles = profileModule(1,{})
                if profiles == False:
                    print("You dont have any profiles!")
                if profiles != False:
                    for profile in profiles["profileList"]:
                        print(profile["profileName"])
                input()
            if str(profileInput).lower() == "back" or str(profileInput) == "4":
                userInput = None
                os.system('cls' if os.name == 'nt' else 'clear')

        # Webhook Settings
        if str(userInput).lower() == "webhook" or str(userInput) == "4":
            os.system('cls' if os.name == 'nt' else 'clear')
            print("Webhook Settings")
            print("1.Add\n2.Remove\n3.Back")
            webhookInput = input()

            if str(webhookInput).lower() == "add" or str(webhookInput) == "1":
                print("Paste The Discord webhook you would like to add")
                addWebhook = input()
                webhookModule({},addWebhook,3)
            if str(webhookInput).lower() == "remove" or str(webhookInput) == "2":
                webhooks = webhookModule({},"",2)
                if webhooks != False and len(webhooks["urls"]) > 0:
                    print("Choose the number of the webhook you want to remove")
                    for i in range(len(webhooks["urls"])):
                        print(str(i+1)+". "+webhooks["urls"][i])
                    webhookModule({},input(),4)
                print("You dont have any webhooks yet!")
            if str(webhookInput).lower() == "back" or str(webhookInput) == "3":
                userInput = None
                os.system('cls' if os.name == 'nt' else 'clear')

        # General Settings
        if str(userInput).lower() == "settings" or str(userInput) == "5":
            os.system('cls' if os.name == 'nt' else 'clear')
            print("General Settings")
            print("Type the option to change its value, or type back")
            settings = settingsModule(1,None)
            if settings == False:
                settings['forceCheckout'] = False
                settings['headless'] = False
                settings['queueTasks'] = 1

            print("1. Force Checkout : "+str(settings['forceCheckout']))
            print("2. Dev Mode : "+str(settings['headless']))
            print("3. Queue Tasks : "+str(settings['queueTasks']))
            if settings['qtProfile'] == "":
                print("4. Quick Task Profile: "+"Not Set")
            else:
                print("4. Quick Task Profile: "+settings['qtProfile']['profileName'])

            userCheckout = input()
            if str(userCheckout).lower() == "force checkout" or str(userCheckout) == "1":
                settingsModule(2,not settings['forceCheckout'])
                userInput = None
                os.system('cls' if os.name == 'nt' else 'clear')
                print("Saved setting!\n")
            if str(userCheckout).lower() == "dev mode" or str(userCheckout) == "2":
                settingsModule(3,not settings['headless'])
                userInput = None
                os.system('cls' if os.name == 'nt' else 'clear')
                print("Saved setting!\n")
            if str(userCheckout).lower() == "queue tasks" or str(userCheckout) == "3":
                print("enter how many you would like for when the queue is detected")
                settingsModule(5,input())
                userInput = None
                os.system('cls' if os.name == 'nt' else 'clear')
                print("Saved setting!\n")
            if str(userCheckout).lower() == "quick task profile" or str(userCheckout) == "4":
                profiles = profileModule(1,{})
                if profiles == False:
                    print("You dont have any profiles!")
                    taskInput = None
                if profiles != False:
                    print("Select a profile to set as the quick task profile.")
                    counter = 1
                    for profile in profiles["profileList"]:
                        print(str(counter)+". "+profile["profileName"])
                        counter += 1
                profileSelect = input()
                for i in range(len(profiles["profileList"])):
                    if profiles["profileList"][i]["profileName"].lower() == profileSelect.lower() or profileSelect == str(i+1):
                        settingsModule(6,profiles["profileList"][i])

            if str(userCheckout).lower() == "back":
                userInput = None
                os.system('cls' if os.name == 'nt' else 'clear')

        # Exit
        if str(userInput).lower() == "exit" or str(userInput) == "6":
            print("Exiting FortuneBot, Bye!")
            running = False
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

#Splash Pane
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

#Menu Pane
class MenuPane:
    global root
    def __init__(self):
        self.frame = Frame(width=200,height=720,bg="#141425")

        self.lbl_logo = Label(self.frame,text="FortuneBot",fg="#F06543",bg="#141425",font=font.Font(size=30))
        self.lbl_version = Label(self.frame,text=botVersion,fg="#F06543",bg="#141425")

        self.btn_search = Button(self.frame,text="Search (Developer)",width=50,height=3)
        self.btn_tasks = Button(self.frame,text="Tasks",width=50,height=3)
        self.btn_profiles = Button(self.frame,text="Profiles",width=50,height=3)
        self.btn_settings = Button(self.frame,text="Settings",width=50,height=3,command=root.showSettings)

        self.lbl_logo.grid(row=0,column=0)

        self.btn_search.grid(row=2,column=0)
        self.btn_tasks.grid(row=3,column=0)
        self.btn_profiles.grid(row=4,column=0)
        self.btn_settings.grid(row=5,column=0)

        self.lbl_version.grid(row=7,column=0)

#Settings Pane
class SettingsPane:
    def __init__(self):
        self.frame = Frame(width=1070,height=720)

    def toggleForceCheckout(self):
        settingsModule(2,not self.settings['forceCheckout'])
    def toggleDevMode(self):
        settingsModule(3,not self.settings['headless'])
    def toggleQueue(self):
        settingsModule(5,self.queue.get())

    def getPane(self):
        self.settings = settingsModule(1, None)
        self.force = BooleanVar(value=bool(self.settings['forceCheckout']))
        self.dev = BooleanVar(value=bool(self.settings['headless']))
        self.queue = IntVar(value=int(self.settings['queueTasks']))

        self.forceCheckout = Checkbutton(self.frame, text='Force Checkout',variable=self.force, onvalue=True, offvalue=False, command=self.toggleForceCheckout)
        self.devMode = Checkbutton(self.frame, text='Developer Mode',variable=self.dev, onvalue=True, offvalue=False, command=self.toggleDevMode)
        self.queueTasks = Entry(self.frame, textvariable=self.queue, validate='key', validatecommand=self.toggleQueue)

        self.forceCheckout.grid(row=0,column=0)
        self.devMode.grid(row=1,column=0)
        self.queueTasks.grid(row=2,column=1)
        return self.frame

#Root Window
class RootWindow:

    def __init__(self):
        self.roots = Tk()

        self.splash = SplashPane()
        self.splashPane = self.splash.frame

        
        self.roots.resizable(False, False)
        self.roots.title("FortuneBot")
        self.roots.geometry('1280x720')

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

    def showSettings(self):
        if self.content != None:
            self.content.pack_forget()
        self.content = SettingsPane()
        self.content.getPane().pack(fill=BOTH,side=RIGHT)
root = RootWindow()

# Main Function
if __name__ == "__main__":
    multiprocessing.freeze_support()

    wait = appInit()
    
    root.start()
    
    
    