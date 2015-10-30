BUILTIN_OPS = (
    #Math ops
    u'+',
    u'-',
    u'*',
    u'/',
    u'num',
    u'BAND',
    u'BOR',
    u'BXOR',
    u'BNOT',
    #String ops
    u'concat',
    u'string',
    u'letterof',
    #IO ops
    u'print',
    u'input',
    #Stack ops
    u'pop',
    u'dup',
    u'dumpstack',
    #Bool ops
    u'or',
    u'and',
    u'=',
    u'!=',
    u'not',
    #List ops
    u'lnth',
    u'lappend',
    u'lslice',
    u'llen',
    u'lin',
    u'linsert',
    u'lindex',
    u'lreverse',
    u'lclear',
    u'lpop',
    u'lpopn',
    u'ldeln',
    u'lreplace',
    #Variable ops
    u'set',
    u'get',
    u'del',
    #Control flow
   # 'while',
    u'if',
    u'ifelse',
    #Word Definition ops
    u'def',
    u'call',
    #Scope ops
    u'push_scope',
    u'pop_scope',
    u'dump_scope',
    #Misc ops
    u'wait',
    u'reverse',
    )

DATA_TYPES = (
    u'str',
    u'num',
    u'bool',
    u'list',
    u'name',
    u'code'
    )
BLOCK_START = u'{'
BLOCK_END   = u'}'
BLOCKS = (BLOCK_START, BLOCK_END)

LIST_START = u'['
LIST_END   = u']'
LISTS = (LIST_START, LIST_END)


def is_op(op):
    return op in BUILTIN_OPS
def is_str(val):
    try:
        return val[0] == u"'" and val[-1] == u"'"
    except (IndexError,TypeError):
        return False
def is_num(val):
    try:
        return type(float(val)) == float
    except ValueError:
        return False
def is_bool(val):
    return val in (u'True',u'False')
def is_list(val):
    return val in (u'[]',u'list')
def is_name(val):
    return  val[0] == u'`'
##    return \
##           val not in BUILTIN_OPS and\
##           val not in BLOCKS and\
##           val not in LISTS and\
##           not is_str(val) and\
##           not is_num(val) and\
##           not is_bool(val)
def is_var(val):
        return \
           val not in BUILTIN_OPS and\
           val not in BLOCKS and\
           val not in LISTS and\
           not is_str(val) and\
           not is_num(val) and\
           not is_bool(val) and\
           not is_name(val)
