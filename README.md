PyTextDiff
==========

[![Build Status](http://176.58.119.7:8080/job/PyTextDiff/badge/icon)](http://176.58.119.7:8080/job/PyTextDiff/)

The ability to keep various versions of documents and view changes between versions is something that is widely adopted in the programming community and there are numerous free or paid solutions available. The requirements for version control of text documents is similar, yet subtly different.  In many instances an entire paragraph may be on a single line, and hence most programming version control systems would 'diff' an entire paragraph even if only a word was changed.  Generating diffs by words can be messy and where multiple editors are working on a single piece of text may lead to sentences that don't make read correctly if two users modify the same sentence in different ways.

PyTextDiff attempts to solve this riddle by generating diffs by 'sentence part,' that is either whole sentences or through key puncutation.  For instance if we took a sentence:

    This is a diff. Do you like it?
    
and changed it to

    This is a diff.  I really like it!
    
PyTextDiff would generate a 'diff' something like:

    - Do you like it?
    + I really like it!

PyTextDiff is 'punctuation aware', and retains newlines wtihin text.  This means that changing the puncutation at the end of a sentence will generate a diff for only that part of the sentence.  For instance

    This is my original text.
    
If changed to

    This is my original text! 
    
Would generate a 'diff' like

    - .
    + !

As most version control diff formats (for instance the unified format) are geared towards programming files, a custom diff format is used which is a string that can be saved to database or file.  PyTextDiff is able to 'pack' and 'unpack' these strings into an internal diff object.

Availability
============

PyTextDiff is available as completely free and open source software under the permissive MIT license. There are no requirements for using the code in your own project, however if you do use this library, it would be really nice to know about it!

Currently PyTextDiff is in active development and hence not suitable for a production environment.  Some function names and behaviour **will** change before a 'version 1.0' is released.  


Features
========

Currently PyFreeDiff allows:
 - Generate diffs at sentence level
 - Apply patches to a file
 - Remove patches from a file
 - A complete set of unit tests

Roadmap
=========

Currently in development:
 - Three way merge

Usage
=====

Clone the repository to your local computer. 

A simple example usage may be as follows

    from PyTextDiff import DiffEngine

    sd = DiffEngine()
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


The unit tests can be run as follows, from within the PyTextDiff directory

    >>> python PyTextDiffTests.py


License
=======

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

