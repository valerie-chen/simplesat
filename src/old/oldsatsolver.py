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
def setWatching(formula, satvars, watching, clause_watch, w_index, assignment):
	unit_propped = []
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
			for watched in clause_watch[c_index]:
				ind = int((watched - (watched % 2)) / 2)
				if not watched == w_index and assignment[ind] == 0:
					watching[w_index].pop(0) # TODO: should this be here?
					assignment[ind] = 1
					unit_propped.append(ind)
					unit = True
					break
			if not unit:
				if len(clause_watch[c_index]) == 2 and clause_watch[c_index][0] >> 2 == clause_watch[c_index][1] >> 2:
					watching[w_index].pop(0)
				else:
					# for ind in unit_propped:
					# 	assignment[ind] = 0
					return False # conflict!!
	return True # if watching at w_index is empty then it's just true

def satSolve(formula, satvars, numvars, watching, clause_watch, index, assignment):
	sat = False
	# first try assigning false
	assignment[index] = -1
	# val = satvars[index]
	f_ind = 2 * index + 1 # the atom v becomes false, move those watching
	if setWatching(formula, satvars, watching, clause_watch, f_ind, assignment):
		try:
			next_index = assignment.index(0)
		except:
			return True
		sat = satSolve(formula, satvars, numvars, watching, clause_watch, next_index, assignment) #count+1, assignment)
	# else:
	if not sat:
		# backtrack
		# for c_ind, clause in watching[f_ind]:
		# 	for a_ind in clause_watch[a_ind]
		# then if failed try assigning true
		assignment[index] = 1
		t_ind = 2 * index # the atom !v becomes false, move those watching
		if setWatching(formula, satvars, watching, clause_watch, t_ind, assignment):
			try:
				next_index = assignment.index(0)
			except:
				return True
			sat = satSolve(formula, satvars, numvars, watching, clause_watch, next_index, assignment) #count+1, assignment)

	if not sat:
		assignment[index] = 0 # backtrack
		# for c_ind, clause in watching[f_ind]:
	return sat

def main():
	for file in sys.argv[1:]:
		f = open(file, "r")
		contents = f.read()
		f.close()
		formula, numVars, numClauses = formatInput(contents)
		satVars = getVars(formula) # [1, 2, ... n]
		watching, clause_watch = getWatching(formula, satVars, numVars, numClauses)
		# watching = watch_ret[0] # indexed by 2(n-1)[+1] value, contains clauses 
		# clause_watch = watch_ret[1] # indexed by clause index, contains tuples (ind, ind2) of watched literals by 2(n-1)[+1] value
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
		sat = satSolve(formula, satVars, numVars, watching, clause_watch, 0, assignment)
		if sat: # and satCheck(formula, assignment, False):
			print("SATISFIABLE")
			# satPrint(assignment)
			# satCheck(formula, assignment, True)
		else: 
			print("UNSATISFIABLE")

if __name__ == '__main__':
	main()