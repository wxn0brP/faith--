from lib.lexer import tokenize
from lib.parser import Parser
from lib.evaluator import Evaluator

def execute(code, base_dir=None, args=None):
    tokens = tokenize(code)
    parser = Parser(tokens)
    stmts = parser.parse_program()
    evaluator = Evaluator(base_dir)
    if args:
        for i, val in enumerate(args):
            try:
                evaluator.variables[f"arg_{i}"] = int(val)
            except ValueError:
                evaluator.variables[f"arg_{i}"] = 0
    evaluator.exec(stmts)
