import datetime as dt 

class Scheduler:
    def __init__(self, from_times, to_times, low, high):
        self.from_times = from_times
        self.to_times = to_times
        self.low = low
        self.high = high
    
    def create_time(self, time):
        m = time.split(" ")
        t = m[0].split(":")
        t = [int(t[0]), int(t[1])]
        if m[1] == "PM" and t[0] != 12:
            t[0] += 12
        return dt.time(t[0], t[1], 0)

    def connection(self, from_time, to_time):
        diff = dt.datetime.combine(dt.date.min, to_time[0]) - dt.datetime.combine(dt.date.min, from_time[1])
        return dt.timedelta(minutes=self.high) > diff > dt.timedelta(minutes=self.low)
    
    def convert_times(self, times):
        t = []
        for i in range(len(times)):
            t.append([])
            for j in times[i]:
                t[i].append(self.create_time(j))
        return t

    def find_connections(self):
        connections = []
        f = self.convert_times(self.from_times)
        t = self.convert_times(self.to_times)
        for i in f:
            for j in t:
                if self.connection(i, j):
                    connections.append([i, j])
        return connections
    
    def print_connections(self, conn):
        # maybe edit this format letter, include time difference between stops?
        # edge case: no connections
        string = ""
        for c in conn:
            string += "STEP 1: From: " + c[0][0].strftime('%I:%M %p') + " To: " + c[0][1].strftime('%I:%M %p') + "\n"
            string += "STEP 2: From: " + c[1][0].strftime('%I:%M %p') + " To: " + c[1][1].strftime('%I:%M %p')
            string += "\n\n"
        return string
    
    def generate(self):
        return self.print_connections(self.find_connections())