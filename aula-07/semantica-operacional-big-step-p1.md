## Como a formalização da semântica foi apresentada

Como a sintaxe e a semântica podem ser descritas com precisão, usando a notação
formal apropriada?

O plano também menciona explicitamente que a semântica de avaliação será
expressa na forma **`⟨e, ρ⟩ ⇓ v`** ("a expressão `e`, sob o ambiente `ρ`,
avalia para o valor `v`"), e que essa notação é a mesma forma de regra de
inferência já vista em lógica (dedução natural), agora aplicada a programas.

Nas notas de aula já publicadas, a formalização da semântica começa a ser
introduzida no contexto de **regras de transição** (semântica de passos
pequenos) para a linguagem RPN. A ideia de **ambiente** (`environment`) aparece
associada à introdução de variáveis: *"um ambiente associa nomes a valores;
avaliar uma variável significa consultar o ambiente corrente"*. Na
implementação de referência, o ambiente será representado como um dicionário
Python (ou lista de dicionários, para escopos aninhados).

O material que segue formaliza a semântica **big-step** (também chamada de
semântica natural ou de avaliação) para a `calc-v2`, preparando o caminho para
a linguagem com variáveis.


# Semântica Operacional Big-Step de `calc-v2`

Semântica natural da LP `calc-v2`, a versão da LP que calcula expressões com
notação infixa, precedência e associatividade já implementada em sala. A
formalização segue a notação `⟨e, ρ⟩ ⇓ v` e abre o caminho para a próxima
mini-linguagem do curso, que estenderá `calc` com **variáveis** e **ambiente**.


## 1. Sintaxe Abstrata

A sintaxe abstrata de `calc-v2` é dada pela seguinte gramática (em BNF):

```
e ::= n                      (número inteiro)
    | e1 + e2                (soma)
    | e1 - e2                (subtração)
    | e1 * e2                (multiplicação)
    | e1 / e2                (divisão inteira)
    | (e)                    (parênteses — não aparece na AST)
```

Lembrem que na AST (Abstract Syntax Tree), os parênteses não aparecem; a
estrutura da árvore já codifica a precedência e a associatividade, conforme
discutido nas aulas anteriores.


## 2. Domínios Semânticos

Definimos os domínios de valores e de resultados:

| Domínio            | Descrição |
|--------------------|-----------|
| `ℤ`                | Conjunto dos números inteiros |
| `Val = ℤ ∪ {erro}` | Valores possíveis: inteiros ou o valor especial `erro` |
| `Env = Var ⇀ Val`  | Ambiente: função parcial de variáveis para valores |


O **ambiente** `ρ` é uma função parcial que associa nomes de variáveis a
valores. Na próxima linguagem, `ρ` será construído com dicionários. Nesta
versão `calc-v2` (em que não temos variáveis) o ambiente está sempre vazio. A
ideia é apenas introduzir a nova forma de notação formal de semântica de forma
gradual.

> **Nota:** `Var` é o conjunto (infinito) de identificadores válidos da linguagem.


## 3. Forma do Julgamento

A semântica é expressa por meio de um **julgamento de avaliação**:

$$
\[
\langle e, \rho \rangle \Downarrow v
\]
$$

Lê-se: *"a expressão `e`, sob o ambiente `ρ`, avalia para o valor `v`"*.

Este julgamento é definido **indutivamente** por um conjunto de **regras de
inferência** (regras de avaliação), cada uma com a forma:
 
$$
\[
\frac{\text{premissas}}{\text{conclusão}}
\]
$$

Se todas as premissas são deriváveis, a conclusão também é. A semântica
big-step caracteriza-se por **avaliar a expressão inteira em um único passo**,
produzindo diretamente o valor final.



## 4. Regras de Avaliação

### 4.1 Números

$$
\[
\frac{}{\langle n, \rho \rangle \Downarrow n} \quad \text{(Num)}
\]
$$

Um literal numérico avalia para si mesmo, independentemente do ambiente.


### 4.2 Operações Aritméticas

Para cada operador binário `op ∈ {+, -, *, /}`:

$$
\[
\frac{
  \langle e_1, \rho \rangle \Downarrow v_1 \qquad
  \langle e_2, \rho \rangle \Downarrow v_2 \qquad
  v_1 \text{ op } v_2 = v
}{
  \langle e_1 \text{ op } e_2, \rho \rangle \Downarrow v
} \quad \text{(Op)}
\]
$$

**Leitura:** para avaliar uma expressão `e1 op e2`, avaliamos primeiro `e1` no
ambiente `ρ`, obtendo `v1`; em seguida avaliamos `e2` no mesmo ambiente `ρ`,
obtendo `v2`; por fim, aplicamos a operação semântica correspondente a `v1` e
`v2`, produzindo `v`.

Note que **o ambiente não muda durante a avaliação** nesta versão: `calc-v2` é
uma linguagem puramente expressiva, sem atribuições ou vinculações. Note ainda
que a especificação formal dá uma visão recursiva para a interpretação (por
isso chamada de natural).


### 4.3 Divisão por Zero (Erro)

$$
\[
\frac{
  \langle e_1, \rho \rangle \Downarrow v_1 \qquad
  \langle e_2, \rho \rangle \Downarrow 0
}{
  \langle e_1 \text{ / } e_2, \rho \rangle \Downarrow \mathbf{erro}
} \quad \text{(DivZero)}
\]
$$

A divisão por zero é um caso especial que produz o valor `erro`, propagando-se
pela avaliação.


### 4.4 Propagação de Erro

Se uma subexpressão avalia para `erro`, o resultado da expressão inteira também
é `erro`:

$$
\[
\frac{
  \langle e_1, \rho \rangle \Downarrow \mathbf{erro}
}{
  \langle e_1 \text{ op } e_2, \rho \rangle \Downarrow \mathbf{erro}
} \quad \text{(ErrEsq)}
\qquad
\frac{
  \langle e_2, \rho \rangle \Downarrow \mathbf{erro}
}{
  \langle e_1 \text{ op } e_2, \rho \rangle \Downarrow \mathbf{erro}
} \quad \text{(ErrDir)}
\]
$$

Note o quanto essa especificação se assemelha ao esquema de erros monádico que
montamos para nossa implementação.


## 5. Exemplos de Derivação

### Exemplo 1: `2 + 3 * 4`

A AST correspondente é:

```
    +
   / \
  2   *
     / \
    3   4
```

**Derivação:**

1. `⟨2, ρ⟩ ⇓ 2` (Num)
2. `⟨3, ρ⟩ ⇓ 3` (Num)
3. `⟨4, ρ⟩ ⇓ 4` (Num)
4. `⟨3 * 4, ρ⟩ ⇓ 12` (Op, 2–3)
5. `⟨2 + (3 * 4), ρ⟩ ⇓ 14` (Op, 1 e 4)

**Conclusão:** `⟨2 + 3 * 4, ρ⟩ ⇓ 14`.

### Exemplo 2: `(2 + 3) * 4`

A AST correspondente é:

```
    *
   / \
  +   4
 / \
2   3
```

**Derivação:**

1. `⟨2, ρ⟩ ⇓ 2` (Num)
2. `⟨3, ρ⟩ ⇓ 3` (Num)
3. `⟨2 + 3, ρ⟩ ⇓ 5` (Op, 1–2)
4. `⟨4, ρ⟩ ⇓ 4` (Num)
5. `⟨(2 + 3) * 4, ρ⟩ ⇓ 20` (Op, 3–4)

**Conclusão:** `⟨(2 + 3) * 4, ρ⟩ ⇓ 20`.

Observe como é a estrutura da AST, e não a ordem textual, que determina a ordem
de avaliação.

### Exemplo 3: `10 / (5 - 5)`

1. `⟨10, ρ⟩ ⇓ 10` (Num)
2. `⟨5, ρ⟩ ⇓ 5` (Num)
3. `⟨5, ρ⟩ ⇓ 5` (Num)
4. `⟨5 - 5, ρ⟩ ⇓ 0` (Op, 2–3)
5. `⟨10 / (5 - 5), ρ⟩ ⇓ erro` (DivZero, 1 e 4)

**Conclusão:** `⟨10 / (5 - 5), ρ⟩ ⇓ erro`.


## 6. Propriedades da Semântica Big-Step

- **Determinismo:** para toda expressão `e` e todo ambiente `ρ`, se `⟨e, ρ⟩ ⇓
v₁` e `⟨e, ρ⟩ ⇓ v₂`, então `v₁ = v₂`. Isto é, a semântica é uma **função
parcial** de expressões para valores.

- **Composicionalidade:** o valor de uma expressão é determinado exclusivamente
pelos valores de suas subexpressões imediatas. Isso se reflete diretamente na
estrutura das regras de inferência.

- **Independência do ambiente:** em `calc-v2` (sem variáveis), o ambiente `ρ` é
irrelevante: o valor de qualquer expressão independe de `ρ`. Na próxima
linguagem, isso deixará de ser verdade.
