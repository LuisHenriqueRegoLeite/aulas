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


## 7. Da Semântica Formal à Implementação

A estrutura das regras de avaliação espelha diretamente a implementação do
interpretador em Python. Cada regra corresponde a um ramo da função `avalia`:

| Regra Formal      | Ramo na implementação |
|-------------------|----------------------|
| `(Num)`           | `if isinstance(ast, int): return ast` |
| `(Op)`            | `elif ast[0] == 'op': v1 = avalia(ast[1], env); v2 = avalia(ast[2], env); return apply_op(ast[0], v1, v2)` |
| `(DivZero)`       | tratado dentro de `apply_op` |
| `(ErrEsq/ErrDir)` | propagação automática via exceções ou valores `erro` |


A correspondência entre as regras formais e o código é **intencional** aqui. A
ideia é que você veja que a formalização não é um exercício abstrato, mas uma
**especificação executável** do comportamento do interpretador, tal como foi o
caso da sintaxe em relação ao parser.

## 8. Nossa próxima Linguagem: calc com variáveis

(`aljabr`?)

Ideia de sintaxe: `let` para expressões puras com vinculação.

Na próxima mini-linguagem do curso, estenderemos `calc-v2` com **variáveis**,
mantendo a natureza **puramente expressiva** da linguagem: não há atribuições
(no sentido estrito), sequenciamento, laços nem efeitos colaterais. A única
forma de introduzir nomes é através de vinculações (_bindings_):

```
let x = <exp> in <exp>
```

Isto é, vinculamos um nome `x` a uma expressão `e1` e usamos esse nome no corpo
`e2`. O resultado da expressão inteira é o resultado de `e2`.


### 8.1 Sintaxe Abstrata Estendida

A gramática de `calc-v2` ganha duas produções:

```
e ::= n                      (número inteiro)
    | x                      (identificador)        ← NOVO
    | let x = e1 in e2       (vinculação local)     ← NOVO
    | e1 + e2                (soma)
    | e1 - e2                (subtração)
    | e1 * e2                (multiplicação)
    | e1 / e2                (divisão inteira)
    | (e)                    (parênteses — não aparece na AST)
```


### 8.2 Ambiente Não-Vazio

Diferente de `calc-v2`, o ambiente `ρ` deixa de ser irrelevante. Agora:

- `ρ` é uma função parcial de variáveis para valores;
- `ρ(x)` denota o valor associado a `x`, se existir;
- `ρ[x ↦ v]` denota o ambiente `ρ` **estendido** (ou sobrescrito) com a associação `x ↦ v`. Formalmente:

$$
\rho[x \mapsto v](y) =
\begin{cases}
v & \text{se } y = x \\
\rho(y) & \text{caso contrário}
\end{cases}
$$

Na implementação, `ρ` pode ser modelado como um dicionário Python (ou lista de
dicionários, para escopos aninhados). A operação `ρ[x ↦ v]` corresponde a uma
**cópia estendida** do dicionário — sem mutação do ambiente original,
preservando a semântica funcional.

### 8.3 Novas Regras de Avaliação

#### Variável

$$
\frac{\rho(x) = v}{\langle x, \rho \rangle \Downarrow v} \quad \text{(Var)}
$$

Se o ambiente associa `x` a `v`, então `x` avalia para `v`.

#### Variável Não Vinculada (Erro)

$$
\frac{x \notin \mathrm{dom}(\rho)}{\langle x, \rho \rangle \Downarrow \mathbf{erro}} \quad \text{(VarNaoLigada)}
$$

Se `x` não está no domínio de `ρ`, a avaliação resulta em `erro`. Isso
generaliza o tratamento de erro já presente em `calc-v2`.

#### Vinculação Local (`let`)

$$
\frac{
  \langle e_1, \rho \rangle \Downarrow v_1 \qquad
  \langle e_2, \rho[x \mapsto v_1] \rangle \Downarrow v_2
}{
  \langle \text{let } x = e_1 \text{ in } e_2, \rho \rangle \Downarrow v_2
} \quad \text{(Let)}
$$

Para avaliar `let x = e1 in e2`:

1. avaliamos `e1` no ambiente **corrente** `ρ`, obtendo `v1`;
2. avaliamos `e2` no ambiente **estendido** `ρ[x ↦ v1]`, obtendo `v2`;
3. o resultado é `v2`.

Observe que:

- o ambiente `ρ` **não é modificado**: `ρ[x ↦ v1]` é uma nova função;
- `e1` é avaliado **antes** de `x` ser vinculado — portanto `x` **não** está em
escopo dentro de `e1` (o `let` **não é recursivo**);
- o escopo de `x` é **estritamente** o corpo `e2`.

### 8.4 Escopo Léxico e Sombreamento (Shadowing)

Como `ρ[x ↦ v]` **sobrescreve** a associação de `x` quando ela já existe, a
nova associação **esconde** a antiga dentro do corpo. Considere:

```
let x = 1 in (let x = 2 in x) + x
```

- A ocorrência de `x` no `let` interno refere-se ao valor `2`;
- A ocorrência de `x` fora do `let` interno (mas dentro do `let` externo) refere-se ao valor `1`;
- Resultado: `2 + 1 = 3`.

Este comportamento corresponde ao **escopo léxico** (também dito estático), no
qual cada ocorrência de uma variável é resolvida pelo `let` mais próximo
**sintaticamente** que a vincula.

### 8.5 Exemplo de Derivação

Considere `let x = 2 + 3 in x * x` com ambiente inicial `ρ = ∅`.

