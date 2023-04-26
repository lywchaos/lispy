from typing import List
from env import global_env

def eval(expression, env=global_env):
    if isinstance(expression, str):
        return env[expression]
    elif isinstance(expression, (int, float)):
        return expression
    elif expression[0] == "if":
        (_, test, conseq, alt) = expression
        exp = conseq if test else alt
        return eval(exp)
    elif expression[0] == "define":
        (_, symbol, exp) = expression
        env[symbol] = eval(exp, env)
    else:
        proc = eval(expression[0], env)
        args = [eval(arg, env) for arg in expression[1:]]
        return proc(*args)

def parse(program: str):
    return eval(grammer_analyse(lexical_analyse(program)))

def lexical_analyse(chars: str) -> List[str]:
    """Convert chars to Scheme tokens"""
    return chars.replace("(", " ( ").replace(")", " ) ").split()

def grammer_analyse(tokens: List[str]):
    """Conver Scheme tokens to Scheme AST represented in python List
    
    Return ast represented in List[List[str ....]], can be recursive
    """
    if len(tokens) == 0:
        raise SyntaxError("unexpected EOF")
    # L1 级的递归下降语法分析
    token = tokens.pop(0)
    if token == "(":
        L = []
        while tokens[0] != ")":
            L.append(grammer_analyse(tokens))
        tokens.pop(0)
        return L
    elif token == ")":
        raise SyntaxError("unexpected )")
    else:
        try:
            return int(token)
        except:
            try:
                return float(token)
            except:
                return token

if __name__ == "__main__":
    program = "(begin (define r 10) (* pi (* r r)))"
    parse(program)