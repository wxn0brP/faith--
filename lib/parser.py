from lib.tokens import (
    INTEGER, IDENTIFIER, IF_TILDE, LOOP_QUESTION,
    PRINT, END,
    PLUS, MINUS, STAR, SLASH,
    AMPERSAND_AMPERSAND, PIPE_PIPE, BANG, TILDE_EQUALS,
    EQUALS, COLON_EQUALS, COLON_EQUALS_QUESTION,
    LPAREN, RPAREN, EOF,
)

from lib.ast import Integer, Variable, BinOp, UnaryOp, Assign, Print, If, Loop

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    def peek(self):
        return self.tokens[self.pos]

    def consume(self, kind=None):
        tok = self.peek()
        if kind is not None and tok.kind != kind:
            raise SyntaxError(f"Expected {kind}, got {tok.kind}({tok.value})")
        self.pos += 1
        return tok

    def parse_program(self):
        stmts = []
        while self.peek().kind != EOF:
            stmt = self.parse_stmt()
            if stmt is not None:
                stmts.append(stmt)
        return stmts

    def parse_stmt(self):
        tok = self.peek()
        if tok.kind == IF_TILDE:
            return self.parse_if()
        if tok.kind == LOOP_QUESTION:
            return self.parse_loop()
        if tok.kind == PRINT:
            return self.parse_print()
        if tok.kind == END:
            return None
        if tok.kind == IDENTIFIER:
            return self.parse_assign()
        raise SyntaxError(f"Unexpected token: {tok.kind}({tok.value})")

    def parse_if(self):
        self.consume(IF_TILDE)
        condition = self.parse_expr()
        body = []
        while self.peek().kind not in (END, EOF):
            stmt = self.parse_stmt()
            if stmt is None:
                break
            body.append(stmt)
        if self.peek().kind == END:
            self.consume(END)
        return If(condition, body)

    def parse_loop(self):
        self.consume(LOOP_QUESTION)
        count = self.parse_expr()
        body = []
        while self.peek().kind not in (END, EOF):
            stmt = self.parse_stmt()
            if stmt is None:
                break
            body.append(stmt)
        if self.peek().kind == END:
            self.consume(END)
        return Loop(count, body)

    def parse_print(self):
        self.consume(PRINT)
        self.consume(LPAREN)
        expr = self.parse_expr()
        self.consume(RPAREN)
        return Print(expr)

    def parse_assign(self):
        name_tok = self.consume(IDENTIFIER)
        name = name_tok.value
        tok = self.peek()
        if tok.kind == EQUALS:
            self.consume(EQUALS)
            kind = "normal"
        elif tok.kind == COLON_EQUALS:
            self.consume(COLON_EQUALS)
            kind = "sticky"
        elif tok.kind == COLON_EQUALS_QUESTION:
            self.consume(COLON_EQUALS_QUESTION)
            kind = "unstable"
        else:
            raise SyntaxError(f"Expected assignment, got {tok.kind}({tok.value})")
        value = self.parse_expr()
        return Assign(name, value, kind)

    def parse_expr(self):
        return self.parse_semantic_drift()

    def parse_semantic_drift(self):
        left = self.parse_logical()
        while self.peek().kind == TILDE_EQUALS:
            self.consume(TILDE_EQUALS)
            right = self.parse_logical()
            left = BinOp("~=", left, right)
        return left

    def parse_logical(self):
        left = self.parse_additive()
        while self.peek().kind in (AMPERSAND_AMPERSAND, PIPE_PIPE):
            op = self.consume().kind
            right = self.parse_additive()
            op_str = "&&" if op == AMPERSAND_AMPERSAND else "||"
            left = BinOp(op_str, left, right)
        return left

    def parse_additive(self):
        left = self.parse_multiplicative()
        while self.peek().kind in (PLUS, MINUS):
            op = self.consume().kind
            right = self.parse_multiplicative()
            op_str = "+" if op == PLUS else "-"
            left = BinOp(op_str, left, right)
        return left

    def parse_multiplicative(self):
        left = self.parse_unary()
        while self.peek().kind in (STAR, SLASH):
            op = self.consume().kind
            right = self.parse_unary()
            op_str = "*" if op == STAR else "/"
            left = BinOp(op_str, left, right)
        return left

    def parse_unary(self):
        if self.peek().kind == BANG:
            self.consume(BANG)
            operand = self.parse_unary()
            return UnaryOp("!", operand)
        if self.peek().kind == MINUS:
            self.consume(MINUS)
            operand = self.parse_unary()
            return UnaryOp("-", operand)
        return self.parse_primary()

    def parse_primary(self):
        tok = self.peek()
        if tok.kind == INTEGER:
            self.consume(INTEGER)
            return Integer(tok.value)
        if tok.kind == IDENTIFIER:
            self.consume(IDENTIFIER)
            return Variable(tok.value)
        if tok.kind == LPAREN:
            self.consume(LPAREN)
            expr = self.parse_expr()
            self.consume(RPAREN)
            return expr
        raise SyntaxError(f"Unexpected token: {tok.kind}({tok.value})")
