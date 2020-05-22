import datetime
import time


def get_near_ndays(days=7):
    res = []
    today = datetime.datetime.now()
    for i in range(0, days):
        oneday = datetime.timedelta(days=i)
        day = today - oneday
        date_to = datetime.datetime(day.year, day.month, day.day)
        res.insert(0, str(date_to).split(" ")[0])
    return res


def get_running_time(start_time, end_time)-> int:
    print('----------  start_time  ', start_time)
    print('------------  end_time  ', end_time)
    if start_time == "None" and end_time == "None":
        return 0
    elif start_time != "None" and end_time == "None":
        start_time_stramp = int(time.mktime(time.strptime(start_time, "%Y-%m-%d %H:%M:%S")))
        end_time_stramp = int(time.time())
        return int((end_time_stramp - start_time_stramp)/60)
    elif start_time != "None" and end_time != "None":
        start_time_stramp = int(time.mktime(time.strptime(start_time, "%Y-%m-%d %H:%M:%S")))
        end_time_stramp = int(time.mktime(time.strptime(end_time, "%Y-%m-%d %H:%M:%S")))
        return int((end_time_stramp - start_time_stramp)/60)
    else:
        return 0