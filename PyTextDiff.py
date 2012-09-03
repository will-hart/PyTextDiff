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

import collections
import difflib
import re

'''
Constants for determining the status of a diff_result
'''
DELETED = '-'
UNCHANGED = ' '
INSERTED = '+'
CONFLICT_MINE = '?'
CONFLICT_THEIRS = '!'


'''
Constant for a standard sentence parts split - splits on commas, full stops,
exclamation marks and question marks. This may be overriden when DiffEngine.diff()
is called.
'''
STANDARD_REGEX = '[,.!?]'

'''
A constant used to replace new line characters in a string before passing to 
diff manager.  This is because most diff algorithms relying on newlines for 
splitting texts and we want to retain new lines
'''
NEWLINE_MASK = '~~#%#'


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
    
    def lines_touched():
        return set(range(self.start_index, self.start_index + self.length))
    
    def contains(self, other_result):
        return self.lines_touched().isdisjoint(other_result.lines_touched())
        
    def get_contained_indices(self, other_result):
        return self.lines_touched().intersection(other_result.lines_touched())
    
    def split(self, index):
        # split the DiffResult at the given index, returning the two halves
        # assumes default diffing behaviour was used
        splits = self._split_with_maintain(line)
        
        a_splits = splits[:index-self.start_index]
        b_splits = splits[index-self.start_index:]
        
        return DiffResult(self.start_index, index, ''.join(a_splits), self.operation), \
                DiffResult(self.start_index + index, self.length-index, ''.join(b_splits), self.operation)
    
    def __str__(self):
        return str(self.operation) + "{number:03}".format(number=self.start_index) + \
        "@" + "{number:03}".format(number=self.length) + ":" + ''.join(self.line)


