import time

A = [0, 0, 0, 10]

summary = A[3] + (A[2] * 60) + (A[1] * 60 * 60) + (A[0] * 24 * 60 * 60)

while A != [0, 0, 0, 0]:
    if not summary:
        summary = 31*24*60*60

    summary -= 1

    d = summary // (60*60*24)
    h = (summary - d*(60*60*24)) // (60 * 60)
    m = (summary - (d*86400 + h * (60*60))) // 60
    s = (summary - (d*86400 + h * (60*60) + m*60))

    time.sleep(1)
