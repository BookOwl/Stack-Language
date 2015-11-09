import types


def mapobj(interpeter, stack, scopes, stream):
    val1 = stack.pop()
    obj = {}
    for item in val1.VAL:
        key = item.VAL[0].VAL
        val = item.VAL[1].VAL
        obj[key] = val
    tok = interpeter.Token(TYPE="py-obj", VAL=obj)
    stack.append(tok)


def newobj(interpeter, stack, scopes, stream):
    tok = interpeter.Token(TYPE="py-obj", VAL={})
    stack.append(tok)


def prop(interpeter, stack, scopes, stream):
    val2, _val1 = stack.pop().VAL, stack.pop()

    val1 = _val1.VAL

    if ("var_oop_markers" in scopes[-1].keys()):
        scopes[-1]["var_oop_markers"].VAL.append((
            "GET", val2, "OF", interpeter.tok_overview(_val1), ))

    if isinstance(val1, dict):
        if not val2 in val1.keys():
            interpeter.report_error(
                "OOP_ERROR",
                "propof",
                "Property not in object!")
    elif "__all__" in dir(val1):
        if not val2 in val1.__all__:
            interpeter.report_error(
                "OOP_ERROR",
                "propof",
                "Property not in object!")
    elif not val2 in dir(val1):
        interpeter.report_error(
            "OOP_ERROR",
            "propof",
            "Property not in object!")

    if isinstance(val1, types.ModuleType):
        value = val1.__dict__[val2]
    else:
        value = val1[val2]

    tok_type = "ha"
    if isinstance(value, str):
        tok_type = "str"
    elif isinstance(value, float) or isinstance(value, int):
        tok_type = "num"
    elif isinstance(value, bool):
        tok_type = "bool"
    elif (
        isinstance(value, interpeter.stack_parser.Token) or
        isinstance(value, interpeter.Token)
    ):
        stack.append(value)
        return
    tok = interpeter.Token(TYPE=tok_type, VAL=value)
    stack.append(tok)


def setprop(interpeter, stack, scopes, stream):
    val3 = stack.pop()
    val2 = stack.pop().VAL
    val1 = stack.pop()
    val1.VAL[val2] = val3
    stack.append(val1)


def popsetprop(interpeter, stack, scopes, stream):
    # Like setprop, but without re-appending the object to the stack.
    # Useful for if you're using variables.
    val3 = stack.pop()
    val2 = stack.pop().VAL
    val1 = stack.pop()
    val1.VAL[val2] = val3


module = {
    "newobj": newobj,
    "mapobj": mapobj,
    "prop": prop,
    "setprop": setprop,
    "popsetprop": popsetprop
}
