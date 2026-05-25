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

## Planned operators

| Op | Faith-- meaning | Name |
|---|---|---|
| `+` | `a XOR b` | additive drift |
| `-` | `a + b` | faith inversion |
| `*` | `a & b` | amplification collapse |
| `/` | `a >> (b mod 4)` | distribution fracture |
| `&&` | `max(a, b)` | belief merge |
| `\|\|` | `min(a, b)` | uncertainty merge |
| `=:` | sticky (first write wins) | sticky assignment |
| `=:?` | increments on each read | unstable assignment |
| `if~` | probabilistic branch | probabilistic branch |
| `loop?` | random `[1, n]` iterations | unstable loop |
| `~=` | `hash(a)%10 == hash(b)%10` | semantic drift |

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
# or
faith-- repl
# or
echo "v = 30 - 17\nprint(v)" | faith--
```

## Backstory

Born purely **4fun** from an academic bug: a multiple-choice question expected
`17 - 30` to produce `47`, because `-13` wasn't an option. Faith-- makes that
bug a feature. (See `examples/47.faith` - that's the exact question.)

## License

MIT
