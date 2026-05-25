from lib.tokens import (
    INTEGER, IDENTIFIER,
    PRINT, READ, IMPORT, IF, ELSE, LOOP, SWITCH, BREAK, END,
    PLUS, MINUS, STAR, SLASH,
    AMPERSAND_AMPERSAND, PIPE_PIPE, BANG,
    TILDE_EQUALS, EQUALS_TILDE, TILDE_LESS, GREATER_TILDE, TILDE_MINUS,
    EQUALS, COLON_EQUALS, COLON_EQUALS_QUESTION,
    LPAREN, RPAREN, STRING, DOT, EOF,
)

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
        if tok.kind == IF:
            return self.parse_if()
        if tok.kind == ELSE:
            return self.parse_else()
        if tok.kind == LOOP:
            return self.parse_loop()
        if tok.kind == SWITCH:
            return self.parse_switch()
        if tok.kind == BREAK:
            return self.parse_break()
        if tok.kind == PRINT:
            return self.parse_print()
        if tok.kind == READ:
            return self.parse_read()
        if tok.kind == IMPORT:
            return self.parse_import()
        if tok.kind == END:
            return None
        if tok.kind == IDENTIFIER:
            return self.parse_assign()
        raise SyntaxError(f"Unexpected token: {tok.kind}({tok.value})")

    def parse_if(self):
        self.consume(IF)
        expr = self.parse_expr()
        body = self.parse_body()
        if self.peek().kind == END:
            self.consume(END)
        return If(expr, body)

    def parse_else(self):
        self.consume(ELSE)
        expr = self.parse_expr()
        body = self.parse_body()
        if self.peek().kind == END:
            self.consume(END)
        return Else(expr, body)

    def parse_body(self):
        body = []
        while self.peek().kind not in (END, EOF):
            stmt = self.parse_stmt()
            if stmt is None:
                break
            body.append(stmt)
        return body

    def parse_loop(self):
        self.consume(LOOP)
        count = self.parse_expr()
        body = self.parse_body()
        if self.peek().kind == END:
            self.consume(END)
        return Loop(count, body)

    def parse_switch(self):
        self.consume(SWITCH)
        expr = self.parse_expr()
        body = self.parse_body()
        if self.peek().kind == END:
            self.consume(END)
        return Switch(expr, body)

    def parse_break(self):
        self.consume(BREAK)
        expr = self.parse_expr()
        body = self.parse_body()
        if self.peek().kind == END:
            self.consume(END)
        return Break(expr, body)

    def parse_print(self):
        self.consume(PRINT)
        self.consume(LPAREN)
        expr = self.parse_expr()
        self.consume(RPAREN)
        return Print(expr)

    def parse_read(self):
        return self.parse_read_expr()

    def parse_import(self):
        self.consume(IMPORT)
        name_tok = self.consume(IDENTIFIER)
        parts = [name_tok.value]
        while self.peek().kind == DOT:
            self.consume(DOT)
            part = self.consume(IDENTIFIER)
            parts.append(part.value)
        args = []
        while self.peek().kind == INTEGER:
            tok = self.consume(INTEGER)
            args.append(tok.value)
        return Import(".".join(parts), args)

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
        while self.peek().kind in (TILDE_EQUALS, EQUALS_TILDE, TILDE_LESS, GREATER_TILDE):
            op = self.consume().kind
            right = self.parse_logical()
            op_str = {
                TILDE_EQUALS: "~=",
                EQUALS_TILDE: "=~",
                TILDE_LESS: "][",
                GREATER_TILDE: "[]",
            }[op]
            left = BinOp(op_str, left, right)
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
        while self.peek().kind in (PLUS, MINUS, TILDE_MINUS):
            op = self.consume().kind
            if op == PLUS:
                op_str = "+"
            elif op == MINUS:
                op_str = "-"
            else:
                op_str = "~-"
            right = self.parse_multiplicative()
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
            return UnaryOp(">", operand)
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
        if tok.kind == STRING:
            self.consume(STRING)
            return String(tok.value)
        if tok.kind == IDENTIFIER:
            self.consume(IDENTIFIER)
            return Variable(tok.value)
        if tok.kind == READ:
            return self.parse_read_expr()
        if tok.kind == LPAREN:
            self.consume(LPAREN)
            expr = self.parse_expr()
            self.consume(RPAREN)
            return expr
        raise SyntaxError(f"Unexpected token: {tok.kind}({tok.value})")

    def parse_read_expr(self):
        self.consume(READ)
        self.consume(LPAREN)
        prompt = None
        if self.peek().kind == STRING:
            tok = self.consume(STRING)
            prompt = tok.value
        self.consume(RPAREN)
        return Read(prompt)
