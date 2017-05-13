#!/usr/bin/python

from progress.bar import IncrementalBar as Bar

# Progress Bar
p = Bar(max=100)
p.start()
p.message = "Looking for device config path".encode('utf-8')

for x in range(1,100):
    p.next()





