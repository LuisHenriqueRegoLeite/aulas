from tipos import Ast, Erro, monadic_error, Stream
from lexer import tokenizador
from parser import parser

# tabela de operações da linguagem
OPERACAO = {
    "+": lambda *args: sum(args),
    "*": lambda a, b: a * b,
    "-": lambda *args: -args[0] if len(args) == 1 else args[0] - args[1],
    "/": lambda a, b: a / b,
    "?": lambda : int(input()),
    "**": lambda a, b: a ** b,
}

# analisador semântico
@monadic_error
def eval(ast: Ast) -> int | float | Erro:
    if isinstance(ast, int):
        return ast

    # argumentos
    args = [eval(e) for e in ast[1:]]
    for erro in args:
        if isinstance(erro, Erro):
            return erro

    # operação
    operador = str(ast[0])
    operacao = OPERACAO[operador]
    try:
        significado = operacao(*args)
    except ZeroDivisionError:
        return Erro("RUNTIME: divisão por zero")
    return significado


def main():
    programa = input("calc? ")

    tokens = tokenizador(programa)
    ast = parser(tokens)
    significado = eval(ast)

    print(f"{programa}   -->   {significado}")


if __name__ == "__main__":
    main()

