#!/usr/bin/python

import sys
import fileinput
import re

from getters import getWatching
from getters import getVars
from getters import formatInput

from debug import satCheck
from debug import satPrint

# 0 = undefined, -1 = false, 1 = true

# ret bool
# true if was able to move watching for index
# false otherwise (i.e. conflict)
def setWatching(satVars, watching, clause_watch, w_index, assignment):
	i = 0
	while i < len(watching[w_index]):
	# for clause in watching[w_index]:
		c_index, clause = watching[w_index][i]
		foundTrue = False
		lastUnassigned = -1
		notAssigned = 0
		for literal in clause:
			assn = assignment[literal >> 2]
			if assn * literal > 0: # true
				foundTrue = True
				break
			elif assn == 0:
				notAssigned += 1
				lastUnassigned = assn
		if foundTrue:
			# print("found true")
			i += 1
			continue
		elif notAssigned == 1:
			# print("one unassigned")
			assignment[literal >> 2] = 1
			try:
				next_index = assignment.index(0)
			except:
				return True # all assignments satisfied
			return satSolve(satVars, watching, clause_watch, next_index, assignment)
		elif notAssigned == 0:
			# print("none assigned")
			return False
		else: # swap
			# print("move watched")
			# don't need to modify i in this case
			watching[lastUnassigned].append(watching[w_index].pop(0))
			print(clause_watch[c_index])
			print("TRY REMOVE: " + str(w_index))
			clause_watch[c_index].remove(w_index)
			clause_watch[c_index].append(lastUnassigned)
	try:
		next_index = assignment.index(0)
	except:
		return True # all assignments satisfied
	return satSolve(satVars, watching, clause_watch, next_index, assignment)

def satSolve(satVars, watching, clause_watch, index, assignment):
	t_ind = 2*index + 1
	f_ind = 2*index
	assignment[index] = -1
	if setWatching(satVars, watching, clause_watch, t_ind, assignment): # sat
		return True
		# try:
		# 	next_index = assignment.index(0)
		# except:
		# 	return True # all assignments satisfied
		# sat = satSolve(satVars, watching, clause_watch, next_index, assignment)
	# else:
		# backtrack
	assignment[index] = 1
	if setWatching(satVars, watching, clause_watch, f_ind, assignment):
		return True
			# try:
			# 	next_index = assignment.index(0)
			# except:
			# 	return True # all assignments satisfied
			# sat = satSolve(satVars, watching, clause_watch, next_index, assignment)
		# else:
			# backtrack
	assignment[index] = 0
	return False

def main():
	for file in sys.argv[1:]:
		f = open(file, "r")
		contents = f.read()
		f.close()
		formula, numVars, numClauses = formatInput(contents)
		satVars = getVars(formula) # [1, 2, ... n]
		watch_ret = getWatching(formula, satVars, numVars, numClauses)
		watching = watch_ret[0] # indexed by 2(n-1)[+1] value, contains clauses 
		clause_watch = watch_ret[1] # indexed by clause index, contains tuples (ind, ind2) of watched literals by 2(n-1)[+1] value
																# i.e. indexes watching
		assignment = [0 for _ in satVars] # indexed by val-1, contains -1/0/1 truth value
		# print(satVars)
		# print(satatoms)
		# print(formula)
		# print(watching)
		# print(clause_watch)
		# for w in watching:
		# 	for c in w:
		# 		print(c)
		# 		print()
		# 	print("- - - - - - - - - - ")
		#print(assignment)
		sat = satSolve(satVars, watching, clause_watch, 0, assignment)
		if sat:
			print("SATISFIABLE" + str(satCheck(formula, assignment, False)))
			# satPrint(assignment)
			# satCheck(formula, assignment, True)
		else: 
			print("UNSATISFIABLE")

if __name__ == '__main__':
	main()