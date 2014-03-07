########################################################
#### Python IRC Bot
#### Created by Courtney Cotton on 1/17/14
#### 
#######################################################

#######################################################
### Libraries
#######################################################
import socket
import string
import sys
import time
import random
from random import choice

#######################################################
### VARIABLES
#######################################################
# Some basic variables used to configure the bot        
server = "chat.freenode.net" # Server
port = 6667
botnick = "mushu" # Your bots nick
debug = False
# Debug Mode, Toggle true or false. 
# Determines connection to channel based on debug variable.
if debug == True:
  channel = '#aplacefortesting'
elif debug == False:
  channel = '#therealchanneliwant'

#######################################################
### FUNCTIONS
#######################################################

# Responds when asked information.
def commands(nick,channel,message):
  #Looks for message .fox and reads a random line from files/fox.txt to be sent.
  if message.find('.fox')!=-1:
    f = open('files/fox.txt')
    rFoxPhrase = random.choice(open('files/fox.txt').readlines())
    ircsock.send('PRIVMSG ' + channel + " :" + rFoxPhrase + "\n")
    f.close
  #Looks for message .list and prints out available commands.
  elif message.find('.list')!=-1:
    ircsock.send('PRIVMSG %s :%s: .fox | .compliment | .fortune | .quote \r\n' % (channel,nick))
  #Looks for message .compliment and reads a random line from files/compliments.txt to be sent.
  elif message.find('.compliment')!=-1:
    f = open('files/compliments.txt')
    rComList = random.choice(open('files/compliments.txt').readlines())
    ircsock.send('PRIVMSG ' + channel + " :" + rComList + "\n")
    f.close
  elif message.find('.fortune')!=-1:
    f = open('files/fortunes.txt')
    rFortune = random.choice(open('files/fortunes.txt').readlines())
    ircsock.send('PRIVMSG ' + channel + " :" + rFortune + "\n")
    f.close
  elif message.find('.quote')!=-1:
    f = open('files/quotes.txt')
    rQuotes = random.choice(open('files/quotes.txt').readlines())
    ircsock.send('PRIVMSG ' + channel + " :" + rQuotes + "\n")
    f.close

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