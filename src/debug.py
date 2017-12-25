#!/usr/bin/python

import sys
import fileinput
import re

def satCheck(formula, assignment, do_print):
	for clause in formula:
		found = False
		for atom in clause:
			ind = abs(atom) - 1
			if assignment[ind]*atom > 0:
				found = True
				break
		if not found:
			if do_print:
				print("DIDN'T WORK!")
				print(clause)
			return False
	return True

# remember the off by 1!
def satPrint(assignment):
	lst = []
	for ind, a in enumerate(assignment):
		if a == 1:
			lst.append(str(ind+1))
		else: # a == -1
			lst.append(str(-1*(ind+1)))
	print(" ".join(lst))