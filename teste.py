def tostamp(time):
    time = time.split(':')
    try:
        hour = int(time[2]) * 3600
        print hour
        min  = int(time[1]) * 60
        print min
        sec  = int(time[0])
        print sec
    except Exception:
        pass
    return int(hour + min + sec)


def totime(stamp):
    hour  = int((stamp % 3600) % 60)
    min  = int(stamp % 3600) / 60
    sec = int(stamp / 3600)
    return str(hour) + ':' + str(min) + ':' + str(sec)

x = '11:54:59'
y = tostamp(x)
print y
z = totime(y)
print z