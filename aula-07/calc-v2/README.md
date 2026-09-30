# Especificação da Sintaxe de `calc`

## Sintaxe

### Conceitual, idealizada

```python
exp    ::= exp + termo | exp - termo | termo
termo  ::= termo * fator | termo / fator | fator
fator  ::= atomo ** fator | atomo
atomo  ::= INTEIRO | ( exp )
```

### EBNF efetiva usada

```python
exp     ::= termo { ( + | - ) termo }
termo   ::= fator { ( * | / ) fator }
fator   ::= atomo [ ** fator ]
atomo   ::= INTEIRO | ( exp )
```

### AST

- precedência de operadores: `**` > `*`, `/` > `+`, `-`
- os operadores `+`, `-`, `*` e `/` são associativos à esquerda
- o operador `**` é associativo à direita

Como optamos por uma gramática em EBNF e uma implementação de referência com um
parser descendente recursivo, precisamos fazer nossa gramática ser LL(1) e,
portanto, sem recursões à esquerda. Apesar disso, a linguagem exige as
associatividades acima indicadas.


## Semântica

Aqui… estamos na dívida.
