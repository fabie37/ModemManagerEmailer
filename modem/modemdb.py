import sqlite3
from os.path import exists
from modem.modemmanger import Message
from modem.modemmanger import ModemManager
from datetime import datetime

DB_FILE = 'sms.sqlite'


class ModemDB:

    def __init__(self):
        self.__createDB()

    def __createDB(self):
        if exists(DB_FILE):
            self.con = sqlite3.connect(DB_FILE)
            self.cursor = self.con.cursor()
            return
        with open(DB_FILE, 'x') as f:
            pass

        self.con = sqlite3.connect(DB_FILE)
        self.cursor = self.con.cursor()

        # Create table
        self.cursor.execute('''
                CREATE TABLE messages
                (id INTEGER NOT NULL PRIMARY KEY, number TEXT, message TEXT, timestamp DATETIME, type TEXT, mailed BOOL)
        ''')

        self.con.commit()

    def close(self):
        self.con.close()
        self.cursor = None

    def insertMessage(self, message, mailed=False):
        if (isinstance(message, Message)):
            if self.existsMessage(message):
                return True

            id = int(message.getID())
            type = message.getType()
            number = message.getNumber()
            timestamp = message.getTimestamp()
            timestamp = datetime.fromisoformat(timestamp)
            message = message.getText()

            self.cursor.execute(f'''
                    INSERT INTO messages VALUES ({id},"{number}","{message}","{timestamp.__str__()}","{type}",{mailed})
            ''')

            self.con.commit()

            return True
        return False

    def existsMessage(self, message):
        if (isinstance(message, Message)):
            id = int(message.getID())

            returnedData = self.cursor.execute(f'''
                SELECT * FROM messages WHERE id={id}
            ''').fetchone()
            if returnedData:
                return True
        return False
