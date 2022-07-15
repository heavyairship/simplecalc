import pdb
import traceback

# simplecalc grammar**:
#
# expr ->
# | n
# | expr + expr
# | expr - expr
# | expr * expr
# | expr / expr
# | expr % expr
# | (expr)
# | -expr
#
# **note that all operations (including negation!) are right-associative and of equal precedence

ADD = "+"
SUB = "-"
MUL = "*"
DIV = "/"
MOD = "%"
OPS = [ADD, SUB, MUL, DIV, MOD]
LPAREN = "("
RPAREN = ")"

def number(s):
    i = 0
    while i < len(s) and (s[i].isdigit() or s[i] in [".", "e"]):
        i += 1
    return s[0:i], i

def tokenize(raw_expr):
    tokens = []
    i = 0
    while i < len(raw_expr):
        c = raw_expr[i]
        if c.isspace():
            i += 1
        elif c.isdigit():
            d, n = number(raw_expr[i:])
            tokens.append(d)
            i += n
        elif c in OPS:
            tokens.append(c)
            i += 1
        elif c == LPAREN:
            tokens.append(LPAREN)
            i += 1
        elif c == RPAREN:
            tokens.append(RPAREN)
            i += 1
        else:
            raise ValueError(f"tokenization error on character {c} at index {i} in input {raw_expr}")
    return tokens

class Node:
    def __init__(self):
        raise ValueError("abstract class `Node` cannot be instantiated")
    def evaluate(self):
        pass

class Neg(Node):
    def __init__(self, n):
        self.n = n
    
    def evaluate(self):
        return -1 * self.n.evaluate()

class Number(Node):
    def __init__(self, v):
        self.v = v

    def evaluate(self):
        return self.v

class Add(Node):
    def __init__(self, l, r):
        self.l = l
        self.r = r

    def evaluate(self):
        return self.l.evaluate() + self.r.evaluate()

class Sub(Node):
    def __init__(self, l, r):
        self.l = l
        self.r = r

    def evaluate(self):
        return self.l.evaluate() - self.r.evaluate()

class Mul(Node):
    def __init__(self, l, r):
        self.l = l
        self.r = r

    def evaluate(self):
        return self.l.evaluate() * self.r.evaluate()

class Div(Node):
    def __init__(self, l, r):
        self.l = l
        self.r = r

    def evaluate(self):
        return self.l.evaluate() / self.r.evaluate()

class Mod(Node):
    def __init__(self, l, r):
        self.l = l
        self.r = r

    def evaluate(self):
        return self.l.evaluate() % self.r.evaluate()

def get_op(op):
    if op == ADD:
        return Add
    if op == SUB:
        return Sub
    if op == MUL:
        return Mul
    if op == DIV:
        return Div
    if op == MOD:
        return Mod

def peek(tokens):
    if tokens == []:
        return None
    return tokens[0]

def pop(tokens):
    return tokens.pop(0)

def is_number(t):
    try:
        float(t)
    except ValueError:
        return False
    return True

def parse_expr(tokens):
    if tokens == []:
        raise ValueError("empty expression not allowed!")
    elif peek(tokens) == SUB:
        pop(tokens)
        expr = Neg(parse_expr(tokens))
    elif is_number(peek(tokens)):
        expr = Number(float(pop(tokens)))
    elif peek(tokens) == LPAREN:
        pop(tokens)
        expr = parse_expr(tokens)
        if peek(tokens) != RPAREN:
            raise ValueError(f"expected but did not find `{RPAREN}`")
        pop(tokens)
    else:
        raise ValueError(f"unexpected token `{peek(tokens)}`")
    if peek(tokens) in OPS:
        op = get_op(pop(tokens))
        return op(expr, parse_expr(tokens))
    return expr

def parse(tokens):
    expr = parse_expr(tokens)
    if len(tokens) > 0:
        raise ValueError(f"expected end of input but found token `{tokens[0]}`")
    return expr

def evaluate(parse_tree):
    return parse_tree.evaluate()

while True:
    try:
        print(evaluate(parse(tokenize(input("> ")))))
    except KeyboardInterrupt:
        break
    except EOFError:
        break
    except:
        traceback.print_exc()