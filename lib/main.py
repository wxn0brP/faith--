from lib.lexer import tokenize
from lib.parser import Parser
from lib.evaluator import Evaluator

def execute(code):
    tokens = tokenize(code)
    parser = Parser(tokens)
    stmts = parser.parse_program()
    evaluator = Evaluator()
    evaluator.exec(stmts)
