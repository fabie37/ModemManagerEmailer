from mail import Mailbox
from modem import ModemDB, ModemManager
from time import sleep

# Setup
db = ModemDB()
modemManger = ModemManager()
modem = modemManger.getModems()[0]

while (True):
    print("Finding new sms messages...")
    messages = modemManger.getMessages(modem)
    for msg in messages:
        if (not db.existsMessage(msg)):
            print("Found new msg!")
            if Mailbox.sendMessage(msg):
                db.insertMessage(msg, True)

    sleep(10)
