from email.message import EmailMessage
import smtplib
import ssl
from modem import Message

METHOD = "dummy"  # Change this to "gmail" for gmail
FROM = 'email@email.com'
TO = 'email@email.com'
SERVER = 'localhost'
PORT = 1025
PASSWORD = "yourpassword"


class Mailbox:

    def _gmailServer(msg):
        context = ssl.create_default_context()

        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
            server.login(FROM, PASSWORD)
            server.send_message(msg)

    def _dummyServer(msg):
        s = smtplib.SMTP(SERVER, PORT)
        s.send_message(msg)
        s.quit()

    @staticmethod
    def sendMessage(message: Message):

        server = {
            "dummy": Mailbox._dummyServer,
            "gmail": Mailbox._gmailServer
        }

        try:
            msg = EmailMessage()
            msg.set_content(str(message))
            msg['Subect'] = f'Text from {message.getNumber()}'
            msg['To'] = TO
            msg['From'] = FROM
            server[METHOD](msg)
            return True
        except:
            return False
