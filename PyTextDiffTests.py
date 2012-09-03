'''
Some basic speed tests for PyFreeDiff

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

from PyTextDiff import *
import unittest

class TestDiffUtilities(unittest.TestCase):

	def setUp(self):
		self.engine = DiffEngine()
		
		
	def test_splitting_of_text(self):
		easy_split_text = """This. Is an easy. splitting? function! it should return
			at least 14 sections when split."""
			
		result = self.engine._split_with_maintain(easy_split_text)
		self.assertEqual(len(result), 14)		# correct number of splits
		self.assertEqual(result[0], "This")		# correct first split
		self.assertEqual(result[2], " ")		# correct space split
		self.assertEqual(result[13], ".")		# correct last split
		
		
	def test_splitting_of_text_ignoring_trailing_spaces(self):
		easy_split_text = """This. Is an easy. splitting? function! it should return
			at least 14 sections when split."""
			
		result = self.engine._split_with_maintain(easy_split_text, False)
		self.assertEqual(len(result), 10)			# correct number of splits
		self.assertEqual(result[0], "This")			# correct first split
		self.assertEqual(result[2], " Is an easy")	# correct space split
		self.assertEqual(result[9], ".")			# correct last split
		
		
	def test_packing_of_diffs_to_string(self):
		pack_diff_text = "+ insert\n skip\n- remove\n+ insert2"
		expected_result = "+000@001:insert\n-002@001:remove\n+002@001:insert2"
		result = self.engine._pack_results(pack_diff_text)
		self.assertEquals(result, expected_result)
		
		
	def test_empty_pack_returns_empty(self):
		self.assertEquals(self.engine._pack_results(None), None)
		self.assertEquals(self.engine._pack_results([]), None)
		
		
	def test_unpacking_of_diffs_to_objects(self):
		unpack_diff_text = "+000@001:insert\n-001@001:remove\n+001@001:insert2"
		result = self.engine._unpack_results(unpack_diff_text)
		
		# check the individual diff objects
		self.assertEquals(len(result), 3)
		self.assertEquals(result[0].start_index, 0)
		self.assertEquals(result[1].start_index, 1)
		self.assertEquals(result[2].start_index, 1)
		self.assertEquals(result[0].length, 1)
		self.assertEquals(result[1].length, 1)
		self.assertEquals(result[2].length, 1)
		self.assertEquals(result[0].operation, "+")
		self.assertEquals(result[1].operation, "-")
		self.assertEquals(result[2].operation, "+")
		self.assertEquals(result[0].line, "insert")
		self.assertEquals(result[1].line, "remove")
		self.assertEquals(result[2].line, "insert2")
		
		
	def test_flattening_of_list(self):
		input_list = [[1,2],[3],[4,5,6,7],[8,[9,10]]]
		expected_output = [1,2,3,4,5,6,7,8,9,10]
		
		output = list(self.engine._flatten(input_list))
		self.assertEquals(output, expected_output)
		
		
class TestDiffFormatting(unittest.TestCase):
	
	# TODO: Patch to HTML and test
	
	def setUp(self):
		self.engine = DiffEngine()
		
	def test_html_output(self):
		diff_text = "+000@001:insert\n-001@001:remove\n+001@001:insert2"
		expected_output = "<ins>insert</ins>\n<del>remove</del>\n<ins>insert2</ins>\n"
		
		output = self.engine.diffs_to_html(diff_text)
		self.assertEquals(output, expected_output)
	
	
class TestDiffResults(unittest.TestCase):
	
	def setUp(self):
		self.engine = DiffEngine()
		
	def test_basic_diffs_to_string(self):
		original = "skip. remove. "
		revised = "insert. skip. insert2!"
		expected_result = "+000@003:insert. \n+003@002:insert2!\n-003@003:remove. "
		
		result = self.engine.diff(original,revised)
		self.assertEquals(result, expected_result)
	
	# TODO: Diff Tests

	
	
	# TODO: Diff3 Tests
	# TODO: Patch Tests
	
	
if __name__ == '__main__':
	unittest.main()	
	