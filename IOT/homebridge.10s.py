#!/usr/bin/python3
#encoding: utf-8

# <bitbar.title>Homebridge Controller</bitbar.title>
# <bitbar.version>v1.0</bitbar.version>
# <bitbar.author>Eric Andrechek</bitbar.author>
# <bitbar.author.github>EricAndrechek</bitbar.author.github>
# <bitbar.desc>Control Homebridge and connected devices.</bitbar.desc>
# <bitbar.image>https://user-images.githubusercontent.com/35144594/102293908-0b849200-3f16-11eb-9778-7ce25edcc7ec.png</bitbar.image>
# <bitbar.dependencies>python, requests module</bitbar.dependencies>
# <bitbar.abouturl>https://homebridge.io/</bitbar.abouturl>

import requests
import json
import pathlib
import os
import sys


homebridgeIcon = "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"
offlineIcon = "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"

def printer(content):
    if type(content) is list:
        for line in content:
            print(line + " | color=white")
    elif content != "---" and content != "--":
        print(content + " | color=white")
    else:
        print(content)


def doStuff(token, url, icon, command, unit):
    headers = {
        'accept': '*/*',
        'Authorization': 'Bearer {}'.format(token),
    }

    if command:
        if command == "restart":
            requests.put('{}/api/server/restart'.format(url), headers=headers)
        elif command == "reboot":
            requests.put('{}/api/platform-tools/linux/restart-host'.format(url), headers=headers)
    else:
        cpu = ""
        temp = ""
        ram = ""
        updates = []
        numUpdates = 0
        uptime = ""
        status = ""
        state = False

        updatesRequest = requests.get('{}/api/plugins'.format(url), headers=headers)
        if updatesRequest.status_code == 200:
            for plugin in updatesRequest.json():
                name = plugin['name']
                update = plugin['updateAvailable']
                link = ""
                try:
                    name = plugin['displayName']
                except:
                    pass
                try:
                    link = plugin['links']["homepage"]
                except:
                    pass
                if update is True:
                    numUpdates += 1
                updates.append("{} v{} - {} | href={}".format(name, plugin['installedVersion'], "up to date" if not update else "new update v{}".format(plugin['latestVersion']), link))
        nodeJSRequest = requests.get('{}/api/status/nodejs'.format(url), headers=headers)
        if nodeJSRequest.status_code == 200:
            nodeVersion = nodeJSRequest.json()
            updates.append("NodeJS {} - {}".format(nodeVersion['currentVersion'], "up to date" if not nodeVersion['updateAvailable'] else "new update {}".format(nodeVersion['latestVersion'])))
            numUpdates += 1
        numUpdates = "Avaliable Updates: " + str(numUpdates)

        cpuRequest = requests.get('{}/api/status/cpu'.format(url), headers=headers)
        if cpuRequest.status_code == 200:
            cpu = "CPU: " + str(round(float(cpuRequest.json()["currentLoad"]))) + "%"
            try:
                init_temp = float(cpuRequest.json()["cpuTemperature"]["main"])
                if unit == "F":
                    init_temp = str(round((init_temp * (9/5)) + 32))
                else:
                    init_temp = str(round(init_temp)) 
                temp = "Temperature: " + init_temp + "˚" + unit
            except:
                pass
        
        ramRequest = requests.get('{}/api/status/ram'.format(url), headers=headers)
        if ramRequest.status_code == 200:
            ram = "RAM: " + str(round((int(ramRequest.json()["mem"]["used"]) / int(ramRequest.json()["mem"]["total"])) * 100)) + "%"
        
        uptimeRequest = requests.get('{}/api/status/uptime'.format(url), headers=headers)
        if uptimeRequest.status_code == 200:
            uptime = "Uptime: " + str(round(round(float(uptimeRequest.json()["processUptime"])) / 86400)) + " days"
        
        statusRequest = requests.get('{}/api/status/homebridge'.format(url), headers=headers)
        if statusRequest.status_code == 200:
            status = "Homebridge is " + statusRequest.json()["status"] + ""
            if statusRequest.json()["status"] == "up":
                state = True
        
        ico = ""
        if icon.upper() == "CPU":
            ico = cpu.split(": ")[1]
        elif icon.upper() == "RAM":
            ico = ram.split(": ")[1]
        elif icon.upper() == "TEMP":
            ico = temp.split(": ")[1]
        elif icon.upper() == "UPTIME":
            ico = uptime.split()[1] + "d"
        elif icon.upper() == "UPDATES":
            ico = numUpdates.split(": ")[1]
        else:
            ico = "| image={}".format(homebridgeIcon) if state else "| image={}".format(offlineIcon)
        print(ico)
        printer('---')
        printer(status + " | href=" + url)
        printer(numUpdates)
        printer(uptime)
        printer('---')
        printer(cpu)
        printer(ram)
        printer(temp)
        printer('---')
        printer(updates)
        printer('---')
        print('Restart Homebridge | bash="' + str(__file__) + '" param1=restart terminal=false')
        print('Reboot Server | bash="' + str(__file__) + '" param1=reboot terminal=false')

