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

def unit_propagate(satVars, watching, clause_watch, assignment):
	return 

# ret bool
# true if was able to move watching for index
# false otherwise (i.e. conflict)
def setWatching(satVars, watching, clause_watch, w_index, assignment):
	# unit_propped = []
	while watching[w_index]: # if any clauses left watching this literal
		c_index, clause = watching[w_index][0] # first clause watching this literal
		moved = False
		for another in clause: # other literals in the clause
			val = another
			sign = 1 if val > 0 else 0
			ind = abs(val) - 1 
			new_w_index = 2*ind + sign
			sign = -1 if val == 0 else 1
			# if (assignment[ind] == 1):
			# 	moved = True
			# 	break
			if (not new_w_index in clause_watch[c_index] # can't be other watched val or this one
					and not assignment[ind] == sign):
				# move clause to watching something else
				watching[new_w_index].append(watching[w_index].pop(0))
				clause_watch[c_index].remove(w_index)
				clause_watch[c_index].append(new_w_index)
				moved = True # replaced!!
				break
		if not moved: # attempt unit propagation
			unit = False
			# return False
			for watched in clause_watch[c_index]:
				ind = int((watched - (watched % 2)) / 2)
				sign = 1 if watched > 0 else -1
				if not watched == w_index and assignment[ind] * sign > 0: # technically includes assignment[ind] == 0
					watching[w_index].pop(0) # TODO: should this be here?
					clause_watch[c_index].remove(w_index)
					assignment[ind] = sign
					unit = True
					break
			if not unit:
				return False
				# if len(clause_watch[c_index]) == 2 and clause_watch[c_index][0] >> 2 == clause_watch[c_index][1] >> 2:
				# 	assignment[ind] = 1
				# 	watching[w_index].pop(0)
				# else:
				# 	# print("false " + str(w_index))
				# 	# print(assignment)
				# 	return False # conflict!!
	# print("true " + str(w_index))
	# print(assignment)
	return True # if watching at w_index is empty then it's just true

def satSolve(satVars, watching, clause_watch, assignment):
	unit_propagate(satVars, watching, clause_watch, assignment)
	oldAssignment = assignment
	index = 0
	try:
		index = assignment.index(0)
	except:
		return True # all assignments satisfied
	t_ind = 2*index + 1
	f_ind = 2*index
	sat = False
	assignment[index] = -1
	if setWatching(satVars, watching, clause_watch, t_ind, assignment): # sat
		sat = satSolve(satVars, watching, clause_watch, assignment)
		# try:
		# 	next_index = assignment.index(0)
		# except:
		# 	return True # all assignments satisfied
		# sat = satSolve(satVars, watching, clause_watch, next_index, assignment)
	else:
		assignment = oldAssignment
	if not sat:
		assignment[index] = 1
		if setWatching(satVars, watching, clause_watch, f_ind, assignment):
			sat = satSolve(satVars, watching, clause_watch, assignment)
			# try:
			# 	next_index = assignment.index(0)
			# except:
			# 	return True # all assignments satisfied
			# sat = satSolve(satVars, watching, clause_watch, next_index, assignment)
		# else:
			# backtrack
	if not sat:
		assignment = oldAssignment
		assignment[index] = 0
	return sat

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
		# print(assignment)
		sat = satSolve(satVars, watching, clause_watch, assignment)
		if sat:
			print("SATISFIABLE") #+ " " + str(satCheck(formula, assignment, False)) + " " + file)
			satPrint(assignment)
			# satCheck(formula, assignment, True)
		else: 
			print("UNSATISFIABLE")

if __name__ == '__main__':
	main()