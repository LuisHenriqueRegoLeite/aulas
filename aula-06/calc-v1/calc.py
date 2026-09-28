from collections.abc import Iterator

import re

from tipos import Ast, Erro, monadic_error, Stream

# tabela de operações da linguagem
OPERACAO = {
    "+": lambda *args: sum(args),
    "*": lambda a, b: a * b,
    "-": lambda *args: -args[0] if len(args) == 1 else args[0] - args[1],
    "/": lambda a, b: a / b,
    "?": lambda : int(input()),
    "**": lambda a, b: a ** b,
}

# lexer
OPERADORES = set(OPERACAO.keys())
OPERADORES_STR = ''.join(sorted(OPERADORES, key=lambda c: c == '-'))  # '-' no fim
OPERADOR = lambda tok: tok and re.fullmatch(rf"[{OPERADORES_STR}]", tok)

LPAREN = lambda tok: tok == "("
RPAREN = lambda tok: tok == ")"
INTEIRO = lambda tok: tok and re.fullmatch(r"[0-9]+", tok) is not None
OPS_ADIT = lambda tok: tok in {"+", "-"}
OPS_MULT = lambda tok: tok in {"*", "/"}

def preprocessa(linha: str) -> str:
    linha = linha.replace("(", " ( ")
    linha = linha.replace(")", " ) ")
    linha = linha.replace("+", " + ")
    linha = linha.replace("-", " - ")
    #linha = linha.replace("*", " * ")
    linha = linha.replace("**", " ** ")
    return linha


def tokenizador(programa: str) -> list[str] | Erro:
    tokens = preprocessa(programa).split()
    for tok in tokens:
        if not(tok.isdigit() or tok in OPERADORES or tok in '()'):
            return Erro(f"erro léxico: token desconhecido {tok}")
    return tokens


# parser
@monadic_error
def parser(tokens: list[str]) -> Ast | Erro:
    stream = Stream(tokens)
    erro = ast = parse_exp(stream)

    if isinstance(erro, Erro):
        return erro

    # se ainda há tokens no stream, é erro
    if stream.peek() is not None:
        return Erro("sintaxe: tokens depois da s-expressão")

    return ast


@monadic_error
def parse_exp(stream: Stream) -> Ast | Erro:
    """exp ::= termo { ( + | - ) termo }"""
    termo = parse_termo(stream)
    while OPS_ADIT(stream.peek()):
        op = stream.next()           # lê o operador
        termo2 = parse_termo(stream) # lê um novo termo
        termo = [op, termo, termo2]  # faz folding à esquerda

    return termo


@monadic_error
def parse_termo(stream: Stream) -> Ast | Erro:
   """termo ::= fator { ( * | / ) fator }"""
   fator = parse_fator(stream)
   while OPS_MULT(stream.peek()):
      op = stream.next()           # lê o operador
      fator2 = parse_fator(stream) # lê um fator
      fator = [op, fator, fator2]  # faz o folding à esquerda

   return fator


@monadic_error
def parse_fator(stream: Stream) -> Ast | Erro:
   """fator  ::= atomo [ ** fator ]"""

   atomo = parse_atomo(stream)  # parte em comum pras duas produções

   if stream.peek() != "**":  # look-ahead de 1
      return atomo

   stream.next()                # era um `**`, então descarta
   fator = parse_fator(stream)  # chama a função recursivamente
   return ["**", atomo, fator]  # monta o nó da AST


@monadic_error
def parse_atomo(stream: Stream) -> Ast | Erro:
   """atomo ::= INTEIRO | ( exp )"""

   if INTEIRO(stream.peek()):   # look-ahead de 1 pra decidir a produção
      return int(stream.next()) # era INTEIRO, aplica produção 1

   stream.next()            # o primeiro não era inteiro, deve ser LPAREN
   exp = parse_exp(stream)  # recorre à função para exp
   stream.next()            # descarta o RPAREN pra concluir

   return exp       # retorna só o que interessa


# analisador semântico
@monadic_error
def interpretador(ast: Ast) -> int | float | Erro:
    if isinstance(ast, int):
        return ast

    # argumentos
    args = [interpretador(e) for e in ast[1:]]
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
    programa = input("mlisp? ")

    tokens = tokenizador(programa)
    ast = parser(tokens)
    significado = interpretador(ast)

    print(f"{programa}   -->   {significado}")


if __name__ == "__main__":
    main()
