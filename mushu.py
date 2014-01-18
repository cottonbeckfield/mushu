########################################################
#### Python IRC Bot
#### Created by Courtney Cotton on 1/17/14
#### Utilized Shellium (http://wiki.shellium.org/) for 
#### support.
#######################################################

#######################################################
### Libraries
#######################################################
import socket
import string
import sys
import time
from random import choice

#######################################################
### VARIABLES
#######################################################
# Some basic variables used to configure the bot        
server = "chat.freenode.net" # Server
port = 6667
botnick = "mushu" # Your bots nick
debug = True
# Debug Mode, Toggle true or false. 
# Determines connection to channel based on debug variable.
if debug == True:
  channel = '#testinglandville'
elif debug == False:
  channel = '#forrealsieschat'

sfox = [' :Ring ding ding ding ding a ding a ding!\r\n', 
        ' :Wa-pa-pa-pa-pa-pa-pow!\r\n', 
        ' :Chacha-chacha-chacha-chow!\r\n', 
        ' :Hatee-hatee-hatee-ho!\r\n']

#######################################################
### FUNCTIONS
#######################################################

# Responds when asked information on what it does.
def commands(nick,channel,message):
   
   if message.find('.fox')!=-1:
      ircsock.send('PRIVMSG ' + channel + choice(sfox))
      #ircsock.send('PRIVMSG ' + channel + " :Ring ding ding ding ding a ding a ding!\r\n ")
   elif message.find('.list')!=-1:
      ircsock.send('PRIVMSG %s :%s: .fox (DONTUJUDGEME...)\r\n' % (channel,nick))

# Responds to server pings.
def ping(): 
  ircsock.send("PONG :pingis\n")  

# Sends messages to channel.
def sendmsg(chan , msg): 
  ircsock.send("PRIVMSG "+ chan +" :"+ msg +"\n") 

# Join a Channel
def joinchan(chan):
  ircsock.send("JOIN "+ chan +"\n")

# Responds to Users who say Hello
def hello(): # This function responds to a user that inputs "Hello Euthumeo"
  ircsock.send("PRIVMSG "+ channel +" :Hello!\n")
                  
#######################################################
### Code
#######################################################

## Connection Section
ircsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ircsock.connect((server, port)) # Here we connect to the server using the port 6667
ircsock.send("NICK "+ botnick +"\n") # here we actually assign the nick to the bot
ircsock.send('USER AffixBot AffixBot AffixBot :Affix IRC\r\n')
# Sleep is required because IRC may not be able to keep up with the
# information being sent, and will fail.
# Sleeping requires a proper response, and you're able to join channel.
time.sleep(3)
# Join Channel
joinchan(channel) 

while 1: 
  ircmsg = ircsock.recv(2048) 
  ircmsg = ircmsg.strip('\n\r') 
  if ircmsg.find(' PRIVMSG ')!=-1:
     nick=ircmsg.split('!')[0][1:]
     channel=ircmsg.split(' PRIVMSG ')[-1].split(' :')[0]
     commands(nick,channel,ircmsg)
  if ircmsg.find(":Hello "+ botnick) != -1:
    hello()

# Responds if server pings. Keeps session active.
  if ircmsg.find("PING :") != -1: 
    ping()