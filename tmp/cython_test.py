#! /usr/bin/python
# -*- coding: utf-8 -*-

def test(b):
    a = 0
    for i in b:
        a += i
    return a

if __name__ == "__main__":
    import cython_test_def
    b = [i for i in range(10)]
    print test(b)
    print cython_test_def.simple_add(b)
