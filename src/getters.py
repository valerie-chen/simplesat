#!/usr/bin/python

import sys
import fileinput
import re

def getWatching(formula, satVars, numVars, numClauses):
	watching = [[] for _ in range(2*numVars)]
	clause_watch = [[] for _ in range(numClauses)]
	for i, clause in enumerate(formula):
		# first watched literal
		val = clause[0]#clause[0][0]
		sign = 1 if val > 0 else 0
		ind = 2 * (abs(val)-1) + sign
		watching[ind].append((i, clause))
		clause_watch[i].append(ind)
		# second watched literal
		if len(clause) > 1:
			val = clause[1]#clause[1][0]
			sign = 1 if val > 0 else 0
			ind = 2 * (abs(val)-1) + sign
			watching[ind].append((i, clause))
			clause_watch[i].append(ind)
	return (watching, clause_watch)

def getVars(formula):
	satvars = []
	for clause in formula:
		for var in clause:
			if var < 0:
				var_t = -1 * var
			else:
				var_t = var
			if var_t not in satvars:
				satvars.append(var_t)
	return sorted(satvars)

def formatInput(contents):
	formatted = []
	lines = contents.splitlines()
	while not lines[0].startswith('p cnf'):
		lines = lines[1:]
	numVars = int(lines[0].split()[2])
	numClauses = int(lines[0].split()[3])
	for line in lines[1:]:
		clause = []
		split = line.split()
		for val in split:
			#math math
			v_int = int(val)
			if v_int is not 0:
				clause.append(v_int) #clause.append((v_int, 0))
		formatted.append(clause)
	return (formatted, numVars, numClauses)