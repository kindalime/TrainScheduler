import smtplib, ssl

class Emailer:
    def __init__(self, password, receiver, file=True, port=465):
        self.port = port
        self.receiver = receiver
        def get_password(password, file):
            if file:
                with open(password, "r") as f:
                    return f.readline()
            else:
                return password
        self.password = get_password(password, file)

    def send_email(self, text, subject="Train Schedules"):
        context = ssl.create_default_context()

        with smtplib.SMTP_SSL("smtp.gmail.com", self.port, context=context) as server:
            server.login("danielkim0test@gmail.com", self.password)
            sender_email = "danielkim0test@gmail.com"
            receiver_email = self.receiver
            message = "Subject:" + subject + "\n\n" + text
            server.sendmail(sender_email, receiver_email, message)