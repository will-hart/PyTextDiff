PyFreeDiff
==========

PyFreeDiff is a completely free and open source library built from the ground up to provide efficient *diff*, *patch* and *merge* functionality in python, with a focus on text based comparisons.

It was developed in response to the large number of diff algorithms available in the public domain under highly resrtrictive GPL type licenses.  This code uses the permissive MIT license, which allows just about any use under the sun, hence Python **FREE** diff library became PyFreeDiff.

If you do use this library, it would be really nice to know about it, and also if you find any issues or make any improvements that you felt like  contributing back that would be great!


Features
========

Currently PyFreeDiff allows:
 - Generate diffs at sentence level
 - Apply patches to a file
 - Remove patches from a file


Roadmap
=========

Currently in development:
 - Word level diff
 - Three way merge
 - Generation of unified diff/patch format diffs

Usage
=====

Download (or checkout) the `PyFreeDiff.py` file and place it in a directory such as `lib`.

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

