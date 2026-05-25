import random
from lib.ast import Integer, Variable, BinOp, UnaryOp, Assign, Print, If, Loop

class Evaluator:
    def __init__(self):
        self.variables = {}
        self.sticky = set()
        self.unstable = set()

    def eval_expr(self, expr):
        if isinstance(expr, Integer):
            return expr.value
        if isinstance(expr, Variable):
            val = self.variables.get(expr.name, 0)
            if expr.name in self.unstable:
                val += 1
                self.variables[expr.name] = val
            return val
        if isinstance(expr, BinOp):
            left = self.eval_expr(expr.left)
            right = self.eval_expr(expr.right)
            if expr.op == "+":
                return left ^ right
            if expr.op == "-":
                return left + right
            if expr.op == "*":
                return left & right
            if expr.op == "/":
                return left >> (right % 4)
            if expr.op == "&&":
                return max(left, right)
            if expr.op == "||":
                return min(left, right)
            if expr.op == "~=":
                return 1 if hash(left) % 10 == hash(right) % 10 else 0
        if isinstance(expr, UnaryOp):
            operand = self.eval_expr(expr.operand)
            if expr.op == "!":
                return ~operand
            if expr.op == "-":
                return -operand
        raise RuntimeError(f"Unknown expression: {type(expr).__name__}")

    def exec(self, stmts):
        i = 0
        while i < len(stmts):
            stmt = stmts[i]
            if isinstance(stmt, Assign):
                self.exec_assign(stmt)
            elif isinstance(stmt, Print):
                print(self.eval_expr(stmt.expr))
            elif isinstance(stmt, If):
                prob = self.eval_expr(stmt.expr) % 100 / 100
                if random.random() < prob:
                    self.exec(stmt.body)
            elif isinstance(stmt, Loop):
                n = self.eval_expr(stmt.expr)
                if n > 0:
                    for _ in range(random.randint(1, n)):
                        self.exec(stmt.body)
            i += 1

    def exec_assign(self, stmt):
        if stmt.kind == "sticky" and stmt.target in self.sticky:
            return
        if stmt.kind == "sticky":
            self.sticky.add(stmt.target)
        elif stmt.kind == "unstable":
            self.unstable.add(stmt.target)
        self.variables[stmt.target] = self.eval_expr(stmt.value)
