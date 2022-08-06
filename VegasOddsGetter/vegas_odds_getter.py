from pysbr import *
from datetime import datetime

def get_odds():
    nhl = NHL()
    sb = Sportsbook()
    start = datetime.strptime('2021-11-25', '%Y-%m-%d')
    end = datetime.strptime('2021-12-05', '%Y-%m-%d')
    e = EventsByDateRange(nhl.league_id, start, end)
    event_list = e.list()
    cl = CurrentLines(e.ids(), nhl.market_ids(['moneyline']), sb.ids(['bovada']))
    cl_list = cl.list()
    print(cl_list[0])
