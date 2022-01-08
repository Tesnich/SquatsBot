# squatsbot.py

import os
from os.path import exists

import discord
from discord.ext import tasks, commands

import csv

import datetime

TOKEN = "" #secret, do not share!

notificationDelay = 24 #in hours

class CustomClient(discord.Client):

    #///////////////////////////////////////////////////////////////////////////////////
    #   Method Run On Bot Connection To Discord Servers
    async def on_ready(self):
        print(str(client.user) + ' has connected to Discord!')
        for guild in client.guilds:
            print('Connected to ... ' + str(guild)+'!')
            if(exists(str(guild) +'.csv')):
                print('    '+str(guild)+'.csv found!')
                print('    ...Ready!')
            else:
                print('    '+str(guild)+'.csv MISSING! Creating...')
                with open (str(guild)+'.csv', 'w') as csvIn: #will associating the guild name with file storage be a problem? What if server is renamed ... fix it later?
                    filewriter = csv.writer(csvIn)
                    filewriter.writerow(['Server', str(guild)])
                    filewriter.writerow(['Standard',10,15,20,25,0,30,35,40,45,0,50,55,60,65,0,70,75,80,85,0,90,95,100,105,0,110,115,120,125,130])
                    filewriter.writerow(['Hard',50,55,60,0,70,75,80,0,100,105,110,0,130,135,140,0,150,155,160,0,180,185,190,0,220,225,230,0,240,250])
                    filewriter.writerow(['USERS'])
                print('    ...Done. Ready!')

    #///////////////////////////////////////////////////////////////////////////////////
    #   Messaging new members to discord to get swole!
    async def on_member_join(self, member):
        await member.create_dm()
        await member.dm_channel.send('Hi '+ member.name +', welcome to the discord! If you want to get swole hit me up fam.')

    #///////////////////////////////////////////////////////////////////////////////////
    #   method run anytime a message is dropped in a channel visible to the bot
    async def on_message(self, message):
        #dont respond to self
        if message.author == client.user:
            return
        
        #///////////////////////////////////////////////////////////////////////////////////
        #   Help text/ explainer
        if message.content == '!squatsbot help':
            response = "Looks like you want to get swole... **BEHOLD THY COMMANDS!**\n----------------------------------------------------------------------------\n!squatsbot signup - Sign up for daily Squatifications!\n!squatsbot swolechief managed - End your daily Squatifications.\n!squatsbot schedule event - schedule a new 30 day event starting now! (replaces old schedule)\n!squatsbot start notify - Start bot notifications! The time at which this command is sent will be the time participants will get a reminder each day!\n!squatsbot stop notify - Stop daily reminders.\n----------------------------------------------------------------------------"
            #\n!SquatsBot Heathens - Show active squatters! *Maybe lock the door next time...*
            await message.channel.send(response)

        #///////////////////////////////////////////////////////////////////////////////////
        #   Subcribe to notifications
        if message.content == '!squatsbot signup':
            guildFileName = str(message.guild) +'.csv' #depending on  when server is added file might not exist
            userFound = False
            lines = list()
            users = list()

            with open (guildFileName, 'r') as csvOut:
                fileReader = csv.reader(csvOut)
                for row in fileReader:
                    if(row[0] == 'USERS'):
                        for item in row:
                            users.append(item)
                            if (item == str(message.author.id)):
                                userFound = True
                    else:
                        lines.append(row)

            if (userFound):
                response = "**Chillout" + str(message.author) + ",** you are already a squatter."
                await message.channel.send(response)
            else:
                with open (guildFileName, 'w') as csvIn:
                    fileWriter = csv.writer(csvIn)
                    for line in lines:
                        fileWriter.writerow(line)
                    users.append(str(message.author.id))
                    fileWriter.writerow(users)

                response = "**Your journey has begun " + str(message.author) + "!** You will get a daily reminder to participate for the duration of the event!"
                await message.channel.send(response)
        
        #///////////////////////////////////////////////////////////////////////////////////
        #   Un-subcribe from notifications
        if message.content == '!squatsbot swolechief managed':
            guildFileName = str(message.guild) + '.csv' #depending on  when server is added file might not exist
            userFound = False
            lines = list()
            users = list()

            with open (guildFileName, 'r') as csvOut:
                fileReader = csv.reader(csvOut)
                for row in fileReader:
                    if(row[0] == 'USERS'):
                        for item in row:
                            if (item != str(message.author.id)):
                                users.append(item)
                            else:
                                userFound = True
                    else:
                        lines.append(row)
                lines.append(users)

            if (userFound):   
                with open (guildFileName, 'w') as csvIn:
                    fileWriter = csv.writer(csvIn)
                    for line in lines:
                        fileWriter.writerow(line)

                response = "**Congrats on getting swole " + str(message.author) + "!** Go out there and show off those beautiful leg muscles! Kick in a door or something idk."
                await message.channel.send(response)
            else:
                response = "**You are not currently subscribed to squatifications, " + str(message.author) + ".** Nothing has been done."
                await message.channel.send(response)
        
        #///////////////////////////////////////////////////////////////////////////////////
        #   Get an update on progress of event
        # if message.content == '!SquatsBot Update':
        #     response = "Update!"
        #     await message.channel.send(response)

        #///////////////////////////////////////////////////////////////////////////////////
        #   See all subcribed participants
        # if message.content == '!SquatsBot Heathens':
        #     response = "We got lots of people, james is just busy and hasn't coded this yet."
        #     await message.channel.send(response)

        #///////////////////////////////////////////////////////////////////////////////////
        #   Schedule Event (fill dates)
        if message.content == '!squatsbot schedule event':
            if (message.author.top_role.permissions.administrator or str(message.author.id) == '234466321465737216'):
                today = datetime.date.today()
                now = datetime.datetime.now()
                startTime = now.strftime("%H:%M:%S")
                print("Today's date:", today)
                print("Start Time : ", startTime)
                dates = list()
                dates.append('Date')
                for i in range(30):
                    dates.append((today + datetime.timedelta(i)).isoformat())
                print (dates)

                guildFileName = str(message.guild) +'.csv' #depending on  when server is added file might not exist

                lines = list()

                with open (guildFileName, 'r') as csvOut:
                    fileReader = csv.reader(csvOut)
                    for row in fileReader:
                        if(row[0] == 'Date'):
                            continue
                        else:
                            lines.append(row)

                with open (guildFileName, 'w') as csvIn:
                    fileWriter = csv.writer(csvIn)
                    for line in lines:
                        fileWriter.writerow(line)
                    fileWriter.writerow(dates)

                response = "**New event scheduled from " + dates[1] + " to " + dates[30] + "**. To start notifications use the command '!squatsbot start notify'."
                await message.channel.send(response)


        #///////////////////////////////////////////////////////////////////////////////////
        #   Comand to start event notifications
        if '!squatsbot start notify' in message.content:
            if (message.author.top_role.permissions.administrator or str(message.author.id) == '234466321465737216'):
                response = "**Participants will be at notified every " + str(notificationDelay) + " hours.**"
                await message.channel.send(response)
                client.MentionUsers.start(message)
            else:
                response = "**You must be an admin to use this command :(**"
                await message.channel.send(response)

        #///////////////////////////////////////////////////////////////////////////////////
        #   Comand to end event notifications
        if '!squatsbot stop notify' in message.content:
            client.MentionUsers.stop()
            response = "Notifications have been turned off."
            await message.channel.send(response)


    #///////////////////////////////////////////////////////////////////////////////////
    #   Looping task to mention all subscribed users in a daily reminder
    @tasks.loop(hours=notificationDelay)
    #@tasks.loop(minutes=.1)
    async def MentionUsers(self, message):
        now = datetime.datetime.now()
        print("Mention Users Started ... ", now.strftime("%H:%M:%S"))

        today = datetime.date.today().isoformat()
        day = 0
        datesloaded = False
        standardSquats = 9999
        hardSquats = 9999

        guildFileName = str(message.guild) +'.csv'
        userNames = ""

        with open (guildFileName, 'r') as csvOut:
                fileReader = csv.reader(csvOut)
                for row in fileReader:
                    if(row[0] == 'Date'):
                        datesloaded = True
                        for item in row:
                            if item == today:
                                break
                            else:
                                day += 1

        if datesloaded:
            with open (guildFileName, 'r') as csvOut:
                fileReader = csv.reader(csvOut)
                for row in fileReader:
                    if(row[0] == 'Standard'):
                        standardSquats = row[day]
                    if(row[0] == 'Hard'):
                        hardSquats = row[day]
                    if(row[0] == 'USERS'):
                        for item in row:
                            if item == 'USERS':
                                continue
                            else:
                                userNames += '<@' + item + '> ' 
            if day > 30:
                await message.channel.send(userNames + '**Congrats! The squat challenge is Complete!** Thanks For All the Hard Work!')
                client.MentionUsers.stop()
            else:
                await message.channel.send(userNames + 'Welcome to day ' + str(day) + ' of squats! Complete **' + str(standardSquats) + '** squats for the standard challenge, or **'+ str(hardSquats)+ '** for the advanced. Good Luck!')
        else:
            await message.channel.send("**Notifications canceled, no active event in database!** Use the command '!sqautsbot schedule event' to start a 30 day course.")
            client.MentionUsers.stop()

client = CustomClient()
client.run(TOKEN)

# one awesome comment, thank me later
# Kevin's very cool comment
