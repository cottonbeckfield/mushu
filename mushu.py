########################################################
#### Python IRC Bot
#### Created by Courtney Cotton on 1/17/14
#### Utilized Shellium (http://wiki.shellium.org/) for 
#### support.
#######################################################

#######################################################
### Libraries
#######################################################
import logging
import socket
import string
import sys
import time
from datetime import date
from random import choice
import compliments

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
        ' :Hatee-hatee-hatee-ho!\r\n',
        " :It's an ancient mystery. You will never know."]

comList = [' :You are a wonderful person.\r\n', 
            ' :If it was a Zombie Apocalypse and I was a Zombie, I would eat you first.\r\n', 
            ' :Hey Albert Einste--wait! Nevermind! You are far more brilliant!\r\n', 
            ' :You are brilliant.\r\n',
            ' :You smell better than a field full of flowers.',
            ' :My only regret is that I cannot be you.']

#######################################################
### FUNCTIONS
#######################################################

# Connect variable.
def connect():
    global ircsock
    ircsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    ircsock.connect((server, port))
    ircsock.send("NICK " + botnick + "\n") 
    ircsock.send('USER SherlockBot SherlockBot SherlockBot :Sherlock IRC\r\n')

# Responds when asked information on what it does.
def commands(nick,channel,message):
   
   if message.find('.fox')!=-1:
      ircsock.send('PRIVMSG ' + channel + choice(sfox))
   elif message.find('.list')!=-1:
      ircsock.send('PRIVMSG %s :%s: .fox | .compliment\r\n' % (channel,nick))
   elif message.find('.compliment')!=-1:
      ircsock.send('PRIVMSG ' + channel + choice(comList))

# Responds to server pings.
def ping(): 
  ircsock.send('PONG :pingis\n')  

# Sends messages to channel.
def sendmsg(chan , msg): 
  ircsock.send('PRIVMSG ' + chan + ' :' + msg + '\n') 

# Join a Channel
def joinchan(chan):
  ircsock.send('JOIN ' + chan + '\n')

# Responds to Users who say Hello
def hello(): 
  ircsock.send('PRIVMSG ' + channel + ' :Hello!\n')
            
#######################################################
### Code
#######################################################

## Connection Section
connect()
# Sleep is required because IRC may not be able to keep up with the
# information being sent, and will fail.
# Sleeping requires a proper response, and you're able to join channel.
time.sleep(3)
# Join Channel
joinchan(channel) 

while 1: 
  ircmsg = ircsock.recv(4096)
  if len(ircmsg) == 0:
    print "Disconnected!" # Put a logging statement here instead.
    connect() 
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