1. `⟨2, ρ⟩ ⇓ 2` (Num)
2. `⟨3, ρ⟩ ⇓ 3` (Num)
3. `⟨2 + 3, ρ⟩ ⇓ 5` (Op, 1–2)
4. `⟨x, ρ[x ↦ 5]⟩ ⇓ 5` (Var, pois `ρ[x ↦ 5](x) = 5`)
5. `⟨x, ρ[x ↦ 5]⟩ ⇓ 5` (Var)
6. `⟨x * x, ρ[x ↦ 5]⟩ ⇓ 25` (Op, 4–5)
7. `⟨let x = 2 + 3 in x * x, ρ⟩ ⇓ 25` (Let, 3 e 6)

**Conclusão:** `⟨let x = 2 + 3 in x * x, ∅⟩ ⇓ 25`.

### 8.6 Exemplo com Sombreamento

Considere `let x = 1 in (let x = 2 in x) + x` com `ρ = ∅`.

1. `⟨1, ρ⟩ ⇓ 1` (Num)
2. `⟨2, ρ[x ↦ 1]⟩ ⇓ 2` (Num)
3. `⟨x, ρ[x ↦ 1][x ↦ 2]⟩ ⇓ 2` (Var) — note que `ρ[x ↦ 1][x ↦ 2] = ρ[x ↦ 2]`
4. `⟨let x = 2 in x, ρ[x ↦ 1]⟩ ⇓ 2` (Let, 2–3)
5. `⟨x, ρ[x ↦ 1]⟩ ⇓ 1` (Var)
6. `⟨(let x = 2 in x) + x, ρ[x ↦ 1]⟩ ⇓ 3` (Op, 4–5)
7. `⟨let x = 1 in (let x = 2 in x) + x, ρ⟩ ⇓ 3` (Let, 1 e 6)

**Conclusão:** `⟨let x = 1 in (let x = 2 in x) + x, ∅⟩ ⇓ 3`.

### 8.7 Exemplo com Variável Livre

Considere `let x = 1 in x + y` com `ρ = ∅`.

1. `⟨1, ρ⟩ ⇓ 1` (Num)
2. `⟨x, ρ[x ↦ 1]⟩ ⇓ 1` (Var)
3. `y ∉ dom(ρ[x ↦ 1])` — a variável `y` é livre
4. `⟨y, ρ[x ↦ 1]⟩ ⇓ erro` (VarNaoLigada)
5. `⟨x + y, ρ[x ↦ 1]⟩ ⇓ erro` (ErrDir)
6. `⟨let x = 1 in x + y, ρ⟩ ⇓ erro` (Let, 1 e 5)

**Conclusão:** `⟨let x = 1 in x + y, ∅⟩ ⇓ erro`.

### 8.8 Pureza e Ausência de Efeitos

Apesar da introdução de variáveis, a linguagem **permanece puramente expressiva**:

- não há comandos de atribuição (`x := e`);
- não há sequenciamento (`e1; e2`);
- não há laços nem condicionais nesta versão;
- a única forma de alterar o ambiente é o `let`, que produz um **novo** ambiente — sem mutação.

Isso preserva a **composicionalidade** da semântica: o valor de `let x = e1 in
e2` depende apenas do valor de `e1` e do valor de `e2` no ambiente estendido.
Também preserva o **determinismo**: a semântica continua sendo uma função
parcial de expressões (e ambientes) para valores.

### 8.9 Propriedades Atualizadas

- **Determinismo:** mantém-se. Para toda expressão `e` e todo ambiente `ρ`,
existe no máximo um `v` tal que `⟨e, ρ⟩ ⇓ v`.
- **Composicionalidade:** mantém-se. O valor de uma expressão é função dos
valores de suas subexpressões imediatas (e do ambiente, para as variáveis).
- **Ambiente agora relevante:** o valor de uma expressão passa a depender de
`ρ` sempre que houver variáveis livres. `calc-v2` era o caso degenerado em que
`ρ` era irrelevante.
- **Ausência de recursão:** o `let` é **não-recursivo** (`let x = e1 in e2`):
`x` **não** está em escopo dentro de `e1`. Isso reflete a ordem de avaliação:
`e1` é avaliado **antes** da vinculação.

---

## 9. Resumo

| Aspecto                            | `calc-v2`                               | `aljabr` |
|------------------------------------|-----------------------------------------|----------------------------|
| **Sintaxe**                        | Números, `+`, `-`, `*`, `/`, parênteses | + `x`, `let x = e1 in e2` |
| **Forma do julgamento**            | `⟨e, ρ⟩ ⇓ v`                            | `⟨e, ρ⟩ ⇓ v` |
| **Ambiente**                       | Vazio (sem variáveis)                   | Não-vazio; funções parciais estendidas por `let` |
| **Estilo de semântica**            | Big-step                                | Big-step |
| **Determinismo**                   | Sim                                     | Sim |
| **Propagação de erro**             | Sim (divisão por zero)                  | Sim (divisão por zero + variável não vinculada) |
| **Efeitos colaterais**             | Nenhum                                  | Nenhum (mantém-se puramente expressiva) |
| **Novas regras**                   | —                                       | `(Var)`, `(VarNaoLigada)`, `(Let)` |

---

## 10. Referências

- Plano de curso PLP/UFCG — Estágios 1–3 e ciclo pedagógico de cada estágio.
- Aula 06 — Gramática de `calc-v2`, precedência, associatividade e parsers
recursivos descendentes.
- Material de semântica operacional big-step (semântica natural), baseado na
formulação de Gilles Kahn.
- Implementação de referência: `calc-v2/` no repositório da disciplina.
- Nielson & Nielson, *Semantics with Applications: A Formal Introduction* —
capítulo sobre semântica natural, para o tratamento de `let` e ambientes.
