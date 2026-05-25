import os
import random
from lib.ast import (
    Integer,
    String,
    Variable,
    BinOp,
    UnaryOp,
    Assign,
    Print,
    Read,
    If,
    Else,
    Loop,
    Switch,
    Break,
    Import
)

class Evaluator:
    def __init__(self, base_dir=None):
        self.variables = {}
        self.sticky = set()
        self.unstable = set()
        self.base_dir = base_dir or os.getcwd()

    def read_int(self, prompt=None):
        if prompt:
            print(prompt, end="")
        try:
            return int(input())
        except (ValueError, EOFError):
            return 0

    def eval_num(self, expr):
        val = self.eval_expr(expr)
        if isinstance(val, str):
            return len(val)
        return val

    def eval_expr(self, expr):
        if isinstance(expr, Integer):
            return expr.value
        if isinstance(expr, String):
            return expr.value
        if isinstance(expr, Read):
            return self.read_int(expr.prompt)
        if isinstance(expr, Variable):
            val = self.variables.get(expr.name, 0)
            if expr.name in self.unstable:
                val += 1
                self.variables[expr.name] = val
            return val
        if isinstance(expr, BinOp):
            if expr.op in ("=~", "][", "[]"):
                left = self.eval_expr(expr.left)
                right = self.eval_expr(expr.right)
                if expr.op == "=~":
                    return 1 if left == right else 0
                if expr.op == "][":
                    return 1 if left < right else 0
                if expr.op == "[]":
                    return 1 if left > right else 0
            left = self.eval_num(expr.left)
            right = self.eval_num(expr.right)
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
            if expr.op == "~-":
                return left - right
        if isinstance(expr, UnaryOp):
            operand = self.eval_num(expr.operand)
            if expr.op == ">":
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
            elif isinstance(stmt, Read):
                self.read_int(stmt.prompt)
            elif isinstance(stmt, If):
                prob = self.eval_num(stmt.expr) % 100 / 100
                if random.random() < prob:
                    self.exec(stmt.body)
            elif isinstance(stmt, Else):
                if self.eval_num(stmt.expr) != 0:
                    self.exec(stmt.body)
            elif isinstance(stmt, Loop):
                n = self.eval_num(stmt.expr)
                if n > 0:
                    for _ in range(random.randint(1, n)):
                        self.exec(stmt.body)
            elif isinstance(stmt, Switch):
                while self.eval_num(stmt.expr) != 0:
                    self.exec(stmt.body)
            elif isinstance(stmt, Break):
                n = self.eval_num(stmt.expr)
                if n > 0:
                    for _ in range(n):
                        self.exec(stmt.body)
            elif isinstance(stmt, Import):
                self.exec_import(stmt)
            i += 1

    def exec_import(self, stmt):
        from lib.lexer import tokenize
        from lib.parser import Parser
        rel_path = stmt.name.replace(".", os.sep) + ".faith"
        path = os.path.join(self.base_dir, rel_path)
        if not os.path.exists(path):
            raise RuntimeError(f"Cannot import '{stmt.name}': file not found")
        with open(path) as f:
            code = f.read()
        tokens = tokenize(code)
        parser = Parser(tokens)
        stmts = parser.parse_program()
        old_base = self.base_dir
        old_fn = {}
        for k in list(self.variables):
            if k.startswith("fn_"):
                old_fn[k] = self.variables.pop(k)
        for i, val in enumerate(stmt.args):
            self.variables[f"fn_{i}"] = val
        self.base_dir = os.path.dirname(os.path.abspath(path))
        self.exec(stmts)
        for k in list(self.variables):
            if k.startswith("fn_"):
                del self.variables[k]
        self.variables.update(old_fn)
        self.base_dir = old_base

    def exec_assign(self, stmt):
        if stmt.kind == "sticky" and stmt.target in self.sticky:
            return
        if stmt.kind == "sticky":
            self.sticky.add(stmt.target)
        elif stmt.kind == "unstable":
            self.unstable.add(stmt.target)
        self.variables[stmt.target] = self.eval_expr(stmt.value)
