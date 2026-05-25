#!/usr/bin/env python3

import os
import sys
from lib.main import execute

if len(sys.argv) < 2:
    print("Faith-- + 'Trust the syntax, not the meaning.'")
    print("Without a file, Faith-- has nothing to misread. Here's 47 for free.")
    print("Usage: faith-- <file.faith>")
    sys.exit(1)

path = sys.argv[1]

if not os.path.exists(path):
    print(f"Lack of faith: '{path}' exists only in your imagination. Even 47 can't save you now.")
    sys.exit(1)

with open(path) as f:
    execute(f.read())
