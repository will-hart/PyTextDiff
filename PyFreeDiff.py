'''
A simple diff by breaking into sentences and comparing adjacent sentences.
Available under the ultra permissive MIT license

Version 0.2 - 29-08-2012
		- performance updates including hashing of strings before diffing
		- implementation of patching and removal of patches
Version 0.1 - 28-08-2012
		- initial release, splitting of sentences and diff object/html diff generation


The MIT License (MIT)
Copyright (c) 2012, William Hart

Permission is hereby granted, free of charge, to any person obtaining a copy of
this software and associated documentation files (the "Software"), to deal in
the Software without restriction, including without limitation the rights to use,
copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the
Software, and to permit persons to whom the Software is furnished to do so,
subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER
IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
'''

import re

'''
Constants for determining the status of a diff_result
'''
DELETED = -1
UNCHANGED = 0
INSERTED = 1
NOT_SET = -99


'''
Constant for a standard sentence split
'''
STANDARD_REGEX = '[.!?]'


'''
A container for diff results
'''
class DiffResult():
	start_index = 0
	length = 0
	line = None
	operation = 0

	def __init__(self, start_index, length, line, operation):
		self.start_index = start_index
		self.length = length
		self.line = line
		self.operation = operation


'''
A class for performing diff and patch operations on strings
'''
class PyFreeDiff(object):
	
	def __init__(self):
		return
	
	'''
	Performs a basic diff on two strings, splitting by sentence and returning
	the diffs between original and revised
	'''
	def diff(self, original, revised):
		hashTable = {}
		hashed_original = []
		hashed_revised = []
		unhashed_diffs = []
		counter = 0
		
		# build a hash map for each string
		original_arr = self._split_with_maintain(original)
		new_arr = self._split_with_maintain(revised)
		
		counter, hashTable, hashed_original = self._build_hash(counter, hashTable, original_arr)
		counter, hashTable, hashed_revised = self._build_hash(counter, hashTable, new_arr)
		
		# generate diffs
		hashed_diffs = self._generate_diff(hashed_original, hashed_revised, 0)
		
		# unmap diff hashes - at this point lines are lists of hashTable numbers
		reverseHashTable = dict([(v,k) for (k,v) in hashTable.items()])
		
		for d in hashed_diffs:
			line = self._unhash(d.line, reverseHashTable)
			unhashed_diffs.append(DiffResult(d.start_index, d.length, line, d.operation))
		
		return unhashed_diffs
		
	'''
	Generates a 3 way diff between three related documents, allowing rebasing of 'mine'
	based on changes from 'theirs'
	'''
	def diff3(self, mine, original, theirs):
		hashTable = {}
		hashed_mine = []
		hashed_original = []
		hashed_theirs = []
		counter = 0

		# build a hash map for each string
		mine_arr = self._split_with_maintain(mine)
		original_arr = self._split_with_maintain(original)
		their_arr = self._split_with_maintain(theirs)

		counter, hashTable, hashed_mine = self._build_hash(counter, hashTable, mine_arr)
		counter, hashTable, hashed_original = self._build_hash(counter, hashTable, original_arr)
		counter, hashTable, hashed_theirs = self._build_hash(counter, hashTable, their_arr)

		# get patches between theirs and original
		their_updates = self.diff(hashed_original, hashed_theirs)
		your_updates = self.diff(hashed_original, hashed_mine)
		
		# now compare their updates to mine and see if there are any overlaps
		
		pass


	'''
	Splits a string based on a list of chars and returns the list.
	For instance, when calling split_with_maintain(str, '[.!?]')
		"This is a test.  It should split awesomely."
	Becomes:
		["This is a test.", "  ", "It should split awesomely"]
	'''
	def _split_with_maintain(self, value, treat_trailing_spaces_as_sentence = True, split_char_regex = STANDARD_REGEX):
		result = []
		check = value
		
		# compile regex
		rx = re.compile(split_char_regex)
		
		# traverse the string
		while len(check) > 0:
			found  = rx.search(check)
			if found == None:
				result.append(check)
				break
			
			idx = found.start() + 1
			result.append(check[:idx])
			check = check[idx:]
			
			# group the trailing spaces if requested
			if treat_trailing_spaces_as_sentence:
				space_idx = 0
				while True:
					if space_idx >= len(check):
						break
					if check[space_idx] != " ":
						break
					space_idx += 1
				
				if space_idx != 0:
					result.append(' ' * space_idx)
			
				check = check[space_idx:]
			
			# if treat_trailing_spaces_as_sentence is true we parse until we find a non-space character
			
		return result


	'''
	Builds a hash map from a given set of items, appending to anything already in existing
	
	Returns the hashmap and the translated hash items
	'''
	def _build_hash(self, start_counter, existing, items):
		translated_hash = []
		for s in items:
			if s not in existing:
				existing[s] = start_counter
				idx = start_counter
				start_counter += 1
			else:
				idx = existing[s]
			translated_hash.append(idx)

		return start_counter, existing, translated_hash


	'''
	Takes a list of diffs and a hashtable and converts the diffs back into strings
	'''
	def _unhash(self, diffs, hashtable):
		return ''.join(hashtable[i] for i in diffs)


	'''
	Generate a 'dumb' diff between two strings.
	'''
	def _generate_diff(self, original, revised, start_idx):
				
		# check if we have empty lists - means we are at the bottom of recursion
		if len(original) == 0 and len(revised) == 0:
			return None
		
		# check if the strings are the same
		if original == revised: #",".join( map( str, original ) ) == ",".join( map( str, revised ) ):
			return [DiffResult(start_idx, len(revised), revised, UNCHANGED)]
		
		# speed up - check for original being empty (complete insertion)
		if len(original) == 0:
			return [DiffResult(start_idx, len(revised), revised, INSERTED)]
		
		# speed up - check for revised being empty (complete deletion)
		if len(revised) == 0:
			return [DiffResult(start_idx, len(original), original, DELETED)]
		
		# set up some variables
		result = []
		matrix = [[0 for x in range(len(revised))] for x in range(len(original))] 
		old_max = 0
		new_max = 0
		max_len = 0
		
		for old_idx, old_val in enumerate(original):
			
			for new_idx, new_val in enumerate(revised):
				
				if new_val == old_val:
					# check previous indices and see if they matched
					if old_idx > 0 and new_idx > 0:
						matrix[old_idx][new_idx] = matrix[old_idx-1][new_idx-1] + 1
					else:
						matrix[old_idx][new_idx] = 1
					
					if matrix[old_idx][new_idx] > max_len:
						max_len = matrix[old_idx][new_idx]
						old_max = old_idx + 1 - max_len
						new_max = new_idx + 1 - max_len
		
		if max_len == 0:
			result.append(DiffResult(start_idx, len(original), original, DELETED))
			result.append(DiffResult(start_idx, len(revised), revised, INSERTED))
			return result

		others = self._generate_diff(original[0:old_max], revised[0:new_max], start_idx)
		if others is not None:
			result += others
		
		o = DiffResult(start_idx + new_max, max_len, revised[new_max : new_max + max_len], UNCHANGED)  
		result.append(o) #TODO - is this unchanged or inserted??
		
		others = self._generate_diff(original[old_max + max_len :], revised[new_max + max_len :], old_max + start_idx)
		if others is not None:
			result += others
	
		return result

		
	'''
	Generate basic HTML for a set of diffs
	'''
	def generate_html_diffs(self, diffs):
		if diffs == None:
			return ""

		start = ""
		end = ""
		result = ""
		
		for diff in diffs:
			op = diff.operation
			if op == INSERTED:
				start = "<ins>"
				end = "</ins>"
			elif op == DELETED:
				start = "<del>"
				end = "</del>"
			else:
				start = ""
				end = ""
			result += start + diff.line + end + "\n"
			
		return result

	
	'''
	Apply a set of diffs to an original file to produce a new text file
	'''
	def apply_patch(self, doc, diffs):
		if diffs == None:
			return doc

		splits = self._split_with_maintain(doc)
		result = []
		lastIndex = 0

		for d in diffs:
			# bring the original document up to speed
			if d.start_index > lastIndex:
				result += splits[lastIndex:d.start_index]
			lastIndex += 1

			# respond to the diff
			if d.operation == DELETED:
				lastIndex += d.length
			elif d.operation == INSERTED:
				result += d.line
			else:
				result += d.line
				lastIndex += d.length

		return ''.join(result)

	'''
	Reverse the direction of a patch
	'''
	def reverse_patch(self, diff):
		result = []
		for d in diff:
			if d.operation == INSERTED:
				new_op = DELETED
			elif d.operation == DELETED:
				new_op = INSERTED
			else:
				new_op = UNCHANGED

			d.operation = new_op
			result.append(DiffResult(d.start_index, d.length, d.line, new_op))
		
		return result

	'''
	Convenience method for removing a patch
	'''
	def remove_patch(self, doc, diffs):
		patches = self.reverse_patch(diffs)
		return self.apply_patch(doc, patches)


