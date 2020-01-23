import re
from abc import ABC, abstractmethod
from bs4 import BeautifulSoup as bs

class Parser(ABC):
    def __init__(self, data):
        self.data = data
    
    @abstractmethod
    def parse_data(self):
        pass

class NJParser(Parser):
    def __init__(self, data):
        super().__init__(data)
    
    def parse_data(self):
        nj_soup = bs(self.data, features="lxml")
        times = [nj_soup.findAll("div", {"class": "trip_color1"}), nj_soup.findAll("div", {"class": "trip_color2"})]
        ordered = []
        for i in range(len(times[0])):
            ordered.append(str(times[0][i]))
            if len(times[1]) < i:
                ordered.append(str(times[1][i]))
        sched = []
        for i in ordered:
            t = [match.group() for match in re.finditer(r'(0[1-9]|1[0-2]):[0-5][0-9]\s[AP]M', i)]
            if len(t) == 2:
                sched.append(t)
        return sched

class CTParser(Parser):
    def __init__(self, data):
        super().__init__(data)
    
    def parse_data(self):
        ct_soup = bs(self.data, features="lxml")
        raw = [x.string for x in ct_soup.findAll("td", {"class": "ctr"})]
        table = []
        for i in range(len(raw) // 5):
            table.append([raw[i*5].strip(), raw[i*5+2].strip()])
        return(table)
