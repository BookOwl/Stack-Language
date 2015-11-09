import math


def ceil(interpeter, stack, scopes, stream):
    val1 = stack.pop()
    val = math.ceil(val1.VAL)
    tok = interpeter.Token(TYPE="num", VAL=val)
    stack.append(tok)


module = {
    "ceil": ceil
}
