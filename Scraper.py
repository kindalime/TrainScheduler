import requests
import datetime

class Scraper:
    def __init__(self, from_ct, date, time):
        def combine_times(date, time):
            """
            if date:
                d = date.split("/")
                d = datetime.date(d[2], d[0], d[1])
            else:
                d = datetime.date.today()
            
            if time:
                t = time.split(":")
                t = datetime.time(t[0], t[1], 0)
            else:
                t = datetime.time.now()
            """
            return datetime.datetime.combine(d, t)
            
        def create_data(d, t):
            d = datetime.datetime.combine(d, t) + datetime.timedelta(minutes=150)
            if from_ct:
                date = d.strftime('%m/%d/%Y')
                ct_time = d.strftime('%I:%M')
                ct_ampm = d.strftime('%p')

                return dict(nj_orig = "105_BNTN_New+York+Penn+Station",
                    nj_dest = "92_MNE_Morristown",
                    ct_orig = "NEW+HAVEN",
                    ct_orig_id = 149,
                    ct_dest = "Grand+Central+Terminal",
                    ct_dest_id = 1,
                    ct_date = date,
                    ct_time = ct_time,
                    ct_ampm = ct_ampm,
                    nj_date = date)
            else:
                nj_date = d.strftime('%m/%d/%Y')
                d = d + datetime.timedelta(minutes=90)
                ct_date = d.strftime('%m/%d/%Y')
                ct_time = d.strftime('%I:%M')
                ct_ampm = d.strftime('%p')

                return dict(nj_orig = "92_MNE_Morristown",
                    nj_dest = "105_BNTN_New+York+Penn+Station",
                    ct_orig = "Grand+Central+Terminal",
                    ct_orig_id = 1,
                    ct_dest = "NEW+HAVEN",
                    ct_dest_id = 149,
                    ct_date = ct_date,
                    ct_time = ct_time,
                    ct_ampm = ct_ampm,
                    nj_date = nj_date)
        data = create_data(date, time)

        self.nj_payload = {
            "selOrigin": data["nj_orig"],
            "selDestination": data["nj_dest"],
            "txtDate": data["nj_date"],
        }
        self.ct_payload = {
            "orig_station": data["ct_orig_id"],
            "dest_station": data["ct_dest_id"],
            "orig_station_name": data["ct_orig"],
            "dest_station_name": data["ct_dest"],
            "orig_id": data["ct_orig_id"],
            "dest_id": data["ct_dest_id"],
            "Filter_id": 1,
            "traveldate": date,
            "Time_id": data["ct_time"],
            "SelAMPM1": data["ct_ampm"],
            "cmdschedule": "see+schedule",
        }
    
    def fetch_nj(self):
        with requests.session() as nj:
            act = nj.post("https://m.njtransit.com/mo/mo_servlet.srv?hdnPageAction=TrainSchedulesFrom", data=self.nj_payload)
        return act.content


    def fetch_ct(self):
        with requests.session() as ct:
            resp = ct.post("http://as0.mta.info/mnr/schedules/sched_results.cfm?n=y", data=self.ct_payload)
        return resp.content

    def fetch_full(self):
        return(self.fetch_nj(), self.fetch_ct())
