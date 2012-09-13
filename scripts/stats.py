#!/usr/bin/python

# gives stats i want to know

import util
import math

# (prob / doc length) distribution
def doclen(filename):
	fin = open(util.projdir+filename, "r")
	docs = {}

	for fields in [doc.split(' ') for doc in fin]:
		docs[fields[0]] = ( float(fields[1]), int(fields[2]) )
		print str(docs[fields[0]][0]) +" "+ str(docs[fields[0]][1])

def map_len():
	fin = open(util.projdir+"scripts/tmp", "r")
	fout = open("maplen", "w")
	docs = {}

	fout.write("{ ")
	for fields in [doc.split(' ') for doc in fin]:
		x = fields[0]
		docs[x] = ( (-1) * math.log(float(fields[1])) / math.log(10), int(fields[2]) )
		fout.write("{"+str(docs[x][1])+","+str(docs[x][0])+"},")
	fout.write(" }")

map_len()
#doclen("scripts/test-prob")
