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
    
    def __str__(self):
        return str(self.operation) + "@" + str(self.start_index) + "-" + str(self.start_index + self.length) + ": " + self.line


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
        new_text = self._split_with_maintain(revised)
        
        # diff the result
        raw_diffs = list(difflib.ndiff(original_text, new_text))
        
        # pack the raw_diffs into a string format and return the results
        return self._pack_results(raw_diffs)

    
    '''
    Generates a 3 way diff between three related documents, allowing rebasing of 'mine'
    based on changes from 'theirs', and flags conflicts where both sets of changes attempt
    to modify the same text
    '''
    def diff3(self, mine, original, theirs):
        results = {}
        
        my_diffs = self._unpack_results(self.diff(original, mine))
        their_diffs = self._unpack_results(self.diff(original, theirs))
        
        # find the collisions between the two diffs using python sets
        my_lines = set(self._flatten([range(d.start,d.start+d.length) for d in my_diffs]))
        their_lines = set(self._flatten([range(d.start,d.start+d.length) for d in their_diffs]))
        collisions = my_lines.intersection(their_lines).sort()

        # now go through and merge the diffs, flagging collisions separately
        index = 0
        my_idx = 0
        their_idx = 0
        conflict = 0
        while my_idx < len(my_diffs) or their_idx < len(their_diffs):

            # process the next diff
            if my_diffs[my_idx].start_index < their_diffs[their_idx].start_index:
                diff_to_process = my_diffs[my_idx]
                my_idx += 1
            else:
                diff_to_process = their_diffs[their_idx]
                their_idx += 1
        
            
        pass

        
    '''
    Generate basic HTML for a diff string generated from DiffEngine.diff() or DiffEngine.diff3()
    '''
    def diff_to_html(self, diffs):
        if diffs == None:
            return ""

        start = ""
        end = ""
        result = ""
        
        for diff in self._unpack_results(diffs):
        
            if len(diff) == 0:
                continue
            
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
    def _split_with_maintain(self, value, treat_trailing_spaces_as_sentence = True, split_char_regex = STANDARD_REGEX):
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
            result.append(str(check[:idx]))         # append the string
            result.append(str(check[idx:idx+1]))    # append the puncutation so changing ? to . doesn't invalidate the whole sentence
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
        raw_list = raw_diffs.split('\n')
        results = []
        index = 0
        last_op = ''
        last_op_idx = 0
        current_str = ''
        
        for r in raw_list:
            if r[0] == last_op:
                current_str += r[2:]
            else:
                if last_op != ' ': # ignore no change lines to compress results
                    results.append(last_op + str(last_op_idx).format("\3d") + "@" + \
                            str(index-last_op_idx).format("\3d") + ":" + current_str)
                    current_str = r[2:]
                else: 
                    current_str = None
                last_op = r[0]
                last_op_idx = index
            
            index += 1
        return '\n'.join(results)
        
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
            text = raw[9:]
            operation = raw[0]
            
            results.append(DiffResult(start_idx, length, operation, text))
        
        return results


    '''
    Flatten an irregular list of ints
     --> http://stackoverflow.com/questions/2158395
    '''
    def _flatten(l):
        for el in l:
            if isinstance(el, collections.Iterable) and not isinstance(el, basestring):
                for sub in flatten(el):
                    yield sub
            else:
                yield el