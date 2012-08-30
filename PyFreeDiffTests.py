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

import PyFreeDiff
import time

class SpeedTests(object):
	t1 = "This is a simple text. Lorem Ipsum etc. I want to iterate 10,000 times and count elapsed.  Some more matched text.  Some other unmatched text.  Finally some joy"
	t2 = "This is a simple text. Lorem Ipsum etc. Some more matched text.  Some other changed text.  Finally some joy! There could be some more?  What do you think!? I don't know.  Its weird This thing that have with the guy in the lemon popsicle."

	
	# crudely tests 'n' iterations of the algorith... currently 1,000,000 takes ~270 seconds using
	def multi_test(self, num_tests):
		start = time.time()
		for i in range(num_tests):
			sd = PyFreeDiff.DiffEngine()
			d = sd.diff(self.t1, self.t2)
			h = sd.generate_html_diffs(d)
			
		elapsed = time.time() - start
		print str(num_tests) + " DiffEngine.diff() iterations took " + str(elapsed) + " seconds"
		return elapsed, d, h