def login(username, password, url, icon, command, unit, config):
    headers = {
        'accept': '*/*',
        'Content-Type': 'application/json',
    }
    data = {
        "username": username,
        "password": password
    }
    response = requests.post('{}/api/auth/login'.format(url), headers=headers, data=json.dumps(data))
    if response.status_code == 201:
        token = response.json()['access_token']
        firstSection = ""
        lastSection = ""
        with open(config, 'r') as oldConfig:
            conf = oldConfig.read().split('[homebridge]')
            firstSection = conf[0]
            try:
                lastSection = "[" + conf[1].split("[")[1]
            except IndexError:
                pass
        with open(config, 'w') as newConfig:
            newConfig.write(firstSection)
            newConfig.write('[homebridge]\n')
            newConfig.write("# edit the username and password to your homebridge's and then save and close\n")
            newConfig.write("# you can also modify the url from the default if desired\n")
            newConfig.write("# to change the icon image, specify whether you want to see: \"CPU\", \"TEMP\", \"RAM\", \"UPTIME\", \"UPDATES\", or \"STATUS\". Defaults to \"STATUS\"\n")
            newConfig.write("username = \"{}\"\n".format(username))
            newConfig.write("password = \"{}\"\n".format(password))
            newConfig.write("url = \"{}\"\n".format(url))
            newConfig.write("icon = \"{}\"\n".format(icon))
            newConfig.write("token = \"{}\"\n".format(token))
            newConfig.write("unit = \"{}\"\n".format(unit))
            newConfig.write(lastSection)
        doStuff(token, url, icon, command, unit)
    else:
        printer('❌') # login failed

config = pathlib.Path.home().joinpath('.config', 'bitbar', 'config')
config.touch(exist_ok=True)

command = None
if len(sys.argv) > 1:
    command = sys.argv[1]

hbConfig = []
with open(config, 'r') as file:
    for section in file.read().split('['):
        if section.split('\n')[0] == 'homebridge]':
            hbConfig = section.split('\n')[3:]
if hbConfig == []:
    with open(config, "a") as file:
        file.write("\n[homebridge]\n")
        file.write("# edit the username and password to your homebridge's and then save and close\n")
        file.write("# you can also modify the url from the default if desired\n")
        file.write("# to change the icon image, specify whether you want to see: \"CPU\", \"TEMP\", \"RAM\", \"UPTIME\", \"UPDATES\", or \"STATUS\". Defaults to \"STATUS\"\n")
        file.write("username = \"\"\n")
        file.write("password = \"\"\n")
        file.write("url = \"http://homebridge.local\"\n")
        file.write("icon = \"STATUS\"\n")
        file.write("token = \"\"\n")
        file.write("unit = \"C\"\n")
    os.system("open " + str(config))
else:
    token = ""
    username = ""
    password = ""
    url = ""
    icon = ""
    unit = ""
    for line in hbConfig:
        if line.split(" = ")[0] == "username":
            username = line.split(" = ")[1].split("\"")[1]
        elif line.split(" = ")[0] == "password":
            password = line.split(" = ")[1].split("\"")[1]
        elif line.split(" = ")[0] == "token":
            token = line.split(" = ")[1].split("\"")[1]
        elif line.split(" = ")[0] == "url":
            url = line.split(" = ")[1].split("\"")[1]
        elif line.split(" = ")[0] == "icon":
            icon = line.split(" = ")[1].split("\"")[1]
        elif line.split(" = ")[0] == "unit":
            unit = line.split(" = ")[1].split("\"")[1]
    if token:
        headers = {
            'accept': '*/*',
            'Authorization': 'Bearer {}'.format(token),
        }

        checkToken = requests.get('{}/api/auth/check'.format(url), headers=headers)
        if checkToken.status_code == 401:
            login(username, password, url, icon, command, unit, config)
        elif checkToken.status_code == 200:
            doStuff(token, url, icon, command, unit)
        else:
            printer("❌")
    else:
        login(username, password, url, icon, command, unit, config)
