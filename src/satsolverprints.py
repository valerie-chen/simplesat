#!/usr/bin/python

import sys
import fileinput
import re

# 0 = undefined, -1 = false, 1 = true

def satCheck(formula, assignment):
	for clause in formula:
		found = False
		for atom in clause:
			ind = abs(atom) - 1
			if assignment[ind]*atom > 0:
				found = True
				break
		if not found:
			print("DIDN'T WORK!")
			print(clause)
			return

# remember the off by 1!
def satPrint(assignment):
	lst = []
	for ind, a in enumerate(assignment):
		if a == 1:
			lst.append(str(ind+1))
		else: # a == -1
			lst.append(str(-1*(ind+1)))
	print(" ".join(lst))

# ret bool
# true if was able to move watching for index
# false otherwise (i.e. conflict)
def setWatching(formula, satvars, watching, clause_watch, w_index, assignment):
	while watching[w_index]: # if any clauses left watching this literal
		c_index, clause = watching[w_index][0] # first clause watching this literal
		moved = False
		for another in clause: # other literals in the clause
			val = another
			sign = 1 if val > 0 else 0
			ind = abs(val) - 1 
			new_w_index = 2*ind + sign
			sign = -1 if val == 0 else 1
			if (not new_w_index in clause_watch[c_index] # can't be other watched val
					# and not new_w_index == w_index # make sure it's not the same val
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
					# TODO: more to do here?
					watching[w_index].pop(0) # TODO: should this be here?
					assignment[ind] = 1
					unit = True
					print("UNIT:")
					print(assignment)
					break
			if not unit:
				if len(clause_watch[c_index]) == 2 and clause_watch[c_index][0] >> 2 == clause_watch[c_index][1] >> 2:
					watching[w_index].pop(0)
					return True
				print("FALSE: " + str(w_index))
				print(assignment)
				print(clause_watch[c_index])
				print()
				return False # conflict!!
	print("TRUE: " + str(w_index))
	print()
	# print(assignment)
	return True # if watching at w_index is empty then it's just true

def satSolve(formula, satvars, numvars, watching, clause_watch, index, assignment):
	# if index == numvars:
	# 	return True
	if 0 not in assignment:
		return True
	# TODO: skip this assignment if already assigned
	#if not assignment[index] == 0:
	sat = False
	# first try assigning false
	assignment[index] = -1
	val = satvars[index]
	f_ind = 2 * (val-1) + 1 # the atom v becomes false, move those watching
	if setWatching(formula, satvars, watching, clause_watch, f_ind, assignment):
		try:
			next_index = assignment.index(0)
		except:
			return True
		sat = satSolve(formula, satvars, numvars, watching, clause_watch, next_index, assignment) #count+1, assignment)
	# else:
	if not sat:
		# then if failed try assigning true
		assignment[index] = 1
		t_ind = 2 * (val-1) # the atom !v becomes false, move those watching
		if setWatching(formula, satvars, watching, clause_watch, t_ind, assignment):
			try:
				next_index = assignment.index(0)
			except:
				return True
			sat = satSolve(formula, satvars, numvars, watching, clause_watch, next_index, assignment) #count+1, assignment)

	if not sat:
		assignment[index] = 0 # backtrack
	return sat

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
		# add to clause_watch
	return (watching, clause_watch)

def getVars(formula):
	satvars = []
	for clause in formula:
		for var in clause: # for tup in clause:
			#var = tup[0]
			if var < 0:
				var_t = -1 * var
			else:
				var_t = var
			if var_t not in satvars:
				satvars.append(var_t)
	return sorted(satvars)

# def getAtoms(satvars):
# 	negs = [v * -1 for v in satvars]
# 	return negs + satvars

def formatInput(contents):
	formatted = []
	lines = contents.splitlines()
	while not lines[0].startswith('p cnf'):
		lines = lines[1:]
	numVars = int(lines[0].split()[2])
	numClauses = int(lines[0].split()[3])
	#print("numVars: " + numVars)
	#print("numClauses: " + numClauses)
	for line in lines[1:]:
		clause = []
		split = line.split()
		for val in split:
			#math math
			v_int = int(val)
			if v_int is not 0:
				clause.append(v_int) #clause.append((v_int, 0))
		formatted.append(clause)
	# print(formatted)
	return (formatted, numVars, numClauses)

def main():
	for file in sys.argv[1:]:
		f = open(file, "r")
		contents = f.read()
		f.close()
		formula, numVars, numClauses = formatInput(contents)
		# formula = ret[0]
		# numVars = ret[1]
		# numClauses = ret[2]
		satVars = getVars(formula) # [1, 2, ... n]
		# satatoms = getAtoms(satvars)
		watch_ret = getWatching(formula, satVars, numVars, numClauses)
		watching = watch_ret[0] # indexed by 2(n-1)[+1] value, contains clauses 
		clause_watch = watch_ret[1] # indexed by clause index, contains tuples (ind, ind2) of watched literals by 2(n-1)[+1] value
																# i.e. indexes watching
		assignment = [0 for _ in satVars] # indexed by val-1, contains -1/0/1 truth value
		# print(satvars)
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
		#print(str(sat))
		if sat:
			print("SATISFIABLE")
			satPrint(assignment)
			satCheck(formula, assignment)
		else: 
			print("UNSATISFIABLE")

if __name__ == '__main__':
	main()