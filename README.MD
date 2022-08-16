# Modem Manager SMS Emailer

---

- This project was for a friend who needed a way to get SMS messages and get them sent via email. The easiest way to do this is by using a cheapo modem (this was tested on Ericsson N5321) and using modem manager (which can be found on many linux based operating systems)
- This has very limited functionality as is a lite python wrapper for the Modem Manager CLI.

## Goals

- To receive sms txt messages and email to an address
- A script which can be used on a raspberry pi to indefintely run.

## Requirements

- Linux Based Machine
- SMTP Server / GMail Dev Account

## Prerequisites 

- SQL Lite 3
- Python 3
- Modem Manager (Linux) 
> sudo apt-get install sqlite3
> sudo apt-get install python3
> sudo apt-get install modemmanager

## Setup

- In order for this service to send emails, you'll need to connect it to a SMTP server. 
- To run the dummy email server use `$ sudo python -m smtpd -c DebuggingServer -n localhost:1025` and this will start a server for you which will output any outgoing messages onto a terminal.
- If you wish to use gmail you will need to edit a few constants under the directory ` mail/mailbox.py` namely:

> mailbox.py
> > METHOD = **"gmail"**
FROM = **'email@email.com'**
TO = 'email@email.com'
SERVER = 'localhost'
PORT = 1025
PASSWORD = **"yourpassword"**


- Details for seting up SMTP for your gmail account can be found here: https://www.androidauthority.com/gmail-smtp-settings-801100/

- Note: For Gmail and 2 factor auth you'll need to setup a app password, more details on link above.

- The static method `sendMessage(message)` can be updated to whatever server or library you will want to use.


## Running 

- Simply run `$ python main.py` and the program will run indefinitely.
 