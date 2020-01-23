from Parser import NJParser, CTParser
from Scraper import Scraper
from Scheduler import Scheduler
from Emailer import Emailer
import argparse
import datetime
import sys

class Main:
    def __init__(self, args):
        self.from_ct = args.ct
        self.date = args.date
        self.time = args.time
        self.low = args.low
        self.high = args.high
        self.password = args.password
        self.file = args.file
        self.email = args.email

    def main(self):
        scrape = Scraper(self.from_ct, self.date, self.time)
        data = scrape.fetch_full()
        nj = NJParser(data[0]).parse_data()
        ct = CTParser(data[1]).parse_data()
        if self.from_ct:
            schedule = Scheduler(ct, nj, self.low, self.high).generate()
        else:
            schedule = Scheduler(nj, ct, self.low, self.high).generate()
        message = "Train schedules for " + self.date.strftime('%Y-%m-%d')
        Emailer(self.password, self.email, self.file).send_email(message + ":\n" + schedule, message)

def valid_date_type(arg_date_str):
    """custom argparse *date* type for user dates values given from the command line"""
    try:
        return datetime.datetime.strptime(arg_date_str, "%Y-%m-%d").date()
    except ValueError:
        msg = "Given Date ({0}) not valid! Expected format, YYYY-MM-DD!".format(arg_date_str)
        raise argparse.ArgumentTypeError(msg)
        
def valid_time_type(arg_datetime_str):
    """custom argparse type for user datetime values given from the command line"""
    try:
        return datetime.datetime.strptime(arg_datetime_str, "%H:%M").time()
    except ValueError:
        msg = "Given Datetime ({0}) not valid! Expected format, 'HH:mm'!".format(arg_datetime_str)
        raise argparse.ArgumentTypeError(msg)        

def parse_args():
    # TODO: verify that the email arg is an email format
    parser = argparse.ArgumentParser()
    parser.add_argument("password", type=str, help="")
    parser.add_argument("email", type=str, help="")
    parser.add_argument("--file", nargs='?', default=False, const=True, help="")
    parser.add_argument('--ct', nargs='?', default=False, const=True)
    parser.add_argument("--date", type=valid_date_type, default=datetime.datetime.today().strftime('%Y-%m-%d'), help="")
    parser.add_argument("--time", type=valid_time_type, default=datetime.datetime.now().strftime('%H:%M'), help="")
    parser.add_argument("--low", type=int, default=20, help="")
    parser.add_argument("--high", type=int, default=60, help="")
    args = parser.parse_args()
    print(args)
    return args

m = Main(parse_args())
m.main()