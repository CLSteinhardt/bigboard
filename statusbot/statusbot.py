from __future__ import print_function
import discord, mysql.connector, re, asyncio
from pprint import pprint
from oauth2client import file, client, tools
from googleapiclient.discovery import build
from httplib2 import Http
from apiclient import errors
import settings

TOKEN = settings.token #'NTI0OTk1MzY4ODc0NjcyMTQ5.Dv1arQ.sag2SagcVd1yif8iTZ-DsE-aiTo'
SCOPES = ('https://www.googleapis.com/auth/spreadsheets','https://www.googleapis.com/auth/drive')
store = file.Storage('token.json')
creds = store.get()
if not creds or creds.invalid:
    flow = client.flow_from_clientsecrets('credentials.json', SCOPES)
    creds = tools.run_flow(flow, store)
sheet_service = build('sheets', 'v4', http=creds.authorize(Http()))
drive_service = build('drive', 'v3', http=creds.authorize(Http()))
client = discord.Client()

SHAREDFOLDER = '1EPw1snH_ENgAQUCwKS9-qMtZDHwBFnCC' #Change as needed
TAGLIST = ['stuck','backsolved','needshelp'] # Making this global so it only get changed in one place.
TOOLSBASEURL = settings.toolsbaseurl
DBHOST = settings.dbhost

