from os import listdir
from os.path import isfile, join
import random
import re

lib = "Lib"
files = [join(lib,f) for f in listdir(lib) if isfile(join(lib, f))]

table = {}

def test():
    return (open(files[0])).readlines()

class Tab:
    def __init__(self, num):
        self.n = num
    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.n == other.n
        else:
            return False
    def __hash__(self):
        return hash(self.n)
    def __str__(self):
        return "\t"*self.n
    def compare(self):
        return self.n

class Newline:
    def __hash__(self):
        return hash('\n')
    def __str__(self):
        return "\n"
    def compare(self):
        return -3

class EOF:
    def __hash__(self):
        return hash(1)
    def __str__(self):
        return ''
    def compare(self):
        return -1

class SOF:
    def __hash__(self):
        return hash(0)
    def __str__(self):
        return ''
    def compare(self):
        return -2

newline = Newline()
EOF = EOF()
SOF = SOF()

def add_to_table(file):
    f = open(file)
    try:
        lines = f.readlines()
    except:
        return
    tabspace = 0
    tokens = []
    docstring = False
    for line in lines:
        if line.split() == []:
            continue
        if docstring:
            if '"""' in line:
                docstring = False
            continue
        if '"""' in line:
            docstring = True
            continue
        if line.lstrip().startswith('#'):
            continue
        l_s = len(line) - len(line.lstrip())
        if l_s == 0 or l_s == 1:
            pass
        elif tabspace == 0:
            tabspace = l_s
            if tabspace > 4:
                return
            tokens.append(Tab(1))
        else:
            num = l_s // tabspace
            tokens.append(Tab(num))
        for token in line.split():
            if '#' in token:
                break
            else:
                tokens.append(token)
        tokens.append(newline)
    tokens.append(EOF)
    prev = SOF
    for token in tokens:
        if prev in table:
            table[prev].append((token, 1))
        else:
            table[prev] = [(token, 1)]
        prev = token

def list_endswith(s, l):
    if type(s) == str:
        for e in l:
            if type(e) != str:
                continue
            if s.endswith(e):
                return True
    else:
        for e in l:
            if s.compare() == e.compare():
                return True
    return False

def list_contains(s, l):
    if type(s) == str:
        for e in l:
            if type(e) != str:
                continue
            if e in s:
                return True
    else:
        for e in l:
            if s.compare() == e.compare():
                return True
    return False

def construct_line(t, token, until, no):
    result = ''
    last = token
    counter = 0
    while not list_endswith(token, until):
        if list_contains(token, no):
            if counter > 100:
                return "FAIL"
            counter += 1
            token = random.choice(table[last])[0]
            continue
        counter = 0
        result += str(token) + ' '
        last = token
        token = random.choice(t[token])[0]
    return result + str(token)

for file in files:
    add_to_table(file)

def dont_fail(t, token, until, no):
    line = construct_line(t, token, until, no)
    while line == "FAIL":
        line = construct_line(t, token, until, no)
    return line

def def_line():
    return dont_fail(table, 'def', [':'], [newline, EOF])

def while_line():
    return dont_fail(table, 'while', [':'], [newline, EOF])

def if_line():
    return dont_fail(table, 'if', [':'], [newline, EOF])

def elif_line():
    return dont_fail(table, 'elif', [':'], [newline, EOF])

def else_line():
    return dont_fail(table, 'else', [':'], [newline, EOF])

def tab_line(num):
    #print("This")
    return dont_fail(table, Tab(num), [newline], [':', EOF])

def triple_quote():
    return dont_fail(table, '"""', [newline], [EOF])

def construct_program():
    return dont_fail(table, SOF, [EOF], [])
        
