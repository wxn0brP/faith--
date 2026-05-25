#!/usr/bin/env python3

import os
import sys
from lib.main import execute

if not sys.stdin.isatty():
    execute(sys.stdin.read())
    sys.exit(0)

if len(sys.argv) >= 2 and sys.argv[1] in ("--repl", "repl"):
    from lib.repl import repl
    repl()
    sys.exit(0)

if len(sys.argv) < 2:
    print("Faith-- + 'Trust the syntax, not the meaning.'")
    print("Without a file, Faith-- has nothing to misread. Here's 47 for free.")
    print("Usage: faith-- <file.faith>")
    print()
    sys.exit(0)

path = sys.argv[1]
if not os.path.exists(path):
    print(f"Lack of faith: '{path}' exists only in your imagination. Even 47 can't save you now.")
    print()
    sys.exit(1)
base_dir = os.path.dirname(os.path.abspath(path))
with open(path) as f:
    execute(f.read(), base_dir, sys.argv[2:])
