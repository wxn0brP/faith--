from lib.tokens import (
    Token,
    INTEGER, IDENTIFIER, IF_TILDE, LOOP_QUESTION,
    PLUS, MINUS, STAR, SLASH,
    AMPERSAND_AMPERSAND, PIPE_PIPE, BANG, TILDE_EQUALS,
    EQUALS, COLON_EQUALS, COLON_EQUALS_QUESTION,
    LPAREN, RPAREN, EOF,
    KEYWORDS,
)

def tokenize(source):
    tokens = []
    i = 0
    while i < len(source):
        ch = source[i]
        if ch in " \t\n\r":
            i += 1
            continue
        if ch == "#":
            while i < len(source) and source[i] != "\n":
                i += 1
            continue
        if ch.isdigit():
            j = i
            while j < len(source) and source[j].isdigit():
                j += 1
            tokens.append(Token(INTEGER, int(source[i:j])))
            i = j
            continue
        if ch == "i" and source[i:i+3] == "if~":
            tokens.append(Token(IF_TILDE))
            i += 3
            continue
        if ch == "l" and source[i:i+5] == "loop?":
            tokens.append(Token(LOOP_QUESTION))
            i += 5
            continue
        if ch.isalpha() or ch == "_":
            j = i
            while j < len(source) and (source[j].isalnum() or source[j] == "_"):
                j += 1
            word = source[i:j]
            kind = KEYWORDS.get(word, IDENTIFIER)
            value = None if kind != IDENTIFIER else word
            tokens.append(Token(kind, value))
            i = j
            continue
        if ch == "(":
            tokens.append(Token(LPAREN))
            i += 1
            continue
        if ch == ")":
            tokens.append(Token(RPAREN))
            i += 1
            continue
        if ch == "~" and i + 1 < len(source) and source[i + 1] == "=":
            tokens.append(Token(TILDE_EQUALS))
            i += 2
            continue
        if ch == "&" and i + 1 < len(source) and source[i + 1] == "&":
            tokens.append(Token(AMPERSAND_AMPERSAND))
            i += 2
            continue
        if ch == "|" and i + 1 < len(source) and source[i + 1] == "|":
            tokens.append(Token(PIPE_PIPE))
            i += 2
            continue
        if ch == "=" and i + 1 < len(source) and source[i + 1] == ":":
            if i + 2 < len(source) and source[i + 2] == "?":
                tokens.append(Token(COLON_EQUALS_QUESTION))
                i += 3
            else:
                tokens.append(Token(COLON_EQUALS))
                i += 2
            continue
        if ch == "=":
            tokens.append(Token(EQUALS))
            i += 1
            continue
        if ch == "+":
            tokens.append(Token(PLUS))
            i += 1
            continue
        if ch == "-":
            tokens.append(Token(MINUS))
            i += 1
            continue
        if ch == "*":
            tokens.append(Token(STAR))
            i += 1
            continue
        if ch == "/":
            tokens.append(Token(SLASH))
            i += 1
            continue
        if ch == "!":
            tokens.append(Token(BANG))
            i += 1
            continue
        raise SyntaxError(f"Unexpected character: {ch!r}")
    tokens.append(Token(EOF))
    return tokens