'''
Run some basic tests on the class

from SimpleDiff import SimpleDiff
sd = SimpleDiff()
test1 = "a.b.c.d"
test2 = "a.g.c.d"
d = sd.diff(test1, test2)
h = sd.generate_html_diffs(d)
print h


'''

'''
run some speed tests - 1,000,000 took 135 seconds


from writer.libs.PyFreeDiff import PyFreeDiff
import time

t1 = "This is a simple text. Lorem Ipsum etc. I want to iterate 10,000 times and count elapsed.  Some more matched text.  Some other unmatched text.  Finally some joy"
t2 = "This is a simple text. Lorem Ipsum etc. Some more matched text.  Some other changed text.  Finally some joy! There could be some more?  What do you think!? I don't know.  Its weird This thing that have with the guy in the lemon popsicle."

def multi_test():
    start = time.time()
    for i in range(1000000):
        sd = PyFreeDiff()
        d = sd.diff(t1,t2)
        h = sd.generate_html_diffs(d)
    end = time.time() - start
    return end, d, h

elapsed,last_diff,last_html = multi_test()

elapsed

'''



sd = PyFreeDiff()
t1 = "This is a sample. Text of awesomeness. Can I patch it?"
t2 = "This is a sample.  Text of awesomeness.  Can I change it? Should I play it?  Can I patch it?"
diffs = sd.diff(t1, t2)
t3 = sd.apply_patch(t1, diffs)
print t2
print t3
print t2 == t3

t4 = sd.remove_patch(t3, diffs)
print t4
print t1
print t4 == t1


