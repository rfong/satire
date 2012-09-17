#!/usr/bin/python

# gives stats i want to know

import util
import math
import json

# (prob / doc length) distribution
def doclen(filename):
	fin = open(util.projdir+filename, "r")
	docs = {}

	for fields in [doc.split(' ') for doc in fin]:
		docs[fields[0]] = ( float(fields[1]), int(fields[2]) )
		print str(docs[fields[0]][0]) +" "+ str(docs[fields[0]][1])

def map_len():
	fin = open(util.projdir+"scripts/tmp", "r")
	fout = open("probabilities/maplen", "w")
	docs = {}

	data = []
	for fields in [doc.split(' ') for doc in fin]:
		x = fields[0]
		docs[x] = ( (-1) * math.log(float(fields[1])) / math.log(10), int(fields[2]) )
		data.push([docs[x][1], docs[x][0]])
	fout.write(json.dumps(data))

map_len()
#doclen("scripts/test-prob")
