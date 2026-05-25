class Integer:
    def __init__(self, value):
        self.value = value


class String:
    def __init__(self, value):
        self.value = value


class Variable:
    def __init__(self, name):
        self.name = name


class BinOp:
    def __init__(self, op, left, right):
        self.op = op
        self.left = left
        self.right = right


class UnaryOp:
    def __init__(self, op, operand):
        self.op = op
        self.operand = operand


class Assign:
    def __init__(self, target, value, kind):
        self.target = target
        self.value = value
        self.kind = kind


class Print:
    def __init__(self, expr):
        self.expr = expr


class If:
    def __init__(self, expr, body):
        self.expr = expr
        self.body = body


class Loop:
    def __init__(self, expr, body):
        self.expr = expr
        self.body = body


class Else:
    def __init__(self, expr, body):
        self.expr = expr
        self.body = body


class Switch:
    def __init__(self, expr, body):
        self.expr = expr
        self.body = body


class Break:
    def __init__(self, expr, body):
        self.expr = expr
        self.body = body


class Read:
    def __init__(self, prompt=None):
        self.prompt = prompt


class Import:
    def __init__(self, name, args=None):
        self.name = name
        self.args = args or []
