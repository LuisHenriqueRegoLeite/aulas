from tipos import Erro
from calc import eval

# + variádico
assert eval(["+", 1, 2, 3, 4]) == 10
assert eval(["+", 5]) == 5
assert eval(["+"]) == 0

# - unário
assert eval(["-", 1]) == -1

#########
# abaixo os testes originais

# literais
assert eval(0) == 0
assert eval(42) == 42

# aritmética básica
assert eval(["+", 1, 2]) == 3
assert eval(["-", 5, 3]) == 2
assert eval(["*", 4, 3]) == 12
assert eval(["/", 10, 2]) == 5

# subexpressões
assert eval(["+", 1, ["*", 2, 3]]) == 7
assert eval(["*", ["+", 1, 2], ["+", 3, 4]]) == 21
assert eval(["-", ["+", 5, 5], ["/", 8, 4]]) == 8

# divisão por zero
assert eval(["/", 1, 0]) == Erro("RUNTIME: divisão por zero")
assert eval(["+", 1, ["/", 1, 0]]) == Erro("RUNTIME: divisão por zero")

print("Todos os testes passaram!")
