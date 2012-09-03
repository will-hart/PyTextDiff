PyFreeDiff
==========

PyTextDiff is a completely free and open source wrapper for Python's difflib that provides efficient  *diff*, *patch* and *merge* functionality.  PyTextDiff is different in that its main focus is on the versioning of text documents, where the traditional 'line by line' diffing approach is not desirable. Therefore it generates diffs on the basis of 'sentence parts'.

It is available as truly free and open source software under the permissive MIT license. There are no requirements for using the code in your own project, however if you do use this library, it would be really nice to know about it!

Currently PyTextDiff is in active development and hence not suitable for a production environment as some function names and behaviour is likely to change.


Features
========

Currently PyFreeDiff allows:
 - Generate diffs at sentence level
 - Apply patches to a file
 - Remove patches from a file


Roadmap
=========

Currently in development:
 - Three way merge

Usage
=====

Clone the repository to your local computer. 

A simple example usage may be as follows

    from PyFreeDiff import PyFreeDiff

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