@client.event
async def on_message(message):
    # we do not want the bot to reply to itself
    if message.author == client.user:
        return
    print(message.content)
    if(message.content.startswith('**<')): # Remove user hook from Titan to parse commands
        inputstr = message.content.split('>** ', 1)
        message.content = str(inputstr[1])
        print(message.content)
    
    if(message.content.startswith('**[')): # Remove user hook from Titan to parse commands
        inputstr = message.content.split(']** ', 1)
        message.content = str(inputstr[1])
        print(message.content)
        

    if message.content.startswith('!hello'):
        print('Hello called!')
        msg = 'Hello {0.author.mention}'.format(message)
        print(msg)
        await client.send_message(message.channel, msg)

    if message.content.startswith('!dbtest'):
        print('DB Test called!')
        msg = str(mydb).format(message)
        print(msg)
        await client.send_message(message.channel, msg)

    if message.content.startswith('!puzzleinfo'):
        print('Puzzle Info called!')
        mycursor = mydb.cursor()
        cmd = 'SELECT * FROM hunts_puzzle WHERE discordchannelid = %s;' % int(message.channel.id)
        try:
            mycursor.execute(cmd)
            myresult = mycursor.fetchall() # mycursor.execute(cmd)
            for x in myresult:
               print(x)           
               msg = str(x[0:2]).format(message)
               print(msg)
               await client.send_message(message.channel, msg)
            mycursor.close()
        except:
            msg = 'ERROR: Usage !puzzleinfo'
            await client.send_message(message.channel, msg)

    if message.content.startswith('!set '): #UPDATE columns in hunts_puzzle, with dictionary below in parse_col and parse_cmd.  !set_r is for rounds.
        print('Set Puzzle Info called!')
        inputstr = message.content.split(' ', 2)
        print(inputstr)
        mycursor = mydb.cursor()
        if(message.channel.name.startswith('round_')): # This is a round
            try:
                mycursor.execute('SELECT roundid FROM hunts_round WHERE discordchannelid = %s;' % int(message.channel.id))
                res = mycursor.fetchall()
                cmd = 'UPDATE hunts_round SET %s = \'%s\', last_update=now() WHERE roundid = %d;' % (parse_r_col(str(inputstr[1])), str(inputstr[2]), int(res[0][0]))
                mycursor = mydb.cursor()
                mycursor.execute(cmd)
                mycursor.execute("COMMIT;")
                mycursor.close()
                msg = 'Updated %s to %s.' % (parse_r_cmd(str(inputstr[1])), str(inputstr[2]))
                if(str(inputstr[1]) == 'name'): #Update channel name
                    namestr = 'round_' + str(re.sub('[^A-Za-z0-9]+', '', str(inputstr[2])))
                    await client.edit_channel(message.channel, name=namestr)
            except: # Error as e:
                #print(e)
                msg = 'ERROR: Usage !set ([name, active]) (value)'
            print(msg)
            await client.send_message(message.channel, msg)
        else:
            try:
                mycursor.execute('SELECT puzzid FROM hunts_puzzle WHERE discordchannelid = %s;' % int(message.channel.id))
                res = mycursor.fetchall()
                cmd = 'UPDATE hunts_puzzle SET %s = \'%s\', last_update=now() WHERE puzzid = %d;' % (parse_col(str(inputstr[1])), str(inputstr[2]), int(res[0][0]))
                mycursor = mydb.cursor()
                mycursor.execute(cmd)
                mycursor.execute("COMMIT;")
                mycursor.close()
                msg = 'Updated %s to %s.' % (parse_cmd(str(inputstr[1])), str(inputstr[2]))        
                if(str(inputstr[1]) == 'name'): #Update channel name and sheet name
                    namestr = str(re.sub('[^A-Za-z0-9]+', '', str(inputstr[2])))
                    await client.edit_channel(message.channel, name=namestr) #Update channel name
                    # And now update spreadsheet name
                    mycursor = mydb.cursor()
                    mycursor.execute('SELECT googlesheet FROM hunts_puzzle WHERE discordchannelid = %s;' % int(message.channel.id))
                    res = mycursor.fetchall()
                    spreadsheetid = res[0][0]
                    mycursor.execute("COMMIT;")                
                    mycursor.close()
                    requests = []
                    requests.append({
                        'updateSpreadsheetProperties': {
                            'properties': {
                                'title': str(inputstr[2])
                            },
                            'fields': 'title'
                        }
                    })
                    body = {
                        'requests': requests
                    }
                    sheet_service = build('sheets', 'v4', credentials=creds)
                    response = sheet_service.spreadsheets().batchUpdate(
                        spreadsheetId=spreadsheetid,
                        body=body).execute()
            except: # Error as e:
                #print(e)
                msg = 'ERROR: Usage !set ([url, name, priority, active, meta]) (value)'
            print(msg)
            await client.send_message(message.channel, msg)   
    
    if message.content.startswith('!add_p '): #Add new puzzle.  
        print('Add Puzzle called!')
        mycursor = mydb.cursor()
        inputstr = message.content.split(' ', 1) # Everything after the first command is considered part of the puzzle name
        puzzName = str(re.escape(str(inputstr[1]))) # Sanitize but otherwise keep
        chanName = str(re.sub('[^A-Za-z0-9]+', '', str(inputstr[1]))) # Strip spaces, non alphanumeric 
        try: # Create Channel and get id
            chan = await client.create_channel(message.server, chanName, type=discord.ChannelType.text)
            await asyncio.sleep(1)
            await client.move_channel(chan, 3)
        except:
            print('Failed to create %s') % (chanName)
        # NOTE: Somewhere here we have to change the group the channel lies in.
        print(chan.id)
        mycursor.execute('SELECT huntid_id FROM hunts_puzzle WHERE discordchannelid = %s;' % int(message.channel.id))
        res = mycursor.fetchall()
        huntid = int(res[0][0])               
        cmd = 'INSERT INTO hunts_puzzle (puzzname, last_update, isMeta, active, huntid_id, url, discordchannelid, priority) VALUES (\'%s\', now(), 0, 1, %d, \'\', %d, 0);' % (puzzName, huntid, int(chan.id))            
        try: # Set up the puzzle page in the database.
            mycursor = mydb.cursor()
            mycursor.execute(cmd)
            mycursor.execute("COMMIT;")
            mycursor.execute('SELECT puzzid FROM hunts_puzzle WHERE discordchannelid = %s;' % int(chan.id))
            res = mycursor.fetchall()
            mycursor.execute("COMMIT;")
            puzzid = int(res[0][0])
            topicstr = 'Puzzle ID: %d' % puzzid
            await client.edit_channel(chan, topic=topicstr) # Note: this gives us an id which can use either to build a link or to help fill out rounds.
            msg = 'Created puzzle %s' % (chanName)
        except:
           msg = 'ERROR: Usage !add_p (name)'
        await client.send_message(message.channel, msg)
        try: #Create a google sheet
            print('Sheet Creation called!')
            drive_service = build('drive', 'v3', http=creds.authorize(Http())) #Using google drive instead of sheets.
            copied_file = {'name': str(inputstr[1])}
            response = drive_service.files().copy(
                    fileId='12jxFviWNueQJH-d5HOxUujT9VV5fv8et9C1OZS3RxVo', body=copied_file).execute() #Copying from static template.
            spreadsheetid = response.get('id')
            print(response)
            print(spreadsheetid)
            msg = 'Created spreadsheet from template.'
            await client.send_message(message.channel, msg)
        except:
            msg = 'ERROR: Google sheets creation failed.'
            await client.send_message(message.channel, msg)
        if(1==1):  # Move the sheet to the shared folder.
            print('Move Sheet called!')
            folder_id = SHAREDFOLDER #Static definition above
            # Retrieve the existing parents to remove
            file = drive_service.files().get(fileId=spreadsheetid,
                                             fields='parents').execute()
            previous_parents = ",".join(file.get('parents'))
            # Move the file to the new folder
            file = drive_service.files().update(fileId=spreadsheetid,
                                                addParents=folder_id,
                                                removeParents=previous_parents,
                                                fields='id, parents').execute()
            msg = 'Created a google sheet for the puzzle.'
        if(1==0):
            msg = 'Google drive manipulation failed.'
        await client.send_message(message.channel, msg)
        try: #Put the sheet id into the database
            cmd = 'UPDATE hunts_puzzle SET googlesheet =  \'%s\' WHERE puzzid = %d;' % (spreadsheetid, puzzid)            
            mycursor.execute(cmd)
            mycursor.execute("COMMIT;")
            msg = 'Everything should be ready now.  You can now use the puzzle page on the big board.'
        except:
            msg = 'Google sheet insertion failed'
        await client.send_message(message.channel, msg)
        msg = 'You can now view your new puzzle and change settings at http://%s/puzzle/%s' % (TOOLSBASEURL, puzzid)
        await client.send_message(message.channel, msg)
        

    if message.content.startswith('!add_r '): #Add new round.  
        print('Add round called!')
        inputStr = message.content.split(' ', 1) # Everything after the first command is considered part of the round name
        roundName = str(re.escape(str(inputStr[1]))) # Sanitize but otherwise keep
        chanName = 'round_' + str(re.sub('[^A-Za-z0-9]+', '', str(inputStr[1]))) # Strip spaces, non alphanumeric 
        try: # Create Channel and get id
            chan = await client.create_channel(message.server, chanName, type=discord.ChannelType.text)
            await asyncio.sleep(1)
            await client.move_channel(chan, 3)
        except:
            print('Failed to create %s') % (chanName)
        # NOTE: Somewhere here we have to change the group the channel lies in.
        print(chan.id)        
        mycursor.execute('SELECT huntid_id FROM hunts_puzzle WHERE discordchannelid = %s;' % int(message.channel.id))
        res = mycursor.fetchall()
        huntid = int(res[0][0])  
        cmd = 'INSERT INTO hunts_round (roundname, last_update, active, huntid_id, discordchannelid) VALUES (\'%s\', now(), 1, %d, %d);' % (roundName, huntid, int(chan.id))            
        try: # Set up the puzzle page in the database.
            mycursor = mydb.cursor()
            mycursor.execute(cmd)
            mycursor.execute("COMMIT;")
            mycursor.execute('SELECT roundid FROM hunts_round WHERE discordchannelid = %s;' % int(chan.id))
            res = mycursor.fetchall()
            mycursor.execute("COMMIT;")
            roundid = int(res[0][0])
            topicstr = 'Round ID: %d (Use this ID for assigning puzzles to this round)' % roundid
            await client.edit_channel(chan, topic=topicstr) # Note: this gives us an id which can use either to build a link or to help fill out rounds.
            msg = 'Created round %s' % (chanName)
        except:
           msg = 'ERROR: Usage !add_r (name)'
        await client.send_message(message.channel, msg)

    if message.content.startswith('!link_round '): #Add to a round in hunts_puzzround.
        print('Link to Round called!')
        inputstr = message.content.split(' ', 2)
        mycursor = mydb.cursor()
        try:
            print(inputstr)
            mycursor.execute('SELECT puzzid FROM hunts_puzzle WHERE discordchannelid = %s;' % int(message.channel.id))
            res = mycursor.fetchall()
            cmd = 'DELETE FROM hunts_puzzround WHERE puzzid_id = %d AND roundid_id = %d' % (int(res[0][0]), int(inputstr[1]))        
            mycursor.execute(cmd)
            cmd = 'INSERT INTO hunts_puzzround (puzzid_id, roundid_id) VALUES (%d, %d)' % (int(res[0][0]), int(inputstr[1]))
            mycursor.execute(cmd)
            mycursor.execute("COMMIT;")
            mycursor.close()
            msg = 'Linked to round %d.' % (int(inputstr[1]))
        except: # Error as e:
            #print(e)
            msg = 'ERROR: Usage !link_round (roundid), roundid can be obtained in topic of round discord channel.'
        print(msg)
        await client.send_message(message.channel, msg)

    if message.content.startswith('!unlink_round '): #Add to a round in hunts_puzzround.
        print('Unlink from Round called!')
        inputstr = message.content.split(' ', 2)
        mycursor = mydb.cursor()
        try:
            print(inputstr)
            mycursor.execute('SELECT puzzid FROM hunts_puzzle WHERE discordchannelid = %s;' % int(message.channel.id))
            res = mycursor.fetchall()
            cmd = 'DELETE FROM hunts_puzzround WHERE puzzid_id = %d AND roundid_id = %d' % (int(res[0][0]), int(inputstr[1]))
            print(cmd)
            mycursor.execute(cmd)
            mycursor.execute("COMMIT;")
            mycursor.close()
            msg = 'Removed link to round %d.' % (int(inputstr[1]))
        except: # Error as e:
            #print(e)
            msg = 'ERROR: Usage !unlink_round (roundid), roundid can be obtained in topic of round discord channel.'
        print(msg)
        await client.send_message(message.channel, msg)

    if message.content.startswith('!remove_answer '): #Remove answer to this puzzle.
        print('Remove answer called!')
        inputstr = message.content.split(' ', 1) #Parse full remaining text in answer
        mycursor = mydb.cursor()
        try:
            print(inputstr)
            mycursor.execute('SELECT puzzid FROM hunts_puzzle WHERE discordchannelid = %s;' % int(message.channel.id))
            res = mycursor.fetchall()
            cmd = 'DELETE FROM hunts_answer WHERE puzzid_id = %d AND answer = \'%s\'' % (int(res[0][0]), str(inputstr[1]))
            mycursor.execute(cmd)
            cmd = 'SELECT COUNT(*) FROM hunts_answer WHERE puzzid_id = %d;' % (int(res[0][0]))
            mycursor.execute(cmd)  #Check whether there are still any answers left
            res = mycursor.fetchall()
            mycursor.execute("COMMIT;")
            mycursor.close()
            msg = 'Removed answer %s.' % (str(inputstr[1]))
            if (int(res[0][0]) == 0): # Move puzzle back to the unsolved puzzles channel group
                msg += '  Also set puzzle to unsolved.' # TODO: Implement this     
        except: # Error as e:
            #print(e)
            msg = 'Error: IOU one (1) error message'
        print(msg)
        await client.send_message(message.channel, msg)

    if message.content.startswith('!answer '): #Remove answer to this puzzle.
        print('Answer called!')
        inputstr = message.content.split(' ', 1) #Parse full remaining text in answer
        mycursor = mydb.cursor()
        try:
            print(inputstr)
            print(str(inputstr[1]))
            mycursor.execute('SELECT puzzid FROM hunts_puzzle WHERE discordchannelid = %s;' % int(message.channel.id))
            res = mycursor.fetchall()
            cmd = 'DELETE FROM hunts_answer WHERE puzzid_id = %d AND answer = \'%s\'' % (int(res[0][0]), str(inputstr[1])) # Avoid multiple copies
            mycursor.execute(cmd)
            cmd = 'INSERT INTO hunts_answer (puzzid_id,last_update, answer) VALUES (%d, now(), \'%s\');' % (int(res[0][0]), str(inputstr[1]))
            mycursor.execute(cmd)
            mycursor.execute("COMMIT;")
            mycursor.close()
            msg = 'Added answer %s.' % (str(inputstr[1]))
            # Now move the puzzle to the solved group (TODO: Implement this)
            msg += '  Also set puzzle to solved.'     
        except: # Error as e:
            #print(e)
            msg = 'Error: IOU one (1) error message'
        print(msg)
        await client.send_message(message.channel, msg)

    if message.content.startswith('!roundlist'):
        print('Round List called!')
        mycursor = mydb.cursor()
        cmd = 'SELECT roundid, roundname FROM hunts_round WHERE huntid_id = 1 AND active = 1'  
        try:
            print(cmd)
            mycursor.execute(cmd)
            myresult = mycursor.fetchall() 
            for x in myresult:
               print(x)           
               msg = str(x[0:2]).format(message)
               print(msg)
               await client.send_message(message.channel, msg)
            mycursor.close()
        except:
            msg = 'ERROR: Usage !roundlist'
            await client.send_message(message.channel, msg)

    if message.content.startswith('!tag '): #Remove answer to this puzzle.  Note that the space is important here.
        print('Tag called!')
        inputstr = message.content.split(' ', 1) #Parse full remaining text as tag
        if valid_tag(str(inputstr[1])): # Add the tag.
            mycursor = mydb.cursor()
            try:
                print(inputstr)
                mycursor.execute('SELECT puzzid FROM hunts_puzzle WHERE discordchannelid = %s;' % int(message.channel.id))
                res = mycursor.fetchall()
                cmd = 'DELETE FROM puzzle_tag WHERE puzzid_id = %d AND tag = \'%s\'' % (int(res[0][0]), str(inputstr[1])) #Avoid duplicates
                
                print(cmd)
                mycursor.execute(cmd)
                cmd = 'INSERT INTO puzzle_tag (puzzid_id, tag) VALUES (%d, \'%s\');' % (int(res[0][0]), str(inputstr[1]))
                print(cmd)

                mycursor.execute(cmd)
                mycursor.execute("COMMIT;")
                mycursor.close()
                msg = 'Added tag %s.' % (str(inputstr[1]))   
            except: # Error as e:
                #print(e)
                msg = 'ERROR: Usage !tag (tag value)'
            print(msg)
            await client.send_message(message.channel, msg)
        else: #Invalid tag
            msg = 'ERROR: Invalid tag.  !taglist will return a list of valid tags.'
            await client.send_message(message.channel, msg)

    if message.content.startswith('!remove_tag '): #Remove answer to this puzzle.
        print('Remove tag called!')
        inputstr = message.content.split(' ', 1) #Parse full remaining text as tag
        if valid_tag(str(inputstr[1])): # Remove the tag.
            mycursor = mydb.cursor()
            try:
                print(inputstr)
                mycursor.execute('SELECT puzzid FROM hunts_puzzle WHERE discordchannelid = %s;' % int(message.channel.id))
                res = mycursor.fetchall()
                cmd = 'DELETE FROM puzzle_tag WHERE puzzid_id = %d AND tag = \'%s\'' % (int(res[0][0]), str(inputstr[1]))
                mycursor.execute(cmd)
                mycursor.execute("COMMIT;")
                mycursor.close()
                msg = 'Removed tag %s.' % (str(inputstr[1]))   
            except: # Error as e:
                #print(e)
                msg = 'ERROR: Usage !tag (tag value)'
            print(msg)
            await client.send_message(message.channel, msg)
        else: #Invalid tag
            msg = 'ERROR: Invalid tag.  !taglist will return a list of valid tags.'
            await client.send_message(message.channel, msg)

    if message.content.startswith('!taglist'): #Return list of valid tags.
        print('Taglist called!')
        await client.send_message(message.channel, TAGLIST)


    if message.content.startswith('!help'): #Return list of valid tags.
        print('Help called!')
        msg = 'A list of commands is available at https://docs.google.com/document/d/1Ut3-qMI4dPRqRaf6HQ1efbgm3JisSzzhcrlhITRpEbw/'
        await client.send_message(message.channel, msg)
        

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

mydb = mysql.connector.connect(
  auth_plugin="mysql_native_password",
  host=DBHOST,
  user="statusbot",
  passwd="statusbot.pass",
  database="bigboard",  
)

def parse_col(str):
    switcher = {
        'url': 'url',
        'name': 'puzzname',
        'priority': 'priority',
        'active': 'active',
        'meta': 'isMeta'
        }
    return switcher.get(str, '')
                                                                     
def parse_cmd(str):
    switcher = {
        'url': 'URL',
        'name': 'puzzle name',
        'priority': 'priority',
        'active': 'active',
        'meta': 'metapuzzle'
        }
    return switcher.get(str, '(error not found)')

def parse_r_col(str): #Switcher for rounds to database editing
    switcher = {
        'name': 'roundname',
        'active': 'active',
        }
    return switcher.get(str, '')
                                                                     
def parse_r_cmd(str): #Switcher for rounds to discord output
    switcher = {
        'name': 'round name',
        'active': 'active',
        }
    return switcher.get(str, '(error not found)')



def valid_tag(str):
    if str in TAGLIST:
        return True
    else:
        return False
    
client.run(TOKEN)
