import datetime


def get_near_ndays(days=7):
    res = []
    today = datetime.datetime.now()
    for i in range(0, days):
        oneday = datetime.timedelta(days=i)
        day = today - oneday
        date_to = datetime.datetime(day.year, day.month, day.day)
        res.insert(0, str(date_to).split(" ")[0])
    return res


a = [1,2]
b = a[:50]