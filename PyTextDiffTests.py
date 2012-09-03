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

import PyTextDiff
import unittest

class TestDiffGeneration(unittest.TestCase):

	def setUp(self):
		self.engine = PyTextDiff.DiffEngine()

	
	def test_splitting_of_text(self):
		easy_split_text = """This. Is an easy. splitting? function! it should return
			at least 14 sections when split."""
	
		result = self.engine._split_with_maintain(easy_split_text)
		self.assertEqual(len(result), 14)		# correct number of splits
		self.assertEqual(result[0], "This")		# correct first split
		self.assertEqual(result[2], " ")		# correct space split
		self.assertEqual(result[13], ".")		# correct last split
		
	def test_flattening_of_list(self):
		input_list = [[1,2],[3],[4,5,6,7],[8,[9,10]]]
		expected_output = [1,2,3,4,5,6,7,8,9,10]
		
		output = list(self.engine._flatten(input_list))
		self.assertEquals(output, expected_output)


if __name__ == '__main__':
	unittest.main()	
	