import os
import readline # for arrow keys support
from lib.lexer import tokenize
from lib.parser import Parser
from lib.evaluator import Evaluator
from lib.ast import Assign

def repl():
    evaluator = Evaluator(os.getcwd())
    print("Faith-- REPL - 'Trust the syntax, not the meaning.'")
    print("Type '.exit' or Ctrl+D to quit.")

    while True:
        try:
            line = input("faith> ")
        except EOFError:
            print()
            break
        except KeyboardInterrupt:
            print()
            continue

        text = line.strip()
        if not text:
            continue
        if text == ".exit":
            break

        lines = [line]
        opens = text.count("if ") + text.count("loop ") + text.count("switch ")
        opens += text.count("else")
        closes = text.count("end")

        while opens > closes:
            try:
                extra = input("  ... ")
            except EOFError:
                print()
                return
            except KeyboardInterrupt:
                print()
                break

            extra_stripped = extra.strip()
            if not extra_stripped or extra_stripped == ".exit":
                break

            lines.append(extra)
            combined = "\n".join(lines)
            opens = combined.count("if ") + combined.count("loop ") + combined.count("switch ")
            opens += combined.count("else")
            closes = combined.count("end")

        code = "\n".join(lines)
        try:
            tokens = tokenize(code)
            parser = Parser(tokens)
            stmts = parser.parse_program()
            evaluator.exec(stmts)
            if stmts and isinstance(stmts[-1], Assign):
                print(evaluator.variables.get(stmts[-1].target, 0))
        except SyntaxError as e:
            print(f"SyntaxError: {e}")
        except RuntimeError as e:
            print(f"RuntimeError: {e}")
