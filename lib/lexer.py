from lib.tokens import (
    Token,
    INTEGER, IDENTIFIER,
    PRINT, IMPORT,
    PLUS, MINUS, STAR, SLASH,
    AMPERSAND_AMPERSAND, PIPE_PIPE, BANG,
    TILDE_EQUALS, EQUALS_TILDE, TILDE_LESS, GREATER_TILDE, TILDE_MINUS,
    EQUALS, COLON_EQUALS, COLON_EQUALS_QUESTION,
    LPAREN, RPAREN, STRING, DOT, EOF,
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
        if ch == "~" and i + 1 < len(source):
            if source[i + 1] == "=":
                tokens.append(Token(TILDE_EQUALS))
                i += 2
                continue
            if source[i + 1] == "<":
                tokens.append(Token(TILDE_LESS))
                i += 2
                continue
            if source[i + 1] == "-":
                tokens.append(Token(TILDE_MINUS))
                i += 2
                continue
        if ch == ">" and i + 1 < len(source) and source[i + 1] == "~":
            tokens.append(Token(GREATER_TILDE))
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
        if ch == "=" and i + 1 < len(source) and source[i + 1] == "~":
            tokens.append(Token(EQUALS_TILDE))
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
        if ch == ">":
            tokens.append(Token(BANG))
            i += 1
            continue
        if ch == ".":
            tokens.append(Token(DOT))
            i += 1
            continue
        if ch == "'":
            i += 1
            j = i
            while j < len(source) and source[j] != "'":
                j += 1
            if j >= len(source):
                raise SyntaxError("Unterminated string literal")
            tokens.append(Token(STRING, source[i:j]))
            i = j + 1
            continue
        if ch == "]" and i + 1 < len(source) and source[i + 1] == "[":
            tokens.append(Token(TILDE_LESS))
            i += 2
            continue
        if ch == "[" and i + 1 < len(source) and source[i + 1] == "]":
            tokens.append(Token(GREATER_TILDE))
            i += 2
            continue
        raise SyntaxError(f"Unexpected character: {ch!r}")
    tokens.append(Token(EOF))
    return tokens
