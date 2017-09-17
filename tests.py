import utilities as ut
import time

time1 = ut.time_str()
time.sleep(0.5)
time2 = ut.time_str()

def test():
    if time1 < time2:
        print "yes"

test()