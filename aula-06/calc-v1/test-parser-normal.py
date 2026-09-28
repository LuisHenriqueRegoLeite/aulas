import sys
from calc import parser

# expressão simples: + 1 2 -> ['+', 1, 2]
resultado = parser(["1", "+", "2"])
assert resultado == ["+", 1, 2], f"esperava ['+', 1, 2], obtive {resultado!r}"

# expressão aninhada: 1 + 2 * 3 -> ['+', 1, ['*', 2, 3]]
resultado = parser("1 + 2 * 3".split())
assert resultado == ["+", 1, ["*", 2, 3]]

# aninhamento de operandos: (* (+ 1 2) (- 3 4))
exp = " ( 1 + 2 ) * ( 3 - 4 )".split()
resultado = parser(exp)
assert resultado == ["*", ["+", 1, 2], ["-", 3, 4]]

# associatividade de subtração
exp = "2 - 3 - 2".split()
resultado = parser(exp)
assert resultado == ['-', ['-', 2, 3], 2]

# associatividade de subtração trocada por parênteses
exp = "2 - ( 3 - 2 )".split()
resultado = parser(exp)
assert resultado == ['-', 2, ['-', 3, 2]]

# associatividade de divisão
exp = "8 / 2 / 4".split()
resultado = parser(exp)
assert resultado == ['/', ['/', 8, 2], 4]

# associatividade de subtração trocada por parênteses
exp = "8 / ( 2 / 4 )".split()
resultado = parser(exp)
assert resultado == ['/', 8, ['/', 2, 4]]

# associatividade da exponenciação
exp = "2 ** 3 ** 2".split()
resultado = parser(exp)
assert resultado == ['**', 2, ['**', 3, 2]]

# associatividade de subtração trocada por parênteses
exp = "( 2 ** 3 ) ** 2".split()
resultado = parser(exp)
assert resultado == ['**', ['**', 2, 3], 2]

print("Todos os testes NORMAIS passaram!")
