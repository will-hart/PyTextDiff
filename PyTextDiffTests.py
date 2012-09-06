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
        self.assertEqual(len(result), 14)        # correct number of splits
        self.assertEqual(result[0], "This")        # correct first split
        self.assertEqual(result[2], " ")        # correct space split
        self.assertEqual(result[13], ".")        # correct last split
        
        
    def test_splitting_of_text_ignoring_trailing_spaces(self):
        easy_split_text = """This. Is an easy. splitting? function! it should return
            at least 14 sections when split."""
            
        result = self.engine._split_with_maintain(easy_split_text, False)
        self.assertEqual(len(result), 10)            # correct number of splits
        self.assertEqual(result[0], "This")            # correct first split
        self.assertEqual(result[2], " Is an easy")    # correct space split
        self.assertEqual(result[9], ".")            # correct last split
        
        
    def test_packing_of_diffs_to_string(self):
        pack_diff_text = "+ insert\n skip\n- remove\n+ insert2"
        expected_result = "+000@001:insert\n-002@001:remove\n+002@001:insert2"
        result = self.engine._pack_results(pack_diff_text)
        self.assertEqual(result, expected_result)
        
        
    def test_empty_pack_returns_empty(self):
        self.assertEqual(self.engine._pack_results(None), None)
        self.assertEqual(self.engine._pack_results([]), None)
        
        
    def test_unpacking_of_diffs_to_objects(self):
        unpack_diff_text = "+000@001:insert\n-001@001:remove\n+001@001:insert2"
        result = self.engine._unpack_results(unpack_diff_text)
        
        # check the individual diff objects
        self.assertEqual(len(result), 3)
        self.assertEqual(result[0].start_index, 0)
        self.assertEqual(result[1].start_index, 1)
        self.assertEqual(result[2].start_index, 1)
        self.assertEqual(result[0].length, 1)
        self.assertEqual(result[1].length, 1)
        self.assertEqual(result[2].length, 1)
        self.assertEqual(result[0].operation, "+")
        self.assertEqual(result[1].operation, "-")
        self.assertEqual(result[2].operation, "+")
        self.assertEqual(result[0].line, ["insert"])
        self.assertEqual(result[1].line, ["remove"])
        self.assertEqual(result[2].line, ["insert2"])
        
        
    def test_flattening_of_list(self):
        input_list = [[1,2],[3],[4,5,6,7],[8,[9,10]]]
        expected_output = [1,2,3,4,5,6,7,8,9,10]
        
        output = list(self.engine._flatten(input_list))
        self.assertEqual(output, expected_output)
    
    def test_splitting_of_diffs_zero_start_index(self):
        d = DiffResult(0, 5, ['a','b','c','d','e'], "+")
        a,b = d.split(2)
        
        self.assertEqual(a.start_index, 0)
        self.assertEqual(b.start_index, 2)
        self.assertEqual(a.length, 2)
        self.assertEqual(b.length, 3)
        self.assertEqual(a.operation, "+")
        self.assertEqual(b.operation, "+")
        self.assertEqual(''.join(a.line),'ab')
        self.assertEqual(''.join(b.line),'cde')
    
        
    def test_splitting_of_diffs_non_zero_start_index(self):
        d = DiffResult(5, 5, ['a','b','c','d','e'], "+")
        a,b = d.split(2)
        
        self.assertEqual(a.start_index, 5)
        self.assertEqual(b.start_index, 7)
        self.assertEqual(a.length, 2)
        self.assertEqual(b.length, 3)
        self.assertEqual(a.operation, "+")
        self.assertEqual(b.operation, "+")
        self.assertEqual(''.join(a.line),'ab')
        self.assertEqual(''.join(b.line),'cde')
        
    def test_splitting_of_diffs_where_index_exceeds_length(self):
        d = DiffResult(0, 5, ['a','b','c','d','e'], "+")
        a,b = d.split(9)
        
        self.assertEqual(a.start_index, 0)
        self.assertEqual(b, None)
        self.assertEqual(a.length, 5)
        self.assertEqual(a.operation, "+")
        self.assertEqual(''.join(a.line),'abcde')
    

    def test_splitting_of_diffs_where_index_negative(self):
        d = DiffResult(0, 5, ['a','b','c','d','e'], "+")
        a,b = d.split(-1)
        
        self.assertEqual(b.start_index, 0)
        self.assertEqual(a, None)
        self.assertEqual(b.length, 5)
        self.assertEqual(b.operation, "+")
        self.assertEqual(''.join(b.line),'abcde')
       
        
        
class TestDiffFormatting(unittest.TestCase):
    
    # TODO: Patch to HTML and test
    
    def setUp(self):
        self.engine = DiffEngine()
        
    def test_html_output(self):
        diff_text = "+000@001:insert\n-001@001:remove\n+001@001:insert2"
        expected_output = "<ins>insert</ins>\n<del>remove</del>\n<ins>insert2</ins>\n"
        
        output = self.engine.diffs_to_html(diff_text)
        self.assertEqual(output, expected_output)
    
    
class TestDiffResults(unittest.TestCase):
    
    def setUp(self):
        self.engine = DiffEngine()
        
    def test_basic_diffs_to_string(self):
        original = "skip. remove. "
        revised = "insert. skip. insert2!"
        expected_result = "+000@003:insert. \n-003@003:remove. \n+003@002:insert2!"
         
        result = self.engine.diff(original,revised)
        self.assertEqual(result, expected_result)
        
    def test_complex_diffs_to_string(self):
        original = \
"""This is a complex diff.  It contains newlines

exclamation marks! changes in spaces (like here). and some other. weird?! formatting.

We need to check it parses properly"""
        
        revised = \
"""This is a complex diff!  It has newlines, exclamation marks! changes in spaces (like here). and some other formatting.

We need to check it parses properly"""
        
        expected_output = "-001@001:.\n+001@001:!\n-003@001:It contains newlines~~#%#~~#%#exclamation marks!\n" + \
                        "+003@001:It has newlines, exclamation marks\n-009@008:and some other. weird?! formatting\n"+\
                        "-009@001:and some other formatting"
    
        output = self.engine.diff(original, revised)
        self.assertEqual(output, expected_output)
    
    def test_basic_noconflict_diff3_to_string(self):
        output = self.engine.diff3("a.b.c.d","a.b.e.c.d","a.c.h.d")
        self.assertEqual(output,"")
    
    
    # TODO: Patch Tests, including patch_to_html, maintenance of newlines during diff/patch
    
    
if __name__ == '__main__':
    unittest.main()    
    