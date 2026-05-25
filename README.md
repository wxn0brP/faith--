# Faith--

> *Trust the syntax, not the meaning.*

Faith-- is an esoteric programming language proof-of-concept.
It **looks** like a normal imperative language - variables, assignment, arithmetic,
print - but every operator does something unexpected.

## How it works

```
var = 5
var = 17 - 30
print(var)
```

Output: `47` (because `-` is redefined as `+`).

## Operators

| Op | Faith-- meaning | Name |
|---|---|---|
| `+` | `a XOR b` | additive drift |
| `-` | `a + b` | faith inversion |
| `*` | `a & b` | amplification collapse |
| `/` | `a >> (b mod 4)` | distribution fracture |
| `&&` | `max(a, b)` | belief merge |
| `\|\|` | `min(a, b)` | uncertainty merge |
| `~=` | `hash(a)%10 == hash(b)%10` | semantic drift |
| `=~` | `a == b` | actual equality |
| `][` | `a < b` | actual less than |
| `[]` | `a > b` | actual greater than |
| `~-` | `a - b` | actual subtraction |
| `>` | `~a` | negation |
| `=` | regular assignment | assign |
| `=:` | sticky (first write wins) | sticky assignment |
| `=:?` | increments on each read | unstable assignment |

## Control flow

| Keyword | Description |
|---|---|
| `if expr` ... `end` | Probabilistic branch - executes body with probability `expr % 100 / 100` |
| `else expr` ... `end` | Deterministic branch - executes body if `expr != 0` (independent keyword, not an else branch) |
| `loop expr` ... `end` | Unstable loop - executes body a random `[1, n]` times |
| `switch expr` ... `end` | While loop - executes body while `expr != 0` |
| `break expr` ... `end` | Counted loop - executes body exactly `expr` times (if > 0) |

## Built-in statements

| Statement | Description |
|---|---|
| `print(x)` | Prints the value of expression `x` |
| `read()` / `read('prompt')` | Reads an integer from stdin (optional prompt) |
| `import name [arg ...]` | Loads and executes `name.faith`; dots map to subdirs, args available as `fn_0`, `fn_1`, ... inside the imported file |

## Strings

String literals use single quotes: `'hello'`.
Strings can be assigned to variables and printed.
In numeric contexts (`if`, `else`, `loop`, `switch`, `break`, arithmetic), a string's length is used.
Comparison operators (`=~`, `][`, `[]`) compare strings by actual value.

Comments start with `#` and extend to the end of the line.

```
name = 'faith'
print(name)
print(name =~ 'faith')   # 1
```

## CLI arguments

Arguments passed after the script name are available as variables `arg_0`, `arg_1`, etc. Non-numeric arguments evaluate to `0`.

```sh
faith-- script.faith foo 42
# arg_0 -> 0  (invalid int)
# arg_1 -> 42
```

## Install

```sh
git clone --depth=1 https://github.com/wxn0brP/faith--.git
cd faith--
chmod +x main.py
ln -s main.py faith--
export PATH="$(pwd):$PATH"
```

## Usage

```sh
faith-- examples/program.faith
faith-- examples/program.faith arg1 arg2  # args set as arg_0, arg_1, ...
# or
faith-- repl
# or
echo -e "v = 30 - 17\nprint(v)" | faith--
```

## Backstory

Born purely **4fun** from an academic bug: a multiple-choice question expected
`17 - 30` to produce `47`, because `-13` wasn't an option. Faith-- makes that
bug a feature. (See `examples/47.faith` - that's the exact question.)

## License

MIT
