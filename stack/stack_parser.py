from __future__ import absolute_import
import collections, pickle, string
from stack.constants import *
from io import open

Token = collections.namedtuple(u'Token',u'TYPE VAL')

def split(s):
    s = s.strip()
    res = []
    in_string = False
    cur = []
    for i, char in enumerate(s):
        if char in string.whitespace and not in_string:
            w = u''.join(cur)
            if not w == u'':
                res.append(w)
                cur = []
        else:
            if char == u"/" and s[i+1] == u"'":
                char = u''
            if char == u"'" :
                if i > 0 and s[i-1] == u'/':
                    pass
                else:
                    in_string = not in_string
            cur.append(char)
    if cur:
        res.append(u''.join(cur))
    return res
def _parse_iter(prog):
    prog_len = len(prog) - 1
    prog_index = -1
    tokens = []
    while prog_index < prog_len:
        prog_index += 1
        tok = prog[prog_index]
        if is_op(tok):
            tokens.append(Token(TYPE=u'op',VAL=tok))
        elif is_str(tok):
            tokens.append(Token(TYPE=u'str',VAL=tok[1:-1]))
        elif is_num(tok):
            tokens.append(Token(TYPE=u'num',VAL=float(tok)))
        elif is_bool(tok):
            tokens.append(Token(TYPE=u'bool',VAL=(True if tok == u'True' else False)))
        elif is_list(tok):
            tokens.append(Token(TYPE=u'list',VAL=[]))
        elif is_name(tok):
            tokens.append(Token(TYPE=u'name',VAL=tok[1:]))
        elif is_var(tok):
            tokens.append(Token(TYPE=u'var',VAL=tok))
        elif tok == BLOCK_START:
            code, end = _parse_iter(prog[prog_index+1:])
            prog_index += end + 1
            tokens.append(Token(TYPE=u'code',VAL=code))
        elif tok == BLOCK_END:
            break
    return tokens, prog_index

def parse(prog_string):
    return _parse_iter(split(prog_string))[0]

def compile_to_file(prog,filename):
    code = parse(prog)
    f = open(filename, u'wb')
    pickle.dump(code,f)
    f.close()
if __name__ == u'__main__':
    print parse(u"5 `n set n")
