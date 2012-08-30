'''
A simple diff by breaking into sentences and comparing adjacent sentences.
Based on Python Difflib and available under the ultra permissive MIT license


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
import difflib

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
class DiffEngine(object):

	'''
	Performs a basic diff on two strings, splitting by sentence and returning
	the diffs between original and revised
	'''
	def diff(self, original, revised):
		results = []
		
		# build a list of sentences for each input string
		original_arr = self._split_with_maintain(original)
		new_arr = self._split_with_maintain(revised)
		
		# diff the result
		raw_diffs = list(difflib.ndiff(original_arr, new_arr))
		
		# convert to diff format
		for i,d in enumerate(raw_diffs):
			if d[0] == '-':
				op = DELETED
			elif d[0] == '+':
				op = INSERTED
			else:
				op = UNCHANGED
			results.append(DiffResult(i, 1, d[2:], op))
		
		return results
		
	'''
	Generates a 3 way diff between three related documents, allowing rebasing of 'mine'
	based on changes from 'theirs'
	
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
			found  = rx.search(str(check))
			if found == None:
				result.append(check)
				break
			
			idx = found.start()
			result.append(str(check[:idx]))			# append the string
			result.append(str(check[idx:idx+1]))	# append the puncutation so changing ? to . doesn't invalidate the whole sentence
			check = check[idx + 1:]
			
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
					result.append(check[0:space_idx])
			
				check = check[space_idx:]
			
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
	def switch_patch_direction(self, diff):
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
		patches = self.switch_patch_direction(diffs)
		return self.apply_patch(doc, patches)

