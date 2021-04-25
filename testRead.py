import os

f=open("test.txt", "r")
contents = f.read()
scores = []
for score in contents.split(','):
    scores += [int(score)]
if

f=open("test.txt", "w")
f.write('1,0,0')

