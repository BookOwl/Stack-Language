from __future__ import division
from __future__ import absolute_import
import sys, time
import stack.stack_parser
from stack.constants import *
#Token = stack.stack_parser.Token
class Token(object):
    def __init__(self,TYPE,VAL):
        self.TYPE = TYPE
        self.VAL = VAL
    def __str__(self):
        return u'Token(TYPE=%s, VAL=%s)' % (unicode(self.TYPE), unicode(self.VAL))

def report_error(error_type,op, error_msg):
    print u'***%s ERROR***' % error_type
    print u'Operation: %s' % op
    print error_msg
    sys.exit(1)

def _stream_interpet(token_stream):
    scopes = [ { u'user-words':{} } ]
    data_stack = []
    #print(token_stream)
    for i, token in enumerate(token_stream):
        #print(i,token)
        if token.TYPE in DATA_TYPES:
            #Push data onto the stack
            data_stack.append(token)
        elif token.TYPE == u'var':
            #Token is the name of a var or user defined word
            # Retrieve the var or call the word
            if u'var_' + token.VAL in scopes[-1]:
                token_stream[i+1:i+1] = [ Token(TYPE=u'name',VAL=token.VAL), Token(TYPE=u'op',VAL=u'get') ]
            elif u'word_' + token.VAL in scopes[-1][u'user-words']:
                token_stream[i+1:i+1] = [ Token(TYPE=u'name',VAL=token.VAL), Token(TYPE=u'op',VAL=u'call') ]
            else:
                print scopes
                report_error(u'DATA_ERROR',  u'~intrnal', u'%s is not defined as a variable or word!' % token.VAL)
        else:
            #Token is a word
            
            #INDEX:
            # (op type)   (lines)
            # Math ops: 32-149
            # String ops: 150-173
            # IO ops: 174-191
            # Data Stack ops: 193-212
            # Bool ops: 214-269
            # List ops: 272-445
            # Scope and variable ops: 446-499
            # Misc ops: 500-512
            # Control Flow ops: 514-549
            # User words ops: 550-578
            
            op = token.VAL
            #Math ops
            if op == u'+':
                try:
                    val2, val1 = data_stack.pop(), data_stack.pop()
                except IndexError:
                    report_error(u'DATA_STACK', u'+',
                                 u'There are not enough values to pop.')
                if val1.TYPE != u'num':
                    report_error(u'TYPE', u'+',
                                 u'%s is not a number!' % unicode(val1))
                if val2.TYPE != u'num':
                    report_error(u'TYPE', u'+',
                                 u'%s is not a number!' % unicode(val2))
                res = Token(TYPE=u'num', VAL=val1.VAL+val2.VAL)
                data_stack.append(res)
            elif op == u'-':
                try:
                    val2, val1 = data_stack.pop(), data_stack.pop()
                except IndexError:
                    report_error(u'DATA_STACK', u'-',
                                 u'There are not enough values to pop.')
                if val1.TYPE != u'num':
                    report_error(u'TYPE', u'-',
                                 u'%s is not a number!' % unicode(val1))
                if val2.TYPE != u'num':
                    report_error(u'TYPE', u'-',
                                 u'%s is not a number!' % unicode(val2))
                res = Token(TYPE=u'num', VAL=val1.VAL-val2.VAL)
                data_stack.append(res)
            elif op == u'*':
                try:
                    val2, val1 = data_stack.pop(), data_stack.pop()
                except IndexError:
                    report_error(u'DATA_STACK', u'*',
                                 u'There are not enough values to pop.')
                if val1.TYPE != u'num':
                    report_error(u'TYPE', u'*',
                                 u' %s is not a number!' % unicode(val1))
                if val2.TYPE != u'num':
                    report_error(u'TYPE', u'*',
                                 u'%s is not a number!' % unicode(val2))
                res = Token(TYPE=u'num', VAL=val1.VAL*val2.VAL)
                data_stack.append(res)
            elif op == u'/':
                try:
                    val2, val1 = data_stack.pop(), data_stack.pop()
                except IndexError:
                    report_error(u'DATA_STACK', u'/',
                                 u'There are not enough values to pop.')
                if val1.TYPE != u'num':
                    report_error(u'TYPE', u'/',
                                 u'%s is not a number!' % unicode(val1))
                if val2.TYPE != u'num':
                    report_error(u'TYPE', u'/',
                                 u'%s is not a number!' % unicode(val2))
                res = Token(TYPE=u'num', VAL=val1.VAL/val2.VAL)
                data_stack.append(res)
            elif op == u'num':
                try:
                    val1 = data_stack.pop()
                except IndexError:
                    report_error(u'DATA_STACK', u'num',
                                 u'There are not enough values to pop.')
                res = Token(TYPE=u'num', VAL=float(val1.VAL))
                data_stack.append(res)
            elif op == u'BAND':
                try:
                    val2, val1 = data_stack.pop(), data_stack.pop()
                except IndexError:
                    report_error(u'DATA_STACK', u'BAND',
                                 u'There are not enough values to pop.')
                if val1.TYPE != u'num':
                    report_error(u'TYPE', u'BAND',
                                 u'%s is not a number!' % unicode(val1))
                if val2.TYPE != u'num':
                    report_error(u'TYPE', u'BAND',
                                 u'%s is not a number!' % unicode(val2))
                res = Token(TYPE=u'num', VAL=int(val1.VAL)&int(val2.VAL))
                data_stack.append(res)
            elif op == u'BOR':
                try:
                    val2, val1 = data_stack.pop(), data_stack.pop()
                except IndexError:
                    report_error(u'DATA_STACK', u'BOR',
                                 u'There are not enough values to pop.')
                if val1.TYPE != u'num':
                    report_error(u'TYPE', u'BOR',
                                 u'%s is not a number!' % unicode(val1))
                if val2.TYPE != u'num':
                    report_error(u'TYPE', u'BOR',
                                 u'%s is not a number!' % unicode(val2))
                res = Token(TYPE=u'num', VAL=int(val1.VAL)|int(val2.VAL))
                data_stack.append(res)
            elif op == u'BXOR':
                try:
                    val2, val1 = data_stack.pop(), data_stack.pop()
                except IndexError:
                    report_error(u'DATA_STACK', u'BXOR',
                                 u'There are not enough values to pop.')
                if val1.TYPE != u'num':
                    report_error(u'TYPE', u'BXOR',
                                 u'%s is not a number!' % unicode(val1))
                if val2.TYPE != u'num':
                    report_error(u'TYPE', u'BXOR',
                                 u'%s is not a number!' % unicode(val2))
                res = Token(TYPE=u'num', VAL=int(val1.VAL)^int(val2.VAL))
                data_stack.append(res)
            elif op == u'BNOT':
                try:
                    val2 = data_stack.pop()
                except IndexError:
                    report_error(u'DATA_STACK', u'BNOT',
                                 u'There are not enough values to pop.')
                if val2.TYPE != u'num':
                    report_error(u'TYPE', u'BNOT',
                                 u'%s is not a number!' % unicode(val2))
                res = Token(TYPE=u'num', VAL=~int(val2.VAL))
                data_stack.append(res)
            #String ops
            elif op == u'concat':
                try:
                    val2, val1 = data_stack.pop(), data_stack.pop()
                except IndexError:
                    report_error(u'DATA_STACK', u'concat',
                                 u'There are not enough values to pop.')
                if val1.TYPE != u'str':
                    report_error(u'TYPE', u'concat',
                                 u'%s is not a string!' % unicode(val1))
                if val2.TYPE != u'str':
                    report_error(u'TYPE', u'concat',
                                 u'%s is not a string!' % unicode(val2))
                res = Token(TYPE=u'str', VAL=val1.VAL+val2.VAL)
                data_stack.append(res)
            elif op == u'string':
                try:
                    val = data_stack.pop()
                except IndexError:
                    report_error(u'DATA_STACK', u'string',
                                 u'There are not enough values to pop.')
                res = Token(TYPE=u'str', VAL=unicode(val1.VAL))
                data_stack.append(res)
            elif op == u'letterof':
                try:
                    val2, val1 = data_stack.pop(), data_stack.pop()
                except IndexError:
                    report_error(u'DATA_STACK', u'letterof',
                                 u'There are not enough values to pop.')
                if val1.TYPE != u'num':
                    report_error(u'TYPE', u'letterof',
                                 u'%s is not a number!' % unicode(val1))
                if val2.TYPE != u'str':
                    report_error(u'TYPE', u'letterof',
                                 u'%s is not a string!' % unicode(val2))
                res = Token(TYPE=u'str', VAL=val2.VAL[val1.VAL])
                data_stack.append(res)
            #IO ops
            elif op == u'print':
                try:
                    val = data_stack.pop()
                except IndexError:
                    report_error(u'DATA_STACK', u'string',
                                 u'There are not enough values to pop.')
                print val.VAL
            elif op == u'input':
                try:
                    val = data_stack.pop()
                except IndexError:
                    report_error(u'DATA_STACK', u'input',
                                 u'There are not enough values to pop.')
                res = raw_input(val.VAL)
                res = Token(TYPE=u'str', VAL = res)
                data_stack.append(res)
            #Data stack ops
            elif op == u'pop':
                try:
                    val = data_stack.pop()
                except IndexError:
                    report_error(u'DATA_STACK', u'pop',
                                 u'There are not enough values to pop.')
            elif op == u'dup':
                try:
                    res = data_stack.pop()
                except IndexError:
                    report_error(u'DATA_STACK', u'pop',
                                 u'There are not enough values to pop.')
                data_stack.append(res)
                data_stack.append(res)

            elif op == u'dumpstack':
                print u'***DATA STACK DUMP***'
                for i, tok in enumerate(data_stack):
                    print u'Item %s: %s' % (i, tok)
            #Bool ops
            elif op == u'or':
                try:
                    val2, val1 = data_stack.pop(), data_stack.pop()
                except IndexError:
                    report_error(u'DATA_STACK', u'or',
                                 u'There are not enough values to pop.')
                if val1.TYPE != u'bool':
                    report_error(u'TYPE', u'or',
                                 u'%s is not a bool!' % unicode(val1))
                if val2.TYPE != u'bool':
                    report_error(u'TYPE', u'or',
                                 u'%s is not a bool!' % unicode(val2))
                res = Token(TYPE=u'bool', VAL=(val1.VAL or val2.VAL))
                data_stack.append(res)
            elif op == u'and':
                try:
                    val2, val1 = data_stack.pop(), data_stack.pop()
                except IndexError:
                    report_error(u'DATA_STACK', u'and',
                                 u'There are not enough values to pop.')
                if val1.TYPE != u'bool':
                    report_error(u'TYPE', u'and',
                                 u'%s is not a bool!' % unicode(val1))
                if val2.TYPE != u'bool':
                    report_error(u'TYPE', u'and',
                                 u'%s is not a bool!' % unicode(val2))
                res = Token(TYPE=u'bool', VAL=(val1.VAL and val2.VAL))
                data_stack.append(res)
            elif op == u'not':
                try:
                    val1 = data_stack.pop()
                except IndexError:
                    report_error(u'DATA_STACK', u'not',
                                 u'There are not enough values to pop.')
                if val1.TYPE != u'bool':
                    report_error(u'TYPE', u'not',
                                 u'%s is not a bool!' % unicode(val1))
                res = Token(TYPE=u'bool', VAL=(not val1.VAL))
                data_stack.append(res)
            elif op == u'=':
                try:
                    val2, val1 = data_stack.pop(), data_stack.pop()
                except IndexError:
                    report_error(u'DATA_STACK', u'=',
                                 u'There are not enough values to pop.')
                res = Token(TYPE=u'bool', VAL=((val1.TYPE == val2.TYPE) and (val1.VAL == val2.VAL)))
                data_stack.append(res)
            elif op == u'!=':
                try:
                    val2, val1 = data_stack.pop(), data_stack.pop()
                except IndexError:
                    report_error(u'DATA_STACK', u'!!=',
                                 u'There are not enough values to pop.')
                res = Token(TYPE=u'bool', VAL=((val1.TYPE != val2.TYPE) or (val1.VAL != val2.VAL)))
                data_stack.append(res)
            #List ops
            elif op == u'lnth':
                try:
                    val2, val1 = data_stack.pop(), data_stack.pop()
                except IndexError:
                    report_error(u'DATA_STACK', u'lnth',
                                 u'There are not enough values to pop.')
                if val1.TYPE != u'list':
                    report_error(u'TYPE', u'lnth',
                                 u'%s is not a list!' % unicode(val1))
                if val2.TYPE != u'num':
                    report_error(u'TYPE', u'lnth',
                                 u'%s is not a number!' % unicode(val2))
                data_stack.append(val1.VAL[int(val2.VAL)])
            elif op == u'lappend':
                try:
                    val2, val1 = data_stack.pop(), data_stack.pop()
                except IndexError:
                    report_error(u'DATA_STACK', u'lappend',
                                 u'There are not enough values to pop.')
                if val1.TYPE != u'list':
                    report_error(u'TYPE', u'lappend',
                                 u'%s is not a list!' % unicode(val1))
                val1.VAL.append(val2)
                data_stack.append(val1)
            elif op == u'llen':
                try:
                    val1 = data_stack.pop()
                except IndexError:
                    report_error(u'DATA_STACK', u'llen',
                                 u'There are not enough values to pop.')
                if val1.TYPE != u'list':
                    report_error(u'TYPE', u'llen',
                                 u'%s is not a list!' % unicode(val1))
                data_stack.append(Token(TYPE=u'num',VAL=len(val1.VAL)))
            elif op == u'lslice':
                try:
                    val3, val2, val1 = data_stack.pop(), data_stack.pop(),data_stack.pop()
                except IndexError:
                    report_error(u'DATA_STACK', u'lslice',
                                 u'There are not enough values to pop.')
                if val1.TYPE != u'list':
                    report_error(u'TYPE', u'lslice',
                                 u'%s is not a list!' % unicode(val1))
                if val2.TYPE != u'num':
                    report_error(u'TYPE', u'lslice',
                                 u'%s is not a number!' % unicode(val2))
                if val3.TYPE != u'num':
                    report_error(u'TYPE', u'lslice',
                                 u'%s is not a number!' % unicode(val3))
                data_stack.append(Token(TYPE=u'list',VAL=val1.VAL[int(val2.VAL):int(val3.VAL)]))
            elif op == u'lin':
                try:
                    val2, val1 = data_stack.pop(), data_stack.pop()
                except IndexError:
                    report_error(u'DATA_STACK', u'lin',
                                 u'There are not enough values to pop.')
                if val1.TYPE != u'list':
                    report_error(u'TYPE', u'lin',
                                 u'%s is not a list!' % unicode(val1))
                data_stack.append(Token(TYPE=u'bool', VAL=val2 in val1.VAL))
            elif op == u'linsert':
                try:
                    val3, val2, val1 = data_stack.pop(), data_stack.pop(),data_stack.pop()
                except IndexError:
                    report_error(u'DATA_STACK', u'linsert',
                                 u'There are not enough values to pop.')
                if val1.TYPE != u'list':
                    report_error(u'TYPE', u'linsert',
                                 u'%s is not a list!' % unicode(val1))
                if val2.TYPE != u'num':
                    report_error(u'TYPE', u'linsert',
                                 u'%s is not a number!' % unicode(val2))
                val1.VAL.insert(int(val3.VAL),val2)
                data_stack.append(val1)
            elif op == u'lindex':
                try:
                    val2, val1 = data_stack.pop(), data_stack.pop()
                except IndexError:
                    report_error(u'DATA_STACK', u'lindex',
                                 u'There are not enough values to pop.')
                if val1.TYPE != u'list':
                    report_error(u'TYPE', u'lindex',
                                 u'%s is not a list!' % unicode(val1))
                try:
                    n = val1.VAL.index(val2)
                except ValueError:
                    n = -1
                data_stack.append(Token(TYPE=u'num', VAL = n))
            elif op == u'lreverse':
                try:
                    val1 =  data_stack.pop()
                except IndexError:
                    report_error(u'DATA_STACK', u'lreverse',
                                 u'There are not enough values to pop.')
                if val1.TYPE != u'list':
                    report_error(u'TYPE', u'lreverse',
                                 u'%s is not a list!' % unicode(val1))
                val1.VAL.reverse()
                data_stack.append(val1)
            elif op == u'lclear':
                try:
                    val1 =  data_stack.pop()
                except IndexError:
                    report_error(u'DATA_STACK', u'lclear',
                                 u'There are not enough values to pop.')
                if val1.TYPE != u'list':
                    report_error(u'TYPE', u'lclear',
                                 u'%s is not a list!' % unicode(val1))
                val1.VAL.clear()
                data_stack.append(val1)
            elif op == u'lpop':
                 try:
                    val1 =  data_stack.pop()
                 except IndexError:
                    report_error(u'DATA_STACK', u'lpop',
                                 u'There are not enough values to pop.')
                 if val1.TYPE != u'list':
                    report_error(u'TYPE', u'lpop',
                                 u'%s is not a list!' % unicode(val1))
                 try:
                  v = val1.VAL.pop()
                 except IndexError:
                    report_error(u'LIST_ERROR', u'lpop',
                                 u'List is empty!')
                 else:
                    data_stack.append(v)
            elif op == u'lpopn':
                try:
                    val2, val1 =  data_stack.pop(), data_stack.pop()
                except IndexError:
                    report_error(u'DATA_STACK', u'lpopn',
                                 u'There are not enough values to pop.')
                if val1.TYPE != u'list':
                    report_error(u'TYPE', u'lpopn',
                                 u'%s is not a list!' % unicode(val1))
                if val2.TYPE != u'num':
                    report_error(u'TYPE', u'lpopn',
                        u'%s is not a number!' % unicode(val2))
                try:
                  v = val1.VAL.pop(int(val2.VAL))
                except IndexError:
                    report_error(u'LIST_ERROR', u'lpopn',
                                 u'List is empty!')
                else:
                    data_stack.append(v)
            elif op == u'ldeln':
                try:
                    val2, val1 =  data_stack.pop(), data_stack.pop()
                except IndexError:
                    report_error(u'DATA_STACK', u'ldeln',
                                 u'There are not enough values to pop.')
                if val1.TYPE != u'list':
                    report_error(u'TYPE', u'ldeln',
                                 u'%s is not a list!' % unicode(val1))
                if val2.TYPE != u'num':
                    report_error(u'TYPE', u'ldeln',
                        u'%s is not a number!' % unicode(val2))
                del val1.VAL[int(val2.VAL)]
                data_stack.append(val1)
            elif op == u'lreplace':
                try:
                    val3, val2, val1 = data_stack.pop(), data_stack.pop(),data_stack.pop()
                except IndexError:
                    report_error(u'DATA_STACK', u'lreplace',
                                 u'There are not enough values to pop.')
                if val1.TYPE != u'list':
                    report_error(u'TYPE', u'lreplace',
                                 u'%s is not a list!' % unicode(val1))
                if val2.TYPE != u'num':
                    report_error(u'TYPE', u'lreplace',
                                 u'%s is not a number!' % unicode(val2))
                val1.VAL[int(val2.VAL)] = val3
                data_stack.append(val1)
            #Scope and variable ops
            elif op == u'push_scope':
                scopes.append({u'user-words':{}})
            elif op == u'dump_scope':
                print scopes
            elif op == u'pop_scope':
                if len(scopes) < 2:
                    report_error(u'SCOPE_UNDERFLOW', u'pop_scope',
                                 u'You can not pop the global scope!')
                else:
                    scopes.pop()
            elif op == u'set':
                try:
                    val2, val1 = data_stack.pop(), data_stack.pop()
                except IndexError:
                    report_error(u'DATA_STACK', u'set',
                                 u'There are not enough values to pop.')
                if val2.TYPE != u'name':
                    report_error(u'TYPE', u'set',
                                 u'%s is not a name!' % unicode(val2))
                else:
                    scopes[-1][u'var_' + val2.VAL] = val1
            elif op == u'get':
                try:
                    val1 = data_stack.pop()
                except IndexError:
                    report_error(u'DATA_STACK', u'get',
                                 u'There are not enough values to pop.')
                if val1.TYPE != u'name':
                    report_error(u'TYPE', u'get',
                                 u'%s is not a name!' % unicode(val1))
                #Find the var
                for i in xrange(len(scopes) - 1, -1, -1):
                    if (u'var_' + val1.VAL) in scopes[i]:
                        data_stack.append(scopes[i][u'var_' + val1.VAL])
                        break
                else:
                    report_error(u'VARAIBLE_ERROR', u'get',
                                 u'The variable %s does not exist!' % val1.VAL)
            elif op == u'del':
                try:
                    val1 = data_stack.pop()
                except IndexError:
                    report_error(u'DATA_STACK', u'del',
                                 u'There are not enough values to pop.')
                if val1.TYPE != u'name':
                    report_error(u'TYPE', u'del',
                                 u'%s is not a name!' % unicode(val1))
                try:
                    del scopes[-1][u'var_' + val1.VAL]
                except KeyError:
                    report_error(u'VARAIBLE_ERROR', u'del',
                                 u'%s is not a variable!' % val1.VAL)
            #Misc ops
            elif op == u'wait':
                try:
                    val1 = data_stack.pop()
                except IndexError:
                    report_error(u'DATA_STACK', u'wait',
                                 u'There are not enough values to pop.')
                if val1.TYPE != u'num':
                    report_error(u'TYPE', u'wait',
                                 u'%s is not a number!' % unicode(val1))
                time.sleep(val1.VAL)

            elif op == u'reverse':
                try:
                    val1 = data_stack.pop()
                except IndexError:
                    report_error(u'DATA_STACK', u'reverse',
                                 u'There are not enough values to pop.')
                if val1.TYPE not in ( u'list',u'str'):
                    report_error(u'TYPE', u'reverse',
                                 u'%s is not a string or a list!' % unicode(val1))
                res = Token(TYPE=val1.TYPE,VAL=val1.VAL[::-1])
                data_stack.append(res)
            #Control flow ops
            elif op == u'if':
                try:
                    val1, val2 = data_stack.pop(), data_stack.pop()
                except IndexError:
                    report_error(u'DATA_STACK', u'if',
                                 u'There are not enough values to pop.')
                if val1.TYPE != u'code':
                    report_error(u'TYPE', u'if',
                                 u'%s is not a code block!' % unicode(val1))
                if val2.TYPE != u'bool':
                    report_error(u'TYPE', u'if',
                                 u'%s is not a bool!' % unicode(val1))
                if val2.VAL:
                    token_stream[i+1:i+1] = val1.VAL

            elif op == u'ifelse':
                try:
                    val1, val2, val3 = data_stack.pop(), data_stack.pop(),data_stack.pop()
                except IndexError:
                    report_error(u'DATA_STACK', u'ifelse',
                                 u'There are not enough values to pop.')
                #print(val3,val2,val1)
                if val1.TYPE != u'code':
                    report_error(u'TYPE', u'ifelse',
                                 u'%s is not a code block!' % unicode(val1))
                if val2.TYPE != u'code':
                    report_error(u'TYPE', u'ifelse',
                                 u'%s is not a code block!' % unicode(val1))
                if val3.TYPE != u'bool':
                    report_error(u'TYPE', u'ifelse',
                                 u'%s is not a bool!' % unicode(val1))
                if val3.VAL:
                    token_stream[i+1:i+1] = val2.VAL
                else:
                    token_stream[i+1:i+1] = val1.VAL

            #User word ops
            elif op == u'def':
                try:
                    val2, val1 = data_stack.pop(), data_stack.pop()
                except IndexError:
                    report_error(u'DATA_STACK', u'def',
                                 u'There are not enough values to pop.')
                if val1.TYPE != u'code':
                    report_error(u'TYPE', u'def',
                                 u'%s is not a code block!' % unicode(val1))
                if val2.TYPE != u'name':
                    report_error(u'TYPE', u'def',
                                 u'%s is not a name!' % unicode(val1))
                scopes[-1][u'user-words'][u'word_' + val2.VAL] = val1
            elif op == u'call':
                try:
                    val1 = data_stack.pop()
                except IndexError:
                    report_error(u'DATA_STACK', u'call',
                                 u'There are not enough values to pop.')
                if val1.TYPE == u'code':
                    token_stream[i+1:i+1] = val1.VAL
                elif val1.TYPE == u'name' and u'word_' + val1.VAL in scopes[-1][u'user-words']:
                    token_stream[i+1:i+1] = scopes[-1][u'user-words'][u'word_' + val1.VAL].VAL
                else:
                    report_error(u'WORD_ERROR', u'call',
                                 u'%s is not a callable object!' % unicode(val1))
def interpet(prog):
    tok_stream = stack.stack_parser.parse(prog)
    return _stream_interpet(tok_stream)