'''
A class for performing diff and patch operations on strings.  Operations
such as diff and diff3 return a string formatted for saving in a database 
or display.

Functions like diff_to_html and patch take this same formatted string and 
either generate HTML formatted diffs or apply a patch to the file.
'''
class DiffEngine(object):

    '''
    Performs a basic diff on two strings, splitting by sentence and returning
    the diffs between original and revised
    '''
    def diff(self, original, revised):
        
        # build a list of sentences for each input string
        original_text = self._split_with_maintain(original)
        revised_text = self._split_with_maintain(revised)
        
        # diff the result
        raw_diffs = self._generate_diff(original_text, revised_text, 0) #'\n'.join(difflib.ndiff(original_text, new_text))
        
        # pack the raw_diffs into a string format and return the results
        return '\n'.join([d.__str__() for d in raw_diffs])#self._pack_results(raw_diffs)

    
    '''
    Generates a 3 way diff between three related documents, allowing rebasing of 'mine'
    based on changes from 'theirs', and flags conflicts where both sets of changes attempt
    to modify the same text
    '''
    def diff3(self, mine, original, theirs):
        results = []
        
        # get a combined diff object representing the sorted diffs from both parties
        both_diffs = self._unpack_results(self.diff(original, mine))
        both_diffs += self._unpack_results(self.diff(original, theirs))
        sorted(both_diffs, key=attrgetter('start_index'))
        
        # now go through and merge the diffs
        
        
        pass

        
    '''
    Generate basic HTML for a diff string generated from DiffEngine.diff() or DiffEngine.diff3()
    '''
    def diffs_to_html(self, diffs):
        if diffs == None:
            return ""

        start = ""
        end = ""
        result = ""
        
        for diff in self._unpack_results(diffs):
                    
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
            result += start + ''.join(diff.line) + end + "\n"
            
        return result
    
    ''''
    Generates an html output of patched document, with insertions
    and deletions surrounded by <ins> and <del> tags.
    '''
    def patch_to_html(self, doc, patch):
        pass
        
        
    '''
    Apply a set of diffs to an original file to produce a new text file.
    You can either pass a string or a pre-split list of items
    '''
    def apply_patch(self, doc, diffs):
        if diffs == None:
            return doc

        diffs = self._unpack_results(diffs)
        
        result = []
        lastIndex = 1

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

        return ''.join(result).replace(NEWLINE_MASK, '\n')


    '''
    Remove a patch from some text and return the original text
    '''
    def remove_patch(self, doc, diffs):
        diffs = self._unpack_results(diffs)
        patches = self._switch_patch_direction(diffs)
        return self.apply_patch(doc, patches)


    '''
    Reverse the direction of a patch
    '''
    def _switch_patch_direction(self, diff):
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
    Splits a string based on a list of chars and returns the list.
    For instance, when calling split_with_maintain(str, '[.!?]')
        "This is a test.  It should split awesomely."
    Becomes:
        ["This is a test", ".", "  ", "It should split awesomely", "."]
    '''
    def _split_with_maintain(self,
        value,
        treat_trailing_spaces_as_sentence = True,
        split_char_regex = STANDARD_REGEX):
        
        
        result = []
        check = value.replace('\n',NEWLINE_MASK) # mask out new line values
        
        # compile regex
        rx = re.compile(split_char_regex)
        
        # traverse the string
        while len(check) > 0:
            found  = rx.search(str(check))
            if found == None:
                result.append(check)
                break
            
            idx = found.start()
            result.append(str(check[:idx]))         
            result.append(str(check[idx:idx+1]))    
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
    packs up a set of results returned by DiffLib into a string that can
    be returned to the user. This string can be saved into database or file.
    The main operation here is to remove empty lines
    '''
    def _pack_results(self, raw_diffs):
        if raw_diffs == None or len(raw_diffs) == 0:
            return None
        
        results = ''
        raw_list = raw_diffs.split('\n')
        prev_op = ''
        count = 0
        start = 0
        length = 0
        current = ''
        
        for raw in raw_list:
            if len(raw) == 0:
                continue
                
            if raw[0] != prev_op:
                start = count
                if length > 0:
                    results +=  prev_op + "{number:03}".format(number=start) + "@" +\
                                "{number:03}".format(number=length) + ":" + current + "\n"
                    current = ''
                    length = 0
                
            # save the operation
            prev_op = raw[0]
            
            # increment counters
            if prev_op != "+":
                count += 1
            if prev_op != " ":
                current += raw[2:]
                length += 1
                
        if length > 0:
            results += prev_op + "{number:03}".format(number=start) + "@" +\
                        "{number:03}".format(number=length) + ":" + current
            
        return results
        
    '''
    Takes a raw diff string and converts it into native DiffResult objects
    
    The raw diffs must be in the format:  "[OP][START_IDX, 3 digits]@[LENGTH - 3 digits]:[TEXT]\n"
    
    e.g.  +003@001:This text starts at index 3 and goes for one index.\n
    '''
    def _unpack_results(self, raw_string):
        raw_list = raw_string.split('\n')
        results = []
        
        for raw in raw_list:
            #check validity 
            if raw[4] != '@' or raw[8] != ':':
                raise ValueError('Unrecognised diff input line: %s' % raw)
            
            # grab values
            start_idx = int(raw[1:4])
            length = int(raw[5:8])
            lines = self._split_with_maintain(raw[9:])
            operation = raw[0]
            
            results.append(DiffResult(start_idx, length, lines, operation))
            
        return results
        
        
    '''
    Flatten an irregular list of ints
     --> http://stackoverflow.com/questions/2158395
    '''
    def _flatten(self, l):
        for el in l:
            if isinstance(el, collections.Iterable) and not isinstance(el, basestring):
                for sub in self._flatten(el):
                    yield sub
            else:
                yield el
        
    '''
    Generate a 'dumb' diff between two strings.
    '''
    def _generate_diff(self, original, revised, start_idx):
        print start_idx
        # check if we have empty lists - means we are at the bottom of recursion
        if len(original) == 0 and len(revised) == 0:
            return None
            
        # check if the strings are the same
        if ",".join( map( str, original ) ) == ",".join( map( str, revised ) ):
            return None #[DiffResult(start_idx, len(revised), revised, UNCHANGED)]
            
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
        
        # build up the 2d list showing longest common sequence
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
            print "no match"
            print ','.join(original) + " @@" + str(len(original))
            print ','.join(revised) + " @@" + str(len(revised))
            result.append(DiffResult(start_idx, len(original), original, DELETED))
            result.append(DiffResult(start_idx, len(revised), revised, INSERTED))
            return result
            
        # generate diffs that are 'left' of the longest common sequence on the table
        others = self._generate_diff(original[0:old_max], revised[0:new_max], start_idx)
        if others is not None:
            result += others
        
        # ignore central diffs (i.e. ignore common longest sequence)
        #o = DiffResult(start_idx + new_max, max_len, revised[new_max : new_max + max_len], UNCHANGED)  
        #result.append(o)
        
        # generate diffs to the right of the longest common sequence
        others = self._generate_diff(
            original[old_max + max_len :],
            revised[new_max + max_len :],
            old_max + max_len + start_idx)
        if others is not None:
            result += others
    
        return result
