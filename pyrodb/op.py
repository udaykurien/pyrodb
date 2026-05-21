import operator

class Op:
    def __init__ (self, op_function, value):
        self.op_function = op_function
        self.value = value

def eq(value):
    return Op(operator.eq, value)
def gt(value):
    return Op(operator.gt, value)
def lt(value):
    return Op(operator.lt, value)
def gte(value):
    return Op(operator.ge, value)
def lte(value):
    return Op(operator.le, value)
def ne(value):
    return Op(operator.ne, value)
def startswith(value):
    return Op(str.startswith, value)
def endswith(value):
    return Op(str.endswith, value)
