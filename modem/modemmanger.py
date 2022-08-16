from re import sub
import subprocess
import os
import re

from attr import attr


class Cli:
    @staticmethod
    def execute(commands):
        process = subprocess.Popen(
            commands, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()

        if (stderr):
            raise Exception(stderr)
        return stdout


class ModemManagerObject:
    def __init__(self, id, path):
        self.id = id
        self.path = path

    def getID(self):
        return self.id

    def getPath(self):
        return self.path


"""
    Modem :: Class
    Used in Modem Manager for any action
"""


class Modem(ModemManagerObject):
    def __init__(self, id, path):
        super().__init__(id, path)


"""
    Message :: Class
    Used to represent messages
"""


class Message(ModemManagerObject):
    def __init__(self, id, path, type):
        super().__init__(id, path)
        self.type = type
        raw = self.__getRawContent()
        self.data = self.__parseRawContent(raw)

    def __str__(self):
        return f"""
            Phone: {self.getNumber()} \n 
            Timestamp: {self.getTimestamp()} \n
            Text: {self.getText()} \n
        """

    def getData(self):
        return self.data

    def getType(self):
        return self.type

    def getText(self):
        try:
            return self.data["Content"]["text"]
        except:
            return None

    def getNumber(self):
        try:
            return self.data["Content"]["number"]
        except:
            None

    def getTimestamp(self):
        try:
            return self.data["Content"]["timestamp"]
        except:
            return None

    def __getRawContent(self):
        rawString = Cli.execute(["mmcli", "-s", self.id])
        return rawString.decode()

    def __parseRawContent(self, raw):
        dashLinePattern = re.compile("^(?:\s*)(\-+)$")
        categoryPattern = re.compile(
            "^(?:\s*)(\w+)(?:\s*\|\s*)(\w+)(?:\: )(.*)$")
        attributePattern = re.compile("^(?:\s*\|\s*)(\w+)(?:\: )(.*)$")

        data = {}
        currentCategory = ""
        lines = raw.split("\n")
        for line in lines:
            if re.match(dashLinePattern, line):
                continue
            elif match := re.match(categoryPattern, line):
                category = match.group(1)
                attribute = match.group(2)
                value = match.group(3)
                data[category] = {attribute: value}
                currentCategory = category
            elif match := re.match(attributePattern, line):
                attribute = match.group(1)
                value = match.group(2)
                data[currentCategory][attribute] = value

        return data


class ModemManager:

    """
        listModems: returns [Modem]
        Allows you to use select modem to use
    """

    def getModems(self):
        modemString = Cli.execute(["mmcli", "-L"])
        modemString = modemString.decode()
        modemLines = modemString.split("\n")
        modems = []
        for line in modemLines:
            pattern = re.compile("(?:\s*)(\/.*\/(\d+))(?:\s.*)")
            if data := re.match(pattern, line):
                path = data.group(1)
                id = data.group(2)
                modems.append(Modem(id, path))
        return modems

    def getMessages(self, modem):
        messages = []
        if (isinstance(modem, Modem)):
            messageString = Cli.execute(
                ["mmcli", "-m", modem.getID(), "--messaging-list-sms"])
            messageString = messageString.decode()
            messageLines = messageString.split("\n")
            messages = []
            for line in messageLines:
                pattern = re.compile("(?:\s*)(\/.*\/(\d+)) \((.*)\)")
                if data := re.match(pattern, line):
                    path = data.group(1)
                    id = data.group(2)
                    type = data.group(3)
                    messages.append(Message(id, path, type))
        return messages
